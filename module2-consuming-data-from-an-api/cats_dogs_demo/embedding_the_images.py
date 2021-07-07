from six.moves import zip
import basilica
import json
import os

EMB_DIR = '/tmp/basilica-embeddings/'
if not os.path.exists(EMB_DIR):
    os.mkdir(EMB_DIR)

IMG_DIR = 'images/'
API_KEY = 'SLOW_DEMO_KEY'
with basilica.Connection(API_KEY) as c:
    filenames = os.listdir(IMG_DIR)
    embeddings = c.embed_image_files(IMG_DIR + f for f in filenames)
    for filename, embedding in zip(filenames, embeddings):
        with open(EMB_DIR + filename + '.emb', 'w') as f:
            f.write(json.dumps(embedding))
            print(filename)
