from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .aq_dashboard import part2, part2_stretch


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    DB = SQLAlchemy(app)

    class Record(DB.Model):
        id = DB.Column(DB.Integer, primary_key=True)
        datetime = DB.Column(DB.String(25))
        value = DB.Column(DB.Float, nullable=False)

        def __repr__(self):
            return 'TODO - write a nice representation of Records'

    @app.route('/')
    def root():
        s0 = "\n--- PART2 BASELINE --- \n\n" + part2() + '\n\n'
        la, lo, ra = (30, 40, 3)
        #s1 = f"\n--- PART2 STRETCH with args coordinates: ({la}, {lo}), radius: {ra} --- \n\n" + part2_stretch(la, lo, ra)
        return s0  # + s1

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        # TODO Get data from OpenAQ, make Record objects with it, and add to db
        DB.session.commit()
        return 'Data refreshed!'

    return app
