#@+leo-ver=5-thin
#@+node:tom.20220905122752.1: * @file find_peak1.py
# Find a peak near the specified x-axis coordinate
# The peak must be smooth for this to work.
# X-axis points must be ordered

from AbstractPlotMgr import MAIN
from .require_datasets import has_main

SPAN = 10
BUTTON_DEF  = ('Find Peak1', 'find-peak-1', 'Find the peak near the given x-axis location')
# Put our command button into the "Data Processing" goup
OVERRIDE = False

plotmgr = None  # Suppress pyflake complaints

# def mouse_event(event):
    # #print('x: {} and y: {}'.format(event.xdata, event.ydata))
    # return event.xdata

# fig = plt.figure()
# cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
# canvas.mpl_disconnect(cid)

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    _ds = plotmgr.stack[MAIN]
    _x = list(_ds.xdata)
    _y = list(_ds.ydata)  # Might be a numpy nd array.

    # _id = 'peakfinder'
    # lastparm = plotmgr.parmsaver.get(_id, 0.0)
    # dia = GetSingleFloat(plotmgr.root,
                         # 'Find Peak Near', 'X axis coord',
                         # lastparm)
    # if dia.result is None: return
    # plotmgr.parmsaver[_id] = dia.result

    got_mouse = None

    def mouse_event(event):
        global got_mouse
        print('x: {} and y: {}'.format(event.xdata, event.ydata))
        got_mouse = event.xdata
        if plotmgr.after_id:
            plotmgr.root.after_cancel(plotmgr.after_id)
            plotmgr.after_id = None

    def check_mouse(obj = got_mouse):
        if obj:
            print('...... got mouse')
            return
        #plotmgr.after_id = plotmgr.root.after(500, lambda: check_mouse(obj))
        #print('----')

    cid = plotmgr.canvas.mpl_connect('button_press_event', mouse_event)

    plotmgr.after_id = None

    while not got_mouse:
        check_mouse(got_mouse)
    plotmgr.canvas.mpl_disconnect(cid)
    print('====', got_mouse)

    dia = object()
    dia.result = got_mouse
    given = None
    increasing = _x[1] > _x[0]
    #@+<< check inbounds >>
    #@+node:tom.20220905122752.2: ** << check inbounds >>
    # See if coord is and exact value in the list
    if (increasing and (dia.result < _x[0] or dia.result > _x[-1])) \
        or (not increasing and (dia.result > _x[0] or dia.result < _x[-1])):
        plotmgr.announce(f'{dia.result} is out of the range')
        plotmgr.flashit()
        return
    #@-<< check inbounds >>
    # Set given to index of starting point, if found
    #@+<< find starting point >>
    #@+node:tom.20220905122752.3: ** << find starting point >>
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


    plotmgr.announce(
        f'Peak: {peak:0.4f} at {x_peak:0.4f} in ({_x[start]:0.4f}, {_x[end]:0.4f})')
#@-leo
