import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
import math

def run_lstm_model (data, target, drop = [], thresholds = [], window = 7, future = 1,
        input_node = { 'units': 12, 'activation': 'relu', 'drop': .2 },
        hidden_nodes = [
            { 'units': 6, 'activation': 'relu', 'drop': .2 }
        ],
        output_node = { 'units': 1, 'activation': 'relu' },
        optimizer = 'adam',
        epochs = 100, save_path = '', percent = .75, verbose = 0):
    """
    Processes data, creates a neuro network, trains, and tests it.  Returns the trained model, history,
    test data predictions, and actual test data.
    
    data: target and features values in a data frame
    target: the name of the y col in data
    drop: cols to drop from the data
    thresholds: an array of obects with properties 'col' and 'threshold'
        col is the column to bin
        threshold is the value below which all vals should be binned into other
    window: the number of days to use for predictions
    future: the number of days in the future the prediction should be
    input_node: an object with properties 'units' and 'activation'
    hidden_nodes: an array of objects with properties 'units' and 'activation'
    output_node: an object with properties 'units' and 'activation'
        units is an int
        activation is a string in: relu, leaky_relu, tanh, sigmoid
    optimizer: a string in: adadelta, adagrad, adam, adamax, ftrl, optimiser, rmsprop, sgd
    epochs: how long to train the model
    save_path: where to save epoch weights; an empty string tells the code to not save epochs 
    percent: the amount of data that should be in the training set
    verbose: an int to set how much data the model outputs while running
    """
    
    # clone data
    data_clone = data.copy()
    
    # clean data
    data_clone = clean_data(data_clone, drop, thresholds)
    
    #get train/test data and make model
    X_train, X_test, y_train, y_test = get_target_and_features(data_clone, target, percent, window, future)    
    model = create_model(X_train, input_node, hidden_nodes, output_node, optimizer)
    
    #run and evaluate model; return model
    return evaluate(model, X_train, X_test, y_train, y_test, epochs, save_path, verbose)

def clean_data(data, drop, thresholds):
    # drop columns
    data = data.drop(drop, 1)
    
    # compress large sets of data
    for threshold in thresholds:
        data = compress(data, threshold['col'], threshold['threshold'])
        
    ####TODO
    # We need code to handle the date data appropriately
    
    #replace cats as dummys
    return encode(data)

def compress (data, col, threshold):
    
    # get vals to replace
    counts = data[col].value_counts()
    replace = list(counts[counts < threshold].index)
    
    #replace the values and return
    for rep in replace:
        data[col] = data[col].replace(rep, 'Other')
    return data

def encode(data):    
    # get cats     
    cat = data.dtypes[data.dtypes == 'object'].index.tolist()
    
    # make encoder and encode
    enc = OneHotEncoder(sparse = False)
    encode = pd.DataFrame(enc.fit_transform(data[cat]))
    encode.columns = enc.get_feature_names(cat)    
    
    # return new df
    return data.merge(encode, left_index = True, right_index = True).drop(cat, 1)

def get_target_and_features(data, target, percent, window, future):
    # Split our preprocessed data into our features and target arrays
    y = data[target].values
    X = data.drop([target], 1).values

    # Split the preprocessed data into a training and testing dataset
    cutoff = math.floor(len(X) * percent)
    X_train = X[:cutoff]
    X_test = X[cutoff:]
    y_train = y[:cutoff]
    y_test = y[cutoff:]
    
    # Create a StandardScaler instances
    scaler = StandardScaler()

    # Fit the StandardScaler
    X_scaler = scaler.fit(X_train)

    # Scale the data
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    
    # create window increments     
    X_train, y_train = set_window(X_train_scaled, y_train, window, future)
    X_test, y_test = set_window(X_test_scaled, y_test, window, future)
   
    
    return X_train, X_test, y_train, y_test

def set_window(X, y, window, future):
    #Add window
    Xin = []
    next_y = []
    for i in range(window, len(X)):
        try:
            next_y.append(y[i + future - 1])
            Xin.append(X[i-window:i])
        # for the cases where there is no future y, just drop the data.         
        except:
            pass
        
    # Reshape data to format for LSTM
    X, y = np.array(Xin), np.array(next_y)
    X = X.reshape(X.shape[0], X.shape[1], X.shape[2])
    
    return X, y

def create_model(X_train, input_node, hidden_nodes, output_node, optimizer):

    # get the input node number
    input_shape = (X_train.shape[1], X_train.shape[2])
    
    # create model
    nn = tf.keras.models.Sequential()
    
    #add layers
    #input
    nn.add(tf.keras.layers.LSTM(units = input_node['units'], input_shape = input_shape,
                                 activation = input_node['activation'], return_sequences = True))
    nn.add(tf.keras.layers.Dropout(input_node['drop']))
        
    #hidden
    for ind, node in enumerate(hidden_nodes):
        if ind == len(hidden_nodes) - 1:
            nn.add(tf.keras.layers.LSTM(units = node['units'], activation = node['activation']))
        else:
            nn.add(tf.keras.layers.LSTM(units = node['units'], activation = node['activation'],
                                        return_sequences = True))
        nn.add(tf.keras.layers.Dropout(node['drop']))
    
    #output
    nn.add(tf.keras.layers.Dense(units = output_node['units']))

    #compile and return
    nn.compile(loss = 'mse', optimizer = optimizer, metrics = ['accuracy'])
    return nn

def create_callback (path, verbose):
    return ModelCheckpoint(
        filepath = path,
        verbose = verbose,
        save_weights_only = True,
        save_freq = 'epoch')

def evaluate(model, X_train, X_test, y_train, y_test, epochs, save_path, verbose):
    # it either wiith callpaths to save epochs or without
    if save_path != '':
        fit_model = model.fit(X_train, y_train, epochs = epochs, verbose = verbose,
                              callbacks = [create_callback(save_path, verbose)])
    else:
        fit_model = model.fit(X_train, y_train, epochs = epochs, verbose = verbose)
    
    #give feedback on model performance
    model_loss, model_accuracy = model.evaluate(X_test, y_test, verbose = verbose)
    print(f"Loss: {model_loss}, Accuracy: {model_accuracy}")
    
    predictions = model.predict(X_test)
    
    #return the model
    return model, fit_model, predictions, y_test