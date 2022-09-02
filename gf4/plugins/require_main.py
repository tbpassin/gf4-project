#@+leo-ver=5-thin
#@+node:tom.20220830184545.1: * @file require_main.py
from AbstractPlotMgr import MAIN

def needs_main(plotmgr):
    _main = plotmgr.stack[MAIN]
    if not (_main and any(_main.xdata)):
        msg = 'Missing Waveform'
        plotmgr.announce(msg)
        plotmgr.flashit()
#@-leo
