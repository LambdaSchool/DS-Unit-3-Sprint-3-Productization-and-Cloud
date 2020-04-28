"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

# api connection and measurements
api = openaq.OpenAQ()
stats, body = (api.measurements(
	city='Los Angeles',
	parameter='pm25'
	)
)

la_pm25 = []
# web app page
@APP.route('/')
def root():
    """Create list of tuples of Los Angeles Data collection
    of date and value"""
    # la_pm25 = []
    for item in body['results']:
    	tuple_date = item['date']['utc']
    	tuple_value = item['value']
    	timing = (tuple_date, tuple_value)
    	timing = tuple(timing)
    	la_pm25.append(timing)
        # making index return into query that shows
        # values >= 10 as string
    return str(Record.query.filter(Record.value >= 10).all())

"""Part 3"""

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time ' + str(self.datetime) + ' --- Value ' + str(self.value) + '>' 


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from la_pm25,
    for item in la_pm25:
    	# for loop taking data from tuples and parsing into 
    	# Record datetime and Record value objects with it,
    	item_datetime = str(item[0])
    	item_value = str(item[1])
    	record = Record(datetime=item_datetime,
    		value=item_value) 
    # and add/commit to db
    	DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'