"""
Name : estimated_interest_rates.py in Project: seminar
Author : Simon Leiner
Date    : 09.06.2021
Description: Final results of the estimation
"""

# checked: Function works perfectly

import numpy as np
import put_call_parity
import function_collector
import matplotlib.pyplot as plt
import seaborn as sns

# dictionary for saving the data with each fixed differnet desired maturity
fixed_mat_save = {}

# get the dataframe containing the rf for all different maturities
df_result = put_call_parity.get_rf_byput_call()

# convert the maturity back to daily
df_result["maturity"] = df_result["maturity"] / (60*24)
df_result["maturity"] = df_result["maturity"].astype(int)

print("Finished DF:")
print(df_result.head())
print("*" * 10)

# list of maturities in the df
mats_in_df = df_result["maturity"].unique().tolist()

# new rows for fixed maturities:
fixed_mat = [0,7,30,60,90,180]
for fixed_m in fixed_mat:

    # check if the mat is already given by luck
    if fixed_m in mats_in_df:
        pass

    else:

        # for each minute:
        for i in df_result["time_t"].unique():
            # create new row
            new_row = {"risk_free_rate": np.nan, "maturity": fixed_m, "time_t": i}

            # ensure values for interpolation
            if fixed_m == 0:
                new_row = {"risk_free_rate": 0, "maturity": fixed_m, "time_t": i}

            # append to the df
            df_result = df_result.append(new_row, ignore_index=True)

# order by tima and then maturity column
df_result.sort_values(by= ["time_t","maturity"], inplace =True)

# interpolate the risk free rate
df_result["risk_free_rate"].interpolate("linear",inplace = True)

# create multiple df for each fixed maturities
for fixed_m in fixed_mat:

    # subset the data
    fixed_mat_save[fixed_m] = df_result[df_result["maturity"] == fixed_m]

    # get a time index and sort by time
    fixed_mat_save[fixed_m] = function_collector.set_time_index(fixed_mat_save[fixed_m],"time_t")

    # get daily estimates
    fixed_mat_save[fixed_m] = fixed_mat_save[fixed_m].resample("d").mean()

    print(fixed_mat_save[fixed_m])

    # we can now easily plot the results
    # sns.scatterplot(data=fixed_mat_save[fixed_m], x=fixed_mat_save[fixed_m].index, y="risk_free_rate")
    # plt.title(f"Results for maturity : {fixed_m}")
    # plt.show()



