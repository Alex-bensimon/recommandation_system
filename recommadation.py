# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 13:36:59 2020

@author: Alex
"""


import pandas as pd 

hotels = pd.read_csv('hotels.csv')
reviews = pd.read_csv('reviews.csv')

print(reviews.info())

reviews.drop_duplicates(subset ="title",keep = 'first', inplace=True)

print(reviews.info())

print(hotels.info())

hotels.drop_duplicates(subset ="name",keep = 'first', inplace=True)

print(hotels.info())

