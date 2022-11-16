#@+leo-ver=5-thin
#@+node:tom.20221106223828.1: * @file calculator.py
"""Open a dialog that evaluates math expressions. display results in messge band."""
from entry import GetSingleFloat

BUTTON_DEF  = ('Calculator', 'calculate',
            'Evalutes Python Math Expressions. pi and e (type "m_e") are legal.')

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    dia = GetSingleFloat(plotmgr.root, 'Evaluate (use "m_e" for "e" [ln base])',
                         'Expressions', 0)
    if dia.result is None: return

    plotmgr.announce(dia.result)
#@-leo
