from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq_py

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
FLASK_ENV = 'development'


@APP.route('/')
def root():
    """Base view."""
    dateValue = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', dateValue=dateValue, city='Los Angeles')


@APP.route('/reset')
def reset():
    """fully reset the DB without re-populating it"""
    DB.drop_all()
    DB.create_all()
    return 'DB reset'


@APP.route('/refresh')
def refresh():
    """Pull fresh LA data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    rawData = lapm()
    for data in rawData:
        DB.session.add(Record(datetime=data[0], value=data[1]))
    DB.session.commit()
    return 'Data refreshed!'


@APP.route('/newcity')
def newcity():
    ''' allows the user to pick a new city to see pm2.5 data from'''
    cities = citylist()
    return render_template('newcity.html', cities=cities)


@APP.route('/city', methods=['POST'])
def city():
    '''shows pm2.5 data of a user selected city'''
    city = request.values['city']
    dateValue = citypm(city)
    return render_template('base.html', dateValue=dateValue, city=city)


def citylist():
    '''gets a list of cities from the API and returns a sorted list of cities
    that have data on pm2.5'''
    api = openaq_py.OpenAQ()
    status, body = api.cities(limit=100)
    cities = []
    for result in body['results']:
        status, body = api.measurements(city=result['city'], parameter='pm25')
        if len(body['results']) > 0:  # filter the list so only cities with data show
            cities.append(result['city'])
            #DB.session.add(City(cityname=result['city'], country=result['country']))
    # DB.session.commit()
    # The two lines about adding the city to the DB actually will make a mess, proof of concept
    cities.append('Los Angeles')
    return sorted(cities)


def citypm(city):
    '''returns a list of the UTC data and the recorded value of pm2.5 in the
    given city '''
    api = openaq_py.OpenAQ()
    status, body = api.measurements(city=city, parameter='pm25')
    dateValue = []
    for result in body['results']:
        utc = result['date']['utc']
        value = result['value']
        dateValue.append((utc, value))
    return dateValue


def lapm():
    '''collects the date and value recorded for LA's levels of PM25'''
    api = openaq_py.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    dateValue = []
    for result in body['results']:
        utc = result['date']['utc']
        value = result['value']
        dateValue.append((utc, value))
    return dateValue


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    # city = DB.Column(DB.String(60)) #Was going to try and get fancy but ran out of time

    def __repr__(self):
        return 'Record time: {}, value: {}'.format(self.datetime, self.value)


class City(DB.Model):
    '''this is to store data on which cities are in the database. Like Record.city
    I don't think that I have enough time to actually finish and deploy this model'''
    id = DB.Column(DB.Integer, primary_key=True)
    cityname = DB.Column(DB.String(60), nullable=False)
    country = DB.Column(DB.String(2))

    def __repr__(self):
        return 'city: {}'.format(self.cityname)


if __name__ == '__main__':
    APP.run()
