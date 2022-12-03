#@+leo-ver=5-thin
#@+node:tom.20221112235319.1: * @file norm_cdf.py
"""Given a sequence of x, y values, compute a normal CDF.

The CDF will be the CDF of a normal distribution with mean,
standard deviation to match the data values.  The result
will have the same number of points as the input data.
"""

from statistics import mean, stdev
from curve_generators import generateGaussianCdf
from Dataset import Dataset
from AbstractPlotMgr import MAIN
from .require_datasets import has_main

BUTTON_DEF  = ('Normal CDF (1)', 'normal-cdf',
               'Fit a Normal CDF to [X] Data')
OVERRIDE = False
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    dm = plotmgr.stack[MAIN]
    y = dm.ydata
    x = dm.xdata
    avg = mean(y)
    std = stdev(y)
    n = len(x)
    lab = dm.figurelabel

    vals, probs = generateGaussianCdf(n, avg, std)
    plotmgr.stack[MAIN] = Dataset(vals, probs)

    figurelabel = 'Normal CDF'
    if lab:
        figurelabel += f' of {lab}'

    if len(figurelabel) > 90:
        figurelabel = figurelabel[:90] + '...'
    plotmgr.stack[MAIN].figurelabel = figurelabel
    plotmgr.stack[MAIN].yaxislabel = 'Cumulative Normal Probability'

    plotmgr.plot()
#@-leo
