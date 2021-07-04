"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
import requests
import os
from flask_sqlalchemy import SQLAlchemy

api = openaq.OpenAQ()

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


### body.get('results')[n].get('date').get('utc')
### body.get('results')[n].get('value')

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '(datetime ' + self.datetime + ' ) (value ' + str(self.value) + ' )'

@APP.route('/')
def root():
    retstr = ''
    data = Record.query.filter(Record.value >= 10).all()

    for s in data:
        retstr = retstr + str(s) + '<br />'
    return '<body>' + retstr + '</body>'

@APP.route('/pull')
def datapull():
    """Base view."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    date_value = [(body.get('results')[n].get('date').get('utc'),body.get('results')[n].get('value')) for n in range(0,100)]


    retstring = ''
    for s in date_value:
        retstring = retstring + '(' + s[0] + ' , ' + str(s[1]) + ')<br />'
        vals = Record()
        vals.datetime = s[0]
        vals.value = s[1]
        DB.session.add(vals)
    DB.session.commit()
    return retstring
#'TODO - part 2 and beyond!'

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'
