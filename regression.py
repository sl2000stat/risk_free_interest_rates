"""
Name : regression.py in Project: seminar
Author : Simon Leiner
Date    : 24.04.2021
Description: cross-sectional regression functions and estimation of r
"""

import statsmodels.formula.api as sm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# checked: Function works perfectly

# color palette
cmap = sns.color_palette("rocket")
sns.set_theme(palette = cmap)

# surpress warnings
warnings.filterwarnings("ignore")

class REGRESSION():

    def __init__(self,df):
        self.df = df
        return None

    def fit_REG(self):

        """This function fits the regression model and calculates the risk free rate"""

        # time to maturity: there should be only one value so first value is good enough
        self.T = self.df["maturity"].iloc[0]

        # create the model
        model = sm.ols(formula='pi_ci ~ strike', data=self.df)

        # fit the model
        results = model.fit()

        # get reuslts
        # self.alpha = results.params[0]
        self.beta = results.params[1]

        # self.t_stat_alpha = results.tvalues[0]
        # self.t_stat_beta = results.tvalues[1]

        # self.alpha_st = results.bse[0]
        # self.beta_st = results.bse[1]

        # self.adjusted_R = results.rsquared
        self.__summary_table = results.summary()

        self.residuals = results.resid

        self.pred = self.df["pi_ci"] - self.residuals

        # check for 0 division
        if self.T != 0:

            # Note maturitiy T is daily, but we got minutly data and thus recieve minutly estimates
            T = self.T / (24*60)

            if self.beta == 0:
                print("Couldn't calculate the risk free rate , because the beta is 0.")
                self.r_t = 0

            else:
                # calculate the risk free rate with minutely maturites
                self.r_t = -1 / T * np.log(self.beta)

        else:
            print("Couldn't calculate the risk free rate , because the maturity is 0.")
            self.r_t = 0

        return None

    def display_Regression_Table(self):

        """Simple printing function"""

        print(self.__summary_table)
        print("" * 20)
        print(f" The continuously compounded risk free interest rate for Maturity {int(self.T)} days is: {round(self.r_t*100,4)} %")
        print(
            f" The continuously compounded risk free annualized interest rate for Maturity {int(self.T)} days is: {round(self.r_t * 365 * 100, 4)} %")
        print("" * 20)

        return None

    def plot_regression_results(self):

        """Simple plotting function"""

        # plotting the df
        plt.scatter(self.df["strike"], self.df["pi_ci"], color='black', label = "Data")

        # plotting the regression resuluts
        plt.plot(self.df["strike"], self.pred, color='blue', linewidth=2,label = "Regression")

        # styling
        plt.title(f"Regression results for Maturity {int(self.T)} days at time {self.df.quote_datetime.iloc[0]}")
        plt.ylabel("Difference between Put and Call price:")
        plt.xlabel("Strike Price:")
        plt.legend()
        plt.show()

        return None



