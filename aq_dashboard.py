"""OpenAQ AAir Quality Dashboard with Flask."""
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
api = openaq.OpenAQ()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

@APP.route('/')
def root():
    """Base view."""
    refresh()
    high_vals = Record.query.filter(Record.value > 10).all()
    return str(high_vals)

def get_pm25():
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    results = body['results']

    values_list = []
    for result in results:
        values = (result['date']['utc'], result['value'])
        values_list.append(values)
    return values_list

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"< Time {self.datetime} ---- Value {self.value} >"


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    values_list = get_pm25()
    for id, values in enumerate(values_list):
        date_str = str(values[0])
        value = values[1]
        DB.session.add(Record(id=id, datetime=date_str, value=value))
    DB.session.commit()
    return 'Data refreshed!'

    