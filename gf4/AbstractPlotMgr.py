#@+leo-ver=5-thin
#@+node:tom.20211211170701.2: * @file AbstractPlotMgr.py
# pylint: disable = consider-using-f-string, undefined-variable
#@+others
#@+node:tom.20211211170701.3: ** Declarations
"""Base class for a PlotManager."""


from colors import *
from Dataset import Dataset

MAIN = 0; BUFFER = 1
STACKDEPTH = 3
ERRBAND_HI = 0; ERRBAND_LO = 1

#@+node:tom.20211211170701.4: ** class AbstractPlotManager
class AbstractPlotManager:
    """AbstractPlotManager is defined to provide a concise definition of the
    interface for PlotManager.

    Typical usage for a concrete PlotManager -

    plotmgr = PlotManager()
    #...
    Tk.mainloop()
    """

    #@+others
    #@+node:tom.20220402082631.1: *3* Setup
    #@+node:tom.20211211170701.5: *4* AbstractPlotManager.__init__
    def __init__(self, root=None):
        self.root = root
        self.axes = None
        self.figure = None
        self.canvas = None
        self.semilogY = False
        self.semilogX = False
        self.bgcolor = WHITE
        self.gridcolor=DEFAULTGRIDCOLOR
        self.stackdepth = STACKDEPTH
        # List of Dataset objects:
        self.stack = [Dataset() for i in range(self.stackdepth)]
        # Storage for one Dataset:
        self.storage = None
        # Default number of points for generated curves (integer):
        self.num = 256
        # Will hold a Tk Entry widget for single-line edits
        self.editWidget = None
        self.editableLabels = []
        self.parmsaver = {}
        self.commands = {}

        self.setupFigure()

    #@+node:tom.20211211170701.6: *4* AbstractPlotManager.quit
    def quit(self, event=None):
        self.root.destroy()

    #@+node:tom.20211211170701.7: *4* AbstractPlotManager.setupFigure
    def setupFigure(self, title=''): raise NotImplementedError
    #@+node:tom.20211211170701.8: *4* AbstractPlotManager.fix_ticks
    def fix_ticks(self): raise NotImplementedError
    #@+node:tom.20211211170701.9: *4* AbstractPlotManager.setXlabel
    def setXlabel(self, label=''): raise NotImplementedError
    #@+node:tom.20211211170701.10: *4* AbstractPlotManager.setYlabel
    def setYlabel(self, label=''): raise NotImplementedError
    #@+node:tom.20211211170701.11: *4* AbstractPlotManager.setFigureTitle
    def setFigureTitle(self, title=''): raise NotImplementedError
    #@+node:tom.20211211170701.12: *4* AbstractPlotManager.setMenus
    def setMenus(self): raise NotImplementedError
    # can only call this after window has been defined
    #@+node:tom.20211211170701.13: *4* AbstractPlotManager.setWindowTitle
    def setWindowTitle(self, title=''): raise NotImplementedError
    #@+node:tom.20220402082428.1: *3* Plotting Methods
    #@+node:tom.20211211170701.14: *4* AbstractPlotManager.plot
    def plot(self, stackposition=MAIN, clearFirst=True):
        raise NotImplementedError
    #@+node:tom.20211211170701.15: *4* AbstractPlotManager.overplot
    def overplot(self, stackposition=MAIN): raise NotImplementedError
    #@+node:tom.20211211170701.16: *4* AbstractPlotManager.overplotbuff
    def overplotbuff(self): self.overplot(BUFFER)
    #@+node:tom.20211211170701.17: *4* AbstractPlotManager.plotmain
    def plotmain(self): self.plot(MAIN)
    #@+node:tom.20211211170701.18: *4* AbstractPlotManager.plot_stack_top
    def plot_stack_top(self): self.plot(STACKDEPTH - 1)
    #@+node:tom.20211211170701.19: *4* AbstractPlotManager.overplot_stack_top
    def overplot_stack_top(self): self.overplot(STACKDEPTH - 1)
    #@+node:tom.20220402082507.1: *3* Data and Stack Methods
    #@+node:tom.20211211170701.20: *4* AbstractPlotManager.load_data
    def load_data(self, stackpos=MAIN): raise NotImplementedError
    #@+node:tom.20211211170701.21: *4* AbstractPlotManager.load_plot_data
    def load_plot_data(self, fname, overplot=False):  raise NotImplementedError
    #@+node:tom.20211211170701.22: *4* AbstractPlotManager.set_data
    def set_data(self, dataset, stackpos=MAIN):  raise NotImplementedError
    #@+node:tom.20211211170701.23: *4* AbstractPlotManager.save_data
    def save_data(self, saveas=True): raise NotImplementedError
    #@+node:tom.20211211170701.24: *4* AbstractPlotManager.swap_data
    def swap_data(self): raise NotImplementedError
    #@+node:tom.20211211170701.25: *4* AbstractPlotManager.push_data
    def push_data(self, dataset):
        for n in range(len(self.stack)-1, 0, -1):
            self.stack[n] = self.stack[n-1]
        self.stack[0] = dataset
    #@+node:tom.20211211170701.26: *4* AbstractPlotManager.pop_data
    def pop_data(self):
        for n in range(1,len(self.stack)):
            self.stack[n-1] = self.stack[n]
    #@+node:tom.20211211170701.27: *4* AbstractPlotManager.setNum
    def setNum(self, n):
        self.num = int(n)
    #@-others
#@-others
#@@language python
#@@tabwidth -4
#@-leo
