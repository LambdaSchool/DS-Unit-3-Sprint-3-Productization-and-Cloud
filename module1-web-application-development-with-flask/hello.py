from flask import Flask #instance of the class
app = Flask(__name__) #crate an instance of Flask

@app.route('/')
def hello_word():
	return 'Hello, Wrold; Its sunny out'

if __name__=='__main__':
     app.run()

