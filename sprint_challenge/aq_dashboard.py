"""OpenAQ Air Quality Dashboard with Flask."""
import requests as r
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from .openaq_api import get_aq_data
from .model import DB, Record

def create_app():
        
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    DB.init_app(app)


    @app.route('/')
    def root():
        """Base view."""
        # query the database for any Record objects that have value greater or equal to 10
        # Stretch Goal - make it more usable: made response JSON for ease of scraping and data extensibility
        db_query = jsonify([rec.serialize() for  rec in Record.query.filter(Record.value >= 10).all()])
        return db_query


    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        # TODO Get data from OpenAQ, make Record objects with it, and add to db
        for data in get_aq_data():
            db_record = Record(datetime=str(data[0]), value=data[1])
            DB.session.add(db_record)
        DB.session.commit()
        return 'Data refreshed!'

    return app

if __name__ == '__main__':
    app.run()