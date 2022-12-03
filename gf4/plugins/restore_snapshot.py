#@+leo-ver=5-thin
#@+node:tom.20221104194114.1: * @file restore_snapshot.py
"""Restore graph image and dataset stack."""

BUTTON_DEF = ('Restore\nSnapshot', 'get-snapshot', 'Restore saved state of the plot')
OWNER_GROUP = 'PLOT_BUTTONS'
OVERRIDE = True

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    have_snapshot = hasattr(plotmgr, 'snapshot')
    if not (have_snapshot and plotmgr.snapshot):
        plotmgr.announce('No snapshot saved')
        plotmgr.flashit()
        return

    bitmap, stack = plotmgr.snapshot
    fig = plotmgr.figure
    canvas = fig.canvas
    canvas.restore_region(bitmap)
    canvas.blit(fig.bbox)
    plotmgr.stack = stack

#@-leo
