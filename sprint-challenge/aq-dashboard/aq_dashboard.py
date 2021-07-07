"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
import openaq
import templates
api = openaq.OpenAQ()

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'ID: {id}, Date: {self.datetime}, Value: {self.value}'

def query_openaq(city, param):
    status, body = api.measurements(city=city, parameter=param)
    if status == 200:
        query_results = []
        for query in body['results']:
            query_results.append((query['date']['utc'], query['value']))
        return query_results
    else:
        return "API Error, please try again."

@APP.route('/')
def root(refreshed=False):
    """Base view."""
    records = Record.query.filter(Record.value > 10).all()
    record_dicts = []
    for record in records:
        record_dict = {"id": record.id, "datetime": datetime.datetime.strptime(record.datetime, '%Y-%m-%dT%H:%M:%S.%fZ'), "value": record.value}
        record_dicts.append(record_dict)
    return render_template('index.html', title="Air Quality Dashboard", la_pm25=record_dicts)

@APP.route('/refresh')
def refresh():
    DB.drop_all()
    DB.create_all()
    results = query_openaq("Los Angeles", 'pm25')
    for result in results:
        time, value = result
        record = Record(datetime=time, value=value)
        DB.session.add(record)
    DB.session.commit()
    return root(refreshed=True)