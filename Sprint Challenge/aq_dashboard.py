"""OpenAQ Air Quality Dashboard with Flask."""
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    utc_datetime = DB.Column(DB.DateTime)
    location = DB.Column(DB.String(50))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'< Time {self.utc_datetime} --- Value {self.value} >'


def get_measurements(city='Los Angeles', parameter='pm25'):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    return [{'utc_datetime': datetime.strptime(result['date']['utc'],
                                               '%Y-%m-%dT%H:%M:%S.%f%z'),
             'location': result['location'],
             'value': result['value']} for result in body['results']]


@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html',
                           city='Los Angeles',
                           records=records)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = get_measurements()
    for record in data:
        DB.session.add(Record(utc_datetime=record['utc_datetime'],
                              location=record['location'],
                              value=record['value']))
    DB.session.commit()
    return 'Data refreshed!'


@APP.route('/locations/<city>')
def locations(city='Los Angeles'):
    """Pull location meta-data from Open AQ and display it."""
    api = openaq.OpenAQ()
    status, body = api.locations(city=city)
    locations = [{'name': loc['location'],
                  'latitude': loc['coordinates']['latitude'],
                  'longitude': loc['coordinates']['longitude']} for loc in body['results']]
    return render_template('locations.html',
                           city=city,
                           locations=locations)
