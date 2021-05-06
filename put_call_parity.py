"""
Name : put_call_parity.py in Project: seminar
Author : Simon Leiner
Date    : 24.04.2021
Description: Chapter 2.2: Constructing Risk free assets in order to estimate the risk free interest rate
"""

import pandas as pd
import get_df
import matplotlib.pyplot as plt
import regression

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# get the dataframe
df = get_df.get_df()

# things for saving the data
save_data = []

# moving window approach
for i in range(len(df) - 1):

    # if the strike prices and expiration dates are equal
    if df["strike"].iloc[i] == df["strike"].iloc[i + 1] and df["expiration"].iloc[i] == df["expiration"].iloc[i + 1]:

        # get the put and call price and calculate their difference
        if df["option_type"].iloc[i] == "P" and df["option_type"].iloc[i+1] == "C":
            put_call = df["bid"].iloc[i] - df["ask"].iloc[i+1]

        # get the put and call price and calculate their difference
        if df["option_type"].iloc[i] == "C" and df["option_type"].iloc[i+1] == "P":
            put_call = df["bid"].iloc[i+1] - df["ask"].iloc[i]

        # save the data in a dictionary
        data = {"strike": df["strike"].iloc[i], "pi_ci": put_call}

        # append the dictionary to the data list
        save_data.append(data)

# convert the data into a df
df_final = pd.DataFrame(save_data)

# ensure numeric data
df_final["strike"] = pd.to_numeric(df_final["strike"])
df_final["pi_ci"] = pd.to_numeric(df_final["pi_ci"])

# create the regression model
model = regression.REGRESSION(df_final)

# fit the model
model.fit_REG()

# print the summary results
model.display_Regression_Table()

# plt.scatter(df_final["strike"],df_final["pi_ci"])
# plt.show()

# check regression assumptions: Testing or plotting
# 1 homoscedity of residuals
# 2 uncorrelated over time residuals, acf,pacf

# regression results

# plot regression, residuals
