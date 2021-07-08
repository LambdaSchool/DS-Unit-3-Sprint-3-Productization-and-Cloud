import pickle
import json
import requests
import click

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier

DATA_FILE = "Iris.csv"
MODEL_FILE = "iris_model2.pkl"


def train_fit_save():
    iris = pd.read_csv(DATA_FILE)

    le = LabelEncoder()
    le.fit(iris['Species'])

    iris['Species'] = le.transform(iris['Species'])

    X = iris.iloc[:,1:5]
    #print(X.head())
    y = iris.iloc[:,5]
    #print(y.head())
    transform_dict = dict(zip(le.transform(le.classes_), le.classes_))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=45)

    tree = DecisionTreeClassifier()
    model = tree.fit(X_train, y_train)

    pred = model.predict(X_test)

    print(f'accuracy: {accuracy_score(y_test, pred)}')
    print(classification_report(y_test, pred))

    pickle.dump(model, open(MODEL_FILE, 'wb'))
    return transform_dict
   
def call_api(url, data):
    send = requests.post(url, data)
    
    return send
    
@click.command()
@click.option('--inference', default=True, help="Set inference or modeling")
def run(inference):
    if inference == True:
        # making prediction
        url_pred = "http://127.0.0.1:5000/api"
        data_pred = json.dumps({'SepalLengthCm': 7, 'SepalWidthCm': 3.5, 'PetalLengthCm': 4.7, 'PetalWidthCm': 1.4})        
        
        call_pred = call_api(url_pred, data_pred)
        print(f'Predict of {data_pred} is {call_pred.json()}')
        
        # getting model score
        url_score = "http://127.0.0.1:5000/score"
        iris = pd.read_csv(DATA_FILE)

        le = LabelEncoder()
        le.fit(iris['Species'])

        iris['Species'] = le.transform(iris['Species'])

        X = iris.iloc[:,1:5].to_json()
        y = iris.iloc[:,5].to_json()
        
        data_score = json.dumps({'X': X, 'y': y})        
        call_score = call_api(url_score, data_score)
        print(call_score.json())
        
        # making prediction for string output
        url_pred_text = "http://127.0.0.1:5000/api_text"
        data_pred_text = json.dumps({'SepalLengthCm': 7, 'SepalWidthCm': 3.5, 'PetalLengthCm': 4.7, 'PetalWidthCm': 1.4})        
        
        call_pred_text = call_api(url_pred_text, data_pred_text)
        print(f'Predict of {data_pred_text} is {call_pred_text.json()}')
        
    else:    
        iris_dict = train_fit_save()
        # save the dict into a .json file
        with open('iris_dict.json', 'w') as f:
            f.write(str(iris_dict))
        f.close()
    pass


if __name__ == "__main__":
    run()