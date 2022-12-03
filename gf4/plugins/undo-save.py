#@+leo-ver=5-thin
#@+node:tom.20221105131948.1: * @file undo-save.py
"""Store snapshot of image, stack into an undo array.

The stack must have two pointers: 
    
    head -- the index where the next undo snapshot will be stored;
    history -- the index from which the next undo/redo0 will be restored.

The history index can never move beyond the head index.
New snapshots are always added just past the history index, or at index 0
if the history index == 0.
"""
from .require_datasets import has_main

BUTTON_DEF = ('Capture Plot', 'undo-save', 'Save state of the plot in the Undo stack')

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    # Create undo array if not yet created.
    if not hasattr(plotmgr, 'undo_stack'):
        plotmgr.undo_stack = []
        plotmgr.undo_head = None
        plotmgr.undo_history = -1

    # Add snapshot
    fig = plotmgr.figure
    bitmap = fig.canvas.copy_from_bbox(fig.bbox)
    snapshot = bitmap, plotmgr.stack[:]

    if plotmgr.undo_head is None:
        plotmgr.undo_stack.append(snapshot)
        plotmgr.undo_history = 0
        plotmgr.undo_head = 1
    else:
        # The history index may have changed because of undo/redo operations
        plotmgr.undo_head = plotmgr.undo_history + 1
        plotmgr.undo_stack.insert(plotmgr.undo_head, snapshot)
        plotmgr.undo_history += 1
        plotmgr.undo_head += 1

    plotmgr.announce(f'Saved snapshot # {plotmgr.undo_head}')
    plotmgr.fadeit()
#@-leo
