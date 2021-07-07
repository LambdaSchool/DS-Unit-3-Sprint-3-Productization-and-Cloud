from flask import Flask, render_template, request
import openaq
from flask_sqlalchemy import SQLAlchemy
"""
api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
"""
api = openaq.OpenAQ()

APP = Flask(__name__)

@APP.route('/')
def root():
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	value_datetime = []
	for result in body['results']:
		value = result['value']
		#value = str(value)
		utc_datetime = result['date']['utc']
		#utc_datetime = str(utc_datetime)
		value_datetime.append((utc_datetime, value))
	
	return str(value_datetime)

@APP.route('/risky')
def risky():
	risky_place = Record.query.filter(Record.values >= 10).all()
	return render_template('riskly.html', risky_place=risky_place)


"""
@APP.route('/date')
def date_display():
	api = openaq.OpenAQ()
	status, body = api.measurements(city='Los Angeles', parameter='pm25')
	body_lst = body['results'][:100]
	utc_datetime = [d['date']['utc'] for d in body_lst]
	utc_datetime = str(utc_datetime)
	return utc_datetime
"""
# Tina I did this separately above because the root() would not return both the utc_datetime
# and value.  I don't know why.



APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    values = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<datetime: {}, value: {}'.format(self.datetime, self.values)


@APP.route('/refresh')
def refresh():
	DB.drop_all()
	DB.create_all()
	# TODO Get data from OpenAQ, make Record objects with it, and add to db
	value_datetime = root()
	

	for value in value_datetime:
		db_value = Record(datetime=value[0], values=value[1])
		DB.session.add(db_value)
	
	DB.session.commit()
	return 'Data refreshed!'

# Tina when I try to create a DataBase with the /refresh I get this error:
"""
sqlalchemy.exc.InterfaceError: (sqlite3.InterfaceError) Error binding parameter 0 - probably unsupported type. [SQL: 'INSERT INTO record (id, value) VALUES (?, ?)'] [parameters: (<built-in function id>, 2.0)] (Background on this error at: http://sqlalche.me/e/rvf5)
127.0.0.1 - - [08/Mar/2019 10:43:52] "GET /refresh HTTP/1.1" 500 -
"""

