#@+leo-ver=5-thin
#@+node:tom.20221127125345.1: * @file debug_lowess.py
from experimental.debug_lowess import localLowess
from AbstractPlotMgr import MAIN
from Dataset import Dataset
from stats import pearson
from entry import GetSingleInt
from .require_datasets import has_main

BUTTON_DEF  = ('Debug LOWESS', 'debug-lowess',
               '(Debug) Fit [X] Data With Linear LOWESS Fit')
OVERRIDE = False
plotmgr = None

def proc():
    if not has_main(plotmgr):
        return

    _id = 'debug-lowess'
    width = plotmgr.parmsaver.get(_id, 21)
    dia = GetSingleInt(plotmgr.root, 'LOWESS',
                         'Smoothing Width', width)
    if dia.result is None: return
    plotmgr.parmsaver[_id] = width = dia.result

    _ds = plotmgr.stack[MAIN]
    if _ds.isNumpyArray(_ds.xdata):
        _x = _ds.xdata.tolist()
    else:
        _x = _ds.xdata
    if _ds.isNumpyArray(_ds.ydata):
        _y = _ds.ydata.tolist()
    else:
        _y = _ds.ydata

    x, newy, rms, upperlimit, lowerlimit, fliers = \
                    localLowess(_x, _y, width)
    _ds.ydata = newy

    lab = plotmgr.stack[MAIN].figurelabel or ''
    if lab:
        lab = f'LOWESS ({width}) Smooth of {lab}'
    else:
        lab = f'LOWESS ({width}) Smooth'
    _ds.figurelabel = lab

    lower = Dataset(_x, lowerlimit)
    upper = Dataset(_x, upperlimit)
    _ds.errorBands = [upper, lower]

    # correlation coefficient
    r = pearson(newy[1:], newy[:-2])

    plotmgr.plot()

    has_fliers = len(fliers) > 0
    out_list = ''
    if has_fliers:
        # for x, y in fliers:
            # plotmgr.timehack(x)
        out_x = [f'{x:0.3f}'  for x, y in fliers]
        out_list = ', '.join(out_x)
    outliers = f', outliers: [{out_list}]' if has_fliers else ''
    plotmgr.announce(f'Mean standard error: {rms:0.3f}, r={r:0.3f}{outliers}')
#@-leo
