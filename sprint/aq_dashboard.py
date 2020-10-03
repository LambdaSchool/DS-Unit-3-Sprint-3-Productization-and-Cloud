"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy, Model
from openaq import *

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


@APP.route('/', methods = ["GET"])
def root():
    """Base view."""
    tup = get_tup()
    return jsonify(tup)


class Record(Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __init__(self, id, datetime, value):
        self.id = id
        self.datetime = datetime
        self.value = value
        super(Record, self).__init__()

    def __repr__(self):
        return f"Record('{self.datetime}', '{self.value})'>"


def add_records():
    l = get_tup()
    DB.create_all()
    k = 0
    for i in l:
        new_rec = Record(id=k,datetime=i[0],value=i[1])
        DB.session.add(new_rec)
        DB.session.commit()
        k+=1
    return


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    add_records()
    
    return 'Data refreshed!'


def get_products():
    vals = Record.query.filter(Record.value >= 10).all()
    return vals

if __name__ == "__main__":
    APP.run(debug=True)