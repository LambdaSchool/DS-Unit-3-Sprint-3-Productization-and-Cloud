
import openaq
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randint

''' #!$#!$#!$#!$#!@$#@!$#@!

GETS, REQUESTS, ETC.

$#!$#!$#!$#!'''


def rtrn_val_utcdt(r) -> str:
    values = [x['value'] for x in r['results']]
    udt = [x['date']['utc'] for x in r['results']]

    return str(list(zip(values, udt)))


'''
    Import and set up the API object in your aq_dashboard.py file
    Retrieve the data from the API when the main route is called
    Create a list of (utc_datetime, value) tuples, e.g. the first two tuples for the data returned above would be: [('2019-03-08T00:00:00.000Z', 8.13), ('2019-03-07T23:00:00.000Z', 8.13)]
    Return this list in the main route, so loading the web application prints the raw list of tuples of datetimes and values
'''


def part2() -> str:
    api = openaq.OpenAQ()

    status, resp = api.measurements(city='Los Angeles', parameter='pm25')

    return rtrn_val_utcdt(resp)


def part2_stretch(lati: float, lngi: float, radi: float) -> str:
    api = openaq.OpenAQ()

    status, resp = api.measurements(coordinates=(
        lati, lngi), radius=radi, date_from='2015-12-20', date_to='2015-12-29')

    return rtrn_val_utcdt(resp)


''' %$@%$@%$@#%$@#%$@%42

THE APP

%$@%$@%$@%$@%$@'''

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)
    city = DB.Column(DB.String(40))

    def __repr__(self):
        return f'<value: {self.value}, utc_date: {self.datetime} >'


@app.route('/')
def root():
    s0 = "\n------ PART2 BASELINE ------ \n\n" + part2() + '\n\n'
    la, lo, ra = (30, 40, 3)
    #s1 = f"\n--- PART2 STRETCH with args coordinates: ({la}, {lo}), radius: {ra} --- \n\n" + part2_stretch(la, lo, ra)
    return s0  # + s1


def add_or_update_valudts(city):

    try:
        api = openaq.OpenAQ()
        status, resp = api.measurements(city=city, parameter='pm25')
        values = [x['value'] for x in resp['results']]
        udts = [x['date']['utc'] for x in resp['results']]

        for v, d in zip(values, udts):
            DB.session.add(Record(value=v, datetime=d,
                                  city=city, id=randint(10**9, 10**10)))
    except Exception as e:
        print("some issue", e)
    else:
        DB.session.commit()


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data.

    This creates a SQLite database with a Record table suitable for holding the list of tuples you created in part 2. Use that logic/list, and add all the pulled records to the database. As the Record class indicates, store the datetime as a string - SQL does support native datetime objects, and as a stretch goal you can explore and try to implement that.

    """
    DB.drop_all()
    DB.create_all()

    add_or_update_valudts("Los Angeles")
    add_or_update_valudts("Buenos Aires")
    add_or_update_valudts("Dubai")

    return 'Data refreshed!'


@app.route('/risky')
def risky():
    ''' Now that your data is in a database, revisit your main route - instead of pulling all data live, query the database for any Record objects that have value greater or equal to 10. The filter method of SQLALchemy queries will be invaluable for this.

Finally, return this filtered list of "potentially risky" PM 2.5 datetime/value tuples. You now have a (very basic) dashboard, that stores, updates, and displays useful data!'''
    refresh()
    x = Record.query.filter(Record.value >= 8).all()
    return str(x)
