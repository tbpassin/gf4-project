#@+leo-ver=5-thin
#@+node:tom.20211211170819.30: * @file curve_generators.py
# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211170819.31: ** Imports
from __future__ import print_function

import math
import numpy as np
from scipy.stats import norm

#@+node:tom.20211211170819.32: ** generateSine
def generateSine(n=256, cycles=5):
    '''Compute a sine wave with evenly spaced abscissa points.  
    Return a tuple of two arrays (xdata, ydata).

    ARGUMENTS
    n -- number of points to return
    cycles -- number of cycles across the n points

    RETURNS
    a tuple (xdata, ydata)
    '''

    delta = (2.0*cycles*math.pi)/(n-1)
    _x = []
    _y = []

    for i in range(n):
        _x.append(i)
        _y.append(math.sin(i*delta))

    return (_x, _y)

#@+node:tom.20211211170819.33: ** generateSquarewave
def generateSquarewave(n=256, cycles=5):
    '''Compute a square wave with evenly spaced abscissa points. 
    The waveform has an amplitude of 1, and is centered on 0.
    Return a tuple of two arrays (xdata, ydata).

    ARGUMENTS
    n -- number of points to return
    cycles -- number of cycles to return

    RETURNS
    a tuple (xdata, ydata)
    '''

    upper = 0.5
    lower = -0.5
    halfcycle = 0.5*n/cycles

    _x = []
    _y = []

    c = 0
    for i in range(n):
        _x.append(i)
        if c < halfcycle:
            y = upper
        else:
            y = lower
        _y.append(y)

        c += 1
        if c >= 2 * halfcycle:
            c = 0

    return (_x, _y)

#@+node:tom.20211211170819.34: ** generateDampedSine
def generateDampedSine(N=256, cycles = 5, decay=3.0):
    '''Compute a damped sine wave with evenly spaced abscissa points.  
    Return a tuple of two arrays (xdata, ydata).

    ARGUMENTS
    N -- number of points to return.
    cycles -- number of complete cycles.
    decay -- number of decay time constants across the entire curve

    RETURNS
    a tuple (xdata, ydata)
    '''

    _x, _y = generateSine(N, cycles)
    _expon = -decay /(N-1)

    _yd = [_y[n] * math.exp(_expon * n) for n in range(N)]
    
    return (_x, _yd)

#@+node:tom.20211211170819.35: ** generateExponential
def generateExponential(N=256, decay=3.0):
    '''Compute an exponential curve with evenly spaced abscissa points. 
    A positive decay parameter specifies decay, negative specifies 
    increase. Return a tuple of two arrays (xdata, ydata).

    ARGUMENTS
    N -- number of points to return.
    decay -- number of decay time constants across the entire curve

    RETURNS
    a tuple (xdata, ydata)
    '''

    _expon = -decay /(N-1)
    _x = []
    _y = []

    for i in range(N):
        _x.append(i)
        _y.append(math.exp(_expon * i))

    return (_x, _y)


#@+node:tom.20211211170819.36: ** generateRectangle
def generateRectangle(N=256):
    '''Compute a rectangular waveform with evenly spaced points.
    Return a tuple of two arrays (xdata, ydata).

    ARGUMENT
    N -- number of points to return.

    RETURNS
    a tuple (xdata, ydata)
    '''

    _x = list(range(N))
    _y = [1.0 for i in range(N)]
    _y[0] = 0

    return (_x, _y)

#@+node:tom.20211211170819.38: ** generateGaussian
def generateGaussian(N=256, m=0.0, sigma=128): 
    '''Compute a Gaussian probability curve.  Return a tuple of two arrays
    (xdata, ydata).

    ARGUMENTS
    N -- number of points.  If not odd, the curve won't be exactly symmetrical
         around the mean.
    m -- mean of the distribution.
    sigma -- the standard deviation value of the distribution.

    RETURNS
    a tuple of lists (xdata, ydata)
    '''

    _half = N / 2
    lower = -_half + m
    upper = _half + m
    if N % 2 == 1:
        upper += 1

    _range = np.arange(lower, upper, 1)
    #_sig = _half / sigma
    _gauss = norm.pdf(_range, m, sigma)

    _ydata = _gauss.tolist()
    _xdata =_range.tolist()

    return _xdata,_ydata

#@+node:tom.20211211170819.39: ** generateGaussianCdf
def generateGaussianCdf(N=256, m=0.0, sigma=128): 
    '''Compute a Gaussian probability curve.  Return a tuple of two arrays
    (xdata, ydata).

    ARGUMENTS
    N -- number of points.  If not odd, the curve won't be exactly symmetrical
         around the mean.
    m -- mean of the distribution.
    sigma -- the standard deviation value of the distribution.

    RETURNS
    a tuple of lists (xdata, ydata)
    '''

    _half = N / 2
    lower = -_half + m
    upper = _half + m
    if N % 2 == 1:
        upper += 1

    _range = np.arange(lower, upper, 1)
    #_sig = _half / sigma
    _gauss = norm.cdf(_range, m, sigma)

    _ydata = _gauss.tolist()
    _xdata =_range.tolist()

    return _xdata,_ydata

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    def testGauss():
        N = 101
        m = 0.0
        sigma = 20.0
        x,y = generateGaussian(N, m, sigma)
        print ('data length:', len(x))
        plt.plot(x, y, 'g')
        plt.title('Gaussian Showing Mean, Sigma = %s, %s' % (m, sigma))
        plt.show()

    def testGaussCdf():
        N = 101
        m = 0.0
        sigma = 20.0
        x, y = generateGaussianCdf(N, m, sigma)
        print ('data length:', len(x))
        plt.plot(x, y, 'g')
        plt.title('Gaussian CDF Showing Mean, Sigma = %s, %s' % (m, sigma))
        plt.show()

    def runtests(testlist):
        for t in testlist:
            print ('Testing %s' % t.func_name)
            t()
            print()

    Tests = (testGaussCdf,)
    runtests(Tests)
    

#@+node:tom.20211211170819.37: ** generateRamp
def generateRamp(N=256):
    '''Compute a linear ramp with evenly spaced points. Maximum
    amplitude is 1.0. Return a tuple of two arrays (xdata, ydata).

    ARGUMENT
    N -- number of points to return.

    RETURNS
    a tuple (xdata, ydata)
    '''

    _ydelta = 1.0 / (N - 1)
    _y0 = 0.0
    _x = list(range(N))
    _y = [_y0 + _ydelta * i for i in range(N)]

    return (_x, _y)
#@-others
#@@language python
#@@tabwidth -4
#@-leo
