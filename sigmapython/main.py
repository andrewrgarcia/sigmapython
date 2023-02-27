
import sigmapython.histogram as hist
import pandas

class Pop:
    def __init__(self,x=[]) -> None:
        '''
        Pop class. To hold all methods

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


from scipy import stats
import matplotlib.pyplot as plt

class Reg:
    def __init__(self,x=[],y=[]) -> None:
        '''
        Reg class. To hold all methods

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
        self.y = y


    def loadexcel(self,file):
        x,y = pandas.read_excel(file)

        self.x = x
        self.y = y

    def linear(self,plot=True):

        'FITTING'
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.x,self.y)


        'PLOTTING'
        if plot:
            # x=np.arange(0,1,0.01)
            y=slope*self.x+intercept

            plt.figure()

            plt.plot(self.x, self.y,'o',markeredgecolor='k',label=r'measurements')
            plt.plot(self.x, y,label=r'regression line')
            plt.legend(loc='lower right')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('y = {}x + {} ($R^2$ = {})'.format(round(slope,3),round(intercept,3),round(r_value**2,3)))
            plt.show()

            print('y = {}x + {}'.format(slope,intercept))
            print()
            print ("R^2", r_value**2)
            print ("p value", p_value)
            print ("standard error", std_err)
