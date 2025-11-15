#@+leo-ver=5-thin
#@+node:tom.20221101105447.1: * @file autocorrel1.py
"""Calculate autocorrelation of X.  

We want the peak of the autocorrelation to occur at x = 0.  To
get this, the data x axis needs to be renumbered to start at -N,
where N is maximum x value.

The peak is normalized to 1.0 at x-value = 0.

X contains the result.
"""

import numpy as np
from AbstractPlotMgr import MAIN
from .require_datasets import has_main

BUTTON_DEF  = ('Auto\nCorrel (1)', 'autocorrel-experimental',
               ' An experimental autocorrelation the X dataset')
OVERRIDE = False
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    lab = plotmgr.stack[MAIN].figurelabel.strip() or ''
    d1 = plotmgr.stack[MAIN]
    x, y = d1.xdata, d1.ydata

    # Shift x axis
    end = x[-1]
    x = [z - end for z in x]

    correlated = np.correlate(y, y, mode = 'full')
    norm = 1./max(correlated)
    d1.ydata = [y_ * norm for y_ in correlated]
    start = x[0]
    delta = (float(x[-1] - x[0])) / (len(x) - 1)
    d1.xdata = [start + i * delta for i in range(len(d1.ydata))]

    #@+others
    #@+node:tom.20221101105447.2: ** Create Title
    if lab:
        d1.figurelabel = f'[exp] AutoCorrelation of {lab}'
    else:
        d1.figurelabel = '[exp] AutoCorrelation'

    if len(d1.figurelabel) > 90:
        d1.figurelabel = d1.figurelabel[:90] + '...'

    #@-others

    plotmgr.plot()
#@-leo
