from flask import Flask
# global vars are capitalized
APP = Flask(__name__)


@app.route("/")
def hello():
	# deployed model goes here
	return "<h1>Hello World!</h1>"


if __name__ == "__main__":
	app.run(debug=True, port=8080)
