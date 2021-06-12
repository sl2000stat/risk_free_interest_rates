"""
Name : put_call_parity.py in Project: seminar
Author : Simon Leiner
Date    : 24.04.2021
Description: Chapter 2.2: Constructing Risk free assets in order to estimate the risk free interest rate
"""

import pandas as pd
import get_df
import regression
import numpy as np

# printing options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None

def get_rf_byput_call():

    """
    This function executes the regression and thus the estimation of rf for each maturity in the Dataframe
    :return: Dataframe with rf, Maturity and Time
    """

    # list for saving the results of the regression
    save_result_regression = []

    # dictionary for saving the data with different maturity: Dict contains multiple DF
    save_df = {}

    # get the dataframe
    df = get_df.get_df()

    # calcualte the matrutiy in minutes: D days, m minutes
    df["maturity"] = [int((df["expiration"].iloc[j] - df["quote_datetime"].iloc[j]) / np.timedelta64(1, "m")) for j in
                      range(len(df))]

    # sort for maturites
    df.sort_values(by=["strike","quote_datetime"], inplace=True)

    print("Recieved DF:")
    print(df.head(5))
    print("*" * 10)

    # get the unique maturity values as a list
    unique_maturity = df["maturity"].unique()

    print(f"There are {len(unique_maturity)} different Maturites")
    print("*" * 10)

    # split the dataframe into smaller dataframes with the same maturity and save all the dataframes ina dictionary
    for mat in unique_maturity:
        save_df[mat] = df[df["maturity"] == mat]

    print("Ready to start with logic:")
    print("*" * 10)

    # for each dataframe in save_df do:
    for mat in save_df:

        # list for saving the matched output needed for the regression
        save_data_fl = []

        # get the dataframe
        df = save_df[mat]

        # print(df.head())
        # print("*" * 10)

        # moving window approach
        for i in range(len(df) - 1):

            # if the strike prices and expiration dates are equal
            if df["strike"].iloc[i] == df["strike"].iloc[i + 1] and df["quote_datetime"].iloc[i] == \
                    df["quote_datetime"].iloc[i + 1]:

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
                save_data_fl.append(data)

            # no matches found
            else:
                pass

        # convert the data into a df
        df_for_regression = pd.DataFrame(save_data_fl)

        # print("DF for regression:")
        # print(df_for_regression.head())
        # print("*" * 10)

        # for each minute:
        for time_ in df_for_regression["quote_datetime"].unique():

            # subset the data
            df_for_regression = df_for_regression[df_for_regression["quote_datetime"] == time_]

            # create the regression model
            model = regression.REGRESSION(df_for_regression)

            # fit the model
            model.fit_REG()

            # print the result
            # model.display_Regression_Table()

            # plot the result
            # model.plot_regression_results()

            # risk free rate
            risk_free_rate = model.r_t

            # save the output in a dictionary (Maturity being a constant value)
            res = {"risk_free_rate": risk_free_rate, "maturity": mat, "time_t": time_}

            # append the dictionary to the data list
            save_result_regression.append(res)

    # convert the result data into a df for nicer handling
    df_result = pd.DataFrame(save_result_regression)

    print("Finished with estimation.")
    print("*" * 10)

    # print(df.head(5))

    return df_result













