"""
Name : put_call_parity.py in Project: seminar
Author : Simon Leiner
Date    : 24.04.2021
Description: Chapter 2.2: Constructing Risk free assets in order to estimate the risk free interest rate
"""

import pandas as pd
import get_df
import matplotlib.pyplot as plt
import seaborn as sns
import regression
import numpy as np
import function_collector

# color palette
cmap = sns.color_palette("rocket")
sns.set_theme(palette = cmap)

# printing options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None

# list for saving the matched output needed for the regression
save_data = []

# list for saving the resulst of the regression
save_result = []

# dictionary for saving the data with different maturity: Dict contains multiple DF
save_df = {}

# dictionary for saving the data with each fixed differnet desired maturity
fixed_mat_save = {}

# get the dataframe
df = get_df.get_df()

# calcualte the matrutiy: D days, m minutes
df["maturity"] = [int((df["expiration"].iloc[j] - df["quote_datetime"].iloc[j]) / np.timedelta64(1, "m")) for j in range(len(df))]

# get the unique maturity values as a list
unique_maturity = df["maturity"].unique()

# split the dataframe into smaller dataframes with the same maturity and save all the dataframes ina dictionary
for mat in unique_maturity:
    save_df[mat] = df[df["maturity"] == mat]

print("Ready to start with logic.")

# for each dataframe in save_df do:
for mat in save_df:

    # get the dataframe
    df = save_df[mat]


    # moving window approach
    for i in range(len(df) - 1):

        # if the strike prices and expiration dates are equal
        if df["strike"].iloc[i] == df["strike"].iloc[i + 1] and df["quote_datetime"].iloc[i] == df["quote_datetime"].iloc[i + 1]:

            # get the put and call price and calculate their difference
            if df["option_type"].iloc[i] == "P" and df["option_type"].iloc[i + 1] == "C":
                put_call = df["bid"].iloc[i] - df["ask"].iloc[i + 1]

            # get the put and call price and calculate their difference
            elif df["option_type"].iloc[i] == "C" and df["option_type"].iloc[i + 1] == "P":
                put_call = df["bid"].iloc[i + 1] - df["ask"].iloc[i]

            else:
                pass

            # save the data in a dictionary (Maturity being a constant value, thus the time should also be always the same)
            data = {"strike": df["strike"].iloc[i], "pi_ci": put_call, "maturity": df["maturity"].iloc[1]
                ,"quote_datetime" : df["quote_datetime"].iloc[i]}

            # append the dictionary to the data list
            save_data.append(data)

        else:
            pass

    # convert the data into a df
    df_for_regression = pd.DataFrame(save_data)

    # print(df_for_regression)

    # create the regression model
    model = regression.REGRESSION(df_for_regression)

    # fit the model
    model.fit_REG()

    # risk free rate
    risk_free_rate = model.r_t

    # time
    time_t = model.time

    # save the output in a dictionary (Maturity being a constant value)
    res = {"risk_free_rate": risk_free_rate, "maturity": mat, "time_t": time_t}

    # append the dictionary to the data list
    save_result.append(res)

    # print the summary results
    # model.display_Regression_Table()

    # clear the array values and restart the progress
    save_data = []

print("Finished with estimation.")

# convert the result data into a df for nicer handling
df_result = pd.DataFrame(save_result)

# convert the maturity back to daily
df_result["maturity"] = df_result["maturity"] / (60*24)
df_result["maturity"] = df_result["maturity"].astype(int)

# print(df_result)

# list of maturities in the df
mats_in_df = df_result["maturity"].unique().tolist()

# new rows for fixed maturities:
fixed_mat = [7,30,60,90,180]
for fixed_m in fixed_mat:

    # check if the mat is already given by luck
    if fixed_m in mats_in_df:
        pass

    else:
        # create new row
        new_row = {"risk_free_rate": np.nan, "maturity": fixed_m, "time_t": np.nan}

        # append to the df
        df_result = df_result.append(new_row, ignore_index=True)

# order by maturity column
df_result.sort_values(by= ["maturity"], inplace =True)

# interpolate the risk free rate
df_result["risk_free_rate"].interpolate("linear", inplace = True)

#fill up the missing values and always pick the cell above
df_result["time_t"].fillna(method="ffill", inplace=True)

# create multiple df for each fixed maturities
for fixed_m in fixed_mat:
    fixed_mat_save[fixed_m] = df_result[df_result["maturity"] == fixed_m]

    # get a time index an sort by time
    fixed_mat_save[fixed_m] = function_collector.set_time_index(fixed_mat_save[fixed_m],"time_t")

    print(fixed_mat_save[fixed_m])

    # we can now easily plot the results
    sns.scatterplot(data=fixed_mat_save[fixed_m], x=fixed_mat_save[fixed_m].index, y="risk_free_rate")
    plt.title(f"Results for maturity : {fixed_m}")
    plt.show()

# print(df_result)

# convert data into daily estimates: maturities get lost thereby
# df_result = df_result.resample('d', on='time_t').median()

# print(df_result)








