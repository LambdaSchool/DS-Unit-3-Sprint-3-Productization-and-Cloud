"""OpenAQ API file dashboard Flask skewl model thing for Sprint challenge"""

from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
api = openaq.OpenAQ()
DB = SQLAlchemy(APP)
status, body = api.measurements(city='Los Angeles', parameter='pm25')

@APP.route('/')
def root():
    """Base view."""
    return "body['results']['date']['utc'] if i ever figure out how"

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
return "Successfully recorded" + '<Record {}>'.format(self.id)
