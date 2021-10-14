import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from joblib import load
import psycopg2
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from lstm_maker import run_lstm_model



def make_bitpict(user_input_np_arr, output_file):
  db_string = f"postgresql://postgres:umiami17@crypto.cbzxnt6iwq2t.us-east-2.rds.amazonaws.com:5432/postgres"
  engine = create_engine(db_string)
  Session = sessionmaker(bind = engine)
  session = Session()

  coin_market_data = pd.read_sql('SELECT * FROM "BITCOIN"', engine)

  model, history, predictions, actual = run_lstm_model(coin_market_data,
                 target = 'close', epochs = 100, future = 7, drop = ['Date', 'adjClose', 'Symbol'])             
  df = pd.DataFrame({
    'Predictions': predictions.reshape(len(predictions)),
    'Actual': actual})

  x_new = np.array(list(range(60000))).reshape(60000,1)
  fig = px.scatter(x = df['Predictions'], y = df['Actual'],
                    title= "Bitcoin Predictions",
                    labels = {'x':'Predictions', 'y': 'Actual'})
  fig.add_trace(go.Scatter(x = [0, 60000], y = [0, 60000],
                    mode = 'lines',
                    name = 'x = Model'))    

  new_preds = model.predict(user_input_np_arr)
  fig.add_trace(go.Scatter(x=user_input_np_arr.reshape(len(user_input_np_arr)), y= df['Actual'], name='New Outputs', mode ='markers', marker=dict(color ='green', size = 20, line=dict(color ='orange',width=2))))

  fig.write_image(output_file, width = 800, engine='kaleido')
  fig.show()


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