from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user

from dotenv import load_dotenv
load_dotenv()

# make an app factory
def create_app():
    app = Flask(__name__)

    # add our config
    # 3 slashes make this a relative path
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')#'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # now have the database know about the app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message = ''
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} sucessfully added!'
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    # add in a route for predictions
    @app.route('/compare', methods=['POST'])
    def compare():
        message = ''
        user1, user2 = sorted([request.values['user1'], request.values['user2']])

        if user1 == user2:
            message = "Cannot compare a user to themselves"
        else:
            tweet_text = request.values['tweet_text']
            prediction = predict_user(user1, user2, tweet_text)
            message = f""""{request.values['tweet_text']}" is more likely to be said by
            {user1 if prediction else user2} than {user2 if prediction else user1}"""
        return render_template('prediction.html', title='Prediction', message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    return app
