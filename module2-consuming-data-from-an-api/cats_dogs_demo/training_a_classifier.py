import json
import numpy as np
import os
import random
import re
import sklearn.linear_model
import sklearn.preprocessing
import time

EMB_DIR = '/tmp/basilica-embeddings/'
files = [f for f in os.listdir(EMB_DIR)]
random.shuffle(files)
train_size = int(len(files)*0.8)

x_train = np.zeros((train_size, 2048))
x_test = np.zeros((len(files)-train_size, 2048))
y_train = np.zeros(train_size, dtype=int)
y_test = np.zeros(len(files)-train_size, dtype=int)

for i in range(train_size):
    filename = files[i]
    with open(EMB_DIR + filename, 'r') as f:
        x_train[i] = json.load(f)
        y_train[i] = (0 if re.match('.*cat.*', filename) else 1)
for i in range(len(files) - train_size):
    filename = files[train_size+i]
    with open(EMB_DIR + filename, 'r') as f:
        x_test[i] = json.load(f)
        y_test[i] = (0 if re.match('.*cat.*', filename) else 1)

x_train = sklearn.preprocessing.normalize(x_train)
x_test = sklearn.preprocessing.normalize(x_test)
model = sklearn.linear_model.LogisticRegression()
model.fit(x_train, y_train)

print('Train accuracy: %.3f' % model.score(x_train, y_train))
print('Test accuracy: %.3f' % model.score(x_test, y_test))

test_proba = model.predict_proba(x_test)
probabilities = [(pred[y], f) for f, y, pred in zip(files[train_size:], y_test, test_proba)]
probabilities.sort()
for prob, filename in probabilities[:3]:
    print('%s: %.2f' % (filename, prob))
