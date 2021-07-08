import pickle
import json
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, render_template

MODEL_FILE = "iris_model2.pkl"
OUTPUT_DICT = "iris_dict.json"

# model
iris_model = pickle.load(open(MODEL_FILE, 'rb'))

app = Flask(__name__)

def value_predictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, -1)
    loaded_model = pickle.load(open(MODEL_FILE, 'rb'))
    result = loaded_model.predict(to_predict)
    return result[0]
    
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
    
@app.route("/result", methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        print(to_predict_list)
        result = value_predictor(to_predict_list)
        print(result)
        with open(OUTPUT_DICT, 'r') as f:
            s = f.read()
            iris_dict = eval(s)
        
        result = iris_dict[result]
        print(result)
    return render_template('results.html', prediction=result)

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
    
    with open(OUTPUT_DICT, 'r') as f:
        s = f.read()
        iris_dict = eval(s)
        
    print(iris_dict[y_pred[0]])
    
    output = {'y_pred' : iris_dict[y_pred[0]]}
    
    return jsonify(results=output)
    
if __name__ == "__main__":
    app.run(debug = True)