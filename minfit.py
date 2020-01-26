# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 13:04:28 2018

@author: garci
"""

'''EQUATION FITTING THROUGH MINIMIZED SUM OF RESIDUALS TECHNIQUE'
Andrew Garcia'''
import numpy as np
import scipy.optimize as optimize
import matplotlib.pyplot as plt


'''LOAD EXPERIMENTAL DATA'''
import xlwings as xw

'CHANGE TO PATH OF EXCEL FILE WITH DATA'
path = r'C:\Users\garci\Dropbox (Personal)\scripts\statistics\templates-examples\minfit_template.xlsx'
book = xw.Book(path)

sheet='Sheet1'

from frame_pdsfit import lastRow

x=book.sheets[sheet].range('A2:A'+str(lastRow(sheet,book))).value
exps=book.sheets[sheet].range('B2:B'+str(lastRow(sheet,book))).value

#print(x,exps)

def eqn(x,pars):
    
    C1,C2 = pars
    
    return C1*x**2 + C2



def E(pars):
    
    C1,C2= pars
    
    
    SUM = 0
    i=0
    while i < len(x):        
        SUM += ( eqn(x[i],pars)- exps[i] )**2 
#        SUM += (  ( eqn(x[i],pars)- exps[i] ) / exps[i]  )**2 

        i+=1
        
    return SUM

def make():
        
    initial_guess = [-1, -1]
    result = optimize.minimize(E, initial_guess)
    
    
    print('fitted coefficients \n',result.x)
    x_theory=np.linspace(min(x),max(x),100)
    
    fit = eqn(x_theory,result.x)
    
    plt.figure()
    
    plt.plot(x,exps,'o',label='data')
    plt.text(0,1,'$s$')
    plt.plot(x_theory,fit,label='fit')
    plt.legend()
    
#make()