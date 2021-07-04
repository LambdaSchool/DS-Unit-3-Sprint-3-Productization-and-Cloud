from decouple import config
from flask import Flask, render_template, request
from .models import DB, User

# make an app factory

def create_app():
    app = Flask(__name__)

    # add our config
    # 3 slashes make this a relative path
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')#'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ENV'] = config('ENV')
    # now have the database know about the app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html',title = 'Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset', users=[])

    return app
