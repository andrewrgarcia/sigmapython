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


    n0, bin_edges = np.histogram(data,bins = bins)
    
    binwidth = bin_edges[1]-bin_edges[0]
    'Area of scaled histogram'
    Ahist = np.sum(n0*binwidth)
    
    
#    n = n/np.max(n0)
    
    'plot density histogram'
#    wts = np.ones_like(data) / np.max(n0)
    wts = np.ones_like(data) /  Ahist

    
    n, bins, patches = plt.hist(data,bins = bins,stacked =True, weights=wts,\
                                color='dodgerblue',edgecolor='w',linewidth=1.2)
    
    
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
        'Normalize pdf (integral of pdf ~ 1.0)'
        max_pdf = np.max(statspdf(lspc, *pars))
        max_normbins=np.max(n)
        
        
        #    max_normbins=np.max(n0)/Ahist

        pdf = statspdf(lspc, *pars)  * (max_normbins/max_pdf)     
    
        plt.plot(lspc, pdf,color=colr,label=pltlbl) if plots is True else None
    
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
#    plt.xlabel('x-axis')
    plt.xlabel('Crystal Length  /  $\mu m$')

#    plt.title(name)
    'only for gauss'
    plt.title(r'$\bar{x}$ ='+'{} $\mu m$'.format(np.round(pars[0],2))+\
              r'    $\bar{s}$ ='+'{}    (N = {})'.format(np.round(pars[1],2),len(data))
              ) if plots is True else None
    plt.legend() if plots is True else None
    plt.show()
    return stats_lbl, stats_val


'''    EXECUTION   '''

'''MAKE YOUR OWN DATABASE
*you may use my database template XRD_database_template.py
at https://github.com/andrewrgarcia/xrd'''
def one(path='',label='',sheet='Sheet1',column='B2',bins=8,dists=['gauss','lognorm','expon','gamma','beta']):
    idx = sheet
    book=xw.Book(path)    
    column_data = book.sheets[idx].range( column + ':' + column[0]+str(lastRow(idx,book)) ).value

    make(column_data,label,dists,bins,plots=True,xlims='')
    book.close()



def multiple(sheet,column='B2',toexcel=True,plots=True):
    
    Gval = []
    samples = mysamples()

    for i in samples:
        book=xw.Book(directory+r'/'+filename[i])
        label= labl[i]
        
        idx = sheet
        column_data = book.sheets[idx].range( column + ':' + column[0]+str(lastRow(idx,book)) ).value

        
        lbl,val = make(column_data, label,['gauss','lognorm'],plots=plots)
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

'''------------------------------------------------------------------------------------'''



'''EXAMPLES'''
#ex1 = np.random.normal(10, 10, 1000)
#ex2 = 2*np.random.uniform(1,40, 1000) + np.random.normal(10, 10, 1000)
#ex3 = 3*np.random.exponential(4,1000)
##
##
#make(ex1,'example 1',['gamma','beta'],bins=20,xlims='')
#make(ex2,'example 2',['gauss'],bins=20,xlims='')
#make(ex3,'example 3',bins=20,xlims='')

'''------------------------------------------------------------------------------------'''