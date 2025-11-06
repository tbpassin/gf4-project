#@+leo-ver=5-thin
#@+node:tom.20250928143427.1: * @file fox_autocor.py
"""Calculate the lag-1 autocorrelation of the X Dataset per method of Fox.

The data should be residuals from fitting some data, and will be zeroed
before the calculation. The calculation is explained in:
    
    "Nonparametric Simple Regression", J. Fox, Sage University, 2000.

The data in the Dataset is not changed.

Displays the result in the announciator bar, along with Pearson's
lag-1 autocorrelation.
"""

from AbstractPlotMgr import MAIN
from .require_datasets import has_main
from stats import pearson_autocorr

BUTTON_DEF  = ('Fox Auto Correl', 'fox-autocorrel',
               'Lag-1 autocorrelation of the X dataset per Fox and Pearson')
OVERRIDE = True  # Override default location.
OWNER_GROUP = 'STATS_BUTTONS'
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    d1 = plotmgr.stack[MAIN].copy()
    ydata = d1.ydata

    # Remove any DC bias
    avg = float(sum(ydata)) / len(ydata)
    d1.addConstant(-avg)

    accum = sqr = 0.
    ydata = d1.ydata
    leng = len(ydata)
    for i, y in enumerate(ydata):
        if i < leng - 1:
            accum += ydata[i+1] * y
        sqr += y**2

    ρ_fox = accum/sqr
    ρ_pearson = pearson_autocorr(ydata)
    plotmgr.announce(f"Fox: {ρ_fox:.3f}, Pearson: {ρ_pearson:.3f}")
#@-leo
