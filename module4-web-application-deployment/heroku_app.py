import os
import numpy as np
from flask import Flask, render_template, request
import pickle


# Prediction Function
def valuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, -1)
    loaded_model = pickle.load(open('iris_model.pkl', 'rb'))
    result = loaded_model.predict(to_predict)
    return result[0]

# Create app
app = Flask(__name__)

# Create routes
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        
        result = valuePredictor(to_predict_list)
        
        if result == 0:
            result = 'Setosa'
        elif result == 1:
            result =  'Versicolor'
        else:
            result = 'Virginica'

        return render_template('results.html', prediction=result)
        
if __name__ == '__main__':
    app.run(port=9000, debug=True)