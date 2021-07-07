"""OpenAQ Air Quality Dashboard with Flask."""

from openaq import API, OpenAQ
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = OpenAQ()
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """Base view."""
    city_list = [('Los Angeles',1),('Abu Dhabi',2)]
    return render_template('home.html', 
                            city_list=city_list,
                            title='Air Quality Monitor')


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    city_list = ['Los Angeles','Abu Dhabi']
    
    for name in city_list:
        db_city=City(name=name)

        for x in times_and_values(city=db_city.name):
            db_record = Record(datetime=x[0], value=x[1])
            db_city.records.append(db_record)
            DB.session.add(db_record)
    
    DB.session.commit()
    return 'Data refreshed!'

@APP.route('/city/<city_id>', methods=['GET'])
def city(city_id=None):
    city_id = city_id
    above10 = Record.query.filter(Record.value > 10).all()
    this_city = City.query.filter(City.id == city_id).one()
    return render_template('city.html', 
                            above10=above10, 
                            this_city=this_city)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    city_id = DB.Column(DB.Integer, DB.ForeignKey('city.id'), nullable=False)
    city = DB.relationship('City', backref=DB.backref('records', lazy=True))

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)


class City(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(25), nullable=False)

    def __repr__(self):
        return '< {} --- {} >'.format(self.id, self.name)


def times_and_values(city='Los Angeles', parameter='pm25'):
    status, body = api.measurements(city=city, parameter=parameter)
    results = []
    for row in body['results']:
        date = row['date']['utc']
        value = row['value']
        results.append((date, value))
    return results