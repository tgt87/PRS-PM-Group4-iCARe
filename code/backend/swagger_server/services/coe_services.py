import six
import pandas as pd
import os 
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
import joblib
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
import sys
import datetime
import json

ROOT_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, ROOT_DIR)

from swagger_server.models.category_prediction import CategoryPrediction
from swagger_server.models.predictions import Predictions

def get_predictions():
    # load forecasted coe prices from json file and return it
    with open('data/coe_prices.json', 'r') as f:
        coe_prices = json.load(f)
    
    return coe_prices

def generate_predictions(category="Category A", num_forecast=48, look_back=36, model_mape=6.8, historical_count=48):
    '''
    predict prices for specified category for #num_forecast of time steps in the future  

    Returns a list of CategoryPrediction object
    '''
    
    categoryPredictionlist = []

    categoryPrediction = CategoryPrediction() # instantiate CategoryPrediction object
    categoryPrediction.name = category # set name as category -> to be used to label the series
    categoryPrediction.series = []

    # Define file paths for dataset, scaler and model
    coe_filepath = '\data\COE_merged.csv'
    model_filepath = '\models\single-LSTM.hdf5'
    scaler_filepath = '\models\single-LSTM-scaler.gz'

    coe_folderpath = ROOT_DIR + coe_filepath
    model_folderpath = ROOT_DIR + model_filepath
    scaler_folderpath = ROOT_DIR + scaler_filepath

    # Read COE dataset into a DataFrame
    df = pd.read_csv(coe_folderpath)
    
    # Select relevant columns and rows from DataFrame
    cat = category[-1] # extract category (A, B, C, etc)
    cols_selected = ['Quota Premium ' + cat]
    price_df = df[cols_selected]
    price_df = price_df.iloc[-look_back:]
    
    # load model and scaler objects
    model = load_model(model_folderpath)
    scaler = joblib.load(scaler_folderpath) 

    # prepare dataset for model inference
    dataset = scaler.transform(price_df).reshape(1,-1)
    
    # make forecasts
    predictions = make_forecasts(model, dataset, 48)
    predictions = scaler.inverse_transform(predictions)
    
    # generate index for forecasted values
    df_date = pd.to_datetime(df['date'], format='%Y-%m-%d')
    latest_date = df_date.iloc[-1-historical_count]
    index = generate_index(latest_date, historical_count+num_forecast)

    
    cutoff = df.shape[0] - historical_count
    historical_df = df[cols_selected]
    historical_df = historical_df.iloc[-historical_count:]
    date_df = df['date']
    date_df = date_df.iloc[-historical_count:]

    # populate categoryPrediction object
    # insert actual values for the past #historical_count exercises
    for i in range(historical_count):
        # create Predictions object
        prediction = Predictions()
        prediction.name = get_label(date_df.iloc[i])      
        prediction.value = historical_df.iloc[i,0]
        prediction.min = historical_df.iloc[i,0]
        prediction.max = historical_df.iloc[i,0]
        # add Predictions object to categoryPrediction
        categoryPrediction.series.append(prediction) 
    
    # insert predictions 
    for i in range(num_forecast):
        # create Predictions object
        prediction = Predictions()
        prediction.name = index[i+historical_count]
        prediction.value = predictions[i][0]
        prediction.min = predictions[i][0] * (1 - model_mape/100)
        prediction.max = predictions[i][0] * (1 + model_mape/100)
        # add Predictions object to categoryPrediction
        categoryPrediction.series.append(prediction) 
    
    
    categoryPredictionString = json.loads(str(categoryPrediction).replace("'", '"')) 
    categoryPredictionlist.append(categoryPredictionString)

    with open('data/coe_prices.json', 'w', encoding='utf-8') as f:
        json.dump(categoryPredictionlist, f, ensure_ascii=False, indent=4)

    return categoryPredictionlist


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)


def make_forecasts(model, testX, n_forecast=48):
    testPredict = []
    for i in range(n_forecast):
        if i == 0:
            seq = testX[i] # get first set of lookback values
            seq = np.reshape(seq, (1, 1, seq.shape[0]))
            pred = model.predict(seq, verbose=0) # predict next time step
            testPredict.append(pred) # add first prediction to testPredict array
        else:
            seq = seq[0][0][1:] # remove first element of lookback values
            seq = np.append(seq, [pred])# append previous time-step prediction
            seq = np.reshape(seq, (1, 1, len(seq)))
            pred = model.predict(seq, verbose=0) # predict next time step
            testPredict.append(pred)          
    testPredict = np.reshape(testPredict, (len(testPredict), 1))
    return testPredict


def generate_index(latest_date=datetime.date.today(), num_forecast=48):
    '''
    Create a list of indexes for the forecasted values
    '''
    month_dict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

    # Extract day, month and year from latest_date
    day = latest_date.day
    month = latest_date.month
    year =  latest_date.year

    # instantiate list of index
    index = [] 

    # determine the next bidding exercise
    next_bidding_exercise = 0 
    if day < 15:
        next_bidding_exercise = 2
    elif day >= 15:
        next_bidding_exercise = 1

    for i in range(num_forecast):
        month_string = month_dict[month]
        year_string = str(year)
        bidding_exercise_string = str(next_bidding_exercise)
        index_string = month_string + ' ' + year_string + ' (' + bidding_exercise_string + ')'
        index.append(index_string)

        # change values for next bidding exercise
        if next_bidding_exercise == 2:
            next_bidding_exercise = 1
            if month == 12: 
                month = 1
                year += 1
            elif month < 12:
                month += 1
        elif next_bidding_exercise == 1:
            next_bidding_exercise = 2
    
    return index

def get_label(date):
    '''
    Convert COE bidding exercise date to 'MMM YYYY (<num>)' format
    '''
    month_dict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
    
    date = pd.to_datetime(date)
    day = date.day
    month = date.month
    year = date.year

    if day <= 14:
        bidding_exercise = '1'
    elif day >= 15:
        bidding_exercise = '2'

    month_string = month_dict[month]
    year_string = str(year)

    label_string = month_string + ' ' + year_string + ' (' + bidding_exercise + ')'
        
    return label_string

