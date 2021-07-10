from flask import Flask, render_template



#create Flask web server, when I run this, it's going to execute itself

app = Flask(__name__)

posts = [
	{
		"author": "Corey Shafer",
		"title": "Blog Post 1",
		"content": "First post",
		"date_posted": "April 20, 2019"
	}
]

#routes 
@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/predictions")
def preds():
	return "Make Predictions"

@app.route("/about")
def about():
	return render_template('about.html', title='About')

if __name__ == "__main__":
	app.run(debug=True)
