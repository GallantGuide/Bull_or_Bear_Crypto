from flask import Flask, render_template, request,redirect, url_for
from joblib import load
# from functions import make_picture, user_input_np_arr
# from variables import *
from sqlalchemy import Table, MetaData, create_engine
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import uuid
import os

app = Flask(__name__)

 db_path = os.getenv('DATABASE_URL')

# App connector and Table Data for DB Pulls
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy(app)

K_Bitcoin = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)
K_Cardano = db.Table('K_CARDANO', db.metadata, autoload=True, autoload_with=db.engine)
K_Ethereum = db.Table('K_ETHEREUM', db.metadata, autoload=True, autoload_with=db.engine)


# Default App Route 
@app.route("/", methods = ['GET','POST'])
def Welcome():
    request_type = request.method
    href1='static/images/BTC_Components.png'
    href2='static/images/BTC_Accuracy.png'
    dref1='static/images/schema.png'
    if request_type == 'GET':
        return render_template('index.html', href1=href1, href2=href2, dref1=dref1)  
    if request_type == 'POST':
        url_param = request.form["url"]
        return redirect(url_for("url_param",param=url_param))


# @app.route("/<param>")
# def url_param(param):
#     request_type = request.method
#     if request_type == 'GET':
#         return render_template('index.html')  
#     if request_type == 'POST':
#         url_param = request.form["url"]
#         return redirect(url_for("url_param",param=url_param))

@app.route("/test_model")
def test_model():
    test_np_input = np.array([[1],[2],[17]])
    model = load('test_model.joblib')
    preds = model.predict(test_np_input)
    preds_str = str(preds)
    return preds_str

# Images and plots
@app.route("/bitcoin", methods = ['GET','POST'])
def Bitcoin_Image():
    request_type = request.method
    href1='static/images/Actual_vs_Predictions_Bitcoin_just_market.svg'
    href2='static/images/Actual_vs_Predictions_Bitcoin_just_reddit.svg'
    href3='static/images/Actual_vs_Predictions_Bitcoin_all_data.svg'
    if request_type == 'POST':
        return render_template('bitcoin.html', href1=href1, href2=href2, href3=href3)
    else:
        return render_template('bitcoin.html', href1=href1, href2=href2, href3=href3) 

@app.route("/cardano", methods = ['GET','POST'])
def Cardano_Image():
    request_type = request.method
    href1='static/images/Actual_vs_Predictions_Cardano_just_market.svg'
    href2='static/images/Actual_vs_Predictions_Cardano_just_reddit.svg'
    href3='static/images/Actual_vs_Predictions_Cardano_all_data.svg'
    if request_type == 'POST':
        return render_template('cardano.html', href1=href1, href2=href2, href3=href3)
    else:
        return render_template('cardano.html', href1=href1, href2=href2, href3=href3)  

@app.route("/ethereum", methods = ['GET','POST'])
def Ethereum_Image():
    request_type = request.method
    href1='static/images/Actual_vs_Predictions_Ethereum_just_market.svg'
    href2='static/images/Actual_vs_Predictions_Ethereum_just_reddit.svg'
    href3='static/images/Actual_vs_Predictions_Ethereum_all_data.svg'
    if request_type == 'POST':
        return render_template('ethereum.html', href1=href1, href2=href2, href3=href3)
    else:
        return render_template('ethereum.html', href1=href1, href2=href2, href3=href3)                        


@app.route("/site", methods = ['GET','POST'])
def site_template():
    request_type = request.method
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'static/AgesAndHeights.pkl'
        model = load('static/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'static/uuid/' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('site.html', href=path)
        # return render_template('site.html', href=path[4:])
    else:
        return render_template('site.html', href='static/images/Base_image.svg')  

# Database connector app routes
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

# # Local site app config 
# if __name__ == "__main__":
#     app.run(debug=True)        
