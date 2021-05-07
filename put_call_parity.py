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

        # first_maturuity:
        first_maturity = int((df["expiration"].iloc[5] - df["quote_datetime"].iloc[5]) / np.timedelta64(1, "D"))

        # get the put and call price and calculate their difference
        if df["option_type"].iloc[i] == "P" and df["option_type"].iloc[i+1] == "C":
            put_call = df["bid"].iloc[i] - df["ask"].iloc[i+1]

        # get the put and call price and calculate their difference
        if df["option_type"].iloc[i] == "C" and df["option_type"].iloc[i+1] == "P":
            put_call = df["bid"].iloc[i+1] - df["ask"].iloc[i]

        maturity = int((df["expiration"].iloc[i] - df["quote_datetime"].iloc[i]) / np.timedelta64(1, "D"))

        if maturity != first_maturity:
            break

        # save the data in a dictionary
        data = {"strike": df["strike"].iloc[i], "pi_ci": put_call,"maturity": maturity}

        # append the dictionary to the data list
        save_data.append(data)

# convert the data into a df
df_final = pd.DataFrame(save_data)

# print(df_final)

# ensure numeric data
df_final["strike"] = pd.to_numeric(df_final["strike"])
df_final["pi_ci"] = pd.to_numeric(df_final["pi_ci"])

# # # # # #

"plotting"

#get the scatter plot
sns.scatterplot(data=df_final,x = "strike",y="pi_ci")

plt.title(f"Scatterplot of the S&P 500 option Data:")
plt.xlabel(f"Strike Price:")
plt.ylabel(f"Put Price - Call Price:")
# plt.show()

# # # # # #

# create the regression model
model = regression.REGRESSION(df_final)

# fit the model
model.fit_REG()

# print the summary results
model.display_Regression_Table()


sns.lmplot(x="strike", y="pi_ci", data=df_final, x_jitter=.05)
plt.title(f"Linear Regression plot of the S&P 500 option Data:")
plt.xlabel(f"Strike Price:")
plt.ylabel(f"Put Price - Call Price:")
# plt.show()


sns.residplot(x="strike", y="pi_ci", data=df_final,scatter_kws={"s": 80})
plt.title(f"Residualplot of the S&P 500 option Data:")
plt.xlabel(f"Strike Price:")
plt.ylabel(f"Put Price - Call Price:")
# plt.show()
