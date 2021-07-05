"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from openaq import OpenAQ
from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col

APP = Flask(__name__)

@APP.route('/')
def root():
    """Base view."""
    class ItemTable(Table):
        datetime = Col('datetime')
        value = Col('value')
        city = Col('city')
    items = Record.query.filter(Record.value >= 10).all()
    # # Populate the table
    table = ItemTable(items)
    # Print the html
    return table.__html__()

# @APP.route('/mostpolluted')
# def most_polluted():
# # Declare your table
#     class ItemTable(Table):
#         datetime = Col('datetime')
#         value = Col('value')
#         city = Col('city')
#     items = Record.query.all()
#     # Populate the table
#     table = ItemTable(items)
#     # Print the html
#     return table.__html__()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    city = DB.Column(DB.String(50))

    def __repr__(self):
        st = 'Time {} --- Value {} -- City {}'
        return st.format(self.datetime, self.value, self.city)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api = OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    # List of tuples
    # [(i['date']['utc'], i['value']) for i in body['results']]
    ids = [i for i in range(len(body['results']))]
    dates =[i['date']['utc'] for i in body['results']]
    values =[i['value'] for i in body['results']]
    cities = [i['city'] for i in body['results']]
    for i, d, v, c in zip(ids, dates, values, cities):
        record = Record(id=i, datetime=d, value=v, city=c)
        DB.session.add(record)
        DB.session.commit()
    return 'Data refreshed!'
