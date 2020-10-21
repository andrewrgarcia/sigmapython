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
import pandas 


from minfit_eqn import eqn


import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--equation_editor", \
                default = '',\
                    type = str, help="equation editor: type any letter or number\
                        to open the equation editor")
                        
ap.add_argument("-s", "--simple_regression", \
                default = '',\
                    type = str, help=r"if regression has only one independent 'x' variable\
                        (e.g. y = 4x and not y =3a + 4b**2 +5c) type any letter or number \
                            here")
                        
ap.add_argument("-os", "--operating_system", \
                default = 'LIN',\
                    type = str, help="name of operating system: LIN for Linux \
                        WIN for Windows or Mac")
                        
    
ap.add_argument("-p", "--path_repository", \
                default = '/home/andrew/scripts/statistics/',\
                    type = str, help=r"type the computer path of the folder containing \
                        this python file (for windows something like this r'C:\Users\...\statistics\' )")
                        
ap.add_argument("-d", "--pathfile_data", \
                default = '/home/andrew/scripts/statistics/templates-examples/minfit_template.xlsx',\
                    type = str, help=r"type the path and filename of your Excel sheet \
                        data file  (for windows something like this \
                                    r'C:\Users\...\statistics\templates-examples\minfit_template.xlsx")
                        
ap.add_argument("-sh", "--sheet_data", \
                default = 'Sheet1',\
                    type = str, help="if not on Sheet1, type the name of the sheet \
                        with your data")
                        
args = vars(ap.parse_args())


def E(coeffs):
    
    # C1,C2,C3,C4 = coeffs
    C1,C2 = coeffs
    
    if args['simple_regression'] != '':
        SUM=0
        for i in range(len(varls.T)):
            SUM += ( eqn(varls.T[i],coeffs)- y_obs[i] )**2 
            # SUM += (  ( eqn(varls.T[i],coeffs)- y_obs[i] ) / y_obs[i]  )**2 
            
    else:
        SUM = np.sum(( eqn(varls,coeffs) - y_obs )**2)

    return SUM

def make():
    
    #initial_guess = [-1, -1, -1, -1]    
    initial_guess = [-1, -1]
    result = optimize.minimize(E, initial_guess)
    
    # print(len(varls_packed.columns))
    vpc= varls_packed.columns
    print('fitted coefficients')
    
    [print('C_{} : {}'.format(i+1, result.x[i])) \
     for i in range(len(result.x))]
    print('\nSOLVER information')
    print(result)
    
    # fit = eqn(varls_theory,result.x)
    
    plt.figure()
    for i in range(len(varls)):
        plt.plot(varls[i],y_obs,'o',label='y_obs=y_obs({})'.format(vpc[i]))
        # plt.text(0,1,'$s$')
        # plt.plot(varlsa,fit,label='fit')
        plt.legend()



# if True == True:
if args['equation_editor'] != '':
    pathrep = args['path_repository']
    if args['operating_system'] == 'LIN':

        '''Linux'''
        'Write the equation'
        import subprocess, sys
        filename  = pathrep+'minfit_eqn.py'
        filename2 = pathrep+'minfit.py'
        opener ="open" if sys.platform == "darwin" else "xdg-open"

        called2 = subprocess.call([opener, filename2])
        called = subprocess.call([opener, filename])

    if args['operating_system'] == 'WIN':
        '''Windows'''
        'Write the equation'
        import os
        os.startfile(pathrep+'minfit.py')
        os.startfile(pathrep+'minfit_eqn.py')



else: 
    
    'load data to fit'
    #'Windows
    # file = r'C:\Users\...\statistics\templates-examples\minfit_template.xlsx'
    #'Linux
    file = args['pathfile_data']
    
    xls = pandas.ExcelFile(file)
    sht = pandas.read_excel(xls, args['sheet_data'])
    
    varls=sht[sht.columns[0]]
    y_obs = sht[sht.columns[-1]]
    print(y_obs)
    
    # table = sht[sht.columns[0:-1][0]]
    varls_packed = sht.loc[:, sht.columns != 'y']
    
    varls = varls_packed.T.values
    
    # print((eqn(varls,(1,1))-y_obs)**2)
    
    make()
