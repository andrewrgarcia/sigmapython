# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:43:08 2018

@author: garci
"""

''' 
pdsfit.py - A PROBABILITY DENSITY FUNCTION (PDF) FITTING SCRIPT
Andrew Garcia*

*adapted from Daniel Hnyk's python code:
http://danielhnyk.cz/fitting-distribution-histogram-using-python/
'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
import xlwings as xw
import pandas as pd

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


def make(data,name,pds=['gauss','lognorm','expon','gamma','beta'],\
         plots=True,bins= 15,xlims=[0,400]):
        
    plt.figure() if plots is True else None

    'plot density histogram'
    wts = np.ones_like(data) / float(len(data))
    
    n, bins, patches = plt.hist(data,bins = bins,stacked =True, weights=wts,\
                                color='dodgerblue',edgecolor='k',linewidth=1.2)
    
    plt.xlim(xlims) if xlims != '' else None
    
    '''find minimum and maximum of xticks, so we know
     where we should compute theoretical distribution'''
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    
    lspc = np.linspace(xmin, xmax, 1000)
    
    'to scale normalized bins with fits'
#    max_normbins = np.max(hist(data, stacked =True, weights=wts)[0])
    max_normbins = np.max(n)

    'save stats -- labels and values'
    stats_lbl = []
    stats_val = []


    def fit(typedist):
    
        if typedist == 'gauss':
            distfit,statspdf = stats.norm.fit,stats.norm.pdf
            labels,pltlbl = ['normal_mean', 'normal_sdev'], 'normal'
            
        elif typedist == 'lognorm':
            distfit,statspdf = stats.lognorm.fit,stats.lognorm.pdf
            labels,pltlbl = ['lognorm_s/sigma', 'lognorm_loc','lognorm_scale/median/exp_mean'], 'lognormal'
            
            '''parametrization
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
            mean = np.log(scale)
            sigma = s
            median = scale '''
            
        elif typedist == 'expon':
            distfit,statspdf = stats.expon.fit,stats.expon.pdf
            labels,pltlbl = ['expon_loc','expon_scale'], 'exponential'
        
        elif typedist == 'gamma':
            distfit,statspdf = stats.gamma.fit,stats.gamma.pdf
            labels,pltlbl = ['gamma_a','gamma_b','gamma_c'], 'gamma'
        elif typedist == 'beta':
            distfit,statspdf = stats.beta.fit,stats.beta.pdf
            labels,pltlbl = ['beta_a','beta_b','beta_c','beta_d'], 'beta'
        
        
        pars = distfit(data)
        'scale "normalized" pdf to normalized bins'
        max_pdf = np.max(statspdf(lspc, *pars))
        pdf = statspdf(lspc, *pars)  * (max_normbins/max_pdf)     
    
        plt.plot(lspc, pdf,label=pltlbl) if plots is True else None
    
        print('')
        print(name)
        
        for i in range(len(labels)):
            print(labels[i],pars[i])
        
        for i in range(len(labels)):
            stats_lbl.append(labels[i]), stats_val.append(pars[i])
        
#        return labels, pars
    

    fit('gauss') if 'gauss' in pds else None
    fit('lognorm') if 'lognorm' in pds else None
    fit('expon') if 'expon' in pds else None
    fit('gamma') if 'gamma' in pds else None
    fit('beta') if 'beta' in pds else None

#    print(stats_lbl)
#    print(stats_val)

    plt.title(name) if plots is True else None
    plt.legend() if plots is True else None
    plt.show()
    return stats_lbl, stats_val


'''    EXECUTION   '''

'''MAKE YOUR OWN DATABASE
*you may use my database template XRD_database_template.py
at https://github.com/andrewrgarcia/xrd'''
from pds_database import excelbook, mysample, mysamples

def single():
    book, label = excelbook('SEM',mysample())
    idx = 'Results'
    diam =   book.sheets[idx].range( 'I2:I'+str(lastRow(idx,book)) ).value 
#    make(diam,label+' (Diameter)',['gauss','lognorm'],bins=100,plots=True,xlims='')
    make(diam,label+' (Diameter)',['lognorm'],bins=100,plots=True,xlims='')
    book.close()

#single()

def batch(toexcel=True,plots=True):
    
    Gval = []
    samples = mysamples()

    for i in samples:
        book, label = excelbook('SEM',i)
        idx = 'Results'
        diam =   book.sheets[idx].range( 'I2:I'+str(lastRow(idx,book)) ).value 
#        feret =   book.sheets[idx].range( 'D2:D'+str(lastRow(idx,book)) ).value 
#        minferet =   book.sheets[idx].range( 'H2:H'+str(lastRow(idx,book)) ).value    
        lbl,val = make(diam,label+' (Diameter)',['gauss','lognorm'],plots=plots)
        book.close()

        Gval.append(val)

        
    df = pd.DataFrame(Gval, columns=lbl)
    print(df)
    
    if toexcel is True:
        'write to excel'
        wb = xw.Book()
        sht = wb.sheets['Sheet1']
        sht.range('A1').value = df
        sht.range('A1').options(pd.DataFrame, expand='table').value

#batch(True)

'''------------------------------------------------------------------------------------'''



'''EXAMPLES'''
ex1 = np.random.normal(10, 10, 1000)
ex2 = 2*np.random.uniform(1,40, 1000) + np.random.normal(10, 10, 1000)
ex3 = 3*np.random.exponential(4,1000)


make(ex1,'example 1',['gamma','beta'],bins=20,xlims='')
make(ex2,'example 2',['gauss'],bins=20,xlims='')
make(ex3,'example 3',bins=20,xlims='')

'''------------------------------------------------------------------------------------'''