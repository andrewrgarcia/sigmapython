# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 19:11:35 2020

@author: garci
"""
''' 
A PROBABILITY DENSITY FUNCTION (PDF) FITTING PROGRAM
pdsfit_more.py  - fit multiple datasets to probability distributions and tabulate all statistical data thereof to Excel
Andrew Garcia, 2020

'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
# import xlwings as xw
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
                default= '/home/andrew/scripts/statistics/templates/pdsfit/dataset', 
                help="global path to folder containing folders with datasets")

ap.add_argument("-fn", "--xlfilename", default='Results.xls', 
                help="To simplify iteration of several fits, all Excel files from \
                different experiments (different folders) should have the same name\
                (default file name: Results.xls)")
'----------------------------------------------------------------------------------------'
ap.add_argument("-s", "--sheet", default='Results', 
                help="name of sheet containing dataset (default: Results)")
ap.add_argument("-n", "--column_name", default='value', 
                help="column name to get histogram info ")
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

ap.add_argument("-xl", "--toExcel", default='y', 
                help="tabulate results of all statistical fits to excel file\\ python pandas module\
                (default: y[yes])")

args = vars(ap.parse_args())

import os 

folders = os.listdir(args["path"])
print(folders)

def mult(toexcel=args["toExcel"]):
    
    Gval = []
    folder_names = os.listdir(args["path"])
    for name in folder_names:
        # book=xw.Book(args["path"]+r'/'+ name + r'/' + args["xlfilename"])
        book = pd.read_excel(args["path"]+r'/'+ name + r'/' + args["xlfilename"])
        
        # idx = args["sheet"]
        # column_data = book.sheets[idx].range( args["column"] + ':' + args["column"][0]+str(lastRow(idx,book)) ).value
#        plt.style.use("ggplot")
        f = make_wplt if args["plots"] == 'y' else make
        lbl,val = f(book[args["column_name"]], name,args["distribution"],bins=args["bins"],\
                       xlims=[float(args["xrange"][0]),float(args["xrange"][1])] \
                       if args["xrange"] is not None else '', colorbins=args["colorbins"])
        # lbl,val = f(column_data, name,args["distribution"],bins=args["bins"],\
        #                xlims=[float(args["xrange"][0]),float(args["xrange"][1])] \
        #                if args["xrange"] is not None else '', colorbins=args["colorbins"])
        # book.close()
        Gval.append(val)
        
    df = pd.DataFrame(Gval, columns=lbl)
    df.insert(0,'Experiment Name',folder_names)
    print(df)
    
    if toexcel == 'y':
        'write to excel'
        # wb = xw.Book()
        # sht = wb.sheets['Sheet1']
        # sht.range('A1').value = df
        # sht.range('A1').options(pd.DataFrame, expand='table').value
        df.to_excel('/home/andrew/scripts/statistics/pdsfitmore_info.xlsx', index = False)
mult()