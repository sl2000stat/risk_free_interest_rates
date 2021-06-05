"""
Name : regression.py in Project: seminar
Author : Simon Leiner
Date    : 24.04.2021
Description: cross-sectional regression functions and estimation of r
"""

import statsmodels.formula.api as sm
import numpy as np

class REGRESSION():

    def __init__(self,df):
        self.df = df
        return None

    def fit_REG(self):

        """This function fits the regression model and calculates the risk free rate"""

        # time to maturity: there should be only one value so first value is good enough
        self.T = self.df["maturity"].iloc[0]

        # time: there should be only one value, there should be only one value so first value is good enough
        self.time = self.df["quote_datetime"].iloc[0]

        # create the model
        model = sm.ols(formula='pi_ci ~ strike', data=self.df)

        # fit the model
        results = model.fit()

        # get reuslts
        self.alpha = results.params[0]
        self.beta = results.params[1]

        self.t_stat_alpha = results.tvalues[0]
        self.t_stat_beta = results.tvalues[1]

        self.alpha_st = results.bse[0]
        self.beta_st = results.bse[1]

        self.adjusted_R = results.rsquared
        self.__summary_table = results.summary()

        self.residuals = results.resid

        # check for 0 division
        if self.T != 0:

            # calculate the risk free rate
            self.r_t = -1 / self.T * np.log(self.beta)

        else:
            print("Couldn't calculate the risk free rate , because the maturity is 0.")
            self.r_t = 0

        return None

    def display_Regression_Table(self):

        """Simple printing function"""

        print(self.__summary_table)
        print("" * 20)
        print(f" The continuously compounded risk free interest rate for Maturity {self.T} days is: {round(self.r_t*100,4)} %")
        print("" * 20)
        print(
            f" The continuously compounded risk free annualized interest rate for Maturity {self.T} days is: {round(self.r_t * 365 * 100, 4)} %")
        print("" * 20)

        return None



