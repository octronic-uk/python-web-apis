from flask import Flask, abort, request, jsonify, url_for, g
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from octronic.webapis.user.UserDB import UserDB
from octronic.webapis.event.EventDB import EventDB
from octronic.webapis.common import Constants
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
import base64
import logging

# Module Variables
log = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
user_db = UserDB()
event_db = EventDB()
rsa_key = RSA.generate(Constants.rsa_key_length)


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
    log.debug("Authenticating hash/signature %s / %s",hash,signature)

    hash_bytes = base64.b64decode(hash)
    signature_bytes = base64.b64decode(signature)
    signature_string = str(signature_bytes,encoding='ascii')
    print(signature_string)
    sig_int = int(signature_string)
    signature_verify_result = rsa_key.verify(hash_bytes,(sig_int,None))

    if signature_verify_result:
        return True
    else:
        return False
    pass


def username_password_verification(username,password):
    log.debug("Authenticating user %s with username/password.",username)
    g.user = user_db.get_user(username=username)
    if not g.user or not g.user.verify_password(password):
        log.error("Unable to verify - User: %s Pass %s",username,password)
        return False
    else:
        return True
    pass


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
    uid_hash = SHA.new(uid_bytes).hexdigest().encode()
    uid_hash_b64 = base64.b64encode(uid_hash)
    uid_hash_b64_str = str(uid_hash_b64,encoding='ascii')
    print(uid_hash_b64_str)

    signed_uid_hash = str(rsa_key.sign(uid_hash,1)[0]).encode()
    signed_uid_hash_b64_str = str(base64.b64encode(signed_uid_hash),encoding='ascii')

    log.debug("Signed token: %s",signed_uid_hash_b64_str)
    return jsonify({
        Constants.hash : uid_hash_b64_str,
        Constants.token : signed_uid_hash_b64_str
    })


@app.route('/user/test_resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
