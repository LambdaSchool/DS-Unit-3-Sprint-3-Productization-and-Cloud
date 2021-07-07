"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq_py


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = openaq_py.OpenAQ()

DB = SQLAlchemy(APP)


def dt_values():
    _, body = api.measurements(city='Los Angeles', parameter='pm25')
    tup_list = []
    
    for i in body['results']:
        datetime = i['date']['utc']
        value = i['value']
        tup_list.append((datetime, value))

    return tup_list


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<DateTime: {} --- Value: {}>'.format(self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
    filtered = Record.query.filter(Record.value >= 10).all()

    return render_template('layout.html', filtered=filtered)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    results = dt_values()
    for i, val in enumerate(results):
        record = Record(id=i, datetime=val[0],
                        value=val[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'
