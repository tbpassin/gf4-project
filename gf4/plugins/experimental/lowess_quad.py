#@+leo-ver=5-thin
#@+node:tom.20221128184351.1: * @file lowess_quad.py
"""Implementation of LOWESS with quadratic local fits using brute force.

This function is adapted from SmoothPointLowessQuad() but changes the way
the fit is computed.
"""
from math import sqrt, fsum
import numpy as np
from smoother import WtStats
from randnum import gaussian_vals

#@+others
#@+node:tom.20221128184753.1: ** smoothPointLocalQuad
def smoothPointLocalQuad(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
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

    sz = wt.smoothzone # Full width of smoothing window in data points
    wt.weights = [np.float64(w) for w in wt.weights]
    # wt.weights = [np.float64(1.) for w in wt.weights]  # uniform weights

    xdata = [np.float64(z) for z in xdata]
    ydata = [np.float64(z) for z in ydata]

    half = wt.center
    window_left = i - half
    window_right = i + half
    _offset = i - half

    #@+others
    #@+node:tom.20221129135200.1: *3* compute_coeffs
    def compute_coeffs(wt, xdata, ydata, window_left, window_right, offset):
        '''Return the coefficients a, b, c for the local fit to the data slice.
        
        Also returns the determinant and the fitted point on the x axis.
        '''
        i = window_left + wt.center

        _swt = np.float64(0) # sum of weights
        _swx = np.float64(0) # weighted sum of x
        _swy = np.float64(0) # weighted sum of xy
        _swxy = np.float64(0) # weighted sum of xy
        _swxx = np.float64(0) # weighted sum of xx
        # _swyy = np.float64(0) # weighted sum of yy
        _swxxx = np.float64(0) # weighted sum of xxx
        _swxxxx = np.float64(0) # weighted sum of x^4
        _swyxx = np.float64(0) # weighted sum of y*x^2
        # _sww = np.float64(0) # Sum of squared weights

        # This only works right because the weight function is symmetrical
        for j in range(window_left, window_right + 1):
            assert j < len(xdata), f'j too large: {j}, points: {len(xdata)}; {window_left}  {window_right}; {j - offset}'
            weight_index = j - offset
            wj = wt.weights[weight_index]
            xtemp = xdata[j]
            ytemp = ydata[j]
            xsqr = xtemp**2
            x3 = xtemp**3
            x4 = xtemp**4
            # ysqr = ytemp**2
            _swx += wj*xtemp
            _swy += wj*ytemp
            _swxy += wj* xtemp*ytemp
            _swxx += wj* xsqr
            # _swyy += wj * ysqr
            _swt += wj
            _swxxx += wj * x3
            _swxxxx += wj * x4
            # _sww += wj**2

        Swx = _swx
        Swy = _swy
        Swxy = _swxy
        Swxx = _swxx
        # Swyy = fsum(_swyy)  # not actually used
        Swt = _swt
        Swxxx = _swxxx
        Swxxxx = _swxxx
        Swyxx = _swyxx
        # Sww = fsum(_sww)  # apparently not actually used

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
        return det, xdata[i - 1], a, b ,c
    #@-others

    det, x0, a,b,c = compute_coeffs(wt, xdata, ydata, window_left, window_right, _offset)
    # y0 = a*x**2 + b*x + c
    y0 = x0 * (a * x0 + b) + c
    parms = a, b, c
    Svar = 0.
    Swt = 0.
    Sww = 0.
    A, B, C = parms
    for j in range(window_left, window_right + 1):
        weight_index = j - _offset
        wj = wt.weights[weight_index]
        xj = xdata[j]
        yj = ydata[j]
        # yfit = A*xj**2 + B*xj + C
        yfit = xj * (A * xj + B) + C
        Svar += wj*(yj-yfit)**2
        Swt += wj
        Sww += wj*wj

    var = (Svar / Swt) * 0.5 * sz/(.5 * sz - 1)

    # Approximate standard error of the fitted point
    #se = ((var * Sww)**0.5) / Swt
    se = ((Svar/Swt) / ((Swt**2 / Sww) - 1))**0.5

    is_flier = (abs(ydata[i] - y0) > cliplevel * sqrt(SqrDev))

    return (y0, x0, var, se, is_flier)

#@+node:tom.20221128224611.1: ** ysmoothPointLocalQuad
def ysmoothPointLocalQuad(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
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

    sz = wt.smoothzone # Full width of smoothing window in data points

    xdata = [np.float64(z) for z in xdata]
    ydata = [np.float64(z) for z in ydata]

    N = len(xdata)

    x = xdata[i]
    #yfocal = ydata[i]

    half = sz // 2
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
        wt.weights = [np.float64(w) for w in wt.weights]
        # wt.weights = [np.float64(1.) for w in wt.weights]  # uniform weights

        # This only works right because the weight function is symmetrical
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

        Swx = fsum(_swx)
        Swy = fsum(_swy)
        Swxy = fsum(_swxy)
        Swxx = fsum(_swxx)
        # Swyy = fsum(_swyy)  # not actually used
        Swt = fsum(_swt)
        Swxxx = fsum(_swxxx)
        Swxxxx = fsum(_swxxx)
        Swyxx = fsum(_swyxx)
        # Sww = fsum(_sww)  # apparently not actually used

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
    # y0 = a*x**2 + b*x + c
    y0 = x * (a * x + b) + c
    parms = a, b, c

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
        # y0_est = a*_x_recen**2 + b*_x_recen + c
        y0_est = _x_recen * (a * _x_recen + b) + c

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
        # yfit = A*xj**2 + B*xj + C
        yfit = xj * (A * xj + B) + C
        Svar += wj*(yj-yfit)**2
        Swt += wj
        Sww += wj*wj

    var = (Svar / Swt) * 0.5 * sz/(.5 * sz - 1)

    # Approximate standard error of the fitted point
    #se = ((var * Sww)**0.5) / Swt
    se = ((Svar/Swt) / ((Swt**2 / Sww) - 1))**0.5

    is_flier = (abs(ydata[i] - y0) > cliplevel * sqrt(SqrDev))

    return (y0, var, se, is_flier)

#@+node:tom.20221128212052.1: ** xsmoothPointLocalQuad
def xsmoothPointLocalQuad(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
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

    half = sz // 2
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
        # wt.weights = [np.float64(w) for w in wt.weights]
        wt.weights = [np.float64(1.) for w in wt.weights]

        # This only works right because the weight function is symmetrical
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

        Swx = fsum(_swx)
        Swy = fsum(_swy)
        Swxy = fsum(_swxy)
        Swxx = fsum(_swxx)
        # Swyy = math.fsum(_swyy)
        Swt = fsum(_swt)
        Swxxx = fsum(_swxxx)
        Swxxxx = fsum(_swxxx)
        Swyxx = fsum(_swyxx)
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
    # y0 = a*x**2 + b*x + c
    y0 = x * (a * x + b) + c
    parms = a, b, c

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
        # y0_est = a*_x_recen**2 + b*_x_recen + c
        y0_est = _x_recen * (a * _x_recen + b) + c

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
        # yfit = A*xj**2 + B*xj + C
        yfit = xj * (A * xj + B) + C
        Svar += wj*(yj-yfit)**2
        Swt += wj
        Sww += wj*wj

    var = (Svar / Swt) * 0.5 * sz/(.5 * sz - 1)

    # Approximate standard error of the fitted point
    #se = ((var * Sww)**0.5) / Swt
    se = ((Svar/Swt) / ((Swt**2 / Sww) - 1))**0.5

    is_flier = (abs(ydata[i] - y0) > cliplevel * sqrt(SqrDev))

    return (y0, var, se, is_flier)

#@+node:tom.20221128190006.1: ** determinant
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

#@+node:tom.20221128184715.1: ** localQuadLowess
def localQuadLowess(xdata, ydata, smoothzone=11, omitOne=False):
    '''Smooth sequence of points using Cleveland's LOWESS algorithm.
    Return the smoothed points, and the mean square error of the residuals
    (calculated according to p36 of

    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.)

    For each point, neighboring points are used to calculate the fit using
    a quadratic weighted least squares fit, using a table of weights to
    weight the points.  The window includes smoothzone points on either
    side of the given point.  The window width is adjusted when the given
    point gets too close to either end of the data.
    The data is extended by 0 for smoothzone points to the left and right.

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

    width = wt.center
    fliers = []
    smooths = []
    x_smoothed = []
    ses = []
    upperlimit = []
    lowerlimit = []
    delta_x = float(xdata[-1] - xdata[0]) / (N - 1)
    errorlimit = 2.0

    # Extend xdata to left and right to provide a "landing pad"
    # so we don't have to fool around truncating the weights near the ends.
    extension_left = [(-width + i)* delta_x for i in range(width)]
    extension_right = [(N + i) * delta_x for i in range(width)]
    newx = extension_left
    newx.extend(xdata)
    newx.extend(extension_right)

    # Extend ydata with the average values of the left and right to
    # avoid sudden jumps where non-zero data ends.
    runout = 5
    yl_avg = ydata[0] #sum(ydata[0: runout]) / runout
    yr_avg = ydata[-1] #sum(ydata[-runout:]) / runout
    y_extension = [yl_avg] * width
    newy = y_extension
    newy.extend(ydata)
    newy.extend([yr_avg] * width)

    # Iterate over only the original points, not the extended ones.
    for i in range(width, len(xdata) + width, 1):
        # Target point is at index i
        y, x, v, se, is_flier = smoothPointLocalQuad(newx, newy, wt, i)
        smooths.append(y)
        x_smoothed.append(x)
        ses.append(se)
        upperlimit.append(y + errorlimit * se)
        lowerlimit.append(y - errorlimit * se)
        if is_flier:
            fliers.append((newx[i], newy[i]))

    # smooths = smooths[smoothzone: -smoothzone]
    # ses = ses[smoothzone: -smoothzone]
    # upperlimit = upperlimit[smoothzone: -smoothzone]
    # lowerlimit = lowerlimit[smoothzone: -smoothzone]
    mean_err = sum(ses) / len(xdata)

    return (x_smoothed, smooths, mean_err, upperlimit, lowerlimit, fliers)

#@-others
#@-leo
