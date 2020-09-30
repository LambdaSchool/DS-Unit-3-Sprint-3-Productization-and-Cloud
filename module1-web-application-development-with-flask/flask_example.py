from flask import Flask

app = Flask(__name__)  # the name of our flask app is 'app'
# same thing you'd be using 'main' for to execute this function


@app.route('/')  # Flask will start a virtual web server on my machine
# & in order to access, I have to have a route
# if I had made the route '/aboutme' that would only work if I did
# my weblink + /aboutme
def home():
    # deployed model goes here:
    return '<h1>Hello, World!</h1>'
    # meaning -- when you ping this route, you'll get 'hello world'


if __name__ == '__main__':
    app.run(debug=True, port=8080)
    # this prevents us from having to call the function specifically
    # will cover more specifics tomorrow
