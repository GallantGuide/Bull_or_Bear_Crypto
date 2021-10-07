from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import functions
import uuid

app = Flask(__name__)


@app.route("/", methods = ['GET','POST'])
def test_template():
    request_type = request.method
    if request_type == 'GET':
        return render_template('index.html', href='static/Base_image.svg')
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = functions.user_input_np_arr(text)
        path = 'app/static/' + random_string + '.svg'
        functions.make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])


@app.route("/Site")

@app.route("/test_model")
def test_model():
    test_np_input = np.array([[1],[2],[17]])
    model = load('app/test_model.joblib')
    preds = model.predict(test_np_input)
    preds_str = str(preds)
    return preds_str


@app.route("/hello_world")
def hello_world():
    return "Hello, World!"