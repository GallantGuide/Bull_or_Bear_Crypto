# dataprocessing
import pandas as pd
import numpy as np
from datetime import datetime

# graphing
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def assemble_data(coin, client, engine):
    """ Given a coin name, and a connection to the sql and mongo DBs, return the data for modeling """
    # get the sql data
    coin_market_data = pd.read_sql(f'SELECT * FROM "{coin.upper()}"', engine)
    coin_market_data['Date'] = coin_market_data['Date'].astype(str)
    
    
    coin_posts = clean_reddit_data(client['Reddit_Comments'][coin].find())
    return coin_market_data.merge(coin_posts, how = 'left', on = 'Date')


def clean_reddit_data(raw_posts):
    by_date_dict = dict()

    # sort comments by date into new dict
    for post in raw_posts:
        date = post['date'].split(' ')[0]
        post['num_comments'] = int(post['num_comments'])
        post['score'] = int(post['score'])
        post['pos'] = float(post['pos'])
        post['neu'] = float(post['neu'])
        post['compound'] = float(post['compound'])
        if (date not in by_date_dict.keys()):
            by_date_dict[date] = []
        by_date_dict[date].append(post)
        
    
    composite_data = dict({
    'Date': [],
    'Num_Posts': [],
    'Ave_Comments': [],
    'Ave_Score': [],
    'Ave_Compound': []
    })
    
    # get daily metrics
    for key, value in by_date_dict.items():
        composite_data['Date'].append(string_to_date(key))
        composite_data['Num_Posts'].append(len(value))
        composite_data['Ave_Comments'].append(np.mean([post['num_comments'] for post in value]))
        composite_data['Ave_Score'].append(np.mean([post['score'] for post in value]))
        composite_data['Ave_Compound'].append(np.mean([post['compound'] for post in value]))
    return pd.DataFrame(composite_data)

#https://stackoverflow.com/questions/23581128/how-to-format-date-string-via-multiple-formats-in-python
def string_to_date(text):
    for fmt in ['%Y-%m-%d', '%m/%d/%Y']:
        try:
            return datetime.strptime(text, fmt).strftime('%Y-%m-%d')
        except:
            pass
    raise ValueError(f"no valid date format found for: {text}")

def loss_plot(history, title):
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.ylabel('loss'); plt.xlabel('epoch')
    plt.semilogy(history.history['loss'])

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.set_ylim(1, max(history.history['loss']))
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='both', colors='white')
    plt.savefig(f"Loss_{title}.png")
    plt.show()

def accuracy_vs_prediction_plot(predictions, actual, title):
    df = pd.DataFrame({
        'Predictions': predictions.reshape(len(predictions)),
        'Actual': actual
    })
    fig = go.Figure()

    # Add traces
    maximum_value = max(max(df['Predictions']), max(df['Actual']))
    fig.add_trace(go.Scatter(x = df['Predictions'], y = df['Actual'],
                        mode = 'markers',
                        name = 'Prediction vs. actual'))
    fig.add_trace(go.Scatter(x = [0, maximum_value], y = [0, maximum_value],
                        mode = 'lines',
                        name = 'x = 1'))

    fig.layout = dict(xaxis=dict(title = 'Predictions'),
                yaxis=dict(title = 'Actual'))

    fig.write_image(f"images/Actual_vs_Predictions_{title}.svg", width = 800)
    fig.show()
