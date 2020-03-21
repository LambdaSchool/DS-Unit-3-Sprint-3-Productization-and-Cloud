from flask import Flask, render_template # Instance of the class from the module itself.
app = Flask(__name__) # create an instance of Flask

@app.route('/') # Web page  (also referred to as an endpoint - this us where our data will go)
def home():
    return render_template('home.html')

@app.route('/about') # this will be the 2nd page
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
