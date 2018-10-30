# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 13:04:28 2018

@author: garci
"""

'''EQUATION FITTING THROUGH MINIMIZED SUM OF RESIDUALS TECHNIQUE'
Andrew Garcia'''

import scipy.optimize as optimize
import matplotlib.pyplot as plt

def eqn(x,pars):
    
    C1,C2 = pars
    
    return C1*x**2 + C2


exps=[162,120,100,70,80,30,50,20,60,90,130,170]


x=linspace(-50,50,len(exps))

def E(pars):
    
    C1,C2= pars
    
    
    SUM = 0
    i=0
    while i < len(x):        
        SUM += ( eqn(x[i],pars)- exps[i] )**2 
#        SUM += (  ( eqn(x[i],pars)- exps[i] ) / exps[i]  )**2 

        i+=1
        
    return SUM
        
        
initial_guess = [-1, -1]
result = optimize.minimize(E, initial_guess)


print(result.x)

fit = eqn(x,result.x)

plt.figure()

plt.plot(x,exps,'o',label='data')
plt.text(0,1,'$s$')
plt.plot(x,fit,label='fit')
plt.legend()
