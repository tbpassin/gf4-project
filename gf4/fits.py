# @+leo-ver=5-thin
# @+node:tom.20211211181438.12: * @file fits.py
# @+others
# @+node:tom.20211211181438.13: ** Imports
"""Piecewise Linear and other curve fitting procedures."""
import numpy as np
import pwlf
from Dataset import Dataset
# @+node:tom.20211211181438.14: ** piecewiseLinear (fits.py)
def piecewiseLinear(x, y, num):
    """Return an optimum piece-wise 2-D linear fit. set 2 s.e. error bands.

    ARGUMENTS
    x -- (sorted) list or numpy array of independent variable values.
    y -- list or numpy array of dependent values corresponding
         to the x values.
    num -- number of segments to use for the fit.

    RETURNS
    a tuple of NumPy 1D arrays: (fitted y values, lower_error_y, upper_error_y)
    """

    fitter = pwlf.PiecewiseLinFit(x, y, False)
    fitter.fit(num)
    yHat = fitter.predict(x)
    se = np.sqrt(fitter.prediction_variance(x))

    lower = yHat - 1.96 * se
    upper = yHat + 1.96 * se

    return yHat, lower, upper

if __name__ == '__main__':
    def show(a,b):
        for i, z in enumerate(a):
            print (z, b[i])

    x = [1,2,3,4,5,6]
    y = [1.1,2.05,2.85,5.07,6.92,9.3]
    show(x, y)
    print()

    yh, x_err, y_err = piecewiseLinear(x, y, 2)

    show(x, yh)
    print(f'{len(x_err)=}, {len(y_err)=}')
# @-others
# @@language python
# @@tabwidth -4
# @-leo
