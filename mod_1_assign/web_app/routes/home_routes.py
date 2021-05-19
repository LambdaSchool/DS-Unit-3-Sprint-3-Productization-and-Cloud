# web_app/routes/home_routes.py

from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    return "Welcome to our twitoff, hosted by lambda school students!"

@home_routes.route("/about")
def about():
    return "Here we will be creating a dataframe of usernames and a dataframe of their tweets."