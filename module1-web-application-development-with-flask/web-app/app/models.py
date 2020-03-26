# Create some database models

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)