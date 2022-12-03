#@+leo-ver=5-thin
#@+node:tom.20220903150123.1: * @file correl1.py
"""Correlate [X] with [Y] datasets.

[X] contains the result. [Y] is unchanged.

The result is normalized so that the autocorrelation of each
of the datasets would have a maximum value of 1.0.
"""

import numpy as np
from AbstractPlotMgr import MAIN, BUFFER
from .require_datasets import has_main_buffer

BUTTON_DEF  = ('Correlate (1)', 'correl-experimental', ' An experimental Correlation of X with Y datasets')
OVERRIDE = False
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main_buffer(plotmgr):
        return

    lab = plotmgr.stack[MAIN].figurelabel.strip() or ''
    lab1 = plotmgr.stack[BUFFER].figurelabel.strip() or ''

    # Correlate shorter with longer
    main_shorter = len(plotmgr.stack[MAIN].xdata) <= len(plotmgr.stack[BUFFER].xdata)
    if main_shorter:
        d1= plotmgr.stack[MAIN]
        d2 = plotmgr.stack[BUFFER]
    else:
        d1 = plotmgr.stack[BUFFER]
        d2 = plotmgr.stack[MAIN]

    # Calculate normalization factors
    d1sqr = [z**2 for z in d1.ydata]
    d2sqr = [z**2 for z in d2.ydata]
    norm1, norm2  = sum(d1sqr), sum(d2sqr)
    norm = 1./(norm1 * norm2)**0.5

    correlated = np.correlate(d1.ydata, d2.ydata, mode = 'full')
    correlated = [z * norm for z in correlated]
    dm = plotmgr.stack[MAIN]
    dm.ydata = correlated

    delta = (float(d2.xdata[-1] - d2.xdata[0])) / (len(d2.xdata) - 1)
    start = d2.xdata[0]
    dm.xdata = [start + i * delta for i in range(len(dm.ydata))]

    #@+others
    #@+node:tom.20220903150123.3: ** Create Title
    if lab:
        dm.figurelabel = f'[exp]Correlation of {lab}'
        if lab1:
            dm.figurelabel += f' with {lab1}'
    else:
        dm.figurelabel = '[exp]Correlation'

    if len(dm.figurelabel) > 90:
        dm.figurelabel = dm.figurelabel[:90] + '...'

    #@-others

    plotmgr.plot()
#@-leo
