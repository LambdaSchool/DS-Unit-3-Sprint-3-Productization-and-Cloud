from flask import Flask
app = Flask(__name__)

@app.route("/")
def flask():
    return "hello world!"

