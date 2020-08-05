#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 20:01:01 2020

@author: andrew
"""
from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
import pandas


# 'bins are number of bins; alpha is transparency level'
def make_stuff(file_name,bins=6,colorbins='C01',alpha=0.5):
    
    data = pandas.read_excel(file_name)
    
    plt.hist(data.transpose(), alpha = 0.5, color=colorbins, \
             stacked = True, bins = bins, edgecolor='w',linewidth=1.2)
        

file1 = 'first_file.xlsx'
file2 = 'second_file.xlsx'


make_stuff(file1,6,'magenta',0.7)
make_stuff(file2,6,'blue',0.5)