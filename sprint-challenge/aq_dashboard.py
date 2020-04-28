from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
api = openaq.OpenAQ()


"""Base view."""


@APP.route('/')
def root():
    risky = Record.query.filter(Record.value >= '10').all()
    return render_template('base.html', risky=risky)


def utcAndValues():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    dates = []
    for i in range(100):
        newDate = body['results'][i]['date']['utc']
        dates.append(newDate)

    values = []
    for i in range(100):
        newValue = body['results'][i]['value']
        values.append(newValue)

    utcAndValues = list(zip(dates, values))
    return utcAndValues


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<utc: {} and value: {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # Get data from OpenAQ, make Record objects with it, and add to db
    data = utcAndValues()
    for i in range(100):
        dates = data[i][0]
        values = data[i][1]
        newRecord = Record(datetime=dates, value=values)
        DB.session.add(newRecord)
    DB.session.commit()
    return 'Data refreshed!'
