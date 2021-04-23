"""OpenAQ Air Quality Dashboard with Flask."""
# imports
import openaq
from app import app
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from decouple import config
import requests

# app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

DB = SQLAlchemy(app)
api = openaq.OpenAQ()


def utc_values(city='Los Angeles', parameter='pm25'):
    """Takes in air quality measurements and returns list of utc and values"""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    big_dict = body['results']
    date = []
    for i in big_dict:
        for x, y in i.items():
            if x == 'date':
                date.append(y)
    utc = []
    for b in date:
        for c, d in b.items():
            if c == 'utc':
                utc.append(d)

    value = []
    for p in big_dict:
        for q, r in p.items():
            if q == 'value':
                value.append(r)

    list_of_zipped_items = list(zip(utc, value))
    return list_of_zipped_items


@app.route('/')
def root():
    """Returns values greater than 10"""
    risky = Record.query.filter(Record.value >= 10).all()
    return str(risky)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Date-time: {} - Value: {} >'.format(self.datetime,
                                                      self.value)


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    la = utc_values(city='Los Angeles', parameter='pm25')
    for v in la:
        tupl = Record(datetime=v[0], value=v[1])
        DB.session.add(tupl)

    DB.session.commit()
    return 'Data refreshed!'
