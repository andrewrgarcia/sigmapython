# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:43:08 2018

@author: garci
"""

''' 
A PROBABILITY DENSITY FUNCTION (PDF) FITTING PROGRAM
frame_pdsfit.py - framework for pdsfit and pdsfitmore scripts
Andrew Garcia*

*adapted from Daniel Hnyk's python code:
http://danielhnyk.cz/fitting-distribution-histogram-using-python/
'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
# import xlwings as xw
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

def fit_core(data,typedist):

    if typedist == 'gauss':
        distfit,statspdf = stats.norm.fit,stats.norm.pdf
        labels,pltlbl,colr = ['normal_mean', 'normal_sdev'], 'normal','C1'
        
    elif typedist == 'lognorm':
        distfit,statspdf = stats.lognorm.fit,stats.lognorm.pdf
        labels,pltlbl,colr = ['lognorm_s/sigma', 'lognorm_loc',\
                              'lognorm_scale/median/exp_mean'], 'lognormal','C0'
        
        '''parametrization
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
        mean = np.log(scale)
        sigma = s
        median = scale '''
        
    elif typedist == 'expon':
        distfit,statspdf = stats.expon.fit,stats.expon.pdf
        labels,pltlbl,colr = ['expon_loc','expon_scale'], 'exponential','k'

    elif typedist == 'gamma':
        distfit,statspdf = stats.gamma.fit,stats.gamma.pdf
        labels,pltlbl,colr = ['gamma_a','gamma_b','gamma_c'], 'gamma','magenta'
    elif typedist == 'beta':
        distfit,statspdf = stats.beta.fit,stats.beta.pdf
        labels,pltlbl,colr = ['beta_a','beta_b','beta_c','beta_d'], 'beta','C2'
    
    
    pars = distfit(data)
    
    return distfit,statspdf,labels,pltlbl,colr,pars

def make_wplt(data,name,pds=['gauss','lognorm','expon','gamma','beta'],\
         bins= 15,xlims=[0,400],colorbins='dodgerblue'):
    
    plt.figure()

    n0, bin_edges = np.histogram(data,bins = bins)
    
    binwidth = bin_edges[1]-bin_edges[0]
    'Area of scaled histogram'
    Ahist = np.sum(n0*binwidth)
    
    
#    n = n/np.max(n0)
    
    'plot density histogram'
#    wts = np.ones_like(data) / np.max(n0)
    wts = np.ones_like(data) /  Ahist

    
    n, bins, patches = plt.hist(data,bins = bins,stacked =True, weights=wts,\
                                color=colorbins,edgecolor='w',linewidth=1.2) 
    
    
    plt.xlim(xlims) if xlims != '' else None
    
    '''find minimum and maximum of xticks, so we know
     where we should compute theoretical distribution'''
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    
    lspc = np.linspace(xmin, xmax, 1000)
    
    'to scale normalized bins with fits'
#    max_normbins = np.max(hist(data, stacked =True, weights=wts)[0])
#    max_normbins = np.max(n)

    'save stats -- labels and values'
    stats_lbl = []
    stats_val = []

    def fit(typedist):
    
        distfit,statspdf,labels,pltlbl,colr,pars = fit_core(data,typedist)
        
        'Normalize pdf (integral of pdf ~ 1.0)'
        max_pdf = np.max(statspdf(lspc, *pars))
        max_normbins=np.max(n)
        
        #    max_normbins=np.max(n0)/Ahist

        pdf = statspdf(lspc, *pars)  * (max_normbins/max_pdf)     
    
        plt.plot(lspc, pdf,color=colr,label=pltlbl)
    
        print('')
        print(name)
        
        for i in range(len(labels)):
            print(labels[i],pars[i])
        
        for i in range(len(labels)):
            stats_lbl.append(labels[i]), stats_val.append(pars[i])
        
        return pars
    

    pars=fit('gauss') if 'gauss' in pds else None
    fit('lognorm') if 'lognorm' in pds else None
    fit('expon') if 'expon' in pds else None
    fit('gamma') if 'gamma' in pds else None
    fit('beta') if 'beta' in pds else None

    
    plt.ylabel('Normalized Counts')

    'only for gauss'
    if 'gauss' in pds:
        plt.title(r'Gaussian dist. stats: $\bar{x}$ ='+'{}'.format(np.round(pars[0],2))+\
                  r'    $\bar{s}$ ='+'{}    (N = {})'.format(np.round(pars[1],2),len(data))
                  ) 
    
    plt.legend() 
    plt.show() 
    return stats_lbl, stats_val


def make(data,name,pds=['gauss','lognorm','expon','gamma','beta'],\
         bins= 15,xlims=[0,400],colorbins='dodgerblue'):
    
    'save stats -- labels and values'

    stats_lbl = []
    stats_val = []
    def fit(typedist):

        distfit,statspdf,labels,pltlbl,colr,pars = fit_core(data,typedist)
           
        print('')
        print(name)
        
        for i in range(len(labels)):
            print(labels[i],pars[i])
        
        for i in range(len(labels)):
            stats_lbl.append(labels[i]), stats_val.append(pars[i])
        
        return stats_lbl, stats_val

    pars=fit('gauss') if 'gauss' in pds else None
    fit('lognorm') if 'lognorm' in pds else None
    fit('expon') if 'expon' in pds else None
    fit('gamma') if 'gamma' in pds else None
    fit('beta') if 'beta' in pds else None
    
    return pars