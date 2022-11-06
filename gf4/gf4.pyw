#@+leo-ver=5-thin
#@+node:tom.20211207165051.2: * @file gf4.pyw
# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211207165051.3: ** Imports
from __future__ import print_function

import sys
from pathlib import PurePath

import tkinter as Tk
import tkinter.font as tkFont
from tkinter import filedialog as fd

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

from numpy import ndarray
from scipy.stats import spearmanr
from statsmodels.tsa.stattools import pacf

#from randnum import *
from AbstractPlotMgr import AbstractPlotManager
from AbstractPlotMgr import MAIN, BUFFER, STACKDEPTH, ERRBAND_HI, ERRBAND_LO

import createMenus
from colors import (BLACK, CYAN, GRAY, LIGHTGRAY, DEFAULTGRIDCOLOR,
                    ColorBgPairs)

from Dataset import Dataset
from Linestyle import (Linestyle, LINETHIN, LINEMED)
#from Linestyle import (CIRCLE, HEXAGON, DIAMOND, SQUARE, TRIANGLE,
#                       SYM_NONE, LINE_NONE, LINE_SOLID, LINETHICK)
import smoother
lowess2_stddev = smoother.lowess2_stddev

from fits import piecewiseLinear
import stats

from entry import TextFade, GetSingleInt, GetSingleFloat #, GetTwoFloats
from entry import GetTwoNumbers #, GetTwoInts
from editDialog import editDialog
from trend import mann_kendall, YESNO

from cmdwin import cmdwindow
from utility import ICONPATH, setIcon

matplotlib.use('TkAgg')

#@+node:tom.20211207171026.1: ** Declarations
COMMENTS = (';', '#')

ENCODING = 'utf-8'
# Special data import keyword
ENDDATASET = 'ENDDATASET'

HOMEPATH = PurePath(__file__).parent
ICONFILE = 'linechart1.png'
# Unusual but legal syntax for PurePath
ICONPATH = PurePath(HOMEPATH) / 'icons' / ICONFILE
#@+node:tom.20211207165051.4: ** class PlotManager(AbstractPlotManager)
class PlotManager(AbstractPlotManager):

    # pylint: disable = import-outside-toplevel
    # pylint: disable = too-many-public-methods

    # Putting these imports at the top of the module doesn't work
    # Because they expect to be called as methods with a "self" param.
    from Plot import plot
    from Timehack import timehack
    from BuildCommands import buildCommands
    from MakeWaveforms import (
        makeExponential, makeSine, makeDampedSine,
        makeStep, makeDelta, makeRamp,
        makeSquarewave, makeRandomNoise,
        makeUniformNoise, makeGaussianNoise,
        pdfGaussian, cdfGaussian)

    #@+others
    #@+node:tom.20211207211642.1: *3* Decorators
    #@+node:tom.20211207165051.5: *4* doErrorBands
    def doErrorBands(method):
        '''A decorator method to process error bands in the same way that
        the y data is processed.  The original method call must return
        the Dataset it is being applied to, and the method it applies.
        '''
        # pylint: disable = no-self-argument
        # pylint: disable = not-callable
        def new_method(*args):
            # args[0] will be the calling instance (i.e., self)
            # Call original method
            _ds, func = method(args[0])

            if _ds and _ds.errorBands:
                func(_ds.errorBands[0])
                func(_ds.errorBands[1])

        return new_method

    #@+node:tom.20211207165051.6: *4* REQUIRE_MAIN
    def REQUIRE_MAIN(procedure):
        """A decorator method to check if there is data in the MAIN slot.

        If not, exit procedure with error message.  Otherwise,
        execute the procedure.

        ARGUMENT
        procedure -- an instance method that takes no parameters.
        """
        # pylint: disable = no-self-argument
        # pylint: disable = not-callable
        def new_proc(*args):
            # args[0] will be the calling instance (i.e., self)
            self = args[0]
            _main = self.stack[MAIN]
            if not (_main and any(_main.xdata)):
                msg = 'Missing Waveform'
                self.announce(msg)
                self.flashit()
                return
            procedure(*args)
        return new_proc

    #@+node:tom.20211207165051.7: *4* REQUIRE_MAIN_BUFF
    def REQUIRE_MAIN_BUFF(procedure):
        """A decorator method to check if there is data in the MAIN
        and BUFFER slots.

        If not, exit procedure with error message.  Otherwise,
        execute the procedure.

        ARGUMENT
        procedure -- an instance method that takes no parameters.
        """
        # pylint: disable = no-self-argument
        # pylint: disable = not-callable

        def new_proc(*args):
            # args[0] will be the calling instance (i.e., self)
            self = args[0]
            _main = self.stack[MAIN]
            _buff = self.stack[BUFFER]
            if not (_main and any(_main.xdata) and
                    _buff and any(_buff.xdata)):
                self.announce("Missing one or both waveforms")
                self.flashit()
                return
            procedure(self)
        return new_proc

    #@+node:tom.20211207165051.8: *3* __init__
    def __init__(self, root=None):
        super().__init__(root)
        self.toolbar = None

        self.linestyles = [Linestyle() for i in range(self.stackdepth)]
        self.linestyles[MAIN].linecolor = BLACK
        self.linestyles[MAIN].sym_mec = BLACK
        self.linestyles[MAIN].linewidth = LINEMED
        self.linestyles[BUFFER].linecolor = CYAN
        self.linestyles[BUFFER].sym_mec = BLACK
        self.linestyles[BUFFER].sym_mfc = CYAN
        self.linestyles[BUFFER].linewidth = LINEMED

        self.errorbar_linestyles = Linestyle()
        self.errorbar_linestyles.linecolor = GRAY
        self.errorbar_linestyles.linewidth = LINETHIN

        self.main_symbol_color = Tk.StringVar()
        self.buffer_symbol_color = Tk.StringVar()
        self.main_line_color = Tk.StringVar()
        self.buffer_line_color = Tk.StringVar()
        self.radio_main_linestyle = Tk.StringVar()
        self.radio_buffer_linestyle = Tk.StringVar()
        self.main_symbol_shape = Tk.StringVar()
        self.buffer_symbol_shape = Tk.StringVar()
        self.graph_bg_color = Tk.StringVar()

        self.initpath = '.'  # for File Dialog directory
        self.current_path = ''
        self.buildCommands()
        self.setMenus()

        self.set_init_pos()
    #@+node:tom.20221006234409.1: *3* set_init_pos
    def set_init_pos(self):
        """Set initial position of main window.
        
        A position near left of screen leaves room for button window 
        to be located without overlapping main window on most screens.
        A position not too far above the screen bottom leaves room above
        the window for the stack readout window.
        """
        self.root.update()  # Required to get the actual window height.
        hs = self.root.winfo_screenheight()
        hw = self.root.winfo_height()
        y = hs - hw - 150
        self.root.geometry(f'+50+{y}')
    #@+node:tom.20211207165051.22: *3* setMenus
    def setMenus(self):
        mainMenu = createMenus.setMenus(self)
        self.root.config(menu=mainMenu)

    #@+node:tom.20211207165051.9: *3* openAuxWin
    def openAuxWin(self):
        if not self.hasToplevel():
            cmdwindow(self)

    #@+node:tom.20211207211739.1: *3* Widget Utilities
    #@+node:tom.20211207165051.10: *4* open_editDialog
    def open_editDialog(self):
        editDialog()

    #@+node:tom.20211207165051.11: *4* setWindowTitle
    def setWindowTitle(self, title=''):
        if self.root:
            self.root.wm_title(title)

    #@+node:tom.20211207165051.12: *4* label_select_all
    def label_select_all(self, event):
        '''Select all text in an edit widget (Tk.Entry) when <CNTRL-A>
        is pressed. It seems that the default key is <CTRL-/>
        (standard for linux) and this overrides that.  The
        "return 'break'" is essential, otherwise this gets ignored.
        '''

        event.widget.selection_range(0, Tk.END)
        return 'break'

    #@+node:tom.20211207165051.13: *4* setupFigure
    def setupFigure(self, title='GF4'):
        root = Tk.Tk()
        root.option_add('*tearOff', False)  # Tk specific menu option

        root.bind('<Alt-F4>', self.quit)

        f = Figure(figsize=(9, 6), dpi=100, facecolor=LIGHTGRAY)
        ax = None
        ax = f.gca()
        ax.set_facecolor(self.bgcolor)

        canvas = FigureCanvasTkAgg(f, master=root)
        self.toolbar = NavigationToolbar2Tk(canvas, root)
        self.toolbar.update()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.toolbar.pack()

        self._sv = Tk.StringVar()
        self._sv.set('')
        self.editWidget = Tk.Entry(root, textvariable=self._sv, width=80)
        self.editWidget.bind('<Return>', self.doneEditLabel)
        self.editWidget.bind('<Escape>', self.doneEditLabel)
        self.editWidget.bind('<Control-a>', self.label_select_all)

        self.root = root
        self.axes = ax
        self.figure = f
        self.canvas = canvas
        self.fix_ticks()
        self.setWindowTitle(title)

        canvas.mpl_connect('button_press_event', self.edit_label)

        _ann = TextFade(root, height=1, font='size 12',
                        width=100, bd=0, pady=5, bg='LightBlue')
        _ann.insert(1.0, '')
        _ann.config(state=Tk.DISABLED)
        _ann.pack()

        self.announcer = _ann

        self.set_editable_labels()
        self.currentLabelEditing = None

    #@+node:tom.20211207165051.14: *4* fadeit
    def fadeit(self, widget=None):
        '''For TextFade widgets and similar with a fade() method.'''
        if widget and 'fade' not in dir(widget): return
        if not widget:
            widget = self.announcer
        widget.fade()

    #@+node:tom.20211207165051.15: *4* flashit
    def flashit(self, color='yellow', widget=None):
        '''For TextFade widgets and similar with a flash() method.'''
        if widget and 'flash' not in dir(widget): return
        if not widget:
            widget = self.announcer
        widget.flash(color)
        widget.after(1000)
        self.fadeit(widget)

    #@+node:tom.20211207165051.16: *4* announce
    def announce(self, msg='This is a test'):
        '''Show an message in the announcement area.'''
        _ann = self.announcer
        _ann.config(state=Tk.NORMAL)
        _ann.delete(1.0, Tk.END)
        _ann.insert(1.0, msg)
        _ann.config(state=Tk.DISABLED)

    #@+node:tom.20211207165051.17: *4* set_editable_labels
    def set_editable_labels(self):
        '''Create a list of those labels that can be edited with the standard
        single-line edit widget.  Return nothing.
        '''
        if not self.axes: return

        self.editableLabels.extend([
            self.axes.get_xaxis().get_label(),
            self.axes.get_yaxis().get_label()]
        )

    #@+node:tom.20211207165051.18: *4* edit_label
    def edit_label(self, event):
        '''Respond to a mouse-press event.  Check all the editable labels,
        plus other Text items in the figure, to see if the event belongs to
        one of them.  If so, display the label edit widget over the label.

        ARGUMENT
        event - a mathplotlib event;  MouseEvent is expected.

        RETURNS
        nothing.
        '''
        if not self.axes: return

        _labels = [item for item in self.axes.get_children()
                   if isinstance(item, matplotlib.text.Text)]
        _labels.extend(self.editableLabels)

        lab = None
        for _lab in _labels:
            if _lab.contains(event)[0]:
                lab = _lab
                break

        if lab is None:
            self.currentLabelEditing = None
            return

        self.currentLabelEditing = lab
        ew = self.editWidget
        self._sv.set(lab.get_text())

        #@+<< configure editwidget >>
        #@+node:tom.20220115225226.1: *5* << configure editwidget >>
        lab_fontsize = int(lab.get_size())
        tkfont = tkFont.Font(size=lab_fontsize)

        bbox = lab.get_window_extent()
        ul, lr = bbox.get_points()
        ulx, uly = ul
        lrx, lry = lr

        canvas = self.canvas
        dpi = canvas.figure._dpi
        canvas_bbox_ul = canvas.figure.bbox_inches.get_points()[1]
        canv_ulx, canv_uly = \
            int(dpi * canvas_bbox_ul[0]), int(dpi * canvas_bbox_ul[1])

        ew.configure(font=tkfont)
        #@-<< configure editwidget >>
        ew.place(x=ulx, y=canv_uly - lry)
        ew.selection_clear()
        ew.focus_set()
        ew.lift()

    #@+node:tom.20211207165051.19: *4* doneEditLabel
    def doneEditLabel(self, event):
        """Receive <Return> and <Escape> events.  For <Escape>, leave.
        For <Return>, also change the label's text, and set the Dataset's
        corresponding label, if any.
        """

        if not self.currentLabelEditing: return

        if event.keysym == 'Return':
            _newtext = event.widget.get()
            self.currentLabelEditing.set_text(_newtext)
            self.canvas.draw()

            if self.currentLabelEditing is self.axes.get_xaxis().get_label():
                self.stack[MAIN].xaxislabel = _newtext
            elif self.currentLabelEditing is self.axes.get_yaxis().get_label():
                self.stack[MAIN].yaxislabel = _newtext
            elif _newtext == self.axes.get_title():
                self.stack[MAIN].figurelabel = _newtext
        elif event.keysym == 'Escape':
            self.canvas.draw()

        event.widget.lower()
        event.widget.selection_clear()
        self.currentLabelEditing = None

    #@+node:tom.20211207212159.1: *3* Data Stack
    #@+node:tom.20211207165051.32: *4* copyToBuffer
    def copyToBuffer(self):
        if not self.stack[MAIN]:
            self.announce("No waveform to copy")
            self.flashit()
            return

        self.stack[BUFFER] = self.stack[MAIN].copy()

    #@+node:tom.20211207165051.33: *4* swap_data
    def swap_data(self):
        if not self.stack[MAIN] or not self.stack[BUFFER]:
            self.announce("Missing one or both waveforms  - nothing to swap")
            self.flashit()
            return

        _temp = self.stack[BUFFER].copy()
        self.stack[BUFFER] = self.stack[MAIN].copy()
        self.stack[MAIN] = _temp

    #@+node:tom.20211207165051.34: *4* paste_data
    def paste_data(self):
        if not self.stack[BUFFER]:
            self.announce("No waveform to paste")
            self.flashit()
            return

        self.stack[MAIN] = self.stack[BUFFER].copy()

    #@+node:tom.20211207165051.35: *4* drop_stack
    def drop_stack(self):
        '''Drop stack of datasets, leave top one unchanged.'''
        for i in range(STACKDEPTH - 1):
            self.stack[i] = self.stack[i + 1].copy()

    #@+node:tom.20211207165051.36: *4* push_with_copy
    def push_with_copy(self):
        '''Push dataset stack up, duplicate duplicate bottom:
            top-1 -> top        -2 -> -1
            ...
            1 -> 2
            0 -> 1
            0 stays unchanged
        '''

        for i in range(STACKDEPTH - 1, 0, -1):
            self.stack[i] = self.stack[i - 1].copy()

    #@+node:tom.20211207165051.37: *4* rotate_stack_up
    def rotate_stack_up(self):
        '''Rotate dataset stack up:
            1 -> 2
            2 -> 3
            ...
            top -> 1
        '''

        temp = self.stack[STACKDEPTH - 1].copy()
        self.push_with_copy()
        self.stack[0] = temp

    #@+node:tom.20211207165051.38: *4* rotate_stack_down
    def rotate_stack_down(self):
        '''Rotate stack downwards:
                top -> top-1
                ...
                2 -> 1
                1 -> top
        '''
        temp = self.stack[0].copy()
        self.drop_stack()
        self.stack[STACKDEPTH - 1] = temp

    #@+node:tom.20211207165051.39: *4* copy_to_top
    def copy_to_top(self):
        '''Copy active dataset to top of stack.'''
        self.stack[STACKDEPTH - 1] = self.stack[MAIN].copy()

    #@+node:tom.20211207165051.40: *4* copy_from_top
    def copy_from_top(self):
        '''Copy top dataset to bottom of stack ("main").'''
        self.stack[MAIN] = self.stack[STACKDEPTH - 1].copy()

    #@+node:tom.20211207165051.66: *4* store1
    def store1(self):
        """Store X dataset in a special location outside the stack."""
        _ds = self.stack[MAIN].copy()
        self.storage = _ds

    #@+node:tom.20211207165051.67: *4* recall1
    def recall1(self):
        """Recall stored dataset to X."""
        if self.storage:
            self.stack[MAIN] = self.storage.copy()
        else:
            self.announce("No stored data to recall")
            self.flashit()

    #@+node:tom.20211207211946.1: *3* Configure Graph
    #@+node:tom.20211207165051.24: *4* set_axis_bg
    def set_axis_bg(self):
        self.axes.set_facecolor('yellow')
    # =============================================================

    #@+node:tom.20211207165051.20: *4* setYMin
    def setYMin(self, val):
        if not self.axes: return
        axis = self.axes
        axis.set_ybound(self.stack[MAIN].ymin)

    #@+node:tom.20211207165051.26: *4* setSemilogX
    def setSemilogX(self):
        self.semilogY = False
        self.semilogX = True
        self.plot()

    #@+node:tom.20211207165051.25: *4* setSemilogY
    def setSemilogY(self):
        self.semilogY = True
        self.semilogX = False
        self.plot()

    #@+node:tom.20211207165051.21: *4* fix_ticks
    def fix_ticks(self):
        '''Make tick marks point out of the figure's frame rather than the
        default of inwards.
        '''
        if not self.axes: return

        # tick mark adjustments adapted from
        # http://osdir.com/ml/python.matplotlib.general/2005-01/msg00076.html
        axis = self.axes
        xticks = axis.get_xticklines()
        for tick in xticks:
            tick.set_markersize(6)

        yticks = axis.get_yticklines()
        for tick in yticks:
            tick.set_markersize(6)

        xlabels = axis.get_xticklabels()
        for label in xlabels:
            label.set_y(-0.02)
            label.set_size('small')

        ylabels = axis.get_yticklabels()
        for label in ylabels:
            label.set_x(-0.02)
            label.set_size('small')

    #@+node:tom.20211207165051.27: *4* setLogLog
    def setLogLog(self):
        self.semilogY = True
        self.semilogX = True
        self.plot()

    #@+node:tom.20211207165051.28: *4* setLinLin
    def setLinLin(self):
        self.semilogY = False
        self.semilogX = False
        self.plot()

    #@+node:tom.20211207165051.41: *4* setPlotLineWidth
    def setPlotLineWidth(self, position, width):
        self.linestyles[position].set_linewidth(width)

    #@+node:tom.20211207165051.42: *4* setLineColor
    def setLineColor(self, stackpos):
        '''Called only though a menu selection, so that self.x_line_color
        is set before this method is called.
        '''

        if stackpos == MAIN:
            _color = self.main_line_color.get()
        else:
            _color = self.buffer_line_color.get()
        self.linestyles[stackpos].set_linecolor(_color)

    #@+node:tom.20211207165051.43: *4* setLineColorMain
    def setLineColorMain(self):
        self.setLineColor(MAIN)

    #@+node:tom.20211207165051.44: *4* setLineColorBuffer
    def setLineColorBuffer(self):
        self.setLineColor(BUFFER)

    #@+node:tom.20211207165051.45: *4* setSymColor
    def setSymColor(self, stackpos):
        '''Called only though a menu selection, so that self.x_symbol_color
        is set before this method is called.
        '''

        if stackpos == MAIN:
            _color = self.main_symbol_color.get()
        else:
            _color = self.buffer_symbol_color.get()
        self.linestyles[stackpos].set_sym_color(_color)

    #@+node:tom.20211207165051.46: *4* setSymColorMain
    def setSymColorMain(self):
        self.setSymColor(MAIN)

    #@+node:tom.20211207165051.47: *4* setSymColorBuffer
    def setSymColorBuffer(self):
        self.setSymColor(BUFFER)

    #@+node:tom.20211207165051.48: *4* setBgColor
    def setBgColor(self):
        _color = self.graph_bg_color.get()
        self.axes.set_facecolor(_color)
        _gridcolor = ColorBgPairs.get(_color, DEFAULTGRIDCOLOR)
        self.gridcolor = _gridcolor

    #@+node:tom.20211207165051.49: *4* setMainLineWidth
    def setMainLineWidth(self):
        _width = float(self.radio_main_linestyle.get())
        self.setPlotLineWidth(MAIN, _width)

    #@+node:tom.20211207165051.50: *4* setBufferLineWidth
    def setBufferLineWidth(self):
        _width = float(self.radio_buffer_linestyle.get())
        self.setPlotLineWidth(BUFFER, _width)

    #@+node:tom.20211207165051.51: *4* setMarkerStyle
    def setMarkerStyle(self, stackpos):
        # pylint: disable = no-member
        if stackpos == MAIN:
            _ms = self.main_marker_style
        else:
            _ms = self.buffer_marker_style
        _style = int(_ms.get())
        _ls = self.linestyles[stackpos]
        if _style == 1:
            _ls.useLine = True
            _ls.useSym = False
        elif _style == 2:
            _ls.useLine = False
            _ls.useSym = True
        else:
            _ls.useLine = True
            _ls.useSym = True

    #@+node:tom.20211207165051.52: *4* setMainMarkerStyle
    def setMainMarkerStyle(self):
        self.setMarkerStyle(MAIN)

    #@+node:tom.20211207165051.53: *4* setBufferMarkerStyle
    def setBufferMarkerStyle(self):
        self.setMarkerStyle(BUFFER)

    #@+node:tom.20211207165051.54: *4* setSymShape
    def setSymShape(self, stackpos):
        if stackpos == MAIN:
            _shp = self.main_symbol_shape
        else:
            _shp = self.buffer_symbol_shape
        _shape = _shp.get()
        _ls = self.linestyles[stackpos]
        _ls.set_sym_style(_shape)

    #@+node:tom.20211207165051.55: *4* setSymShapeMain
    def setSymShapeMain(self):
        self.setSymShape(MAIN)

    #@+node:tom.20211207165051.56: *4* setSymShapeBuffer
    def setSymShapeBuffer(self):
        self.setSymShape(BUFFER)

    #@+node:tom.20211207165051.57: *4* setXlabel
    def setXlabel(self, label=''):
        self.axes.set_xlabel(label)

    #@+node:tom.20211207165051.58: *4* setYlabel
    def setYlabel(self, label=''):
        self.axes.set_ylabel(label)

    #@+node:tom.20211207165051.59: *4* setFigureTitle
    def setFigureTitle(self, title=''):
        #self.axes.set_title(title, size='x-large', y=1.025)
        self.axes.set_title(title, size='large', y=1.025)

    #@+node:tom.20211207212931.1: *3* Data Load/Save
    #@+node:tom.20211207165051.60: *4* set_data
    def set_data(self, dataset, stackpos=MAIN):
        self.stack[stackpos] = dataset.copy()

    #@+node:tom.20211207165051.61: *4* save_data
    def save_data(self, saveas=True):
        '''Write x,y data in MAIN to an ASCII file.  Labels and other meta data
        are also written.

        ARGUMENT
        saveas -- if True, use Save As dialog.  Otherwise, use original
                  filename if one exists, and use Save As instead.

        RETURNS
        nothing
        '''

        opt = {}

        if self.stack[MAIN].orig_filename:
            opt['initialfile'] = self.stack[MAIN].orig_filename
        if self.initpath:
            opt['initialdir'] = self.initpath

        if saveas:
            fname = fd.asksaveasfilename(**opt)
        else:
            fname = self.stack[MAIN].orig_filename or \
                    fd.asksaveasfilename(**opt)

        self.stack[MAIN].writeAsciiData(fname)
        self.stack[MAIN].orig_filename = fname

    #@+node:tom.20211207165051.62: *4* load_data
    def load_data(self, stackpos=MAIN):
        '''Open a file dialog for reading, and remember its directory and filename.
        Use that last stored directory or file as the initial directory when
        opening the file dialog.  Load the data from the selected file into
        the specified Dataset. Assumes data is in ASCII format.  Plot
        the data if no other data has yet been plotted.
        
        If there are more than two numeric columns,
        show a dialog for the user to select the two columns to use.

        The data set may be divided into parts by the special
        comment string ';;ENDDATASET'.  If so, load each such delineated
        part into stack positions MAIN, BUFFER, and the top-most
        position, if there are enough data parts.

        ARGUMENT
        stackpos -- integer specifying the stack position to load
                    the data into.

        RETURNS
        Nothing.
        '''

        if not self.current_path:
            f = fd.askopenfile(mode='r', initialdir=self.initpath)
        else:
            f = fd.askopenfile(mode='r', initialfile=self.current_path)
        if not f:
            return

        fname = f.name
        data = f.read()
        f.close()

        self.initpath = PurePath(fname).parent
        self.current_path = fname

        blocks = data.split(ENDDATASET)
        numblocks = len(blocks)
        if numblocks < 1:
            self.announce('No data found')
            return

        first_time = self.stack[MAIN].xdata is None

        for n in range(min(len(blocks), STACKDEPTH)):
            block = blocks[n]
            if not block.split():
                continue

            lines = block.split('\n')
            _data = Dataset(None, None, PurePath(fname).name)
            _data.orig_filename = fname
            err = _data.setAsciiData(lines, root = self.root)
            if err:
                self.announce(f'No data in block {n}')
                self.flashit()
                self.announce(f'No data in block {n}')
                print(len(lines), 'lines')
                return

            if n <= BUFFER:
                self.set_data(_data, n)
            elif n == BUFFER + 1:
                self.set_data(_data, STACKDEPTH - 1)

        if first_time:
            self.plot()

    #@+node:tom.20211207165051.63: *4* load_plot_data
    def load_plot_data(self, fname, overplot=False):
        '''Load the data from the specified file into the specified Dataset.
        Load the dataset into the MAIN stack buffer position.
        Assumes data is in ASCII format.  Plot the data if no other
        data has yet been plotted, otherwise plot or overplot it
        according to the value of the overplot parameter.

        ARGUMENT
        fname -- path to a file
        overplot -- Boolean

        RETURNS
        Nothing.
        '''

        with open(fname, encoding = ENCODING) as f:
            data = f.read()

        self.initpath = PurePath(fname).parent

        blocks = data.split(ENDDATASET)
        numblocks = len(blocks)
        if numblocks < 1:
            self.announce('No data found')
            return

        for n in range(min(len(blocks), STACKDEPTH)):
            block = blocks[n]
            lines = block.split('\n')
            _data = Dataset()
            _data.orig_filename = fname
            err = _data.setAsciiData(lines)
            if err:
                self.announce('%s' % err)
                self.flashit()
                self.announce('%s' % err)
                return

            if n <= BUFFER:
                self.set_data(_data, n)
            elif n == BUFFER + 1:
                self.set_data(_data, STACKDEPTH - 1)

        if not self.axes:
            self.plot()
        else:
            if overplot: self.overplot()
            else: self.plot()

    #@+node:tom.20211207165051.64: *4* copy_data_to_clipboard
    def copy_data_to_clipboard(self):
        '''Copy data from MAIN stack buffer position into the clipboad.
        Do not copy any error bands.

        ARGUMENTS
        none

        RETURNS
        nothing
        '''

        _ds = self.stack[MAIN]
        if _ds is None or not any(_ds.xdata):
            self.announce("No data to work with")
            self.flashit()
            return

        _data = _ds.data2String()

        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(_data)
        except Exception as e:
            self.announce("Error wwriting to clipboard: %s" % (e))
            self.flashit()

    #@+node:tom.20211207165051.65: *4* load_data_from_popup
    def load_data_from_popup(self):
        '''Pop up an editor dialog that returns a string of data lines.
        The data set may be divided into parts by the special
        comment string ';; ENDDATASET'.  If so,load  each such delineated
        part into stack positions MAIN, BUFFER, and the top-most
        position, if there are enough data parts.

        Assumes the data is in ASCII format.  Plot the MAIN data if no
        other data has yet been plotted.

        ARGUMENTS
        none

        RETURNS
        nothing
        '''

        data = editDialog(self.root, 'Enter Data').result
        if not data.strip(): return

        blocks = data.split(ENDDATASET)
        numblocks = len(blocks)
        if numblocks < 1:
            self.announce('No data found')
            return

        first_time = self.stack[MAIN].xdata is None

        for n in range(min(len(blocks), STACKDEPTH)):
            block = blocks[n]
            lines = block.split('\n')
            _data = Dataset()
            err = _data.setAsciiData(lines)
            if err:
                self.announce('%s' % err)
                self.flashit()
                self.announce('%s' % err)
            else:
                if n < STACKDEPTH:
                    self.set_data(_data, n)

        if first_time:
            self.plot()
    #@+node:tom.20211207213410.1: *3* Curve Operations
    #@+node:tom.20211207165051.68: *4* setNumPoints
    def setNumPoints(self):
        current = self.num
        dia = GetSingleInt(self.root, 'Set Number Of Points',
                           'Number', current)
        if dia.result is None: return
        self.setNum(dia.result)

    #@+node:tom.20211207165051.69: *4* replaceX
    def replaceX(self):
        '''Replace X axis values.  New values will be uniformly spaced.
        If there are any error bands, replace their axes too.  If either
        the new start value or new delta cannot be an integer, then both
        will be taken to be floating point numbers.
        '''

        _ds = self.stack[MAIN]
        if not (_ds and any(_ds.xdata)):
            self.announce("No data to work with")
            self.flashit()
            return

        _xdata = _ds.xdata

        _id = 'replaceX'
        current = (_xdata[0], _xdata[1] - _xdata[0])
        _start, _delta = self.parmsaver.get(_id, current)
        dia = GetTwoNumbers(self.root, 'Set New X Axis', 'Start',
                            'Increment', _start, _delta)
        if dia.result is None: return

        new_start, new_delta = dia.result
        _ds.xdata = [new_start + 1.0 * n * new_delta for n in
                     range(0, len(_ds.xdata))]

        if _ds.errorBands:
            for eb in _ds.errorBands:
                eb.xdata = _ds.xdata

        self.plot()

        self.parmsaver[_id] = (new_start, new_delta)
    #@+node:tom.20211207165051.70: *4* dedup
    @REQUIRE_MAIN
    def dedup(self):
        self.stack[MAIN].dedup()

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = '%s De-duplicated' % (lab)
        else:
            lab = 'De-duplicated Points'
        self.stack[MAIN].figurelabel = lab

        self.plot()

    #@+node:tom.20211207165051.71: *4* pad_truncate
    @REQUIRE_MAIN
    def pad_truncate(self):
        _ds = self.stack[MAIN]
        num = len(_ds.xdata)

        dia = GetSingleInt(self.root, 'Pad or Truncate Data',
                           'New Number of Points', num)
        if dia.result is None: return

        _ds.pad_truncate(dia.result)

        lab = self.stack[MAIN].figurelabel
        if lab:
            label_str = f'{lab} Padded' if dia.result > num else f'{lab} Truncated'
            self.stack[MAIN].figurelabel = label_str

        self.plot()
    #@+node:tom.20211207165051.73: *4* shift
    @REQUIRE_MAIN
    def shift(self):
        _id = 'shift'
        lastparm = self.parmsaver.get(_id, 0)

        dia = GetSingleInt(self.root, 'Shift Horizontally',
                           'Distance', lastparm)
        if dia.result is None: return

        self.parmsaver[_id] = dia.result

        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = f'Shifted {lab}'

        self.stack[MAIN].shift(dia.result)
        self.plot()
    #@+node:tom.20211207165051.74: *4* transpose
    @REQUIRE_MAIN
    def transpose(self):
        if not self.stack[MAIN]:
            self.announce("No data to work with")
            self.flashit()
            return None, None

        _ds = self.stack[MAIN]
        _ds.transpose()
        self.plot()

        return _ds, Dataset.transpose
    #@+node:tom.20211207165051.75: *4* sortX
    @REQUIRE_MAIN
    def sortX(self):
        self.stack[MAIN].sortX()
        self.plot()
    #@+node:tom.20211207213522.1: *3* Curve Math
    #@+node:tom.20211207165051.76: *4* scale
    @REQUIRE_MAIN
    def scale(self):
        _id = 'scale'
        lastparm = self.parmsaver.get(_id, 1.0)
        dia = GetSingleFloat(self.root, 'Scale Y Data',
                             'Scaling Factor', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        _ds = self.stack[MAIN]
        _ds.scale(dia.result)

        if _ds.errorBands:
            _ds.errorBands[0].scale(dia.result)
            _ds.errorBands[1].scale(dia.result)

        self.plot()
    #@+node:tom.20211207165051.77: *4* add_constant
    @REQUIRE_MAIN
    def add_constant(self):
        _ds = self.stack[MAIN]

        _id = 'add_constant'
        lastparm = self.parmsaver.get(_id, 0.0)
        dia = GetSingleFloat(self.root,
                             'Add Constant To Y Data', 'Constant',
                             lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        _ds.addConstant(dia.result)

        if _ds.errorBands:
            _ds.errorBands[0].addConstant(dia.result)
            _ds.errorBands[1].addConstant(dia.result)

        self.plot()
    #@+node:tom.20211207165051.78: *4* differentiate
    @REQUIRE_MAIN
    def differentiate(self):
        self.stack[MAIN].differentiate()
        self.stack[MAIN].figurelabel = ' Derivative of %s' % \
            (self.stack[MAIN].figurelabel)
        self.plot()
    #@+node:tom.20211207165051.79: *4* differentiate2
    @REQUIRE_MAIN
    def differentiate2(self):
        self.stack[MAIN].differentiate2()
        self.stack[MAIN].figurelabel = ' Derivative of %s' % \
            (self.stack[MAIN].figurelabel)
        self.plot()
    #@+node:tom.20211207165051.80: *4* integrate
    @REQUIRE_MAIN
    def integrate(self):
        self.stack[MAIN].integrate()
        lab = self.stack[MAIN].figurelabel
        if lab:
            self.stack[MAIN].figurelabel = ' Integral of %s' % (lab)
        self.plot()
    #@+node:tom.20211207165051.81: *4* absolute
    @REQUIRE_MAIN
    def absolute(self):
        self.stack[MAIN].absolute()
        lab = self.stack[MAIN].figurelabel
        if lab:
            self.stack[MAIN].figurelabel = ' Absolute Value of %s' % (lab)
        self.plot()
    #@+node:tom.20211207165051.82: *4* square
    @REQUIRE_MAIN
    def square(self):
        self.stack[MAIN].square()
        lab = self.stack[MAIN].figurelabel
        if lab:
            self.stack[MAIN].figurelabel = ' Square of %s' % (lab)
        self.plot()
    #@+node:tom.20211207165051.83: *4* rectify
    @REQUIRE_MAIN
    def rectify(self):
        self.stack[MAIN].ydata = [abs(y) for y in self.stack[MAIN].ydata]
        lab = self.stack[MAIN].figurelabel or ''
        lab += ' Rectified'
        self.stack[MAIN].figurelabel = lab
        self.plot()
    #@+node:tom.20211207165051.84: *4* half_rectify
    @REQUIRE_MAIN
    def half_rectify(self):
        self.stack[MAIN].ydata = [max(y, 0.) for y in self.stack[MAIN].ydata]
        lab = self.stack[MAIN].figurelabel or ''
        lab += ' Half Wave Rectified'
        self.stack[MAIN].figurelabel = lab
        self.plot()
    #@+node:tom.20211207165051.85: *4* clip
    @REQUIRE_MAIN
    def clip(self):
        _id = 'clip'
        lastparm = self.parmsaver.get(_id, 1.0)
        dia = GetSingleFloat(self.root, 'Clipping Level',
                             'Clip', lastparm)
        if dia.result is None: return

        self.parmsaver[_id] = abs(dia.result)
        clip = abs(dia.result)
        _y = []
        for y in self.stack[MAIN].ydata:
            if y >= 0:
                _y.append(min(y, clip))
            else:
                _y.append(-min(-y, clip))
        self.stack[MAIN].ydata = _y
        lab = self.stack[MAIN].figurelabel or ''
        lab += ' Clipped'
        self.stack[MAIN].figurelabel += lab
        self.plot()
    #@+node:tom.20211207165051.86: *4* decimate
    @REQUIRE_MAIN
    def decimate(self):
        _id = 'decimate'
        current = 12
        delta = self.parmsaver.get(_id, current)
        dia = GetSingleInt(self.root, 'Thin X Axis', 'Keep 1 in ', delta)
        if dia.result is None: return

        delta = dia.result
        self.parmsaver[_id] = delta

        _ds = self.stack[MAIN]
        lab = self.stack[MAIN].figurelabel or ''
        lab = '%s Thinned To One in %s' % (lab, delta)

        self.stack[MAIN] = _ds.thin(delta)
        self.stack[MAIN].figurelabel = lab

        self.plot()
    #@+node:tom.20211207165051.87: *4* trim
    @REQUIRE_MAIN
    def trim(self):
        _id = 'trim'
        default = 0
        N = self.parmsaver.get(_id, default)
        dia = GetSingleInt(self.root, 'Trim Data', 'Integer # to Remove', N)
        N = dia.result or 0
        self.parmsaver[_id] = N

        _ds = self.stack[MAIN]
        if N > 0:
            _ds.xdata = _ds.xdata[:-N]
            _ds.ydata = _ds.ydata[:-N]
        elif N < 0:
            _ds.xdata = _ds.xdata[-N:]
            _ds.ydata = _ds.ydata[-N:]

        lab = self.stack[MAIN].figurelabel or ''
        lab = '%s Trimmed by %s' % (lab, N)
        self.stack[MAIN].figurelabel = lab

        self.plot()
    #@+node:tom.20211207165051.88: *4* log
    @REQUIRE_MAIN
    def log(self):
        success = self.stack[MAIN].log()
        if not success:
            self.announce("Data contains 0 or negative values - can't take its log")
            self.flashit()
            return
        lab = self.stack[MAIN].figurelabel
        if lab:
            self.stack[MAIN].figurelabel = 'Natural Log of %s' % (lab)
        self.plot()
    #@+node:tom.20211207165051.89: *4* log10
    @REQUIRE_MAIN
    def log10(self):
        success = self.stack[MAIN].log10()
        if not success:
            self.announce("Data contains 0 or negative values - can't take its log")
            self.flashit()
            return
        lab = self.stack[MAIN].figurelabel
        if lab:
            self.stack[MAIN].figurelabel = 'Log base 10 of %s' % (lab)
        self.plot()
    #@+node:tom.20211207165051.122: *4* normalize
    @REQUIRE_MAIN
    def normalize(self):
        """ Normalize the X data to 1.0.  Replot.
        """
        self.stack[MAIN].normalize()

        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = f'Normalized {lab}'

        self.plot()
    #@+node:tom.20211207165051.90: *4* mulBuffer
    @REQUIRE_MAIN_BUFF
    def mulBuffer(self):
        success = self.stack[MAIN].multiply(self.stack[BUFFER])
        if not success:
            self.announce("Number of data points differs (main: %s, buff: %s)"
                          "- can't multiply"
                          % (len(self.stack[MAIN].xdata),
                             len(self.stack[BUFFER].xdata)))
            self.flashit()
            return

        lab = self.stack[MAIN].figurelabel or ''
        lab1 = self.stack[BUFFER].figurelabel or ''
        if lab and lab1:
            self.stack[MAIN].figurelabel = '%s * %s' % (lab, lab1)
        else:
            self.stack[MAIN].figurelabel = 'Product'

        self.plot()
    #@+node:tom.20211207165051.91: *4* divBuffer
    @REQUIRE_MAIN_BUFF
    def divBuffer(self):
        '''Divide BUFFER by MAIN, pointwise. Return result in MAIN,
        and plot MAIN'''

        success = self.stack[MAIN].divide(self.stack[BUFFER])
        if not success:
            self.announce(
                "Zero in denominator or Number of data points differs"
                " (main: %s, buff: %s)- can't divide"
                % (len(self.stack[MAIN].xdata), len(self.stack[BUFFER].xdata)))
            self.flashit()
            return

        mainlab = self.stack[MAIN].figurelabel or ''
        bufflab = self.stack[BUFFER].figurelabel or ''
        if mainlab and bufflab:
            self.stack[MAIN].figurelabel = '%s / %s' % (bufflab, mainlab)
        else:
            self.stack[MAIN].figurelabel = 'Quotient'

        self.plot()
        if self.stack[MAIN].xdata != self.stack[BUFFER].xdata:
            self.announce('WARNING: The two data sets had different'
                          ' X-axis values')
            self.flashit()
    #@+node:tom.20211207165051.92: *4* addBuffer
    @REQUIRE_MAIN_BUFF
    def addBuffer(self):
        '''Add y data in the buffer to y data in the main data set,
        point by point. store the result in MAIN.  Plot the result.

        Assumes that the x values are the same for both sequences.
        The only check made is whether the length of both arrays is the same.
        If not, write a message and return without doing anything.
        '''

        _m = self.stack[MAIN]
        _b = self.stack[BUFFER]

        if len(_m) != len(_b):
            self.announce(
                'MAIN and BUFFER must have the same number of points '
                '(main: %s, buff: %s)'
                % (len(self.stack[MAIN].xdata),
                   len(self.stack[BUFFER].xdata)))
            self.flashit()
            return

        if _m.isNumpyArray(_m.ydata):
            _my = _m.ydata.tolist()
        else:
            _my = _m.ydata

        if _b.isNumpyArray(_b.ydata):
            _by = _b.ydata.tolist()
        else:
            _by = _b.ydata

        result = []
        for n, _ in enumerate(_my):
            result.append(_my[n] + _by[n])

        _m.ydata = result

        lab = self.stack[MAIN].figurelabel or ''
        lab1 = self.stack[BUFFER].figurelabel or ''
        if lab and lab1:
            self.stack[MAIN].figurelabel = '%s + %s' % (lab, lab1)
        else:
            self.stack[MAIN].figurelabel = 'Sum'

        self.plot()
    #@+node:tom.20211207165051.93: *4* subFromBuffer
    @REQUIRE_MAIN_BUFF
    def subFromBuffer(self):
        '''subtract y data in the main data set from y data in thebuffer,
        point by point. store the result in MAIN.  Plot the result.

        Assumes that the x values are the same for both sequences.
        The only check made is whether the length of both arrays is the same.
        If not, write a message and return without doing anything.
        '''

        _m = self.stack[MAIN]
        _b = self.stack[BUFFER]

        if len(_m) != len(_b):
            self.announce(
                'MAIN and BUFFER must have the same number of points '
                '(main: %s, buff: %s)'
                % (len(self.stack[MAIN].xdata),
                   len(self.stack[BUFFER].xdata)))
            self.flashit()
            return

        if _m.isNumpyArray(_m.ydata):
            _my = _m.ydata.tolist()
        else:
            _my = _m.ydata

        if _b.isNumpyArray(_b.ydata):
            _by = _b.ydata.tolist()
        else:
            _by = _b.ydata

        _m.ydata = [y - x for x, y in zip(_my, _by)]

        lab = self.stack[MAIN].figurelabel or ''
        lab1 = self.stack[BUFFER].figurelabel or ''
        if lab and lab1:
            self.stack[MAIN].figurelabel = '%s - %s' % (lab1, lab)
        else:
            self.stack[MAIN].figurelabel = 'Difference'

        self.plot()

        # return _m, suby
    #@+node:tom.20211207165051.113: *4* make_phasespace
    @REQUIRE_MAIN
    def make_phasespace(self):
        '''Replace the X axis data of the MAIN ds by replacing the x axis
           data with the ydata shifted left by one step.  That is,
           x[i] = y[i-1]. The non-overlapping ends are trimmed.
           Plot the new data set.
        '''

        _id = 'phasespace'
        lastparm = self.parmsaver.get(_id, 1)
        dia = GetSingleInt(self.root,
                             'Shift X Data', 'Points To Shift',
                             lastparm)
        if dia.result is None: return
        N = dia.result
        self.parmsaver[_id] = N

        _ds = self.stack[MAIN]
        _y = _ds.ydata

        _ds.shift(N)
        # Remove points zeroed by the shift
        if N >= 0:
            _ds.xdata = _y[N:]
            _ds.ydata = _ds.ydata[N:]
        else:
            _ds.xdata = _y[:N]
            _ds.ydata = _ds.ydata[:N]
        lag = f'+ {N}' if N >= 0 else f'- {-N}'
        _ds.figurelabel = f'"Phase Space" for {_ds.figurelabel} (Lag {lag})'
        _ds.xaxislabel = 'Y(t)'
        _ds.yaxislabel = f'Y(t {lag})'
        self.plot()
    #@+node:tom.20211207165051.114: *4* YvsX
    @REQUIRE_MAIN
    def YvsX(self):
        '''Replace the x axis of the data in X with its y data.
        Replace the y axis of the x data with the y data of
        the data in Y.  Plot the result.  The effect is to
        plot Y vs X.  For this to make sense, both data sets
        must have data for the same x-axis values (e.g., time).

        A check is made to make sure the two curves have the same
        number of points.

        The result is sorted on the x axis.
        '''

        _X = self.stack[MAIN]
        _Y = self.stack[BUFFER]
        _x = _X.ydata[:]
        _y = _Y.ydata[:]

        if not len(_x) == len(_y):
            self.announce('X and Y data must have the same number of points')
            self.flashit()
            return

        _X.xdata = _x
        _X.ydata = _y
        _X.figurelabel = '%s vs %s' % (_X.figurelabel, _Y.figurelabel)
        _X.xaxislabel = _X.yaxislabel
        _X.yaxislabel = _Y.yaxislabel

        #self.sortX()
        self.plot()
    #@+node:tom.20220806224143.1: *4* zero
    @REQUIRE_MAIN
    def zero(self):
        """Subtract the mean of the Y data of the MAIN Dataset. Replot"""
        self.stack[MAIN].zero()

        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = f'{lab} Zeroed'

        self.plot()
    #@+node:tom.20211207213812.1: *3* Data Processing
    #@+node:tom.20211207165051.123: *4* fft
    @REQUIRE_MAIN
    def fft(self):
        self.stack[MAIN].rfft()
        lab = self.stack[MAIN].figurelabel
        if lab:
            self.stack[MAIN].figurelabel = 'FFT of %s' % (lab)
        self.stack[MAIN].xaxislabel = 'Frequency'
        self.stack[MAIN].yaxislabel = 'Relative Amplitude'
        self.plot()
    #@+node:tom.20211207165051.97: *4* lopass
    @REQUIRE_MAIN
    def lopass(self):
        _id = 'lopass'
        lastparm = self.parmsaver.get(_id, 5.0)

        dia = GetSingleFloat(self.root, 'Time constant in units of dt',
                             'Tau', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        if self.stack[MAIN].lopass(dia.result):
            lab = self.stack[MAIN].figurelabel or ''
            if lab:
                lab = 'Low Pass Filter of %s' % (lab)
            else:
                lab = 'Low Pass Filter'
            self.stack[MAIN].figurelabel = lab

            self.plot()
        else:
            self.announce('tau  <= 0.0 or no data')
            self.flashit()
    #@+node:tom.20211207165051.98: *4* hipass
    @REQUIRE_MAIN
    def hipass(self):
        _id = 'hipass'
        lastparm = self.parmsaver.get(_id, 5.0)
        _LIMIT = 0.1

        dia = GetSingleFloat(self.root, 'Time constant in units of dt',
                             'Tau', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        if self.stack[MAIN].hipass(dia.result, _LIMIT):
            lab = self.stack[MAIN].figurelabel or ''
            if lab:
                lab = 'High Pass Filter of %s' % (lab)
            else:
                lab = 'High Pass Filter'
            self.stack[MAIN].figurelabel = lab

            self.plot()
        else:
            self.announce('tau  <= %s or no data' % _LIMIT)
            self.flashit()
    #@+node:tom.20211207165051.95: *4* correlateWithBuffer
    @REQUIRE_MAIN
    def correlateWithBuffer(self):
        self.stack[MAIN].correlate(self.stack[BUFFER])

        lab = self.stack[MAIN].figurelabel or ''
        lab1 = self.stack[BUFFER].figurelabel or ''
        if lab:
            self.stack[MAIN].figurelabel = 'Correlation of %s' % (lab)
            if lab1:
                self.stack[MAIN].figurelabel += ' with %s' % (lab1)
        else:
            self.stack[MAIN].figurelabel = 'Correlation'

        self.plot()
    #@+node:tom.20211207165051.94: *4* convolveWithBuffer
    @REQUIRE_MAIN
    def convolveWithBuffer(self):
        lab = self.stack[MAIN].figurelabel or ''
        lab1 = self.stack[BUFFER].figurelabel or ''

        d1 = self.stack[MAIN]
        d2 = self.stack[BUFFER]

        d1.convolve(d2)

        if lab:
            self.stack[MAIN].figurelabel = 'Convolution of %s' % (lab)
            if lab1:
                self.stack[MAIN].figurelabel += ' with %s' % (lab1)
        else:
            self.stack[MAIN].figurelabel = 'Convolution'

        self.plot()
    #@+node:tom.20211207165051.96: *4* autocorrelate
    @REQUIRE_MAIN
    def autocorrelate(self):
        self.stack[MAIN].correlate(self.stack[MAIN])

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            self.stack[MAIN].figurelabel = 'Autocorrelation of %s' % (lab)
        else:
            self.stack[MAIN].figurelabel = 'Autocorrelation'

        self.plot()
    #@+node:tom.20221104001727.1: *4* partial_autocorrel
    @REQUIRE_MAIN
    def partial_autocorr(self):
        _ds = self.stack[MAIN]
        partial_ac, conf_bands = pacf(_ds.ydata, alpha = .05, method = 'ywm')

        new_x = [n for n in range(len(partial_ac))]
        _ds.ydata = partial_ac
        _ds.xdata = new_x

        # Error bands
        low, hi = list(zip(*conf_bands))
        upper = Dataset(new_x, hi)
        lower = Dataset(new_x, low)
        _ds.errorBands = [upper, lower]

        lab = _ds.figurelabel.strip() or ''
        lab = 'Partial Autocorrelation of ' + lab
        _ds.figurelabel = lab
        _ds.xaxislabel = 'Lag'
        _ds.yaxislabel = 'Autocorrelation'

        self.plot()
    #@+node:tom.20211207165051.99: *4* moving_median
    @REQUIRE_MAIN
    def moving_median(self):
        _id = 'moving_median'
        lastparm = self.parmsaver.get(_id, 5)

        dia = GetSingleInt(self.root, 'Window Width (odd)',
                             'Width', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        _x = self.stack[MAIN].xdata
        _y = self.stack[MAIN].ydata

        self.stack[MAIN].xdata, self.stack[MAIN].ydata = \
            smoother.moving_median(_x, _y, dia.result)
        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = 'Moving Median of %s' % (lab)
        else:
            lab = 'Moving Median'
        self.stack[MAIN].figurelabel = lab

        self.plot()
    #@+node:tom.20211207213827.1: *3* Fit
    #@+node:tom.20211207165051.100: *4* cubicSpline
    @REQUIRE_MAIN
    def cubicSpline(self):
        _ds = self.stack[MAIN]
        _x = _ds.xdata
        _y = _ds.ydata
        _ds.xdata, _ds.ydata = smoother.cspline(_x, _y)
        self.plot()
    #@+node:tom.20211207165051.72: *4* fit_piecewise
    @REQUIRE_MAIN
    def fit_piecewise(self):
        _ds = self.stack[MAIN]
        _id = 'fit_piecewise'
        lastparm = self.parmsaver.get(_id, 2)

        dia = GetSingleInt(self.root, 'Piecewise Linear Fit',
                           'Number of Segments to Use', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        _fitted = piecewiseLinear(_ds.xdata, _ds.ydata, dia.result)
        _ds.ydata = _fitted

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = 'Piecewise Linear Fit to %s' % (lab)
        else:
            lab = 'Piecewise Linear Fit'
        self.stack[MAIN].figurelabel = lab

        self.plot()
    #@+node:tom.20211207165051.110: *4* leastsqr
    @REQUIRE_MAIN
    def leastsqr(self):
        _ds = self.stack[MAIN]
        _x = _ds.xdata
        _y = _ds.ydata

        newy, mean, rms, r, upperbound, lowerbound = smoother.leastsqr(_x, _y)
        _ds.ydata = newy

        lower = Dataset()
        lower.ydata = lowerbound
        lower.xdata = _x

        upper = Dataset()
        upper.ydata = upperbound
        upper.xdata = _x

        # Subgraphs get stored in the errorBands list
        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        if _ds.figurelabel:
            _ds.figurelabel = 'Least Squares Fit to %s' % (_ds.figurelabel)
        else:
            _ds.figurelabel = 'Least Squares Fit'

        self.plot()
        self.announce('Mean=%0.3f, rms = %0.3f, r=%0.3f' % (mean, rms, r))
    #@+node:tom.20211207165051.111: *4* leastsqr_quad
    @REQUIRE_MAIN
    def leastsqr_quad(self):
        _ds = self.stack[MAIN]

        _x = _ds.xdata
        _y = _ds.ydata

        newy, mean, rms, r, upperbound, lowerbound = \
            smoother.leastsqr(_x, _y, 2)
        _ds.ydata = newy

        lower = Dataset()
        lower.ydata = lowerbound
        lower.xdata = _x

        upper = Dataset()
        upper.ydata = upperbound
        upper.xdata = _x

        # Subgraphs get stored in the errorBands list
        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        if _ds.figurelabel:
            _ds.figurelabel = 'Least Squares Quadratic Fit to %s' \
                % (_ds.figurelabel)
        else:
            _ds.figurelabel = 'Least Squares Quadratic Fit'

        self.plot()
        self.announce('Mean=%0.3f, rms=%0.3f, r=%0.3f' % (mean, rms, r))
    #@+node:tom.20211207165051.112: *4* thiel
    @REQUIRE_MAIN
    def thiel(self):
        _ds = self.stack[MAIN]
        _x = _ds.xdata
        _y = _ds.ydata

        fitted, slope, intercept, sd_slope = smoother.thiel_sen(_x, _y)
        _ds.ydata = fitted

        if _ds.figurelabel:
            _ds.figurelabel = 'Thiel-Sen Fit to %s' % (_ds.figurelabel)
        else:
            _ds.figurelabel = 'Thiel-Sen Least Squares Fit'

        self.plot()

        slope_str = 'Slope = %0.2g, ' % (slope)
        int_str = 'Intercept = %0.3g, ' % (intercept)
        sd_str = 'Estimated S.D. of slope: %0.3g, ' % (sd_slope)
        self.announce(slope_str + int_str + sd_str)
    #@+node:tom.20220402083822.1: *3* Plot Operations
    #@+node:tom.20211207165051.29: *4* overplotbuff
    def overplotbuff(self):
        self.overplot(BUFFER)

    #@+node:tom.20211207165051.30: *4* overplot_errorbands
    def overplot_errorbands(self, stackposition=MAIN):
        if not self.stack[stackposition].errorBands:
            self.announce('No errorband data to plot')
            self.flashit()
            return

        _ds = self.stack[stackposition]

        # Overplot error bands
        upper = _ds.errorBands[ERRBAND_HI]
        lower = _ds.errorBands[ERRBAND_LO]

        del self.stack[STACKDEPTH:]
        self.stack.append(upper)
        self.stack.append(lower)

        self.axes.fill_between(self.stack[MAIN].xdata,
                self.stack[STACKDEPTH + ERRBAND_HI].ydata,
                self.stack[STACKDEPTH + ERRBAND_LO].ydata,
                facecolor='lightgrey', alpha=0.1)

        for g in [STACKDEPTH + ERRBAND_HI, STACKDEPTH + ERRBAND_LO]:
            self.overplot(g)

    #@+node:tom.20211207165051.31: *4* overplot
    def overplot(self, stackposition=MAIN):
        self.plot(stackposition, False)

    #@+node:tom.20211207214009.1: *3* Smoothing
    #@+node:tom.20211207165051.101: *4* lowess
    @REQUIRE_MAIN
    def lowess(self):
        _ds = self.stack[MAIN]
        if _ds.isNumpyArray(_ds.xdata):
            _x = _ds.xdata.tolist()
        else:
            _x = _ds.xdata
        if _ds.isNumpyArray(_ds.ydata):
            _y = _ds.ydata.tolist()
        else:
            _y = _ds.ydata

        _id = 'lowess'
        lastparm = self.parmsaver.get(_id, 6)

        dia = GetSingleInt(self.root, 'Smoothing Width', 'Enter Integer',
                           lastparm)
        if dia.result is None: return

        self.parmsaver[_id] = dia.result
        self.stack[MAIN].parms['smoothwidth'] = '%s' % (dia.result)

        x, newy, rms, upperlimit, lowerlimit = smoother.lowess2(_x, _y,
                                                                dia.result)
        _ds.ydata = newy

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = f'LOWESS Smooth ({dia.result}) of {lab}'
        else:
            lab = f'LOWESS Smooth ({dia.result})'
        self.stack[MAIN].figurelabel = lab

        lower = Dataset()
        lower.ydata = lowerlimit
        lower.xdata = _x  # not a copy

        upper = Dataset()
        upper.ydata = upperlimit
        upper.xdata = _x  # not a copy

        # Subgraphs get stored in the errorBands list
        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        # correlation coefficient
        r = smoother.correlationCoeff(_y, newy)

        self.plot()

        n = float(len(_x))
        msg = f'RMS deviation = {rms:.3f}, r = {r:.3f}'
        self.announce(msg)
    #@+node:tom.20211207165051.102: *4* lowess2Quad
    @REQUIRE_MAIN
    def lowess2Quad(self):
        _ds = self.stack[MAIN]
        if _ds.isNumpyArray(_ds.xdata):
            _x = _ds.xdata.tolist()
        else:
            _x = _ds.xdata
        if _ds.isNumpyArray(_ds.ydata):
            _y = _ds.ydata.tolist()
        else:
            _y = _ds.ydata

        _id = 'lowess2Quad'
        lastparm = self.parmsaver.get(_id, 6)

        dia = GetSingleInt(self.root, 'Smoothing Width', 'Enter Integer',
                           lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        x, newy, rms, upperlimit, lowerlimit = smoother.lowess2Quad(_x, _y,
                                                                    dia.result)
        _ds.ydata = newy

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = 'LOWESS Quadratic Smooth of %s' % (lab)
        else:
            lab = 'LOWESS Quadratic Smooth'
        self.stack[MAIN].figurelabel = lab

        lower = Dataset()
        lower.ydata = lowerlimit
        lower.xdata = _x

        upper = Dataset()
        upper.ydata = upperlimit
        upper.xdata = _x

        # Subgraphs get stored in the errorBands list
        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        # correlation coefficient
        r = smoother.correlationCoeff(_y, newy)

        self.plot()

        self.announce('RMS Deviation: %0.3f, r=%0.3f' % (rms, r))
    #@+node:tom.20211207165051.103: *4* lowess_adaptive
    @REQUIRE_MAIN
    def lowess_adaptive(self):
        _ds = self.stack[MAIN]
        if _ds.isNumpyArray(_ds.xdata):
            _x = _ds.xdata.tolist()
        else:
            _x = _ds.xdata
        if _ds.isNumpyArray(_ds.ydata):
            _y = _ds.ydata.tolist()
        else:
            _y = _ds.ydata

        _id = 'lowess_adaptive'
        lastparm = self.parmsaver.get(_id, 1.0)

        dia = GetSingleFloat(self.root, 'Smoothness Weight',
                             'Enter Number', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        x, newy, span, rms, upperlimit, lowerlimit = \
            smoother.lowessAdaptive(_x, _y, dia.result)
        _ds.ydata = newy

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = 'Adaptive LOWESS Smooth of %s' % (lab)
        else:
            lab = 'Adaptive LOWESS Smooth'
        self.stack[MAIN].figurelabel = lab

        lower = Dataset()
        lower.ydata = lowerlimit
        lower.xdata = _x

        upper = Dataset()
        upper.ydata = upperlimit
        upper.xdata = _x

        # Subgraphs get stored in the errorBands list
        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        # correlation coefficient
        r = smoother.correlationCoeff(_y, newy)

        self.plot()
        msg = f'Span: {span}, RMS deviation = {rms:.3f}, r = {r:.3f}'
        self.announce(msg)
    #@+node:tom.20211207165051.104: *4* lowess_adaptive_ac
    @REQUIRE_MAIN
    def lowess_adaptive_ac(self):
        _ds = self.stack[MAIN]
        if _ds.isNumpyArray(_ds.xdata):
            _x = _ds.xdata.tolist()
        else:
            _x = _ds.xdata
        if _ds.isNumpyArray(_ds.ydata):
            _y = _ds.ydata.tolist()
        else:
            _y = _ds.ydata

        x, newy, span, rms, ac, upperlimit, lowerlimit = \
            smoother.lowessAdaptiveAC(_x, _y)
        _ds.ydata = newy

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = 'Adaptive LOWESS Autocorrelation Smooth of %s' % (lab)
        else:
            lab = 'Adaptive LOWESS Autocorrelation Smooth'
        self.stack[MAIN].figurelabel = lab

        lower = Dataset()
        lower.ydata = lowerlimit
        lower.xdata = _x

        upper = Dataset()
        upper.ydata = upperlimit
        upper.xdata = _x

        # Subgraphs get stored in the errorBands list
        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        # correlation coefficient
        r = smoother.correlationCoeff(_y, newy)

        self.plot()
        self.announce('Span: %s; ac = %0.3f; RMS deviation = %0.3f, '
                      'r=%0.3f' % (span, ac, rms, r))
    #@+node:tom.20211207165051.105: *4* correlationCoeff
    @REQUIRE_MAIN
    def correlationCoeff(self):
        '''Calculate correlation coefficient between MAIN and BUFFER,
        and display the result.  MAIN should be fitted to data in BUFFER,
        e.g., by least squares.   Both sequences must have the same length.
        '''

        fitted = self.stack[MAIN].ydata
        data = self.stack[BUFFER].ydata

        if len(fitted) != len(data):
            self.announce('Both curves must have same number of points: '
                          'fitted: %s, data: %s'
                          % (len(fitted), len(data)))
            self.flashit()
            return

        r = smoother.correlationCoeff(data, fitted)
        if r == -1:
            self.announce('Too much variation in BUFFER, or '
                          'no variation in MAIN')
            self.flashit()
        else:
            self.announce('r=%0.3f' % r)
    #@+node:tom.20211207165051.106: *4* poissonSmooth
    @REQUIRE_MAIN
    def poissonSmooth(self):
        _ds = self.stack[MAIN]
        if _ds.isNumpyArray(_ds.xdata):
            _x = _ds.xdata.tolist()
        else:
            _x = _ds.xdata
        if _ds.isNumpyArray(_ds.ydata):
            _y = _ds.ydata.tolist()
        else:
            _y = _ds.ydata

        _id = 'poissonSmooth'
        lastparm = self.parmsaver.get(_id, 6)

        dia = GetSingleInt(self.root, 'Smoothing Width', 'Enter Integer',
                           lastparm)
        if dia.result is None: return

        self.parmsaver[_id] = dia.result
        self.stack[MAIN].parms['smoothwidth'] = '%s' % (dia.result)

        try:
            x, newy, rms = smoother.poissonSmooth(_x, _y, dia.result)
        except ValueError as e:
            self.announce(e)
            self.flashit()
            return

        _ds.ydata = newy
        _ds.xdata = x  # may have been sorted, so use the return values

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = 'Poisson Smooth of %s' % (lab)
        else:
            lab = 'Poisson Smooth'
        self.stack[MAIN].figurelabel = lab

        # correlation coefficient
        r = smoother.correlationCoeff(_y, newy)

        self.plot()

        self.announce('RMS Deviation: %0.3f, r=%0.3f' % (rms, r))
    #@+node:tom.20211207165051.115: *4* spline_smooth
    @REQUIRE_MAIN
    def spline_smooth(self):
        _ds = self.stack[MAIN]
        _id = 'spline_smooth'
        lastparm = self.parmsaver.get(_id, 0.3)

        _x = _ds.xdata
        _y = _ds.ydata
        dia = GetSingleFloat(self.root, 'Smoothing Width',
                             'Enter Number Between 0 and 1', lastparm)
        if not dia.result:
            return
        self.parmsaver[_id] = dia.result

        x, newy = smoother.splineSmooth(_x, _y, dia.result)
        _ds.ydata = newy

        lab = _ds.figurelabel or ''
        if lab:
            lab = ' Spline Smooth of %s' % (lab)
        else:
            lab = ' Spline Smooth'
        _ds.figurelabel = lab

        self.plot()
    #@+node:tom.20211207214046.1: *3* Statistics
    #@+node:tom.20211207165051.107: *4* spearman
    @REQUIRE_MAIN_BUFF
    def spearman(self):
        '''Calculate the Spearman rank correlation coefficient of
        data sequences in MAIN and BUFFER.  The data remains unchanged.'''

        _y = self.stack[MAIN].ydata
        _x = self.stack[BUFFER].ydata

        if not (len(_x) and len(_y)):
            self.announce('One or both data sets are empty')
            self.flashit()
            return

        if len(_x) != len(_y):
            self.announce('Both curves must have same number of points: '
                          'fitted: %s, data: %s'
                          % (len(_x), len(_y)))
            self.flashit()
            return

        are_equal = all([x == y for x, y in zip(_x, _y)])
        if are_equal:
            self.announce("Both data sets are the same")
            self.flashit()
            return

        r, p = spearmanr(_y, _x)

        self.announce('Spearman Rank Correlation Coefficient='
                      '%0.3g, p = %0.3g' % (r, p))

    #@+node:tom.20211207165051.108: *4* pearson
    @REQUIRE_MAIN_BUFF
    def pearson(self):
        '''Calculate the Spearman rank correlation coefficient of
        data sequences in MAIN and BUFFER.  The data remains unchanged.'''

        _y = self.stack[MAIN].ydata
        _x = self.stack[BUFFER].ydata

        if len(_x) != len(_y):
            self.announce('Both curves must have same number of points: '
                          'fitted: %s, data: %s'
                          % (len(_x), len(_y)))
            self.flashit()
            return

        r = stats.pearson(_y, _x)

        if r is None:
            self.announce("Failed: data lengths don't match")
            self.flashit()
        else:
            self.announce("Pearson's Correlation Coefficient=%0.3g" % (r))

    #@+node:tom.20211207165051.116: *4* cdf
    @REQUIRE_MAIN
    def cdf(self):
        _ds = self.stack[MAIN]
        ydata = _ds.ydata
        newx, newy, upperbounds, lowerbounds = stats.cdf(ydata)
        _ds.xdata = newx
        _ds.ydata = newy
        _lab = 'CDF'
        if _ds.figurelabel:
            _lab = _lab + ' of %s' % (_ds.figurelabel)
        _ds.figurelabel = _lab
        _ds.yaxislabel = 'P'
        _ds.xaxislabel = 'Value'

        lower = Dataset()
        lower.ydata = lowerbounds
        lower.xdata = newx

        upper = Dataset()
        upper.ydata = upperbounds
        upper.xdata = newx

        _ds.errorBands = []
        _ds.errorBands.append(upper)
        _ds.errorBands.append(lower)

        self.plot()

    #@+node:tom.20211207165051.118: *4* fitCdfWithNormal
    @REQUIRE_MAIN
    def fitCdfWithNormal(self):
        _ds = self.stack[MAIN]
        _newx, _newy, mean, sigma = \
            stats.fitNormalToCdf(_ds.xdata, _ds.ydata, self.num)
        _ds.xdata = _newx
        _ds.ydata = _newy
        if _ds.figurelabel:
            _lab = 'CDF Fitted to %s' % (_ds.figurelabel)
        else:
            _lab = 'Fitted CDF'
        _ds.figurelabel = _lab
        self.plot()
        self.announce('mean: %0.3f,sigma: %0.3f'
                      % (mean, sigma))
    #@+node:tom.20211207165051.119: *4* fitCdfNormalAdaptive
    @REQUIRE_MAIN
    def fitCdfNormalAdaptive(self):
        _ds = self.stack[MAIN]
        values = _ds.xdata
        probs = _ds.ydata
        _newx, _newy, mean, sigma, correl = \
            stats.fitNormalToCdfAdaptive(values, probs, 0.001)
        _ds.xdata = _newx
        _ds.ydata = _newy

        if _ds.figurelabel:
            _lab = 'Adaptive Normal Fit to %s' % (_ds.figurelabel)
        else:
            _lab = 'Adaptive Normal Fit to CDF'
        _ds.figurelabel = _lab
        self.plot()
        self.announce('mean: %0.3f,sigma: %0.3f, correlation coeff: %0.3f'
                      % (mean, sigma, correl))

    #@+node:tom.20211207165051.120: *4* histogram
    @REQUIRE_MAIN
    def histogram(self):
        _id = 'histogram'
        lastparm = self.parmsaver.get(_id, 10)

        dia = GetSingleInt(self.root, ' Histogram', 'Number Of Bins', lastparm)
        if not dia.result:
            return
        self.parmsaver[_id] = dia.result
        bins = dia.result

        _ds = self.stack[MAIN]
        ydata = _ds.ydata
        if bins >= len(ydata):
            self.announce(
                'Too many bins - must be less than number of points'
                '(%s)' % (len(ydata)))
            self.flashit()
            return

        newx, newy = stats.histogram(ydata, bins)

        _ds = Dataset()
        _ds.xdata = newx
        _ds.ydata = newy
        _ds.figurelabel = 'Histogram'
        _ds.yaxislabel = 'P'
        _ds.xaxislabel = 'Data Value'
        self.stack[MAIN] = _ds
        self.plot()

        self.announce('Total counts: %s' % (len(ydata)))

    #@+node:tom.20211207165051.121: *4* mean_std
    @REQUIRE_MAIN
    def mean_std(self):
        ydata = self.stack[MAIN].ydata
        mean, std = stats.meanstd(ydata)
        _max = max(ydata)
        se = std / (len(ydata) - 1)**0.5

        # Check ydata type because it might not be a list
        # pylint: disable = unidiomatic-typecheck
        if type(ydata) == type(ndarray(1)):
            _ydata_list = ydata.tolist()
            _maxy_index = _ydata_list.index(_max)
            _maxy_index = _ydata_list.index(_max)
        else:
            _maxy_index = ydata.index(_max)
            _maxy_index = ydata.index(_max)
        _max_x_coord = self.stack[MAIN].xdata[_maxy_index]

        # Lag-1 autocorrelation
        sum_resid = sum([y**2 for y in ydata])
        sum_lag = 0
        for i in range(1, len(ydata)):
            sum_lag += ydata[i] * ydata[i - 1]

        rho = sum_lag / sum_resid

        _temp = self.stack[MAIN].copy()
        _temp.integrate()
        area = _temp.ydata[-1]
        span = abs(max(ydata) - min(ydata))

        msg = (f' Max: {_max:0.4g} at x={_max_x_coord:0.3g}  Mean: {mean:0.4g}  '
              f'Span: {span:0.4g}  Std Dev: {std:0.4}  SE: {se:0.4g}  area: {area: .2g}  '
              f'rho: {rho:0.3g}  N = {len(ydata)}')
        self.announce(msg)

    #@+node:tom.20211207214310.1: *3* Trend
    #@+node:tom.20211207165051.117: *4* trend_mann_kendall
    @REQUIRE_MAIN
    def trend_mann_kendall(self):
        _ds = self.stack[MAIN]
        s, z, h, p = mann_kendall(_ds.ydata)
        self.announce('s: %s, z: %0.3f, trend? %s, p: %0.3f'
                      % (s, z, YESNO[h], p))

    #@+node:tom.20211207214759.1: *3* Windowing
    #@+node:tom.20211207165051.124: *4* h_super_gaussian
    @REQUIRE_MAIN
    def h_super_gaussian(self):
        self.stack[MAIN].halfSupergaussian()
        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = 'Windowed %s' % (lab)

        self.plot()

    #@+node:tom.20211207165051.125: *4* gaussian_window
    @REQUIRE_MAIN
    def gaussian_window(self):
        self.stack[MAIN].fullSuperGaussian(2)
        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = ' Gaussian Windowed %s' % (lab)

        self.plot()

    #@+node:tom.20211207165051.126: *4* super_gaussian
    @REQUIRE_MAIN
    def super_gaussian(self):
        self.stack[MAIN].fullSuperGaussian()
        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = ' SuperGaussian Windowed %s' % (lab)

        self.plot()

    #@+node:tom.20211207165051.127: *4* h_cosine
    @REQUIRE_MAIN
    def h_cosine(self):
        self.stack[MAIN].halfCosine()
        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = f' Half Cosine Windowed {lab}'

        self.plot()

    #@+node:tom.20211207165051.128: *4* full_cosine
    @REQUIRE_MAIN
    def full_cosine(self):
        self.stack[MAIN].fullCosine()
        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = f'Cosine Windowed {lab}'

        self.plot()

    #@+node:tom.20220402084339.1: *3* Misc
    #@+node:tom.20211207165051.109: *4* sliding_var
    @REQUIRE_MAIN
    def sliding_var(self):
        '''Calculate the standard deviations in a window that slides across the
        MAIN data set. The result replaces the MAIN data set.
        
        Uses a LOWESS weighted sliding window, and computes the std deviation
        at each fitted point (not the standard error of the mean).  The result
        is plotted.
        '''

        _ds = self.stack[MAIN]
        if not (_ds and any(_ds.ydata)):
            self.announce("No data to work with")
            self.flashit()
            return

        _id = 'sliding_var'
        lastparm = self.parmsaver.get(_id, 10)

        dia = GetSingleInt(self.root, 'Sliding Window', 'Number Of Points',
                           lastparm)
        if not dia.result: return
        self.parmsaver[_id] = dia.result

        # _newx, _stds, sigma = _ds.sliding_var(dia.result)
        _newx, _stds = lowess2_stddev(_ds.xdata, _ds.ydata, dia.result)
        _ds.xdata = _newx
        _ds.ydata = _stds

        lab = self.stack[MAIN].figurelabel or ''
        if lab:
            lab = f'Weighted Windowed ({dia.result}) Standard Deviations of {lab}'
        else:
            lab = f'Weighted Windowed ({dia.result}) Standard Deviations'
        self.stack[MAIN].figurelabel = lab


        self.plot()

    #@+node:tom.20211207165051.129: *4* var_ratio
    @REQUIRE_MAIN
    def var_ratio(self):
        _id = 'var_ratio'
        lastparm = self.parmsaver.get(_id, 40)

        dia = GetSingleInt(self.root, 'Variance Ratio',
                           'Window Width', lastparm)
        if dia.result is None: return
        self.parmsaver[_id] = dia.result

        lab = self.stack[MAIN].figurelabel
        if lab and lab != 'Figure Label':
            self.stack[MAIN].figurelabel = 'Variance Ratio for %s' % (lab)

        self.stack[MAIN].var_ratio(dia.result)
        self.plot()

    #@+node:tom.20211207165051.130: *4* y_vs_y
    @REQUIRE_MAIN_BUFF
    def y_vs_y(self):
        '''Plot y values from BUFFER against y values from MAIN,
        The previous data in MAIN is overrwritten.
        '''

        if len(self.stack[MAIN]) != len(self.stack[BUFFER]):
            self.announce('MAIN and BUFFER must be the same length')
            self.flashit()
            return

        self.stack[MAIN].xdata = self.stack[MAIN].ydata[:]
        self.stack[MAIN].ydata = self.stack[BUFFER].ydata[:]

        self.plot()

    #@+node:tom.20211207165051.131: *4* addTimehack
    def addTimehack(self):
        if not self.stack[MAIN]:
            self.announce('No data')
            self.flashit()
            return

        _id = 'timehack'
        lastparm = self.parmsaver.get(_id, 118)
        dia = GetSingleFloat(self.root, 'X-value Marker',
                             'X Position', lastparm)
        if dia.result is None: return

        self.parmsaver[_id] = dia.result
        self.timehack(dia.result)

    #@+node:tom.20211207165051.132: *4* runMacro
    def runMacro(self, cmdlist=''):
        '''Given a string of commands, one per line, execute the commands
        in order.  First check to make sure all commands are valid;
        execute the sequence of commands if they are.  Lines whose first
        non-whitespace character is ';' or '#' are ignored as comment lines.

        Return nothing.

        ARGUMENT
        cmdlist --  a string of line-separated command names.

        RETURNS
        nothing
        '''

        if not cmdlist:
            self.announce('No command list to run')
            self.flashit()
            return

        cmds = cmdlist.splitlines()
        cmds = [c.strip() for c in cmds if c.strip()]
        cmds = [c for c in cmds if c[0] not in COMMENTS]
        unknowns = []

        for cmd in cmds:
            if not self.commands.get(cmd):
                unknowns.append(cmd)

        if unknowns:
            msg = 'unknown commands: %s' % (' '.join(unknowns))
            self.announce(msg)
            self.flashit()
            return

        for cmd in cmds:
            self.interpret(cmd)

    #@+node:tom.20211207165051.133: *4* testMacro
    def testMacro(self):
        self.runMacro('''dsin
                        copy2buff
                        sqr
                        plot
                        ; comment
                        overplotbuf
                        # another comment
                        loglog
                        ''')

    #@+node:tom.20211207165051.134: *4* interpret
    def interpret(self, command=''):
        '''Given a string alias for a command, find and execute the command.
        If no such command is found, announce an error.

        ARGUMENT
        command -- a string.

        RETURNS
        nothing.
        '''

        if not command:
            self.announce('No command to execute')
            self.flashit()
            self.fadeit()
            return

        if not self.commands.get(command, None):
            self.announce('Unknown command: "%s"' % (command))
            self.flashit()
            self.fadeit()
            return

        self.commands[command]()

    #@+node:tom.20211207165051.135: *4* hasToplevel
    def hasToplevel(self):
        for c in self.root.winfo_children():
            if c.winfo_class() == 'Toplevel':
                return True
        return False

    #@+node:tom.20211207165051.23: *4* test_announce
    def test_announce(self):
        self.announce('testing the Announcer')

    #@-others

#@+node:tom.20211207165051.136: ** __main__
if __name__ == '__main__':
    matplotlib.rcParams['xtick.direction'] = 'out'
    matplotlib.rcParams['ytick.direction'] = 'out'

    plotmgr = PlotManager()
    plotmgr.root.update_idletasks()
    setIcon(plotmgr.root, ICONPATH)

    fname = ''

    # Overplot all files listed on the command line
    _first = True
    for fname in sys.argv[1:]:
        try:
            if _first:
                plotmgr.load_plot_data(fname)
                _first = False
            else:
                plotmgr.load_plot_data(fname, True)
        except Exception as e:
            print (e)

    cmdwindow(plotmgr)
    plotmgr.announce('Using: %s' % (sys.executable))
    plotmgr.fadeit()

    Tk.mainloop()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
