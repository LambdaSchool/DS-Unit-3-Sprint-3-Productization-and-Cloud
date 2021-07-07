import pandas as pd
import numpy as numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
import pickle
import json
import requests

iris = pd.read_csv('iris.csv')
le = LabelEncoder()
le.fit(iris['Species'])
iris['Species'] = le.transform(iris['Species'])

# Features
X = iris.iloc[:,1:5]
y = iris.iloc[:,5]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state=123)

algo = DecisionTreeClassifier()
model = algo.fit(X_train, y_train)

# Preds
preds = model.predict(X_test)

# Check accuracy
print(f'Accuracy Score: {accuracy_score(y_test, preds)}')

# Pickle
pickle.dump(model, open('iris_model.pkl', 'wb'))

url = 'http://localhost:9000/api'

data = json.dumps({'SepalLengthCm': 7, 'SepalWidthCm': 3.5, 'PetalLengthCm': 4.7, 'PetalWidthCm': 1.4})

send = requests.post(url, data)

print(send.json())

url = 'http://localhost:9000/goodness'

data = json.dumps({'SepalLengthCm': 7, 'SepalWidthCm': 3.5, 'PetalLengthCm': 4.7, 'PetalWidthCm': 1.4})

send = requests.post(url, data)

print(send.json())