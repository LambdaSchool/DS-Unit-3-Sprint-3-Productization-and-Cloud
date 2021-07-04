from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

# Part 1 & 2

# Data Generation - for root
def dat_gen(city):
    """generate datetime and value for specified city"""
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']
    dates_values = [(result['date']['utc'], result['value']) for result in results]
    return dates_values


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)



@APP.route('/')
def root():
    """Base view."""
    return render_template('home.html')

# Part 3
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    city = DB.Column(DB.String(25))

    def __repr__(self):
        return f'<city: {self.city} - datetime: {self.datetime} - value: {self.value}>'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    cities = ['Los Angeles','Los Angeles-Long Beach-Santa Ana']
    for city in cities:
        city_data = dat_gen(city)
        for dat in city_data:
            record = Record(city=city, datetime=dat[0], value=dat[1])
            DB.session.add(record)
        DB.session.commit()
    return render_template('refresh.html', message='Data refreshed!')


@APP.route('/la')
def LA():
    """Los Angeles view."""
    big_values = Record.query.filter(Record.value >= 10, Record.city == 'Los Angeles').all()
    return render_template('la.html', records=big_values)


@APP.route('/la-us')
def LA_US():
    """Other Los Angeles view."""
    big_values = Record.query.filter(Record.value >= 10, Record.city == 'Los Angeles-Long Beach-Santa Ana').all()
    return render_template('la-us.html', records=big_values)

# A failed attempt to make a generic page for any city
""" 
@APP.route('/city/<city_name>',city_name=None)
def city():
    city_name = request.values["city_name"]
    #Other Los Angeles view.
    big_values = Record.query.filter(Record.value >= 10, Record.city == city_name).all()
    return render_template('city.html', records=big_values)
"""
