#@+leo-ver=5-thin
#@+node:tom.20251114142829.1: * @file make_triangle.py
# pylint: disable = relative-beyond-top-level
from entry import GetSingleInt
from AbstractPlotMgr import MAIN
from Dataset import Dataset

BUTTON_DEF  = ('Make Triangle', 'make-triangle',
               'Generate Triangular Curve. Width must be > 2.  Will be adjusted to an odd length')

OVERRIDE = True
OWNER_GROUP = 'GENERATOR_BUTTONS'

#@+others
#@+node:tom.20251114143526.1: ** makeTriangle
def makeTriangle(plotmgr, ds):
    _id = 'makeTriangle'
    lastparm = plotmgr.parmsaver.get(_id, plotmgr.num)

    dia = GetSingleInt(plotmgr.root, 'Width', 'Points', lastparm)
    if not dia.result: return
    plotmgr.parmsaver[_id] = dia.result

    ds.xdata, ds.ydata, actual_width = generateTriangle(plotmgr.num, dia.result)
    ds.figurelabel = f'Triangle [{actual_width}]'

    plotmgr.set_data(ds, MAIN)
    plotmgr.plot()

    if actual_width < dia.result:
        plotmgr.announce('Triangle width trimmed to actual_width')
        plotmgr.fadeit()
#@+node:tom.20251114143543.1: ** generateTriangle
def generateTriangle(N = 256, w = 255):
    '''Compute a triangular waveform with evenly spaced points.
    The non-zero region starts at point 1.
    
    Return a tuple (xdata, ydata, actual_width).

    ARGUMENT
    N -- the total length of the waveform
    w -- width of non-zero region; w>2.. if w > N - 1, set w = N - 1

    RETURNS
    a tuple (xdata, ydata, actual_width). actual_width is the span,
    which is one less than the number of points.
    '''

    w = min(w, N - 1)
    w = max(3, w)
    if w % 2 == 0:
        w += 1
    x = list(range(N))

    # increment
    delta = 1./((w-1) // 2)

    # The actual width of the triangle is one less than the number of points
    # so we need to have w + 1 points in the non-zero region.
    # _y = [0] + [1] * (w + 1)
    z = 0
    y = [0]
    apex = w//2 + 1; print(f'{apex=} {w=}', flush=True)
    for i in range(1, apex, 1):
        z += delta
        y += [z]
    for i in range(apex, w, 1):
        z -= delta
        y += [z]
    if w < N - 1:
        y.extend([0] * (N - w + 1))

    # Sanity check: length of x, y lists must be equal
    xlen, ylen = len(x), len(y)
    if ylen > xlen:
        y = y[:xlen]
    elif ylen < xlen:
        y.extend([0] * (xlen - ylen))

    return (x, y, w - 1)
#@-others
plotmgr = None  # Suppress pyflake complaints

# plotmgr will have been injected into the module by the time this is called
def proc():
    ds = Dataset()
    makeTriangle(plotmgr, ds)

#@-leo
