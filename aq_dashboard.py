"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)



# Directing the file to the SQL database
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time of Reading {} --- PM2.5 {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
   
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    for endpoint in body['results']:
        instance = Record(datetime=endpoint['date']['utc'], value=endpoint['value'])
        DB.session.add(instance)





    DB.session.commit()
    return 'Data refreshed!'



@APP.route('/')
def root():
    """Base view."""

    dirty_air = Record.query.filter(Record.value >= 10).all()

    return render_template('htm_hell.html', title='home', readings=dirty_air)