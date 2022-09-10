#@+leo-ver=5-thin
#@+node:tom.20220909175119.1: * @file readout.py
"""Display y value at specified point."""

from AbstractPlotMgr import MAIN
from .require_datasets import needs_main
from entry import GetSingleFloat

BUTTON_DEF  = ('Readout Y', 'readout', 'Show the y value of a specified point')
plotmgr = None  # Suppress pyflake complaints

#@+others
#@+node:tom.20220909180932.1: ** find_closest
def find_closest(value, x):
    """If value is not exactly a member of the list, return the 
    closest point.
    
    Assumes ordered points.

    ARGUMENTS
    value -- a value that should be included in the values of x.
    x -- a list.
    
    RETURNS
    the index of the closest value, else -1.
    """

    given = -1
    try:
        given = x.index(value)
    except ValueError:  # Didn't get an exact x value
        # Scan until we exceed the given x value
        increasing = x[1] >= x[0]
        foundit = False
        for i, v in enumerate(x):
            foundit = v >= value if increasing else v < value
            if foundit:
                given = i
                break
    return given
#@-others

def proc():
    if not needs_main(plotmgr):
        return

    _id = 'readout'
    lastparm = plotmgr.parmsaver.get(_id, 0.0)
    dia = GetSingleFloat(plotmgr.root,
                         'Find Peak Near', 'X axis coord', lastparm)
    if dia.result is None:
        return
    plotmgr.parmsaver[_id] = dia.result

    _ds = plotmgr.stack[MAIN]
    _x = list(_ds.xdata)
    _y = list(_ds.ydata)  # Might be a numpy nd array.

    given = find_closest(dia.result, _x)
    if given == -1:
        plotmgr.announce(f"Can't find point near X = {dia.result}")
        return

    height = _y[given]
    plotmgr.announce(
        f'Y: {height:0.4f} at X: {_x[given]:0.4f}')
#@-leo
