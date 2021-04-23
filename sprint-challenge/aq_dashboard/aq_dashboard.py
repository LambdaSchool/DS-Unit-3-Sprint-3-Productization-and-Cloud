"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


@APP.route('/')
def root():
    """Base view."""
    print(len(Record.query.all()))
    if len(Record.query.all()) == 0:
        refresh()
    records = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', records=records)
    return str(records)


def get_times(api):
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for i in range(len(body['results'])):
        new_record = Record(id=i,
                            datetime=str(body['results'][i]['date']['utc']),
                            value=body['results'][i]['value'])
        DB.session.add(new_record)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'Time: {self.datetime}, Value: {self.value}'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api = openaq.OpenAQ()
    get_times(api)
    DB.session.commit()
    return render_template("refresh.html", refresh='Data refreshed!')
    return 'Data refreshed!'
