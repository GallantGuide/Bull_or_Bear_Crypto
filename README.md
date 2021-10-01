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

#### Prophet Model
The goal was to create a machine learning model using facebook's prophet library in order to predict the price of bitcoin and some other altcoins. The way to go around this problem was to first extract the data from kaggle. Please refer [here](https://www.kaggle.com/sudalairajkumar/cryptocurrencypricehistory?select=coin_Ethereum.csv). We used bitcoin, ethereum, and solana's cryptocurrencies. The raw data came in CSVs of 10 columns and as many rows as days of lifetime for each coin. For example, Bitcoins csv file looked like this: 

 |    |   SNo | Name    | Symbol   | Date                |    High |      Low |    Open |   Close |   Volume |   Marketcap |
|---:|------:|:--------|:---------|:--------------------|--------:|---------:|--------:|--------:|---------:|------------:|
|  0 |     1 | Bitcoin | BTC      | 2013-04-29 23:59:59 | 147.488 | 134      | 134.444 |  144.54 |        0 | 1.60377e+09 |
|  1 |     2 | Bitcoin | BTC      | 2013-04-30 23:59:59 | 146.93  | 134.05   | 144     |  139    |        0 | 1.54281e+09 |
|  2 |     3 | Bitcoin | BTC      | 2013-05-01 23:59:59 | 139.89  | 107.72   | 139     |  116.99 |        0 | 1.29895e+09 |
|  3 |     4 | Bitcoin | BTC      | 2013-05-02 23:59:59 | 125.6   |  92.2819 | 116.38  |  105.21 |        0 | 1.16852e+09 |
|  4 |     5 | Bitcoin | BTC      | 2013-05-03 23:59:59 | 108.128 |  79.1    | 106.25  |   97.75 |        0 | 1.086e+09   |

Moreover, prophet required the data to be preprocessed into a two-column datetime and price dataframe. The preprocessing included filtering the columns that were not going to be used, change the date string to a date data type, and renaming the columns as 'DS' for the date and 'y' for the price. 

### Dashboard

In addition to using a Flask template, we will also integrate Plotly.js for a fully functioning and interactive dashboard. It will be hosted on ___.
>>>>>>> flask
