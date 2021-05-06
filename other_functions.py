"""
Name : other_functions.py in Project: seminar
Author : Simon Leiner
Date    : 06.05.2021
Description: Different functions used in the code
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def set_time_index(df, timecolname):

    """This function sets the time col as index and makes sure it's a datetime object.

    :param df: full Dataframe
    :param timecolname: colname of the column that has time information in it
    :return: full Dataframe
    """
    # take the time column and convert it to a datetime object
    df[timecolname] = pd.to_datetime(df[timecolname])

    # set the index of the DF as the time Column
    df.set_index(timecolname, inplace = True)

    return df