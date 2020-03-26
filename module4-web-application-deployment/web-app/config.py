from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """ Base configuration reading from .env file """

    DEBUG = os.environ.get("DEBUG")
    SECRETKEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_ADDRESS")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("TRACK_MOD")