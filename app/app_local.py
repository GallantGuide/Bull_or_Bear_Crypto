from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import Table, MetaData
from flask_sqlalchemy import SQLAlchemy
from joblib import load
from typing import DefaultDict
from functions import make_picture, user_input_np_arr, make_bitpict
# heroku name convention from .functions import make_picture, user_input_np_arr, make_bitpict
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:umiami17@crypto.cbzxnt6iwq2t.us-east-2.rds.amazonaws.com:5432/postgres'
db = SQLAlchemy(app)


# Table Data for DB Pulls
K_Bitcoin = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)
K_Cardano = db.Table('K_CARDANO', db.metadata, autoload=True, autoload_with=db.engine)
K_Ethereum = db.Table('K_ETHEREUM', db.metadata, autoload=True, autoload_with=db.engine)
Ethereum = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)
Cardnamo = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)


@app.route("/", methods = ['GET','POST'])
def welcome():
    request_type = request.method
    if request_type == "POST":
        url_param = request.form["url"]
        return redirect(url_for("url_param",param=url_param))
    else:    
        return render_template("welcome.html")

@app.route("/bitcoin_db", methods = ['GET','POST'])
def Bitcoin_Search():
    request_type = request.method
    if request_type == 'POST':
        return "You clicked a button"
    else:
        k_bitcoin = db.session.query(K_Bitcoin).all()
        return render_template('bitcoin_db.html', k_bitcoin=k_bitcoin)

@app.route("/cardano_db", methods = ['GET','POST'])
def Cardano_Search():
    request_type = request.method
    if request_type == 'POST':
        return "You clicked a button"
    else:
        k_cardano = db.session.query(K_Cardano).all()
        return render_template('cardano_db.html', k_cardano=k_cardano)
        
@app.route("/ethereum_db", methods = ['GET','POST'])
def Ethereum_Search():
    request_type = request.method
    if request_type == 'POST':
        return "You clicked a button"
    else:
        k_ethereum = db.session.query(K_Ethereum).all()
        return render_template('ethereum_db.html', k_ethereum=k_ethereum)

# Testing Bitcoin site settings 
@app.route("/bitcoin", methods = ['GET','POST'])
def Bitcoin_Image():
    request_type = request.method
    if request_type == 'POST':
        text = request.form['data']
        random_string = uuid.uuid4().hex
        user_input = user_input_np_arr(text)
        path = 'static/' + random_string + '.svg'
        make_bitpict(user_input, path)
        return render_template('bitcoin.html', href=path)
    else:
        return render_template('bitcoin.html', href='static/actual_vs_predictions.svg') 

@app.route("/<param>")
def url_param(param):
    return f'<h1> {param} <h1>'

# heroku site settings 
@app.route("/site", methods = ['GET','POST'])
def site_template():
    request_type = request.method
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])
    else:
        return render_template('index.html', href='static/Base_image.svg')    


# Local test site settings 
@app.route("/test_site", methods = ['GET','POST'])
def test_template():
    request_type = request.method
    if request_type == 'POST':
        text = request.form['data']
        random_string = uuid.uuid4().hex
        file = 'static/AgesAndHeights.pkl'
        model = load('test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'static/uuid/' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path)
    else:
        return render_template('index.html', href='static/Base_image.svg') 


@app.route("/index_base", methods = ['GET','POST'])
def JS_testing():
    return render_template('index_base.html') 

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


# Local site app config 
if __name__ == "__main__":
    app.run(debug=True)



# class config(object):
#     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:umiami17@crypto.cbzxnt6iwq2t.us-east-2.rds.amazonaws.com:5432/postgres' 
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# app.config.from_object(config)
# db = SQLAlchemy(app)
# metadata = MetaData()

# table_reflection = Table("K_BITCOIN", metadata, autoload=True, autoload_with=db.engine)
# attrs = {"__table__": table_reflection}
# Kaggle = type("K_BITCOIN", (db.Model,), attrs)
