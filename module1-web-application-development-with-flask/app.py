# Import Flask
from flask import Flask, render_template

#create Flask web server

app = Flask(__name__)

# routes (determine loccation)
@app.route("/")
def template():
    return render_template('template.html')

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
