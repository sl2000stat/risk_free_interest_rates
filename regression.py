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

        # time to maturity
        self.T = self.df["maturity"].mean()

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

        # calculate the risk free rate
        self.r_t = -1 / self.T * np.log(self.beta)

        return None

    def display_Regression_Table(self):
        print(self.__summary_table)


        print("" * 20)
        print(f" The continuously compounded risk free interest rate for Maturity {self.T} is: {round(self.r_t*100,4)} %")
        print("" * 20)
        return None



