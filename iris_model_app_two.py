import numpy as np
from flask import Flask, jsonify, request
import pickle

# model
my_model = pickle.load(open('iris_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def make_predict():
    # get data
    data = request.get_json(force=True)
    # 1. parse / 2. transform data
    predict_request = [data['SepaLengthCm'], data['SepalWidthCm'], data['PetalLengthCm'], data['PetalWidthCm']]
    predict_request = np.array(predict_request).reshape(1,-1)
    # preds
    y_hat = my_model.predict(predict_request)
    # send back to browser
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 9000, debug=True)