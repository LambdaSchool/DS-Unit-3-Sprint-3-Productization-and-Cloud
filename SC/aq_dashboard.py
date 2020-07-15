"""OpenAQ Air Quality Dashboard with Flask"""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

# Create SQLAlchemy db


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
DB.init_app(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Time:', datetime, '--- Value:', value

# Function to pull data from API
def pull_data():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    if status != 200:
        return 'Error!'
    else:    
        return body['results']

# Function to extract tuple of UTC date and value
def pull_date_value(results):
    result_list = []
    y = len(results)
    for i in range(y):
        x = (results[i]['date']['utc'],results[i]['value'])
        result_list.append(x)
    
    return result_list

@APP.route('/')
def root():
    q_results = DB.query.all()
    return q_results

if __name__ == "__main__":
    APP.run(debug=True)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    fresh_data = pull_date_value(pull_data())
    for tup in range(len(fresh_data)):
        rec = Record(datetime=tup[0], value=tup[1])
        DB.session.add(rec)

    DB.session.commit()
    return 'Data refreshed!'
