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

class T_User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String)
    location = db.Column(db.String)
    followers_count = db.Column(db.Integer)
    latest_tweet_id = db.Column(db.BigInteger)

class T_Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger) # , db.ForeignKey("T_User.id")
    full_text = db.Column (db.String(500))
    embedding = db.Column(db.PickleType)