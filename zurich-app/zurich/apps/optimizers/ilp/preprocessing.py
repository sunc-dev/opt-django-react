# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 12:30:58 2020

@author: csunj
"""

try:
    import os
    import pandas as pd

except (RuntimeError, Exception) as err_msg:
    print("Some Modules are Missing {}".format(err_msg))


class Path():
    '''class to define path'''
    def __init__(self):
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.folder = os.path.join(self.root, 'data')

    def path_items(self):
        '''function to return root and folder paths'''
        return self.root, self.folder


class Processor():
    '''class that defines data load'''
    def __init__(self):
        self.data = 'Id'

    def get_data(self, __data):
        '''function to load data - replace with sql connection'''
        root, folder = Path().path_items()
        data = pd.read_csv(os.path.join(root, folder, __data))

        return data

    def normalize_data(self, data):
        '''function to run normalization logic on data'''
        inputs = data

        def norm_water(row):
            if row['Water'] == 'Poor':
                return 0.4
            if row['Water'] == 'Good':
                return 0.6
            if row['Water'] == 'Excellent':
                return 1
            return 0

        def norm_endangered(row):
            if row['Endangered'] <= 40:
                return row['Endangered'] * 0.005
            if row['Endangered'] > 60:
                return (row['Endangered'] - 60) * 0.005 + .8
            return (row['Endangered'] - 40) * 0.03 + 0.2

        def norm_reserve(row):
            if row['NaturalReserve'] <= 7:
                return ((-0.5 / 7) * row['NaturalReserve']) + 1
            return (-0.5 / 3) * (row['NaturalReserve'] - 7) + 0.5

        inputs['Area'] = inputs['Area'] * 0.2
        inputs['Trees'] = inputs['Trees'] * 1 / 200
        inputs['Water'] = inputs.apply(lambda row: norm_water(row), axis=1)
        inputs['Endangered'] = inputs.apply(lambda row: norm_endangered(row),
                                            axis=1)
        inputs['NaturalReserve'] = inputs.apply(lambda row: norm_reserve(row),
                                                axis=1)
        return inputs
