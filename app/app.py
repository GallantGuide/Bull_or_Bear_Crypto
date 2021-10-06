from flask import Flask, render_template, request
from joblib import load
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import uuid

app = Flask(__name__)


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
        return render_template('index.html', href='static/Base_image.svg')
    else:
        text = request.form['text']
        random_string = uuid.uuid4().hex
        file = 'app/static/AgesAndHeights.pkl'
        model = load('app/test_model.joblib')
        user_input = user_input_np_arr(text)
        path = 'app/static/predictions' + random_string + '.svg'
        make_picture(file, model, user_input, path)
        return render_template('index.html', href=path[4:])

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
  fig.add_trace(go.Scatter(x=user_input_np_arr.reshape(len(user_input_np_arrl)), y = new_preds, name='New Outputs', mode ='markers', marker=dict(color ='green', size = 20, line=dict(color ='orange',width=2))))

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


