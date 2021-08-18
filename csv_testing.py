"""
Name : csv_testing.py in Project: seminar
Author : Simon Leiner
Date    : 03.07.2021
Description: 
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

sns.set()

yearlist = [2004,2005,2006,2007,2008,2009,2010]

matlist = [7,30,60,90,180]

frequencylist = ["daily","minutely"]

d = {}


for mat in matlist:

    for frequency in frequencylist:

        freq_mat = frequency + str(mat)

        # save the data into a df
        d[freq_mat] = pd.DataFrame()

        for year in yearlist:

            path = f"C:/Users/win10/PycharmProjects/seminar/csv_files/{year}/{frequency}_estimates{mat}"

            # list with the files
            file_list = glob.glob(os.path.join(path, "*.csv"))

            for file_path in file_list:
                with open(file_path) as f_input:
                    # get the new data
                    df_new = pd.read_csv(f_input, sep=",", header=0)

                    # append them to the big Dataframe
                    d[freq_mat] = d[freq_mat] .append(df_new)

        d[freq_mat].to_csv(f"csv_files/total_{frequency}_estimates_{mat}.csv")


sns.scatterplot(data = df, x = "time_t", y = "risk_free_rate")
plt.title("7 days Mat daily estimates")
plt.show()

sns.lineplot(data = df, x = "time_t", y = "risk_free_rate")
plt.title("7 days Mat daily estimates")
plt.show()

