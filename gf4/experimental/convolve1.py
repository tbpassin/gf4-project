#@+leo-ver=5-thin
#@+node:tom.20220831132228.1: * @file convolve1.py
"""Convolve [X] with [Y] datasets.  
[X] contains the result. [Y] is unchanged.

If one dataset is shorter than the other, their order is reversed
so that the arguments d1, d2 in the calculation of convolve(d1, d2)
are always in the order of <shortest>, <longest>.
"""

import numpy as np
from AbstractPlotMgr import MAIN, BUFFER
from .require_datasets import has_main_buffer

BUTTON_DEF  = ('Convolve (1)', 'convolve-experimental', ' An experimental Convolve X with Y datasets')
OVERRIDE = False
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main_buffer(plotmgr):
        return

    lab_main = plotmgr.stack[MAIN].figurelabel.strip() or ''
    lab_buff = plotmgr.stack[BUFFER].figurelabel.strip() or ''

    # Convolve shorter with longer - re-order if necessary
    main_shorter = len(plotmgr.stack[MAIN].xdata) <= len(plotmgr.stack[BUFFER].xdata)
    if main_shorter:
        d1 = plotmgr.stack[MAIN]
        d2 = plotmgr.stack[BUFFER]
    else:
        d1 = plotmgr.stack[BUFFER]
        d2 = plotmgr.stack[MAIN]

    convolved = np.convolve(d1.ydata, d2.ydata, mode = 'full')

    dm = plotmgr.stack[MAIN]
    dm.ydata = convolved
    delta = (float(d2.xdata[-1] - d2.xdata[0])) / (len(d2.xdata) - 1)
    start = d2.xdata[0]
    dm.xdata = [start + i * delta for i in range(len(dm.ydata))]

    #@+others
    #@+node:tom.20220831173009.1: ** Create Title
    if lab_main:
        dm.figurelabel = f'[exp]Convolution of {lab_main}'
        if lab_buff:
            dm.figurelabel += f' with {lab_buff}'
    else:
        dm.figurelabel = '[exp]Convolution'

    if len(dm.figurelabel) > 110:
        dm.figurelabel = dm.figurelabel[:110] + '...'
    #@-others

    plotmgr.plot()
#@-leo
