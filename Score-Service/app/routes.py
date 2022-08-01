import io
from urllib import response
from charset_normalizer import logging
from flask import Flask, request, jsonify, make_response, Response, send_from_directory
import uuid
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from app.models import Score

app.logger.setLevel(logging.INFO)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/totalscore/<user_id>', methods=['GET'])
def get_total_score(user_id):

    app.logger.info('get_total_score')
    scores = Score.query.filter_by(user_id=user_id).all()

    total_score = total_attempts = 0

    for score in scores:
        total_score += score.score
        total_attempts += score.attempts

    return jsonify({'total_score' : total_score, 'total_attempts': total_attempts})

@app.route('/score/card/<card_id>', methods=['GET'])
def get_score_of_card(card_id):

    app.logger.info('get_score_of_card')
    score = Score.query.filter_by(card_id=card_id).first()

    if not score:
        app.logger.error('No score found!')
        return jsonify({'message' : 'No card found!'}), 404

    
    return jsonify({"id" :score.id, "score": score.score, "attempts" :score.attempts, "timestamp" :score.timestamp, "cardId": score.card_id, "userId": score.user_id})

@app.route('/score', methods=['POST'])
def create_score():

    app.logger.info('create_score')    
    data = request.get_json()
    new_score = Score(score=0, attempts=0, card_id=data["cardId"], user_id=data["userId"])
    db.session.add(new_score)
    db.session.commit()

    return jsonify({"id" :new_score.id, "score": new_score.score, "attempts" :new_score.attempts, "timestamp" :new_score.timestamp, "cardId": new_score.card_id, "userId": new_score.user_id}), 201

@app.route('/score/increment/<card_id>', methods=['PUT'])
def increment_score(card_id):

    app.logger.info('increment_score') 
    score = Score.query.filter_by(card_id=card_id).first()

    if not score:
        app.logger.error('No score found!')
        return jsonify({'message' : 'No score found!'}), 404

    score.score += 1
    score.attempts += 1
    db.session.commit()

    return jsonify({'message' : 'Score/Attempts Incremented!'}), 202

@app.route('/attempts/increment/<card_id>', methods=['PUT'])
def increment_attempts(card_id):

    app.logger.info('increment_attempts') 
    score = Score.query.filter_by(card_id=card_id).first()

    if not score:
        app.logger.error('No score found!')
        return jsonify({'message' : 'No card found!'}), 404

    score.attempts += 1
    db.session.commit()

    return jsonify({'message' : 'Attempts Incremented!'}), 202

@app.route('/score/card/<card_id>', methods=['DELETE'])
def delete_score(card_id):

    app.logger.info('delete_score')
    score = Score.query.filter_by(card_id=card_id).first()

    if not score:
        app.logger.error('No score found!')
        return jsonify({'message' : 'No score found!'}), 404

    db.session.delete(score)
    db.session.commit()

    return jsonify({'message' : 'Score item deleted!'})

@app.route('/score/user/<user_id>', methods=['DELETE'])
def delete_all_score(user_id):

    app.logger.info('delete_all_score')
    scores = Score.query.filter_by(user_id=user_id).all()

    if not scores:
        app.logger.error('No score found!')
        return jsonify({'message' : 'No score found!'}), 404

    delete_q = Score.__table__.delete().where(Score.user_id == user_id)
    db.session.execute(delete_q)
    db.session.commit()

    return jsonify({'message' : 'Scores item deleted!'})