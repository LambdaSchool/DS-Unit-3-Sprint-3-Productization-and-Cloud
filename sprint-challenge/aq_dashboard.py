from flask import Flask, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

def getLaData():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    return status, body

@APP.route('/')
def index():
    res = Record.query.filter(Record.value >= 10).all()
    return render_template('index.html', res=res)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"< Time {self.datetime} --- Value {self.value} >"

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()

    data = getLaData()
    for d in data[1]['results']:
        DB.session.add(Record(datetime=str(d['date']['utc']), value=d['value']))
        DB.session.commit()
    return 'Data refreshed!'

if __name__ == '__main__':
    APP.run(debug=True)

