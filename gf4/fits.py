#@+leo-ver=5-thin
#@+node:tom.20211211181438.12: * @file fits.py
#@+others
#@+node:tom.20211211181438.13: ** Imports
"""Piecewise Linear and other curve fitting procedures."""



import pwlf

#@+node:tom.20211211181438.14: ** piecewiseLinear (fits.py)
def piecewiseLinear(x, y, num):
    """Return an optimum piece-wise 2-D linear fit.

    ARGUMENTS
    x -- (sorted) list or numpy array of independent variable values.
    y -- list or numpy array of dependent values corresponding
         to the x values.
    num -- number of segments to use for the fit.

    RETURNS
    a numpy 1-D array of fitted y values
    """
    
    fitter = pwlf.PiecewiseLinFit(x, y, False)
    
    fitter.fit(num)    
    yHat = fitter.predict(x)

    return yHat

if __name__ == '__main__':
    def show(a,b):
        for i, z in enumerate(a):
            print (z, b[i])

    x = [1,2,3,4,5,6]
    y = [1.1,2.05,2.85,5.07,6.92,9.3]
    show(x, y)
    print()

    yh = piecewiseLinear(x, y, 2)

    show(x, yh)
#@-others
#@@language python
#@@tabwidth -4
#@-leo
