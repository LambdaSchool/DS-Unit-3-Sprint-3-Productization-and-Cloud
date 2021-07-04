from flask import Flask, render_template

# make the application
app = Flask(__name__)

# make the route
@app.route("/")

# define a function
def hello():
    return render_template('home.html')

# create another route
@app.route('/about')

def preds():
    return render_template('about.html')
