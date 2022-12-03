#@+leo-ver=5-thin
#@+node:tom.20221121191416.1: * @file poly_lowess.py
from experimental.lowess_poly import localPolyLowess
from AbstractPlotMgr import MAIN
from Dataset import Dataset
from smoother import correlationCoeff
from entry import GetTwoInts
from .require_datasets import has_main

BUTTON_DEF  = ('Poly LOWESS', 'poly-lowess',
               'Fit [X] Data With nth-Order LOWESS Fit')
OVERRIDE = False
plotmgr = None

def proc():
    if not has_main(plotmgr):
        return

    _id = 'poly-lowess'
    deg, width = plotmgr.parmsaver.get(_id, (1, 5))
    dia = GetTwoInts(plotmgr.root, 'Local Polynomial Regression',
                         'Degree', 'Smoothing Width', deg, width)
    if dia.result is None: return
    plotmgr.parmsaver[_id] = deg, width = dia.result

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
                    localPolyLowess(_x, _y, width, degree = deg)
    _ds.ydata = newy

    lab = plotmgr.stack[MAIN].figurelabel or ''
    if lab:
        lab = f'Poly-LOWESS ({deg}, {width}) Smooth of {lab}'
    else:
        lab = f'Plot-LOWESS ({deg}, {width}) Smooth'
    _ds.figurelabel = lab

    lower = Dataset()
    lower.ydata = lowerlimit
    lower.xdata = _x

    upper = Dataset()
    upper.ydata = upperlimit
    upper.xdata = _x

    # Subgraphs get stored in the errorBands list
    _ds.errorBands = []
    _ds.errorBands.append(upper)
    _ds.errorBands.append(lower)

    # correlation coefficient
    r = correlationCoeff(_y, newy)

    plotmgr.plot()

    has_fliers = len(fliers) > 0
    out_list = ''
    if has_fliers:
        # for x, y in fliers:
            # plotmgr.timehack(x)
        out_x = [f'{x}'  for x, y in fliers]
        out_list = f"({', '.join(out_x)})"
    outliers = f'{len(fliers)} outliers: {out_list}' if has_fliers else ''
    plotmgr.announce(f'RMS Deviation: {rms:0.3f}, r={r:0.3f}, {outliers}')
#@-leo
