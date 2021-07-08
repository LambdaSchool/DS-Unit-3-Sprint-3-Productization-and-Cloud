

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

migrate = Migrate()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.String(128))


# class User(db.Model):
#     # __table_name__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128))


# class Tweet(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     text = db.Column(db.String(500))


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String)
    location = db.Column(db.String)
    followers_count = db.Column(db.Integer)
    #latest_tweet_id = db.Column(db.BigInteger)


class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    full_text = db.Column(db.String(500))
    embedding = db.Column(db.PickleType)
    user = db.relationship("User", backref=db.backref("tweets", lazy=True))
