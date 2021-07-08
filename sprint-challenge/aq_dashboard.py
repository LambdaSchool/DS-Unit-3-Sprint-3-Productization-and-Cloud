"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ
import html

APP = Flask(__name__)

api = OpenAQ()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

"""Main application and logic"""


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record: datetime:{} value:{}>' \
                   .format(self.datetime, self.value)


def get_measurements(**kwargs):
    status, body = api.measurements(**kwargs)
    locations = body['results'][:2]
    res = [(locations[i]['date']['utc'], locations[i]['value'])
           for i in range(len(locations))]
    return res


def add_measurements(measurements):
    try:
        for m in measurements:
            rec = Record(datetime=m[0], value=m[1])
            DB.session.add(rec)
    except Exception as e:
        print('Error processing {}'.format(measurements))
        raise e
    else:  # If there is no error, do this.
        DB.session.commit()


@APP.route('/')
def root():
    """Base view."""
    res = get_measurements(city='Los Angeles',
                           parameter='pm25')
    if len(res) > 0:
        add_measurements(res)
    return str(res)


@APP.route('/filter')
def filter():
    query_res = Record.query.filter(Record.value >= 3).all()
    res = html.escape(",".join([str(r) for r in query_res]))
    return res


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'
