"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
l = []
for x in range(len(body['results'])):
    l.append((body['results'][x]['date']['utc'], body['results'][x]['value']))

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_ECHO'] = True
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Date: {} -- PM 2.5: {}'.format(self.datetime, self.value)

@APP.route('/')
def root():
    """Base view."""
   
    return str(list(Record.query.filter(Record.value >= 10).all()))


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    for x in range(len(body['results'])):
        datetime = str(body['results'][x]['date']['utc'])
        value = float(body['results'][x]['value'])
        db_user = Record(datetime=datetime, value = value)
        DB.session.add(db_user)
    DB.session.commit()
    return 'Data refreshed!'