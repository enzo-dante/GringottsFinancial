#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 00:01:32 2023

@author: enzo_dante
"""

import unittest
from gringotts_financial_script import readData, addAnnualIncomeColumn, addFicoCategoryColumn, addInterestRateAnalysis
from gringotts_financial_strings import *

class BlueLoansTests(unittest.TestCase):
        
    def setUp(self):
        self.file = FILE_NAME
        self.data = readData(self.file)
        self.data_length = 9578
        
    def test_readData(self):
        """should return dataframe of articles.xlsl excel file"""
        actual = readData(self.file)
        expected = self.data_length

        self.assertEqual(expected, len(actual))

    def test_addAnnualIncomeColumn(self):
        """should return dataframe with with annual income column"""
        actual = addAnnualIncomeColumn(self.data)
        expected = 15

        self.assertEqual(expected, len(actual.columns))
        
    def test_addFicoColumn(self):
        """should return dataframe with with fico category column"""
        actual = addFicoCategoryColumn(self.data)
        expected = 15

        self.assertEquals(expected, len(actual.columns))
  
    def test_addInterestRateColumn(self):
        """should return dataframe with with interest rate category column"""
        actual = addInterestRateAnalysis(self.data)
        expected = 15

        self.assertEquals(expected, len(actual.columns))
        
if __name__ == "__main__":
    unittest.main()
