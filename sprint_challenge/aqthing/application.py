"""OpenAQ Air Quality Dashboard with Flask."""
from aqthing import openaq
from flask import Flask, render_template
from .aq_dashboard import DB, Record


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        """Base view."""
        api = openaq.OpenAQ()
        status, body = api.measurements(city='Los Angeles', parameter='pm25')
        results = body['results']
        for result in results:
            time = result['date']['local']
            pm = result['value']
            new = Record(datetime=str(time), value=pm)
            DB.session.add(new)
        DB.session.commit()
        highs = Record.query.filter(Record.value >= 10).all()
        return render_template('display.html',
                               highs=highs)
    return app
