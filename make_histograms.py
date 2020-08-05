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

your_file_here = 'test.xlsx'

data = pandas.read_excel(your_file_here)

#number of histogram bins
bins = 6
#color of your bins
colorbins = 'C0'

plt.hist(data.transpose(), alpha = 0.5, color=colorbins, \
         stacked = True, bins = bins, edgecolor='w',linewidth=1.2)