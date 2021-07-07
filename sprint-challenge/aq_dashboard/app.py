"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from .openaq import *

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Date {} , Value {}'.format(self.datetime, self.value)





def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)



    @app.route('/')

    def root():
        """Base view."""
        api = OpenAQ()
        l =list()
        status, body = api.measurements(city='Los Angeles', parameter='pm25')
        for i in body['results']:
            l.append((i['date']['utc'],i['value']))

        result = Record.query.filter(Record.value>=10).all()
        return str(l)

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()

        api = OpenAQ()
        l = list()
        status, body = api.measurements(city='Los Angeles', parameter='pm25')
        for i in body['results']:
            l.append((i['date']['utc'], i['value']))

        # TODO Get data from OpenAQ, make Record objects with it, and add to db
        for i in l:
            db_record = Record(datetime=i[0],value=i[1])
            DB.session.add(db_record)
        DB.session.commit()
        return 'Data refreshed!'

    return app