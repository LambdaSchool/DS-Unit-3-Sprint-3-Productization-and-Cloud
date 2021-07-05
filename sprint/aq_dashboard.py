"""OpenAQ Air Quality Dashboard with Flask."""
from decouple import config 
from flask import Flask, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Record
import requests
import openaq
import pandas


app = Flask(__name__)
api = openaq.OpenAQ()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)
DB.init_app(app)

@app.route('/')
def root():
    data1 = api.measurements(city='Los Angeles', parameter='pm25')
    return render_template('home.html', data1=data1)

@app.route('/load')
def get_data():
    data = api.measurements(city='Los Angeles', parameter='pm25', df=True)
    for index, row in data.iterrows():
        records = Record(datetime=row['date.utc'], value=row['value'])
        DB.session.add(records)
        DB.session.commit()

@app.route('/refresh')
def refresh():
    DB.drop_all()
    DB.create_all()
    DB.session.commit()
    return 'Data refreshed!'

if __name__ == '__main__':
    app.run(port=5000,debug=True)