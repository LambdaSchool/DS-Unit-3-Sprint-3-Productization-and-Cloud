"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq.OpenAQ()

DB = SQLAlchemy(APP)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'


class Record(DB.Model):
    """Makes our DB model"""
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)


def checkAPI():
    """Queries the API and saves the data"""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    tuple_list = []
    for i in body['results']:
        timecon = tuple((i['date']['utc'], i['value']))
        tuple_list.append(timecon)
        tc_record = Record(datetime=timecon[0], value=timecon[1])
        DB.session.add(tc_record)
    return tuple_list


def checkDB():
    """Checks the database for potentially risky tuples"""
    return Record.query.filter(Record.value > 2.5).all()[:]


@APP.route('/')
def root():
    """Base view."""
    # Gets the data from the API and adds the records.
    get_data = checkDB()
    return str(get_data)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    get_data = checkAPI()
    # Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'
