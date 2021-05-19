# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template #, flash, redirect

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def hello():
    return "Hello everyone and welcome to Twitoff!"