from flask import Flask, render_template, request
from joblib import load
<<<<<<< HEAD
from .functions import make_picture, user_input_np_arr
=======
>>>>>>> main
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
<<<<<<< HEAD
=======
import functions
>>>>>>> main
import uuid

app = Flask(__name__)

<<<<<<< HEAD
@app.route("/")
def welcome():
    return(
    '''
    Welcome to Bull or Bear Crypto '\n
    Available Routes: \n
    /site \n
    /test_site \n
    /test_model \n
    /hello_world \n
    /api/v1.0
    '''
    )

@app.route("/site", methods = ['GET','POST'])
def site_template():
    request_type = request.method
    if request_type == 'GET':
        return render_template('index.html', href='static/Base_image.svg')
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])

@app.route("/test_site", methods = ['GET','POST'])
=======

@app.route("/", methods = ['GET','POST'])
>>>>>>> main
def test_template():
    request_type = request.method
    if request_type == 'GET':
        return render_template('index.html', href='static/Base_image.svg')
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
<<<<<<< HEAD
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])

=======
        file = 'static/AgesAndHeights.pkl'
        model = load('test_model.joblib')
        user_input = functions.user_input_np_arr(text)
        path = 'static/' + random_string + '.svg'
        functions.make_picture(file, model, user_input, path)
        return render_template('index.html', href=path)


@app.route("/Site")
>>>>>>> main

@app.route("/test_model")
def test_model():
    test_np_input = np.array([[1],[2],[17]])
<<<<<<< HEAD
    model = load('app/test_model.joblib')
=======
    model = load('test_model.joblib')
>>>>>>> main
    preds = model.predict(test_np_input)
    preds_str = str(preds)
    return preds_str


@app.route("/hello_world")
def hello_world():
<<<<<<< HEAD
    return "Hello, World!"
=======
    return "Hello, World!"




if __name__=='__main__':
    app.run(debug=True)    
>>>>>>> main
