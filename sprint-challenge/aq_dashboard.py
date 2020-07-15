"""OpenAQ Air Quality Dashboard with Flask."""

import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


def query_aq():
    """Queries OpenAQ for air quality data in Los Angeles and parses tuple data via nested key extraction"""
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    results = []
    utc_list = []
    value_list = []

    x = 0
    for result in body['results']:

        results.append(body['results'][x])
        utc_list.append(results[x]['date']['utc'])
        value_list.append(results[x]['value'])
        x = x + 1
    # BULLY, lists cannot be rendered by Flask, we will cast to string in our root function.
    return list(zip(utc_list, value_list))


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "Datetime {0} : Value {1} \n".format(self.datetime, self.value)


def populate_db():
    """ Acts as a querying object for current OpenAQ data, parses the resulting tuple from query_aq()
        Writes the parsed data to local database on per record basis.
    """
    utc = 0
    value = 1

    query = query_aq()

    for tuples in query:

        record = Record(datetime=tuples[utc], value=tuples[value])
        DB.session.add(record)
        DB.session.commit()


@APP.route('/')
def root():
    """Base view. Uses utility functions to return Air Quality data and serves to Flask for web rendering"""
    bad_air = DB.session.query(Record).filter(Record.value >= 10).all()
    for air in bad_air:
        return str(air)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    populate_db()
    return 'Data refreshed!'
