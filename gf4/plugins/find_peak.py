#@+leo-ver=5-thin
#@+node:tom.20220904105233.1: * @file find_peak.py
# Find a peak near the specified x-axis coordinate
# The peak must be smooth for this to work.
# X-axis points must be ordered

from AbstractPlotMgr import MAIN
from .require_datasets import needs_main
from entry import GetSingleFloat

SPAN = 10
BUTTON_DEF  = ('Find Peak', 'find-peak', 'Find the peak near the given x-axis location')
# Put our command button into the "Data Processing" goup
OVERRIDE = True
OWNER_GROUP = 'DATA_PROCESSING_BUTTONS'

plotmgr = None  # Suppress pyflake complaints

def proc():
    if not needs_main(plotmgr):
        return

    _ds = plotmgr.stack[MAIN]
    _x = list(_ds.xdata)
    _y = list(_ds.ydata)  # Might be a numpy nd array.

    _id = 'peakfinder'
    lastparm = plotmgr.parmsaver.get(_id, 0.0)
    dia = GetSingleFloat(plotmgr.root,
                         'Find Peak Near', 'X axis coord',
                         lastparm)
    if dia.result is None: return
    plotmgr.parmsaver[_id] = dia.result

    given = None
    increasing = _x[1] > _x[0]
    #@+<< check inbounds >>
    #@+node:tom.20220904112303.1: ** << check inbounds >>
    if dia.result < min(_x) or dia.result > max(_x):
        plotmgr.announce(f'{dia.result} is out of the range')
        plotmgr.flashit()
        return
    #@-<< check inbounds >>
    # Set given to index of starting point, if found
    #@+<< find starting point >>
    #@+node:tom.20220904112345.1: ** << find starting point >>
    try:
        given = _x.index(dia.result)
    except ValueError:
        # this exact value is not in the list
        # Scan to get close
        for i, v in enumerate(_x):
            if increasing:
                if v > dia.result:
                    given = i
                    break
            else:
                if v < dia.result:
                    given = i
                    break

    if given is None:
        plotmgr.announce(f"Can't find {dia.result}")
        plotmgr.flashit()
        return

    #@-<< find starting point >>

    start = max(given - SPAN, 0)
    end = min(given + SPAN, len(_x))
    segment = _y[start:end]
    if not segment:
        plotmgr.announce(f'Computed improper bounds: ){start:0.4f}, {end:0.4f}')
        plotmgr.flashit()
        return

    peak = max(segment)
    peak_index = _y.index(peak)
    x_peak = _x[peak_index]
    # Might have max at end of segment - if so, it's not a peak
    if (_y[peak_index - 1] > peak) or (_y[peak_index + 1] > peak):
        plotmgr.announce(f'No peak found in ({_x[start]:0.4f}, {_x[end]:0.4f})')
        return

    plotmgr.timehack(x_peak)
    plotmgr.announce(
        f'Peak: {peak:0.4f} at {x_peak:0.4f} in ({_x[start]:0.4f}, {_x[end]:0.4f})')
#@-leo
