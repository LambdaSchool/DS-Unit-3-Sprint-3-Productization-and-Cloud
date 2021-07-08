"""OpenAQ Air Quality Dashboard with Flask"""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq.OpenAQ()

def get_results():
	status, resp = api.measurements(city='Los Angeles', parameter='pm25')
	utcs = []
	for utc in range(0, len(resp['results'])):
		u = resp['results'][utc]['date']['utc']
		utcs.append(u)

	values = []
	for value in range(0, len(resp['results'])):
		v = resp['results'][value]['value']
		values.append(v)

	result = zip(utcs, values)

	return list(result)

DB = SQLAlchemy(APP)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

class Record(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	datetime = DB.Column(DB.String(25))
	value = DB.Column(DB.Float, nullable=False)
	
	def __repr__(self):
		tup = (self.datetime, self.value)
		return '<Date: {}, Value: {}>'.format(tup)

@APP.route('/')
def root():
	"""Base view."""
	data = Record.query.filter(Record.value >= 10).all()
	return data

@APP.route('/refresh')
def refresh():
	"""Pull fresh data from Open AQ and replace existing data."""
	DB.drop_all()
	DB.create_all()
	api = openaq.OpenAQ()
	status, resp = api.measurements(city='Los Angeles', parameter='pm25')
	ids = [x for x in range(len(resp['results']))]
	dts = [x['date']['utc'] for x in resp['results']]
	vals = [x['value']for x in resp['results']]
	for ids, dts, vals in zip(ids, dts, vals):
		record = Record(id=ids, datetime=dts, value=vals)
		DB.session.add(record)
		DB.session.commit()
	return 'Data refreshed!'
