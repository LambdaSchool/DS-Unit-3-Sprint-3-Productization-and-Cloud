# twitoff_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify
from twitoff_app.models import db, User, Tweet, parse_records
from twitoff_app.services.twitter_service import twitter_api_client
from twitoff_app.services.basilica_service import connection as basilica_connection

twitter_routes = Blueprint("twitter_routes", __name__)


@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    api = twitter_api_client()

    twitter_user = api.get_user(screen_name)
    # statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=500, exclude_replies=False, include_rts=True)

    print("STATUSES COUNT:", len(statuses))
    #return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()
    #return "OK"
    #breakpoint()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_connection.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_client.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()
    # breakpoint()
    return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets

@twitter_routes.route("/users")
def print_users():
    user_records = User.query.all()[:10]
    tweet_records = Tweet.query.all()[:10]

    return render_template("user.html", user=user_records, tweets=tweet_records)