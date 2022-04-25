"""Plotting routine for gf4.  This code was removed from the
PlotManager class to reduce the size of the class.  The name
of the parameter "self" has been retained to simplify this
refactoring."""

from Linestyle import LINE_SOLID, LINETHIN, SYM_NONE, LINE_NONE
from AbstractPlotMgr import MAIN, STACKDEPTH

def plot(self, stackposition=MAIN, clearFirst=True):
    """Plot a 2-D graph.

    ARGUMENTS
    self -- an instance of a PlotManager
    stackposition -- an integer denoting which data set to plot.
    clearFirst -- True if the previous plot should be cleared, else False.

    RETURNS
    nothing
    """
    # pylint: disable = too-many-locals
    # pylint: disable = too-many-branches
    _dat = self.stack[stackposition]

    if stackposition < STACKDEPTH:
        _linestyles = self.linestyles[stackposition]
    else:
        _linestyles = self.errorbar_linestyles

    if not _dat:
        self.announce('No data to plot')
        self.flashit()
        return

    _xdata = _dat.xdata
    _ydata = _dat.ydata

    f = self.figure
    if not self.axes:
        try:  # Python 2.7
            ax = f.add_subplot(111, axisbg=self.bgcolor)
        except:  # Python 3.7
            ax = f.add_subplot(111, facecolor=self.bgcolor)
        self.axes = ax
    else:
        ax = self.axes
        if _dat is None or \
                (_xdata is None or len(_xdata) == 0) or \
                (_ydata is None or len(_ydata) == 0):
            if clearFirst:
                ax.clear()
                self.fix_ticks()
                self.canvas.show()
            return

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
    canvas = self.canvas
    if clearFirst:
        ax.clear()
        self.setFigureTitle(_figlabel or 'Figure Label')

    ax.grid(b=True, linestyle=LINE_SOLID, color=self.gridcolor,
            linewidth=LINETHIN)
    ax.set_xlabel(_xlabel or 'X Axis')
    ax.set_ylabel(_ylabel or 'Y Axis')
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
    if self.semilogY:
        ax.set_yscale('log')
    else:
        ax.set_yscale('linear')

    if self.semilogX:
        ax.set_xscale('log')
    else:
        ax.set_xscale('linear')


    ax.plot(_xdata, _ydata, _color,
            linestyle=_ls, linewidth=_lw,
            marker=_marker, mec=_mec, mfc=_mfc, mew=_mew)

    self.fix_ticks()
    if hasattr(_dat, 'ymin'):
        ax.set_ylim(bottom=_dat.ymin)

    if hasattr(_dat, 'ymax'):
        ax.set_ylim(top=_dat.ymax)

    canvas.draw()
    if clearFirst:
        self.announce('')
