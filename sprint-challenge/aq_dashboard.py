"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from tabulate import tabulate
import openaq


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(app)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"< Time {self.datetime} --- Value {self.value} >"
        
    #def __iter__(self):
    #    return f"< Time {self.datetime} --- Value {self.value} >"

class CityRecord(DB.Model):
    """
    Record for City data from OpenAQ
    """
    id = DB.Column(DB.Integer, primary_key=True)
    city = DB.Column(DB.String(250))
    count = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f"< City {self.city} --- Count {self.count} >"


def extract_utc_value(records):
    #print(records)
    date_value_pair = [(r['date']['utc'], r['value']) for r in records]
    
    return date_value_pair
    
@app.route("/query")
def index():
    """
    query for LA PM2.5
    """
    return render_template('index.html')

@app.route("/result", methods = ['POST'])
def result():
    """
    displaying query results for LA PM2.5
    """
    if request.method == 'POST':
        # screw error checking.
        f = request.form.to_dict()
        f = f['pm25']
     
    out = Record.query.filter(Record.value >= float(f)).all()
    #print(type(out))
    #print(out)
    #print(tabulate(list(out), tablefmt='html'))

    return render_template('results.html', prediction=out)
    
@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api = openaq.OpenAQ()
    
    # query LA pm25
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    if status == 200:
        pm25 = extract_utc_value(body['results'])
        for r in range(len(pm25)):
            DB.session.add(Record(id = r, datetime=pm25[r][0], value=pm25[r][1]))
    else:
        return f"ERROR: Unable to retrieve from API, status {status}"
        
    # query city name and counts
    status, body = api.cities()
    if status == 200:
        cities = body['results']
        for r in range(len(cities)):
            DB.session.add(CityRecord(id = r, city=cities[r]['city'], count=cities[r]['count']))
    else:
        return f"ERROR: Unable to retrieve from API, status {status}"
    # TODO
    DB.session.commit()
    return 'Data refreshed!'

@app.route('/refresh_cities')
def refresh_cities():
    """
    Displaying city query from OpenAQ
    """
    api = openaq.OpenAQ()
    status, body = api.cities()
    if status == 200:
        return str(body['results'])
    else:
        return f"ERROR: Unable to retrieve from API, Status {status}"

@app.route('/cities')
def cities():
    """
    Displaying city query from database with data 
    pulled from OpenAQ
    """
    out = CityRecord.query.all()
    return str(out)

@app.route('/')
def root():
    """Base view."""
    out = Record.query.filter(Record.value >= 10).all()
    
    return str(out)
    
    
if __name__ == "__main__":
    app.run(debug = True)