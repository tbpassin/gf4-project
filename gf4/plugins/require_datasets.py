#@+leo-ver=5-thin
#@+node:tom.20220830184545.1: * @file require_datasets.py
from AbstractPlotMgr import MAIN, BUFFER

def needs_main(plotmgr):
    """Flash error message and return False if there is no X dataset."""
    _main = plotmgr.stack[MAIN]
    if not (_main and any(_main.xdata)):
        msg = 'Missing Waveform'
        plotmgr.announce(msg)
        plotmgr.flashit()
        return False
    else:
        return True

def needs_main_buffer(plotmgr):
    if not (_main and any(_main.xdata) and
            _buff and any(_buff.xdata)):
        plotmgr.announce("Missing one or both waveforms")
        plotmgr.flashit()
#@-leo
