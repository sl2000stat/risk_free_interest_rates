"""
Name : database.py in Project: seminar
Author : Simon Leiner
Date    : 06.05.2021
Description: Contains database queries
"""

def sp500_query():
    query = f"""SELECT TOP (1000) * FROM [CBOE].[dbo].[CBOE_60sec_VIEW_SP500_2018]"""
    return query