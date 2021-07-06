"""OpenAQ Air Quality Dashboard with Flask."""

import os
from flask import Flask, render_template
from .openaq import OpenAQ
from flask_sqlalchemy import SQLAlchemy
from decouple import config

APP = Flask(__name__)
DB = SQLAlchemy(APP)
api = OpenAQ()


class Record(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    city = DB.Column(DB.String(60), nullable=False)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<DATE: {}, VALUE: {}>'.format(self.datetime, self.value)


def create_app():
    """Base view."""
    APP.config['ENV'] = config('ENV')
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def make_list():
    """Returns a list of tuples."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    date_values = []
    results = body['results']
    for result in results:
        result_tuple = (str(result['date']['utc']), result['value'])
        date_values.append(result_tuple)

        return date_values

    return APP


@APP.route('/')
def root():
    """Main route."""
    potential_poor_air = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html',
                           records=potential_poor_air)


def new_city(city):
    status, body = api.measurements(city=city, parameter='pm25')
    citydata = str(body['results'])
    for result in citydata:
        db_record = Record(city=city, datetime=result[0], value=result[1])
        DB.session.add(db_record)


@APP.route('/refresh')
def refresh():
    """Refresh data from Open AQ and replace current data."""
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    cities = ['Los Angeles']
    for city in cities:
        new_city(city)
    DB.session.commit()
    return 'Data refreshed!'


