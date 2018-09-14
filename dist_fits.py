# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 17:43:08 2018

@author: garci
"""

''' 
A probability distribution fitting script

adapted from Daniel Hnyk's python code:
http://danielhnyk.cz/fitting-distribution-histogram-using-python/
'''

from scipy import stats  
import numpy as np  
import matplotlib.pylab as plt

'''import your own database (for help on building a database, 
see database template on my XRD repository)'''
from dist_database import library, labels

'''OR
# create some normal random noisy data'''
#ser = np.random.normal(10, 10, 100)
#ser2 = 2*np.random.uniform(1,40, 100) + np.random.normal(10, 10, 100)

def do(ser,name):
    
    # plot normed histogram
    plt.hist(ser, normed=True, label=name)

    # find minimum and maximum of xticks, so we know
    # where we should compute theoretical distribution
    xt = plt.xticks()[0]  
    xmin, xmax = min(xt), max(xt)  
    lnspc = np.linspace(xmin, xmax, len(ser))
    
    '# lets try the normal distribution first'
    m, s = stats.norm.fit(ser) # get mean and standard deviation  
    pdf_g = stats.norm.pdf(lnspc, m, s) # now get theoretical values in our interval  
#    plt.plot(lnspc, pdf_g,label="Normal " + name) # plot it
    plt.plot(lnspc, pdf_g) 

    print(name, 'distribution statistics')
    print('sample size = ',size(ser))
    print('normal: ' ,'mean', np.round(m,2),'std_dev', np.round(s,2))
    #
    
    'lognormal dist.'
    s, loc, scale = stats.lognorm.fit(ser) # get mean and standard deviation  
    pdf_logn = stats.lognorm.pdf(lnspc, s,loc,scale) # now get theoretical values in our interval  
#    plt.plot(lnspc, pdf_logn,label="Lognorm " + name) # plot it
    plt.plot(lnspc, pdf_logn) # plot it
    
    print('lognormal: ' ,'s', np.round(s,2),'loc', np.round(loc,2),\
          'scale', np.round(scale,2))
    

    'gamma'
    ag,bg,cg = stats.gamma.fit(ser)  
    pdf_gamma = stats.gamma.pdf(lnspc, ag, bg,cg)  
#    plt.plot(lnspc, pdf_gamma, label="Gamma " + name )
    plt.plot(lnspc, pdf_gamma )
    print('Gamma: ' ,'aG', np.round(ag,2),'bG', np.round(bg,2),\
          'cG', np.round(cg,2))

    
    'beta'
    ab,bb,cb,db = stats.beta.fit(ser)  
    pdf_beta = stats.beta.pdf(lnspc, ab, bb,cb, db)  
#    plt.plot(lnspc, pdf_beta, label="Beta " + name)
    plt.plot(lnspc, pdf_beta)
    print('Beta: ' ,'aB', np.round(ab,2),'bB', np.round(bb,2),\
          'cB', np.round(cb,2),'dB', np.round(db,2))
    print()


    plt.legend()
    
    plt.show()  
    

#do(ser,'example')
#do(ser2,'example 2')


'database: performs function for all entries on database:'
for i in range(size(library())):
    do(library()[i],labels()[i])
    
'database: performs function for selected entries on database:'
#do(library()[0],labels()[0])
#do(library()[1],labels()[1])

