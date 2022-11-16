#@+leo-ver=5-thin
#@+node:tom.20221115225742.1: * @file local_poly_fit.py
"""Fit [X] dataset using a local-polynomial regression."""

from numpy import asarray
from localreg import localreg, rbf
from AbstractPlotMgr import MAIN
from entry import GetTwoInts
from .require_datasets import has_main

BUTTON_DEF  = ('Local Poly Fit', 'local-quad', 'Fit [X] with Local Polynomial Regression')
OVERRIDE = False
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    _id = 'local-poly-regr'
    deg, width = plotmgr.parmsaver.get(_id, (2, 10))
    dia = GetTwoInts(plotmgr.root, 'Local Polynomial Regression',
                         'Degree', 'Smoothing Width', deg, width)
    if dia.result is None: return
    plotmgr.parmsaver[_id] = deg, width = dia.result

    ds = plotmgr.stack[MAIN]
    y0 = ds.ydata
    x0 = ds.xdata
    radius =  width / 2
    lab = plotmgr.stack[MAIN].figurelabel.strip() or ''

    y1 = localreg(asarray(x0), asarray(y0), degree=deg, kernel=rbf.tricube, radius = radius)
    ds.ydata = list(y1)

    #@+others
    #@+node:tom.20221115233007.1: ** Create Title
    if lab:
        lab = f'Local Order-{deg} Polynomial Fit ({width}) of {lab}'

    if len(lab) > 110:
        lab = lab[:110] + '...'
    ds.figurelabel = lab

    #@-others
    plotmgr.plot()
#@-leo
