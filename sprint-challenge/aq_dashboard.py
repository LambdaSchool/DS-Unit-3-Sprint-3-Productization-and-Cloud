"""
OpenAQ Air Quality Dashboard with Flask.
"""
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
DB = SQLAlchemy(APP)
API = openaq.OpenAQ()


def get_date_and_measure(city, parameter):
    status, body = API.measurements(city=city, parameter=parameter)

    return [(result['date']['utc'], result['value'])
            for result in body['results']]


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {} >'.format(self.datetime, self.value)


@APP.route('/')
def root():
    records=list(DB.session.query(Record).filter(Record.value >= 10))
    return render_template('dash.html', title='Los Angeles', records=records)


@APP.route('/refresh')
def refresh():
    '''
    Pull fresh data from Open AQ and replace existing data.
    '''
    DB.drop_all()
    DB.create_all()
    data = get_date_and_measure('Los Angeles', 'pm25')
    for item in data:
        record = Record(datetime=item[0], value=item[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'
