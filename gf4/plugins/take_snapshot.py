#@+leo-ver=5-thin
#@+node:tom.20221104193114.1: * @file take_snapshot.py
"""Capture the current graph and the dataset stack for restoration later."""

from .require_datasets import has_main

BUTTON_DEF = ('Snapshot', 'snapshot', 'Save state of the plot')
OWNER_GROUP = 'PLOT_BUTTONS'
OVERRIDE = True

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    fig = plotmgr.figure
    bitmap = fig.canvas.copy_from_bbox(fig.bbox)
    plotmgr.snapshot = bitmap, plotmgr.stack[:]

    plotmgr.announce('Saved snapshot')
    plotmgr.fadeit()
#@-leo
