""" Database Models """

from flask_sqlalchemy import SQLAlchemy

# import database, capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users we analyze"""
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False) # max length allowed by twitter unames

    def __repr__(self):
        return f'<User {self.name}>'

class Tweet(DB.Model):
    """The user's tweets from twitter"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280)) # max tweet length allowed by twitter (280 chars)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User',backref=DB.backref('tweets',lazy=True))

    def __repr__(self):
        return f'<Tweet {self.text}>'



