# Bull_or_Bear_Crypto

<<<<<<< HEAD

# Work Notes:
The neural network function DOES NOT handle date data.  We'll have to add code to the data processing function for this once we decide how to handle the date data.  For current the test, I am just dropping the date column from the data frame. -- Cristina
=======
## Technologies Used

- `Beautiful Soup`
- `Splinter`
- `Pandas`
- `SQL`
- `Mongo`
- `Python`
  - `Prophet` library

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
