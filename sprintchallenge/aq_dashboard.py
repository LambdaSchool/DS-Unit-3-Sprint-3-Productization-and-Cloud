from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
api = openaq.OpenAQ()
DB = SQLAlchemy(app)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record {}, {}'.format(self.datetime,self.value)

@app.route('/')
def root():
    la_25 = get_data()
    commit_data(la_25)
    risks = Record.query.filter(Record.value > 10).all()
    records = Record.query.all()
    return render_template("base.html", risks=risks, records=records, la_25=la_25)

@app.route('/refresh')
def refresh():
    DB.drop_all()
    DB.create_all()
    la_25 = get_data()
    commit_data(la_25)
    risks = Record.query.filter(Record.value > 10).all()
    records = Record.query.all()

    return render_template('refresh.html', risks=risks, records=records)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # I think this is how to do Part4...
    risks = Record.query.filter(Record.value > 10).all()
    records = Record.query.all()

    return render_template("dashboard.html", risks=risks, records=records)

def commit_data(data):
    for record in data:
        if not DB.session.query(Record).filter(Record.datetime == record.datetime).first():
            DB.session.add(record)
    DB.session.commit()

def get_data():
    status, body = api.measurements(city="Los Angeles",parameter = 'pm25')
    la_25 = []
    api_data = [(record['date']['utc'], record['value'])
                    for record in body['results']]
    for record in api_data:
        la_25.append(Record(datetime=record[0], value=record[1]))

    return la_25