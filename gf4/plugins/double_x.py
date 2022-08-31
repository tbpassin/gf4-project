#@+leo-ver=5-thin
#@+node:tom.20220830135417.1: * @file double_x.py
#@@language python
"""Developmental plugin - does nothing useful."""

from AbstractPlotMgr import MAIN, BUFFER
try:
    from .require_datasets import needs_main
except Exception as e:
    print(e)

BUTTON_DEF  = ('Double X', 'double-x', 'Double y values of the X dataset')

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not needs_main(plotmgr):
        return
    _ds = plotmgr.stack[MAIN]
    _ds.scale(2)
    plotmgr.plot()

#@-leo
