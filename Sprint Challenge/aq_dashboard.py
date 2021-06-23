"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)

@APP.route('/')
def root():
    """Base view."""
    risky_air = Record.query.filter(Record.value >= 10.0).all()
    return str(risky_air)
    # return "hello"

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    for x in utc_value_list(city='Los Angeles', parameter='pm25'):
        r = Record(datetime = x[0], value = x[1])
        DB.session.add(r)
        DB.session.commit()
    return 'Data refreshed!'

def utc_value_list(city='Los Angeles', parameter='pm25'):
    """list of (utc_datetime, value) tuples"""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    
    new_list = []

    for i in body['results']:
        i['date']['utc']
        utc_time = i['date']['utc']
        value = i['value']
        new_list.append(tuple((utc_time,value)))

    return new_list
    # return str(body['results'])

   

