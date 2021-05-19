# twitoff_app/__init__.py

from flask import Flask
from twitoff_app.models import db, migrate
from twitoff_app.routes.home_routes import home_routes
from twitoff_app.routes.book_routes import book_routes
from twitoff_app.routes.twitter_routes import twitter_routes
from twitoff_app.routes.stats_routes import stats_routes

#DATABASE_URI = "sqlite:///web_app_99.db" # using relative filepath
DATABASE_URI = "sqlite:////Users/Daniel/Desktop/Lambda/3_DS_Data_Engineering/3_Productization_and_Cloud/DS-Unit-3-Sprint-3-Productization-and-Cloud/sprint_3_lecture/twitoff_app.db" # using absolute filepath on Mac (recommended)

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    app.register_blueprint(twitter_routes)
    app.register_blueprint(stats_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)

