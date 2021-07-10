import numpy as np
from flask import Flask, abort, jsonify, request
import pickle

my_model = pickle.load(open('iris_model.pkl', 'rb'))

app = Flask(__name__)


@app.route('/api', methods=['POST'])

def make_predict():
    # get data from post (4 features)
    data = request.get_json(force=True)
    # transforms
    predict_request = [data['sepal_width'], data['sepal_length'],
                       data['petal_width'], data['petal_length']]
    predict_request = np.array(predict_request).reshape(1, -1)
    # preds
    y_hat = my_model.predict(predict_request)
    # send preds back
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port=9000, debug=True)