"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
import openaq
from .openaq import DB, Record



def create_app():
    """create and configure an instance of the flask application"""
    APP = Flask(__name__)
    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(APP)


    @APP.route("/")
    def root():
        """Base view"""
        records = Record.query.filter(Record.value >= 10.0).all()
        return render_template("layout.html", title=records)

    @APP.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        add_record()
        DB.session.commit()
        return 'Data refreshed!'


    return APP

def answers():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    l = []
    for i in range(len(body['results'])):
        a = list(body['results'][i].values())[2:4]
        date, value = list(a[0].values())[0], a[1]
        t = (date, value)
        l.append(t)
    return l

def add_record():
    a = answers()
    for i in range(len(a)):
        db_record = Record(id=i, datetime=a[i][0], value=a[i][1])
        DB.session.add(db_record)
    DB.session.commit()
