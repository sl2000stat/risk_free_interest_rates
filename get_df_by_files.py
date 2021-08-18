"""
Name : get_df_by_files.py in Project: seminar
Author : Simon Leiner
Date    : 01.07.2021
Description: Read in the excel files
"""

import pandas as pd
import glob
from datetime import datetime

# try
# eomonth_sl

def get_df():

    """Get the Data from multiple csv files given the folder path, wehere the data lays"""

    print("*" * 10)
    print(f"Starting the process {datetime.now()}")
    print("*" * 10)

    # list with the files
    file_list = glob.glob(r"C:/KIT/SS_2021/Seminar/try/2010_2/*.csv")

    # save the data into a df
    df = pd.DataFrame()

    for file_path in file_list:
        with open(file_path) as f_input:
            # get the new data
            df_new = pd.read_csv(f_input, sep=",")

            # append them to the big Dataframe
            df = df.append(df_new)

    # adjust the time columns
    df["quote_datetime"] = pd.to_datetime(df["quote_datetime"], errors="coerce")
    df["expiration"] = pd.to_datetime(df["expiration"], errors="coerce")

    # ensure numeric data
    df["strike"] = pd.to_numeric(df["strike"])
    df["bid"] = pd.to_numeric(df["bid"])
    df["ask"] = pd.to_numeric(df["ask"])

    # drop unnecessary columns
    df.drop(["underlying_bid","underlying_ask"],axis = 1, inplace = True)

    # remove 0 values: if ask and bid are both 0: there clearly is some data missing, thus remove them
    df = df[(df["bid"] != 0) & (df["ask"] != 0)]

    print(f"Data recieved sucessfully. ({str(df.shape[0])} rows): {datetime.now()}")
    print("*" * 10)

    return df

