"""SQLAlchemy models for OpenAQ dashboard."""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(2))
    city = db.Column(db.String(25))
    location = db.Column(db.Text)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<Record (country='{}', city='{}', location='{}', datetime='{}', value='{}')>".format(self.country, self.city, self.location, self.datetime, self.value)
