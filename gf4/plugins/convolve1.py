#@+leo-ver=5-thin
#@+node:tom.20220831132228.1: * @file convolve1.py
"""Convolve X with Y datasets.  
X contains the result.  Y is unchanged.
"""

import numpy as np
from AbstractPlotMgr import MAIN, BUFFER
from .require_datasets import needs_main_buffer

BUTTON_DEF  = ('Convolve (raw)', 'convolve-experimental', ' An experimental Convolve X with Y datasets')
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

    probe_x = d1.xdata[:]
    probe_len = len(probe_x)
    orig_data_len = len(d2.xdata)

    convolved = np.convolve(d1.ydata, d2.ydata, mode = 'full')

    #@+others
    #@+node:tom.20220831172914.1: ** Adjust Length
    dm = plotmgr.stack[MAIN]

    # Trim away extra points added at start and end to get full overlap
    # Half the original length of the shorter dataset will have been added at each end.
    trim = int(probe_len / 2)
    convolved = convolved[trim:]
    convolved = convolved[:orig_data_len]
    dm.ydata = convolved

    # Make new MAIN x data the same length as the new y data
    delta = d2.xdata[1] - d2.xdata[0]
    start = d2.xdata[0]
    dm.xdata = [start + i * delta for i in range(orig_data_len)]
    #@+node:tom.20220831173009.1: ** Create Title
    if lab:
        dm.figurelabel = f'[exp]Convolution of {lab}'
        if lab1:
            dm.figurelabel += f' with {lab1}'
    else:
        dm.figurelabel = '[exp]Convolution'

    dm.figurelabel = dm.figurelabel[:110] + '...'
    #@-others

    plotmgr.plot()
#@-leo
