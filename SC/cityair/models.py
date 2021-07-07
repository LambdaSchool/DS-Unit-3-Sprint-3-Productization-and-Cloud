"""SQLAlchemy models for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Measurement(DB.Model):
    """Pulling city air quality particulate PM2.5"""
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(50), nullable=True )
    country = DB.Column(DB.String(2), nullable=True)
    location = DB.Column(DB.String(80),nullable=True)
    parameter = DB.Column(DB.String(10), nullable=True)
    date_utc = DB.Column(DB.String(10), nullable=True)
    date_local = DB.Column(DB.String(10), nullable=True)
    pm25 = DB.Column(DB.Float)
    unit = DB.Column(DB.String(10),nullable=True)
    latitude = DB.Column(DB.Float)
    longitude = DB.Column(DB.Float)

    def __repr__(self):
        return '<Measurement {}>'.format(self.name)

