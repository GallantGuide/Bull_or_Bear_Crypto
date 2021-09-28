# Import our dependencies
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint

def run_nn_model (data, target, drop = [], thresholds = [],
        input_node = { 'units': 80, 'activation': 'relu' },
        hidden_nodes = [{ 'units': 30, 'activation': 'relu' }],
        output_node = { 'units': 1, 'activation': 'sigmoid' },
        optimizer = 'adam',
        epochs = 100, save_path = '', seed = 0, verbose = 0):
    """
    Processes data, creates a neuro network, trains, and tests it.  Returns the trained model.
    data: target and features values in a data frame
    target: the name of the y col in data
    drop: cols to drop from the data
    thresholds: an array of obects with properties 'col' and 'threshold'
        col is the column to bin
        threshold is teh value below which all vals should be binned into other
    target: the name of the target col
    input_node: an object with properties 'units' and 'activation'
    hidden_nodes: an array of objects with properties 'units' and 'activation'
    output_node: an object with properties 'units' and 'activation'
        units is an int
        activation is a string in: relu, leaky_relu, tanh, sigmoid
    optimizer: a string in: adadelta, adagrad, adam, adamax, ftrl, optimiser, rmsprop, sgd
    epochs: how long to train the model
    save_path: where to save epoch weights; an empty string tells the code to not save epochs 
    seed: an int to seed the train/test split on
    verbose: an int to set how much data the model outputs while running
    """
    
    # clone data
    data_clone = data.copy()
    
    # clean data
    data_clone = clean_data(data_clone, drop, thresholds)
    
    #get train/test data and make model
    X_train, X_test, y_train, y_test = get_target_and_features(data_clone, target, seed)
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


def get_target_and_features(data, target, seed):
    # Split our preprocessed data into our features and target arrays
    y = data[target].values
    X = data.drop([target], 1).values

    # Split the preprocessed data into a training and testing dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = seed)

    # Create a StandardScaler instances
    scaler = StandardScaler()

    # Fit the StandardScaler
    X_scaler = scaler.fit(X_train)

    # Scale the data
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

def create_model(X_train, input_node, hidden_nodes, output_node, optimizer):

    # get the input node number
    num_features = len(X_train[0])
    
    # create model
    nn = tf.keras.models.Sequential()
    
    #add layers
    #input
    nn.add(tf.keras.layers.Dense(units = input_node['units'], input_dim = num_features,
                                 activation = input_node['activation']))

    #hidden
    for node in hidden_nodes:
        nn.add(tf.keras.layers.Dense(units = node['units'], activation = node['activation']))
        
    #output
    nn.add(tf.keras.layers.Dense(units = output_node['units'], activation = output_node['activation']))

    #compile and return
    nn.compile(loss = 'binary_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
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
    
    #return the model
    return model