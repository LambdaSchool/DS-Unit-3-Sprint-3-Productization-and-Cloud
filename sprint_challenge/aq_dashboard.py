"""OpenAQ Air Quality Dashboard with Flask."""

from open_aq import API, OpenAQ
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

def create_app():
    """Initialize OpenAQ dashboard"""
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    DB.init_app(APP)

    api = OpenAQ()


    @APP.route('/')
    def root():
        """Base view."""
        # import pdb; pdb.set_trace()
        # add new records
        add_records(get_records(api=api), database=DB)

        # select potentially risky records
        records = Record.query.filter(Record.value > 5)

        return render_template('base.html', records=records)

    @APP.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        # reset data
        DB.drop_all()
        DB.create_all()

        # add new records
        add_records(get_records(api=api), database=DB)
        records = Record.query.filter(Record.value > 5)

        return render_template('base.html', records=records,
                               message='Data refreshed!')

    return APP


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Date: %str, pm25: %f' % (self.datetime, self.value)


def get_records(api, city='Los Angeles', paramter='pm25'):
    """
    Queries OpenAQ for a given city and measurement
    """
    records = []
    status, body = api.measurements(city=city, parameter=paramter)
    observations = [(res['date']['utc'], res['value'])
                    for res in body['results']]
    for obs in observations:
        records.append(Record(datetime=obs[0], value=obs[1]))
    return records

def add_records(records, database):
    """
    Adds a list of records to the SQLite Database
    """
    for r in records:
        if not DB.session.query(Record).filter(Record.datetime == r.datetime).first():
            database.session.add(r)
    DB.session.commit()


