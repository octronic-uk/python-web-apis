from flask import Flask, abort, request, jsonify, g, url_for
from flask_httpauth import HTTPBasicAuth

from octronic.webapis.user import Constants
from octronic.webapis.user import UserDB

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = Constants.secret_key

# extensions
auth = HTTPBasicAuth()
user_db = UserDB()

@auth.verify_password
def verify_password(username, password):
    # try to authenticate with username/password
    user = user_db.get_user_by_username(username)
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.route('/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)    # missing arguments
    if user_db.user_exists_by_username(username):
        abort(400)    # existing user
    user = user_db.create_user(username,password)
    user.hash_password(password)
    session_db.add(user)
    return (jsonify(
        {'username': user.username}), 201,
        {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/users/<id>')
def get_user(id):
    user = user_db.get_user_by_id(id)
    if not user:
        abort(400)
    return jsonify({
        'username': user.username
    })


@app.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})

if __name__ == '__main__':
    app.run(debug=True)
