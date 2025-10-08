#@+leo-ver=5-thin
#@+node:tom.20220905122752.1: * @file find_peak.py
"""Find a peak within the span denoted by dragging the mouse.

X-axis points must be ordered. The peak will be the point
with the highest value in the span. The peak will be marked
with a vertical marker.
"""

from numpy import searchsorted, argmax
from AbstractPlotMgr import MAIN
from .require_datasets import has_main

BUTTON_DEF  = ('Find Peak', 'find-peak', 'Find the peak near the given x-axis location. Drag mouse across peak after clicking this button.')
OVERRIDE = False

# plotmgr will have been injected into the module by the time this is called
plotmgr = None  # Suppress pyflake complaints

def getSpan(xmin, xmax):
    _ds = plotmgr.stack[MAIN]
    _x = _ds.xdata  # Might be a numpy nd array.
    _y = _ds.ydata  # Might be a numpy nd array.

    span = (xmin, xmax)
    start, end = searchsorted(_x, span)
    segment = _y[start:end]
    if len(segment) == 0:
        plotmgr.announce(f'Computed improper bounds: ){start:0.4f}, {end:0.4f}')
        plotmgr.flashit()
        return

    peak = max(segment)
    peak_index = start + argmax(segment)
    x_peak = _x[peak_index]
    # Might have max at end of segment - if so, it's not a peak
    if (_y[peak_index - 1] > peak) or (_y[peak_index + 1] > peak):
        plotmgr.announce(f'No peak found in ({_x[start]:0.4f}, {_x[end]:0.4f})')
        return

    plotmgr.timehack(x_peak)
    plotmgr.announce(
        f'Peak: {peak:0.4f} at {x_peak:0.4f})')

# All plugins must define a proc()
def proc():
    if not has_main(plotmgr):
        return

    plotmgr.createSpanSelection(getSpan)
    plotmgr.announce('Select span with mouse ...')

#@-leo
