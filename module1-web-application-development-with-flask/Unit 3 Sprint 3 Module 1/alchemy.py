# Begin with import packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# Create user class
class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(15), nullable)
    
    # Shows name of user/helps with assignment/grabs info from user?
    def __repr__(self):
        return '<Users {}>'.format(self.name)

class Tweet(DB.Model):
    id: DB.Column(DB.Integer, primary_key)
    text = DB.Column(DB.Unicode(280))
    user_id = DB.Column(DB.integer, DB.ForeignKey('user.id'), nullable = False)
    user = DB.relationship('User', backref = DB.backref('tweets', lazy = True))
    
    # Lets us see the name of the user
    def __repr__(self):
        return '<Tweet {}.format(self.text)'