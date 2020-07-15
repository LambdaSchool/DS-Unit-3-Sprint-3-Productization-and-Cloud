import basilica
import json
import numpy as np
import os
import random
import re
import sklearn.decomposition
import sklearn.neighbors
import sklearn.preprocessing
import time

EMB_DIR = '/tmp/basilica-embeddings/'
files = [f for f in os.listdir(EMB_DIR) if re.match('.*dog.*', f)]
random.shuffle(files)

signatures = np.zeros((len(files), 2048))
for i, filename in enumerate(files):
    with open(EMB_DIR + filename, 'r') as f:
        signatures[i] = json.load(f)

scaler = sklearn.preprocessing.StandardScaler(with_std=False)
pca = sklearn.decomposition.PCA(n_components=200, whiten=True)

signatures = sklearn.preprocessing.normalize(signatures)
signatures = scaler.fit_transform(signatures)
signatures = pca.fit_transform(signatures)
signatures = sklearn.preprocessing.normalize(signatures)

nbrs = sklearn.neighbors.NearestNeighbors(n_neighbors=4).fit(signatures)

IMG_DIR = 'images/'
target_files = ['dog.1.jpg', 'dog.2.jpg', 'dog.3.jpg']
with basilica.Connection('84a86904-19a2-453e-acd5-45a45a1369da') as c:
    targets = np.array(list(c.embed_image_files(IMG_DIR + f for f in target_files)))

targets = sklearn.preprocessing.normalize(targets)
targets = scaler.transform(targets)
targets = pca.transform(targets)
targets = sklearn.preprocessing.normalize(targets)

_, all_indices = nbrs.kneighbors(targets)
for indices in all_indices:
    print(' '.join(files[i] for i in indices))

