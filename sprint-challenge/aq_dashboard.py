"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq_py

api = openaq_py.OpenAQ()
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


def get_data(city):
    status, body = api.measurements(city=city, parameter='pm25')
    if status >= 400:
        return 'error: status 400 or above'
    dates_and_values = [(entry['date']['utc'], entry['value'])
                        for entry in body['results']]
    return dates_and_values


def populate_database():
    DB.drop_all()
    DB.create_all()
    cities = ['Los Angeles', 'Los Angeles-Long Beach-Santa Ana']
    for city in cities:
        entries = get_data(city)
        for entry in entries:
            record = Record(city=city, datetime=entry[0], value=entry[1])
            DB.session.add(record)
        DB.session.commit()
    return 'Data refreshed!'


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(60))
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'City: {self.city} Time: {self.datetime} pm25 value: {self.value}'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    message = populate_database()
    return render_template('refresh.html', message=message)


@APP.route('/')
def root():
    """Base view."""
    return render_template('base.html')


@APP.route('/la')
def LA():
    """Los Angeles view."""
    big_values = Record.query.filter(Record.value >= 10,
                                     Record.city == 'Los Angeles').all()
    return render_template('la.html', records=big_values)


@APP.route('/la-us')
def LA_US():
    """Other Los Angeles view."""
    big_values = Record.query.filter(
        Record.value >= 10,
        Record.city == 'Los Angeles-Long Beach-Santa Ana').all()
    return render_template('la-us.html', records=big_values)


@APP.route('/about')
def about():
    """About view."""
    return render_template('about.html')
