# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:43:08 2018

@author: garci
"""

''' 
pdsfit.py - A PROBABILITY DENSITY (PD) FITTING SCRIPT
Andrew Garcia*

*adapted from Daniel Hnyk's python code:
http://danielhnyk.cz/fitting-distribution-histogram-using-python/
'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt
import xlwings as xw

'''make your own database (for help on building a database, 
see database template on my XRD repository)'''
from dist_database import excelbook
book, label = excelbook()

end = 60
#end = 77
#end = 301

diam =   book.sheets['Results'].range( 'I2:I'+str(end) ).value 
feret =   book.sheets['Results'].range( 'D2:D'+str(end) ).value 
minferet =   book.sheets['Results'].range( 'H2:H'+str(end) ).value 


'''some random noisy data (examples)'''
#ex1 = np.random.normal(10, 10, 1000)
#ex2 = 2*np.random.uniform(1,40, 1000) + np.random.normal(10, 10, 1000)
#ex3 = 3*np.random.exponential(4,1000)


def make(data,name,pds=['gauss','lognorm','expon','gamma','beta']):
        
    plt.figure()

    'plot density histogram'
    wts = np.ones_like(data) / float(len(data))
    
    plt.hist(data, stacked =True, weights=wts,color='navy')

    '''find minimum and maximum of xticks, so we know
     where we should compute theoretical distribution'''
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    
#    N_lspc = len(data)
    N_lspc = 1000

    lspc = np.linspace(xmin, xmax, N_lspc)
    
    'to scale normalized bins with fits'
    max_normbins = np.max (hist(data, stacked =True, weights=wts)[0])

    
    '''*NORMAL DISTRIBUTION (GAUSSIAN)'''
    if 'gauss' in pds:
        m, s = stats.norm.fit(data) # get mean and standard deviation  
        
        'scale "normalized" pdf to normalized bins'
        max_pdf = np.max(stats.norm.pdf(lspc, m, s))
        pdf_g = stats.norm.pdf(lspc, m, s)  * (max_normbins/max_pdf)     
    #    plt.plot(lspc, pdf_g,label="Normal " + name) # plot it
    
        plt.plot(lspc, pdf_g,color='k',label='normal') 
    
    #    print(name, 'distribution fit statistics')
        print('')
        print(name)
    
    
        print('sample size = ',size(data))
        print('normal: ' ,'mean', np.round(m,2),'std_dev', np.round(s,2))
    
    '''*LOGNORMAL DISTRIBUTION'''
    if 'lognorm' in pds:

        s, loc, scale = stats.lognorm.fit(data) # get mean and standard deviation 
        '''parametrization'
    #    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html
    #    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.lognorm.html'''
        mu = np.log(scale)
        sigma = s
        
        mean = np.exp(mu + 0.5*sigma**2)
        median = np.exp(mu)
        mode = np.exp(mu -sigma**2)
#        variance = (np.exp(sigma**2) - 1) *np.exp(2*mean +sigma**2)
        
        'scale normalized pd to bins'
        max_pdf = np.max(stats.lognorm.pdf(lspc, s,loc,scale))
        pdf_logn = stats.lognorm.pdf(lspc, s,loc,scale) * (max_normbins/max_pdf)
        
        plt.plot(lspc, pdf_logn,color='lime',label="lognormal") # plot it
        
        plt.xlabel('Length  /  $\mu m$')
        print('\n lognormal: \n s {} loc {} scale {} \
              \n mean = {} \n median = {} \n mode = {} \
              \n '.format(np.round(s,2),np.round(loc,2), np.round(scale,2),mean,median,mode))

    '''*EXPONENTIAL DISTRIBUTION'''
    if 'expon' in pds:
        loc, scale = stats.expon.fit(data)
        pdf_expon = stats.expon.pdf(lspc, loc, scale)  
        'scale normalized pd to bins'
        max_pdf = np.max(stats.expon.pdf(lspc, loc,scale))
        pdf_expon = stats.expon.pdf(lspc, loc,scale)  * (max_normbins/max_pdf)   
        
        plt.plot(lspc, pdf_expon,label="expon")
        print('\n exponential: \n loc {} scale {} \
              \n '.format(loc,scale))
        
        
        
    '''*GAMMA DISTRIBUTION'''
    if 'gamma' in pds:

        ag,bg,cg = stats.gamma.fit(data)  
        pdf_gamma = stats.gamma.pdf(lspc, ag, bg,cg)  
        'scale normalized pd to bins'
        max_pdf = np.max(stats.gamma.pdf(lspc, ag,bg,cg))
        pdf_gamma = stats.gamma.pdf(lspc, ag,bg,cg)  * (max_normbins/max_pdf)   
        
        plt.plot(lspc, pdf_gamma,label="gamma")
        print('Gamma: ' ,'aG', np.round(ag,2),'bG', np.round(bg,2),\
              'cG', np.round(cg,2))

    
    '''*BETA DISTRIBUTION'''
    if 'beta' in pds:

        ab,bb,cb,db = stats.beta.fit(data)  
        pdf_beta = stats.beta.pdf(lspc, ab, bb,cb, db)  
    #    plt.plot(lspc, pdf_beta, label="Beta " + name)
        'scale normalized pd to bins'
        max_pdf = np.max(stats.beta.pdf(lspc, ab,bb,cb,db))
        pdf_beta = stats.beta.pdf(lspc, ab,bb,cb,db)  * (max_normbins/max_pdf)   
        
        plt.plot(lspc, pdf_beta,label="beta")
        print('Beta: ' ,'aB', np.round(ab,2),'bB', np.round(bb,2),\
              'cB', np.round(cb,2),'dB', np.round(db,2))
        print()

    plt.title(name)
    plt.legend()
    
    plt.show()  
    
    
#make(feret,label+' (Feret Long)')
#make(minferet,label+' (Feret Short)')
make(diam,label+' (Diameter)')

book.close()



#make(ex1,'example 1')
#make(ex2,'example 2')
#make(ex3,'example 3')


