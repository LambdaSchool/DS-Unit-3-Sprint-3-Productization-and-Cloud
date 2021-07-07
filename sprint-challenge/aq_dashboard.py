"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy


# Instantiate app with Flask
APP = Flask(__name__)


# SQLAlchemy stuff
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Time:' + str(self.datetime) + ', Value:' + str(self.value)


# API pull function
def pull_pm(city, parameter):
    api = openaq.OpenAQ()
    status, body = api.measurements(city=city, parameter=parameter)
    return [(entry['date']['utc'], entry['value']) for entry in body['results']]


# Pages
@APP.route('/')
def root():
    """Base View"""
    samples = Record.query.filter(Record.value >= 10.0).all()
    return str(samples)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    samples = pull_pm('Los Angeles', 'pm25')
    for sample in samples:
        measure = Record(datetime = str(sample[0]), value = sample[1])
        DB.session.add(measure)
    DB.session.commit()
    return 'Data refreshed!'


# Run App
if __name__ == '__main__':
    APP.run(debug=True)