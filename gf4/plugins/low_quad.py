#@+leo-ver=5-thin
#@+node:tom.20221120044718.1: * @file low_quad.py
"""LOWESS order-2 fit."""

# from .require_datasets import has_main


BUTTON_DEF  = ('LOWESS Quad', 'lowess-quad',
               'Fit [X] Data With Order-2 LOWESS Fit')
OVERRIDE = False
plotmgr = None

def proc():
    plotmgr.lowess2Quad()
#@-leo
