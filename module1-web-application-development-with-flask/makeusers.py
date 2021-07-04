#!/usr/bin/env python3

from TWITOFF.models import *
from flask import Flask
import requests
from bs4 import BeautifulSoup
from numpy.random import choice


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.sqlite3'
DB.init_app(app)

with app.app_context():
        
    
    # generate random text from wikipedia
    def random_wiki():
        source = requests.get("https://en.wikipedia.org/wiki/Special:Random").text
        soup = BeautifulSoup(source,'html.parser')
        title = soup.find('title')
        paragraphs = soup.find_all('p',text=True)
                            # text=True. Ignores all the hyperlink
        plist = []
        for i in paragraphs:
            if len(list(i.text)) > 0 and i.text != '\n':
                plist.append(i.text)
    
        if len(plist) < 1:
            random_wiki()
    
        rand = choice(plist)
        return rand
    
    def generate_tweets(u):
        text1, text2 = random_wiki(), random_wiki()
        tweet1 = Tweet(text=text1)
        tweet2 = Tweet(text=text2)
        u.tweets.append(tweet1)
        u.tweets.appnd(tweet2)
    
        DB.session.add(u)
        DB.session.add(tweet1)
        DB.session.add(tweet2)
        
    
    # Drop existing tables
    DB.drop_all()
    DB.create_all()
    
    
    # Create users:
    
    USERS = list('Abby Bobert Cedric')
    
    for USER in USERS:
        u = User(name=USER)
        generate_tweets(u)
    
    DB.session.commit()
