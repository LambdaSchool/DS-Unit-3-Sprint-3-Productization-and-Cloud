# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify

from web_app.models import db, User, Tweet, parse_records
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)


def store_twitter_user_data(screen_name):
    api = twitter_api_client()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150)

    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    print("STATUS COUNT:", len(statuses))
    basilica_api = basilica_api_client()
    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter += 1
    db.session.commit()

    return db_user, statuses


@twitter_routes.route("/users")
@twitter_routes.route("/users.json")
def list_users():
    db_users = User.query.all()
    users = parse_records(db_users)
    return jsonify(users)


@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    db_user, statuses = store_twitter_user_data(screen_name)
    return render_template("user.html", user=db_user, tweets=statuses)
