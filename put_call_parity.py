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


# color palette
cmap = sns.color_palette("rocket")
sns.set_theme(palette = cmap)

# printing options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None

def get_rf_byput_call():

    """
    This function executes the regression and thus the estimation of rf for each maturity in the Dataframe
    :return: Dataframe with rf, Maturity and Time
    """

    # list for saving the matched output needed for the regression
    save_data = []

    # list for saving the results of the regression
    save_result = []

    # dictionary for saving the data with different maturity: Dict contains multiple DF
    save_df = {}

    # get the dataframe
    df = get_df.get_df()

    # calcualte the matrutiy in minutes: D days, m minutes
    df["maturity"] = [int((df["expiration"].iloc[j] - df["quote_datetime"].iloc[j]) / np.timedelta64(1, "m")) for j in
                      range(len(df))]

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

        # for testing
        if mat == 0:
            print(df["quote_datetime"])
            print(df["expiration"])

        # moving window approach
        for i in range(len(df) - 1):

            # if the strike prices and expiration dates are equal
            if df["strike"].iloc[i] == df["strike"].iloc[i + 1] and df["quote_datetime"].iloc[i] == \
                    df["quote_datetime"].iloc[i + 1] and df["expiration"].iloc[i] == \
                    df["expiration"].iloc[i + 1]:

                # get the put and call price and calculate their difference
                if df["option_type"].iloc[i] == "P" and df["option_type"].iloc[i + 1] == "C":
                    put_call = df["bid"].iloc[i] - df["ask"].iloc[i + 1]

                # get the put and call price and calculate their difference
                elif df["option_type"].iloc[i] == "C" and df["option_type"].iloc[i + 1] == "P":
                    put_call = df["bid"].iloc[i + 1] - df["ask"].iloc[i]

                # nothing happend
                else:
                    pass

                # save the data in a dictionary (Maturity being a constant value, thus the time should also be always the same)
                data = {"strike": df["strike"].iloc[i], "pi_ci": put_call, "maturity": df["maturity"].iloc[1]
                    , "quote_datetime": df["quote_datetime"].iloc[i]}

                # append the dictionary to the data list
                save_data.append(data)

            # no mathes found
            else:
                pass

        # convert the data into a df
        df_for_regression = pd.DataFrame(save_data)

        # print(df_for_regression)

        # scatterplot of the original data
        sns.scatterplot(data=df_for_regression, x="strike", y="pi_ci")
        plt.title(f"Scatterplot of the S&P 500 option Data:")
        plt.xlabel(f"Strike Price:")
        plt.ylabel(f"Put Price - Call Price:")
        # plt.show()

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

    # convert the result data into a df for nicer handling
    df_result = pd.DataFrame(save_result)

    print("Finished with estimation.")

    return df_result














