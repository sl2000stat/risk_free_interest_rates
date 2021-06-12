"""
Name : get_df.py in Project: seminar
Author : Simon Leiner
Date    : 06.05.2021
Description: Get the Dataframe from the database
"""

import database
from config.config_utils import ConfigUtils
import pyodbc
import pandas as pd
from datetime import datetime

# checked: Function works perfectly

def get_df():

    """This functions gets the Dataframe containing the option information"""

    print("*" * 10)
    print(f"Starting the process {datetime.now()}")
    print("*" * 10)

    # get the constants from the config file
    cfg = ConfigUtils()
    server = cfg.read_cfgvalue("DB", "server")
    databasename = cfg.read_cfgvalue("DB", "database")
    username = cfg.read_cfgvalue("DB", "username")
    password = cfg.read_cfgvalue("DB", "password")
    driver = "{ODBC Driver 17 for SQL Server}"

    # define the name of the columns
    # colnames = ["underlying_symbol", "quote_datetime", "root", "expiration", "strike", "option_type", "open", "high",
    #             "low", "close",
    #             "trade_volume", "bid_size", "bid", "ask_size", "ask", "underlying_bid", "underlying_ask",
    #             "number_of_exchanges",
    #             "sonstiges"]

    # things for saving the data (empty array)
    data = []

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
        rows = []
        print(f"The following Exepction ocurred: {str(e)}  and if nothing is shown: MemoryError" )

    # if rows object is empty
    if not rows:
        raise Exception("Something went wrong with getting the Data.")

    # for each row do:
    for row in rows:
        dict_data = {'underlying_symbol': row[0],
                     'quote_datetime': row[1],
                     # 'root': row[2],
                     'expiration': row[3],
                     'strike': row[4],
                     'option_type': row[5],
                     # 'open': row[6],
                     # 'high': row[7],
                     # 'low': row[8],
                     # 'close': row[9],
                     # 'trade_volume': row[10],
                     # 'bid_size': row[11],
                     'bid': row[12],
                     # 'ask_size': row[13],
                     'ask': row[14],
                     # 'underlying_bid': row[15],
                     # 'underlying_ask': row[16],
                     # 'number_of_exchanges': row[17],
                     # 'sonstiges': row[18]
                     }

        # append to data
        data.append(dict_data)

    # convert the data into a df
    df = pd.DataFrame(data)

    # adjust the time columns
    df["quote_datetime"] = pd.to_datetime(df["quote_datetime"], errors = "coerce")
    df["expiration"] = pd.to_datetime(df["expiration"], errors="coerce")

    # ensure numeric data
    df["strike"] = pd.to_numeric(df["strike"])
    df["bid"] = pd.to_numeric(df["bid"])
    df["ask"] = pd.to_numeric(df["ask"])

    # print(df)
    print(f"Data recieved sucessfully. ({str(df.shape[0])} rows)")
    print("*" * 10)

    return df
