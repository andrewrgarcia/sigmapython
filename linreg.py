# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 19:15:40 2019

@author: garci
"""
'''linreg: a python template for linear regression data fit
Andrew Garcia'''

import numpy as np
import pylab as plt
import scipy.linalg as lin
from scipy import stats

''' ARGS LIBRARY (line 21 -) '''
import argparse
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-xl", "--fromExcel", default=False, 
                help="if -xl True, must specify -p -s -xv and -yv to import\
                xy data from Excel file. If False, x and y are randomly chosen data points")
'----------------------------------------------------------------------------------------'
'if -xl True, must specify -p -s -xv and -yv'
ap.add_argument("-p", "--path", 
                default= r'C:[your_path]\yourfile.xls', 
                help="path to dataset with file name")
ap.add_argument("-s", "--sheet", default='Sheet1', 
                help="name of sheet containing dataset")
ap.add_argument("-xv", "--xcol", default='A2', 
                help="vector/column with x dataset for linear regression")
ap.add_argument("-yv", "--ycol", default='B2', 
                help="vector/column with y dataset for linear regression")
'----------------------------------------------------------------------------------------'

args = vars(ap.parse_args())

import xlwings as xw
from frame_pdsfit import lastRow

def xlloader():
    idx = args["sheet"]
    book=xw.Book(args["path"])    
    x = book.sheets[idx].range( args["xcol"] + ':' + args["xcol"][0]+str(lastRow(idx,book)) ).value
    y = book.sheets[idx].range( args["ycol"] + ':' + args["ycol"][0]+str(lastRow(idx,book)) ).value
    book.close()
    return x,y

if args["fromExcel"] is True:
    x_expt, y_expt = xlloader()
else:
    x_expt, y_expt = np.random.random(25), np.random.random(25)

'FITTING'
slope, intercept, r_value, p_value, std_err = stats.linregress(x_expt,y_expt)


'PLOTTING'
x=np.arange(0,1,0.01)
y=slope*x+intercept

plt.figure()

plt.plot(x_expt, y_expt,'o',markeredgecolor='k',label=r'measurements')
plt.plot(x, y,label=r'regression line')
plt.legend(loc='lower right')
plt.xlabel('x')
plt.ylabel('y')
plt.title('y = {}x + {} ($R^2$ = {})'.format(round(slope,3),round(intercept,3),round(r_value**2,3)))
plt.show()

print('y = {}x + {}'.format(slope,intercept))
print()
print ("R^2", r_value**2)
print ("p value", p_value)
print ("standard error", std_err)
