"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

# App routes
@APP.route('/')
def root():
    records = Record.query.filter(Record.value >= 10).all()
    return render_template('aq_base.html', title='Records with values 10 and above.', records=records)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    update_db()
    DB.session.commit()
    records = Record.query.all()
    return render_template('aq_base.html', title='Refreshed!', records=records)

# Functions
def tup_list():
    """Creates list of (utc_datetime, value) from using openaq API"""
    list=[]
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for i in range(1,100):
        utc_datetime = body['results'][i].get('date').get('utc')
        value = body['results'][i].get('value')
        tup = (utc_datetime, value)
        list.append(tup)
    return list

def update_db():
    """Updates database adding new data if it's available"""
    try:
        for record in tup_list():
            db_tup = Record(datetime=record[0], value=record[1])
            DB.session.add(db_tup)
    except Exception as e:
        print('Error processing: {}'.format(e))
        raise e

# DB models
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<({}, {})>'.format(self.datetime, self.value)