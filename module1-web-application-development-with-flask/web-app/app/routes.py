from flask import current_app as app
from flask import render_template, url_for, redirect, request, flash
from .models import User, Tweet, db

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
            flash("This name does not match the Id!")
    else:
        new_user = User(name=request.form['Name'], user_id=request.form["Id"])
        new_tweet = Tweet(tweet=request.form['Tweet'], user_id=request.form["Id"])
        db.session.add(new_user)
        db.session.add(new_tweet)

    db.session.commit()
    return redirect('/')