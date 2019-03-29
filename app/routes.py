from app import app
from flask import jsonify, request
from werkzeug.exceptions import HTTPException
import datetime
import jwt


@app.route('/user', methods=['GET'])
def user():
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return jsonify({'status': False, 'message': 'Unauthorized - Missing Auth Header'}), 401

    auth_token = auth_header.split(" ")[1]

    if not validate_token(auth_token):
        return jsonify({'status': False, 'message': 'Unauthorized'}), 401

    data = request.args
    if not data['email']:
        return jsonify({'status': False, 'message': 'Bad request parameters!'}), 400

    search_user = app.mongo.db.users.find_one({'email': data['email']})
    return jsonify(search_user), 200


@app.route('/user', methods=['POST'])
def create():
    data = request.get_json()

    if data.get('name', None) is not None or data.get('email', None) is not None \
            or data.get('password', None) is not None:

        search_user = app.mongo.db.users.find_one({'email': data['email']})

        if search_user:
            return jsonify({'status': False, 'message': 'User with email {} already exists!'.format(data['email'])}), 200

        data['password'] = app.flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
        data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data['token'] = '{}'.format(generate_token().decode('utf-8'))
        data['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        data['last_login'] = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        app.mongo.db.users.insert_one(data)
        del(data['password'])

        return jsonify({'status': True, 'message': 'User created successfully!', 'user': data}), 200
    else:
        return jsonify({'status': False, 'message': 'Bad request parameters!'}), 400


@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    if data.get('email', None) is None or data.get('password', None) is None:
        return jsonify({'status': False, 'message': 'Bad request parameters!'}), 400

    search_user = app.mongo.db.users.find_one({'email': data['email']})
    if search_user and app.flask_bcrypt.check_password_hash(search_user['password'], data['password']):

        if not validate_token(search_user['token']):
            token = '{}'.format(generate_token().decode('utf-8'))
            app.mongo.db.users.update_one(search_user, {"$set": {"token": token}})

        del(search_user['password'])
        return jsonify({'status': True, 'message': 'User created successfully!', 'user': search_user}), 200

    return jsonify({'status': True, 'message': 'Invalid user email and/or password'}), 200


@app.route('/api/v1.0/ping', methods=['GET'])
def ping_endpoint():
    return jsonify({'data': 'Server running'}), 200


@app.errorhandler(Exception)
def handle_error(e):
    print(e)
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

def generate_token():
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow(),
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

def validate_token(t):
    try:
        print('aaa')
        jwt.decode(t, app.secret_key)
        return True
    except jwt.ExpiredSignatureError:
        print('bbb')
        return False
    except jwt.InvalidTokenError:
        print('ccc')
        return False
