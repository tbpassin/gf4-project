#@+leo-ver=5-thin
#@+node:tom.20220905122752.1: * @file find_peak1.py
"""Find a peak near the specified x-axis coordinate
The peak must be smooth for this to work.
X-axis points must be ordered
"""
from matplotlib.widgets import SpanSelector
from AbstractPlotMgr import MAIN
from .require_datasets import has_main

SPAN = 10
BUTTON_DEF  = ('Find Peak1', 'find-peak-1', 'Find the peak near the given x-axis location')
OVERRIDE = False

plotmgr = None  # Suppress pyflake complaints

def onSpanSelect(xmin, xmax):
    print("Selected:", xmin, xmax, flush=True)
    plotmgr.SpanSelector = None
    plotmgr.span = (xmin, xmax)
    doSomething()

def doSomething():
    print(f'{plotmgr.span=}', flush=True)
    plotmgr.span = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    ax = plotmgr.axes

    plotmgr.SpanSelector = SpanSelector(
        ax,
        onSpanSelect,
        "horizontal", 
        useblit=True,
        interactive=False,
    )

#@+at
#     _ds = plotmgr.stack[MAIN]
#     _x = list(_ds.xdata)
#     _y = list(_ds.ydata)  # Might be a numpy nd array.
#
#     # _id = 'peakfinder'
#     # lastparm = plotmgr.parmsaver.get(_id, 0.0)
#     # dia = GetSingleFloat(plotmgr.root,
#                          # 'Find Peak Near', 'X axis coord',
#                          # lastparm)
#     # if dia.result is None: return
#     # plotmgr.parmsaver[_id] = dia.result
#
#@+at 
#     plotmgr.announce(
#         f'Peak: {peak:0.4f} at {x_peak:0.4f} in ({_x[start]:0.4f}, {_x[end]:0.4f})')
#@-leo
