"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests


APP = Flask(__name__)
api = openaq.OpenAQ()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)




@APP.route('/')
def root():
    """Base view."""
    over_10 = Record.query.filter(Record.value >= 10.0).all()
    return str(over_10)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    for i in time_x_values():
        DB.session.add(Record(datetime=i[0], value=i[1]))
    DB.session.commit()
    return 'Data refreshed!'

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} <--> Value {}>'.format(self.datetime, self.value)

def time_x_values(city='Los Angeles', parameter='pm25'):
    """Pulling data using API"""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    values = []
    for result in body['results']:
        time = result['date']['utc']
        value = result['value']
        time_x_value.append((time, value))


    
