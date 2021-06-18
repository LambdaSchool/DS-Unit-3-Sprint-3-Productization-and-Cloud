"""OpenAQ Air Quality Dashboard with Flask."""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests

"""Create and configure an instance of the Flask application."""
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
api = openaq.OpenAQ()


def aqmeasurements(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    la_results = body['results']
    date = []
    for b in la_results:
        for x, y in b.items():
            if x == 'date':
                date.append(y)
    utc = []
    for c in date:
        for k, v in c.items():
            if k == 'utc':
                utc.append(v)
    val = []
    for d in la_results:
        for m, n in d.items():
            if m == 'value':
                val.append(n)

    utc_value = list(zip(utc, val))
    return utc_value


@APP.route('/')
def root():
    hazard = Record.query.filter(Record.value >= 10).all()
    return str(hazard)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Date-time: {} - PM value: {} >'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    utc_value = aqmeasurements(city='Los Angeles', parameter='pm25')
    for x in utc_value:
        db_record = Record(datetime=x[0], value=x[1])
        DB.session.add(db_record)

    DB.session.commit()
    return 'Data refreshed!'
