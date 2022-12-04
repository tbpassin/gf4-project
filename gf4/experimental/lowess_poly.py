#@+leo-ver=5-thin
#@+node:tom.20221121171312.1: * @file lowess_poly.py
"""Implementation of LOWESS with degree-n local fits using numpy poly fits.

This function is adapted from SmoothPointLowessQuad() but changes the way
the fit is computed.
"""
from math import sqrt
import numpy as np
from smoother import WtStats

#@+others
#@+node:tom.20221122144251.1: ** smoothPointLocalPoly
def smoothPointLocalPoly(xdata, ydata, wt, i, degree = 1, cliplevel=2.0, causal=False):
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
    degree -- degree of the polynomial fit
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
    # Full width of smoothing window in data points. Always odd
    sz = wt.smoothzone
    num = len(xdata)
    center_wt_index = wt.center
    # Use working x-axis sequentially indexed for the poly fit
    x_prime = [i for i, z in enumerate(ydata)]

    if i < center_wt_index:
        width = center_wt_index + i + 1
        wghts = wt.weights[center_wt_index - i:]
        x_left = 0
        x_right = width
    elif i <= num - center_wt_index - 2:
        x_left = i - center_wt_index
        x_right = i + center_wt_index + 1
        wghts = wt.weights
    else:
        width = (num - i) + center_wt_index# number of points in window
        wghts = wt.weights[0:width]
        x_left = num - width - 1
        x_right = num - 1
        # print(i, x_left, x_right, width, wghts)

    span = (x_left, x_right)
    x_ = x_prime[x_left: x_right]
    y_ = ydata[x_left: x_right]
    try:
        polyfit = np.polynomial.polynomial.Polynomial.fit(x_, y_, degree, window = span, w = wghts)
    except Exception as e:
        print('====', e)
        print('target:', i, 'sz:', sz, 'smoothzone:', wt.smoothzone, ', len(x):', len(x_), ', len(y):', len(y_), ', len(wts):', len(wghts), ', span:', span, x_left, x_right)
        raise e

    y0 = np.polynomial.polynomial.polyval(x_prime[i], polyfit.coef)
    Svar = 0.
    Swt = 0.
    Sww = 0.
    for j in range(x_left, x_right):
        weight_index = j - x_left
        # if i > num - center_wt_index - 3: print(i, j, weight_index)
        wj = wt.weights[weight_index]
        xj = x_prime[j]
        yj = ydata[j]
        yfit = np.polynomial.polynomial.polyval(xj, polyfit.coef)
        Svar += wj*(yj-yfit)**2
        Swt += wj
        Sww += wj*wj

    var = (Svar / Swt) *0.5*sz/(.5*sz - 1)

    # Approximate standard error of the fitted point
    #se = ((var * Sww)**0.5) / Swt
    se = sqrt((Svar/Swt) / ((Swt**2 / Sww) - 1))

    is_flier = (abs(ydata[i] - y0) > cliplevel * sqrt(var))

    return (y0, var, se, is_flier)

#@+node:tom.20221121190901.1: ** localPolyLowess
def localPolyLowess(xdata, ydata, smoothzone=11, degree = 1, omitOne=False):
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
    smoothzone = min(N - 1, smoothzone)

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
        y, v, se, is_flier = smoothPointLocalPoly(xdata, ydata, wt, i, degree = degree)
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
