"""
Name : old_versions.py in Project: seminar
Author : Simon Leiner
Date    : 06.05.2021
Description: 
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from sklearn.linear_model import LinearRegression

def run_regression(X,Y):

    """This function computes the cross sectional regression.
    :param X: Dataframe containing the Ki: strike price
    :param Y: pandas Seriers containing the target-values: pi - ci (put-call price)
    :returns: intercept,coefficients,r_squared, residuals, r_t
    """

    # get the shape of the DF
    shape_x = X.shape()

    # get the second dimension
    T = shape_x[1]

    # create a simple regression model
    model = LinearRegression(fit_intercept=True)

    # fit the model
    model.fit(X,Y)

    # make predictions
    prediction = model.predict(X)

    # get the residuals
    residuals = (Y - prediction)

    # get the fitted coefficients of the trained model
    coefficients = pd.Series(model.coef_, index=X.columns)

    # intercept
    intercept = model.intercept_

    # get the R^2 of the prediciton
    r_squared = model.score(X,Y)

    # calculate the risk free rate
    r_t = -1/T*np.log(coefficients[""].iloc[0])

    return intercept,coefficients,r_squared, residuals, r_t