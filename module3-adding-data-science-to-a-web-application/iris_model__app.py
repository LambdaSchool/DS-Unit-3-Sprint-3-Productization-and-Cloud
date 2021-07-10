import numpy as np
from flask import Flask, abort, jsonify, request
import pickle

my_model = pickle.load(open("iris_model.pkl", "rb"))
app = Flask(__name__)

@app.route('/api', methods=['POST'])#sending information to this route, have to set up
#a method for endpoint to capture information
#POSTING new data, new data coming to API endpoint
def make_predict():
    #get data from post,
    #provide with new data, data has to be structured based on model it has been built
    #size should be the number of features that you have
    #set up a variable, request to get it
    #should contain the 4 features of your model
    data = request.get_json(force=True) #transforms
    #grab whatever is into post, going to be a list,
    #jupyter notebook sending data in the form of a dictionary, it comes in as a string
    #data object will be passed through will turn out to be a list
    #the model needs to be in some type of array
    predict_request = [data['SepalWidthCm'], data['SepalLengthCm'], data['PetalWidthCm'], data['PetalLengthCm']]
    predict_request = np.array(predict_request).reshape(1, -1)#reshaping to 1, -1 array
    y_hat = my_model.predict(predict_request)#similar to predict(X_test)
    
    #send predictions back
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output)#prediction saved to output, it is in the y_hat output
    #building a dictionary, jsonifying, coming back as string
    #at this point, it is possible to print our results and it will show in browser
    #we will print a json string, jsonify will give us a dictionary, we will retrieve it
    #in jupyter notebook
    
if __name__ == '__main__':#set up to run on a certain port
    app.run(port = 9000, debug = True)