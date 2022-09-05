#@+leo-ver=5-thin
#@+node:tom.20220903150123.1: * @file correl1.py
"""Convolve X with Y datasets.  
X contains the result.  Y is unchanged.
"""

import numpy as np
from AbstractPlotMgr import MAIN, BUFFER
from .require_datasets import needs_main_buffer

BUTTON_DEF  = ('Correlate (1)', 'correl-experimental', ' An experimental Correlation of X with Y datasets')
OVERRIDE = False
plotmgr = None

def proc():
    if not needs_main_buffer(plotmgr):
        return

    lab = plotmgr.stack[MAIN].figurelabel.strip() or ''
    lab1 = plotmgr.stack[BUFFER].figurelabel.strip() or ''

    # Convolve shorter with longer
    main_shorter = len(plotmgr.stack[MAIN].xdata) <= len(plotmgr.stack[BUFFER].xdata)
    if main_shorter:
        d1= plotmgr.stack[MAIN]
        d2 = plotmgr.stack[BUFFER]
    else:
        d1 = plotmgr.stack[BUFFER]
        d2 = plotmgr.stack[MAIN]

    correlated = np.correlate(d1.ydata, d2.ydata, mode = 'full')
    dm = plotmgr.stack[MAIN]
    dm.ydata = correlated

    #@+others
    #@+node:tom.20220903150123.2: ** Adjust Length
    # Trim away extra points added at start and end to get full overlap
    # The original length of the shorter datasset will have been added at each end.
    old_x = d1.xdata
    old_len = len(old_x)
    new_len = len(correlated)
    correlated = correlated[old_len:]
    correlated = correlated[:-old_len]


    # Make new MAIN x data the same length as the new y data
    delta = old_x[1] - old_x[0]
    dm.xdata = [old_x[0] + i * delta for i in range(new_len)]

    #@+node:tom.20220903150123.3: ** Create Title
    if lab:
        dm.figurelabel = f'[exp]Correlation of {lab}'
        if lab1:
            dm.figurelabel += f' with {lab1}'
    else:
        dm.figurelabel = '[exp]Correlation'

    dm.figurelabel = dm.figurelabel[:40] + '...'
    #@-others

    plotmgr.plot()
#@-leo
