# web_app/routes/home_routes.py

from flask import Blueprint, render_template

home_routes = Blueprint("home_routes", __name__)


@home_routes.route("/")
def index():
    print("VISITED THE HOME PAGE")
    return render_template("prepare_to_predict.html")


@home_routes.route("/hello")
def hello():
    print("VISITED THE HELLO PAGE")
    return "Hello World!"


@home_routes.route("/about")
def about():
    print("VISITED THE ABOUT PAGE")
    return "About Me!"
