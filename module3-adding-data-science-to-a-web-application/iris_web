import os 
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

#logic
def ValuePredictor(to_predict_list):
	to_predit = np.array(to_predict_list).reshape(1,-1)
	loaded_model = pickle.load(open("iris_model.pkl", "rb" )
	ans = loaded_model.predict(to_predict)
	return ans[0]	

#app
app = Flask(__name__)
#routes
@app.route('/')
@app.route('/index')
def index():
	return flask.render_template('index.html')
@app.route('/result', methods = ['POST'])
def resuts():
	if request.method == 'POST':
		to_predict_list = request.form.to_dict()
		to_predict_list = list(to_predict_list.values())
		to_predict_list = list(map(int, to_predict_list))
		result = ValuePredictor(to_predict_list)	
	return render_template("results.html", prediction= result)
#
if __name__ == '__main__':
	app.run(port=9000, debug= TRUE)

