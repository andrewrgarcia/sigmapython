# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 19:11:35 2020

@author: garci
"""
''' 
pdsfit_more.py  - fit multiple datasets to probability distributions and tabulate all statistical data thereof to Excel
Andrew Garcia, 2020

'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
import xlwings as xw
import pandas as pd

from frame_pdsfit import *

''' ARGS LIBRARY (line 27) '''

# import the necessary packages
import argparse
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
'----------------------------------------------------------------------------------------'
'SPECIFY PATH AND FILE NAME HERE'
ap.add_argument("-p", "--path", 
                default= r'C:\[your_path]\templates-examples\pdsfit\dataset', 
                help="global path to folder containing folders with datasets")

ap.add_argument("-fn", "--xlfilename", default='Results.xls', 
                help="To simplify iteration of several fits, all Excel files from \
                different experiments (different folders) should have the same name")
'----------------------------------------------------------------------------------------'

ap.add_argument("-s", "--sheet", default='Results', 
                help="name of sheet containing dataset")
ap.add_argument("-v", "--column", default='H2', 
                help="vector/column with dataset")


ap.add_argument("-d", "--distribution", default=['gauss','lognorm','expon','gamma','beta'],
                help="distributions to fit to histogram") 

ap.add_argument("-plt", "--plots", default=True, 
                help="make plots for all data being fitted")
ap.add_argument("-b", "--bins", type=int, default=8, 
                help="# of bins to display for histogram")
ap.add_argument("-r", "--xrange", default='',
                help="range of x-axis expressed as [low,high] (e.g. [0,400])")  
ap.add_argument("-c", "--colorbins", default='dodgerblue',
                help="color of bins")  


ap.add_argument("-xl", "--toExcel", default=True, 
                help="tabulate results of all statistical fits to excel file (pandas)")

args = vars(ap.parse_args())



import os 

folders = os.listdir(args["path"])
print(folders)

def mult(toexcel=args["toExcel"]):
    
    Gval = []
    folder_names = os.listdir(args["path"])

    for name in folder_names:
        book=xw.Book(args["path"]+r'/'+ name + r'/' + args["xlfilename"])
        
        idx = args["sheet"]
        column_data = book.sheets[idx].range( args["column"] + ':' + args["column"][0]+str(lastRow(idx,book)) ).value

        plt.style.use("ggplot")
        lbl,val = make(column_data, name,args["distribution"],bins=args["bins"],plots=args["plots"],xlims=args["xrange"],colorbins=args["colorbins"])

        if args["plots"] is not True:
            plt.close()
        
        book.close()

        Gval.append(val)
        
    df = pd.DataFrame(Gval, columns=lbl)
    df.insert(0,'Experiment Name',folder_names)
    print(df)
    
    if toexcel is True:
        'write to excel'
        wb = xw.Book()
        sht = wb.sheets['Sheet1']
        sht.range('A1').value = df
        sht.range('A1').options(pd.DataFrame, expand='table').value
        
mult()