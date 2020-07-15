"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import openaq
import requests

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy()
DB.init_app(APP)

api = openaq.OpenAQ()
status, dict_value = api.measurements(city='Los Angeles', parameter='pm25')

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        clean_list = []
        for i in range(len(dict_value['results'])):
            datetime = dict_value['results'][i]['date']['utc'] # UTC code
            value = dict_value['results'][i]['value'] # Recorded Value
            clean_list.append((datetime,value)) # List of tuples

        return clean_list

@APP.route('/')
def root():
    """Base view."""
    record = Record.query.all()
    return None

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    db_record = Record()
    DB.session.add(db_record)
    DB.session.commit()
    return 'Data refreshed!'

