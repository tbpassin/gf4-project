import sys

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#import Tkinter as Tk
import tkinter as Tk

class PlotManager():
    def __init__(self, root=None):
        self.setupFigure()

    def setupFigure(self, title='GF4'):
        root = Tk.Tk()

        #f = Figure(figsize=(9,6), dpi=100)
        f = Figure()

        canvas = FigureCanvasTkAgg(f, master=root)
        sys.exit(0)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


if __name__ == '__main__':
    plotmgr = PlotManager()

    Tk.mainloop()
