"""
Name : database.py in Project: seminar
Author : Simon Leiner
Date    : 06.05.2021
Description: Contains database queries
"""

# checked: Function works perfectly

def sp500_query():
    query = f"""SELECT * 
                FROM [CBOE].[dbo].[CBOE_60sec_VIEW_SP500_2018] 
                WHERE quote_datetime >= '2018-01-10 09:31:00'
                AND quote_datetime <= '2018-01-10 09:31:30'
                Order BY quote_datetime ASC
    """
    return query

def msft_query():
    query = f"""SELECT TOP (100000) * FROM [CBOE].[dbo].[CBOE_60sec_VIEW_SP500_2018]"""
    return query

def otherfirm_query():
    query = f"""SELECT TOP (100000) * FROM [CBOE].[dbo].[CBOE_60sec_VIEW_SP500_2018]"""
    return query