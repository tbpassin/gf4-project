#@+leo-ver=5-thin
#@+node:tom.20211211171913.2: * @file Plot.py
"""Plotting routine for gf4.  This code was removed from the
PlotManager class to reduce the size of the class.  The name
of the parameter "self" has been retained to simplify this
refactoring."""

#@+others
#@+node:tom.20211211171913.3: ** Imports
from Linestyle import LINE_SOLID, LINETHIN, SYM_NONE, LINE_NONE
from AbstractPlotMgr import MAIN, STACKDEPTH

#@+node:tom.20211211171913.4: ** plot (Plot.py)
def plot(self, stackposition=MAIN, clearFirst=True):
    """Plot a 2-D graph.

    ARGUMENTS
    self -- an instance of a PlotManager
    stackposition -- an integer denoting which data set to plot.
    clearFirst -- True if the previous plot should be cleared, else False.

    RETURNS
    nothing
    """
    _dat = self.stack[stackposition]

    if stackposition < STACKDEPTH:
        _linestyles = self.linestyles[stackposition]
    else:
        _linestyles = self.errorbar_linestyles

    if not (_dat and any(_dat.xdata)):
        self.announce('No data to plot')
        self.flashit()
        return

    _xdata = _dat.xdata
    _ydata = _dat.ydata

    f = self.figure
    #@+<< get axes >>
    #@+node:tom.20220115175642.1: *3* << get axes >>
    if not self.axes:
        ax = f.gca()
        self.axes = ax
    else:
        ax = self.axes
    #@-<< get axes >>
    #@+<< bail if no data >>
    #@+node:tom.20220115175032.1: *3* << bail if no data >>
    if _dat is None or \
            (_xdata is None or len(_xdata) == 0) or \
            (_ydata is None or len(_ydata) == 0):
        if clearFirst:
            ax.clear()
            self.fix_ticks()
            self.canvas.show()
        return

    #@-<< bail if no data >>
    #@+<< setup labels >>
    #@+node:tom.20220115175205.1: *3* << setup labels >>
    _figlabel = ''
    _xlabel = ''
    _ylabel = ''
    if clearFirst:
        _figlabel = _dat.figurelabel
        _xlabel = _dat.xaxislabel
        _ylabel = _dat.yaxislabel
    else:
        _main = self.stack[MAIN]
        _figlabel = _main.figurelabel
        _xlabel = _main.xaxislabel
        _ylabel = _main.yaxislabel

    self.set_editable_labels()
    #@-<< setup labels >>
    canvas = self.canvas
    #@+<< set axes appearance >>
    #@+node:tom.20220401210413.1: *3* << set axes appearance >>
    if clearFirst:
        ax.clear()
        self.setFigureTitle(_figlabel or 'Figure Label')

    ax.grid(visible=True, linestyle=LINE_SOLID, color=self.gridcolor,
            linewidth=LINETHIN)
    ax.set_xlabel(_xlabel or 'X Axis')
    ax.set_ylabel(_ylabel or 'Y Axis')
    #@-<< set axes appearance >>
    #@+<< set linestyles >>
    #@+node:tom.20220115175458.1: *3* << set linestyles >>
    _color = _linestyles.linecolor
    _lw = _linestyles.linewidth
    _mec = _linestyles.sym_mec
    _mfc = _linestyles.sym_mfc
    _mew = _linestyles.sym_mew

    _plotsyms = _linestyles.useSym
    _plotline = _linestyles.useLine

    if _plotsyms:
        _marker = _linestyles.symbol
    else:
        _marker = SYM_NONE

    if _plotline:
        _ls = _linestyles.linestyle
    else:
        _ls = LINE_NONE
    #@-<< set linestyles >>
    #@+<< set log or linear >>
    #@+node:tom.20220115175337.1: *3* << set log or linear >>
    if self.semilogY:
        ax.set_yscale('log')
    else:
        ax.set_yscale('linear')

    if self.semilogX:
        ax.set_xscale('log')
    else:
        ax.set_xscale('linear')

    #@-<< set log or linear >>

    ax.plot(_xdata, _ydata, _color,
            linestyle=_ls, linewidth=_lw,
            marker=_marker, mec=_mec, mfc=_mfc, mew=_mew)

    self.fix_ticks()
    #@+<< set max-min >>
    #@+node:tom.20220115175943.1: *3* << set max-min >>
    if hasattr(_dat, 'ymin'):
        ax.set_ylim(bottom=_dat.ymin)

    if hasattr(_dat, 'ymax'):
        ax.set_ylim(top=_dat.ymax)
    #@-<< set max-min >>

    canvas.draw()
    if clearFirst:
        self.announce('')
#@-others
#@@language python
#@@tabwidth -4
#@-leo
