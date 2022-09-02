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

    convolved = np.convolve(d1.ydata, d2.ydata, mode = 'full')
    dm = plotmgr.stack[MAIN]
    dm.ydata = convolved

    #@+others
    #@+node:tom.20220831172914.1: ** Adjust Length
    # Make new MAIN x data the same length as the new y data
    new_len = len(convolved)
    old_x = dm.xdata
    old_len = len(old_x)
    orig_len = len(plotmgr.stack[BUFFER].ydata)
    delta = old_x[1] - old_x[0]
    dm.xdata = [old_x[0] + i * delta for i in range(new_len)]


    if new_len > orig_len:
        # Trim excess points to the left and right
        offset = int(old_len / 2)
        dm.xdata = dm.xdata[offset:]
        dm.ydata = dm.ydata[offset:]
        dm.xdata = dm.xdata[:orig_len]
        dm.ydata = dm.ydata[:orig_len]

    #@+node:tom.20220831173009.1: ** Create Title
    if lab:
        dm.figurelabel = f'[override]Convolution of {lab}'
        if lab1:
            dm.figurelabel += f' with {lab1}'
    else:
        dm.figurelabel = '[override]Convolution'

    dm.figurelabel = dm.figurelabel[:50] + '...'
    #@-others

    plotmgr.plot()
#@-leo
