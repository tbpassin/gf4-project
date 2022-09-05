#@+leo-ver=5-thin
#@+node:tom.20220830135417.1: * @file double_x.py
#@@language python
"""A demo plugin - doubles the data in the X position."""

from AbstractPlotMgr import MAIN
from .require_datasets import needs_main

BUTTON_DEF  = ('Double X', 'double-x', 'Double y values of the X dataset')

# plotmgr will have been injected into the module by the time this is called
def proc():
    # Return without trying to do anything if there is no X dataset.
    # This could happen on startup.
    if not needs_main(plotmgr):
        return

    _ds = plotmgr.stack[MAIN]
    _ds.scale(2)
    plotmgr.plot()

#@-leo
