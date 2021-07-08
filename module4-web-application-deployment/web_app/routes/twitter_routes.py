from flask import Blueprint, render_template, jsonify
from web_app.services.twitter_service import twitter_api
from web_app.services.basilica_service import basilica_api_client
from web_app.models import User, Tweet, db
from pdb import set_trace as st

twitter_routes = Blueprint("twitter_routes", __name__)


@twitter_routes.route("/users/<screen_name>/")
def get_user(screen_name=None):
    print(screen_name)
    api = twitter_api()
    user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    # return jsonify({"user": user._json, "tweets": [s._json for s in statuses]})

    db_user = User.query.get(user.id) or User(id=user.id)
    db_user.screen_name = user.screen_name
    db_user.name = user.name
    db_user.location = user.location
    db_user.followers_count = user.followers_count
    db.session.add(db_user)
    db.session.commit()
    #breakpoint()

    all_tweet_texts = [status.full_text for status in statuses]
    # st()
    basilica_connection = basilica_api_client()
    embeddings = list(basilica_connection.embed_sentences(sentences=all_tweet_texts, model="twitter"))
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
    #breakpoint()
    return "OK"
