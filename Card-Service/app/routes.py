import io
from urllib import response
from flask import Flask, request, jsonify, make_response, Response, send_from_directory
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from app import app, db
from app.models import Card
import requests

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/card/user/<user_id>', methods=['GET'])
def get_all_cards(user_id):

    app.logger.info('get_all_cards')
    cards = Card.query.filter_by(user_id=user_id).all()

    output = []

    for card in cards:
        card_data = {}
        card_data['id'] = card.id
        card_data['topic'] = card.topic
        card_data['question'] = card.question
        card_data['answer'] = card.answer
        card_data['timestamp'] = card.timestamp
        card_data['userId'] = card.user_id
        output.append(card_data)

    response = jsonify({'cards' : output})
    return response

@app.route('/card/data/user/<user_id>', methods=['GET'])
def cards_data(user_id):

    app.logger.info('cards_data')
    cards = Card.query.filter_by(user_id=user_id).all()
		
    output = []

    for card in cards:
        res = requests.get('http://127.0.0.1:5002/score/card/'+str(card.id))
        score = res.json()
        app.logger.info(score)
        output.append({'id': str(card.id), 'topic': str(card.topic), 'question': str(card.question), 'answer': str(card.answer), 'timestamp': str(card.timestamp), 'score': score['score'],'attempts': score['attempts']})
		
    return jsonify({'cards': output})

@app.route('/card/<card_id>', methods=['GET'])
def get_one_card(card_id):

    app.logger.info('get_one_card')
    card = Card.query.filter_by(id=card_id).first()

    if not card:
        app.logger.error('No card found!')
        return jsonify({'message' : 'No card found!'}), 404

    card_data = {}
    card_data['id'] = card.id
    card_data['topic'] = card.topic
    card_data['question'] = card.question
    card_data['answer'] = card.answer
    card_data['timestamp'] = card.timestamp
    card_data['userId'] = card.user_id

    response = jsonify(card_data)
    return response

@app.route('/card', methods=['POST'])
def create_card():

    app.logger.info('create_card')
    data = request.get_json()
    new_card = Card(topic=data['topic'], question=data['question'], answer=data['answer'], user_id=data['userId'])
    db.session.add(new_card)
    db.session.commit()
    res = requests.post('http://127.0.0.1:5002/score', json={'cardId': new_card.id,'userId':new_card.user_id})
    print(res)
    return jsonify({'message' : "Card created!"}), 201

@app.route('/card/<card_id>', methods=['PUT'])
def update_card(card_id):

    app.logger.info('update_card')
    data = request.get_json()
    card = Card.query.get(card_id)
    card.question = data["question"]
    card.answer = data["answer"]
    card.topic = data["topic"]
    
    db.session.commit()

    return jsonify({'message' : 'Card has been updated!'}), 202

@app.route('/card/<card_id>', methods=['DELETE'])
def delete_card(card_id):

    app.logger.info('delete_card')
    card = Card.query.filter_by(id=card_id).first()
    if not card:
        app.logger.error('No card found!')
        return jsonify({'message' : 'No card found!'}), 404

    db.session.delete(card)
    res = requests.delete('http://127.0.0.1:5002/score/card/'+ str(card_id))
    print(res)
    db.session.commit()

    return jsonify({'message' : 'Card deleted!'})