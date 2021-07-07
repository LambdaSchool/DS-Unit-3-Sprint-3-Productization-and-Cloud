"""Main application and routing logic for Sprint Challenge OpenAQ."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
import openaq
import pandas
from decouple import config

api = openaq.OpenAQ() 

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    #df_la = api.measurements(city='Los Angeles', parameter='pm25', df=True)
    #date_values = df_la[['date.utc', 'value']]
    value10 = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', values=value10)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {}, Value: {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    df_la = api.measurements(city='Los Angeles', parameter='pm25', df=True)
    date_values = df_la[['date.utc', 'value']]
    for index, row in date_values.iterrows():
        measures = Record(datetime=row['date.utc'].strftime("%Y-%m-%d %H:%M"), value=row['value'])
        DB.session.add(measures)
    DB.session.commit()
    return 'Data refreshed!'