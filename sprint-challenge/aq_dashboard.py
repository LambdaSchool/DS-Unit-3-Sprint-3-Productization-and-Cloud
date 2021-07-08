"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy
import datetime


APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
api = openaq.OpenAQ()


class Record(DB.Model):
    """Model for records from API."""
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(), nullable=False)
    country = DB.Column(DB.String(), nullable=False)
    datetime = DB.Column(DB.DateTime(), nullable=False)
    value = DB.Column(DB.Float, nullable=False)


class Call(DB.Model):
    """Model for calls to API."""
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(), nullable=True)
    country = DB.Column(DB.String(), nullable=True)
    date_from = DB.Column(DB.DateTime(), nullable=True)
    date_to = DB.Column(DB.DateTime(), nullable=True)
    min_val = DB.Column(DB.Float(), nullable=True)
    max_val = DB.Column(DB.Float(), nullable=True)


@APP.route('/')
def root():
    """Base view."""
    return render_template("root.html")


@APP.route('/refresh')
def refresh():
    """Remove all data from database."""
    DB.drop_all()
    DB.create_all()
    return 'Data refreshed!'


@APP.route('/get', methods=["POST"])
def get():
    """Push table of locations, datetimes and pm25 values based on user
    input."""
    params = {'parameter': 'pm25'}
    city = request.form.get('city')
    if city is not '':
        params['city'] = city
    else:
        city = None
    country = request.form.get('country')
    if country is not '':
        params['country'] = country
    else:
        country = None
    date_from = request.form.get('date_from')
    if date_from is not '':
        params['date_from'] = date_from
        date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    else:
        date_from = None
    date_to = request.form.get('date_to')
    if date_to is not '':
        params['date_to'] = date_to
        date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    else:
        date_to = None
    min_val = request.form.get('min_val')
    if min_val is not '':
        min_val = float(min_val)
        params['value_from'] = min_val
    else:
        min_val = None
    max_val = request.form.get('max_val')
    if max_val is not '':
        max_val = float(max_val)
        params['value_to'] = max_val
    else:
        max_val = None
    rec = [(r.city, r.country, r.date_from, r.date_to, r.min_val, r.max_val)
           for r in Call.query.all() if r.city == city and
           r.country == country and r.date_from == date_from and
           r.date_to == date_to and r.min_val == min_val and
           r.max_val == max_val]
    if len(rec) == 0:
        n_call = Call(city=city, country=country, date_from=date_from,
                      date_to=date_to, min_val=min_val, max_val=max_val)
        DB.session.add(n_call)
        status, body = api.measurements(**params)
        for status in body['results']:
            d_time = datetime.datetime.strptime(status['date']['utc'],
                                                '%Y-%m-%dT%H:%M:%S.%fZ')
            n_record = Record(city=status['city'],
                              country=status['country'],
                              datetime=d_time,
                              value=status['value'])
            DB.session.add(n_record)
        DB.session.commit()
    print(params)
    q = Record.query.order_by(Record.datetime.asc())
    if city is not None:
        q = q.filter(Record.city == city)
    if country is not None:
        q = q.filter(Record.country == country)
    if date_from is not None:
        q = q.filter(Record.datetime >= date_from)
    if date_to is not None:
        q = q.filter(Record.datetime <= date_to)
    if min_val is not None:
        q = q.filter(Record.value >= min_val)
    if max_val is not None:
        q = q.filter(Record.value <= max_val)
    return render_template("get.html", records=q.all())
