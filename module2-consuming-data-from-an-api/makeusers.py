#!/usr/bin/env python3

from TWITOFF.models import *
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.sqlite3'
DB.init_app(app)

with app.app_context():

    # Drop existing tables
    DB.drop_all()
    DB.create_all()
    
    
    # Create users:
    
    
    u1 = User(name='Abby')
    u2 = User(name='Bobert')
    u3 = User(name='Cassidy')
    
    # "tweets" randomly scraped from wikipedia
    t1 = "FC ViOn Zlaté Moravce is a Slovak football team, based in the town of Zlaté Moravce. The club was founded on 22 January 1995. During the 2014/15 campaign they will be competing in the Slovak Super Liga."
    
    t2 = "Currently the former NATO base is being developed as an international cargo and transport facility (Aeroport de Vatry).  Very little remains of the old USAF base."
    
    t3 = "The Irish Schoolboys side represents the nation against youths of other nations."
    
    t4 = "Then, in his letter of 26 July 1669, Louvois orders Captain De Vauroy, Major of the citadel of Dunkirk, to take the prisoner Dauger to Pignerol. The content of the letters (and the explanatory « loose sheets » which would have accompanied it, which was a common practice at that time) suggests that Louvois also ordered Vauroy not to inform his military superior, the Count of Estrades, of the purpose of his mission, under the false pretext of the deportation of Spanish deserters."
    
    t5 = "Lennart Eberson was son of shop manager Ebbe Eberson and Margit Eberson, née Fardrup. Married in 1957 to Anne-Marie Hansson, daughter of accountant Hilding Hansson and Margareta Hansson, née Lundgren."
    
    t6 = "Rai's third and former logo was used from 1982 to 30 September 2000"
    
    tweet1 = Tweet(text=t1)
    tweet2 = Tweet(text=t2)
    tweet3 = Tweet(text=t3)
    tweet4 = Tweet(text=t4)
    tweet5 = Tweet(text=t5)
    tweet6 = Tweet(text=t6)
    
    # append tweets to users
    
    u1.tweets.append(tweet1)
    u1.tweets.append(tweet2)
    u2.tweets.append(tweet3)
    u2.tweets.append(tweet4)
    u3.tweets.append(tweet5)
    u3.tweets.append(tweet6)
    
    # Add all objects to session to create db
    DB.session.add(u1)
    DB.session.add(u2)
    DB.session.add(u3)
    DB.session.add(tweet1)
    DB.session.add(tweet2)
    DB.session.add(tweet3)
    DB.session.add(tweet4)
    DB.session.add(tweet5)
    DB.session.add(tweet6)
    
    
    DB.session.commit()
