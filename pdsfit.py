# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 19:11:35 2020

@author: garci
"""
''' 
A PROBABILITY DENSITY FUNCTION (PDF) FITTING PROGRAM
pdsfit.py  - fit a single dataset to a probability density function and obtain corresponding statistics
Andrew Garcia, 2020

'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
import xlwings as xw
import pandas as pd
#frame_pdsfit has make and LastRow
from frame_pdsfit import *


''' ARGS LIBRARY (line 27) '''

# import the necessary packages
import argparse
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
'----------------------------------------------------------------------------------------'
'SPECIFY PATH AND FILE NAME HERE'
ap.add_argument("-p", "--path", 
                default= r'C:\[your_path]\your_file.xls', 
                help="path to dataset with file name")
'----------------------------------------------------------------------------------------'
ap.add_argument("-s", "--sheet", default='Results', 
                help="name of sheet containing dataset (default: Results)")
ap.add_argument("-v", "--column", default='H2', 
                help="vector/column with dataset (default: H2)")
ap.add_argument("-d", "--distribution", default=['gauss','lognorm','expon','gamma','beta'],
                nargs = '+', type =str,
                help="distribution fitting models *type each separated by a space\
                i.e. -d gauss lognorm ... (default: all)") 
ap.add_argument("-plt", "--plots", default='y', 
                help="make plots for all data being fitted (default: y[yes])")
ap.add_argument("-b", "--bins", type=int, default=8, 
                help="# of bins to display for histogram (default: 8)")
ap.add_argument("-r", "--xrange", default=None,nargs = '+', 
                help="range of x-axis expressed as: -r low high [e.g. -r 0 400] (default: None)")  
ap.add_argument("-c", "--colorbins", default='dodgerblue',
                help="color of bins (default: 'dodgerblue')")  
ap.add_argument("-l", "--label", default='', 
                help="plot name or label")
args = vars(ap.parse_args())


def one():
    idx = args["sheet"]
    book=xw.Book(args["path"])    
    column_data = book.sheets[idx].range( args["column"] + ':' + args["column"][0]+str(lastRow(idx,book)) ).value
    
#    plt.style.use("ggplot")
    f = make_wplt if args["plots"] == 'y' else make
    f(column_data,args["label"],args["distribution"],bins=args["bins"],\
         xlims=[float(args["xrange"][0]),float(args["xrange"][1])] if args["xrange"] is not None else '',\
         colorbins=args["colorbins"])
    book.close()
    
one()