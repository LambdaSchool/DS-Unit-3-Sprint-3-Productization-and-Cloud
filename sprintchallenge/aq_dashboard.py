"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()


@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', title='Home', records=records)


def laaq():
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    aq = []
    for x in body['results']:
        aq.append((x['date']['utc'], x['value']))
    return aq


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Datetime: {}, Value: {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    results = laaq()
    for result in results:
        record = Record(datetime=result[0], value=result[1])
        DB.session.add(record)
    DB.session.commit()
    return root()
