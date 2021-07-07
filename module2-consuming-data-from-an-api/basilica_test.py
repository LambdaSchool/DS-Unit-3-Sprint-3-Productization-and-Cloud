import basilica
from six.moves import zip
import json
import os
import json
import numpy as np
import random
import re
import sklearn.linear_model
import sklearn.preprocessing
import time

API_KEY = 'SLOW_DEMO_KEY'
with basilica.Connection(API_KEY) as c:
    embedding = c.embed_image_file('images/dog.jpg')

EMB_DIR = '/tmp/basilica-embeddings/'
if not os.path.exists(EMB_DIR):
    os.mkdir(EMB_DIR)

IMG_DIR = 'images/'
with basilica.Connection(API_KEY) as c:
    filenames = os.listdir(IMG_DIR)
    embeddings = c.embed_image_files(IMG_DIR + f for f in filenames)
    for filename, embedding in zip(filenames, embeddings):
        with open(EMB_DIR + filename + '.emb', 'w') as f:
            f.write(json.dumps(embedding))
            print(filename)

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