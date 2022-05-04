#@+leo-ver=5-thin
#@+node:tom.20211211171304.44: * @file fail.py
#@+others
#@+node:tom.20211211171304.45: ** Imports
import sys

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#import Tkinter as Tk
import tkinter as Tk

#@+node:tom.20211211171304.46: ** class PlotManager
class PlotManager():
    #@+others
    #@+node:tom.20211211171304.47: *3* PlotManager.__init__
    def __init__(self, root=None):
        self.setupFigure()

    #@+node:tom.20211211171304.48: *3* PlotManager.setupFigure
    def setupFigure(self, title='GF4'):
        root = Tk.Tk()

        #f = Figure(figsize=(9,6), dpi=100)
        f = Figure()

        canvas = FigureCanvasTkAgg(f, master=root)
        sys.exit(0)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


    #@-others
#@+node:tom.20211211171304.49: ** if __name__ == '__main__': (fail.py)
if __name__ == '__main__':
    plotmgr = PlotManager()

    Tk.mainloop()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
