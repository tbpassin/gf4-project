#@+leo-ver=5-thin
#@+node:tom.20211206205420.2: * @file testing/smoother_tests.py
#@+others
#@+node:tom.20211210160855.3: ** Imports, Declarations
import sys
import os.path
import random
from random import gauss
import math
import matplotlib.pyplot as plt

rcParams = plt.rcParams
gcf = plt.gcf
gca = plt.gca

# pylint: disable = wrong-import-position
# Locate smoother.py, add to Python path so imports work reliably
our_dir = os.path.dirname(__file__)
gf4_dir = os.path.split(our_dir)[0]
sys.path.insert(0, gf4_dir)

from smoother import (deriv, sqr, lowess, lowess2Quad, thiel_sen,
                      lowess2, moving_median, cspline, splineSmooth, lowess1,
                      lowessAdaptiveAC, leastsqr, lowessAdaptive, WtStats)

from randnum import gaussian_vals

STYLE = 'ggplot'

rcParams['figure.figsize'] = (12,9)
rcParams['axes.grid'] = True
rcParams['ytick.direction'] = 'out'
rcParams['xtick.direction'] = 'out'

# pylint: disable = consider-using-f-string
#@+node:tom.20211210160855.4: ** self_printer
def self_printer(f):
    def new_f(*args):
        print()
        print ('Test:', f.__name__)
        if f.__doc__: print (f'"{f.__doc__}"')
        f(*args)
    return new_f

#@+node:tom.20211210160855.5: ** cspline_fit
@self_printer
def cspline_fit():
    'Test Cubic Spline Fit'
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [0, 2, 3, 1, 5, 6, 8]

    r, s = cspline(x, y)

    plt.plot(r,s,'black')
    plt.plot(x,y,'ro')
    plt.title('Cubic Spline Fit')
    figure = gcf()
    figure.canvas.manager.set_window_title('Cubic Spline Smooth')
    plt.show()

#@+node:tom.20211210160855.6: ** spline_smooth
@self_printer
def spline_smooth():
    '''Test Spline Smoother'''

    N = 200
    x = [0.05*i for i in range(0, N)]
    true_y = [math.sin(z)*math.exp(-.2*z) for z in x]
    y = [_y + random.uniform(-.5, .5) for _y in true_y]

    rcParams['figure.figsize'] = 12, 10

    smooths =   (.01, .1, .5, .9)
    for p, s in enumerate(smooths):
        xi, yi = splineSmooth(x, y, s)
        plt.subplot(len(smooths), 1, p + 1)
        plt.plot(x, y, 'o', color='gray',)
        plt.plot(x, yi, 'black')
        plt.plot(x, true_y, 'gray', linewidth=2)
        plt.title(
            'Smoothing with spline - smoothing parameter = %s' \
            % (s))

    figure = gcf()
    #figure.canvas.manager.window.wm_geometry('1200x900+600+50')
    #figure.canvas.manager.window.wm_geometry('+600+50')
    figure.canvas.manager.set_window_title('Spline Smooth')

    plt.show()
#@+node:tom.20211210160855.7: ** lowess_smooth
@self_printer
def lowess_smooth():
    'Test LOWESS Smoother lowess()'

    N = 200
    x = [0.05*i for i in range(0, N)]
    y = [math.sin(z)*math.exp(-.2*z) + random.uniform(-.5, .5) for z in x]

    rcParams['figure.figsize'] = 12, 12
    plt.style.use(STYLE)

    smooth = (10, 15, 20, 25, 30)
    for s, _ in enumerate(smooth):
        xi, yi = lowess(x, y, smooth[s])

        plt.subplot(len(smooth), 1, s+1)
        plt.plot(x, y, 'bo')
        plt.plot(xi, yi, 'g')
        plt.title('Smoothing with LOWESS - smoothing parameter = %s'
            % (smooth[s]))

    figure = gcf()
    #figure.canvas.manager.window.wm_geometry('+600+50')
    figure.canvas.manager.set_window_title('LOWESS Smooth')

    plt.show()
#@+node:tom.20211210160855.8: ** lowess2_smooth
@self_printer
def lowess2_smooth():
    'Test LOWESS2 Smoother'

    N = 200
    x = [0.05*i for i in range(0, N)]
    true_y = [math.sin(z)*math.exp(-.2*z) for z in x]
    y = [_y + random.gauss(0, .2) for _y in true_y]

    rcParams['figure.figsize'] = 8, 6
    plt.style.use(STYLE)
    #ax = plt.gca()
    ax = gca()

    smooths = 10, 15, 20, 30, 45, 60
    for s in smooths:
        xs, ys, mse, upperbound, lowerbound = lowess2(x, y, s)
        plt.plot(x, ys, 'blue', linewidth=1)

    plt.plot(x, upperbound, 'gray', linewidth=1)
    plt.plot(x, lowerbound, 'gray', linewidth=1)
    ax.fill_between(x, upperbound, lowerbound, facecolor='blue', alpha=0.1)
    plt.title('Smoothing with LOWESS Linear - smoothing parameter = %s, mse = %0.3g'
        % (s, mse), fontsize = 13)

    plt.plot(x, true_y, 'black', linewidth=3)
    plt.plot(x, y, 'wo', mew=.2, mec='black')

    figure = gcf()
    figure.canvas.manager.set_window_title('LOWESS Smooth')
    plt.show()
#@+node:tom.20211210160855.9: ** lowess1_autocorr
@self_printer
def lowess1_autocorr(func=None):
    'Test LOWESS Adaptive Smoothing Using Residual Autocorrelations'

    N = 200
    if not func:
        func = lambda z: math.sin(z)*math.exp(-.2*z)

    x = [0.05*i for i in range(0, N)]
    y = [func(z) + 0.25*random.uniform(-.5, .5) for z in x]
    true_y = [func(z) for z in x]

    smooth = (5, 10, 15, 20, 25, 30, 40, 50, 60)
    param = []
    print( 'Span\tAutocorr')
    for s, _ in enumerate(smooth):
        xi, yi, r = lowess1(x, y, smooth[s])
        param.append((abs(r), smooth[s]))
        #print '%s\t%0.3f' % (smooth[s], r)
        print ('{}\t{:.3f}'.format(smooth[s], r))

    param.sort()
    _, sbest = param[0]

    print ( 'Best')
    print ( 'Span\tAutocorr.')
    print ( '%(sbest)s \t%(rmin)0.3f' % (locals()))

    xi, yi, rms, upperbound, lowerbound = lowess2(x, y, sbest)

    #figure = gcf()
    #figure.set_size_inches(12, 8)
    rcParams['figure.figsize'] = 9, 7

    plt.plot(x, true_y, 'black', linewidth=2)
    plt.plot(x, y, 'co', mfc='white')
    plt.plot(xi, yi, 'black', linewidth=1)
    plt.title('LOWESS Autocorrelation Adaptive - smoothing parameter = %s, rms error = %0.3f'
        % (sbest, rms))
    plt.plot(xi, upperbound, 'red')
    plt.plot(xi, lowerbound, 'red')

    #figure.canvas.manager.set_window_title('LOWESS with residual autocorrelation')
    plt.show()
#@+node:tom.20211210160855.10: ** test_lowess_adaptive_ac
@self_printer
def test_lowess_adaptive_ac(func=None):
    '''Test Lowess Autocorrelation Adaptive Fit - lowessAdaptiveAC()'''

    N = 200
    if not func:
        func = lambda z: math.sin(z)*math.exp(-.2*z)
    x = [0.05*i for i in range(0, N)]
    y = [func(z) + 0.25*random.uniform(-.5, .5) for z in x]
    true_y = [func(z) for z in x]

    xi, yi, span, rms, ac, upperbound, lowerbound = lowessAdaptiveAC(x, y)

    rcParams['figure.figsize'] = 12, 8

    plt.plot(x, true_y, 'black', linewidth=2)
    plt.plot(x, y, 'co', mfc='white')
    plt.plot(xi, yi, 'black', linewidth=1)
    plt.title('LOWESS Autocorrelation Adaptive - smoothing parameter = %s, rms error = %0.3f'
        % (span, rms))
    plt.plot(xi, upperbound, 'red')
    plt.plot(xi, lowerbound, 'red')

    plt.title('LOWESS Autocorrelation Adaptive  span %s, autocorr %0.3f, rms %0.3f'
        % (span, ac, rms))

    figure = gcf()
    #figure.canvas.manager.window.wm_geometry('+500+25')
    figure.set_size_inches((8, 6))
    figure.canvas.manager.set_window_title('Adaptive LOWESS with residual autocorrelation')
    plt.show()
#@+node:tom.20211210160855.11: ** lstsqr
@self_printer
def lstsqr():
    'Test Linear Least Squares'
    # pylint: disable = too-many-locals
    x = range(30)
    y_truth = x[:]

    REPS = 50
    SIGMA = 10.

    rcParams['figure.figsize'] = 14, 12
    eps_avg = []

    for rep in range(REPS):
        y = [yt + random.uniform(-SIGMA, SIGMA) for yt in y_truth]
        yf, mean, rms, r, upper, lower = leastsqr(x, y)
        plt.plot(x, yf, 'gray', linewidth=1, alpha=0.3)
        eps = [_upper - _fit for _upper, _fit in zip(upper, yf)]
        if not eps_avg:
            eps_avg = eps
        else:
            _temp = []
            for _prev, _eps in zip(eps_avg, eps):
                _temp.append(_prev + _eps)
            eps_avg = _temp

    eps2_avg = [_eps/REPS for _eps in eps_avg]
    upper_avg = [_y + _eps2 for _y, _eps2 in zip(y_truth, eps2_avg)]
    lower_avg = [_y - _eps2 for _y, _eps2 in zip(y_truth, eps2_avg)]

    plt.plot(x, upper_avg, 'gray', linewidth=1)
    plt.plot(x, lower_avg, 'gray', linewidth=1)
    plt.plot(x, y_truth, linewidth=3, label='Truth', color='black')

    plt.plot(x, y, 'ro', label='Data for Fitting Example')
    plt.plot(x, yf, 'blue', linewidth=2, label='Example Fitted Line')

    factor = 2*SIGMA / (REPS-2)**.5
    sig_upper = [_y + factor for _y in y_truth]
    sig_lower = [_y - factor for _y in y_truth]
    plt.plot(x, sig_upper, 'black', linewidth=2.5)
    plt.plot(x, sig_lower, 'black', linewidth=2.5)

    plt.title('Least Squares Fit,  r=%0.3f' % r)
    plt.legend()

    axes = gca()
    axes.fill_between(x, upper_avg, lower_avg, facecolor='gray', alpha=0.2)

    figure = gcf()
    figure.canvas.manager.window.wm_geometry('+600+50')
    figure.canvas.manager.set_window_title('Linear Least Squares')

    plt.show()
#@+node:tom.20211210160855.12: ** lowess2_mse
@self_printer
def lowess2_mse(func=None):
    """Test LOWESS Adaptive Smoother: MSE with Roughness Penalty"""
    # pylint: disable = too-many-locals

    N = 200
    if not func:
        func = lambda z: math.sin(z)*math.exp(-.2*z) + \
            0.25*random.uniform(-.5, .5)
    x = [0.05*i for i in range(0, N)]
    y = [func(z) for z in x]

    smooth = (3, 5, 10, 15, 20, 25, 30, 40, 60, 80)
    mse = []
    rough = []
    for s in (s1 for s1 in smooth if s1 <= N):
        xi, yi, r, upperbound, lowerbound = lowess2(x, y, s, True)
        mse.append(r)

        xp, dy = deriv(xi, yi)
        xpp, ddy = deriv(xp, dy)
        roughness = 0
        delx = (max(xpp) - min(xpp)) / len(xpp) # mean spacing
        for i in range(len(xpp)):
            roughness += delx * sqr(ddy[i])
        rough.append(roughness)

    mean_rough = 0
    for i in rough:
        mean_rough += i
    mean_rough = mean_rough / len(rough)

    mean_mse = 0
    for i in mse:
        mean_mse += i
    mean_mse = mean_mse / len(mse)

    rough_scale_factor = mean_mse / mean_rough

    penalty = []
    weight = .1
    for i, _ in enumerate(mse):
        penalty.append(mse[i] + rough[i] * rough_scale_factor * weight)

    print ('Span\tMSE\tRough\tPenalty')
    for i, _ in enumerate(smooth):
        #print ('%0.3f\t%0.3f\t%0.2f\t%0.3f' \)
            #% (smooth[i], mse[i], rough[i], penalty[i])
        print ('{:.3f}\t{:.3f}\t{:.2f}\t{:.3f}'.format(smooth[i], mse[i], rough[i], penalty[i]))

    bestindex = penalty.index( min(penalty))
    best = smooth[bestindex]
    print ( '\nBest')
    print ( 'Span\tMSE\tRough\tPenalty')
    print ( '%s\t%0.3f\t%0.3f\t%0.3f' % \
        (best, mse[bestindex], rough[bestindex], penalty[bestindex]))
    print()

    xi, yi = lowess(x, y, best, False)

    rcParams['figure.figsize'] = 12, 10
    plt.subplot(2, 1, 2)
    plt.plot(xi, y, 'bo')
    plt.plot(xi, yi, 'b')
    plt.title('LOWESS Adaptive Smooth For Least Roughness - Span %s, MSE %0.3f' % \
                (best, mse[bestindex]))

    figure = gcf()
    figure.canvas.manager.window.wm_geometry('+600+50')
    figure.canvas.manager.set_window_title('LOWESS Adaptive Smooth using Lowess/MSE')

    plt.show()
#@+node:tom.20211210160855.13: ** test_adaptive_lowess
@self_printer
def test_adaptive_lowess(w):
    'Test lowessAdaptive()'
    N = 200
    func = lambda z: math.sin(z)*math.exp(-.2*z)
    x = [0.05*i for i in range(0, N)]
    true_y = [func(z) for z in x]
    y = [_y + 0.25*random.uniform(-.5, .5) for _y in true_y]

    weight = float(w)
    xf, yf, span, mse, upperbound, lowerbound = lowessAdaptive(x, y, weight)
    print ('Best Span: %s, weight param: %s' % (span, w))

    rcParams['figure.figsize'] = 12, 8
    rcParams['figure.facecolor']= 'lightgrey'

    plt.plot(x, true_y, 'black', linewidth=2)
    plt.plot(x, y, 'co', mfc='white')
    plt.plot(xf, yf, 'black', linewidth=1)
    plt.title('LOWESS Autocorrelation Adaptive - smoothing span = %s, rms error = %0.3f'
        % (span, mse**0.5))
    plt.plot(xf, upperbound, 'red')
    plt.plot(xf, lowerbound, 'red')

    ax = gca()
    ax.fill_between(xf, upperbound, lowerbound, facecolor='red', alpha=0.1)


    figure = gcf()
    #figure.canvas.manager.window.wm_geometry('+500+25')
    figure.canvas.manager.set_window_title('LOWESS Linear Adaptive Smoothing')

    plt.show()

#@+node:tom.20211210160855.14: ** lowess_smooth_quad
@self_printer
def lowess_smooth_quad():
    'Test LOWESS Quadratic Smoother'

    N = 200
    x = [0.05*i for i in range(0, N)]
    true_y = [math.sin(z)*math.exp(-.2*z) for z in x]
    y = [_y + random.gauss(0, .2) for _y in true_y]

    rcParams['figure.figsize'] = 12, 9
    plt.style.use(STYLE)

    smooths = 10, 15, 20, 30, 45, 60
    for s in smooths:
        xs, ys, mse, upperbound, lowerbound = lowess2Quad(x, y, s)
        plt.plot(x, ys, 'blue', linewidth=1)

    plt.title('Smoothing with LOWESS Quadratic - smoothing parameter = %s, mse = %0.3f'
            % (s, mse), fontsize=13)
    plt.plot(x, y, 'wo', mew=.2, mec='black')
    plt.plot(x, true_y, 'black', linewidth=2)
    plt.plot(x, upperbound, 'gray', linewidth=1)
    plt.plot(x, lowerbound, 'gray', linewidth=1)
    ax = gca()
    ax.fill_between(x, upperbound, lowerbound, facecolor='blue', alpha=0.1)

    figure = gcf()
    #figure.canvas.manager.window.wm_geometry('+500+25')
    figure.set_size_inches((8, 6))
    figure.canvas.manager.set_window_title('LOWESS Quadratic Smoothing')

    plt.show()

#@+node:tom.20211210160855.15: ** slope_var
@self_printer
def slope_var():
    """Calculate mean and standard deviation of least-square slope."""
    # pylint: disable = too-many-locals

    SLOPE = 1.0
    SAMPLES = 100
    SIGMA = 1.0
    N = 100 # number of points in any one data set

    A = []  # Holds slope values

    # x will range from 0 to 1
    # y data will be the gaussian noise added to a ramp
    # with slope SLOPE

    for i in range(SAMPLES):
        _xdata, _ydata = gaussian_vals(0.0, SIGMA, N)
        _xdata = [1.0*x/N for x in _xdata]
        _ydata = [_ydata[i] + SLOPE*_xdata[i] for i in range(len(_xdata))]

        Sx = 0.0 # sum of x
        Sy = 0.0 # sum of y
        Sxy = 0.0 # sum of xy
        Sxx = 0.0 # sum of xx
        Syy = 0.0 # sum of yy

        for j, _ in enumerate(_xdata):
            xtemp = _xdata[j]
            ytemp = _ydata[j]
            Sx = Sx + xtemp
            Sy = Sy + ytemp
            Sxy = Sxy + xtemp * ytemp
            Sxx = Sxx + xtemp**2
            Syy = Syy + ytemp**2

        # y = ax + b for linear fit
        a = (N * Sxy - Sx*Sy)/(N * Sxx - sqr(Sx))
        #b = (Sy - a*Sx)/N
        A.append(a)

    a_mean = sum(A) / SAMPLES
    a_var = sum([(z - a_mean)**2 for z in A]) / (SAMPLES-1)
    a_sig = a_var ** 0.5

    # Wikipedia formula for variance of slope
    # https://en.wikipedia.org/wiki/Simple_linear_regression#Numerical_properties
    # var = var(y) / sum((x - xmean)^2)
    xmean = sum(_xdata) / N
    xsqr = sum([(z - xmean)**2 for z in _xdata])
    var_wiki = SIGMA**2 / xsqr
    sig_wiki = var_wiki ** 0.5

    if a_sig < 0.01:
        sd_str = '%0.2e' % a_sig
    else:
        sd_str = '%0.3f' % a_sig
    print ('mean: %0.3f   s.d.: %s    wikipedia formula s.d.: %0.3f' % (a_mean, sd_str, sig_wiki))

    for k, _ in enumerate(A):
        a = A[k]
        plt.plot(k+1, a, 'bo')
    plt.plot([0,SAMPLES], [a_mean, a_mean], 'black', linewidth=2)
    plt.plot([0, SAMPLES], [a_mean+a_sig, a_mean+a_sig], 'gray')
    plt.plot([0, SAMPLES], [a_mean-a_sig, a_mean-a_sig], 'gray')
    plt.title('Fitted Slope for Data Sigma = %0.2f, Data Length = %s' % (SIGMA, N))

    figure = gcf()
    #figure.canvas.manager.window.wm_geometry('+600+50')
    figure.set_size_inches((8, 6))
    figure.canvas.manager.set_window_title('Least Squares Slopes')

    plt.show()
#@+node:tom.20211210160855.16: ** test_thiel
@self_printer
def test_thiel():
    N = 50
    DELTA = 1.
    MU = 0
    SIGMA = 2

    XDATA = [x*DELTA for x in range(0,N)]
    YDATA = [x + gauss(MU, SIGMA) for x in XDATA]
    x1 = int(N//4)
    x2 = int(N - x1)
    YDATA[x1] = YDATA[x1] + 10*SIGMA
    YDATA[x2] = YDATA[x2] + 15*SIGMA

    fitted, slope, intercept, sd = thiel_sen(XDATA, YDATA)

    plt.plot(XDATA, YDATA, 'gray')
    plt.plot(XDATA, fitted)
    plt.title('Thiel-Sen Robust Fitted Line')
    plt.show()

#@+node:tom.20211210160855.17: ** test_lowess_devs
@self_printer
def test_lowess_devs():
    N = 50
    DELTA = 1.
    MU = 0
    SIGMA = 2
    SMOOTHZONE=10

    XDATA = [x*DELTA for x in range(0,N)]
    YBASE = [N*(x/N)**2 for x in XDATA]
    YDATA = [y + gauss(MU, SIGMA) for y in YBASE]

    xi, fitted, mse, upperbound, lowerbound = lowess2(XDATA, YDATA, SMOOTHZONE, False)

    var = sum([(_y - _yfit)**2 for _y, _yfit in zip(YDATA,YBASE)]) / (N-1)
    sd = var**0.5
    print ('routine-estimated mse: %0.3g   actual sd : %0.3g' \
            % (mse, sd))

    err_bounds_width = 0.5*sum([_upper - _lower for \
            _upper, _lower in zip(upperbound, lowerbound)]) / N
    print ('mean half-width of error band: %0.3g' % (err_bounds_width))

    plt.plot(XDATA, YDATA, 'gray')
    plt.plot(XDATA, fitted, 'blue')
    plt.plot(XDATA, YBASE, 'black', linewidth=2)
    plt.plot(XDATA, upperbound, 'lightgrey')
    plt.plot(XDATA, lowerbound, 'lightgrey')

    axes = gca()
    axes.fill_between(XDATA, upperbound, lowerbound, facecolor='lightgrey', alpha=0.2)

    plt.title('Lowess2 Smooth')
    plt.show()
#@+node:tom.20211210160855.18: ** stdErrOfFit
@self_printer
def stdErrOfFit():
    """Test the standard error of a lowess fit.
  Estimated SE -- Standard error of fitted point relative to average
                  of the fitted points at mid-span.
  Actual SE --    Standard error calculated using reported fitted points
                  and the actual (before noise) data point at mid-span.
  avg reported se -- Average of standard error as returned by LOWESS.
  """
    # pylint: disable = too-many-locals

    N = 150
    DELTA = 1.
    MU = 0
    SIGMA = 30
    SMOOTHZONE=13

    XDATA = [x*DELTA for x in range(0,N)]
    YBASE = [N*(x/N)**3 for x in XDATA]

    REPS = 50
    fits = []
    reported_se = []
    # Fitted value in center of span
    fit_index = N/2
    for rep in range(REPS):
        YDATA = [y + gauss(MU, SIGMA) for y in YBASE]
        xi, fitted, mse, upperbound, lowerbound = lowess2(XDATA, YDATA, SMOOTHZONE, False)

        yfit = fitted[fit_index]
        fits.append(yfit)
        reported_se.append(mse)
        plt.plot(XDATA, fitted, 'gray', alpha=0.3)

    mean_fitted = sum(fits) / REPS
    _actual = YBASE[fit_index]
    var_fitted_est = sum([(_fitted - mean_fitted)**2 for _fitted in fits]) / (REPS - 1)
    var_fitted_true = sum([(_fitted - _actual)**2
            for _fitted in fits]) / (REPS - 1)
    se_est = var_fitted_est**0.5
    se_true = var_fitted_true**0.5
    avg_reported_se = sum(reported_se) / REPS

    print ('Estimated SE: {:.3g}  Actual SE: %{:3g}   avg reported se: {:.3g}'.format(se_est, se_true, avg_reported_se))

    se_bounds_upper = [_y + 2*avg_reported_se for _y in YBASE]
    se_bounds_lower = [_y - 2*avg_reported_se for _y in YBASE]

    plt.plot(XDATA, YBASE, 'black', linewidth=3, label='Ground Truth')
    plt.plot(XDATA, se_bounds_upper, 'black', label='2-sigma s.e. error bounds')
    plt.plot(XDATA, se_bounds_lower, 'black')
    plt.plot(XDATA, YDATA, 'red', label='Data for Smoothing Example')
    plt.plot(XDATA, fitted, 'blue', linewidth=1.7, label='One Example of a LOWESS Smooth')

    axes = gca()
    axes.fill_between(XDATA, se_bounds_upper, se_bounds_lower, facecolor='lightgrey', alpha=0.2)

    legend = plt.legend(loc='upper left', title='Plots')
    legend.get_title().set_fontsize('x-large')

    plt.title('Standard Error of LOWESS Fit for Smoothing Width = %s, Noise Sigma = %s'\
                % (SMOOTHZONE, SIGMA))
    plt.show()
#@+node:tom.20211210160855.19: ** test_moving_median
@self_printer
def test_moving_median():
    """Test moving median smoothing."""

    N = 50
    DELTA = 1.
    MU = 0
    SIGMA = 2
    SMOOTHZONE= 7

    XDATA = [x*DELTA for x in range(0,N)]
    YBASE = [N*(x/N)**2 for x in XDATA]
    YDATA = [y + 2. * gauss(MU, SIGMA) for y in YBASE]

    xdata, smoothed = moving_median(XDATA, YDATA, SMOOTHZONE)

    assert len(xdata) == len(smoothed), f'{len(xdata)} != {len(smoothed)}'

    plt.style.use(STYLE)
    plt.plot(XDATA, YDATA, 'gray')
    plt.plot(xdata, smoothed)
    plt.title('Moving Median Smoothing')
    plt.show()

# ========================================================

#@+node:tom.20220802121052.1: ** test_lowess_weights
@self_printer
def test_lowess_weights(width = 10):
    """Plot the Lowess weighting curve."""
    wts = WtStats()
    wts.MakeGaussianWeights(width)

    rcParams['figure.figsize'] = 7, 6
    rcParams['figure.facecolor']= 'lightgrey'
    #plt.style.use(STYLE)


    plt.plot(wts.weights, 'o', mfc='cyan', mec = 'black')
    plt.ylim(bottom = 0)
    plt.xlabel('Point Number')
    plt.ylabel('Weight')
    plt.title(f'LOWESS Weights for Window Width = {width}')
    plt.show()
#@+node:tom.20220802121006.1: ** main
Tests = (#lstsqr,
         #cspline_fit,
         #spline_smooth,
         #lowess_smooth,
         #lowess2_smooth,
         #lowess1_autocorr,
         #lowess2_mse,
         #lowess_smooth_quad,
         #lambda w=.5: test_adaptive_lowess(w),
         #test_lowess_adaptive_ac,
         #slope_var,
         #test_thiel,
         #test_lowess_devs,
         #stdErrOfFit,
         #test_moving_median,
         lambda w = 10: test_lowess_weights(w),
        )

if __name__ == '__main__':
    for t in Tests:
        t()
#@-others
#@@language python
#@@tabwidth -4

#@-leo
