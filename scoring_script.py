# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# --------------------------------------------------------------------------

import json  
import pandas as pd 
import numpy as np 
from typing import List, Union, Any

import sys
sys.path.append('/anaconda/envs/azureml_py38/lib/python3.8/site-packages')
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from setuptools import setup
from azureml.telemetry import INSTRUMENTATION_KEY 
from azureml.core import Run
from azureml.core import Experiment
from azureml.core import Workspace
 
from azureml.automl.core.shared import log_server 
from azureml.train.estimator import Estimator

DateGranularity = 'DateGranularity'
StartDate = 'PeriodStartDate'
EndDate = 'PeriodEndDate'
TimeWindow = 'PredictionTimeWindow'
MeasureColumn = 'MeasureColumn'
TimeColumn = 'TimeColumn'

# Initialize global logger 

try: 

    log_server.enable_telemetry(INSTRUMENTATION_KEY) 
    log_server.set_verbosity('INFO') 
    logger = logging.getLogger( 
        'azureml.automl.core.scoring_script_forecasting_v2') 

except Exception: 

    pass 

def init(): 
    
    print(f"This will show up in files under logs/user on the Azure portal2.")

def forecastForeSingleTimeseries(timeseries_df, params, measure_column, time_column):

    #print(timeseriesinfo)

    dimensions_columns = [col for col in timeseries_df if col not in [time_column, measure_column]]

    first_row = timeseries_df.iloc[0]

    data = timeseries_df[[measure_column,time_column]]

    # Convert TimeColumn to datetime
    data[time_column] = pd.to_datetime(data[time_column], errors='coerce')

    # Feature engineering: Extract year, month, day as separate columns
    data['Year'] = data[time_column].dt.year
    data['Month'] = data[time_column].dt.month
    data['Day'] = data[time_column].dt.day

    # Now you can drop the original time column as it's been replaced by more specific features
    data.drop(time_column, axis=1, inplace=True)


    # List of columns to drop
    columns_to_drop = [measure_column]

    # Drop only if the column exists in the DataFrame
    columns_to_drop = [col for col in columns_to_drop if col in data.columns]

    # Now drop the columns      _Value
    X = data.drop(columns_to_drop, axis=1)
    y = data[measure_column]

    # Ensure that the target variable '_Value' is converted to numeric
    y = pd.to_numeric(y, errors='coerce')

    # Drop any rows with NaN in the target variable      _Value
    data.dropna(subset=[measure_column], inplace=True)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = XGBRegressor()
    model.fit(X_train, y_train)

    # Generate future dates for prediction
    future_dates = pd.date_range(start=params[EndDate] + pd.Timedelta(days=1), periods=params[TimeWindow], freq=params[DateGranularity])

    # Create a dataframe for future predictions
    future_data = pd.DataFrame({time_column: future_dates})
    future_data['Year'] = future_data[time_column].dt.year
    future_data['Month'] = future_data[time_column].dt.month
    future_data['Day'] = future_data[time_column].dt.day

    # Ensure the column order in future_data matches the training data
    future_data = future_data.reindex(columns=X_train.columns, fill_value=0)

    # Predict future values
    future_predictions = model.predict(future_data)

    # Prepare the forecast dataframe
    forecast = pd.DataFrame({time_column: future_dates, measure_column: future_predictions})

    for col in dimensions_columns:
        forecast[col] = first_row[col]

    #return ({timeseries_uniqid: forecast})
    return forecast

def executeForecast(file_path):

    # Read the first two rows for parameters
    first_two_rows_df = pd.read_csv(file_path, nrows = 1)

    # dictionaries for standard and custom parameters
    standard_params = [DateGranularity, StartDate, EndDate, TimeWindow, MeasureColumn, TimeColumn]
    params = first_two_rows_df.iloc[0]
    custom_params = [param for param in params if param not in standard_params]

    # Validate and convert standard parameter values
    params[StartDate] = pd.to_datetime(params[StartDate])
    params[EndDate] = pd.to_datetime(params[EndDate])
    params[TimeWindow] = int(params[TimeWindow])

    # Define the TimeColumn and MeasureColumn based on standard parameters
    time_column = params[TimeColumn]
    measure_column = params[MeasureColumn]

    # Read and print raw dimensions data for debugging
    data = pd.read_csv(file_path, skiprows=lambda x: x in [0, 1, 2] or pd.isna(x), header=0)

    headers = data.columns.tolist()

    non_empty_columns = [col for col in data.columns if data[col].notna().any()]
    data = data[non_empty_columns]

    unique_id_columns = data.columns.difference([measure_column, time_column]).tolist()
    print(unique_id_columns)

    #data['uniqid'] = data[unique_id_columns].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    #print(data['uniqid'])

    forecast = data.groupby(unique_id_columns).apply(lambda t: forecastForeSingleTimeseries(t, params, measure_column, time_column))
    
    # set back index from tuple to int
    forecast.reset_index(drop=True, inplace=True)

    # Add the headers as the first row
    headers = forecast.columns.tolist()
    forecast.loc[-1] = headers
    forecast.index = forecast.index + 1
    forecast = forecast.sort_index()

    return forecast
    
def run(mini_batch: List[str]) -> Union[List[Any], pd.DataFrame]: 
    
    for file_path in mini_batch: 
        forecast = executeForecast(file_path)
     
    return pd.DataFrame(forecast)
