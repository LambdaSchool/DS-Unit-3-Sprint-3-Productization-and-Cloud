import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

def twitter_api_client():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    print("AUTH", auth)
    api = tweepy.API(auth)
    print("API", api)
    #print(dir(api))
    return api

if __name__ == "__main__":

    api = twitter_api_client()
    user = api.get_user("spidadmitchell")
    print("USER", user)
    print(user.screen_name)
    print(user.name)
    print(user.followers_count)

    statuses =  api.user_timeline("spidadmitchell", tweet_mode="extended", count=150, exclude_replies="T")
    status = statuses[0]
    print(dir(status))
    print(status.id)
    print(status.full_text)

    for status in statuses:
        print("----")
        print(status.full_text)

        #public_tweets = api.home_timeline()
        #
        #for tweet in public_tweets:
        #    print(type(tweet)) #> <class 'tweepy.models.Status'>
        #    #print(dir(tweet))
        #    print(tweet.text)
        #    print("-------------")