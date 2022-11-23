#@+leo-ver=5-thin
#@+node:tom.20220911140747.1: * @file frechet.py
"""Calculate and display Frechet distance between X and Y curves."""

# Requires frechetdist package
try:
    from frechetdist import frdist
    frechet_ok = True
except ImportError:
    print("Need the frechetdist package - pip install frechetdist")
    frechet_ok = False

# Only create the required plugin attributes if we have the import.
# Downstream code will skip this plugin if the BUTTON_DEF is missing.
if frechet_ok:
    from AbstractPlotMgr import MAIN, BUFFER
    from .require_datasets import needs_main_buffer
    from Dataset import Dataset

    BUTTON_DEF  = ('Frechet Dist', 'frechet', 'Show Frechet distance between X and Y datasets')
    plotmgr = None  # Suppress pyflake complaints

    def proc():
        if not needs_main_buffer(plotmgr):
            return

        dsX = plotmgr.stack[MAIN]
        dsY = plotmgr.stack[BUFFER]
        if len(dsX.xdata) != len(dsY.xdata):
            msg = 'MAIN, BUFFER must have the same number of points'
            plotmgr.announce(msg)
            plotmgr.flashit()
            return

        Xx, Xy = dsX.xdata, dsX.ydata
        Yy = dsY.ydata
        x = tuple(zip(Xx, Xy))
        y = tuple(zip(Xx, Yy))

        d = frdist(x, y)

        lower = Dataset(Xx, Xy)
        lower.addConstant(-d)

        upper = Dataset(Xx, Xy)
        upper.addConstant(d)

        dsX.errorBands = []
        dsX.errorBands.append(upper)
        dsX.errorBands.append(lower)

        plotmgr.announce(f'Frechet distance: {d:0.4f}'),
#@-leo
