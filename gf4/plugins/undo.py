#@+leo-ver=5-thin
#@+node:tom.20221105143807.1: * @file undo.py
"""Undo last plot change."""
BUTTON_DEF = ('Undo', 'undo', 'Undo last plot change')

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not hasattr(plotmgr, 'undo_stack'):
        plotmgr.announce('No saved plot to restore')
        plotmgr.flashit()
        return

    # Restore bitmap, stack at undo_history index
    if plotmgr.undo_history < 0:
        plotmgr.announce('No more snapshots to restore')
        plotmgr.fadeit()
        return

    bitmap, stack = plotmgr.undo_stack[plotmgr.undo_history]
    fig = plotmgr.figure
    canvas = fig.canvas
    canvas.restore_region(bitmap)
    canvas.blit(fig.bbox)
    plotmgr.stack = stack

    plotmgr.undo_history -= 1

    msg = f'undid # {plotmgr.undo_history}'
    plotmgr.announce(msg)
    plotmgr.fadeit()


#@-leo
