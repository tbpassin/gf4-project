#@+leo-ver=5-thin
#@+node:tom.20230104000405.1: * @file lst_sqr_extrap.py
import numpy as np
from AbstractPlotMgr import MAIN
from Dataset import Dataset
from entry import GetTwoInts
from .require_datasets import has_main
from help_cmds import HELPTEXT

BUTTON_DEF = ('Lst Sqr + Extrap', 'lst-sqr-extrap',
               'Least squares fit of [X] Data With Nth-Order Polynomial and Optional Extrapolation')
OVERRIDE = False
plotmgr = None

#@+<< helptext >>
#@+node:tom.20230106182809.1: ** << helptext >>
HELPTEXT[
    'lst-sqr-extrap',
] = """
Polynomial Fit
===============

Perform a degree-N polynomial least squares fit to the **[X]** data. The fit's
coefficients may optionally be used to extrapolate the fitted curve to the right
beyond the input data points.

The NumPy *np.polyfit* function is used.

The *Points to Extrapolate* input field is interpreted to be the number of points
to be extrapolated.  Their spacing will be the average horizontal spacing of the
**[X]** data set.  Negative numbers will be ignored.

Error bands for the fit will extend only over the span of the unfitted data.

"""
#@-<< helptext >>
#@+<< def calc_stats >>
#@+node:tom.20230104113414.1: ** << def calc_stats >>
def calc_stats(xdata, ydata, fitted_y):
    """Calculate standard error and error bands for the fitted data.
    
    RETURNS
    (upper, lower), where upper/lower are lists of the ±2 s.e. bands
    for the fitted data.
    """
    var = 0.0
    # mean = 0.0
    N = len(fitted_y)

    y_mean = 1.0 * sum(ydata) / N
    x_mean = 1.0 * sum(xdata) / N

    for ys, y in zip(ydata, fitted_y):
        var += (1.0 * ys - y) ** 2

    var = var / (N - 2)  # Variance of any one fitted point
    # rms = (var**0.5)
    se = (var / (N - 1)) ** 0.5  # std error of residuals

    # Estimated SD of slope from least-squares formula:
    # Var(slope) = (1/(N-2)) * sum(yi_fitted - yi)^2 / sum(xi - x_avg)^2
    # See https://en.wikipedia.org/wiki/Simple_linear_regression#Confidence_intervals
    y_mean = 1.0 * sum(ydata) / N
    x_mean = 1.0 * sum(xdata) / N
    # var_slope = (1.0/(N-2)) * sum([(y_fit - _y)**2 for y_fit, _y in zip(fitted_y, ydata)]) \
    #            / sum([(xi - x_mean)**2 for xi in xdata])
    # sd_slope = var_slope**0.5

    # See Wikipedia:
    # https://en.wikipedia.org/wiki/Simple_linear_regression#Confidence_intervals
    eps_2 = [(_y - _yf) ** 2 for _y, _yf in zip(ydata, fitted_y)]
    Sx2 = sum([(_xi - x_mean) ** 2 for _xi in xdata])
    var_all = [
        (1. / (N - 2)) * sum(eps_2) * (1. / N + ((_xi - x_mean) ** 2) / Sx2) \
                for _xi in xdata
    ]
    se_all = [_v ** 0.5 for _v in var_all]

    upper = [y + 2 * se for y, se in zip(fitted_y, se_all)]
    lower = [y - 2 * se for y, se in zip(fitted_y, se_all)]
    return upper, lower
#@-<< def calc_stats >>

def proc():
    if not has_main(plotmgr):
        return

    #@+<< get user params >>
    #@+node:tom.20230104115311.1: ** << get user params >>
    _id = 'lsr-sqr-extrap'
    deg, new_points = plotmgr.parmsaver.get(_id, (1, 0))
    dia = GetTwoInts(plotmgr.root, 'Local Polynomial Regression',
                         'Degree', 'Points to Extrapolate', deg, new_points)
    if dia.result is None: return
    deg, new_points = dia.result
    if new_points < 0:
        plotmgr.announce(
            'Number of Extra Points For Extrapolation Must Be >= 0, no extrapolation')
        plotmgr.flashit()

    new_points = max(0, new_points)
    plotmgr.parmsaver[_id] = deg, new_points
    #@-<< get user params >>

    _ds = plotmgr.stack[MAIN]
    xdata, ydata = _ds.xdata, _ds.ydata
    xdata_orig = xdata[:]

    coeffs = np.polyfit(xdata, ydata, deg)
    p = np.poly1d(coeffs)
    fitted_y = [p(x) for x in xdata]
    upper, lower = calc_stats(xdata, ydata, fitted_y)

    #@+others
    #@+node:tom.20230104114650.1: ** Extrapolate
    extrax = []
    if new_points > 0:
        end = xdata[-1]
        span = end - xdata[0]
        delta = span / len(xdata)  # Works for int or float values
        extrax = [end + (m + 1) * delta for m in range(new_points)]
    fitted_y.extend([p(x) for x in extrax])
    xdata.extend(extrax)
    _ds.ydata = fitted_y
    #@+node:tom.20230104114806.1: ** Re-lable
    lab = plotmgr.stack[MAIN].figurelabel or ''
    lab = f'Least Squares Polynomial Fit ({deg})'
    if lab:
        lab += f' to {lab}'
    if new_points > 0:
        lab += ' (Extrapolated)'

    _ds.figurelabel = lab

    #@-others

    upper_ds = Dataset(xdata_orig, upper)
    lower_ds = Dataset(xdata_orig, lower)
    _ds.errorBands = [upper_ds, lower_ds]

    plotmgr.plot()
    plotmgr.overplot_errorbands()
 
#@-leo
