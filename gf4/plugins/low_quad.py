#@+leo-ver=5-thin
#@+node:tom.20221120044718.1: * @file low_quad.py
"""LOWESS order-2 fit."""

from experimental.lowess_quad import localQuadLowess
from AbstractPlotMgr import MAIN
from Dataset import Dataset
from stats import pearson, pearson_autocorr
from entry import GetSingleInt
from .require_datasets import has_main


BUTTON_DEF  = ('LOWESS Quad', 'lowess-quad',
               'Fit [X] Data With Order-2 LOWESS Fit')
OVERRIDE = False
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    _ds = plotmgr.stack[MAIN]
    if _ds.isNumpyArray(_ds.xdata):
        _x = _ds.xdata.tolist()
    else:
        _x = _ds.xdata
    if _ds.isNumpyArray(_ds.ydata):
        _y = _ds.ydata.tolist()
    else:
        _y = _ds.ydata

    _id = 'lowess2Quad'
    lastparm = plotmgr.parmsaver.get(_id, 7)

    dia = GetSingleInt(plotmgr.root, 'Smoothing Width', 'Enter Integer',
                       lastparm)
    if dia.result is None: return
    plotmgr.parmsaver[_id] = dia.result

    x, newy, rms, upperlimit, lowerlimit, fliers = localQuadLowess(_x, _y,
                                                                dia.result)
    _ds.ydata = newy

    lab = plotmgr.stack[MAIN].figurelabel or ''
    if lab:
        lab = f'LOWESS Quadratic Smooth ({dia.result}) of {lab}'
    else:
        lab = f'LOWESS Quadratic Smooth ({dia.result})'
    plotmgr.stack[MAIN].figurelabel = lab

    lower = Dataset(_x, lowerlimit)
    upper = Dataset(_x, upperlimit)
    _ds.errorBands = [upper, lower]

    # correlation coefficient
    r = pearson(_y, newy)

    # Autocorrelation of residuals
    resid = [y2 - y1 for y2, y1 in zip(_y, newy)]
    resid_ac = pearson_autocorr(resid)

    plotmgr.plot()

    plotmgr.announce(f'Autocorr of residuals: {resid_ac:0.3f}, RMS Deviation: {rms:0.3f}, r:{r:0.3f}')
#@-leo
