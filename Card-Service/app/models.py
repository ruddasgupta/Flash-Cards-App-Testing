from datetime import datetime
from app import db

class Card(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   topic = db.Column(db.String(100))
   question = db.Column(db.String(100000))
   answer = db.Column(db.String(100000))
   timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
   user_id = db.Column(db.Integer)