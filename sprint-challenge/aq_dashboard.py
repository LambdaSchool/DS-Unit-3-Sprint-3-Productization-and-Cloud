"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask,  render_template
import openaq
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['ENV'] = 'debug'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    lat = DB.Column(DB.Float)
    lon = DB.Column(DB.Float)


    def __repr__(self):
        return '<Time :{}> <Date :{}>'.format(self.datetime,self.value)



@APP.route('/')
def root():
    """Base view."""
    my_query = DB.session.query(Record).filter(Record.value > 10)
    ret_list = []
    for q in my_query:
        _=(q.datetime,q.value)
        ret_list.append(_)
    pretty_list = []
    for r in ret_list:
        pretty_list.append('Date : {}, Time : {} and Value : {}'.format(r[0][:10],
                                        r[0][11:19],r[1]))
    #return str(ret_list)
    return render_template('base.html', datas=pretty_list)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    tup_list = []
    for res in body['results']:
        _=(str(res[u'date'][u'utc']), 
            str(res[u'value']))    
        tup_list.append(_)
        for tup in tup_list:
            db_data = Record(datetime = tup[0],value = tup[1])
            DB.session.add(db_data)
    DB.session.commit()
    return str(tup_list)

@APP.route('/latlong')
def latlong():
    """Pull fresh data from Open AQ including latitude and longitude."""
    #DB.drop_all()
    DB.create_all()
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    tup_list = []
    for res in body['results']:
        _=(str(res[u'date'][u'utc']), #datetime
            str(res[u'value']),     #value
            str(res[u'latitude']),     #latitude
            str(res[u'longitude']))     #longitude
        tup_list.append(_)
        for tup in tup_list:
            db_data = Record(datetime = tup[0],value = tup[1],
                                lat = tup[2], lon = tup[3])
            DB.session.add(db_data)
    DB.session.commit()
    return str(tup_list)
