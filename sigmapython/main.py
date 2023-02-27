
import sigmapython.histogram as hist
import pandas

class Dev:
    def __init__(self,x=[]) -> None:
        '''
        Dev class. To hold all methods

        Parameters
        ----------
        1. data - this is the input which holds a vector of all your histogram data
        2. name - any name you would want to give to your specific data
        3. pds - this is an input vector which specifies which distribution types you want to fir to your data; it is defaulted to all the distribution types I have declared in the script, which are:
            a. gauss - Gaussian / normal distribution
            b. lognorm - Lognormal distribution
            c. expon - Exponential distribution
            d. gamma - Gamma distribution
            e. beta - beta distribution
        4. plots - Boolean to plot (or not)
        5. bins - number of bins your histogram holds
        6. xlims - x-axis limits to plot. If xlims = '' computer makes best decision of x-limits

        '''
        self.x = x
        self.name = 'data'
        self.pds = ['gauss','lognorm','expon','gamma','beta']
        self.plots = True
        self.bins = 15
        self.xlims = '' # =[0,400]

        
    def make(self,colorbins='dodgerblue',alpha=0.5,den_norm=True):
        
        if self.plots:
            hist.make_wplt(self.x,self.name,self.pds,self.bins,self.xlims,colorbins,alpha,den_norm)
        else:
            hist.make(self.x,self.name,self.pds,self.bins,self.xlims,colorbins)


    def loadexcel(self,file):
        data = pandas.read_excel(file)
        if len(data.columns) > 1:
            x = data[data.columns[1]]
        else:
            x = data[data.columns[0]]

        self.x = x

