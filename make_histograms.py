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


'''bins         = number of bins
   colorbins    = color of bins 
   alpha        = transparency level
   den_norm     = density normalization (recommended)'''
def make_stuff(file_name,bins=6,colorbins='C01',alpha=0.5,den_norm='y'):
    
    
    data = pandas.read_excel(file_name)
    
    n0, bin_edges = np.histogram(data,bins = bins)
    
    binwidth = bin_edges[1]-bin_edges[0]
    'Area of scaled histogram'
    Ahist = np.sum(n0*binwidth)
    
    
#    n = n/np.max(n0)
    
    'plot density histogram'
#    wts = np.ones_like(data) / np.max(n0)
    wts = np.ones_like(data) /  Ahist if den_norm == 'y' else None
    
    
    
    n, bins, patches = plt.hist(data.transpose(), alpha = 0.5, color=colorbins, \
             stacked = True, weights=wts,bins = bins, edgecolor='w',linewidth=1.2)
        

'EXECUTION'


file1 = 'first_file.xlsx'
file2 = 'second_file.xlsx'

plt.figure()

make_stuff(file1,10,'magenta',0.7)
make_stuff(file2,6,'blue',0.5)