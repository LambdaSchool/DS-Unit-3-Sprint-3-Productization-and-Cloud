# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.users_routes import users_routes
from web_app.routes.tweets_routes import tweets_routes

#DATABASE_URI = "sqlite:///web_app_99.db" # using relative filepath
DATABASE_URI = "sqlite:////Users/Daniel/Desktop/Lambda/3_DS_Data_Engineering/3_Productization_and_Cloud/DS-Unit-3-Sprint-3-Productization-and-Cloud/mod_1_assign/assign_app.db" # using absolute filepath on Mac (recommended)
#DATABASE_URI = "sqlite:///C:\\Users\\Username\\Desktop\\your-repo-name\\web_app_99.db" # using absolute filepath on Windows (recommended) h/t: https://stackoverflow.com/a/19262231/670433

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(users_routes)
    app.register_blueprint(tweets_routes)
    
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)