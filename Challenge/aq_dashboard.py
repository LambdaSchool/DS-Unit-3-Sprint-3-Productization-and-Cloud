"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
	id = DB.Column(DB.Integer, primary_key=True)
	datetime = DB.Column(DB.String(25))
	value = DB.Column(DB.Float, nullable=False)

	def __repr__(self):
		return '<Record date {}>'.format(self.datetime) + '<value {}>'.format(self.value)


api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')

date_and_value = []

for result in body['results']:
	value = result['value']
	keys, values = zip(*result['date'].items())
	utc_datetime, _local = values
	date_and_value.append((str(utc_datetime),value))
	

@APP.route('/')
def root():

	my_list = date_and_value

	return render_template('base.html', title = 'Home', list = my_list)

@APP.route('/main')
def main():

	risky = Record.query.filter(Record.value >= 10).all()

	return render_template('base.html', title = 'Potentially risky days', list = risky)


@APP.route('/refresh')
def refresh():
	"""Pull fresh data from Open AQ and replace existing data."""
	DB.drop_all()
	DB.create_all()

	status, body = api.measurements(city='Los Angeles', parameter='pm25')

	for result in body['results']:
		value = result['value']
		keys, values = zip(*result['date'].items())
		utc_datetime, _local = values
		new_record = Record(datetime = str(utc_datetime), value = value)
		DB.session.add(new_record)

	DB.session.commit()
	return 'Data refreshed!'
