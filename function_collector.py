"""
Name : function_collector.py in Project: seminar
Author : Simon Leiner
Date    : 05.06.2021
Description: Other functions used in the Code
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

    # set the index of the DF as the time Column
    df.set_index(timecolname, inplace = True)

    # sort the index
    df.sort_index(inplace=True)

    return df