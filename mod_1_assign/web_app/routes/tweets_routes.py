# web_app/routes/tweets_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from web_app.models import Tweets, db

tweets_routes = Blueprint("tweets_routes", __name__)

@tweets_routes.route("/tweets.json")
@tweets_routes.route("/tweets_endpoint")
def list_tweets():
    tweets = [
        {"id": 1, "user_id" : 1, "tweet": "Boring Company completes 2nd Vegas tunnel https://t.co/13Hy3toyJR"},
        {"id": 2, "user_id" : 2, "tweet": "The best way to honor the legacy of Dr. Martin Luther King Jr. is to ensure kids understand his purpose, message and impact so that they can carry it forward.  This is a great way to start teaching them. #MLKDay   https://t.co/U5mWmgOFts"},
        {"id": 3, "user_id" : 3, "tweet": "I want to live in a world where a Chicken can cross the road without anybody questioning its motives."},
    ]
    return jsonify(tweets)

@tweets_routes.route("/tweets")
def list_tweets_for_humans():
    # tweets = [
    #     {"id": 1, "user_id" : 1, "tweet": "Boring Company completes 2nd Vegas tunnel https://t.co/13Hy3toyJR"},
    #     {"id": 2, "user_id" : 2, "tweet": "The best way to honor the legacy of Dr. Martin Luther King Jr. is to ensure kids understand his purpose, message and impact so that they can carry it forward.  This is a great way to start teaching them. #MLKDay   https://t.co/U5mWmgOFts"},
    #     {"id": 3, "user_id" : 3, "tweet": "I want to live in a world where a Chicken can cross the road without anybody questioning its motives."},
    # ]

    tweets_records = Tweets.query.all()
    print(tweets_records)

    return render_template("tweets.html", message="Here's some tweets", tweets=tweets_records)

@tweets_routes.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")

@tweets_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))

    new_tweet = Tweets(tweet=request.form["tweet"])
    db.session.add(new_tweet)
    db.session.commit()

    return jsonify({
        "message": "TWEET CREATED OK",
        "tweet": dict(request.form)
    })
    #flash(f"Book '{new_book.title}' created successfully!", "success")
    #return redirect("/books")