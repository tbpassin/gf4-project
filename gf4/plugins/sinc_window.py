#@+leo-ver=5-thin
#@+node:tom.20251011190146.1: * @file sinc_window.py
"""Window [X] waveform with sinc function."""

import numpy as np
from AbstractPlotMgr import MAIN
from .require_datasets import has_main

BUTTON_DEF  = ('Sinc (sin(x)/x)', 'sinc-window',
               'Window [X] with Sinc Curve')
OVERRIDE = True
OWNER_GROUP = 'WINDOW_BUTTONS'

plotmgr = None  # Suppress pyflake complaints

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return
    dm = plotmgr.stack[MAIN]
    ym = dm.ydata  # Might be a numpy nd array.

    N = len(ym)
    x = np.arange(N)
    center = (N - 1) / 2
    scale = center  # main lobe spans endpoints
    sinc = np.sinc((x - center) / scale)
    dm.ydata = ym * sinc

    figurelabel = 'Sinc Windowed'
    lab = dm.figurelabel
    if lab:
        figurelabel += f' {lab}'

    if len(figurelabel) > 90:
        figurelabel = figurelabel[:90] + '...'
    plotmgr.stack[MAIN].figurelabel = figurelabel

    plotmgr.plot()
#@-leo
