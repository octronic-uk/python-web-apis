from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth
from octronic.webapis.user import Constants
from octronic.webapis.user.UserDB import UserDB
from octronic.webapis.session.SessionDB import SessionDB
from octronic.webapis.common import Constants as CommonConstants
import logging

log = logging.getLogger(__name__)
app = Flask(__name__)
auth = HTTPBasicAuth()
user_db = UserDB()
session_db = SessionDB()


@auth.verify_password
def verify_password(username, password):
    user = user_db.get_user(username=username)
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/user/create', methods=['POST'])
def create_user():
    username = request.json.get(CommonConstants.username)
    password = request.json.get(Constants.password)

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

    existing_session = session_db.get_sessions(user_id=g.user.id)
    session = None

    if existing_session is not None and len(existing_session) > 0:
        log.info("Found existing session %s",existing_session)
        for nextSession in existing_session:
            if not nextSession.has_expired():
                log.info("This session is still active")
                session = nextSession
                break
            else:
                log.info("Session has expired %s, Removing session",nextSession)
                session_db.delete_sessions(session=nextSession)
    else:
        log.info("Creating new session for %s",g.user)
        session = session_db.create_session(user=g.user)

    if session is not None:
        return jsonify({ 'token': str(session.id)  })
    else:
        abort(404)


@app.route('/user/test_resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


if __name__ == '__main__':
    app.run(debug=True)
