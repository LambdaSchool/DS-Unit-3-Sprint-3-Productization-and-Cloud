"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '(Datetime %r --- Value %r)' % (self.datetime, self.value)


def get_tuples(body):
    list_of_tuples = []
    for result in body['results']:
        utc_datetime_value_list = []
        utc_datetime_value_list.append(result['date']['utc'])
        utc_datetime_value_list.append(result['value'])
        utc_datetime_value_tuple = tuple(utc_datetime_value_list)
        list_of_tuples.append(utc_datetime_value_tuple)
    return list_of_tuples


@APP.route('/')
def root():
    """Base view."""
    filtered = Record.query.filter(Record.value > 10).all()
    datetimes = []
    values = []
    for record in filtered:
        datetimes.append(record.datetime)
        values.append(record.value)
    return render_template("index.html", len = len(filtered), datetimes = datetimes, values = values)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for tup in get_tuples(body):
        record = Record()
        record.datetime = tup[0]
        record.value = tup[1]
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'