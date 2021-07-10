import os
from flask import Flask
from models import DB


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'#have app know the database
    DB.init_app(app)#have database know about the app

    @app.route('/')
    def root():
        return 'Welcome to TwitOff!'

    return app