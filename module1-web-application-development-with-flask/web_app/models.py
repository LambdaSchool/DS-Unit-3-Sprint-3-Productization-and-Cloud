from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(128))
    user_id = db.Column(db.String(128))
    