#@+leo-ver=5-thin
#@+node:tom.20221124112244.1: * @file show_sigma.py
"""Plot error bands for the mean, standard deviation of the [X] dataset.

The upper and lower error lines will be at +- 2 sigma from the mean.
"""
from statistics import mean, stdev
from AbstractPlotMgr import MAIN
from Dataset import Dataset
from stats import pearson
from .require_datasets import has_main

BUTTON_DEF  = ('Show Sigmas', 'show-sigma',
               'Show 2-sigma Error Bands Around Mean of [X]')
OVERRIDE = False
plotmgr = None

def proc():
    if not has_main(plotmgr):
        return

    ds = plotmgr.stack[MAIN]
    ydata = ds.ydata
    avg = mean(ydata)
    sigma = stdev(ydata)

    # Lag-1 autocorrelation
    shifted = ydata[1:]
    r = pearson(shifted, ydata[:-1])

    # Correct sigma for lag-1 autocorrelation
    try:
        sigma_corr = sigma / (1. - r*r) ** 0.5
    except Exception as e:
        print(e)
        sigma_corr = float("NaN")

    ydata = [avg for _ in ds.xdata]

    hi = [avg + 2. * sigma for _ in ds.xdata]
    low = [avg - 2. * sigma for _ in ds.xdata]

    upper = Dataset(ds.xdata, hi)
    lower = Dataset(ds.xdata, low)
    ds.errorBands = [upper, lower]
    ds.ydata = ydata

    plotmgr.plot()
    plotmgr.overplot_errorbands()

    plotmgr.announce(f'Mean: {avg:0.3f}, Sigma: {sigma:0.3f}, Lag-1 autocorrelation: {r:0.3f}, sigma corrected for a.c.: {sigma_corr:0.3f}')
#@-leo
