""" Main application and routing logic for aq_dashboard """
from flask import Flask, request, render_template
from .models import *
from .functions import *
import openaq
import pandas as pd
import datetime

#  instantiate an API object
open_api = openaq.OpenAQ() 

def create_app():
    """ create + config Flask app obj """
    app = Flask(__name__)

    #  configure the app object 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///openaq.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        message = ''
        over9s = Record.query.filter(Record.value > 9)
        over5s = Record.query.filter(Record.value > 5)
        recs = Record.query.filter(Record.id < 11)
        return render_template('base.html', message=message, over9s=over9s, over5s=over5s, recs=recs)

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        df_meas = open_api.measurements(city='Los Angeles', parameter='pm25', df=True)
        df_meas['date.utc'] = df_meas['date.utc'].astype(str)
        create_DB_records(df_meas)
        DB.session.commit()
        message = 'Data refreshed on: ' + str(datetime.datetime.now())
        over9s = Record.query.filter(Record.value > 9)
        recs = Record.query.filter(Record.id < 20)
        over5s = Record.query.filter(Record.value > 5)
        return render_template('base.html', message=message, over9s=over9s,  over5s=over5s, recs=recs)

    @app.route('/resetDB')
    def resetDB():
        DB.drop_all()
        DB.create_all()
        message = 'DB emptied!'
        return render_template('base.html', message=message)

    return app
