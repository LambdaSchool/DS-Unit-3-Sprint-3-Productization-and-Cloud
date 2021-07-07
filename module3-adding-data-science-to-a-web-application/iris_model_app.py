import numpy as np
from flask import Flask, jsonify, request
import pickle
import iris

# Import model
my_model = pickle.load(open('iris_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def make_predicitons():
    # Get the data
    data = request.get_json(force=True)
    # Transform / Parse
    predict_request = np.array([data['SepalLengthCm'], data['SepalWidthCm'], data['PetalLengthCm'], data['PetalWidthCm']]).reshape(1, -1)
    # Preds
    y_hat = my_model.predict(predict_request)

    # Send back to browser
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output), le.inverse_transform(y_hat[0])

@app.route('/goodness', methods=['POST'])
def check_goodness_of_fit():
    # Get the data
    data = request.get_json(force=True)
    # Transform / Parse
    predict_request = np.array([data['SepalLengthCm'], data['SepalWidthCm'], data['PetalLengthCm'], data['PetalWidthCm']]).reshape(1, -1)
    # Preds
    y_hat = my_model.predict(predict_request)

    # Send back to browser
    return jsonify('Goodness of fit', my_model.score(predict_request, y_hat))
    
if __name__ == '__main__':
    app.run(port=9000, debug=True)