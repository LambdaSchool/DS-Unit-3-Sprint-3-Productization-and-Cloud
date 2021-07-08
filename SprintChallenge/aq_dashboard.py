"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from flask_sqlalchemy import SQLAlchemy





APP = Flask(__name__)

"""#object for calling API
api = openaq.OpenAQ()

#structures for storing API call return values
status, body = api.measurements(city='Los Angeles', parameter='pm25')

#Tuples from the first API call
value_pair1 = (body['results'][0]['date']['utc'], body['results'][0]['value'])
value_pair2 = (body['results'][1]['date']['utc'], body['results'][1]['value'])"""


#assigning a file path to the sqllite db
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)



class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {} ------ Value: {}>'.format(self.datetime, self.value)




@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')

    for item in body['results']:
        n_record = Record(datetime=item['date']['utc'], value=item['value'])
        DB.session.add(n_record)


    DB.session.commit()
    return 'Data refreshed!'






@APP.route('/')
def root():
    """Base view."""
   
    risky_pm25 = Record.query.filter(Record.value >= 10.0).all()

    #risky_pm25 = ' '.join(str(x) for x in risky_pm25)
    
  
    
  
    return render_template('base.html', title='Home', records=risky_pm25)