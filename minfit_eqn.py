#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 13:33:38 2020

@author: andrew
"""
import numpy as np

def eqn(varls,coeffs):
    
    # x, x2, x3, x4 = varls
    # C1,C2,C3,C4 = coeffs
    #return C1*x**2 + C2*x2 + C3*(43-x3) +C4*np.sin(x4)
    
    # x=varls
    # C1,C2 = coeffs
    # return C1*x**2 + C2
    
    # x,x2=varls
    # C1,C2 = coeffs
    # return C1*x**2 + C2*x2 
    
    x=varls
    C1,C2 = coeffs
    return C1*x + C2


    
'if number of coeffs is not 2, change: lines 75 and 91 in minfit.py'

