import os
import numpy as np
import flask
import pickle
from flask import Flask, render_template, request

#we are not using jupyter notebook, so no jsonify

#pred logic, grabs information for us from post
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, -1)#function to capture what comes into post
    loaded_model = pickle.load(open("iris_model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]#similar to the logic of make_predict function
#all the above does the prediction for you

#app
app=Flask(__name__)

#routes
@app.route('/')#defaults to this just in case, legacy reasons
@app.route('/index')
def index():
    return flask.render_template('index.html')#we are going to have a form

#we have to have something to hold and run the results page
@app.route('/result', methods = ['POST'])
def result():#will capture our predictions, handles result
#result will grab post from index.html, instead of host
    if request.method == 'POST':
        #take information from form with nominal data, let html do the work convert to dictionary
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
    return render_template("results.html", prediction=result)
#app run, so we don't export as an actual app
if __name__ == '__main__':
    app.run(port=9000, debug=True)
#windows go to system variables to shut down.