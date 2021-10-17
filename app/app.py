from flask import Flask, render_template, request
from joblib import load
from .functions import make_picture, user_input_np_arr
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
# Ethereum = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)
# Cardnamo = db.Table('K_BITCOIN', db.metadata, autoload=True, autoload_with=db.engine)


# Default App Route 
@app.route("/", methods = ['GET','POST'])
def tWelcome():
    request_type = request.method
    if request_type == 'GET':
        return render_template('index.html', href='static/images/Base_image.svg')  
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/predictions' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])

@app.route("/<param>")
def url_param(param):
    return f'<h1> {param} <h1>'

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
    if request_type == 'POST':
        text = request.form['data']
        random_string = uuid.uuid4().hex
        user_input = user_input_np_arr(text)
        path = 'static/' + random_string + '.svg'
        make_picture(user_input, path)
        return render_template('bitcoin.html', href=path[4:])
    else:
        return render_template('bitcoin.html', href='static/images/actual_vs_predictions.svg')       


@app.route("/site", methods = ['GET','POST'])
def test_site():
    request_type = request.method
    if request_type == 'POST':
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/predictions' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('site.html', href=path[4:])
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

def make_picture(training_data_fname, model, user_input_np_arr, output_file):
  data = pd.read_pickle(training_data_fname)
  data = data[data['Age'] > 0 ]
  ages = data['Age']
  heights = data['Height']
  x_new = np.array(list(range(19))).reshape(19,1)
  preds = model.predict(x_new)
  fig= px.scatter(x = ages, y = heights, title= "Height V Age of People", labels = {'x':'Age (Years)', 'y': 'Heights(inches)'})
  fig.add_trace(go.Scatter(x=x_new.reshape(19), y=preds, mode = 'lines', name = 'Model'))

  new_preds = model.predict(user_input_np_arr)
  fig.add_trace(go.Scatter(x=user_input_np_arr.reshape(len(user_input_np_arr)), y = new_preds, name='New Outputs', mode ='markers', marker=dict(color ='green', size = 20, line=dict(color ='orange',width=2))))

  fig.write_image(output_file, width = 800, engine='kaleido')
  fig.show()

def user_input_np_arr(float_str):
  def is_float(s):
    try:
      float(s)
      return True 
    except:
      return False  
  floats = np.array([float(x) for x in float_str.split(',') if is_float(x)])
  return floats.reshape(len(floats),1)        
