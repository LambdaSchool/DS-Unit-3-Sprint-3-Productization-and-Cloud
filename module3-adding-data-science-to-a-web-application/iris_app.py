import pickle
import json
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

MODEL_FILE = "iris_model2.pkl"
# model
iris_model = pickle.load(open(MODEL_FILE, 'rb'))

app = Flask(__name__)

@app.route("/api", methods=['POST'])
def make_predict():
    data = request.get_json(force=True)
    predict_request = [v for k, v in data.items()]
    predict_request = np.array(predict_request).reshape(1, -1)
    
    y_pred = iris_model.predict(predict_request)
    
    output = {'y_pred' : int(y_pred[0])}
    
    return jsonify(results=output)

@app.route("/score", methods=['POST'])
def model_score():
    data = request.get_json(force=True)
    
    X = pd.read_json(data['X']).values
    y = pd.Series(json.loads(data['y'])).values
    
    score = iris_model.score(X, y)
    output = {'model_score' : score}
    
    return jsonify(results=output)

@app.route("/api_text", methods=['POST'])
def make_predict_text():
    data = request.get_json(force=True)
    predict_request = [v for k, v in data.items()]
    predict_request = np.array(predict_request).reshape(1, -1)
    
    y_pred = iris_model.predict(predict_request)
    
    with open('iris_dict.json', 'r') as f:
        s = f.read()
        iris_dict = eval(s)
        
    print(iris_dict[y_pred[0]])
    
    output = {'y_pred' : iris_dict[y_pred[0]]}
    
    return jsonify(results=output)
    
if __name__ == "__main__":
    app.run(debug = True)