#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 14:58:35 2019

@author: ggash


following
https://www.youtube.com/watch?v=MwZwr5Tvyxo
https://www.youtube.com/watch?v=QnDWIZuWYW0

Python Flask Tutorial: Full-Featured Web App Part 1 - Getting Started
Corey Schafer

"decorators"
a way to add additional functionality to functions

note: these two work the same way
    http://127.0.0.1:5000/
    http://localhost:5000/

# make directory
mkdir Flask_Blog

it is not entirely clear which of these can be run in
python e.g. with a !

# this does not have to be run each time .py is modified
!export FLASK_APP=flaskblog.py

# run server
run flask

# running in debug mode will make it so changes

note on windows "set" instead of export

# for debug mode, run this before doing: flask run
!export FLASK_DEBUG=1

# or, adding this to .py and running normally from flask run
# also goes into debug mode

if __name__ == '__main__':
    app.run(debug=True)

# or!
# you can run flask by running the .py as a python script

$ python flaskblog.py

# in the past running as .py was the main way
# but not flask run is the main way
# flask shells works better with flask run

note:
    return can return html

        return tripple quotes<!doctype html>
        <html>
        tripple quotes

note:
    some text editors such as sublime and atom
    will create an html template by typing html and then tab
    at the top of the new doc

This is a codeblock - a for loop!
      {% for post in post %}

"""



#importing libraries, making sure that libraries are installed
import flask
from flask import Flask, render_template
#name of module (double underscore)
app = Flask(__name__)

posts = [
    {
        'author': 'Fred Wesley',
        'title': 'Weazies',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'George Wesley',
        'title': 'Weazly\'s',
        'content': 'second post content',
        'date_posted': 'April 21, 2018'
    }
]


# / is the root page of the website
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
#    return "Hello World!"
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
