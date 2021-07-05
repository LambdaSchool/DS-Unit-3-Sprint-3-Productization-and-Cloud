"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

date_time = []

def get_data():
  api = openaq.OpenAQ()
  status, body = api.measurements(city='Los Angeles', parameter='pm25') 
  for item in body['results']:
    utc = item['date']['utc']
    value = item['value']
    date_tuple = (utc, value)
    date_time.append(date_tuple)
  return date_time

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record {}>'.format(self.id)

@APP.route('/')
def root():
    """Base view."""
    data = get_data()
    filtered_data = Record.query.filter(Record.value>=10).all()
    return str(filtered_data)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    #Get data from OpenAQ, make Record objects with it, and add to db
    data = get_data()
    for tup in data:
      db_date = tup[0]
      db_val = tup[1]
      db_record = Record(datetime=db_date, value=db_val)
      DB.session.add(db_record)
    DB.session.commit()
    return 'Data refreshed!'