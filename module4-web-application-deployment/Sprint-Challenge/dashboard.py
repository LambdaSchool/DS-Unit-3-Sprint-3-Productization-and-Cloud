"""OpenAQ Air Quality Dashboard with Flask."""
import openaq_py
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq_py.OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    over10 = Record.query.filter(Record.value >= 10).all()
    return str(over10)


def dt_val(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city=city, parameter=parameter)
    vals = []
    for row in body['results']:
        date = row['date']['utc']
        val = row['value']
        vals.append((date, val))
    return vals


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} ~ Value {} >'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for x in dt_val():
        db_record = Record(datetime=x[0], value=x[1])
        DB.session.add(db_record)

    DB.session.commit()
    return 'Data refreshed!'
