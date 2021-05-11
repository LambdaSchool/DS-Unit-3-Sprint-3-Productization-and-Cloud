"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from decouple import config
import openaq 
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

api = openaq.OpenAQ()

@APP.route('/')
def root():
    """Base view."""
    # status, body = api.measurements(city='Los Angeles', parameter='pm25')
    # list_of_t = []
    # for i in range (0,100):
    # 	t = (body['results'][i]['date']['utc'],body['results'][i]['value'])
    # 	list_of_t.append(t)
    records = Record.query.filter(Record.value >10).all()
    list_of_t = []
    for record in records:
    	t = (record.datetime, record.value)
    	list_of_t.append(t)
    return str(list_of_t)



APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<date {} --- value {}>'.format(self.datetime, self.value)




@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for i in range (0,100):
    	t = (body['results'][i]['date']['utc'],body['results'][i]['value'])
    	r = Record(datetime=str(t[0]), value=str(t[1]))
    	DB.session.add(r)
    DB.session.commit()
    return 'Data refreshed!'