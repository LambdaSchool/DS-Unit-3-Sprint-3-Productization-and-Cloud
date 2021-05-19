# The init file indicates that the folder lives inside is like a python module 
# and facilitates the importing of certain files within that module within that directory.
# The other role that it plays, is it's the entry point. It's the first place to look into that module directory

# Imports
from flask import Flask
from web_app.models import db, migrate
from web_app.routes.tweets_routes import tweets_routes
from web_app.routes.home_routes import home_routes

DATABASE_URI = "sqlite:///C:\\Users\\jessi\\OneDrive\\Documents\\School\\Python\\Unit_3\\Sprint_3\\DS-Unit-3-Sprint-3-Productization-and-Cloud\\twitoff_development.db"

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tweets_routes)
    app.register_blueprint(home_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)