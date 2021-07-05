from flask import Flask 

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Lambda World!"

@app.route("/predictions")
def preds():
    return "Make Predictions"

if __name__ == "__main__":
    app.run(debug=True)
