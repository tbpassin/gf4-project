#@+leo-ver=5-thin
#@+node:tom.20220903134519.1: * @file autocorrel1.py
"""Autocorrelation of X datases. """

import numpy as np
from AbstractPlotMgr import MAIN
from .require_datasets import needs_main

BUTTON_DEF  = ('Autocorr [1]', 'autocorrel-exp', ' An experimental Autocorrelation')
OVERRIDE = False
plotmgr = None

def proc():
    if not needs_main(plotmgr):
        return

    d1 = plotmgr.stack[MAIN]
    lab = d1.figurelabel.strip() or ''

    correlated = np.correlate(d1.ydata, d1.ydata, mode = 'full')
    d1.ydata = correlated

    #@+others
    #@+node:tom.20220903134519.2: ** Adjust Length
    # Make new MAIN x data the same length as the new y data
    new_len = len(correlated)
    old_x = d1.xdata
    old_len = len(old_x)
    delta = old_x[1] - old_x[0]

    offset = 0#int((new_len - old_len) / 2.) * delta
    d1.xdata = [old_x[0] - offset + i for i in range(new_len)]
    #@+node:tom.20220903134519.3: ** Create Title
    if lab:
        d1.figurelabel = f'[exp]Autocorrelation of {lab}'

    d1.figurelabel = d1.figurelabel[:40] + '...'
    #@-others

    plotmgr.plot()
#@-leo
