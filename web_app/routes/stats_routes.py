# web_app/routes/stats_routes.py

from flask import Blueprint, request, render_template
from sklearn.linear_model import LogisticRegression
from web_app.models import User
from web_app.services.basilica_service import basilica_api_client

stats_routes = Blueprint("stats_routes", __name__)


@stats_routes.route("/predict", methods=["POST"])
def predict():
    print("PREDICT ROUTE...")
    print("FORM DATA:", dict(request.form))
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    print("-----------------")
    print("FETCHING TWEETS FROM THE DATABASE...")
    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets
    print("USER A", user_a.screen_name, len(user_a.tweets))
    print("USER B", user_b.screen_name, len(user_b.tweets))

    print("-----------------")
    print("TRAINING THE MODEL...")
    embeddings = []
    labels = []
    for tweet in user_a_tweets:
        labels.append(user_a.screen_name)
        embeddings.append(tweet.embedding)

    for tweet in user_b_tweets:
        labels.append(user_b.screen_name)
        embeddings.append(tweet.embedding)

    classifier = LogisticRegression(random_state=0, solver='lbfgs')  # for example
    classifier.fit(embeddings, labels)

    print("-----------------")
    print("MAKING A PREDICTION...")

    basilica_conn = basilica_api_client()
    example_embedding = basilica_conn.embed_sentence(tweet_text, model="twitter")
    result = classifier.predict([example_embedding])

    return render_template("results.html",
                           screen_name_a=screen_name_a,
                           screen_name_b=screen_name_b,
                           tweet_text=tweet_text,
                           screen_name_most_likely=result[0]
                           )
