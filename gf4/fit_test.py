#@+leo-ver=5-thin
#@+node:tom.20211211181438.2: * @file fit_test.py
# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211181438.3: ** Organizer: Declarations (fit_test.py)
'''Test a fitted regression against the null hypothesis of no relationship.'''

import sys
from math import sqrt
from random import sample
from numpy import polyfit, poly1d

from smoother import lowess2, sqr

ENCODING = 'utf-8'
#@+node:tom.20211211181438.4: ** null_rss (fit_test.py)
def null_rss(ydata):
    '''Calculate the residual sum of squares of a sequence (i.e.,
    the square deviations from the mean).

    ARGUMENT
    ydata -- a sequence of data values.

    RETURNS
    a tuple containing the sum of squares of the residuals, the mean
    y value, and the sample standard deviation
    '''

    n = len(ydata)
    mean = 0.0
    for y in ydata:
        mean += y
    mean = mean / n
#    y0sqr = mean * mean

    rss0 = 0.0
    for y in ydata:
        rss0 += sqr(y - mean)

    var = rss0
    try:
        stddev = sqrt(var) / sqrt(n-1)
    except Exception as e:
        print(e)
        print(n, var)
        sys.exit(0)

    return rss0, mean, stddev

#@+node:tom.20211211181438.5: ** null_T (fit_test.py)
def null_T(rss0, rssx):
    '''Calculate a T statistic for two sets of points, using their residual
    sum of squares.  Return the T statistic.  T is used to assess
    whether the two sets of data points differ only by chance or not.
    T is calculated by

        T = (rss0 - rssx)/ rss0

    ARGUMENTS
    rss0 -- the residual sum of squares for the null hypothesis
    rssx -- the residual sum of squares for a fitted curve to the original 
    data set.

    RETURNS
    the T statistic.
    '''

    return (rss0 - rssx) / rss0

#@+node:tom.20211211181438.6: ** permuted_T (fit_test.py)
def permuted_T(xdata, ydata, N, smooth, rss0):
    '''Permute xdata, then fit using LOWESS.  Repeat N times.
    Return the T statistic of the permuted data.

    ARGUMENTS
    xdata, ydata -- the original sequence of data points
    N -- the number of permutations to perform
    smooth -- the one-sided width of the smoothing zone for LOWESS smoothing
    rss0 -- the residual sum of squares of the null hypothesis

    RETURNS
    a list of the N T statistics
    '''

    n = len(ydata)

    Tstat = []
    for i in range(N):
        newy = sample(ydata, n)
        x, y, mse, _, _ = lowess2(xdata, newy, smooth)
        Tstat.append(null_T(rss0, n * mse))
        
    return Tstat

#@+node:tom.20211211181438.7: ** permuted_lstsqr (fit_test.py)
def permuted_lstsqr(xdata, ydata, N, deg=1):
    '''Permute xdata, then fit using linear least sqiares.  Repeat N times.
    Return a list of the fitted curves

    ARGUMENTS
    xdata, ydata -- the original sequence of data points
    N -- the number of permutations to perform

    RETURNS
    a list of the fitted curves [ [y11,y12,...], [y21,y22,...], ...]
    '''

    n = len(ydata)
    fitted_curves = []
    for i in range(N):
        newy = sample(ydata, n)
        coeffs = polyfit(xdata, newy, deg)
        p = poly1d(coeffs)
        fitted_curves.append([p(x) for x in xdata])

    return fitted_curves

#@+node:tom.20211211181438.8: ** pnull (fit_test.py)
def pnull(tstats, tfit):
    '''Calculate probability that the null hypothesis is correct.
    Return the probability.

    ARGUMENTS
    tstats -- a sequence of the randomized test statistics
    tfit -- the test statistic for the fitted data

    RETURNS
    the probability that the fitted test statistic would be larger than it
    is, just by chance, if the null hypothesis were true.
    '''

    count = 0
    for t in tstats:
        if t > tfit: count += 1

    return (1.0 * count) / len(tstats)

#@+node:tom.20211211181438.9: ** dist (fit_test.py)
def dist(tstats):
    '''Calculate the probability distribution of the test statistic.
    Return a list of (p, count) values.

    ARGUMENT
    tstats -- a sequence of the randomized test statistics
    
    RETURNS
    a list [(p1, n1), ...] sorted by the p values
    '''

    probs = []
    counts = {}
    for t in tstats:
        counts[t] = counts.get(t, 0) + 1

    N = float(len(tstats))
    # pylint: disable = modified-iterating-dict
    for t in counts:
        counts[t] = counts[t] / N

    probs = counts.items()
    probs.sort()

    return probs

#@+node:tom.20211211181438.10: ** readfile (fit_test.py)
def readfile(fname):
    if not fname: return None
    with open(fname, encoding = ENCODING) as f:
        lines = f.readlines()

    xdata = []
    ydata = []
    for line in lines:
        text = line.strip()
        if not text: continue
        if text[0] == ';': continue
        fields = text.split()
        if len(fields) < 2: return None

        xdata.append(float(fields[0]))
        ydata.append(float(fields[1]))

    return xdata, ydata


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from os.path import basename

    def plot_permutes_lstsrq(parms):
        xdata = parms['xdata']
        ydata = parms['ydata']
        N = parms['N']
        deg = parms.get('deg') or 1
        fname = parms.get('fname') or ''

        permutes = permuted_lstsqr(xdata, ydata, N, deg)

        # Statistics of ydata
        mean = 0
        meansqr = 0
        num = len(ydata)

        for y in ydata:
            mean += y
            meansqr += sqr(y)
        mean = float(mean) / num
        meansqr = float(meansqr) / num

        var = meansqr - sqr(mean)
        sigma = sqrt(var) * sqrt(num/(num-1))
        stderr = sigma /sqrt(num)

        print('Y mean: %0.3f   Y sigma: %0.3f   Y std err: %0.3f' % (mean, sigma, stderr))

        #fig = plt.figure()
        plt.get_current_fig_manager().set_window_title('Randomization Test Of Null Hypothesis') 
        plt.subplot(1, 1, 1)

        for p in permutes:
            plt.plot(xdata, p, '0.75', linewidth=1)

        plt.plot(xdata, ydata, 'ko')

        # Plot least squares fit
        coeffs = polyfit(xdata, ydata, deg)
        p = poly1d(coeffs)
        plt.plot(xdata, [p(x) for x in xdata], 'k', linewidth=2)

        if fname: plt.suptitle(fname)
        plt.title('%s Linear Least Square Fits to Permuted Data' % N)
        
        plt.show()

    def plot_permutes_lowess(parms={}):
        xdata = parms['xdata']
        ydata = parms['ydata']
        smooth = parms.get('smooth') or 5
        fname = parms.get('fname') or ''

        rss0, ymean, stddev = null_rss(ydata)
        print('Null hypothesis RSS: %0.3f' % rss0)
        print('Null hypothesis mean, std dev: %0.3f, %0.3f' % (ymean, stddev))

        n = len(ydata)
        x, y, mse, _, _ = lowess2(xdata, ydata, smooth)
        print('RSS for LOWESS fit: %0.3f' % (mse*n))

        Tnull = null_T(rss0, n * mse)

        print('Fitted T statistic for null hypothesis: %0.3f' % Tnull)

        tstats = permuted_T(xdata, ydata, 1000, smooth, rss0)

        p = pnull(tstats, Tnull)
        print('Probability of fitted curve if null hypothesis is right:',)
        if p < 1.0e-3:
            print('%1.2e' % p)
        else:
            print('%0.3f' % p)

        #fig = plt.figure()
        plt.get_current_fig_manager().set_window_title('Randomization Test Of Null Hypothesis - LOWESS fits') 
        plt.subplot(1, 1, 1)
        plt.plot(xdata, ydata, 'bo')
        plt.plot(xdata, y, 'b')

        plt.title('Prob(Fitted Curve) = %0.3f If Null Hypothesis Is Right' % p)
        if fname: plt.suptitle(fname)

        plt.show()

    if len(sys.argv) > 1:
        fname = sys.argv[1]
        xdata, ydata = readfile(fname)
        file = basename(fname)
    else:
        xdata = [1,2,3,4,5,6,7]
        ydata = [1,3,2,5,5,7,6]
        file = ''

        #xdata = [1,2,3,4,5,6,7]
        #ydata = [1,3,8,18,29,31,50]

    if len(sys.argv) > 2:
        smooth = int(sys.argv[2])
        N = smooth
    else:
        smooth = 8
        N = 100

    tests = {'Permute-LOWESS': plot_permutes_lowess,
                'Permute-Lstsqr': plot_permutes_lstsrq}

    parms = {'Permute-LOWESS': {
                'xdata':xdata,
                'ydata':ydata,
                'smooth':smooth,
                'fname':file},
             'Permute-Lstsqr': {
                'xdata':xdata,
                'ydata':ydata,
                'N':N,
                'deg': 1,
                'fname':file}
            }

    t = 'Permute-Lstsqr'
    #t = 'Permute-LOWESS'
    tests[t](parms[t])
#@-others
#@@language python
#@@tabwidth -4
#@-leo
