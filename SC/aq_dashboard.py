"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import openaq
import dash
import dash_core_components as dcc
import dash_html_components as html

#def create_app():
APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB = SQLAlchemy(APP)
api = openaq.OpenAQ()


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '[id:{}, time: {}, value:{}]'.format(self.id,
                                                    self.datetime, self.value)


@APP.route('/')
def root():
    """Base view."""
    instance = Record.query.filter(Record.value >= 10).all()
    return render_template('base.html', title='Home', instance=instance)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    server=APP,
    routes_pathname_prefix='/dash/'
)

app.layout = dcc.Graph(
    id='air-graph',
    figure={
        'data': {'x': Record.datetime, 'y': Record.value, 'type': 'scatter'},
        'layout': {
            'title': 'Air quality in LA'
        }
    },
)


@APP.route('/refresh')
def refresh():
    '''Pull fresh data from Open AQ and replace existing data.'''
    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    for result in body['results']:
        utc = result['date']['utc']
        value = result['value']
        db_record = Record(datetime=utc, value=value)
        DB.session.add(db_record)
    DB.session.commit()
    return'Data refreshed!'
