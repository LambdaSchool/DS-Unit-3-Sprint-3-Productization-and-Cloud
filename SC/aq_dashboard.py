"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests
import json
from datetime import datetime
import openaq
import sqlite3

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

def retrieve_data():
    """gets data from OpenAQ api and returns as a string of tuples"""
    api = openaq.OpenAQ()
    test = api.measurements(city='Los Angeles', parameter='pm25')
    number, dict = [i for i in test]
    results_dict = dict['results']
    date_dict = [i['date'] for i in results_dict]
    utc_list = [i['utc'] for i in date_dict]
    value_list = [i['value'] for i in results_dict]
    tuples_list = list(zip(utc_list, value_list))
    return str(tuples_list)

def retrieve_data2():
    """gets data from OpenAQ api and returns as a list of tuples
       used to insert into the database"""
    api = openaq.OpenAQ()
    test = api.measurements(city='Los Angeles', parameter='pm25')
    number, dict = [i for i in test]
    results_dict = dict['results']
    date_dict = [i['date'] for i in results_dict]
    utc_list = [i['utc'] for i in date_dict]
    value_list = [i['value'] for i in results_dict]
    tuples_list = list(zip(utc_list, value_list))
    return tuples_list


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    # def __repr__(self, id=id, datetime=datetime, value=value):
    #     # write a nice representation of Records'
    #     self.id = id
    #     self.datetime = str(datetime)
    #     self.value = value
    #     return '{}, {}, {}'.format(self.id, self.datetime, self.value)
    #     # i tried returning in a nice format
    #     # this didn't work


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api_data = retrieve_data2()

    # enter the data into the sqlite3 database
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.executemany('INSERT INTO Record (datetime,value) VALUES (?,?)', api_data)
    conn.commit()
    conn.close()
    DB.session.commit()

    return 'Data refreshed!'

@APP.route('/')
def root():
    """Base view."""
    data = retrieve_data()

    # Get Records greater than or equal to 10
    def greater_than_10():
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        query = 'SELECT * FROM Record WHERE value >=10;'
        answer = c.execute(query).fetchall()
        return str(answer)

    filtered_records = greater_than_10()
    string = """ The data is: \n {}
                 \n\n
                 The records with values greater than or equal to 10 are: \n {}""".format(data, filtered_records)
    return string

if __name__ == '__main__':
    APP.run(port = 5000, debug=True)