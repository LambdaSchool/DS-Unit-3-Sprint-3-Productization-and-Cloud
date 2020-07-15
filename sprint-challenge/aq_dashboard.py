"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# openaq variables
api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
results = body['results']

# Processes results from openaq api measurements
def process(results):
    return str([(result['date']['utc'], result['value']) for result in results])

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {}, Value {}>'.format(self.datetime, self.value)

@APP.route('/')
def root():
    return str(Record.query.filter(Record.value >= 10).all())

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']
    for result in results:
        date = result['date']['utc']
        val = result['value']
        DB.session.add(Record(datetime=date, value=val))
    DB.session.commit()
    return 'Data refreshed!'