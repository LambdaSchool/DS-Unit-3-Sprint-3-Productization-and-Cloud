"""
Retreive tweets, embeddings, and persist in the database
"""
import basilica 
import tweepy 
from decouple import config 
from .model import DB, Tweet, User

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))

TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_SECRET'))

TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

def add_or_update_user(username):
    """ Add or update user and their tweets, error if no/private_user"""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or 
            User(id=twitter_user.id, name=username))
        DB.session.add(db_user)
        # We want as many non-retweets or replies as we can get, only tweets
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False,
                                       tweet_mode='extended', since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            #get embedding for storing in DB
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e
    else:
        DB.session.commit()

# def add_user(users=TWITTER_USERS):
#     for user in users:
#         add_or_update_user(user)

def update_all_users():
    for user in User.query.all():
        add_or_update_user(user.name)
