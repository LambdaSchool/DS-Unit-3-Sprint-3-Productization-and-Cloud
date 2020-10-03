from flask_sqlalchemy import SQLAlchemy 
# get into flask shell  FLASK_APP=app:app flask shell

DB = SQLAlchemy()

class User(DB.Model):
    '''Defining a table using sql alchemy'''
    id = DB.Column(DB.Integer, primary_key = True)
    name = DB.Column(DB.String(15))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<User {}>'.format(self.name)

class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key = True)
    tweet = DB.Column(DB.String(15), nullable=False)
