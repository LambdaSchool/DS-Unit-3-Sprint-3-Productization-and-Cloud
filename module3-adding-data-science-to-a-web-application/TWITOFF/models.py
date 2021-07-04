""" Database Models """

from flask_sqlalchemy import SQLAlchemy

# import database, capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users we analyze"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False) # max length allowed by twitter unames
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f'<User {self.name}>'

class Tweet(DB.Model):
    """The user's tweets from twitter"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(500)) # more than 280 chars is allowed for links
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User',backref=DB.backref('tweets',lazy=True))

    def __repr__(self):
        return f'<Tweet {self.text}>'



