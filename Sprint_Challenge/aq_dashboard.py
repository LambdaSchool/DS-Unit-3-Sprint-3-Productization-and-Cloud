"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq


"""Create and configure an instance of the flask app"""
APP = Flask(__name__)
api = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


def la_pm(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    utc_datetime_value = []
    for result in body['results']:
        date = result['date']['utc']
        value = result['value']
        utc_datetime_value.append((date, value))

    return utc_datetime_value


@APP.route('/')
def root():
    """Base view."""
    # utc_datetime_value = la_pm(city, parameter)
    value_10 = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', title='Air Quality', value_10=value_10)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} --- Value {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    utc_datetime_value = la_pm('Los Angeles', 'pm25')
    for x in utc_datetime_value:
        record = Record(datetime=x[0], value=x[1])
        DB.session.add(record)
    DB.session.commit()
    return render_template('base.html', title='Data refreshed!')
