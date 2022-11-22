#@+leo-ver=5-thin
#@+node:tom.20211211171913.12: * @file smoother.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:tom.20211211171913.13: ** Imports
"""Functions to smooth and fit x,y data."""

import math
from statistics import median

from scipy import interpolate
#from scipy.interpolate import UnivariateSpline
import numpy as np
from csaps import csaps

from randnum import gaussian_vals
#import matplotlib.pyplot as plt

MaxSmoothZone = 100

#@+others
#@-others


if __name__ == '__main__':

    from testing import smoother_tests
    for t in smoother_tests.Tests:
        t()
#@+node:tom.20211211171913.14: ** sqr
def sqr(x):
    return x**2

#@+node:tom.20211211171913.15: ** cspline
def cspline(x, y):
    '''Fit cubic spline to sequence of points and interpolate between them.
    Return the interpolated points.

    ARGUMENTS
    x,y -- Arrays containing the x and y values for the sequence of points.

    RETURNS
    A tuple of two arrays containing the x and y interpolated values.
    '''

    tck = interpolate.splrep(x, y, s=0)
    # mean distance between x values
    md = 1.0*((x[-1] - x[0])) / len(x)
    xnew = np.arange(x[0], x[-1] + md/10.0, md/10.0)
    ynew = interpolate.splev(xnew, tck, der=0)

    return (xnew, ynew)

#@+node:tom.20211211171913.16: ** splineSmooth
def splineSmooth(x, y, s=.5):
    """Fit a set of points with a set of spline functions.  Return
    the fitted Y values.

    The fit is a statistical fit and may not go through any
    specific data point.  The smoothness of the fit can be adjusted
    using the "s" parameter.

    The parameter s is related to the number of knots that will be fitted.
    s = 1 will give the smoothest fit, and higher number wills have more
    inflections.  s must be a positive floating point number.

    The returned points have the same x values as the originals
    (i.e., no interpolation between data points is done).

    ARGUMENTS
    x -- the x-axis data.  May be a sequence or a numpy array.
    y -- the y-axis data.  May be a sequence or a numpy array.
    s -- a floating point positive number in the range 0 -> 1.

    RETURNS
    an array containing the y smoothed values.
    """
    ys = csaps(x, y, x, smooth=s)
    return (x, ys)

#@+node:tom.20211211171913.17: ** class WtStats
# ========== Auxiliary classes for use in smoothing routines ======

class WtStats:
    #@+others
    #@+node:tom.20211211171913.18: *3* WtStats.__init__
    def __init__(self):
        self.weights = []
        self.smoothzone = 0
        self.center = 0
        self.Swt = 0

    def __str__(self):
        return f'WtStats: len(weights): {len(self.weights)}, center: {self.center}, width: {self.smoothzone}'
    #@+node:tom.20211211171913.19: *3* WtStats.MakeGaussianWeights
    def MakeGaussianWeights(self, smoothwidth=4):
        '''Compute weights to use with smoother. These weights
        form a truncated gaussian curve normalized to 1.0. If 
        smoothwidth is even, increment by one to make it odd.

        ARGUMENT
        smoothwidth -- width of window in data points
                      (two-sided). Should be even; adjusted if odd

        RETURNS
        nothing
        '''

        _smoothzone = smoothwidth
        if smoothwidth % 2 == 0:
            _smoothzone = smoothwidth + 1
        self.smoothzone = _smoothzone
        numwts = _smoothzone # total number of weights
        icenter = int(_smoothzone / 2) # index of center point
        nSigma = 2.0
        self.Swt = 0
        self.center = icenter

        # Half-width is nSigma sigma, so sigma = half-width / nSigma
        SmoothSigma = 1.0 * _smoothzone/(2 * nSigma)
        denom = 1./(2 * sqr(SmoothSigma))
        for i in range(numwts):
            self.weights.append(math.exp(-1.0 * sqr(i - icenter) * denom))
            self.Swt += self.weights[i]

    #@+node:tom.20211211171913.20: *3* WtStats.omitOne
    def omitOne(self):
        '''Omit the center point by setting its weight to 0.  This may be used
        in cross-validation studies.
        '''

        if len(self.weights) > 1:
            center = int(len(self.weights) / 2) # Python now returns floor of integer division
            self.weights[center] = 0.0
    #@-others

#@+node:tom.20211211171913.21: ** correlationCoeff
def correlationCoeff(data, fitted):
    '''Given a sequence of data and a sequence of fitted points (e.g.,
    from a least square fit), return the correlation coefficient.

    See http://ocw.usu.edu/Civil_and_Environmental_Engineering/Uncertainty_in_Engineering_Analysis/Regression_DataFitting_Part2.pdf
    Calculate (1) sum of squared deviations from fitted value, and
    (2) sum of squared deviations from the sample mean.

    Correlation Ceofficient r = sqrt(1 - (1) / (2) )

    Note that this formula is only correct when the mean of the fitted data
    equals the mean of the raw data.  This would be true if the fit were
    by a least squares procedure.  Also, (2) has to be larger than 1, so the variations
    in the data have to be larger than the variations from the fitted points.

    For correctly fitted data, this correlation coefficient generally (always?)
    equals Pearson's Correlation Coefficient, r.

    ARGUMENTS
    data -- a sequence of the data values
    fitted -- a sequence of the fitted values for each of the data values

    RETURNS
    the correlation coefficient, or -1 if r^2 would be negative.
    '''

    mean = 1.0*sum(data) / len(data)
    fitted_mean = 1.0*sum(fitted) / len(fitted)

    def corr(x, xf):
        Sdf = 0.0 # Deviations from fitted points
        Sdm = 0.0 # Deviations from mean
        mean = 1.0*sum(x)/len(x)
        for y, yf in zip(x, xf):
            Sdf += 1.0*(y - yf) **2
            Sdm += 1.0*(y - mean) **2
        return 1 - (Sdf / Sdm)

    r = corr(data, fitted)
    if r >= 0:
        return r**0.5

    # Assume either the means are too far apart or the data have
    # more variation than the "fitted" - in case the "fitted"
    # data are not really fitted by just another random variable.
    # Shift data to match the means and try again.
    if fitted_mean != mean:
        delta = mean - fitted_mean
        new_fitted = [x+delta for x in fitted]
    r = corr(data, new_fitted)

    if  r < 0:
        return - 1

    return r**0.5

#@+node:tom.20211211171913.22: ** SmoothPointLowess
def SmoothPointLowess(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
    '''Fit a point in a sequence using a local linear least squares fit.
    Neighboring points contribute to the fit according to weights
    assigned using a weight table.  Return the fitted point, its square
    deviation, and whether or not if falls outside a clipping level.

    This function implements the core fitting portion of the LOWESS
    smoothing algorithm published by Cleveland.  The code is ported
    and adapted from the original Turbopascal code written by
    Thomas B. Passin for the GSTAT.EXE program.

    ARGUMENTS
    xdata, ydata -- lists of the x and y data.  Must be the same length.
    wt -- a WtStats instance that has the weight table filled in.
    i -- the index of the point (x,y) to be smoothed.
    cliplevel -- threshold for designating points as fliers
    causal -- If True, use only neighbors to left of specified point.  Otherwise,
              use neighbors on both sides.

    RETURNS
    a tuple (s, v, se, is_flier), where s is the smoothed value of the point,
    v is the variance at the point, se is the weighted standard error of the
    mean, and is_flier is boolean that is True if
    the point lies farther than cliplevel standard deviations
    from the fitted point.
    '''
    # pylint: disable=too-many-locals
    Swt = 0.0 # sum of weights
    Swx = 0.0 # weighted sum of x
    Swy = 0.0 # weighted sum of y
    Swxy = 0.0 # weighted sum of xy
    Swxx = 0.0 # weighted sum of xx
    Swyy = 0.0 # weighted sum of yy
    Sww = 0.0 # sum of squared weights
    a = 0.0 # y = ax + b for linear fit within the window
    b = 0.0
    SqrDev = 0

    sz = wt.smoothzone

    N = len(xdata)
    x = xdata[i]

    half = sz / 2
    window_left = int(max(i - half, 0))
    window_right = int(min(1 + i + half, N))
    _offset = i - half

    for j in range(window_left, window_right):
        weight_index = int(j - _offset)
        wj = wt.weights[weight_index]
        xtemp = xdata[j]
        ytemp = ydata[j]
        Swx = Swx +  wj*xtemp
        Swy = Swy +  wj*ytemp
        Swxy = Swxy +  wj* xtemp*ytemp
        Swxx = Swxx + wj * xtemp**2
        Swyy = Swyy + wj * ytemp**2
        Swt = Swt + wj
        Sww += wj**2

    a = (Swt*Swxy - Swx*Swy)/(Swt*Swxx - sqr(Swx))
    b = (Swy - a*Swx)/(Swt)

    y0 = a*x + b

    # Variance
    Svar = 0.
    for j in range(window_left, window_right):
        weight_index = int(j - _offset)
        wj = wt.weights[weight_index]
        xj = xdata[j]
        yj = ydata[j]
        yfit = a*xj + b
        Svar += wj*(yj-yfit)**2

    var = (Svar / Swt) *0.5*sz/(.5*sz - 1)

    # Approximate standard error of the fitted point
    se = ((var * Sww)**0.5) / Swt

    is_flier = (abs(ydata[i] - y0) > cliplevel * math.sqrt(SqrDev))
    return (y0, var, se, is_flier)

#@+node:tom.20211211171913.23: ** lowess
def lowess(xdata, ydata, smoothzone=10, omitOne=False):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points.  For each point, neighboring points
    are used to calculate the fit, using a table of weights to weight
    the points.  The window includes smoothzone points on either side of
    the given point.  The window width is adjusted when the given point
    gets too close to either end of the data.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width in number of data points.
                  Should be even, adjusted up if not.
    omitOne -- For each point, omit that point when computing the fit.
               This can be used for cross-validation assessment.
               Implemented by setting the weight for the point to 0.

    RETURNS
    A tuple of two arrays containing the original x and smoothed y values.
    '''

    wt = WtStats()
    N = len(xdata)
    if N % 2 == 1:
        smoothzone = smoothzone + 1
    smoothzone = min(N - 1, smoothzone)
    wt.MakeGaussianWeights(smoothzone)
    if omitOne:
        wt.omitOne()

    fliers = []
    smooths = []
    for i, _ in enumerate(xdata):
        y, v, se, is_flier = SmoothPointLowess(xdata, ydata, wt, i)
        smooths.append(y)
        if is_flier:
            fliers.append((xdata[i], ydata[i]))

    return (xdata, smooths)

#@+node:tom.20211211171913.24: ** lowess1
def lowess1(xdata, ydata, smoothzone=10, omitOne=False):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points, and the autocorrelation of the residuals
    (calculated according to p49 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    For each point, neighboring points are used to calculate the fit,
    using a table of weights to weight the points.  The window includes
    smoothzone points on either side of the given point.  The window width
    is adjusted when the given point gets too close to either end of the data.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width for the smoothing weights.
    omitOne -- For each point, omit that point when computing the fit.
               This can be used for cross-validation assessment.
               Implemented by setting the weight for the point to 0.

    RETURNS
    A tuple (x, yf, r) where x is the original x series, yf is the fitted
        series, and r is the lag-1 autocorrelation of the residuals.
    '''

    wt = WtStats()
    N = len(xdata)
    if N % 2 == 1:
        smoothzone = smoothzone + 1
    smoothzone = min(N - 1, smoothzone)
    wt.MakeGaussianWeights(smoothzone)
    if omitOne:
        wt.omitOne()

    fliers = []
    smooths = []
    for i, _ in enumerate(xdata):
        y, v, se, is_flier = SmoothPointLowess(xdata, ydata, wt, i)
        smooths.append(y)
        if is_flier:
            fliers.append((xdata[i], ydata[i]))

    e = [smooths[i] - ydata[i] for i in range(len(ydata))] # residuals
    num = 0.0
    denom = 0.0
    for i in e:
        denom += sqr(i)
    for i in range(1, len(ydata)):
        num += e[i] * e[i - 1]
    r = abs(num / denom)

    return (xdata, smooths, r)

#@+node:tom.20211211171913.25: ** deriv
def deriv(xdata, ydata):
    '''Estimate the derivative dy/dx for (possibly) unequally-spaced
    data.  Return a tuple (xnew, dy) where xnew is a list of the
    x values and dy is a list of the derivative values at each of those
    x values. Note that there will be one fewer points than the original data.

    ARGUMENTS
    xdata, ydata -- sequences containing the x and y data values.

    RETURNS
    dy -- list of (x values, derivative values.
    '''

    derivs = []
    for i in range(len(xdata) - 1):
        if i == 0:
            dy = (ydata[i+1] - ydata[i])/(xdata[i+1] -xdata[i])
            derivs.append(dy)
        else:
            dx1 = xdata[i+1] - xdata[i]
            dx = xdata[i] - xdata[i-1]
            dy = (ydata[i+1] - ydata[i]) / dx1 + (ydata[i] - ydata[i-1]) / dx
            dy = 0.5*dy
            derivs.append(dy)

    return xdata[:-1], derivs

#@+node:tom.20220805142529.1: ** lowess2
def lowess2(xdata, ydata, smoothzone=10, omitOne=False):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points, and the rms of the residuals
    (calculated according to p36 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    For each point, neighboring points are used to calculate the fit,
    using a table of weights to weight the points.  The window includes
    smoothzone points on either side of the given point.  The window width
    is adjusted when the given point gets too close to either end of the data.

    Store the fitted point +- 1 s.d. into two subgraphs.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width for the smoothing weights.
    omitOne -- For each point, omit that point when computing the fit.
               This can be used for cross-validation assessment.
               Implemented by setting the weight for the point to 0.

    RETURNS
    A tuple (x, yf, rms, upperbound, lowerbound) where x is the original x series,
    yf is the fitted series, rms is the rms deviation from fitted points,
    and upperbound, lowerbound are the y values for y +/- 2 std dev.
    '''

    wt = WtStats()
    N = len(xdata)
    if N % 2 == 1:
        smoothzone = smoothzone + 1
    smoothzone = min(N - 1, smoothzone)
    wt.MakeGaussianWeights(smoothzone)
    if omitOne:
        wt.omitOne()
    fliers = []
    smooths = []
    ses = []
    upperlimit = []
    lowerlimit = []
    ERRORLIMIT = 2.0

    for i, _ in enumerate(xdata):
        y, v, se, is_flier = SmoothPointLowess(xdata, ydata, wt, i)
        smooths.append(y)
        ses.append(se)
        upperlimit.append(y + ERRORLIMIT *se)
        lowerlimit.append(y - ERRORLIMIT *se)
        if is_flier:
            fliers.append((xdata[i], ydata[i]))

    mean_err = sum(ses) / len(xdata)

    return (xdata, smooths, mean_err, upperlimit, lowerlimit)

#@+node:tom.20220805142822.1: ** lowess2_stddev
def lowess2_stddev(xdata, ydata, smoothzone=10, omitOne=False):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points, the standard deviations, and the rms of the residuals
    (calculated according to p36 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    For each point, neighboring points are used to calculate the fit,
    using a table of weights to weight the points.  The window includes
    smoothzone points on either side of the given point.  The window width
    is adjusted when the given point gets too close to either end of the data.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width for the smoothing weights.
    omitOne -- For each point, omit that point when computing the fit.
               This can be used for cross-validation assessment.
               Implemented by setting the weight for the point to 0.

    RETURNS
    A tuple (x, stddev) where x is the original x series,
    and stddev is a list of the weighted standard deviations at the given
    data points x.
    '''
    wt = WtStats()
    N = len(xdata)
    if N % 2 == 1:
        smoothzone = smoothzone + 1
    smoothzone = min(N - 1, smoothzone)
    wt.MakeGaussianWeights(smoothzone)
    if omitOne:
        wt.omitOne()
    stddevs = []

    for i, _ in enumerate(xdata):
        y, v, se, is_flier = SmoothPointLowess(xdata, ydata, wt, i)
        stddevs.append(v**0.5)

    return (xdata, stddevs)

#@+node:tom.20211211171913.27: ** lowessAdaptive
def lowessAdaptive(xdata, ydata, weight=1.0,
                   spans=(3, 5, 10, 15, 20, 25, 30, 40, 60, 70, 80)):
    """Smooth sequence of points using Cleveland's LOWESS algorithm.
    Estimate the best span of points by making multiple LOWESS
    runs with different spans.  This span balances fit with smoothness
    of the fitted curve.  Return the points smoothed with the
    estimated best span.

    Score each run using a penalty expression (to be minimized) that includes
    the mean squared error and a roughness function, as in Eq. 6.1 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    The penalty expression is

        p = (mse) + w * (msr)

    mse = mean squared error, computed using the cross-validation
          method, that is, to set omitOne = True (i.e., by
          omitting the focal point of the LOWESS calculation).
    msr = mean square of the second derivative.
    w = a weight parameter.  0 neglects the roughness of the fit, very large
        values maximize the importance of a smooth fit.  A value of 1
        is likely to be a useful value to start with.

    To score the set of runs, scale the smoothness function so that its
    average value across the runs equals the average value of the
    mean squared error across the runs.  Then use the weight parameter
    to adjust the multiplier for the smoothness.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    weight -- relative weight to give to the roughness factor.
    spans -- a sequence of span values to use when estimating the best span.

    RETURNS
    A tuple (x, yf, bestspan, rms, upperbound, lowerbound) where x is the original
        x series, yf is the fitted series, bestspan is the estimated best span
        used to compute the fitted series, rms is the rms deviation
        from fitted points, and
        upperbound, lowerbound are the y values
        for y +- sqrt(var).
    """
    # pylint: disable=too-many-locals
    weight = float(weight)
    mse = []
    rough = []

    if type(xdata) is type(np.ndarray([])):
        xdata = xdata.tolist()
    N = len(xdata)

    for s in (s1 for s1 in spans if s1 <= N):
        #xi, yi, rms, upperlimit, lowerlimit = lowess2(xdata, ydata, s, True)
        xi, yi, rms, upperlimit, lowerlimit = lowess2(xdata, ydata, s, False)
        var = sum([float((_y - _yfit)**2)/(N-1) for _y, _yfit in zip(ydata, yi)])
        mse.append(var)

        xp, dy = deriv(xi, yi)
        xpp, ddy = deriv(xp, dy)
        k = sum([abs(_d) for _d in ddy]) / len(ddy) # Mean absolute curvature
        rough.append(k)

    mean_rough = sum(rough) / len(rough)

    mean_mse = sum(mse) / (len(mse) - 1)

    rough_scale_factor = weight * mean_mse / mean_rough

    if __name__ == '__main__':
        print ( 'Roughness Weight:', weight)
        print ( 'roughness scale factor:', rough_scale_factor)
        print ( 'Span \tPenalty   \tmse  \t  Roughness')

    penalty = []
    for i, _ in enumerate(mse):
        penalty.append(mse[i] + rough[i] * rough_scale_factor)

    bestindex = penalty.index(min(penalty))
    best = spans[bestindex]

    xi, yi, rms, upperlimit, lowerlimit = lowess2(xdata, ydata, best, False)
    return xi, yi, best, rms, upperlimit, lowerlimit

#@+node:tom.20211211171913.28: ** leastsqr
def leastsqr(xdata, ydata, deg=1):
    '''Calculate a least squares fit to a set of x,y points.
    Return a list of the fitted Y values evaluated at the original
    X values, the mean, the rms deviation from fitted points,
    the correlation coefficient, and upperbound, lowerbound are the
    y values for y +- sqrt(var).

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    deg -- the degree of the fit (1 = linear, 2 = quadratic, etc): 2 max

    RETURNS
    a tuple  (list of the fitted values, mean, s.e., r, upperbound, lowerbound).
    '''

    coeffs = np.polyfit(xdata, ydata, deg)
    p = np.poly1d(coeffs)
    fitted_y = [p(x) for x in xdata]

    var = 0.0
    #mean = 0.0
    N = len(fitted_y)

    y_mean = 1.0 * sum(ydata) / N
    x_mean = 1.0 * sum(xdata) / N

    for ys, y in zip(ydata, fitted_y):
        var += (1.0*ys - y)**2

    var = var / (N - 2)  # Variance of any one fitted point
    #rms = (var**0.5)
    se = (var/(N-1))**0.5 # std error of residuals

    # Estimated SD of slope from least-squares formula:
    # Var(slope) = (1/(N-2)) * sum(yi_fitted - yi)^2 / sum(xi - x_avg)^2
    # See https://en.wikipedia.org/wiki/Simple_linear_regression#Confidence_intervals
    y_mean = 1.0 * sum(ydata) / N
    x_mean = 1.0 * sum(xdata) / N
    #var_slope = (1.0/(N-2)) * sum([(y_fit - _y)**2 for y_fit, _y in zip(fitted_y, ydata)]) \
    #            / sum([(xi - x_mean)**2 for xi in xdata])
    #sd_slope = var_slope**0.5

    # See Wikipedia:
    # https://en.wikipedia.org/wiki/Simple_linear_regression#Confidence_intervals
    eps_2 = [(_y - _yf)**2 for _y, _yf in zip(ydata, fitted_y)]
    Sx2 = sum([(_xi - x_mean)**2 for _xi in xdata])
    var_all = [(1./(N-2)) * sum(eps_2) * (1./N + ((_xi - x_mean)**2)/Sx2) \
                for _xi in xdata]
    se_all = [_v**0.5 for _v in var_all]

    upper = [y + 2*se for y,se in zip(fitted_y, se_all)]
    lower = [y - 2*se for y,se in zip(fitted_y, se_all)]

    r = correlationCoeff(ydata, fitted_y)

    return (fitted_y, y_mean, se, r, upper, lower)

#@+node:tom.20211211171913.29: ** determinant
def determinant(x11, x12, x13, x21, x22, x23,
        x31, x32, x33):
    '''Compute determinant of 3X3 matrix.  Return the value
    of the determinant.

    ARGUMENTS
    x11, ... x33 -- the nine elements of the 3 X 3 matrix.

    RETURNS
    the value of the matrix's determinant.
    '''
    # pylint: disable=too-many-arguments
    return x11*(x22*x33 - x23*x32) + x12*(x23*x31 - x33*x21) \
                + x13*(x21*x32 -x22*x31)

#@+node:tom.20211211171913.30: ** SmoothPointLowessQuad
def SmoothPointLowessQuad(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
    '''Fit a point in a sequence using a local quadratic least squares fit.
    Neighboring points contribute to the fit according to weights
    assigned using a weight table.  Return the fitted point, its square
    deviation, and whether or not if falls outside a clipping level.

    This function implements the core fitting portion of the LOWESS
    smoothing algorithm published by Cleveland.  The code is ported
    and adapted from the original Turbopascal code written by
    Thomas B. Passin for the GSTAT.EXE program.

    ARGUMENTS
    xdata, ydata -- lists of the x and y data.  Must be the same length.
    wt -- a WtStats instance that has the weight table filled in.
    i -- the index of the point (x,y) to be smoothed.
    cliplevel -- threshold for designating points as fliers
    causal -- If True, use only neighbors to left of specified point.  Otherwise,
              use neighbors on both sides.

    RETURNS
    a tuple (s, v, se, is_flier), where s is the smoothed value of the point,
    v is the variance at the point, se is the weighted standard deviation of the
    fitted point, and is_flier is a boolean that is True if
    the point lies farther than cliplevel standard deviations
    from the fitted point.
    '''
    # pylint: disable=too-many-locals
    # y = axx + bx + c for quadratic fit within the window
    a = np.float64(0.0) # y = axx + bx + c for quadratic fit within the window
    b = np.float64(0.0)
    c = np.float64(0.0)
    SqrDev = np.float64(0)

    sz = wt.smoothzone #Full width of smoothing window in data points

    xdata = [np.float64(z) for z in xdata]
    ydata = [np.float64(z) for z in ydata]

    N = len(xdata)
    x = xdata[i]
    #yfocal = ydata[i]

    half = int(sz / 2)
    window_left = max(i - half, 0)
    window_right = min(1 + i + half, N)
    _offset = i - half

    def compute_dets(wt, xdata, ydata, window_left, window_right, offset):
        ''' Accumulate terms to be summed in lists, so that they can be
        summed using math.fsum().  fsum uses higher precision for the
        intermediate sums.  This avoids occasional problems with
        insufficient precision that we can get if directly adding up
        each term as it is calculated.  See
        http://docs.python.org/2/library/math.html
        '''

        _swt = [] # sum of weights
        _swx = [] # weighted sum of x
        _swy = [] # weighted sum of xy
        _swxy = [] # weighted sum of xy
        _swxx = [] # weighted sum of xx
        _swyy = [] # weighted sum of yy
        _swxxx = [] # weighted sum of xxx
        _swxxxx = [] # weighted sum of x^4
        _swyxx = [] # weighted sum of y*x^2
        _sww = [] # Sum of squared weights

        for j in range(window_left, window_right):
            weight_index = j - offset
            wj = wt.weights[weight_index]
            xtemp = xdata[j]
            ytemp = ydata[j]
            xsqr = xtemp**2
            x3 = xtemp**3
            x4 = xtemp**4
            ysqr = ytemp**2
            _swx.append(wj*xtemp)
            _swy.append(wj*ytemp)
            _swxy.append( wj* xtemp*ytemp)
            _swxx.append(wj* xsqr)
            _swyy.append(wj * ysqr)
            _swt.append(wj)
            _swxxx.append(wj * x3)
            _swxxxx.append(wj * x4)
            _sww.append(wj**2)

            Swx = math.fsum(_swx)
            Swy = math.fsum(_swy)
            Swxy = math.fsum(_swxy)
            Swxx = math.fsum(_swxx)
            #Swyy = math.fsum(_swyy)
            Swt = math.fsum(_swt)
            Swxxx = math.fsum(_swxxx)
            Swxxxx = math.fsum(_swxxx)
            Swyxx = math.fsum(_swyxx)
            #Sww = math.fsum(_sww)

        det = determinant(Swxxxx, Swxxx, Swxx,
                          Swxxx, Swxx, Swx,
                          Swxx, Swx, Swt)

        a = determinant(Swyxx, Swxxx, Swxx,
                        Swxy, Swxx, Swx,
                        Swy, Swx, Swt) / det

        b = determinant(Swxxxx, Swyxx, Swxx,
                        Swxxx, Swxy, Swx,
                        Swxx, Swy, Swt) / det

        c = determinant(Swxxxx, Swxxx, Swyxx,
                        Swxxx, Swxx, Swxy,
                        Swxx, Swx, Swy) / det
        return det, a, b ,c

    det, a,b,c = compute_dets(wt, xdata, ydata, window_left, window_right, _offset)
    y0 = a*x**2 + b*x + c
    parms = a,b,c

    dabs = abs(det)
    #ylim = max([abs(_y) for _y in ydata ])
    recentered = False
    if True or dabs < 100000 and not recentered:
        #  recenter x data
        _xmax = max(xdata)
        _xmin = min(xdata)
        xc = 1.0*(_xmax-_xmin)
        orig_x = xdata[:]
        _xdata = [_x - xc for _x in orig_x]
        recentered = True

        # Quick and dirty check for matrix conditioning
        # Larger determinant is better for stability.
        # Perturb data, then recenter x data, then see
        # which determinant is bigger.
        eps = .2
        delta = [abs((_y2 - _y1))/N for _y2, _y1 in zip(ydata[1:], ydata[:-1])]
        sigma = eps * sum(delta) / N
        _rands = gaussian_vals(0.0, sigma, N)[1]

        _newy = [_y + _r for _y, _r in zip(ydata, _rands)]
        det, a,b,c = compute_dets(wt, _xdata, _newy, window_left, window_right, _offset)
        _x_recen = _xdata[i]
        y0_est = a*_x_recen**2 + b*_x_recen + c

        if abs(det) > dabs:
            y0 = y0_est
            parms = a,b,c
            xdata = _xdata

    Svar = 0.
    Swt = 0.
    Sww = 0.
    A, B, C = parms
    for j in range(window_left, window_right):
        weight_index = j - _offset
        wj = wt.weights[weight_index]
        xj = xdata[j]
        yj = ydata[j]
        yfit = A*xj**2 + B*xj + C
        Svar += wj*(yj-yfit)**2
        Swt += wj
        Sww += wj*wj

    var = (Svar / Swt) *0.5*sz/(.5*sz - 1)

    # Approximate standard error of the fitted point
    #se = ((var * Sww)**0.5) / Swt
    se = ((Svar/Swt) / ((Swt**2 / Sww) - 1))**0.5

    is_flier = (abs(ydata[i] - y0) > cliplevel * math.sqrt(SqrDev))

    return (y0, var, se, is_flier)

#@+node:tom.20211211171913.31: ** ySmoothPointLowessQuad
def ySmoothPointLowessQuad(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
    '''Fit a point in a sequence using a local quadratic least squares fit.
    Neighboring points contribute to the fit according to weights
    assigned using a weight table.  Return the fitted point, its square
    deviation, and whether or not if falls outside a clipping level.

    This function implements the core fitting portion of the LOWESS
    smoothing algorithm published by Cleveland.  The code is ported
    and adapted from the original Turbopascal code written by
    Thomas B. Passin for the GSTAT.EXE program.

    ARGUMENTS
    xdata, ydata -- lists of the x and y data.  Must be the same length.
    wt -- a WtStats instance that has the weight table filled in.
    i -- the index of the point (x,y) to be smoothed.
    cliplevel -- threshold for designating points as fliers
    causal -- If True, use only neighbors to left of specified point.  Otherwise,
              use neighbors on both sides.

    RETURNS
    a tuple (s, d, se, is_flier), where s is the smoothed value of the point,
    d is the variance at the point, se is the weighted standard deviaton of the
    fitted point, and is_flier is a boolean that is True if
    the point lies farther than cliplevel standard deviations
    from the fitted point.
    '''
    # pylint: disable=too-many-locals
    Swt = 0.0 # sum of weights
    Swx = 0.0 # weighted sum of x
    Swy = 0.0 # weighted sum of y
    Swxy = 0.0 # weighted sum of xy
    Swxx = 0.0 # weighted sum of xx
    Swyy = 0.0 # weighted sum of yy
    Swxxx = 0.0 # weighted sum of xxx
    Swxxxx = 0.0 # weighted sum of x^4
    Swyxx = 0.0 # weighted sum of y*x^2
    Sww = 0.0 # Sum of squared weights

    a = 0.0 # y = axx + bx + c for quadratic fit within the window
    b = 0.0
    c = 0.0
    SqrDev = 0

    sz = wt.smoothzone #Full width of smoothing window in data points

    N = len(xdata)
    x = xdata[i]

    half = sz / 2
    window_left = max(i - half, 0)
    window_right = min(1 + i + half, N)
    _offset = i - half

    for j in range(window_left, window_right):
        weight_index = j - _offset
        wj = wt.weights[weight_index]
        xtemp = xdata[j]
        ytemp = ydata[j]
        xsqr = xtemp**2
        x3 = xtemp**3
        x4 = xtemp**4
        ysqr = ytemp**2
        Swx = Swx +  wj*xtemp
        Swy = Swy +  wj*ytemp
        Swxy = Swxy +  wj* xtemp*ytemp
        Swxx = Swxx + wj* xsqr
        Swyy = Swyy + wj * ysqr
        Swt = Swt + wj
        Swxxx = Swxxx + wj * x3
        Swxxxx = Swxxxx + wj * x4
        Swyxx = Swyxx + wj * ytemp * xsqr
        Sww = wj**2

    det = determinant(Swxxxx, Swxxx, Swxx,
                      Swxxx, Swxx, Swx,
                      Swxx, Swx, Swt)

    a = determinant(Swyxx, Swxxx, Swxx,
                    Swxy, Swxx, Swx,
                    Swy, Swx, Swt) / det

    b = determinant(Swxxxx,Swyxx, Swxx,
                    Swxxx, Swxy, Swx,
                    Swxx, Swy, Swt) / det

    c = determinant(Swxxxx, Swxxx, Swyxx,
                    Swxxx, Swxx, Swxy,
                    Swxx, Swx, Swy) / det

    y = a*x**2 + b*x + c
    var = (Swyy - 2.*y*Swy + Swt*y**2) / Swt
    var = max(var, 0)

    se = (var * Sww)**0.5/Swt

    is_flier = (abs(ydata[i] - y) > cliplevel * math.sqrt(SqrDev))
    return (y, var, se, is_flier)

#@+node:tom.20211211171913.32: ** lowess2Quad
def lowess2Quad(xdata, ydata, smoothzone=10, omitOne=False):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points, and the mean square error of the residuals
    (calculated according to p36 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    For each point, neighboring points are used to calculate the fit using
    a quadratic weighted least squares fit, using a table of weights to
    weight the points.  The window includes smoothzone points on either
    side of the given point.  The window width is adjusted when the given
    point gets too close to either end of the data.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width for the smoothing weights.
    omitOne -- For each point, omit that point when computing the fit.
               This can be used for cross-validation assessment.
               Implemented by setting the weight for the point to 0.
               [Not implemented yet]

    RETURNS
    A tuple (x, yf, rms) where x is the original x series, yf is the fitted
        series, rms is the rms deviation from fitted points,
        and upperbound, lowerbound are the y values for y +- standard error.
    '''

    wt = WtStats()
    N = len(xdata)
    if N % 2 == 1:
        smoothzone = smoothzone + 1
    smoothzone = min(N - 1, smoothzone)

    wt.MakeGaussianWeights(smoothzone)
    if omitOne:
        wt.omitOne()
    wt.weights = [np.float64(z) for z in wt.weights]

    fliers = []
    smooths = []
    ses = []
    upperlimit = []
    lowerlimit = []
    errorlimit = 2.0

    for i, _ in enumerate(xdata):
        y, v, se, is_flier = SmoothPointLowessQuad(xdata, ydata, wt, i)
        if y > 2:
            pass #print xdata[i], ydata[i], y, type(ydata[i])
        smooths.append(y)
        ses.append(se)
        upperlimit.append(y + errorlimit * se)
        lowerlimit.append(y - errorlimit * se)
        if is_flier:
            fliers.append((xdata[i], ydata[i]))

    mean_err = sum(ses) / len(xdata)

    return (xdata, smooths, mean_err, upperlimit, lowerlimit)

#@+node:tom.20211211171913.33: ** xlowessAdaptiveAC
def xlowessAdaptiveAC(xdata, ydata):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Estimate the best span of points by making multiple LOWESS
    runs with different spans.  The fit criterion is the value of the
    autocorrelation.   autocorrelation of the residuals is
    calculated according to p49 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.

    Return the points smoothed with the
    estimated best span.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.

    RETURNS
    A tuple (x, yf, bestspan, rms, ac, upperbound, lowerbound) where x is the original
        x series, yf is the fitted series, bestspan is the estimated best span
        used to compute the fitted series, rms is the rms error, ac is the best
        autocorrelation, and upperbound, lowerbound are the y values for y +- sqrt(var).
    '''

    spans=(3, 5, 10, 15, 20, 25, 30, 40, 60)

    if type(xdata) is type(np.ndarray([])):
        xdata = xdata.tolist()
    #N = len(xdata)

    param = []
    for s, _ in enumerate(spans):
        xi, yi, r = lowess1(xdata, ydata, spans[s])
        param.append((abs(r), spans[s]))

    param.sort()
    rmin, sbest = param[0]

    xi, yi, rms, upperlimit, lowerlimit = lowess2Quad(xdata, ydata, sbest, False)

    return xi, yi, sbest, rms, rmin, upperlimit, lowerlimit

#@+node:tom.20211211171913.34: ** lowessAdaptiveAC
def lowessAdaptiveAC(xdata, ydata):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Estimate the best span of points by making multiple LOWESS
    runs with different spans.  The fit criterion is the value of the
    autocorrelation.   autocorrelation of the residuals is
    calculated according to p49 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.

    Return the points smoothed with the
    estimated best span.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.

    RETURNS
    A tuple (x, yf, bestspan, rms, ac, upperbound, lowerbound) where x is the original
        x series, yf is the fitted series, bestspan is the estimated best span
        used to compute the fitted series, rms is the rms error, ac is the best
        autocorrelation, and upperbound, lowerbound are the y values for y +- sqrt(var).
    '''

    #spans=(3, 5, 10, 15, 20, 25, 30, 40, 60)

    if type(xdata) is type(np.ndarray([])):
        xdata = xdata.tolist()
    #N = len(xdata)

    thresh = 0.05
    eps = 0.001
    reps = 0
    rep_limit = 20
    delta = 3 # step size
    #overshot = False
    converged = False
    too_many = False
    #smallest = 0.0
    last_r = 0.0

    smallest_yet = None

    width = 4
    last_r = 0

    #print 'width\tdelta\tr\t\tlast r\tr - last_r'
    while not converged and not too_many:
        xi, yi, r = lowess1(xdata, ydata, int(width))
        #print width, '\t', delta, '\t%f' % r, '\t%f' % last_r,
        reps += 1
        r = abs(r)
        if reps == 1:
            #smallest = r
            last_r = 3*r
            smallest_yet = (r, width)

        #print '%0.4f' % (abs(r - last_r)),  abs(r - last_r) < eps
        if reps > 1 and abs(r - last_r) < eps:
            converged = True
            break

        last_r = r
        converged = (abs(r) < thresh)
        too_many = (reps > rep_limit)

        #print '%s\t%s\t%s\t%0.3f'  % (reps, width, delta, r)
        if r > smallest_yet[0]:
            # reverse and halve distance to best width
            delta = int((smallest_yet[1] - width) / 2.0)
        elif r < smallest_yet[0]:
            smallest_yet = (r, width)

        if delta == 0:
            converged = True
           # print 'Converged'
            break
        width += delta
        if width < 2:
            break

    #print 'Final: %f %s' % smallest_yet
    #print 'results'
    #print '%s\t%s\t%s\t%0.3f'  % (reps, smallest_yet[1], delta, smallest_yet[0])

    xi, yi, rms, upperlimit, lowerlimit = lowess2(xdata, ydata,  smallest_yet[1], False)

    return xi, yi, smallest_yet[1], rms, smallest_yet[0], upperlimit, lowerlimit

#@+node:tom.20211211171913.35: ** SmoothPointPoisson
def SmoothPointPoisson(xdata, ydata, i, smoothzone):
    '''Fit a point in a sequence using a local linear least squares fit.
    Neighboring points contribute to the fit according to weights
    assigned as the estimated inverse variance of the point.  The
    variance is assumed to equal the data value;  This. variance is
    characteristic for a Poisson distribution.

    Return the fitted point, its square deviation, and standard error.

    The y data points must be >= 0

    If a y value is zero, we set its variance to 1, since with a Poisson
    distribution, a count of 0 has the same probability as a count of 1.

    This function implements the core fitting portion of the LOWESS
    smoothing algorithm published by Cleveland.  The code is adapted from the
    LOWESS smoothing code from the gf4 program.

    ARGUMENTS
    xdata, ydata -- lists of the x and y data.  Must be the same length.
    i -- the index of the point (x,y) to be smoothed.
    smoothzone -- width of smoothing window, in data points.

    RETURNS
    a tuple (s, v, se), where s is the smoothed value of the point,
    v is the variance at the point, se is the weighted standard error of the
    mean.
    '''
    # pylint: disable=too-many-locals
    Swt = 0.0 # sum of weights
    Swx = 0.0 # weighted sum of x
    Swy = 0.0 # weighted sum of y
    Swxy = 0.0 # weighted sum of xy
    Swxx = 0.0 # weighted sum of xx
    Swyy = 0.0 # weighted sum of yy
    Sww = 0.0 # sum of squared weights
    a = 0.0 # y = ax + b for linear fit within the window
    b = 0.0
    #SqrDev = 0

    sz = smoothzone

    N = len(xdata)
    x = xdata[i]

    half = sz / 2
    window_left = int(max(i - half, 0))
    window_right = int(min(1 + i + half, N))
    #_offset = i - half


    if ydata[window_left : window_right] == [0] * (window_left - window_right):
        return (0., 0., 0.)

    for j in range(window_left, window_right):
        xtemp = xdata[j]
        ytemp = ydata[j]

        # Weights
        if ytemp == 0:
            wj = 1.
        else:
            wj = 1./ytemp  # Because this is a Poisson distribution.

        Swx = Swx +  wj*xtemp
        Swy = Swy +  wj*ytemp
        Swxy = Swxy +  wj* xtemp*ytemp
        Swxx = Swxx + wj * xtemp**2
        Swyy = Swyy + wj * ytemp**2
        Swt = Swt + wj
        Sww += wj**2

    try:
        a = (Swt*Swxy - Swx*Swy)/(Swt*Swxx - sqr(Swx))
        b = (Swy - a*Swx)/(Swt)

        y = a*x + b
        var = (Swyy - 2.*y*Swy + Swt*y**2) / Swt

        var = max(var, 0)

        # Approximate standard error of the fitted point
        se = ((var * Sww)**0.5)/Swt
    except ZeroDivisionError:
        return (0., 0., 0.)

    return (y, var, se)

#@+node:tom.20211211171913.36: ** poissonSmooth
def poissonSmooth(xdata, ydata, smoothzone=10):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points.  For each point, neighboring points
    are used to calculate the fit, using a table of weights to weight
    the points.  The window includes smoothzone points on either side of
    the given point.  The window width is adjusted when the given point
    gets too close to either end of the data.

    If the x-axis data is not in increasing order, the data are re-ordered
    before smoothing.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width in number of data points.
                  Should be even, adjusted up if not.

    RETURNS
    A tuple of (x, y, mse) x is a sequence containing the sorted x values,
    y contains the smoothed y values, and mse of the fitted points.

    RAISES
    ValueError if any input y value is less than 0.
    '''

    # Test data values for >= 0
    neg_values = []
    for y in ydata:
        if y < 0:
            neg_values.append(y)
    if neg_values:
        raise ValueError ('Negative values not allowed: %0.3f, ...' % neg_values[0])

    N = len(xdata)
    if N % 2 == 1:
        smoothzone = smoothzone + 1
    smoothzone = min(N - 1, smoothzone)
    smooths = []

    _temp = list(zip(xdata, ydata))
    _temp.sort()
    xdata, ydata = zip(*_temp)
    xdata = list(xdata)
    ydata = list(ydata)

    for i in range(len(xdata)):
        y, v, se = SmoothPointPoisson(xdata, ydata, i, smoothzone)
        smooths.append(y)

    e = [sqr(smooths[i] - ydata[i]) for i in range(len(smooths))] # residuals
    mse = 0.0
    for r in e:
        mse += r
    mse = (mse / (len(smooths) - 1))**0.5

    return (xdata, smooths, mse)

#@+node:tom.20211211171913.37: ** thiel_sen
def thiel_sen(x,y):
    """Fit line robustly to X,Y data using Thiel-Sen algorithm.  Return the
    fitted y points as a sequence.

    This is a brute force implementation: the slope between all pairs
    of points is calculated, and the median value is assigned as
    the estimated slope.  The intercept is estimated by
    the median value of b = y - ax, where "a" is the median slope.

    The standard deviation of the slope is estimated using the linear
    least squares formula (since the Thiel-Sen slope is usually
    close to the least squares slope).  This will overestimate the
    S.D. of the slope if there are too many fliers.

    ARGUMENTS
    x -- a sequence of x-values (assumed exact).
    y -- a sequence of y-values (assumed to have errors).

    RETURNS
    a tuple (a list of the fitted y values, slope, intercept, estimated S.D. of slope)
    """

    slopes = []
    for i, _ in enumerate(x):
        for j in range(i+1, len(x)):
            if i == j or x[i] == x[j]:
                continue

            slope = 1.0*(y[j] - y[i]) / (x[j] - x[i])
            if x[i] > x[j]:
                slope = -slope
            slopes.append(slope)

    med_slope = median(slopes)

    # y = ax + b
    b = median([_y - med_slope*_x for _x,_y in zip(x,y)])

    fitted = [med_slope * _x + b for _x in x]

    # Estimated SD of slope from least-squares formula:
    # Var(slope) = (1/(N-2)) * sum(yi_fitted - yi)^2 / sum(xi - x_avg)^2

    N = len(x)
    x_mean = 1.0 * sum(x) / N
    var_slope = (1.0/(N-2)) * sum([(y_fit - _y)**2 for y_fit, _y in zip(fitted, y)]) \
                / sum([(xi - x_mean)**2 for xi in x])
    sd_slope = var_slope**0.5

    return (fitted, med_slope, b, sd_slope)

#@+node:tom.20211211171913.38: ** moving_median
def moving_median(xdata, ydata, w = 7):
    """Smooth a sequence of data values using a moving median.

    The median value within the window is placed at the center
    of the window.  For points closer to the start or end
    of the data set than the window width, the median is
    not computed.  This entails that the start and end of
    the data is truncated by half the window width.

    The window width should be odd;  if not, it is coerced
    to the next higher odd value.

    ARGUMENTS
    ydata -- the sequence of values to smooth
    w -- the width of the smoothing window to use.

    RETURNS
    a tuple (x, y), where y is the smoothed ydata.
    """

    if w % 2 == 0:
        w += 1

    results = []
    offset = w // 2
    for i in range(offset, len(ydata) - offset):
        results.append(median(ydata[i - offset:i + offset]))

    return xdata[offset: -offset], results

#@-others
#@-leo
