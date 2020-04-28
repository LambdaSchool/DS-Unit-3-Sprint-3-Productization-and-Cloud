"""OpenAQ Air Quality Dashboard with Flask."""
#standard library import
from flask import Flask
import requests
import json
from flask_sqlalchemy import SQLAlchemy

#import from openaq file
from openaq_py import openaq

# App initialization
APP = Flask(__name__)

#App configuration to db for Record class
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

#measurements for api request
los_angeles_pm25 = (city = 'Los Angeles', parameters = 'pm25')

# api request from openaq_py
api = openaq.OpenAQ(los_angeles_pm_25)

# webpage connection
@APP.route('/')

#function to call api and information
def root():
	# call for api connection
	response = requests.get(api)
    # need to return requested parameters
    return response.text

# class for recoding data into db
class Record(DB.Model):
	#building db model and input
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
	#use for repeat of get call from request to build db
    def __repr__(self):
        return 

# for when refresh is called
@APP.route('/refresh')
def refresh():
	#calling base root function for current data
    root()
	#db to be forced out of main spot and input of new data
    DB.drop_all()
    DB.create_all(
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
	#looking up SQLAlchemy code
    DB.session.commit()
    return 'Data refreshed!'
