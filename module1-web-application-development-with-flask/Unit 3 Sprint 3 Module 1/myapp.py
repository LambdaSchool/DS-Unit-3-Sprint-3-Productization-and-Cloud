# # import my flask package
# from flask import Flask, render_template
#
# # create Flask web server
# app = Flask(__name__)
#
# # route determines location
# @app.route("/")
#
# # define a little function to tell
# #  app what to do at that route (app.rout("/"))
# # http://127.0.0.1:5000
# def home():
#     return render_template('home.html')
#
# # Create another route
# @app.route("/about")
#
# # Define another function for this new route
# # http://127.0.0.1:5000/about
# def pred():
#     return render_template('about.html')
#
# # Clean things up
# if __name__ == "__main__":
#     app.run(debug = True)
#
#     #conda install Flask==1.0.3 is not buggy
#
# # open CMD/anaconda prompt, cd to directory of
# # myapp.py, run "python myapp.py", go to
# # ip.address provided after "running on https:"
#
# #to run this go to terminal and type python myapp.py
# #alt approach to running it, also in terminal:
# # FLASK_APP= myapp.py flask run

#import my flask package
from flask import Flask, render_template

#create Flask web server
app = Flask(__name__)

#route determines location
@app.route("/")

#define a little function to
#tell it what to do at that route
def home():
    return render_template('home.html')

#Create another route
@app.route("/about")

#define another function for this new route
def pred():
    return render_template('about.html')

#clean things up
if __name__ == "__main__":
    app.run(debug=True)

#to run this go to terminal and type python myapp.py
#alt approach to running it, also in terminal:
# FLASK_APP= myapp.py flask run