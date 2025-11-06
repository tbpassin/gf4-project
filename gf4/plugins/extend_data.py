#@+leo-ver=5-thin
#@+node:tom.20251030132231.1: * @file extend_data.py
"""Extend or trim data at each end by N points.

The extension value will be the average of the last k
points at either end.  Data is assumed to be equally spaced.

If N is negative, trim that number of points from each end.
"""
# pylint: disable = relative-beyond-top-level
from entry import GetSingleInt
from AbstractPlotMgr import MAIN
from .require_datasets import has_main

KAVG = 5  # Number of points at each end to average over
BUTTON_DEF  = ('Extend/Trim', 'extend-data',
               'Extend or trim points of [X] at each end. '
               'Negative = trim. Extension y values are average '
               f'of {KAVG} first or last values.')

OVERRIDE = True
OWNER_GROUP = 'CURVE_BUTTONS'

last_extend = 0  # Must be put here so next invocation will "remember" the last value.
plotmgr = None  # Suppress pyflake complaints

#@+<< def extend_data >>
#@+node:tom.20251030142735.1: ** << def extend_data >>
def extend_data(ext, ds):
    """Extend data on each end or trim for negative extend.
    
    ARGUMENTS
    ext -- an integer. Positive to extend, negative to trim.
           If not an integer, will be truncated to the nearest one. 
    ds -- a Dataset instance. Will be modified in place.
    
    Returns nothing.
    """
    xdata, ydata = ds.xdata, ds.ydata
    if ext < 0:
        abs_extend = -ext
        ds.xdata = xdata[abs_extend:ext]
        ds.ydata = ydata[abs_extend:ext]
    else:
        delta = xdata[1] - xdata[0]
        avg_low = sum(ydata[:KAVG]) / KAVG
        avg_hi = sum(ydata[-KAVG:]) / KAVG
        xdata, ydata = list(xdata), list(ydata)  #  In case of numpy ndarrays

        for _ in range(ext):
            x0 = xdata[0]
            xdata.insert(0, x0 - delta)
            ydata.insert(0, avg_low)
        for _ in range(ext):
            xh = xdata[-1]
            xdata += [xh + delta]
            ydata += [avg_hi]

        ds.xdata = xdata
        ds.ydata = ydata

#@-<< def extend_data >>

# plotmgr will have been injected into the module by the time this is called
def proc():
    global last_extend
    if not has_main(plotmgr):
        return
    dm = plotmgr.stack[MAIN]

    dia = GetSingleInt(plotmgr.root,
                       'Extend/Trim Each End by Number Of Points',
                       'Number', last_extend)

    # The length will be in the extend variable.
    #@+<< get extension length >>
    #@+node:tom.20251030134130.1: ** << get extension length >>
    if dia.result is None:
        return
    last_extend = extend = dia.result
    #@-<< get extension length >>

    extend_data(extend, dm)
    if dm.errorBands is not None:
        for ds in dm.errorBands:
            extend_data(extend, ds)

    #@+<< update figure label >>
    #@+node:tom.20251030142437.1: ** << update figure label >>
    lab = dm.figurelabel
    if extend > 0:
        figurelabel = f'{extend}-point Extensions'
        if lab:
            figurelabel += f' to {lab}'
    else:
        trim = -extend  # pylint: disable = invalid-unary-operand-type
        figurelabel = f'{trim}-point Trimmed'
        if lab:
            figurelabel += f' {lab}'

    if len(figurelabel) > 80:
        figurelabel = figurelabel[:80] + '...'

    plotmgr.stack[MAIN].figurelabel = figurelabel
    #@-<< update figure label >>

    plotmgr.plot()
#@-leo
