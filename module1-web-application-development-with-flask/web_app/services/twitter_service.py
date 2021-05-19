import os
from dotenv import load_dotenv
from tweepy import OAuthHandler, API

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_acess_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = API(auth)
print("API CLIENT:", api)

user = api.get_user("britnelikecafe")
print("TWITTER USER:", type(user))
print(user.id)
print(user.screen_name)
print(user.name)

tweets = api.user_timeline("britnelikecafe")
print("TWEETS", type(tweets))
print(type(tweets[0])) 

breakpoint()
tweet = tweets[0]
print(tweet.id)
print(tweet.text)