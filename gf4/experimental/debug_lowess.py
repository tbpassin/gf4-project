#@+leo-ver=5-thin
#@+node:tom.20221127124842.1: * @file experimental/debug_lowess.py
"""Implementation of LOWESS with degree-n local fits using numpy poly fits.

This function is adapted from SmoothPointLowessQuad() but changes the way
the fit is computed.
"""
from math import sqrt
from smoother import WtStats

def sqr(x):
    return x * x

#@+others
#@+node:tom.20221127124842.2: ** SmoothPointLowess
def smoothPointLowess(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
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

    half = sz // 2
    window_left = max(i - half, 0)
    window_right = min(1 + i + half, N)
    _offset = i - half

    # This only works right because the weight function is symmetrical
    for j in range(window_left, window_right):
        weight_index = j - _offset
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

    is_flier = (abs(ydata[i] - y0) > cliplevel * sqrt(SqrDev))
    return (y0, var, se, is_flier)
#@+node:tom.20221127124842.3: ** localLowess
def localLowess(xdata, ydata, smoothzone = 11, degree = 1, omitOne=False):
    '''
    #@+<< docstring >>
    #@+node:tom.20221127124842.4: *3* << docstring >>
    Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points, and the mean square error of the residuals
    (calculated according to p36 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    For each point, neighboring points are used to calculate the fit using
    a n-degree polynomial weighted least squares fit, using a table of 
    weights to weight the points.  The window includes smoothzone points.
    The window width is adjusted when the given point gets too close to either 
    end of the data.

    ARGUMENTS
    xdata,ydata -- sequences containing the x and y data values.
    smoothzone -- the full window width for the smoothing weights.
    omitOne -- For each point, omit that point when computing the fit.
               This can be used for cross-validation assessment.
               Implemented by setting the weight for the point to 0.

    RETURNS
    A tuple (x, yf, rms) where x is the original x series, yf is the fitted
        series, rms is the rms deviation from fitted points,
        and upperbound, lowerbound are the y values for y +- standard error.
    #@-<< docstring >>
    '''
    wt = WtStats()
    N = len(xdata)
    smoothzone = min(N - 1, smoothzone)
    # Must be odd
    if smoothzone % 2 == 0:
        smoothzone += 1

    wt.MakeGaussianWeights(smoothzone)
    if omitOne:
        wt.omitOne()

    fliers = []
    smooths = []
    ses = []
    upperlimit = []
    lowerlimit = []
    errorlimit = 2.0
    for i, _ in enumerate(xdata):
        y, v, se, is_flier = smoothPointLowess(xdata, ydata, wt, i)
        smooths.append(y)
        ses.append(se)
        upperlimit.append(y + errorlimit * se)
        lowerlimit.append(y - errorlimit * se)
        if is_flier:
            fliers.append((xdata[i], ydata[i]))

    mean_err = sum(ses) / len(xdata)

    return (xdata, smooths, mean_err, upperlimit, lowerlimit, fliers)

#@-others
#@-leo
