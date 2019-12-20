# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:42:46 2019

@author: garci
"""
from pdsfit import *
from pds_database import excelbook, mysample, mysamples


#plt.xlabel('Crystal Length  /  $\mu m$')


def single(path='',bins=30,method='SEM',dists=['gauss','lognorm','expon','gamma','beta']):
    book, label = excelbook(method,mysample()) if path == '' else excelbook(method,path)

    idx = 'Results'
    
    def colvals(colstr):    
        return book.sheets[idx].range( colstr+'2:'+colstr+str(lastRow(idx,book)) ).value
    
    coltitl = book.sheets[idx].range('I1').value
    diam = colvals('I') if coltitl != None else 2*np.sqrt(np.array(colvals('C'))/np.pi)

    make(diam,label+' (Diameter)',dists,bins=bins,plots=True,xlims='')
    book.close()

single(method='SEM',dists=['gauss'])

def batch(toexcel=True,plots=True):
    
    Gval = []
    samples = mysamples()

    for i in samples:
        book, label = excelbook('SEM',i)
        idx = 'Results'
        colval = book.sheets[idx].range( 'I2:I'+str(lastRow(idx,book)) ).value
        coltitl = book.sheets[idx].range('I1').value
        diam = colval if coltitl != '' \
        else 2*np.sqrt(colval/np.pi)

        
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