"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
FLASK_ENV='development'
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'< Time {self.datetime} --- Value {self.value} >'


@APP.route('/')
def root():
    """Base view."""
    danger_zone = Record.query.filter(Record.value >= 10).all()
    return str(danger_zone)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    values = get_records()
    add_records(values)
    DB.session.commit()
    return 'Data refreshed!'


def get_records():
    # Set up the API object
    api = openaq.OpenAQ()
    _, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']
    values = []
    for result in results:
        values.append((result['date']['utc'], result['value'] ))
    return values


def add_records(values):
    for value in values:
        entry = Record()
        DB.session.add(entry)
        entry.datetime = value[0]
        entry.value = value[1]
        DB.session.commit()
