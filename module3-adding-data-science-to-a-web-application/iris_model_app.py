import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
import pickle


# Pickle things in
my_model = pickle.load(open('iris_model.pkl', 'rb'))
accuracy = pickle.load(open('iris_model_accuracy.pkl', 'rb'))
class_key = pickle.load(open('class_key.pkl', 'rb'))
medicare_pipeline = pickle.load(open('medicare_pipeline.pkl', 'rb'))


app = Flask(__name__)


# Home Page
@app.route('/')
def home():
    return """
    <h1>Iris Model API</h1>
    <h2>Decision Tree Classifier</h2>
    """


# Predictions API
@app.route('/api', methods=['POST'])
def make_predict():
    # Get Data
    data = request.get_json(force=True)

    # Parse & Transform Data
    predict_request = [data['SepalLengthCm'],
                       data['SepalWidthCm'],
                       data['PetalLengthCm'],
                       data['PetalWidthCm']]

    predict_request = np.array(predict_request).reshape(1, -1)

    # Make Predictions
    y_pred = my_model.predict(predict_request)

    # Send output back to Browser
    output = {'Prediction': int(y_pred[0])}
    return jsonify(results = output)

######################################################
##################### Assignment #####################
######################################################

# Return Accuracy Score
@app.route('/fit')
def accuracy_page():
    return '<h1>Accuracy Score:  ' + str(accuracy) + '</h1>' + """
    <h2>Looks like we overfit!</h2>
    """


# Class API
@app.route('/class_api', methods=['POST'])
def predict_class():
    # Get Data
    data = request.get_json(force=True)

    # Parse & Transform Data
    predict_request = [data['SepalLengthCm'],
                       data['SepalWidthCm'],
                       data['PetalLengthCm'],
                       data['PetalWidthCm']]

    predict_request = np.array(predict_request).reshape(1, -1)

    # Make Predictions
    y_pred = my_model.predict(predict_request)

    # Send output back to Browser
    output = {'Prediction': class_key[int(y_pred[0])]}
    return jsonify(results = output)


# Medicare App API
@app.route('/medicare_costs', methods=['POST'])
def predict_costs():
    # Get Data
    data = request.get_json(force=True)

    # Parse & Transform Data
    predict_request = [data['diagnosis'],
                       data['state']]

    predict_request = np.array(predict_request).reshape(1, -1)

    request_df = pd.DataFrame(columns = ['diagnosis', 'state'],
                              data = predict_request)

    # Make Predictions
    y_pred = medicare_pipeline.predict(request_df)

    # Send output back
    output = {'Predicted Cost': float(y_pred[0])}
    return jsonify(results = output)


# Run App
if __name__ == '__main__':
    app.run(debug = True)