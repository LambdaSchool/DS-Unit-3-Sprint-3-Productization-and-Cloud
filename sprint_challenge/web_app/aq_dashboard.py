from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
import openaq

import os
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)

class City(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<City: {self.name}>'

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.DateTime(25))
    value = DB.Column(DB.Float, nullable=False)
    parameter = DB.Column(DB.String(15))
    location = DB.Column(DB.String(80), nullable=False)
    city_id = DB.Column(DB.Integer,
                        DB.ForeignKey('city.id'),
                        nullable=False)
    city = DB.relationship(
        'City',
        backref=DB.backref('records', lazy='dynamic'))

    def __repr__(self):
        return f'<Record: {self.city}, {self.datetime}, {self.value}>'
        

def get_city_data(city='Los Angeles', parameter='pm25', 
                  date_from=None, limit=1000, max_records=None):
    api = openaq.OpenAQ()
    _, body = api.measurements(
        city=city, parameter=parameter,
        date_from=date_from, limit=limit,
        )
    pages = body['meta']['pages']
    APP.logger.info(body['meta']['found'])
    results = [(x['date']['utc'],
                x['value'], x['unit'],
                x['location']
                )
                for x in body['results']]

    if pages > 1:
        for i in range(2, pages+1):
            if max_records and max_records <= len(results):
                break
            APP.logger.info(i)
            _, body = api.measurements(
                city=city, parameter=parameter,
                date_from=date_from, page=i, limit=limit)
            results.extend([(x['date']['utc'], 
                             x['value'], x['unit'],
                             x['location']
                             )
                             for x in body['results']])
    return results

def save_city_data(city='Los Angeles', parameter='pm25',
                   date_from=None, limit=1000, max_records=None):

    cityobj = (
            City.query.filter_by(name=city).first() or
            City(name=city))
    DB.session.add(cityobj)
    APP.logger.info(cityobj)
    latest_record = cityobj.records.order_by(Record.datetime.desc()).first()
    if latest_record:
        # Remove the utc time offset because endpoint does not
        # Understand it.
        date_from = latest_record.datetime.isoformat().split('+')[0]
        APP.logger.info(date_from)
        date_from = date_from
        # Set a lower page size to get more frequent updates 
        limit = 50
    APP.logger.info(date_from)
    data = get_city_data(city=city, parameter=parameter,
                         date_from=date_from, limit=limit,
                         max_records=max_records)

    records = []
    if data:
        #filter out existing data
        APP.logger.info(data)
        data = [d for d in data
                if Record.query.filter_by(
                    datetime=d[0], value=d[1], parameter=d[2], location=d[3]).scalar()
                is None]
        
        records = [Record(datetime=d[0], value=d[1], parameter=d[2], location=d[3])
                   for d in data]
        cityobj.records.extend(records)
        DB.session.commit()
    return records

@APP.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        data = get_city_data(limit=100, max_records=100)
        data = [(x[0], x[1], x[3]) for x in data]
        
        potentially_risky = Record.query.filter(Record.value>10).order_by(Record.datetime.desc()).limit(20)
        #APP.logger.info(Record.filter(Record.value>10))
        APP.logger.info('zomg')
    return render_template('index.html', data=data, potentially_risky=potentially_risky)

@APP.route('/save_city')
def save_city():
    data = save_city_data(limit=100, max_records=None)
    
    return str(data)

@APP.route('/data')
def data_summary():
    data = DB.session.query(Record.location, func.avg(Record.value)).group_by(
        Record.location).order_by(func.avg(Record.value).desc())
    return render_template('report.html', data=data)
@APP.route('/clear_db')
def clear():
    DB.drop_all()
    DB.create_all()
    return 'DB cleared'