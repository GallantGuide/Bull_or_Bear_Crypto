# Bull or Bear Crypto
Using machine learning to forecast cryptocurrency prices

## Overview
### Topic
We are interested in analyzing what factors are correlated with the prices of cryptocurrencies over time, and whether these factors can be used to predict the future prices of these currencies.
### Justification
Cryptocurrencies are of great interest to the finance community right now.  Their possible impacts on the global economy are being investigated, and it seems likely that some form of block chain currency will be adopted by nations, [including the US]( https://www.popularmechanics.com/technology/a32869513/us-government-research-crypto-dollar/) as official currencies.  Currently, these currencies can be traded on the stock market and show marked volatility as their underlying worth is unclear.  Being able to predict what factors influence cryptocurrency prices could be a key factor is understating why they are so volatile and what could be done to help stabilize them enough to be an official currency.  It is also of great interest to investors to be able to predict the behavior of these coins and take advantage of these predictions to grow investment accounts.
### Source Data
-	[Kaggle Cryptocurrency Dataset]( https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory) (coin prices over time)
-	Yahoo Finance (stock trends over time) - [web-scraper](web_scraping/load/Yahoo_finance_scraper.py)
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
- `Mongo`
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

Pandas will be used to clean the data and perform an exploratory analysis. Further analysis will be completed using Python.

### Database Storage

Mongo is the database we intend to use, and we will integrate Flask to display the data.

### Machine Learning
#### Neural Network Model
SciKitLearn is the ML library we'll be using to create a classifier. Our training and testing setup is ___. Extra ML verbiage here.

### Prophet Model
The goal was to create a machine learning model using facebook's prophet library in order to predict the price of bitcoin and some other altcoins. The way to go around this problem was to first extract the data from kaggle. Please, refer [here](https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory?select=coin_Ethereum.csv). We used bitcoin, ethereum, and solana's cryptocurrencies. The raw data came in CSVs of 10 columns and as many rows as days of lifetime for each coin. For example, Bitcoins csv file looked like this: 

 |    |   SNo | Name    | Symbol   | Date                |    High |      Low |    Open |   Close |   Volume |   Marketcap |
|---:|------:|:--------|:---------|:--------------------|--------:|---------:|--------:|--------:|---------:|------------:|
|  0 |     1 | Bitcoin | BTC      | 2013-04-29 23:59:59 | 147.488 | 134      | 134.444 |  144.54 |        0 | 1.60377e+09 |
|  1 |     2 | Bitcoin | BTC      | 2013-04-30 23:59:59 | 146.93  | 134.05   | 144     |  139    |        0 | 1.54281e+09 |
|  2 |     3 | Bitcoin | BTC      | 2013-05-01 23:59:59 | 139.89  | 107.72   | 139     |  116.99 |        0 | 1.29895e+09 |
|  3 |     4 | Bitcoin | BTC      | 2013-05-02 23:59:59 | 125.6   |  92.2819 | 116.38  |  105.21 |        0 | 1.16852e+09 |
|  4 |     5 | Bitcoin | BTC      | 2013-05-03 23:59:59 | 108.128 |  79.1    | 106.25  |   97.75 |        0 | 1.086e+09   |

Moreover, prophet required the data to be preprocessed into a two-column datetime and price dataframe. The preprocessing included filtering the columns that were not going to be used, change the date string to a date data type, and renaming the columns as 'DS' for the date and 'y' for the price. The final product was a dataframe that looked like this `prophet_btc`:

 |    | ds                  |      y |
|---:|:--------------------|-------:|
|  0 | 2013-04-29 23:59:59 | 144.54 |
|  1 | 2013-04-30 23:59:59 | 139    |
|  2 | 2013-05-01 23:59:59 | 116.99 |
|  3 | 2013-05-02 23:59:59 | 105.21 |
|  4 | 2013-05-03 23:59:59 |  97.75 |

And finally, we created the instance for the model. The prophet_btc dataframe was used to fit it and we predicted for a period of 365 days. That is to say up to mid 2022. 

 |      | ds                  |    yhat |   yhat_lower |   yhat_upper |
|-----:|:--------------------|--------:|-------------:|-------------:|
| 3351 | 2022-07-02 23:59:59 | 66179.6 |      59114.7 |      73165.2 |
| 3352 | 2022-07-03 23:59:59 | 66245.3 |      58955   |      73208.7 |
| 3353 | 2022-07-04 23:59:59 | 66349.7 |      59069.1 |      73530.3 |
| 3354 | 2022-07-05 23:59:59 | 66449.3 |      59646.1 |      74203.6 |
| 3355 | 2022-07-06 23:59:59 | 66574.6 |      59226   |      73589.1 |

#### Results: 
*Price prediction: from July 2021 to July 22*
![BTC_Prediction](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/BTC_Predictions.png)  

*Yearly, monthly, and weekly components*
![BTC_Components](https://github.com/CaptCarmine/Bull_or_Bear_Crypto/blob/ML_Model/Machine_Learning/Resources/BTC_Components.png)

### Dashboard

In addition to using a Flask template, we will also integrate Plotly.js for a fully functioning and interactive dashboard. It will be hosted on ___.
>>>>>>> flask
