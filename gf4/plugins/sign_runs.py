#@+leo-ver=5-thin
#@+node:tom.20250928233017.1: * @file sign_runs.py
"""Apply Wald–Wolfowitz runs test to [X] data.

    As N = number of points increases, the number of
    runs approaches a normal distribution with

    μ = mean number of runs in a sequence of N elements
      = 1 + (2*N+*N-)/N
    Var = (μ - 1)*(μ - 2) / (N - 1)
    
    The Z statistic is
    
        Z = (N - μ)/ Var**0.5
        
    where N is the total number of runs = N+ + N-.
"""

from AbstractPlotMgr import MAIN
from .require_datasets import has_main

BUTTON_DEF  = ('Sign Runs', 'sign-runs',
               'Assess randomness of a sequence using the Wald–Wolfowitz  test for runs of signs')
OVERRIDE = False  # Override default location.
plotmgr = None

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not has_main(plotmgr):
        return

    d1 = plotmgr.stack[MAIN].copy()
    ydata = d1.ydata
    avg = float(sum(ydata)) / len(ydata)
    d1.addConstant(-avg)

    # Convert data to signs; skip values that equal the average.
    # Use +1 for positive sign, -1 for negative
    signs = []
    for y in d1.ydata:
        if y > 0:
            signs.append(1)
        elif y < 0:
            signs.append(-1)

    positive_vals = 0
    negative_vals = 0
    runs = 0
    last_data = signs[0]

    for s in signs:
        if s == 1:
            positive_vals += 1
        else:
            negative_vals += 1
        if s != last_data:
            runs += 1
            last_data = s

    Npos = positive_vals
    Nneg = negative_vals
    N = Npos + Nneg

    # Expected:
    μ = 1 + (2 * Npos * Nneg)/N
    var = (μ - 1)*(μ - 2) / (N - 1)

    σ = var**0.5
    z = (runs - μ) / σ
    plotmgr.announce(f'Runs: {runs}, Expected: {μ:.2f}, σ: {σ:.2f}, Z: {z:.2f}')
#@-leo
