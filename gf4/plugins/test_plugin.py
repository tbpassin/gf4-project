#@+leo-ver=5-thin
#@+node:tom.20220829181057.1: * @file test_plugin.py
#@@language python
"""Developmental plugin - does nothing useful."""

from AbstractPlotMgr import MAIN, BUFFER, STACKDEPTH


BUTTON_DEF  = ('Plugin Test', 'plugin-test', 'A dummy plugin for development')

def proc():
    print('I am the plugin procedure', plotmgr)

#@-leo
