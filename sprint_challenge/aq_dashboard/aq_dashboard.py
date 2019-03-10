"""   """
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# import matplotlib.pyplot as plt
import openaq
import pandas as pd
import requests
# import seaborn as sns

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    """Base view."""
    data = get_api_data()
    add_data(data)
    records = Record.query.filter(Record.value >= 10).all()

    c = str(records)
    return render_template('base.html', records=records)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    data = get_api_data()
    add_data(data)

    #list of "potentially risky" PM 2.5
    records = Record.query.filter(Record.value >= 10).all()
    b = str(records)
    return render_template('base.html', records=records, message='Data refreshed')

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Date:{}, pm25: {}'.format(self.datetime, self.value)

def add_data(data):

    for record in data:
        if not DB.session.query(Record).filter(Record.datetime == record.datetime).first():
            DB.session.add(record)
    DB.session.commit()

def get_api_data():

    """ Query OpenAQ for LA and pm=25"""
    api = openaq.OpenAQ()
    data = []
    status, resp = api.measurements(city='Los Angeles', parameter='pm25')
    api_data = [(item['date']['utc'], item['value'])
                    for item in resp['results']]
    for record in api_data:
        data.append(Record(datetime=record[0], value=record[1]))

    return data

