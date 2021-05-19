# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.models import db, Tweets

tweets_routes = Blueprint("tweets_routes", __name__)

@tweets_routes.route("/tweets.json")
def list_tweets(): # my love for the office is vast lmao
    tweets = [
        {"id": 1, "Dwight Shrute": "Identiity theft is not a joke JIM."},
        {"id": 2, "Jim Halpert": "Bears. Beets. Battlestar Galactica."},
        {"id": 3, "Michael Scott": "DWIGHT. YOU IGNORANT SLUT"},
    ]
    return jsonify(tweets)

@tweets_routes.route("/tweets/new")
def new_tweet_form():
    return render_template("new_tweet.html")

@tweets_routes.route("/tweets/create", methods="POST")
def create_tweet():
    print("FORM DATA:", dict(request.form)) #> {"book_title": "___", "author_name": "____"}

    new_tweet = Tweets(tweet=request.form["tweets"], author_id=request.form["author_id"])
    db.session.add(new_tweet)
    db.session.commit()

    #return jsonify({
    #    "message": "TWEET CREATE OK",
    #    "book": dict(request.form)
    #})
    flash(f"Tweet '{new_tweet.title}' created successfully!", "dark")
    return redirect("/tweets")