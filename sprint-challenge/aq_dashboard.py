"""OpenAQ Air Quality Dashboard with Flask."""
import openaq
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
api = openaq.OpenAQ()


class Record(DB.Model):
    """
    Records table to hold datetime and values from api request
    """
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record date_time:{}, pm25_value:{}>'.format(self.datetime, self.value)


def set_up():
    """
    set up fuction to create DB, gets date utc and pm25 values and adds them into the
    Records table for the city of Los Angeles
    """
    DB.create_all()
    status, body = api.measurements(city="Los Angeles", parameter="pm25")
    for i in range(len(body['results'])):
        elem = body['results'][i]
        date_time = elem['date']['utc']
        pm25_value = elem['value']

        record = Record(datetime=date_time, value=pm25_value)
        DB.session.add(record)
        DB.session.commit()


@APP.route('/')
def root():
    """ 
    when the main page is loaded try and query the DB returning a list of tuples of 
    datetimes and values for each record in the DB with a value of 10 or greater.

    if the query fails there is no DB so run set_up() to create and add records, print
    out message to use that DB was created and to refresh to see results.
    """
    try:
        highest_values = Record.query.filter(Record.value >= 10).all()
        lst = [(Record.datetime, Record.value) for Record in highest_values]
        return str(lst)
    except:
        set_up()
        return "DB setup, refresh to see results"


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    set_up()
    return 'Data refreshed!'