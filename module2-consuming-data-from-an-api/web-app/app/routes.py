from flask import current_app as app
from flask import render_template, url_for, redirect, request, flash, make_response
from .models import User, Tweet, db, T_User, T_Tweet
from app.Services.twitter_service import twitter_api_client
from app.Services.basilica_service import basilica_api_client

@app.route('/', methods = ['GET','POST'])
def home():
    print("yay it worked")
    return render_template("tweets.html")

@app.route('/create_tweet', methods=["POST"])
def create_tweet():
    name = request.form['Name']
    id = request.form["Id"]
    id_exist = User.query.filter_by(user_id=id).first()
    name_id_exist = User.query.filter_by(user_id=id, name=name).first()

    if id_exist:
        if name_id_exist:
            new_tweet = Tweet(tweet=request.form['Tweet'], user_id=request.form["Id"]) 
            db.session.add(new_tweet)
        else:
            return make_response("The name does not match the Id!")
    else:
        new_user = User(name=request.form['Name'], user_id=request.form["Id"])
        new_tweet = Tweet(tweet=request.form['Tweet'], user_id=request.form["Id"])
        db.session.add(new_user)
        db.session.add(new_tweet)

    db.session.commit()
    return redirect('/')

@app.route('/display_users', methods = ['GET'])
def display_users():
    users = User.query.all()
    return render_template("our_users.html", users=users)


@app.route('/<screen_name>')
def get_user(screen_name=None):
    # Instansiate twitter api class
    api = twitter_api_client()
    # grab username from url and create the api.get_user object
    twitter_user = api.get_user(screen_name)
    # Grab all the tweets from the username in the url
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    # Create a Twitter Username object if one doesn't exist already in the db
    db_user = T_User.query.get(twitter_user.id) or T_User(id=twitter_user.id)
    # Insert twitter screen name
    db_user.screen_name = twitter_user.screen_name
    # Insert twitter user name
    db_user.name = twitter_user.name
    # Insert twitter user location
    db_user.location = twitter_user.location
    # Insert twitter user follower count
    db_user.followers_count = twitter_user.followers_count
    # Add Twitter User Object into the db
    db.session.add(db_user)
    # Commit the changes onto the db
    db.session.commit()
    # Instansiate basilica api class
    basilica_api = basilica_api_client()
    # List comprehension that grabs all the tweets from status and puts it into full_text format
    all_tweets = [status.full_text for status in statuses]
    # Creates a list of all embedding values for each tweet in alL_tweets
    embeddings = list(basilica_api.embed_sentences(all_tweets, model="twitter"))
    # Iterate through each status in statuses
    
    # Create counter variable
    counter = 0
    for status in statuses:
        # create user twitter tweets object from the T_Tweet class if the id doesn't already exist in the db
        db_tweet = T_Tweet.query.get(status.id) or T_Tweet(id=status.id)
        # inserts the twitter user id as the tweet user id
        db_tweet.user_id = db_user.id
        # inserts the full tweet from the twitter user
        db_tweet.full_text = status.full_text
        # creates a variable that holds a single embedding value from a single tweet
        embedding = embeddings[counter]
        # inserts the embedding value from the user's tweet
        db_tweet.embedding = embedding
        # Add the changes to the db
        db.session.add(db_tweet)
        # Increase the counter by one to iterate through each tweet from the list
        counter+=1
    # commit changes
    db.session.commit()
    # Return string if everything worked properly
    return "User has been added to the data base!... hopefully..."