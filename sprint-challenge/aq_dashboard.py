"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, jsonify
from opaq import openaq_py
import json
from flask_sqlalchemy import SQLAlchemy

# Env variables
APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
DB = SQLAlchemy(APP)
api = openaq_py.OpenAQ()

# loose function to parse json
status, body = api.measurements(city="Los Angeles", parameter="pm25")
utc = []
for x in range(100):
    utc.append(str(body["results"][x]["date"]["utc"]))
value = []
for x in range(100):
    value.append(str(body["results"][x]["value"]))
utc_value = list(zip(utc, value))

# web page for all datetime/values returned
@APP.route("/")
def root():
    """Base view."""
    new_list = json.dumps(str(utc_value))
    return new_list


# web page for filtered values over 10
@APP.route("/main")
def main():
    """new page to host filtered query"""
    rec_q = Record.query.filter(Record.value >= 10).all()
    new_req = json.dumps(str(rec_q))
    return new_req


# Database class inheriting from sqlAlchemy.Model
class Record(DB.Model):
    """ schema for db """
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return "(Datetime %r, Value %r)" %(self.datetime, self.value)


# route to make new database values
@APP.route("/refresh")
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for x in utc_value:
        observ = Record(datetime=x[0], value=x[1])
        DB.session.add(observ)
    DB.session.commit()
    return "Data refreshed!"
