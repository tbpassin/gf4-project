#@+leo-ver=5-thin
#@+node:tom.20251030132231.1: * @file extend_data.py
"""Extend data at each end by N points.

The extension value will be the average of the last k
points at either end.  Data is assumed to be equally spaced.

If N is negative, clip that number of points from each end.
"""
from AbstractPlotMgr import MAIN
from .require_datasets import has_main
from entry import GetSingleInt

BUTTON_DEF  = ('Extend/Trim', 'extend-data',
               'Extend or trim points of [X] at each end. Negative = trim. Extension uses average of first or last k values.')
OVERRIDE = False
last_extend = 0
KAVG = 5
plotmgr = None  # Suppress pyflake complaints

# plotmgr will have been injected into the module by the time this is called
def proc():
    global last_extend
    if not has_main(plotmgr):
        return
    dm = plotmgr.stack[MAIN]

    dia = GetSingleInt(plotmgr.root, 'Extend/Trim Each End by Number Of Points',
                       'Number', last_extend)
    # result will be in the extend variable>
    #@+<< get extension length >>
    #@+node:tom.20251030134130.1: ** << get extension length >>
    if dia.result is None: return
    last_extend = extend = dia.result
    #@-<< get extension length >>

    #@+<< extend data >>
    #@+node:tom.20251030142735.1: ** << extend data >>
    # Extend data on each end or trim for negative extend
    xdata, ydata = dm.xdata, dm.ydata
    if extend < 0:
        abs_extend = -extend
        dm.xdata = xdata[abs_extend:extend]
        dm.ydata = ydata[abs_extend:extend]
    else:
        delta = xdata[1] - xdata[0]
        avg_low = sum(ydata[:KAVG]) / KAVG
        avg_hi = sum(ydata[-KAVG:]) / KAVG

        for _ in range(extend):
            x0 = xdata[0]
            xdata.insert(0, x0 - delta)
            ydata.insert(0, avg_low)

        for _ in range(extend):
            xh = xdata[-1]
            xdata += [xh + delta]
            ydata += [avg_hi]
    #@-<< extend data >>
    #@+<< update figure label >>
    #@+node:tom.20251030142437.1: ** << update figure label >>
    lab = dm.figurelabel
    if extend > 0:
        figurelabel = f'{extend}-point Extensions'
        if lab:
            figurelabel += f' to {lab}'
    else:
        figurelabel = f'{-extend}-point Trimmed'
        if lab:
            figurelabel += f' {lab}'

    if len(figurelabel) > 80:
        figurelabel = figurelabel[:80] + '...'

    plotmgr.stack[MAIN].figurelabel = figurelabel
    #@-<< update figure label >>

    plotmgr.plot()
#@-leo
