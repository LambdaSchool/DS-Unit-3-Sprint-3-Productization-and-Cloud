"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)

api = openaq.OpenAQ()
status, body = api.cities()


aq1 = api.measurements(city='Los Angeles', parameter='pm25')[1]
aq1_tup = body['results']

results = aq1.get('results')

tup_list = []


# for res in results:
#     for_list = []
#     a = res.get('date')
#     aa = a.get('utc')
#     aaa = 'Time = ' + aa
#     b = res.get('value')
#     bb = 'Value = ' + str(b)
#     for_list.append(aaa)
#     for_list.append(bb)
#     for_list_tup = tuple(for_list)
#     tup_list.append(for_list_tup)

for res in results:
    for_list = []
    a = res.get('date')
    aa = a.get('utc')
    b = res.get('value')
    for_list.append(aa)
    for_list.append(b)
    for_list_tup = tuple(for_list)
    tup_list.append(for_list_tup)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time: {} --- Value: {}>'.format(self.datetime, self.value)


# @APP.route('/')
# def root():
#     """Base view."""
#     ten_plus_records = Record.query.filter(Record.value >= 10).all()
#     return str(ten_plus_records)

@APP.route('/')
def root():
    """Base view."""
    ten_plus_records = Record.query.filter(Record.value >= 10).all()
    return render_template('DISPLAY.html', ten_plus_records=ten_plus_records)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    data = tup_list
    for ab, point in enumerate(data):
        record = Record(id=ab, datetime=point[0], value=point[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data INSERTED, BABY!!!!!!'
