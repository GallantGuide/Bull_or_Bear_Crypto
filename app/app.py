from flask import Flask, render_template, request
from joblib import load
from .functions import make_picture, user_input_np_arr
from sqlalchemy import Table, MetaData, create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import uuid
import os



app = Flask(__name__)


db_path = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
# app.config['SQLALCHEMY_DATABASE_URI'] = db_path
# db = SQLAlchemy(app)

db = create_engine(db_path)

# # Table Data for DB Pulls
K_Bitcoin = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)


@app.route("/ste")
def welcome():
    return(
    '''
    Welcome to Bull or Bear Crypto '\n
    Available Routes: \n
    /Site \n
    /test_model \n
    /hello_world \n
    /api/v1.0
    '''
    )


@app.route("/", methods = ['GET','POST'])
def test_template():
    request_type = request.method
    if request_type == 'GET':
        return render_template('index.html', href='static/images/Base_image.svg')
    else:
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/predictions' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])


@app.route("/bitcoin", methods = ['GET','POST'])
def Bitcoin_Image():
    request_type = request.method
    if request_type == 'POST':
        text = request.form['data']
        random_string = uuid.uuid4().hex
        user_input = user_input_np_arr(text)
        path = 'static/' + random_string + '.svg'
        make_picture(user_input, path)
        return render_template('bitcoin.html', href=path[4:])
    else:
        return render_template('bitcoin.html', href='static/images/actual_vs_predictions.svg') 

@app.route("/bitcoin_db", methods = ['GET','POST'])
def Bitcoin_Search():
    request_type = request.method
    if request_type == 'POST':
        return "You clicked a button"
    else:
        # k_bitcoin = db.session.query(K_Bitcoin).all()
        return render_template('bitcoin_db.html')        

@app.route("/test_model")
def test_model():
    test_np_input = np.array([[1],[2],[17]])
    model = load('test_model.joblib')
    preds = model.predict(test_np_input)
    preds_str = str(preds)
    return preds_str


@app.route("/hello_world")
def hello_world():
    return "Hello, World!"


