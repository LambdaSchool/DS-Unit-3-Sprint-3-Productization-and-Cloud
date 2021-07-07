"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request, url_for, redirect
from decouple import config
from .models import db, Record
from .openaq import OpenAQ, ApiError


def create_app():
    """Create and configure and instance of flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Initialize database with app instance
    api = OpenAQ()  # Initialize OpenAQ api instance

    @app.route('/')
    def root():
        """Home Page"""
        db_records = Record.query.all()
        if not db_records:
            add_or_update_records(get_records(api))
        # Filter "potentially risky" records
        value = 10
        records = Record.query.filter(Record.value >= value)
        return render_template('base.html', title='Home', records=records)

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from OpenAQ and replace existing data."""
        records = Record.query.all()
        add_or_update_records(get_records(api))
        return render_template('base.html', title='Home', records=records, message='Records Refreshed!')
    return app


def get_records(api, city='Los Angeles', parameter='pm25', country=None):
    """Fetches measurements from OpenAQ `/measurements` REST API endpoint for a a given Country, City, and parameter type, and instanciates them as records of Record table."""

    if country is None:
        status, body = api.measurements(
            city=city, parameter=parameter)
    else:
        status, body = api.measurements(country=country,
                                        city=city, parameter=parameter)
    if not status == 200:
        raise ApiError(f'API Response error, status: {status}')

    records = []
    for row in body['results']:
        record = Record(country=row['country'], city=row['city'],
                        location=row['location'], datetime=row['date']['utc'], value=row['value'])
        records.append(record)
    return records


def add_or_update_records(records):
    """Adds measurements to the Record table of the database."""
    try:
        # Loop through records, and update if no new records found
        for record in records:
            if not db.session.query(Record).filter(Record.datetime == record.datetime).first():
                db.session.add(record)
    except Exception as e:
        print('Error processing {}: {}'.format(e))
        raise e
    else:
        # If no errors happend than commit the records
        db.session.commit()
