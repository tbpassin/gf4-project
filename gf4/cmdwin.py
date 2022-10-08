#@+leo-ver=5-thin
#@+node:tom.20211211170819.9: * @file cmdwin.py
"""Auxilliary controller window for gf4."""

# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211223207.1: ** Imports
from __future__ import print_function
from sys import platform
from math import ceil

try:
    import Tkinter as Tk
except:
    import tkinter as Tk

# try:
    # from Tkinter import Toplevel
# except:
    # from tkinter import Toplevel

try:
    import tkFont
except:
    import tkinter.font as tkFont

try:
    import ttk
except:
    from tkinter import ttk

from buttondefs import (SPACER, CURVE_FIT_BUTTONS, STATS_BUTTONS,
                        GENERATOR_BUTTONS, PLOT_BUTTONS, LOAD_BUTTONS,
                        STACK_BUTTONS, CURVE_BUTTONS, MATH_BUTTONS,
                        DATA_PROCESSING_BUTTONS, WINDOW_BUTTONS, 
                        SMOOTHER_FIT_BUTTONS, TREND_BUTTONS, PLUGIN_BUTTONS)
#@+node:tom.20211211170819.10: ** Declarations
COLS = 6
BUTTONWIDTH = 9
BUTTON_BG = 'white'
BUTTON_HORIZ_BG = 'lightcyan'
BUTTON_RECORD_COLOR = 'RosyBrown3'

MACRO_TEXT = 'Record'
MACRO_FULLTEXT = 'Record Macro'

entry = None
is_recording = False
macro = ''
NEWFONT = None
#@+node:tom.20211211170819.11: ** click
def click(event): 
    global is_recording, macro
    w = event.widget
    bg = w.cget('bg')
    w.config(relief='sunken', bg='cyan')
    w.flash()
    w.config(relief='raised', bg=bg)
    if w.cget('text') == MACRO_TEXT:
        if is_recording:
            is_recording = False
            w.config(bg = BUTTON_BG)
        else:
            w.config(bg=BUTTON_RECORD_COLOR)
            is_recording = True
            macro = ''

#@+node:tom.20211211170819.12: ** on_enter
def on_enter(event):
    global entry
    global is_recording

    w = event.widget
    try:
        t = w.fulltext
        w.old_bg = w.cget('bg')
        entry.configure(text=t)
        if w.cget('text') != MACRO_TEXT:
            w.configure(bg='yellow')
        elif not is_recording:
            w.configure(bg='yellow')

    except Exception:
        pass

#@+node:tom.20211211170819.13: ** on_leave
def on_leave(event):
    global entry
    global is_recording

    w = event.widget
    _bg = w.old_bg
    entry.configure(text='')
    if w.cget('text') != MACRO_TEXT:
        w.configure(bg=_bg)
    else:
        if not is_recording:
            w.configure(bg=BUTTON_BG)

#@+node:tom.20211211170819.14: ** default_command
def default_command(cmd, plotmgr=None):
    global is_recording, macro
    if is_recording:
        macro += '\n' + cmd
    if plotmgr:
        plotmgr.interpret(cmd)
    else:
        print (cmd)

#@+node:tom.20211211170819.15: ** play_macro
def play_macro(plotmgr):
    global macro
    if plotmgr:
        plotmgr.runMacro(macro)
    else:
        print ('Run Macro:')
        print (macro)

#@+node:tom.20211211170819.16: ** clear_macro
def clear_macro():
    global macro
    macro = ''

#@+node:tom.20211211170819.17: ** configure_button_list
def configure_button_list(parent, button_list, plotmgr):
    global NEWFONT
    for b in button_list:
        if b is SPACER:
            ttk.Separator(parent, style='gf.TSeparator').pack(fill=Tk.BOTH)
        else:
            try:
                text, cmd, fulltext = b
            except ValueError:
                print(f'Bad button definition: {b}')
                continue 
            _b = Tk.Button(parent, text=text, relief='raised', width=BUTTONWIDTH, 
                           bg=BUTTON_BG, font=NEWFONT, padx=8,
                           command=lambda x=cmd: default_command(x, plotmgr))
            _b.pack(fill=Tk.X)
            _b.bind('<Button-1>', click)
            _b.bind('<Enter>', on_enter)
            _b.bind('<Leave>', on_leave)
            _b.fulltext = fulltext
            _b.cmd = cmd

#@+node:tom.20211211170819.18: ** configure_horizontal_button_list
def configure_horizontal_button_list(parent, button_list, plotmgr):
    global NEWFONT
    cols = 0
    for b in button_list:
        if cols % COLS == 0:
            _frame = Tk.Frame(parent, bd=1, relief='groove')
            _frame.pack(fill=Tk.BOTH)
        text, cmd, fulltext = b
        but = Tk.Button(_frame, text=text, width=BUTTONWIDTH+1, bg=BUTTON_HORIZ_BG,
                font=NEWFONT, 
                command=lambda x=cmd: default_command(x, plotmgr))
        but.pack(side='left')
        but.bind('<Button-1>', click)
        but.bind('<Enter>', on_enter)
        but.bind('<Leave>', on_leave)
        but.fulltext = fulltext
        but.cmd = cmd

        cols += 1

#@+node:tom.20211211170819.19: ** configure_macro_buttons
def configure_macro_buttons(parent, plotmgr):
    global NEWFONT
    global macro

    _frame = Tk.LabelFrame(parent, text='Macro', bd=3, bg='lightgrey')
    _frame.pack(fill=Tk.BOTH)

    but_record = Tk.Button(_frame, text=MACRO_TEXT, width=BUTTONWIDTH+1, 
                    bg=BUTTON_BG, font=NEWFONT)
    but_record.pack(side='left')
    but_record.bind('<Button-1>', click)
    but_record.bind('<Enter>', on_enter)
    but_record.bind('<Leave>', on_leave)
    but_record.fulltext = MACRO_FULLTEXT

    but_play = Tk.Button(_frame, text='Play', width=BUTTONWIDTH+1, 
                command=lambda x=plotmgr:play_macro(x), bg=BUTTON_BG, font=NEWFONT)
    but_play.pack(side='left')
    but_play.bind('<Enter>', on_enter)
    but_play.bind('<Leave>', on_leave)
    but_play.fulltext = 'Play Back Macro'

    but_clear = Tk.Button(_frame, text='Clear', width=BUTTONWIDTH+1, 
                    command=clear_macro, bg=BUTTON_BG, font=NEWFONT)
    but_clear.pack(side='left')
    but_clear.bind('<Enter>', on_enter)
    but_clear.bind('<Leave>', on_leave)
    but_clear.fulltext = 'Clear Macro'

#@+node:tom.20221007145433.1: ** adjust_font_size(font, ascender_height)
def adjust_font_size(font, ascender_height):
    """Adjust TK font size to make the ascender height as specified.
    
    Returns an integer."""
    metrics = font.metrics()
    params = font.actual()
    ascender = metrics['ascent']
    size = params['size']

    return ceil((1. * ascender_height / ascender) * size)
#@+node:tom.20211211170819.20: ** create_buttons_pack
def create_buttons_pack(host, plotmgr):
    # pylint: disable = too-many-locals
    # Custom font for smaller button font size
    global entry, NEWFONT

    #@+<< Make new Tk font >>
    #@+node:tom.20220402001046.1: *3* << Make new Tk font >>
    phantom = Tk.Button(text='phantom')
    _font =  tkFont.nametofont(phantom['font'])
    sz = _font['size']
    if platform.startswith('win'):
        ascender = 10.6
    else:
        ascender = 9.6

    # Find a preferred font, if installed
    available_fonts = tkFont.families()
    ffamily = ''
    for f in ("Segoe UI", "Open Sans", "Corbel"):
        if f in available_fonts:
            ffamily = f
            break

    if ffamily:
        # Create Tk font for this family
        NEWFONT = tkFont.Font(
                            family = ffamily, name = 'cmdButtonFont',
                            size = int(sz), weight = 'bold')

        sz = adjust_font_size(NEWFONT, ascender)
        NEWFONT.config(size = sz)
        # _font will be the font of the group labels and the help text
        _font.config(**NEWFONT.config())
    else:
        NEWFONT = tkFont.nametofont(_font.name)
        sz = adjust_font_size(NEWFONT, ascender)
        NEWFONT.config(size = sz, weight = 'bold')

    phantom = None
    #@-<< Make new Tk font >>
    #@+<< Create Button Containers >>
    #@+node:tom.20220402001714.1: *3* << Create Button Containers >>
    entryframe = Tk.Frame(host, height=20, bd=3, relief='groove', bg='lightblue')
    entryframe.pack_propagate(0)
    entryframe.pack(fill=Tk.X)

    entry = Tk.Label(entryframe, bg='lightcyan')
    entry.pack(fill=Tk.X)

    cmd_frame = Tk.Frame(host, bd=1, relief='sunken', bg='red')
    cmd_frame.pack(fill=Tk.Y)

    configure_horizontal_button_list(host, GENERATOR_BUTTONS, plotmgr)
    configure_macro_buttons(host, plotmgr)

    #@-<< Create Button Containers >>

    # Create Button Groups
    but_frame_1 = Tk.LabelFrame(cmd_frame, text='Plot', bd=3, bg='lightgrey')
    but_frame_1.pack(side=Tk.LEFT, fill=Tk.BOTH)
    configure_button_list(but_frame_1, PLOT_BUTTONS, plotmgr)

    but_frame_load = Tk.LabelFrame(but_frame_1, text='Load/Save', bd=3, bg='lightgrey')
    but_frame_load.pack(fill=Tk.BOTH)
    configure_button_list(but_frame_load, LOAD_BUTTONS, plotmgr)

    but_frame_2 = Tk.LabelFrame(cmd_frame,text='Stack', bd=3, bg='lightgrey')
    but_frame_2.pack(side=Tk.LEFT, fill=Tk.BOTH)
    configure_button_list(but_frame_2, STACK_BUTTONS, plotmgr)

    but_frame_curve = Tk.LabelFrame(cmd_frame, text='Curve', bd=3, bg='lightgrey')
    but_frame_curve.pack(side=Tk.LEFT, fill=Tk.BOTH)
    configure_button_list(but_frame_curve, CURVE_BUTTONS, plotmgr)

    but_frame_math = Tk.LabelFrame(cmd_frame, text='Math', bd=3, bg='lightgrey')
    but_frame_math.pack(side=Tk.LEFT, fill=Tk.BOTH)
    configure_button_list(but_frame_math, MATH_BUTTONS, plotmgr)

    but_frame_dp = Tk.LabelFrame(cmd_frame, text='Data Processing', bd=3, bg='lightgrey')
    but_frame_dp.pack(side=Tk.LEFT, fill=Tk.BOTH)
    configure_button_list(but_frame_dp, DATA_PROCESSING_BUTTONS, plotmgr)

    but_frame_win = Tk.LabelFrame(but_frame_dp, text='Windowing', bd=3, bg='lightgrey')
    but_frame_win.pack(fill=Tk.BOTH)
    configure_button_list(but_frame_win, WINDOW_BUTTONS, plotmgr)

    but_frame_trend = Tk.LabelFrame(but_frame_dp, text='Trend', bd=3, bg='lightgrey')
    but_frame_trend.pack(fill=Tk.BOTH)
    configure_button_list(but_frame_trend, TREND_BUTTONS, plotmgr)

    but_frame_fit = Tk.LabelFrame(cmd_frame, text='Fit', bd=3,  bg='lightgrey')
    but_frame_fit.pack(side=Tk.LEFT, fill=Tk.BOTH)
    configure_button_list(but_frame_fit, CURVE_FIT_BUTTONS, plotmgr)

    but_frame_smooth = Tk.LabelFrame(but_frame_fit, text='Smooth', bd=3, bg='lightgrey')
    but_frame_smooth.pack(fill=Tk.BOTH)
    configure_button_list(but_frame_smooth, SMOOTHER_FIT_BUTTONS, plotmgr)

    but_frame_stats = Tk.LabelFrame(but_frame_fit, text='Statistics', bd=3, bg='lightgrey')
    but_frame_stats.pack(fill=Tk.BOTH)
    configure_button_list(but_frame_stats, STATS_BUTTONS, plotmgr)

    but_frame_plugins = Tk.LabelFrame(but_frame_curve, text='Plugins', bd=4, bg='lightcyan')
    but_frame_plugins.pack(fill=Tk.BOTH)
    configure_button_list(but_frame_plugins, PLUGIN_BUTTONS, plotmgr)
#@+node:tom.20211211170819.21: ** cmdwindow
def cmdwindow(plotmgr=None):
    _geom = ''
    if plotmgr:
        win = Tk.Toplevel(plotmgr.root)
        win.transient(plotmgr.root)
        _geom = plotmgr.root.geometry()
    else:
        win = Tk.Tk()

    win.title("GF4 Commands")

    create_buttons_pack(win, plotmgr)
    win.update_idletasks()
    if plotmgr:
        plotmgr.root.update_idletasks()

    # Set initial window position in screen
    #win.geometry('+1250+100')
    if _geom:
        # Example geometry syntax: '902x670+182+182'
        root_dims, root_xoffset, root_yoffset = _geom.split('+')
        root_width, root_height = root_dims.split('x')
        xoffset = int(root_xoffset) + int(root_width) + 5
        yoffset = int(root_yoffset)
        w_width = win.winfo_width() + 25
        w_height = win.winfo_height()
        if w_height < int(root_height):
            w_height = int(root_height)
        else:
            w_height = int(root_height) + 40

        #win.geometry('+%s+%s' %(xoffset, yoffset))  # Can just set offsets
        win.geometry(f'{w_width}x{w_height}+{xoffset}+{yoffset}')
    else:
        win.geometry('600x700')

if __name__ == '__main__':
    cmdwindow(None)
    Tk.mainloop()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
