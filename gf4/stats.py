#@+leo-ver=5-thin
#@+node:tom.20211211171913.40: * @file stats.py
#@@language python
#@@tabwidth -4
"""Compute various statistical measures for 2D data."""
#@+others
#@+node:tom.20211211171913.41: ** Imports
from __future__ import print_function

import math
import scipy.special
from scipy.stats import norm, t as t_test
from scipy.stats import spearmanr
import numpy as np

from curve_generators import generateGaussianCdf
# from smoother import correlationCoeff

#@+node:tom.20211211171913.42: ** cdf
def cdf(ydata):
    '''Compute Cumulative Distribution Function.  CDF is
    P(X <= x), where X is a value of the random variable, and x
    is some chosen value. See e.g., Wikipedia at

    http://en.wikipedia.org/wiki/Cumulative_distribution_function#Definition

    The estimated variance of each point is P * (1-P)/N, where P is the
    CDF probability (see http://en.wikipedia.org/wiki/Empirical_distribution_function),
    and N is the number of data points.

    Return val, p, upperbound, lowerbound, where val are the input values,
    p are the calculated CDF probabilities, and upper/lowerbound are the
    estimated p +/- 1 standard deviations.
    point.

    ARGUMENT
    ydata -- a sequence of random values

    RETURNS
    A tuple of sequences (x, y, upperbound, lowerbound). x is a list of the ydata values.
    y is a list of the CDF values.  Upper/lowerbound are sequences of
    y +/-std. dev.
    '''

    _y = ydata[:]

    # To prevent ties between exactly equal values, increment adds a tiny
    # amount so none are exactly equal.  This may be a hack, but it
    # doesn't adversely affect the results and makes a number of
    # calculations much easier.
    dupes = {}
    temp = []
    for _val in _y:
        count = dupes.get(_val, 0) + 1
        dupes[_val] = count
        v = _val
        if count > 1:
            v = v * (1.0 + count * 0.00001)
        temp.append(v)

    _y = temp
    _y.sort()

    # Cumulative probabilities
    x = []
    y = []
    upperbound = []
    lowerbound = []
    N = len(ydata)
    delta = 1.0 / (N + 1)
    prob = 0.0
    for val in _y:
        prob += delta
        sigma = (prob * (1 - prob) / N) ** 0.5
        x.append(val)
        y.append(prob)
        upperbound.append(prob + sigma)
        lowerbound.append(prob - sigma)

    return (x, y, upperbound, lowerbound)

#@+node:tom.20211211171913.43: ** histogram
def histogram(data, nbins=10):
    '''Given a list of data points, compute the histogram.  The histogram's area
    sums to one, so that it is a probability distribution.  A data point
    will go into a bin when lower <= y < upper.  A bin is added to either end,
    so that the first bin will have zero counts and the last bin will contain
    the count of points with the highest value.  Thus, therre will be two
    more bins than requested.  The histogram is normalized to have an area of 1,
    so that its integral will be a CDF curve.

    ARGUMENTS
    data -- an array of data points.
    nbins -- the number of bins to put the values into.

    RETURNS
    a tuple of lists (x, y).  The format is

     pt p: 0   1  2   3   4   5   6            n
    x = [ 0, d, d,  2d,  2d,  3d,  3d,  4d,  ..., dxn-1, dxn]
    y = [y0, y0, y1, y1, y2, y2, ..., yn/2-1, yn/2-1]

    where d = bin width
    '''

    data.sort()
    ymax = 1.0 * data[-1]
    ymin = 1.0 * data[0]

    binwidth = (ymax - ymin) / nbins
    nbins = nbins + 2
    nmax = len(data)

    ny = 0  # index of y (data) array
    lower = ymin
    upper = ymin + binwidth

    binned = [(lower - binwidth, 0)]
    done = False
    count = 0

    while not done:
        if data[ny] < upper:
            count += 1
            ny += 1
            if ny == nmax:
                binned.append((lower, count))
                done = True
        else:
            binned.append((lower, count))
            count = 0
            upper += binwidth
            lower += binwidth
        if ny == nmax:
            done = True

    sum = 0
    for lower, cnt in binned:
        sum += cnt
    _norm = 1.0 / (sum * binwidth)
    _x = []
    _y = []

    for lower, count in (binned):
        # lower, count = binned[n]
        _x.append(lower)
        _x.append(lower + binwidth)
        _ynorm = 1.0 * count * _norm
        _y.append(_ynorm)
        _y.append(_ynorm)

    lower += binwidth
    _x.append(lower)
    _x.append(lower + binwidth)
    _y.append(0)
    _y.append(0)

    return _x, _y

#@+node:tom.20211211171913.44: ** meanstd
def meanstd(ydata):
    '''Return the sample mean, standard deviation s and corrected std dev..

    The corrected std ev is corrected for lag-1 autocorrelation.

    ARGUMENT
    ydata -- a sequence of random values

    RETURNS
    a tuple (mean, stddev, stddev_corrected), or None if there are 
    less than three points in the data
    '''

    N = len(ydata)
    if N < 3: return None

    mean = 1.0 * sum(ydata) / N
    sumsqr = sum([a ** 2 for a in ydata])
    std = math.sqrt((sumsqr - N * mean ** 2) / (N - 1))

    # Lag-1 autocorrelation
    shifted = ydata[1:]
    r = pearson(shifted, ydata[:-1])

    # Correct sigma for lag-1 autocorrelation
    try:
        std_ac = std / (1. - r * r) ** 0.5
    except Exception as e:
        print(e)
        std_ac = float('NaN')


    return (mean, std, std_ac)

#@+node:tom.20211211171913.45: ** fitNormalToCdf
def fitNormalToCdf(dataset):
    '''Given a sequence of x, y values, compute a normal CDF.

    The CDF will be the CDF of a normal distribution with mean,
    standard deviation to match the data values.  The result
    will have the same number of points as the input data.

    Return a tuple of lists (xdata, ydata, mean, stddev).

    ARGUMENTS
    values -- a sequence of the CDF x-data points.
    probs -- a sequence of the CDF probability values.
    N -- Number of points to return.

    RETURNS
    a tuple (values, probs) of the normal CDF values.
    '''

    m, sigma, sigma_corr = meanstd(dataset.ydata)
    n = len(dataset.xdata)
    vals, probs = generateGaussianCdf(n, m, sigma)

    return vals, probs, m, sigma

#@+node:tom.20211211171913.46: ** calcNormalForCdf
def calcNormalForCdf(values, mean=0.0, sigma=1.0):
    '''For a list of values, calculate the cumulative probability
    for a normal distribution.  Typically, the values are the
    x-axis values of a CDF curve.  Return a sequence of the
    calculated probabilities for each of the input points.

    ARGUMENTS
    values -- a list of values whose probabilities will be calculated.
    mean -- the mean of the normal distribution.
    sigma -- the standard deviation of the normal distribution.

    RETURNS
    a list of cumulative probabilities in the same order as the input values.
    '''

    # Scale values to t = (x - mean)/sigma*sqrt(2)
    mean = float(mean)
    sigma = float(sigma)
    factor = 1. / (sigma * 2 ** 0.5)
    scaled_values = [(v - mean) * factor for v in values]
    probs = scipy.special.erf(scaled_values)  # pylint: disable = no-member

    # erf() returns results in the range of (-1,1)
    # Rescale results back to the desired probability range (0,1)
    probs = [0.5 + 0.5 * p for p in probs]

    return probs

#@+node:tom.20211211171913.47: ** fitNormalToCdfAdaptive
def fitNormalToCdfAdaptive(values, probs, tolerance=.01):
    '''Given a CDF curve, fit a normal distribution to it by an
    adaptive process.  Return the final calculated probabilities, and
    the final mean standard deviation, and correlation coefficient between
    data and fitted curve.

    ARGUMENTS
    values -- a sequence of the CDF x-data points.
    probs -- a sequence of the CDF probability values.
    tolerance -- the maximum mean squared error allowed, as a fraction
                 of the mean of the original data.

    RETURNS
    a tuple (xdata, ydata, ms, sigma, correl)
    
        where
        xdata -- a sequence of values
        ydata -- a sequence of matching CDF probability values
        ms -- the fitted mean
        sigma -- the fitted standard deviation
        correl -- the correlation coefficient

    '''
    # pylint: disable = too-many-locals

    m, sigma, sigma_corr = meanstd(values)

    #@+others
    #@+node:tom.20221112230453.1: *3* sqrerror
    # Calculate mean square error
    def sqrerror(values, probs, mean, sigma):
        '''Given a list of values and cdf probabilities, and a target
        mean and standard deviation for a normal distribution,
        Return the mse between the input and a normal distribution
        with the given mean and sigma.

        ARGUMENT
        values -- a list of data values
        probs -- a list of probabilities (the CDF) of the data

        RETURNS
        the mean squared error
        '''

        merr = 0.0
        Sxx = 0.0
        normalprobs = calcNormalForCdf(values, mean, sigma)
        numvals = len(values)
        for i in range(len(values)):
            data_prob = probs[i]
            err = normalprobs[i] - data_prob
            merr += err
            Sxx += (err ** 2) * data_prob
        merr = merr / numvals
        var = Sxx / numvals
        return var
    #@+node:tom.20221112230609.1: *3* sqr_abs_error
    # Calculate mean absolute error
    def sqr_abs_error(values, probs, mean, sigma):
        '''Given a list of values and cdf probabilities, and a target
        mean and standard deviation for a normal distribution,
        Return the square of the mean absolute error between the input and
        a normal distribution with the given mean and sigma.

        ARGUMENT
        values -- a list of data values
        probs -- a list of probabilities (the CDF) of the data

        RETURNS
        the mean absolute error squared
        '''

        merr = 0.0
        normalprobs = calcNormalForCdf(values, mean, sigma)
        numvals = len(values)
        for i in range(len(values)):
            data_prob = probs[i]
            err = abs(normalprobs[i] - data_prob)
            merr += err
        merr = merr / numvals
        var = merr ** 2
        return var
    #@-others

    # Set initial iteration values
    ms = m - 3. * sigma  # Initial guess at the mean (deliberately low)
    delta = 0.9 * sigma
    delta_limit = 0.5 * tolerance * sigma

    mse = sqr_abs_error(values, probs, ms, sigma)

    done = False
    # count = 1
    new_mse = mse
    sane = True
    converged = False
    overshot = False

    # Increment trial mean until we get the error within tolerance
    while not done:
        last_mse = new_mse

        if overshot:
            delta = -delta / 2
        ms += delta

        new_mse = sqrerror(values, probs, ms, sigma)

        overshot = new_mse > last_mse

        delta_in_limits = (abs(delta) > delta_limit)
        sane = delta_in_limits and abs(ms - m) < 5 * sigma
        error_in_tolerance = (mse ** 0.5 <= tolerance)
        converged = error_in_tolerance or not delta_in_limits

        done = (
            (abs(delta / sigma) > 2 * tolerance,
        ) and (converged and overshot)) \
                    or not sane

    if converged:
        pass  #print 'Final mean: %0.3f' % ms
    else:
        # print 'Iterations are diverging too much'
        return [], [], m, sigma, 0

    # Calculate final normal CDF
    _probs = calcNormalForCdf(values, ms, sigma)
    _correl = pearson(values[1:], values[:-1])

    return values, _probs, ms, sigma, _correl

#@+node:tom.20211211171913.48: ** spearman
def spearman(x, y):
    '''Compute Spearman's rank correlation coefficient for two data sequences.
    Return the coefficient and its 95% confidence limit .

    See https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient

    We avoid ties by slightly altering equal values.  Then we can use the
    simplified formula

    R = 1 - 6 * (sum(di^2) /(n*(n^2-1))
    where di = yi - xi, yi, xi are the ranks for the points, and n = number 
    of points in either sequence.

    [Standard error of R is 0.6326/sqrt(n-1)]

    For Z-test:

        F = 0.5 ln((1 + r)/(1 - r))
        Z = F * sqrt((n-3)/1.06)

    Z indicates how large the sample R is relative to expected sample variation.

    For Student's t-test, t = r * sqrt((n-2)/(1-r^2))

    ARGUMENTS
    x, y -- The data sequences whose correlation is to be computed.  Must have same length.

    RETURNS
    a tuple (R, t, C), or None if the sequences are not the same length.  T is the
    value of Student's t, C is the width of the 95% confidence band for no
    correlation (actually, half the total width).
    '''


    if len(x) != len(y):
        return None

    # Alter data to avoid ties and calculate ranks
    def rank(data):
        '''Transform (pos, val) -> {pos:rank} for the data.
        '''

        counts = {}
        delta = 0.00001
        newdata = []

        for pos, _ in enumerate(data):
            val = data[pos]
            n = counts.get(val, 0)
            if n > 0:
                val = val * (1 + n * delta)
            n += 1
            newdata.append((val, pos))
        newdata.sort()

        ranks = {}
        for i, (_, pos) in enumerate(newdata):
            # val, pos = newdata[i]
            ranks[pos] = i

        return ranks

    _x = rank(x)
    _y = rank(y)

    N = len(x)
    N2 = N ** 2

    sum_d2 = 0.
    for i in range(len(_x)):
        d = _y[i] - _x[i]
        sum_d2 += d * d

    R = 1.0 - sum_d2 * 6.0 / (N * (N2 - 1))

    if R == 1.0:
        return R, 0., 0.

    t = R * math.sqrt((N - 2) / (1. - R * R))
    C = t_test.interval(0.95, N - 2)[1]  # t-test 95% confidence interval
    return R, t, C

#@+node:tom.20211211171913.49: ** pearson
def pearson(x, y):
    '''Given two sequences of the same length, return the sample Pearson correlation coefficient.
    See
        http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient

    ARGUMENTS
    x, y -- equal-length sequences of numbers.

    RETURNS
    Pearson's correlation coefficient, r
    '''

    N = len(x)
    xm = 1.0 * sum(x) / N
    ym = 1.0 * sum(y) / N

    # Deviations x - xm, y - ym
    xdev = [z - xm for z in x]
    ydev = [z - ym for z in y]

    # Cross products
    xy = sum([a * b for a, b in zip(xdev, ydev)])

    # Sum Squares
    x2 = sum([a * a for a in xdev])
    y2 = sum([a * a for a in ydev])

    try:
        r = xy / (x2 * y2) ** .5
    except Exception as e:
        print(e)
        r = float('NaN')

    return r
#@+node:tom.20221125220325.1: ** pearson_autocorr
def pearson_autocorr(x):
    """Return the lag-one autocorrelation of a data sequence.

    The autocorrelation is the pearson correlation between the 
    data sequence and itself shifted by one.
    
    Pearson's calculation requires the two datasets to be the same length.
    When the dataset is shifted by one, it loses one datapoint, so
    the unshifted dataset must be truncated by one.
    
    ARGUMENT
    x -- a data sequence.
    
    RETURNS
    the lag-1 autocorrelation.
    """

    return pearson(x[1:], x[:-1])
#@+node:tom.20211212001620.1: ** __main__
if __name__ == '__main__':
    import randnum
    import matplotlib.pyplot as plt

    gcf = plt.gcf

    def self_printer(f):
        def new_f():
            print(f.__name__)
            if f.__doc__:
                print(f.__doc__)
            print()
            f()
            print()
        return new_f

    randn = np.random.randn

    def testCDF():
        data = [1, 5, 2, 6, 2, 3, 5]
        data = [randn() for n in range(50)]
        xdata, ydata, _, _ = cdf(data)

        plt.plot(xdata, ydata, '-')
        plt.plot(xdata, ydata, 'bo')

        plt.show()

    def testCDF2Normal():
        data = [randn() for n in range(20)]
        data = [28, 8, -3, 7, -1, 1, 18, 12]
        xdata, ydata, _, _ = cdf(data)

        normvalues = fitNormalToCdf(xdata, ydata, 100)

        x, y, m, s = normvalues
        print('mean:', m)
        print('sigma:', s)
        print()

        plt.plot(xdata, ydata, 'bo')
        plt.plot(x, y, 'r-')
        plt.show()

    def testCalcNorm():
        data = [28, 8, -3, 7, -1, 1, 18, 12]
        # data = [randn() for n in range(8)]
        xdata, ydata, _, _ = cdf(data)

        probs = calcNormalForCdf(xdata, 6, 10.44)

        plt.plot(xdata, ydata, 'bo')
        plt.plot(xdata, probs, 'r-')
        plt.show()

    def testNormCDF():
        lower = -4  # in sigma
        upper = 4
        m = 1
        sigma = 1.0
        N = 1000
        stepsize = 1.0 * (upper - lower) / N
        _range = np.arange(lower, upper, stepsize)
        _gauss = norm.cdf(_range, m, sigma)

        _ydata = _gauss.tolist()
        _xdata = _range.tolist()

        plt.plot(_xdata, _ydata, '-')
        plt.show()

    def testFitNormalAdaptive():
        data = [28, 8, -3, 7, -1, 1, 18, 12]
        # data = [randn() for n in range(10000)]
        xdata, ydata, _, _ = cdf(data)

        tolerance = 0.001

        values, probs, m, s, _ = fitNormalToCdfAdaptive(xdata, ydata, tolerance)
        print(f'mean: {m:.3f}, sigma: {s:.2f}')

        plt.plot(xdata, ydata, 'bo')
        plt.plot(values, probs, 'r-')
        plt.show()

    def testSdevDist():
        '''Compute mean and variance of variances of a Gaussian distribution.
        '''

        size = 100000
        sample_sdev = 10.44
        sample_size = 8
        vars = []  # Sample variances
        means = []
        for i in range(size):
            index, counts = randnum.gaussian_vals(0, sample_sdev, sample_size)
            m, s, s_corr = meanstd(counts)
            vars.append(s ** 2)

        index1, varprob, _, _ = cdf(means)

        m, s, s_corr = meanstd(vars)
        print(
            'sample size={}, sample standard deviation={:.3f}'.format(\
            sample_size, sample_sdev),
        )
        print('variances: mean={:.3f}, sdev = {:.3f}'.format(m ** .5, s ** .5))

        x, sdev, _, _ = cdf(vars)
        plt.plot(x, sdev, '-')
        plt.show()

    @self_printer
    def testSpearman():
        x = (106, 86, 100, 101, 99, 103, 97, 113, 112, 110)
        y = (7, 0, 27, 50, 28, 29, 20, 12, 6, 17)

        r, t, C = spearman(x, y)
        N = len(x)
        print('1) r={:.3f}, t: {:.3f} Confidence limit={:.3f}'.format(r, t, C),)
        rmax = C * math.sqrt((1 - r * r) / (N - 2))
        print('Rmax = {:.3f}'.format(rmax))

        x = (1, 2, 3, 4, 5)
        y = (1.5, 2.2, 5, 4.5, 6)
        r, t, C = spearman(x, y)
        N = len(x)
        print('2) r={:.3f}, t: {:.3f} Confidence limit={:.3f}'.format(r, t, C),)
        rmax = C * math.sqrt((1 - r * r) / (N - 2))
        print('Rmax = {:.3f}'.format(rmax))

    @self_printer
    def testCorrelations():
        '''Calculate Pearson and Spearman correlation coefficients'''
        x = (106, 86, 100, 101, 99, 103, 97, 113, 112, 110)
        y = (7, 0, 27, 50, 28, 29, 20, 12, 6, 17)

        r = pearson(x, y)
        rspear, t, C = spearman(x, y)
        s = 0.6326 / math.sqrt(len(x) - 1)

        print("1) Pearson's r: {:.3f}".format(r))
        print(
            "1) Spearman's r: {:.3f}, t={:.3f}, C={:.3f}, SE={:.3f}".format(rspear, t, C, s))
        print()

        x = (1, 2, 3, 4, 5)
        y = (1.5, 2.2, 5, 4.5, 6)
        r = pearson(x, y)
        rspear, t, C = spearman(x, y)
        s = 0.6326 / math.sqrt(len(x) - 1)

        print("2) Pearson's r: {:.3f}".format(r))
        print(
            "2) Spearman's r: {:.3f}, t={:.3f}, C={:.3f}, SE={:.3f}".format(rspear, t, C, s))

    @self_printer
    def test_spearmanr():
        """Spearman correlation coefficient using Scipy library routine."""
        x = (106, 86, 100, 101, 99, 103, 97, 113, 112, 110)
        y = (7, 0, 27, 50, 28, 29, 20, 12, 6, 17)
        r, p = spearmanr(x, y)
        print('1) r={:.3f}, p={:.3f}'.format(r, p))

        x = (1, 2, 3, 4, 5)
        y = (1.5, 2.2, 5, 4.5, 6)
        r, p = spearmanr(x, y)
        print('2) r={:.3f}, p={:.3f}'.format(r, p))

    @self_printer
    def compare_spearman_spearmanr():
        """Compare scipy Spearman correlation with indigenous version."""
        x = (106, 86, 100, 101, 99, 103, 97, 113, 112, 110)
        y = (7, 0, 27, 50, 28, 29, 20, 12, 6, 17)
        rr, p = spearmanr(x, y)
        r, _, _ = spearman(x, y)
        print(f'spearmanr: {rr:0.3f}, spearman: {r:0.3f}')

    @self_printer
    def test_meanstd():
        x = [1, 2, 3, 4, 5]
        m, s, s_corr = meanstd(x)
        print('Mean\tstd')
        print('{:.3f}\t{:.3f}'.format(m, s))

    def runtests(testlist):
        for t in testlist:
            plt.get_current_fig_manager().set_window_title(t.__name__)
            t()

    # Tests = (testCalcNorm,)#, testCorrelations, test_spearmanr)#, testSpearman
    Tests = (
        compare_spearman_spearmanr, testCorrelations, test_spearmanr, testSpearman)
    runtests(Tests)
#@-others
#@-leo
