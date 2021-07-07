"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
API = openaq.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    """Base view."""
    records = (Record.query.filter(Record.value >= 10).all())
    return render_template('base.html', title='Home', records=records)


def create_list():
    status, body = API.measurements(city='Los Angeles', parameter='pm25')
    aq = []
    for dict in body['results']:
        aq.append((dict['date']['utc'], dict['value']))
    return aq


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
    results = create_list()
    for result in results:
        record = Record(datetime=result[0], value=result[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'
