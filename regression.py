"""
Name : regression.py in Project: seminar
Author : Simon Leiner
Date    : 24.04.2021
Description: cross-sectional regression functions and estimation of r
"""

import statsmodels.formula.api as sm

class REGRESSION():

    def __init__(self,df):
        self.df = df
        return None

    def fit_REG(self):

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

        return None

    def display_Regression_Table(self):
        print(self.__summary_table)
        return None



