import io
import json
from urllib import response
from flask import Flask, request, jsonify, make_response, Response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
import csv
from functools import wraps
from app import app, db
from app.models import User
import requests

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            app.logger.error('Token is missing!')
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            app.logger.error('Token is invalid!')
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):

    app.logger.info('get_all_users')
    if not current_user.admin:
        app.logger.error('Cannot perform that function!')
        return jsonify({'message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    response = jsonify({'users' : output})
    return response

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    app.logger.info('get_one_user')
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'}), 404

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/admin', methods=['POST'])
def create_admin():

    app.logger.info('create_admin')
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'],  email=data['email'], name=data['name'], password=hashed_password, admin=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'Admin created!'}), 201

@app.route('/register', methods=['POST'])
def register_user():

    app.logger.info('register_user')
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'],  email=data['email'], name=data['name'],password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    response  = jsonify({'message' : 'New user created!'}), 201
    return response

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):

    app.logger.info('create_user')
    if not current_user.admin:
        app.logger.error('Cannot perform that function!')
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'],  email=data['email'], name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'}), 201

@app.route('/currentuser', methods=['GET'])
@token_required
def get_user(current_user):
    
    app.logger.info('get_user')
    user_data = {}
    user_data['id'] = current_user.id
    user_data['public_id'] = current_user.public_id
    user_data['username'] = current_user.username
    user_data['email'] = current_user.email
    user_data['name'] = current_user.name
    response = jsonify(user_data)
    return response

@app.route('/currentuser', methods=['PUT'])
@token_required
def update_user(current_user):

    app.logger.info('update_user')
    data = request.get_json()
    app.logger.info(data, current_user.public_id)

    user = User.query.filter_by(public_id=current_user.public_id).first()

    user.email = data["email"]
    user.name = data["name"]
    
    db.session.commit()

    response = jsonify({'message' : 'The user has been updated!'})
    return response, 202

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):

    app.logger.info('promote_user')
    if not current_user.admin:
        app.logger.error('Cannot perform that function!')
        return jsonify({'message' : 'Cannot perform that function!'}), 201

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        app.logger.error('No user found!')
        return jsonify({'message' : 'No user found!'}), 404

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'}), 202

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):

    app.logger.info('delete_user')
    if not current_user.admin:
        app.logger.error('Cannot perform that function!')
        return jsonify({'message' : 'Cannot perform that function!'}), 401

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        app.logger.error('No user found!')
        return jsonify({'message' : 'No user found!'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/login', methods=['POST'])
def login():

    app.logger.info('login')
    auth = request.authorization 
    username = auth.username
    password = auth.password
    response = None
    if not username or not password:
        app.logger.error('Could not verify, Incorrect username or password')
        response = make_response('Could not verify, Incorrect username or password', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=username).first()

    if not user:
        app.logger.error('Could not verify')
        response = make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=120)}, app.config['SECRET_KEY'])

        response = jsonify({'token' : token.decode('UTF-8')})

    return response

@app.route('/card', methods=['GET'])
@token_required
def get_all_cards(current_user):

    app.logger.info('get_all_cards')
    res = requests.get('http://127.0.0.1:5001/card/user/' + str(current_user.id))
    return res.json(), res.status_code

@app.route('/card/download', methods=['GET'])
@token_required
def downloads_cards(current_user):

    app.logger.info('downloads_cards')
    cards_res = requests.get('http://127.0.0.1:5001/card/data/user/' + str(current_user.id))
    app.logger.info(cards_res.json()['cards'])
    output = io.StringIO()
    writer = csv.writer(output)
		
    line = ['topic, question, answer, timestamp, score, attempts']
    writer.writerow(line)

    for card in cards_res.json()['cards']:
        line = [str(card['topic']) + ',' + str(card['question']) + ',' + str(card['answer']) + ','+ str(card['timestamp']) + ',' + str(card['score']) + ',' + str(card['attempts'])]
        writer.writerow(line)

    output.seek(0)
		
    return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=flash_card_report.csv"})

@app.route('/card/data', methods=['GET'])
@token_required
def cards_data(current_user):

    app.logger.info('cards_data')
    res = requests.get('http://127.0.0.1:5001/card/data/user/' + str(current_user.id))
    return res.json(), res.status_code

@app.route('/card/<card_id>', methods=['GET'])
@token_required
def get_one_card(current_user,card_id):

    app.logger.info('get_one_card')
    res = requests.get('http://127.0.0.1:5001/card/' + str(card_id))
    return res.json(), res.status_code

@app.route('/card', methods=['POST'])
@token_required
def create_card(current_user):

    app.logger.info('current_user')
    res = requests.post('http://127.0.0.1:5001/card', json=request.get_json())
    return res.json(), res.status_code

@app.route('/card/<card_id>', methods=['PUT'])
@token_required
def update_card(current_user, card_id):

    app.logger.info('update_card')
    res = requests.put('http://127.0.0.1:5001/card/' + str(card_id), json=request.get_json())
    return res.json(), res.status_code

@app.route('/card/<card_id>', methods=['DELETE'])
@token_required
def delete_card(current_user, card_id):

    app.logger.info('delete_card')
    res = requests.delete('http://127.0.0.1:5001/card/' + str(card_id))
    return res.json(), res.status_code

@app.route('/totalscore', methods=['GET'])
@token_required
def get_total_score(current_user):

    app.logger.info('get_total_score')
    res = requests.get('http://127.0.0.1:5002/totalscore/' + str(current_user.id))
    return res.json(), res.status_code

@app.route('/score/<card_id>', methods=['GET'])
@token_required
def get_score_of_card(card_id):

    app.logger.info('get_score_of_card')
    res = requests.get('http://127.0.0.1:5002/score/card/' + str(card_id))
    return res.json(), res.status_code

@app.route('/score/increment/<card_id>', methods=['PUT'])
@token_required
def increment_score(current_user, card_id):

    app.logger.info('increment_score')
    res = requests.put('http://127.0.0.1:5002/score/increment/' + str(card_id))
    return res.json(), res.status_code

@app.route('/attempts/increment/<card_id>', methods=['PUT'])
@token_required
def increment_attempts(current_user, card_id):

    app.logger.info('increment_attempts')
    res = requests.put('http://127.0.0.1:5002/attempts/increment/' + str(card_id))
    return res.json(), res.status_code

@app.route('/score/<card_id>', methods=['DELETE'])
@token_required
def delete_score(current_user, card_id):

    app.logger.info('delete_score')
    res = requests.delete('http://127.0.0.1:5002/score/card/' + str(card_id))
    return res.json(), res.status_code

@app.route('/score', methods=['DELETE'])
@token_required
def delete_all_score(current_user):

    app.logger.info('delete_all_score')
    res = requests.delete('http://127.0.0.1:5002/score/user/' + str(current_user.id))
    return res.json(), res.status_code