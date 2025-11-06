#@+leo-ver=5-thin
#@+node:tom.20250930150701.1: * @file ljung_box.py
"""Apply Ljung-Box test for randomness to [X] data.

This test computes an autocorrelation value at
various lags. The test statistic is treated as
being from the Chi-square distribution, and
a p-value is calculated. If the p-value is
low (e.g., < 0.05) one can assume that the
hypothesis of random distribution has been
"rejected" - i.e., that the evidence for
a random distribution is weak.

"""
import statsmodels.api as sm
from AbstractPlotMgr import MAIN
from .require_datasets import has_main
from help_cmds import HELPTEXT

BUTTON_DEF  = ('Ljung-Box', 'ljung-box',
               'Assess randomness of [X] by looking at autocorrelation coefficients using the Ljung-Box test ')
OVERRIDE = False  # Override default location.
GRAY_LOW, GRAY_HI = 0.01, 0.08
BOOL_WORDS = {True: 'yes', False: 'no'}

HELPTEXT['ljung-box'] = """
Ljung-Box test.
"""

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    d1 = plotmgr.stack[MAIN].copy()
    ydata = d1.ydata

    lj = sm.stats.acorr_ljungbox
    result = lj(ydata, (1,2,5,10,20,30))
    print(result)
    pvalue = result['lb_pvalue']

    is_random = None
    is_gray = bool(pvalue.between(GRAY_LOW, GRAY_HI, 
                     inclusive="both").any())

    if pvalue.iloc[0] > GRAY_HI and pvalue.iloc[-1] > GRAY_HI:
        is_random = True
    elif pvalue.iloc[0] < GRAY_LOW and pvalue.iloc[-1] < GRAY_LOW:
        is_random = False

    msg = ''
    if is_random is not None:
        msg = f'Seems random: {BOOL_WORDS[is_random]}'
        if is_gray:
            msg += ' but may be ambiguous'
    else:
        msg = 'Randomness: ambiguous'
    plotmgr.announce(msg)
#@-leo
