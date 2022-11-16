#@+leo-ver=5-thin
#@+node:tom.20220830184545.1: * @file require_datasets.py
from AbstractPlotMgr import MAIN, BUFFER

def needs_main(plotmgr = None):
    """Return True if X (MAIN) dataset exists, otherwise flash error message 
       and return False.
    """
    if not plotmgr:
        return False

    _main = plotmgr.stack[MAIN]
    if not (_main and any(_main.xdata)):
        msg = 'Missing Waveform'
        plotmgr.announce(msg)
        plotmgr.flashit()
        return False
    return True

def needs_main_buffer(plotmgr = None):
    """Return True if both the X and Y (MAIN and BUFFER) datasets exist,
       otherwise flash error message and return False.
    """
    if not plotmgr:
        return False

    _main = plotmgr.stack[MAIN]
    _buff = plotmgr.stack[BUFFER]
    if not (_main and any(_main.xdata) and
            _buff and any(_buff.xdata)):
        plotmgr.announce("Missing one or both waveforms")
        plotmgr.flashit()
        return False
    return True

# Better names:
has_main = needs_main
has_main_buffer = needs_main_buffer
#@-leo
