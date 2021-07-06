from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq

app = Flask(__name__)
db = SQLAlchemy()
openaq_api = openaq.OpenAQ()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    city = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.String(25))
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Record id={} city={} datetime={} value={}>'.format(self.id, self.city, self.datetime, self.value)

db.init_app(app)
db.create_all(app=app)

def particular_matter_samples(city):
    status, response = openaq_api.measurements(city=city, parameter='pm25')
    air_samples = response['results']
    
    if status != 200:
        return []

    return [(sample['date']['utc'], sample['city'], sample['value']) for sample in air_samples]

@app.route('/')
@app.route('/<city>')
def index(city='los-angeles'):
    city = ' '.join([word.capitalize() for word in city.split('-')])
    samples = Record.query.filter(Record.city == city).filter(Record.value >= 10).order_by(Record.value.desc()).all()

    return render_template('samples.html', samples=samples, city=city) 

@app.route('/refresh')
@app.route('/refresh/<city>')
def refresh(city='los-angeles'):
    destination = '/{}'.format(city)

    city = ' '.join([word.capitalize() for word in city.split('-')])
    samples = particular_matter_samples(city)
    records = [Record(datetime=date, city=city, value=measurement) for date, city, measurement in samples]	

    db.session.add_all(records)
    db.session.commit()

    return redirect(destination, 302) 
