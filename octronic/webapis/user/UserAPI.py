from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
import json
from octronic.webapis.user.UserDB import UserDB
from octronic.webapis.session.SessionDB import SessionDB
from octronic.webapis.event.EventDB import EventDB
from octronic.webapis.common import Constants
from Crypto.PublicKey import RSA
import base64
import logging

log = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
user_db = UserDB()
session_db = SessionDB()
event_db = EventDB()
rsa_key = RSA.generate(Constants.rsa_key_length)


@auth.verify_password
def verify_password(username, password):
    log.debug("Verifying...\n--> User: %s\n--> Pass: %s",username,password)
    if password == Constants.token:
        token = username
        try:
            log.debug("Authenticating token %s",token)
            token_bytes=base64.b64decode(token)
            token_decrypted = rsa_key.decrypt(token_bytes)
            token_string = str(token_decrypted,encoding='utf-8')
            log.debug("Decrypted token to %s",token_string)
            session = session_db.get_session(session_id=token_string)
        except:
            log.error("Error decrypting token!")
            event = {"TokenError":str(request.remote_addr)}
            event_db.insert_event(None,None,event)
            return False

        if session is not None:
            log.debug("Found session %s",session)
            g.user = user_db.get_user(user_id=str(session.user))

            if g.user is not None:
                return True
            else:
                return False
        else:
            return False
    else:
        user = user_db.get_user(username=username)
        if not user or not user.verify_password(password):
            log.error("Unable to verify - User: %s Pass %s",username,password)
            return False
        g.user = user
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
            return jsonify({Constants.error : 'User Exists' })

        user = user_db.create_user(username=username,password=password)
        user.hash_password(password)
        user_db.update_user(user)
        session_db.create_session(user=user)

        return (
            jsonify(
                {
                'username': user.username
                }
            ), 201,
            {
                'Location': url_for('get_user', id=str(user.id) ,_external=True)
            }
        )
    else:
        log.error("request has not json")
        abort(400)


@app.route('/user/<id>')
def get_user(id):
    user = user_db.get_user(user_id=id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/user/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    log.info("get_auth_token for %s",g.user.id)

    existing_session = session_db.get_session(user_id=g.user.id)
    session = None

    if existing_session is not None:
        log.info("Found existing session %s",existing_session)
        if existing_session.has_expired():
            log.info("Session has expired %s, Removing session",existing_session)
            session_db.delete_session(session=existing_session)
            session = session_db.create_session(user=g.user)
        else:
            log.info("Found active session for %s",g.user.id)
            session = existing_session
    else:
        log.info("Creating new session for %s",g.user)
        session = session_db.create_session(user=g.user)

    if session is not None:
        log.debug("Returning session %s",session)
        signed_token = str(base64.b64encode(rsa_key.encrypt(str(session.id).encode(),None)[0]),encoding='ascii')
        log.debug("Signed token: %s",signed_token)
        return jsonify(
            {
                Constants.token : signed_token,
                Constants.expire_time : session.expire_time
            }
        )
    else:
        abort(400)


@app.route('/user/test_resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
