"""OpenAQ Air Quality Dashboard with Flask."""
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

class Record(DB.Model):
  id = DB.Column(DB.Integer, primary_key=True)
  datetime = DB.Column(DB.String(25))
  value = DB.Column(DB.Float, nullable=False)

  def __repr__(self):
    return '< Time {} -- Value {} >'.format(self.datetime, self.value)

def get_date_values():
  status, body = api.measurements(city='Los Angeles', parameter='pm25')
  results = body['results']
  date_val_tuples = []
  for res in results:
    tup = str(res['date']['utc']), res['value']
    date_val_tuples.append(tup)
  return date_val_tuples

def make_records(date_val_tuples):
  for tup in date_val_tuples:
    db_record = Record(datetime=tup[0], value=tup[1])
    DB.session.add(db_record)

@APP.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value>=10).all()
    return str(records)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    date_val_tuples = get_date_values()
    make_records(date_val_tuples)    
    DB.session.commit()
    return 'Data refreshed!'