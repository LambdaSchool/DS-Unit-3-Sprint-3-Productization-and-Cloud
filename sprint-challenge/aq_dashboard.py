"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
DB = SQLAlchemy(APP)
#set up app know about database
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#let database now about application
DB.init_app(APP)

api = openaq.OpenAQ()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'<Date: {self.datetime}, Value: {self.value}>'

#tuple logic
def try_this():
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    list = []
    for i in range(len(body['results'])):
        x=body['results'][i]['date']['utc']
        y=body['results'][i]['value']
        adding = Record(datetime=str(x), value=y)
        my_tuple=(x,y)
        list.append(my_tuple)
        DB.session.add(adding)
    DB.session.commit()
    greater_than_10 = Record.query.filter(Record.value >= 10).all()
    return list, render_template('index.html', greater_than_10=greater_than_10)

@APP.route('/')
def root():
    """Base view."""
    return str(try_this())

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'
