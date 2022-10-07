#@+leo-ver=5-thin
#@+node:tom.20220411202149.1: * @file help.py
#@@language python
#@+others
#@+node:tom.20220411210428.1: ** imports
import webbrowser
from versions import APPVERSION, getGitInfo

try:
    import Tkinter as Tk
except ImportError:
    import tkinter as Tk

version, (branch, changeset) = APPVERSION, getGitInfo()
#@+node:tom.20220506224955.1: ** Declarations
BRANCH_STR = f'; Branch: {branch}' if branch else ""
GIT_STR = f'; Changeset; {changeset}' if changeset else ""
#@+node:tom.20220505131030.1: ** helpmsg
#@+others
#@+node:tom.20220505130330.1: *3* Intro
INTRO = f"""
       GF4 Waveform Calculator/Plotter
--------------------------------------------------------
Plots 2D curves and performs calculations on them. GF4 is modeled
after a reverse polish notation (RPN) calculator, where 2D waveforms take 
the place of plain numbers.

Version: {version}{BRANCH_STR}{GIT_STR}
"""
#@+node:tom.20220412003223.1: *3* Data Format
H1 = """
  Input Data Format
-----------------------------------------------
GF4 accepts text files with whitespace-separated columns, one data point per
row.  Optionally they can be separated by a comma.  All data lines in a file 
must use the same separator. Column headers for csv files are extracted from
the line immediately before the first data line if possible.

If there is only one column, GF4 inserts an imputed first column with values
being consecutive integers beginning with 1. The one (and only) data column
becomes the "x", or vertical, axis. If there are more than two columns, a dialog
is displayed so the user can choose the two desired columns. The number of
columns is derived based on the first non-comment, non-blank line whose
fields are all legal floating point number.

Data fields must be numeric.  GF4 cannot make use of non-numeric data.  Data
fields are converted to floating point numbers.

Here is an example data file:

# A comment line
; Another comment line.  Also, blank lines are ignored.
# x  y
1  1
2  4
3  9
# etc 

Data points do not need to be equally spaced on the x axis.

There are specially formatted (optional) comments to specify a title, axis 
labels, and a break between data sets:

;; FIGURELABEL: The Title
;; XLABEL: The x axis
;; YLABEL: the y axis
1    3.0
2    4.0
3    6.0
4    7.0
;; ENDDATASET

The special comment key words are case sensitive.  If there is more than one
dataset, the second one goes into the y position in the stack, and so on up to
the stack depth.  Beyond that additional data sets are ignored.
"""
#@+node:tom.20220412003352.1: *3* The Waveform Stack
H2 = '''
    The Waveform Stack
-------------------------------------
The stack is a group of data sets, where new data sets get added to the "bottom"
or "X" slot, and there are other slots "above" X, namely "Y" (the next one
"up"), and "T", the "topmost" slot. In computer terms, the stack can be pushed,
popped, or rotated. Data sets can also be added directly to the various slots.

New data sets are always loaded into the "X" slot.  The File/Save... menu item
saves the data in the "X" slot as a text file.

Slots in the stack:

    | --- Top --- |
    | ---  Y  --- |
    | ---  X  --- |    <--- Stack Bottom
'''
#@+node:tom.20220412003444.1: *3* Data Input
H3 = '''
    Data Input
----------------------------
GF4 has two ways to get data:

    1. Read a text data file in the format described above;
    2. Type into an edit dialog box, or paste from the clipboard into the edit box.

New data from either source always gets inserted into the "X" slot, replacing
whatever was there. If the data file contains the special comment ";;
ENDDATASET", then the data following that comment will get loaded into the next
higher slot in the stack, replacing the previous contents. If there should be
another data section, it will load into the next higher slot, the top slot. Data
sections beyond this will get ignored.

The first data loaded after startup will be automatically plotted.  Later
data loads will not be plotted.  This gives the user a chance to overlay the
new data over the old, which can be convient.
'''
#@+node:tom.20220412003456.1: *3* Data Output
H4 = '''
    Data Output
-------------------------
Data in the "X" slot can be saved in two ways:

    1. By using the File/Save... menu item;
    2. By copying it to the clipboard.

Saved data will include the plot title and the axis labels, if any have been
added.  The are denoted using the special comments described above.
'''
#@+node:tom.20220412003510.1: *3* Plotting Data
H5 = '''
    Plotting Data
-----------------------------
Data in the X position - the stack bottom - is displayed with the "Plot X"
command button.  The "Overplot Y" button overlays the data in the Y position
onto the existing plot.  By default the color and line thickness contrast
with the X plotted line.  The Y slot cannot be plotted on its own directly.
The stack top ("T") can be plotted or overplotted.

The difference between plotting and overplotting is that the first clears
the screen before showing the data.

The display auto-scales to accommodate all the data.  The scale boundaries
can be set using the toolbar controls on the plot window, or by using the
Pan/Zoom control that is also located on the toolbar.
'''
#@-others
helpmsg = (INTRO
+ H1
+ H2
+ H3
+ H4
+ H5
)
#@+node:tom.20220411202245.1: ** tutorial
def tutorial():
    # helpdoc = 'GF4_Users_Guide.html'
    # path = join(dirname(__file__), 'doc', 'html', helpdoc)
    # path = path.replace('\\', '/')
    # url = f'file:///{path}'
    url = 'http://tompassin.net/gf4/docs/GF4_Users_Guide.html'
    webbrowser.open_new_tab(url)
#@+node:tom.20220508124357.1: ** blog
def blog():
    url = 'http://tompassin.net/gf4/blogsite/'
    webbrowser.open_new_tab(url)
#@+node:tom.20220411210306.1: ** msg_window
def msg_window(text, plotmgr=None):
    _geom = ''
    if plotmgr:
        win = Tk.Toplevel(plotmgr.root)
        win.transient(plotmgr.root)
        _geom = plotmgr.root.geometry()
    else:
        win = Tk.Tk()

    win.title("About GF4")

    win.grid_columnconfigure(0, weight=1)
    win.grid_rowconfigure(0, weight=1)

    text_box = Tk.Text(win, wrap = 'word', padx = 15, width = 100, height = 50)
    text_box.grid(row=0, column=0, sticky='ew')

    # Thanks to https://www.pythontutorial.net/tkinter/tkinter-scrollbar/
    scroll_bar = Tk.Scrollbar(win,  command=text_box.yview)
    scroll_bar.grid(row=0, column=1, sticky='ns')
    text_box['yscrollcommand'] = scroll_bar.set

    font = ('sans-serif', 10, 'normal')
    text_box.configure(font = font)

    text_box.insert(Tk.END, text)
    text_box['state'] = 'disabled'

    win.update_idletasks()
    if plotmgr:
        plotmgr.root.update_idletasks()

    # Set initial window position in screen
    if _geom:
        #902x670+182+182
        root_dims, root_xoffset, root_yoffset = _geom.split('+')
        root_width, root_height = root_dims.split('x')
        xoffset = int(root_xoffset) + int(root_width) + 5
        yoffset = int(root_yoffset)
        #win.geometry(f'600x{root_height}')
        win.geometry('600x800')
        win.geometry('+%s+%s' %(xoffset, yoffset))
    else:
        win.geometry('600x800')

#@+node:tom.20220411201434.1: ** about
def about(parent = None):
    msg_window(helpmsg, parent)
#@-others

if __name__ == '__main__':
    about()
    Tk.mainloop()
#@-leo
