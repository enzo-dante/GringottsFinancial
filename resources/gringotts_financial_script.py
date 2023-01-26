#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 21:24:25 2023

@author: enzo_dante
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from blue_loans_strings import *

def readData(json_file_name):
    
    json_file = open(json_file_name)
    data = json.load(json_file)

    # transform list json to table dataframe
    loan_data = pd.DataFrame(data)

    # describe data
    loan_data.info()
    loan_data.describe()
    
    # describe interest rates & fico
    loan_data[COLUMN_INTEREST_RATES].describe()
    loan_data[COLUMN_FICO].describe()

    # describe debt-to-income ratio
    loan_data[COLUMN_DEBT_TO_INCOME].describe()
    return loan_data

loan_data = readData(FILE_NAME)

def getUniquePurpose(data):
    """"get unique values from the purpose column"""
    return loan_data[COLUMN_PURPOSE].unique()

print(getUniquePurpose(loan_data))

def addAnnualIncomeColumn(data):
    """get annual income using numpy.exp()"""
    income = np.exp(data[COLUMN_ORIGINAL_ANNUAL_INCOME])
    data[COLUMN_NEW_ANNUAL_INCOME] = income
    return data

loan_data = addAnnualIncomeColumn(loan_data)

def addFicoCategoryColumn(data):
    """analyze fico score and build fico category series column"""
    fico_category = []
    
    for fico in data[COLUMN_FICO]:
    
        # exception handling EAFTP & LBYL
        try:
            if fico >= 300 and fico < 400:
                score = FICO_VERY_POOR
            elif fico >= 400 and fico < 600:
                score = FICO_POOR
            elif fico >= 600 and fico < 660:
                score = FICO_FAIR
            elif fico >= 660 and fico < 700:
                score = FICO_GOOD
            elif fico >= 700:
                score = FICO_EXCELLENT
            else:
                score = FICO_UNKNOWN
    
        except:
            score = FICO_ERROR_UNKNOWN
        
        fico_category.append(score)
    
    # convert into a series datatype for table dataframe
    fico_category = pd.Series(fico_category)
    
    # add new fico cateogry series column to loan table dataframe
    data[COLUMN_FICO_CATEGORY] = fico_category
    return data

loan_data = addFicoCategoryColumn(loan_data)

def addInterestRateAnalysis(data):
    """analyze interest rates and build interest rate category series column"""
    # df.loc as conditional statements
    data.loc[data[COLUMN_INTEREST_RATES] > 0.12, COLUMN_INTEREST_TYPE] = COLUMN_INTEREST_HIGH
    data.loc[data[COLUMN_INTEREST_RATES] <= 0.12, COLUMN_INTEREST_TYPE] = COLUMN_INTEREST_LOW
    return data

loan_data = addInterestRateAnalysis(loan_data)

def barPlot(data, column):
    """number of loans/rows by fico category with groupby"""
    column_plot = data.groupby([column]).size()
    
    column_plot.plot.bar(color="red", width=0.1)
    plt.show()

barPlot(loan_data, COLUMN_FICO_CATEGORY)
barPlot(loan_data, COLUMN_PURPOSE)

def scatterPlot(data, x_column, y_column):
    """build scatter plot for annual income to debt-to-income ratio"""
    ypoint = data[y_column]
    xpoint = data[x_column]
    
    # hex code color
    plt.scatter(xpoint, ypoint, color="#4caf50")
    plt.show()
    
scatterPlot(loan_data, COLUMN_NEW_ANNUAL_INCOME, COLUMN_DEBT_TO_INCOME)

# write to csv
loan_data.to_csv(CLEAN_FILE_NAME, index = True)
