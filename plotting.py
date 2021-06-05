"""
Name : plotting.py in Project: seminar
Author : Simon Leiner
Date    : 31.05.2021
Description: 
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

"plotting"

    # scatterplot of the original data
    sns.scatterplot(data=df_final, x="strike", y="pi_ci")
    plt.title(f"Scatterplot of the S&P 500 option Data:")
    plt.xlabel(f"Strike Price:")
    plt.ylabel(f"Put Price - Call Price:")
    # plt.show()

# plot a linear regression
    sns.lmplot(x="strike", y="pi_ci", data=df_final, x_jitter=.05)
    plt.title(f"Linear Regression plot of the S&P 500 option Data:")
    plt.xlabel(f"Strike Price:")
    plt.ylabel(f"Put Price - Call Price:")
    # plt.show()

    # plot the residuals
    sns.residplot(x="strike", y="pi_ci", data=df_final, scatter_kws={"s": 80})
    plt.title(f"Residualplot of the S&P 500 option Data:")
    plt.xlabel(f"Strike Price:")
    plt.ylabel(f"Put Price - Call Price:")
    # plt.show()