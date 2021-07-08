
from flask import Blueprint, jsonify, request, render_template, redirect, flash
from pdb import set_trace as st
from web_app.models import Tweet, User, db
from sqlalchemy.orm import joinedload


user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/")
def index():
    return redirect("/users/")


@user_routes.route("/users/")
def list_users():
    user_records = User.query.all()
    return render_template("users.html", users=user_records)


# @user_routes.route("/users/<username>/")
# def list_user_tweets(username=None):
#     user = User.query.filter_by(username=username).first()
#     user_id = user.id
#     user_tweets = Tweet.query.filter_by(user_id=user_id).all()
#     # st()
#     return render_template("user_tweets.html", username=username, user_tweets=user_tweets)


# @user_routes.route("/users/<username>/new_tweet", methods=["POST"])
# def user_create_new_tweet(username=None):
#     user = User.query.filter_by(username=username).first()
#     # st()
#     user_id = user.id
#     new_tweet = Tweet(user_id=user_id, text=request.form["tweet_text"])
#     db.session.add(new_tweet)
#     db.session.commit()
#     return redirect(f"/users/{username}/")


@user_routes.route("/users/new/")
def new_user():
    return render_template("new_user.html")


@user_routes.route("/users/create", methods=["POST"])
def create_user():
    new_user = User(screen_name=request.form["username"])
    print("FORM DATA:", dict(request.form))
    db.session.add(new_user)
    db.session.commit()
    # flash("asdf")
    return redirect("/users")
