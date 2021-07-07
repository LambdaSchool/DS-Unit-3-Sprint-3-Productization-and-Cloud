import numpy as np
import pandas as pd
from flask import Flask, jsonify, request


# Instantiate app
app = Flask(__name__)


# Home Page
@app.route('/')
def home():
    return """
    <h1>Iris Model API</h1>
    <h2>Decision Tree Classifier</h2>
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


# Run App
if __name__ == '__main__':
    app.run(debug = True)