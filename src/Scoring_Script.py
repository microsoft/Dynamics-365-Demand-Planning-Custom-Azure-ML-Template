# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# --------------------------------------------------------------------------

import json  
import pandas as pd 
import numpy as np 
from typing import List, Union, Any


from xgboost import XGBRegressor
from azureml.telemetry import INSTRUMENTATION_KEY 
from azureml.core import Run
from azureml.automl.core.shared import log_server 

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

def forecastSingleTimeseries(timeseries_df, params, measure_column, time_column):

    # Read the dimension columns of the timeseries
    dimensions_columns = [col for col in timeseries_df if col not in [time_column, measure_column]]
    
    # Read the dimension column values of the timeseries
    first_row = timeseries_df.iloc[0]

    # Create data frame of the timeseries data including measure and time
    data = timeseries_df[[measure_column,time_column]]

    # Convert TimeColumn to datetime
    data[time_column] = pd.to_datetime(data[time_column], errors='coerce')

    # Feature engineering: Extract year, month, day as separate columns
    data['Year'] = data[time_column].dt.year
    data['Month'] = data[time_column].dt.month
    data['Day'] = data[time_column].dt.day

    # Drop the original time column as it's been replaced by more specific features
    data.drop(time_column, axis=1, inplace=True)

    # Drop the measure column from X and assign it to y
    X = data.drop([measure_column], axis=1)
    y = data[measure_column]

    # Ensure that the measure column is converted to numeric
    y = pd.to_numeric(y, errors='coerce')

    # Drop any rows with NaN in the measure column
    data.dropna(subset=[measure_column], inplace=True)

    # Train the model
    model = XGBRegressor()
    model.fit(X, y)

    # Generate future dates for prediction
    future_dates = pd.date_range(start=params[StartDate] + pd.Timedelta(days=1), periods=params[TimeWindow], freq=params[DateGranularity])

    # Create a dataframe for future predictions
    future_data = pd.DataFrame({time_column: future_dates})
    future_data['Year'] = future_data[time_column].dt.year
    future_data['Month'] = future_data[time_column].dt.month
    future_data['Day'] = future_data[time_column].dt.day

    # Ensure the column order in future_data matches the training data
    future_data = future_data.reindex(columns=X.columns, fill_value=0)

    # Predict future values
    future_predictions = model.predict(future_data)

    # Prepare the forecast dataframe
    forecast = pd.DataFrame({time_column: future_dates, measure_column: future_predictions})

    # Set values of the dimension columns for the timeseries
    for col in dimensions_columns:
        forecast[col] = first_row[col]

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

    # Read data and remove the empty columns
    data = pd.read_csv(file_path, skiprows=lambda x: x in [0, 1, 2] or pd.isna(x), header=0)
    non_empty_columns = [col for col in data.columns if data[col].notna().any()]
    data = data[non_empty_columns]

    # Create unique id for timeseries and group them
    unique_id_columns = data.columns.difference([measure_column, time_column]).tolist()
    forecast = data.groupby(unique_id_columns).apply(lambda t: forecastSingleTimeseries(t, params, measure_column, time_column))
    
    # Set back index from tuple to int
    forecast.reset_index(drop=True, inplace=True)

    # Add the column headers as the first row
    headers = forecast.columns.tolist()
    forecast.loc[-1] = headers
    forecast.index = forecast.index + 1
    forecast = forecast.sort_index()

    return forecast
    
def run(mini_batch: List[str]) -> Union[List[Any], pd.DataFrame]: 
    
    for file_path in mini_batch: 
        forecast = executeForecast(file_path)

        return pd.DataFrame(forecast)
