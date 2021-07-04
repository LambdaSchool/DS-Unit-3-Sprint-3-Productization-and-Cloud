from flask import Flask
from .models import DB


def create_app():
    """Create and configure flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route("/")
    def hello():
        return "Welcome to Tweething!!"
    return app
