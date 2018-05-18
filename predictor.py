"""This is an implementation of the stock market predictor as found here:
https://www.datacamp.com/community/tutorials/lstm-python-stock-market

As I follow the tutorial, I'm going to be keeping detailed comments that should
make it easy to read through and understand what's going on"""

import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf
# This line comes from here:
# https://stackoverflow.com/questions/50394873/import-pandas-datareader-gives-importerror-cannot-import-name-is-list-like
# Don't know why it works, but it fixes an import error
# Has to come after pd is already imported
pd.core.common.is_list_like = pd.api.types.is_list_like
from pandas_datareader import data
from sklearn.preprocessing import MinMaxScaler

# =============== LOAD DATE =============================
# This whole block is for creating a pandas DataFrame
# So far, it looks like it's just a database
# Not sure what function it serves

# Kaggle is a zip file database full of historical stock data
# Alphavantage is an API that delivers stock data

data_source = 'kaggle'

if data_source == 'alphavantage':

    # Got this API key from https://www.alphavantage.co/support/#api-key
    # Just put in some bullshit info and a throwaway email
    api_key = '84CEWPCQP5BM2PNJ'

    # American Airlines ticker abbreviation
    ticker = 'AAL'

    # JSON file with all the stock market data
    url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)

    # Save data to this file
    file_to_save = 'stock_market_data-%s.csv'%ticker

    # If CSV file doesn't exist, create it with data from alphavantage
    if not os.path.exists(file_to_save):

        # Loads data from alphavantage api
        url = urllib.request.urlopen(url_string)

        # Parses data into json dictionary
        data = json.loads(url.read().decode())

        # Selects one subdictionary. I don't know what the other keys do
        # This subdict is a collection of dates and their data
        data = data['Time Series (Daily)']

        # I believe a Pandas DataFrame acts like a table
        # So this is creating the headers
        df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])

        # Loops through each key,value pair in the data dict
        # Keys are dates, values are subdicts
        for date, values in data.items():

            # Reformat date into computer-readable format
            date = dt.datetime.strptime(date, '%Y-%m-%d')

            # This list becomes the row for each date in the DataFrame
            data_row = [
                date.date(),
                float(values['3. low']),
                float(values['2. high']),
                float(values['4. close']),
                float(values['1. open'])
            ]

            # I believe this appends the row to the end of the DataFrame
            # Who the fuck thought of this convoluted syntax?
            df.loc[-1,:] = data_row

            # Move onto the next row
            df.index += 1

        # Get that sweet sweet data saved away
        df.to_csv(file_to_save)
        print('Data saved to : %s' % file_to_save)

    # If the data is already there, just load it from the CSV
    else:
        df = pd.read_csv(file_to_save)
        print('File already exists. Loading data from CSV')

else:
    df = pd.read_csv(os.path.join('Stocks','hps.us.txt'),
                     delimiter=',',
                     usecols=['Date','Open','High','Low','Close'])
    print('Loaded data from the Kaggle repository')



# Downloaded this stock market database from here
# https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/version/3
# Unzipped and is now in project folder
