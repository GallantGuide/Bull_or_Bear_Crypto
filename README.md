# Bull or Bear Crypto

Using machine learning to forecast cryptocurrency prices

## Overview

### Topic

We are interested in analyzing what factors are correlated with the prices of cryptocurrencies over time, and whether these factors can be used to predict the future prices of these currencies.

### Justification

Cryptocurrencies are of great interest to the finance community right now.  Their possible impacts on the global economy are being investigated, and it seems likely that some form of block chain currency will be adopted by nations, [including the US]( https://www.popularmechanics.com/technology/a32869513/us-government-research-crypto-dollar/), as official currencies.  Currently, these currencies can be traded on the stock market and show marked volatility as their underlying worth is unclear.  Being able to predict what factors influence cryptocurrency prices could be a key factor is understating why they are so volatile and what could be done to help stabilize them enough to be used an official currency.  It is also of great interest to investors to be able to predict the behavior of these coins and take advantage of these predictions to grow investment accounts.

### Source Data

-	[Kaggle Cryptocurrency Dataset]( https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory) (coin prices over time)
-	Yahoo Finance (stock trends over time) - [web-scraper](web_scraping/load/Yahoo_Finance_Scraper.py)
-	Reddit (posts) - [api-caller](web_scraping/load/Reddit_API_Caller.py)
-	Twitter (posts) - WIP

### Target Questions

-	Is cryptocurrency behavior correlated between different coins?  I.e. Do they all increase and decrease together?
-	What predicts cryptocurrency behavior?
  -	Overall market behavior
  -	Behavior of commodities (e.g. Gold)
  -	Posts about the currencies on social media (e.g. reddit and twitter)
-	How far into the future are predictions about cryptocurrency behavior accurate?


## Project Implementation

### Technologies Used

- `SQL`
- `MongoDB`
- `Python`
  - `Prophet` library
  - `pandas` 1.2.4
  - `requests` 2.25.1
  - `langid` 1.1.6
  - `nltk` 3.6.1
  - `splinter` 0.15.0
  - `bs4` 4.9.3
  - `webdriver_manager` 3.4.1
  - `sklearn` 0.24.1
  - `tensorflow` 2.6.0
  - `os`, `sys`, `time`

### Communication Protocols
All group members belong to a discord server dedicated to this project.  There are text channels dedicated to all aspects of the project (e.g. machine-learning and database channels), as well as channels for resources and error handling.  Additionally, there are voice channels that allow group members to talk through problems live.  Discord offers screen sharing so group members can present their code.  Finally, we created a bot that announces when changes are made to the repository, so all members are informed as changes are pushed.  As a backup, all group members have exchanged phone numbers and email.

### Resources

### Data Cleaning and Analysis

#### Pre-processing
All preprocessing is done in Python.  The Kaggle data is clean and required no preprocessing.  The Yahoo Finance data is scraped from Yahoo Finance in groups of 100.  These groups are then combined and sorted by date.  No other processing is required.  For the Reddit data, posts are pulled from an API.  Posts that are not in English (as identified by langid) are dropped.  Posts with duplicate titles are dropped.  Finally, the NLTK library is used to run a sentiment analysis on the post title and the sentiment data (positive, negative, neutral, composite) is added to each post.

#### Post-processing

#### Analysis

##### Exploratory

We will check for correlations between various cryptocurrency prices.  We will also examine the correlations between individual currency prices and other features like how much a currency is talked about on social media or other market trends.

##### Machine learning

We are using a series of machine learning models to predict the future behavior of cryptocurrencies.  See the machine learning section below for more imdept information.  The models include:
-	Prophet: uses time and price information to predict future prices
-	Neural Network: uses a large number of features which may include time, prices of cryptocurrencies, prices of other market factors (e.g. the S&P500 or commodities), and “buzz” factors


### Database Storage

PostgreSQL will be used to store the data from Kaggle and Yahoo Finance ([SQL Schema](Sql/Schema/schema.sql)). Currently, we are using [csvs](Sql/Resources) for setting up the analysis pipeline. MongoDB will be used to store document-based data including Reddit and Twitter posts.

![SQL schema](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/main/images/SQL_Schema.png?raw=true)  

### Machine Learning

#### Prophet Model

The goal was to create a machine learning model using facebook's prophet library in order to predict the price of bitcoin and some other altcoins. The way to go around this problem was to first extract the data from kaggle. Please, refer [here](https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory?select=coin_Ethereum.csv). We used bitcoin, ethereum, and cardano's cryptocurrencies. The raw data came in CSVs of 10 columns and as many rows as days of lifetime for each coin. For example, Bitcoins csv file looked like this: 

 |    |   SNo | Name    | Symbol   | Date                |    High |      Low |    Open |   Close |   Volume |   Marketcap |
|---:|------:|:--------|:---------|:--------------------|--------:|---------:|--------:|--------:|---------:|------------:|
|  0 |     1 | Bitcoin | BTC      | 2013-04-29 23:59:59 | 147.488 | 134      | 134.444 |  144.54 |        0 | 1.60377e+09 |
|  1 |     2 | Bitcoin | BTC      | 2013-04-30 23:59:59 | 146.93  | 134.05   | 144     |  139    |        0 | 1.54281e+09 |
|  2 |     3 | Bitcoin | BTC      | 2013-05-01 23:59:59 | 139.89  | 107.72   | 139     |  116.99 |        0 | 1.29895e+09 |
|  3 |     4 | Bitcoin | BTC      | 2013-05-02 23:59:59 | 125.6   |  92.2819 | 116.38  |  105.21 |        0 | 1.16852e+09 |
|  4 |     5 | Bitcoin | BTC      | 2013-05-03 23:59:59 | 108.128 |  79.1    | 106.25  |   97.75 |        0 | 1.086e+09   |

Moreover, prophet required the data to be preprocessed into a two-column datetime and price dataframe. The preprocessing included filtering the columns that were not going to be used, changing the date string to a date data type, and renaming the columns as 'DS' for the date and 'y' for the price. 

![BTC Dtypes](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/prophet_btc_dtypes.png)

```
def preprocess_and_model(crypto_df):
    # Preprocessing
    crypto_df = crypto_df.drop(['SNo','Name','Symbol','High','Low','Open','Marketcap','Volume'], axis=1)
    crypto_df['Date'] = crypto_df['Date'].apply(lambda date: dt.strptime(date,'%Y-%m-%d %H:%M:%S'))
    crypto_df = crypto_df.rename(columns={'Date':'ds','Close':'y'})
    train_percent = int(len(crypto_df)*0.80)
    test_periods = int(len(crypto_df)*0.20)
    crypto_train_df = crypto_df.iloc[:train_percent, :]
    
    # Modeling
    m = Prophet()
    m.fit(crypto_train_df)
    future = m.make_future_dataframe(periods=test_periods)
    forecast = m.predict(future)
    forecast_df = forecast[['ds','yhat','yhat_lower','yhat_upper']]
    predict_graph = m.plot(forecast)
    component_graph = m.plot_components(forecast)
    
    # Price prediction (yhat) vs acual price (y)
    price = crypto_df['y']
    acc_forecast = forecast[['ds','yhat']]
    crypto_accuracy_df = acc_forecast.join(price)
    crypto_accuracy_df = crypto_accuracy_df.set_index('ds')
    predict_accuracy_graph = crypto_accuracy_df.plot()
    
    return forecast_df, predict_graph, component_graph, predict_accuracy_graph
```

As it can be seen in the Prophet_ML_Model.ipynb, we wanted to first train the model using data up to 2020, so that the model could predict up to 2021 and we could graphically compare the results to today's price to measure the accuracy. Please refer to the results subtititle. And secondly, as the results were not as accurate because of the 2021 strong and unexpected surge of cryptocurrencies, we wanted to also create Prophet_ML_Future2022.ipynb where we trained our model including data up to present times (mid 2021) to forecast up to mid 2022. The results were a lot different.

##### Results: 

As it can be seen, the predictions for Bitcoin in 2021 were not accurate at all. This is due to the fact that in 2020-2021 there was a strong and unexpected surge in cryptocurrencies as a whole. This could be associated with Covid as the global economy and government's ability to manage the situation was filled with doubt, so many people started relying/trusting in a decentralized monetary system. Not only that, but many countries and entities beginning to trust in these coins pushed a lot more people to invest in them.  

![BTC 2021 Predictions](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/BTC_2021_Prediction.png)

![BTC Accuracy Graph](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/BTC_Accuracy.png)
*Where y is real price and yhat is the model-predicted price*

Moreover, we wanted to train the model using the newest data (up to mid 2021) which displayed the increase in crypto's popularity. Again, these results were not possible to evaluate as they were based on the unknown future (2022), so we wanted to use them to visualize the trend in crypto's price and display the steep slope many investors base their bullish predictions on. 

*Price prediction: from July 2021 to July 22*
![BTC_Prediction](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/BTC_Predictions.png)  

*Yearly, monthly, and weekly components*
![BTC_Components](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/BTC_Components.png)

##### Summary

As a first approach to this project, we wanted to somewhat explore the data and make some simple predictions and visualizations. After evaluating these results, we concluded that there is a lot more analysis to be made. The model was not accurate at all because it was impossible for it to predict the sudden increase of Bitcoin at the end of 2020 using basic statistical predictions on the price. There are many other factors that affect cryptocurrencies now a days such as politics, volume, social media, influencers, other altcoins, crypto new utilities and innovations, adoption, etc. So, furthermore with this project we will be creating reddit and twitter sentiment analyses and using other machine learning models to better predict cryptos' prices. 



#### Neural Network Model
SciKitLearn is the ML library we'll be using to create a classifier.  A function to automate data processing and model training exists, but the time aspect of implementation is still a work in progress.

### Dashboard

In addition to using a Flask template, we will also integrate Plotly.js for a fully functioning and interactive dashboard. It will be hosted on ___.
