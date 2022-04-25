# pylint: disable = consider-using-f-string, undefined-variable
"""Base class for a PlotManager."""


from colors import *
from Dataset import Dataset

MAIN = 0; BUFFER = 1
STACKDEPTH = 3
ERRBAND_HI = 0; ERRBAND_LO = 1

class AbstractPlotManager:
    """AbstractPlotManager is defined to provide a concise definition of the
    interface for PlotManager.

    Typical usage for a concrete PlotManager -

    plotmgr = PlotManager()
    #...
    Tk.mainloop()
    """

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

    def quit(self, event=None):
        self.root.destroy()

    def setupFigure(self, title=''): raise NotImplementedError
    def fix_ticks(self): raise NotImplementedError
    def setXlabel(self, label=''): raise NotImplementedError
    def setYlabel(self, label=''): raise NotImplementedError
    def setFigureTitle(self, title=''): raise NotImplementedError
    def setMenus(self): raise NotImplementedError
    # can only call this after window has been defined
    def setWindowTitle(self, title=''): raise NotImplementedError
    def plot(self, stackposition=MAIN, clearFirst=True):
        raise NotImplementedError
    def overplot(self, stackposition=MAIN): raise NotImplementedError
    def overplotbuff(self): self.overplot(BUFFER)
    def plotmain(self): self.plot(MAIN)
    def plot_stack_top(self): self.plot(STACKDEPTH - 1)
    def overplot_stack_top(self): self.overplot(STACKDEPTH - 1)
    def load_data(self, stackpos=MAIN): raise NotImplementedError
    def load_plot_data(self, fname, overplot=False):  raise NotImplementedError
    def set_data(self, dataset, stackpos=MAIN):  raise NotImplementedError
    def save_data(self, saveas=True): raise NotImplementedError
    def swap_data(self): raise NotImplementedError
    def push_data(self, dataset):
        for n in range(len(self.stack)-1, 0, -1):
            self.stack[n] = self.stack[n-1]
        self.stack[0] = dataset
    def pop_data(self):
        for n in range(1,len(self.stack)):
            self.stack[n-1] = self.stack[n]
    def setNum(self, n):
        self.num = int(n)
