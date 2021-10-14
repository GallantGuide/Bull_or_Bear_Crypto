import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from joblib import load

def make_bitpict(training_data_fname, model, user_input_np_arr, output_file):
  data = pd.read_sql(training_data_fname)
  x_new = np.array(list(range(19))).reshape(19,1)
  preds = model.predict(x_new)
  fig= px.scatter(x = ages, y = heights, title= "Height V Age of People", labels = {'x':'Age (Years)', 'y': 'Heights(inches)'})
  fig.add_trace(go.Scatter(x=x_new.reshape(19), y=preds, mode = 'lines', name = 'Model'))

  new_preds = model.predict(user_input_np_arr)
  fig.add_trace(go.Scatter(x=user_input_np_arr.reshape(len(user_input_np_arr)), y = new_preds, name='New Outputs', mode ='markers', marker=dict(color ='green', size = 20, line=dict(color ='orange',width=2))))

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