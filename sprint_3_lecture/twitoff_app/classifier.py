# twitoff_app/classifier.py


import os
import pickle

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression # for example

MODEL_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "models", "latest_model.pkl")

def train_and_save_model():
    print("TRAINING THE MODEL...")
    X, y = load_iris(return_X_y=True)
    #print(type(X), X.shape) #> <class 'numpy.ndarray'> (150, 4)
    #print(type(y), y.shape) #> <class 'numpy.ndarray'> (150,)
    classifier = LogisticRegression() # for example
    classifier.fit(X, y)

    print("SAVING THE MODEL...")
    with open(MODEL_FILEPATH, "wb") as model_file:
        pickle.dump(classifier, model_file)

    return classifier

def load_model():
    print("LOADING THE MODEL...")
    with open(MODEL_FILEPATH, "rb") as model_file:
        saved_model = pickle.load(model_file)
    return saved_model

if __name__ == "__main__":

    # train_and_save_model()


    clf = load_model()
    print("CLASSIFIER:", clf)

    # breakpoint()

    X, y = load_iris(return_X_y=True) # just to have some data to use when predicting
    inputs = X[:2, :]
    print(type(inputs), inputs)

    result = clf.predict(inputs)
    print("RESULT:", result)