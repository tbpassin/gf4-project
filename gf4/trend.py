#@+leo-ver=5-thin
#@+node:tom.20211211171913.55: * @file trend.py
"""This module contains tests relating to trends in data series."""

#@+others
#@+node:tom.20211211171913.56: ** Imports and Declarations


import numpy as np
import scipy.stats

YESNO = {True:'yes', False:'no'}

#@+node:tom.20211211171913.57: ** mann_kendall (trend.py)
def mann_kendall(x, alpha = 0.05):
    """
    #@+<<docstring >>
    #@+node:tom.20220402002421.1: *3* <<docstring >>
    Perform Mann-Kendall non-parametric test for existence of a monotonic trend.
    Adapted from https://www.uni-goettingen.de/en/524376.html
    which was originally from:

    http://www.ambhas.com/codes/statlib.py

    Also see:

    http://michaelpaulschramm.com/simple-time-series-trend-analysis/
    http://www.stats.uwo.ca/faculty/mcleod/2003/DBeirness/MannKendall.pdf

    Seasonal variations should preferably be removed before the trend analysis.
    though that is not done here.

    Calculate the "S" test statistic, which is the number of data increases minus
    decreases, for every combination of two points, ordered from first to last.
    If S is positive, there appears to be an increasing trend. If negative, 
    a decreasing trend

    Then calculate the variance of S, and use it to calculate the Z-statistic,
    which is roughly normally distributed and denotes the number of standard
    deviations away from 0 that S is.  This value is used to compute the
    probability of such a deviation.  If the probability is low enough,
    the existence of a trend is asserted.

    Return the calculated S, Z, trend, and p values.

    ARGUMENTS
    x -- a sequence of 1-D numpy array of numbers.  Must be time-ordered.
    alpha -- false rejection level (probability of false rejection).

    RETURNS
    a tuple (S, z, h, p), where
    S is the trend statistic
    z -- the number of standard deviations from 0 of the "S" statistic.
    h -- boolean where True indicates a trend is present
    p -- p-value for the trend's existence.
    #@-<<docstring >>
    """

    n = len(x)

    # calculate S    
    listMa = np.matrix(x)               # convert input List to 1D matrix
    subMa = np.sign(listMa.T - listMa)  # calculate all possible differences in matrix
                                        # with itself and save only sign of difference (-1,0,1)
    s = np.sum( subMa[np.tril_indices(n,-1)] ) # sum lower left triangle of matrix

    # calculate the unique data
    # return_counts=True returns a second array that is equivalent to tp in old version    
    unique_x = np.unique(x, return_counts=True)
    g = len(unique_x[0])

    # calculate the var(s)
    if n == g: # there is no tie
        var_s = (n*(n-1)*(2*n+5))/18
    else: # there are some ties in data       
        tp = unique_x[1]
        var_s = (n*(n-1)*(2*n+5) + np.sum(tp*(tp-1)*(2*tp+5)))/18

    if s>0:
        z = (s - 1)/np.sqrt(var_s)
    elif s == 0:
        z = 0
    elif s<0:
        z = (s + 1)/np.sqrt(var_s)

    # calculate the p_value
    p = 2*(1-scipy.stats.norm.cdf(abs(z))) # two tail test
    h = abs(z) > scipy.stats.norm.ppf(1-alpha/2)

    return s, z, h, p

if __name__ == '__main__':
    dat = np.random.rand(100)
    s, z, h, p = mann_kendall(dat)
    print(f's: {s}, z: {z:.3f}, trend? {YESNO[h]}, p: {p:.3f}')
#@-others
#@@language python
#@@tabwidth -4
#@-leo
