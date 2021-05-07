"""
Name : get_df.py in Project: seminar
Author : Simon Leiner
Date    : 06.05.2021
Description: Get the Dataframe
"""

import database
from config.config_utils import ConfigUtils
import pyodbc
import pandas as pd
import other_functions

def get_df():

    """This functions gets the Dataframe containing the option information"""

    # get the constants from the config file
    cfg = ConfigUtils()
    server = cfg.read_cfgvalue("DB", "server")
    databasename = cfg.read_cfgvalue("DB", "database")
    username = cfg.read_cfgvalue("DB", "username")
    password = cfg.read_cfgvalue("DB", "password")
    driver = "{ODBC Driver 17 for SQL Server}"

    # define the name of the columns
    colnames = ["underlying_symbol", "quote_datetime", "root", "expiration", "strike", "option_type", "open", "high",
                "low", "close",
                "trade_volume", "bid_size", "bid", "ask_size", "ask", "underlying_bid", "underlying_ask",
                "number_of_exchanges",
                "sonstiges"]

    # things for saving the data
    data = []

    try:

        # connect to database
        conn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + databasename + ';UID=' + username + ';PWD=' + password)

        # create cursor object
        cursor = conn.cursor()

        # get the query
        query = database.sp500_query()

        # execute the query
        cursor.execute(query)

        # get all data
        rows = cursor.fetchall()

    except Exception as e:
        print("The following Exepction ocurred: " + str(e))

    # for each row do:
    for row in rows:
        dict_data = {'underlying_symbol': row[0], 'quote_datetime': row[1], 'root': row[2], 'expiration': row[3],
                     'strike': row[4], 'option_type': row[5], 'open': row[6], 'high': row[7], 'low': row[8],
                     'close': row[9],
                     'trade_volume': row[10], 'bid_size': row[11],
                     'bid': row[12], 'ask_size': row[13], 'ask': row[14],
                     'underlying_bid': row[15], 'underlying_ask': row[16],
                     'number_of_exchanges': row[17], 'sonstiges': row[18]}

        # append to data
        data.append(dict_data)

    # convert the data into a df
    df = pd.DataFrame(data)

    # adjust the time coolumns
    df["quote_datetime"] = pd.to_datetime(df["quote_datetime"], errors = "coerce")
    df["expiration"] = pd.to_datetime(df["expiration"], errors="coerce")

    # group the data by expiration date and strike price
    df.groupby(["quote_datetime","expiration", "strike"], axis=1)

    # set the time column as index
    # df = other_functions.set_time_index(df,"quote_datetime")

    # sort the dataframe
    # df.sort_index(inplace = True)

    # print(df)

    return df
