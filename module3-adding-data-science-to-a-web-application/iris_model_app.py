import numpy as np
from flask import Flask, jsonify, request
import pickle

#model
my_model = pickle.load(open('iris_model2.pkl', 'rb'))

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def make_predict():
    #get data
    data = request.get_json(force=True)
    #parse
    predict_request = [data['SepalLengthCm'],data['SepalWidthCm'],data['PetalLengthCm'],data['PetalWidthCm']]
    #transform
    predict_request = np.array(predict_request).reshape(1,-1)
    #preds
    y_hat = my_model.predict(predict_request)
    #send back to browser
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output)

@app.route('/iris')
def iris():
    from sklearn.datasets import load_iris
    from sklearn.linear_model import LogisticRegression
    X, y = load_iris(return_X_y=True)
    clf = LogisticRegression(
        random_state=42, solver='lbfgs', multi_class='multinomial').fit(X,y)

    return str(clf.predict(X[:2, :]))

if __name__ == '__main__':
    app.run(port = 9000, debug=True)

