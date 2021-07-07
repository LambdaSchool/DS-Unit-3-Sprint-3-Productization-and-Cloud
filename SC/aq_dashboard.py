"""OpenAQ Air Quality Dashboard with Flask."""
"""$env:FLASK_APP = "aq_dashboard.py"""
"""flask run"""

import openaq
from flask import Flask
from aq_openaq import body
from flask_sqlalchemy import SQLAlchemy
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aq_db.sqlite3'
APP.config['ENV'] = 'debug'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time %s --- Value %.1f>' % (self.datetime, self.value)

# def data():
#     results = body['results']
#     DB.create_all()
#     for x in results:
#         DB.session.add(
#             Record(datetime=str(x['date']['utc']), value=x['value']))
#     DB.session.commit()
#     return Record.query.all()


@APP.route('/')
def root():
    """Base view."""
    results = body['results']
    DB.drop_all()
    DB.create_all()
    for x in results:
        DB.session.add(
            Record(datetime=str(x['date']['utc']), value=x['value']))
    DB.session.commit()
    list_date_value = [(x['date']['utc'], x['value']) for x in results]
    return str(Record.query.filter(Record.value >= 10).all())


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data"""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to DB
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameters='pm25')
    results = body['results']
    for x in results:
        DB.session.add(
            Record(datetime=str(x['date']['utc']), value=x['value']))
    DB.session.commit()
    return 'Data refreshed!'
