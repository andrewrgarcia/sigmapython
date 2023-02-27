import sigmapython as sp
import numpy as np

'''pdsfit_intro.ipynb adaptation'''

ex1 = sp.Pop(np.random.normal(10, 10, 1000))
ex2 = sp.Pop(2*np.random.uniform(1,40, 1000) + np.random.normal(10, 10, 1000))
ex3 = sp.Pop(3*np.random.exponential(4,100))

bins =20 

# make(ex1,'example 1',['gamma','beta'],bins=20,xlims='')
ex1.name = 'example1'
ex1.pds = ['gamma','beta']
ex1.bins = bins
ex1.make()

# make(ex2,'example 2',['gauss'],bins=20,xlims='')
ex2.name = 'example2'
ex2.pds = ['gauss']
ex2.bins = bins
ex2.make()

# make(ex3,'example 3',bins=20,xlims='')

ex3.name = 'example3'
ex3.bins = bins
ex3.make()


'''pdsfit_excel.ipynb adaptation (simpler; pdsfit* functions discontinued)'''
import pandas

for i in range(1,6):
    
    data = sp.Pop()
    data.loadexcel('templates/pdsfit/example{}.xls'.format(i))
    data.name = 'example'+str(3+i)
    data.make()
