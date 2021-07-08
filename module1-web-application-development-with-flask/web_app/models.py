

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

migrate = Migrate()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.String(128))


class User(db.Model):
    # __table_name__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    text = db.Column(db.String(500))
