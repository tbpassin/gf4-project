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
OVERRIDE = True
OWNER_GROUP = 'DATA_PROCESSING_BUTTONS'
plotmgr = None

def proc():
    if not needs_main(plotmgr):
        return

    _ds = plotmgr.stack[MAIN]
    _x = _ds.xdata
    _y = _ds.ydata

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
    # See if coord is and exact value in the list
    if (increasing and (dia.result < _x[0] or dia.result > _x[-1])) \
        or (not increasing and (dia.result > _x[0] or dia.result < _x[-1])):
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

    start = given - SPAN
    end = given + SPAN
    segment = _y[start:end]
    peak = max(segment)
    peak_index = _y.index(peak)
    # Might have max at end of segment - if so, it's not a peak
    if (_y[peak_index - 1] > peak) or (_y[peak_index + 1] > peak):
        plotmgr.announce(f'No peak found in ({_x[start]}, {_x[end]})')
        return

    plotmgr.announce(
        f'Peak: {peak:0.4f} at {_x[peak_index]} in ({_x[start]}, {_x[end]})')
#@-leo
