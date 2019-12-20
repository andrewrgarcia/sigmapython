# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 12:43:59 2019

@author: garci
"""

'''GLOBAL MINIMIZATION "BASINHOPPING" FIT
Andrew Garcia, 2019'''

import scipy.optimize as optimize
from scipy.optimize import basinhopping
import numpy as np
import matplotlib.pyplot as plt

import numpy.random as nran

from scipy.special import jv


'''LOADS EXPERIMENTAL DATA (change line 45)'''
import xlwings as xw

'''lastRow credit: answered Sep 14 '16 at 11:39  -  Stefan 
https://stackoverflow.com/questions/33418119/xlwings-function-to-find-the-last-row-with-data'''
def lastRow(idx, workbook, col=1):
    """ Find the last row in the worksheet that contains data.

    idx: Specifies the worksheet to select. Starts counting from zero.

    workbook: Specifies the workbook

    col: The column in which to look for the last cell containing data.
    """

    ws = workbook.sheets[idx]

    lwr_r_cell = ws.cells.last_cell      # lower right cell
    lwr_row = lwr_r_cell.row             # row of the lower right cell
    lwr_cell = ws.range((lwr_row, col))  # change to your specified column

    if lwr_cell.value is None:
        lwr_cell = lwr_cell.end('up')    # go up untill you hit a non-empty cell

    return lwr_cell.row

'CHANGE TO PATH OF EXCEL FILE WITH DATA'
path = r'C:\Users\garci\Dropbox (Personal)\scripts\statistics\basinhop_TEMPLATE.xlsx'
book = xw.Book(path)

sheet='Sheet1'
x1=book.sheets[sheet].range('A2:A'+str(lastRow(sheet,book))).value
x2=book.sheets[sheet].range('B2:B'+str(lastRow(sheet,book))).value
y_exps=book.sheets[sheet].range('C2:C'+str(lastRow(sheet,book))).value
print(y_exps,x1,x2)



'''EQUATION'''
def eqn(x1,x2,allpars):
    
    c1,c2,c3,c4,c5,c6,c7 = allpars
    order=0
    
    return c1*jv(order, x1**2+x2**2)  + c2*jv(order, c3*x1**2+c4*x2**2) - c5*jv(order, c6*x1**2+c7*x2**2)


'''RESIDUAL FUNCTION TO MINIMIZE i.e. OBJECTIVE FUNCTION
credit:https://github.com/andrewrgarcia/statistics/blob/master/minfit.py'''
def E(allpars):
    
    c1,c2,c3,c4,c5,c6,c7 = allpars

    
    
    SUM = 0
    i=0
    while i < len(x1):        
        SUM += ( eqn(x1[i],x2[i],allpars)- y_exps[i] )**2 
#        SUM += (  ( eqn(x[i],pars)- exps[i] ) / exps[i]  )**2 

        i+=1
        
    return SUM

def make(niter=200):

    '''INITIAL GUESSES'''
    initial_guess = 5*np.ones(7)
    
    
    '''GLOBAL MINIMIZATION'''
    minimizer_kwargs = {"method": "BFGS"}
    result = basinhopping(E, initial_guess, \
                          minimizer_kwargs=minimizer_kwargs,niter=niter)
    
    #print("global minimum: x = %.4f, f(x0) = %.4f" % (result.x, result.fun))
    
    
    print('\n global minimization results \n fitted coefficients:\n',result.x)
    
    
    
    '''PLOTTING (lines 122 -141)'''
    from mpl_toolkits import mplot3d
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    
    'Experimental'
    ax.scatter(x1, x2, y_exps,'o',color='C6',edgecolors='w')
    
    'Theory'
    'lines 94 95: 30 numbers from 0 to 10 for x and T variables'
    x1_theory = np.linspace(min(x1), max(x1), 100)
    x2_theory = np.linspace(min(x2), max(x2), 100)
    'sets up 3d mesh'
    X, Y = np.meshgrid(x1_theory, x2_theory)
    Z = eqn(X,Y,result.x)
    'makes 3d plot'
    ax.contour3D(X, Y, Z, 50, cmap='cool')
    
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')

#make(1)
make()