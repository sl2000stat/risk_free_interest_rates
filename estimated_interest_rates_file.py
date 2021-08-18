"""
Name : estimated_interest_rates.py in Project: seminar
Author : Simon Leiner
Date    : 09.06.2021
Description: Final results of the estimation
"""

# checked: Function works perfectly

import numpy as np
import pandas as pd
import put_call_parity_file
import function_collector
import matplotlib.pyplot as plt
import seaborn as sns

# printing options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None

# dictionary for saving the data with each fixed differnet desired maturity
fixed_mat_save = {}

# get the dataframe containing the rf for all different maturities
df_result = put_call_parity_file.get_rf_byput_call()

print("Finished DF:")
print(df_result.head())
print("*" * 10)

# list of maturities in the df
mats_in_df = df_result["maturity"].unique().tolist()

# one example maturity:
mat_example = mats_in_df[0]
df_example = df_result[df_result["maturity"] == mat_example]
df_example = df_example.iloc[1:]

# plotting
sns.scatterplot(data=df_example, x="time_t", y="risk_free_rate")
plt.show()

# new rows for fixed maturities:
fixed_mat = [0,7,30,60,90,180]

# for each minute:
for i in df_result["time_t"].unique():

    # for each fixed maturity
    for fixed_m in fixed_mat:

        # check if the mat is already given
        if fixed_m in mats_in_df:

            pass

        else:

            # create new row
            new_row = {"risk_free_rate": np.nan, "maturity": fixed_m, "time_t": i}

            # ensure values for interpolation
            if fixed_m == 0:
                new_row = {"risk_free_rate": 0, "maturity": fixed_m, "time_t": i}

            # append to the df
            df_result = df_result.append(new_row, ignore_index=True)


# order by time and then maturity column
df_result.sort_values(by= ["time_t","maturity"], inplace =True)
# print(df_result.head(40))

# interpolate the risk free rate
df_result["risk_free_rate"].interpolate("linear",inplace = True)

# remove artificail created 0 rf rate values: error from computation or first rom
df_result = df_result[df_result["risk_free_rate"] != 0]
# print(df_result.head(40))

# create multiple df for each fixed maturities
for fixed_m in fixed_mat:

    if fixed_m == 0:
        pass

    else:

        # subset the data
        fixed_mat_save[fixed_m] = df_result[df_result["maturity"] == fixed_m]

        fixed_mat_save[fixed_m].to_csv(f"csv_files/2010/minutely_estimates{fixed_m}.csv", index=False)
        print(fixed_mat_save[fixed_m])

        # we can now easily plot the results
        # fig, ax = plt.subplots(figsize=(12, 6))
        # ax.ticklabel_format(useOffset=False)
        # fig = sns.scatterplot(data=fixed_mat_save[fixed_m], x=fixed_mat_save[fixed_m]["time_t"], y="risk_free_rate")
        # x_dates = fixed_mat_save[fixed_m]["time_t"].dt.strftime('%Y-%m-%d')
        # ax.set_xticklabels(labels=x_dates, rotation=45, ha='right')
        # plt.show()

        # get a time index and sort by time
        fixed_mat_save[fixed_m] = function_collector.set_time_index(fixed_mat_save[fixed_m], "time_t")

        # get daily estimates
        fixed_mat_save[fixed_m] = fixed_mat_save[fixed_m].resample("D").median()

        fixed_mat_save[fixed_m].dropna(inplace=True)

        fixed_mat_save[fixed_m].to_csv(f"csv_files/2010/daily_estimates{fixed_m}.csv")
        print(fixed_mat_save[fixed_m])









