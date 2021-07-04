"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = openaq.OpenAQ()

def check_status():
    status, body = api.cities()
    if not status == 200:
        raise ConnectionError('Connection status not equal to 200, connection error:',status)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        
        return '<Datetime {} \n PM 2.5 value {}>'.format(self.datetime, self.value)

@APP.route('/', methods=['GET','POST'])
def root():
    """Base view."""
    date_val = []
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for i in range(100):
        utc_datetime = body['results'][i:i+1][0]['date']['utc']
        value = body['results'][i:i+1][0]['value']
        temp_tuple = (utc_datetime, value)
        date_val.append(temp_tuple)
    filter = Record.query.filter(Record.value>=10).all()
    return render_template('home.html', filter=filter)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    date_val = []
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for i in range(100):
        utc_datetime = body['results'][i:i+1][0]['date']['utc']
        value = body['results'][i:i+1][0]['value']
        temp_tuple = (utc_datetime, value)
        date_val.append(temp_tuple)
    for i in date_val:
      db_record = Record(datetime=i[0], value=i[1])
      DB.session.add(db_record)

    DB.session.commit()
    return 'Data refreshed!'



if __name__ == '__main__':
    app.run(debug=True)