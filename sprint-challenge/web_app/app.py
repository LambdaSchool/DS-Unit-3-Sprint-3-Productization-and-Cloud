import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# Initialize the webapp with persistent services
def create_app():

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_DATABASE_TRACKING"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    return app
