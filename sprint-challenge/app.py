"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import openaq

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['ENV'] = getenv('FLASK_ENV')
DB = SQLAlchemy(APP)
DB.init_app(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "date: {}, value: {}".format(self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
    """api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles',
                                    parameter = 'pm25')
    dicts = body['results'][:100]
    tuples = []
    n = 0
    for item in dicts:
        tuple = (dicts[n]['date']['utc'], dicts[n]['value'])
        tuples.append(tuple)
        n = n+1"""
    return str(Record.query.filter(Record.value >= 10).all())

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles',
                                    parameter = 'pm25')
    dicts = body['results'][:100]

    tuples = []
    n = 0
    for item in dicts:
        tuple = (str(dicts[n]['date']['utc']), dicts[n]['value'])
        tuples.append(tuple)
        n = n+1

    n = 0
    for item in tuples:
        newrecord = Record(id = n, datetime = tuples[n][0], value = tuples[n][1])
        DB.session.add(newrecord)
        n = n+1

    DB.session.commit()
    return 'Data refreshed!'
