"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()


@APP.route('/')
def root():
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    data = []
    for result in body['results']:
        value = result['value']
        utc_datetime = result['date']['utc']
        data.append((utc_datetime, value))

    return str(data)


@APP.route('/part4')
def part4():
	top10 = Record.query.filter(Record.values >= 10).all()
	return render_template('base.html', top10=top10)


class Record(DB.Model):
    record_id = DB.Column(DB.Integer, primary_key=True)
    record_datetime = DB.Column(DB.String(25))
    record_value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<datetime: {}, value: {}'.format(self.datetime, self.values)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = root()
    for result in data:
        record = Record(datetime=result[0], value=result[1])
        DB.session.add(record)
    DB.session.commit()
    return "data refreshed!"

