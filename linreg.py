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

xk = np.random.random(25)
yk = np.random.random(25)
slope, intercept, r_value, p_value, std_err = stats.linregress(xk,yk)

x=np.arange(0,1,0.01)
y=slope*x+intercept

plt.figure()

plt.plot(x, y,color='red',label=r'regression line')
plt.plot(xk, yk,'o',color='gold',label=r'measurements')
plt.legend(loc='lower right')
#plt.xlim(0,1)
#plt.ylim(0,6)
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('title')
plt.show()

plt.text(0.05,0.80,"$R^2$= "+str(round(r_value**2,3)))
plt.text(0.05,0.75,"y = "+str(round(slope,3))+r"x + "+str(round(intercept,3)))

print ("R^2", r_value**2)
print ("p value", p_value)
print ("standard error", std_err)
print ("slope", slope)
