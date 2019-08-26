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


def make(data,name,pds=['gauss','lognorm','expon','gamma','beta'],plots=True,bins= 40,xlims=[0,400]):
        
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
    stats_lbl.append('sample_name')
    stats_val.append(name)
    stats_lbl.append('sample_size')
    stats_val.append(size(data))

    
    '''*NORMAL DISTRIBUTION (GAUSSIAN)'''
    if 'gauss' in pds:
        m, s = stats.norm.fit(data) # get mean and standard deviation  
        
        'scale "normalized" pdf to normalized bins'
        max_pdf = np.max(stats.norm.pdf(lspc, m, s))
        pdf_g = stats.norm.pdf(lspc, m, s)  * (max_normbins/max_pdf)     
    #    plt.plot(lspc, pdf_g,label="Normal " + name) # plot it
    
        plt.plot(lspc, pdf_g,color='purple',label='normal') if plots is True else None
    
    #    print(name, 'distribution fit statistics')
        print('')
        print(name)
    
    
        print('sample_size \n {}'.format(size(data)))
        print('\n normal: \n \
              mean sdev \n \
              {} {}'.format(np.round(m,2),np.round(s,2)))
        
        stats_lbl.append('normal_mean'), stats_val.append(m)
        stats_lbl.append('normal_sdev'), stats_val.append(s)


#        print('normal: ' ,'mean', np.round(m,2),'std_dev', np.round(s,2))
    
    '''*LOGNORMAL DISTRIBUTION'''
    if 'lognorm' in pds:

        s, loc, scale = stats.lognorm.fit(data) # get mean and standard deviation 
        '''parametrization'
    #    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
    #    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html'''
        mean = np.log(scale)
        sigma = s
#        mean, var, skew, kurt = stats.lognorm.stats(s, moments='mvsk')
        
        median = scale
        
        'scale normalized pd to bins'
        max_pdf = np.max(stats.lognorm.pdf(lspc, s,loc,scale))
        pdf_logn = stats.lognorm.pdf(lspc, s,loc,scale) * (max_normbins/max_pdf)
        
        plt.plot(lspc, pdf_logn,color='gold',label="lognormal") if plots is True else None
        
        plt.xlabel('Length  /  $\mu m$')
        
        print('\n lognormal: \n \
              s loc scale mean median \n \
              {} {} {} {} {} \n'.format(np.round(s,2),np.round(loc,2), np.round(scale,2),mean,median))

        stats_lbl.append('lognorm_s'), stats_val.append(s)
        stats_lbl.append('lognorm_loc'), stats_val.append(loc)
        stats_lbl.append('lognorm_scale'), stats_val.append(scale)
        stats_lbl.append('lognorm_mean'), stats_val.append(mean)
        stats_lbl.append('lognorm_median'), stats_val.append(median)

#        print('\n lognormal: \n s {} loc {} scale {} \
#              \n mean = {} \n median = {} \n mode = {} \
#              \n '.format(np.round(s,2),np.round(loc,2), np.round(scale,2),mean,median,mode))

    '''*EXPONENTIAL DISTRIBUTION'''
    if 'expon' in pds:
        loc, scale = stats.expon.fit(data)
        pdf_expon = stats.expon.pdf(lspc, loc, scale)  
        'scale normalized pd to bins'
        max_pdf = np.max(stats.expon.pdf(lspc, loc,scale))
        pdf_expon = stats.expon.pdf(lspc, loc,scale)  * (max_normbins/max_pdf)   
        
        plt.plot(lspc, pdf_expon,color='crimson',label="expon") if plots is True else None
        print('\n exponential: \n loc {} scale {} \
              \n '.format(loc,scale))
        
        stats_lbl.append('expon_loc'), stats_val.append(loc)
        stats_lbl.append('expon_scale'), stats_val.append(scale)
        
        
    '''*GAMMA DISTRIBUTION'''
    if 'gamma' in pds:

        ag,bg,cg = stats.gamma.fit(data)  
        pdf_gamma = stats.gamma.pdf(lspc, ag, bg,cg)  
        'scale normalized pd to bins'
        max_pdf = np.max(stats.gamma.pdf(lspc, ag,bg,cg))
        pdf_gamma = stats.gamma.pdf(lspc, ag,bg,cg)  * (max_normbins/max_pdf)   
        
        plt.plot(lspc, pdf_gamma,label="gamma") if plots is True else None
        print('Gamma: ' ,'aG', np.round(ag,2),'bG', np.round(bg,2),\
              'cG', np.round(cg,2))
        
        stats_lbl.append('gamma_a'), stats_val.append(ag)
        stats_lbl.append('gamma_b'), stats_val.append(bg)
        stats_lbl.append('gamma_c'), stats_val.append(cg)

    
    '''*BETA DISTRIBUTION'''
    if 'beta' in pds:

        ab,bb,cb,db = stats.beta.fit(data)  
        pdf_beta = stats.beta.pdf(lspc, ab, bb,cb, db)  
    #    plt.plot(lspc, pdf_beta, label="Beta " + name)
        'scale normalized pd to bins'
        max_pdf = np.max(stats.beta.pdf(lspc, ab,bb,cb,db))
        pdf_beta = stats.beta.pdf(lspc, ab,bb,cb,db)  * (max_normbins/max_pdf)   
        
        plt.plot(lspc, pdf_beta,label="beta") if plots is True else None
        print('Beta: ' ,'aB', np.round(ab,2),'bB', np.round(bb,2),\
              'cB', np.round(cb,2),'dB', np.round(db,2))
        print()
        
        stats_lbl.append('beta_a'), stats_val.append(ab)
        stats_lbl.append('beta_b'), stats_val.append(bb)
        stats_lbl.append('beta_c'), stats_val.append(cb)
        stats_lbl.append('beta_d'), stats_val.append(db)


    plt.title(name) if plots is True else None
    plt.legend() if plots is True else None
    
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
    make(diam,label+' (Diameter)',['gauss','lognorm'],bins=300,plots=True,xlims='')
    book.close()

single()

def batch(toexcel=True):
    
    Gval = []
    samples = mysamples()

    for i in samples:
        book, label = excelbook('SEM',i)
        idx = 'Results'
        diam =   book.sheets[idx].range( 'I2:I'+str(lastRow(idx,book)) ).value 
#        feret =   book.sheets[idx].range( 'D2:D'+str(lastRow(idx,book)) ).value 
#        minferet =   book.sheets[idx].range( 'H2:H'+str(lastRow(idx,book)) ).value    
        lbl,val = make(diam,label+' (Diameter)',['gauss','lognorm'],plots=True,xlims='')
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

#batch()

'''------------------------------------------------------------------------------------'''



'''EXAMPLES'''
#ex1 = np.random.normal(10, 10, 1000)
#ex2 = 2*np.random.uniform(1,40, 1000) + np.random.normal(10, 10, 1000)
#ex3 = 3*np.random.exponential(4,1000)

#
#make(ex1,'example 1',['gamma','beta'],20)
#make(ex2,'example 2',['gauss'],20)
#make(ex3,'example 3',bins=20)

'''------------------------------------------------------------------------------------'''



