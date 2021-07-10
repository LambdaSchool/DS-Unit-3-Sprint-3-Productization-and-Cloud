from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    '''Twitter users that we pull and analyze tweets for'''
    id = DB.Column(DB.Integer, primary_key=True)#id column in User Table, what type, autogenerates
    name = DB.Column(DB.String(15), nullable=False)#name is required

class Tweet(DB.Model):
    '''Tweets'''
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280))#unicode supports emoji's and extended text