#
# UserAPI.py
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from flask import Flask, abort, request, jsonify, url_for, g
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from octronic.webapis.user.UserDB import UserDB
from octronic.webapis.event.EventDB import EventDB
from octronic.webapis.common import Constants
from octronic.webapis.common.SMTPMailer import SMTPMailer
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Random import random
import base64
import logging

# Constants
two_factor_min = 100000
two_factor_max = 999999

# Module Variables
log = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
user_db = UserDB()
event_db = EventDB()
rsa_key = RSA.generate(Constants.rsa_key_length)
rng = random
mailer = SMTPMailer(host='octronic.co.uk', port=Constants.smtp_port, sender="noreply@octronic.co.uk")

@auth.verify_password
def verify_password(username, password):
    if username_password_verification(username,password):
        return True
    else:
        if token_verification(username,password):
            return True
        else:
            return False


def token_verification(hash,signature):
    log.info("Authenticating hash/signature %s / %s",hash,signature)

    hash_bytes = base64.b64decode(hash)
    signature_bytes = base64.b64decode(signature)
    signature_string = str(signature_bytes,encoding='ascii')
    sig_int = int(signature_string)
    signature_verify_result = rsa_key.verify(hash_bytes,(sig_int,None))

    if signature_verify_result:
        uid_encrypted_b64 = request.headers.get('From')
        if uid_encrypted_b64 is not None:
            uid_encrypted_bytes = base64.b64decode(uid_encrypted_b64)
            uid_plain = rsa_key.decrypt(uid_encrypted_bytes)
            uid_plain_str = str(uid_plain,encoding='ascii')
            log.info("Authenticating user %s",uid_plain_str)
            g.user = user_db.get_user(user_id=uid_plain_str)
            return True
        else:
            return False
    else:
        return False


def username_password_verification(username,password):
    log.info("Authenticating user %s with username/password.",username)
    g.user = user_db.get_user(username=username)
    if not g.user or not g.user.verify_password(password):
        log.debug("Unable to verify - User: %s Pass %s",username,password)
        return False
    else:
        return True


@app.route('/user/create', methods=['POST'])
def create_user():
    if request.json is not None:
        username = request.json[Constants.username]
        password = request.json[Constants.password]

        # missing arguments
        if username is None:
            log.error("Cannot create user: username is missing")
            abort(400)

        if password is None:
            log.error("Cannot create user: password is missing")
            abort(400)

        # existing user
        if user_db.user_exists(username=username):
            log.error("Cannot create user. User %s all ready exists",username)
            abort(400)

        user = user_db.create_user(username=username,password=password)
        user.hash_password(password)
        user_db.update_user(user)

        return (jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=str(user.id) ,_external=True)})
    else:
        log.error("Request has no json body")
        abort(400)


@app.route('/user/<id>')
def get_user(id):
    g.user = user_db.get_user(user_id=id)
    if not g.user:
        abort(400)
    return jsonify({'username': g.user.username})


@app.route('/user/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    log.info("get_auth_token for %s",g.user.id)

    uid_str = str(g.user.id)
    uid_bytes = uid_str.encode()

    encrypted_uid = rsa_key.encrypt(uid_bytes,None)[0]
    encrypted_uid_b64 = base64.b64encode(encrypted_uid)
    encrypted_uid_b64_str = str(encrypted_uid_b64,encoding='ascii')

    uid_hash = SHA.new(encrypted_uid).hexdigest().encode()
    uid_hash_b64 = base64.b64encode(uid_hash)
    uid_hash_b64_str = str(uid_hash_b64,encoding='ascii')

    signed_uid_hash = str(rsa_key.sign(uid_hash,1)[0]).encode()
    signed_uid_hash_b64_str = str(base64.b64encode(signed_uid_hash),encoding='ascii')

    send_second_factor();

    log.info("Signed token: %s",signed_uid_hash_b64_str)
    return jsonify({
        Constants.user      : encrypted_uid_b64_str,
        Constants.hash      : uid_hash_b64_str,
        Constants.signature : signed_uid_hash_b64_str,
    })

def send_second_factor():
    if g.user is None:
        log.error("No user to send second factor to")
        return
    else:
        if g.user.email is None:
            log.error("User %s has no email address",g.user)
            return
        else:
            log.info("Sending second factor to %s",g.user.email)
            mailer.send(subject="Octronic: Your Two-Factor Pin",body=generate_second_factor(),to=g.user.email)
    return


def generate_second_factor():
    pin = str(random.randint(two_factor_min,two_factor_max))
    g.user.second_factor = pin
    user_db.update_user(g.user)
    return "Your two factor login pin is: " + pin


@app.route('/user/test_resource')
@auth.login_required
def get_resource():
    return jsonify({
        'data': 'Hello, %s!' % g.user.username
    })


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
