from flask import Flask,  render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time :{}> <Date :{}>'.format(self.datetime, self.value)

@APP.route('/')
def root():
    # api = openaq.OpenAQ()
    # status, body = api.measurements(city='Los Angeles', parameter='pm25')
    # # utc_datetime = body['results'][1]['date']['utc']
    # # value = body['results'][1]['value']
    # # result = utc_datetime + "," +str(value)
    # # results = body['results'][:2]
    # # utc_datetime_value = []
    # # for result in results:
    # #     utc_datetime_value.append(str((result['date']['utc'],result['value'])))
    query = DB.session.query(Record).filter(Record.value > 10)
    result = []
    for q in query:
        results = (q.datetime, q.value)
        result.append(results)
    pret_list = []
    for r in result:
        pret_list.append('Date : {}, Time : {} and Value : {}'.format(r[0][:10], r[0][11:19], r[1]))
    #return str(result)
    return render_template('aq_dashboard.html', datas=pret_list)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    tuples = []
    for res in body['results']:
        results = (str(res[u'date'][u'utc']), str(res[u'value']))
        tuples.append(results)
        for tup in tuples:
            db_data = Record(datetime=tup[0], value=tup[1])
            DB.session.add(db_data)
    DB.session.commit()
    return str(tuples)
