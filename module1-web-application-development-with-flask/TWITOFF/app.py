from flask import Flask
from .models import DB

# make an app factory

def create_app():
    app = Flask(__name__)

    # add our config
    # 3 slashes make this a relative path
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
 
    # now have the database know abot the app
    DB.init_app(app)

    @app.route('/')
    def root():
        return "Welcome to Twitoff"
    return app
