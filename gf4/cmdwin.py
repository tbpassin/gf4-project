#@+leo-ver=5-thin
#@+node:tom.20211211170819.9: * @file cmdwin.py
"""Auxiliary controller window for gf4."""

# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211223207.1: ** Imports
from __future__ import print_function
from sys import platform
from os.path import normpath, expanduser

from math import ceil
import webbrowser
from tempfile import NamedTemporaryFile

try:
    import Tkinter as Tk
except ImportError:
    import tkinter as Tk

try:
    import tkFont
except ImportError:
    import tkinter.font as tkFont

try:
    import ttk
except ImportError:
    from tkinter import ttk

got_docutils = False
# pylint: disable = wrong-import-position
try:
    from docutils.core import publish_string
    from docutils.utils import SystemMessage
    got_docutils = True
except ImportError:
    pass
if not got_docutils:
    print('*** no docutils - cannot display extended help for commands')
    print('*** Run "python3 -m pip install docutils"')

from buttondefs import (SPACER, CURVE_FIT_BUTTONS, STATS_BUTTONS,
                        GENERATOR_BUTTONS, PLOT_BUTTONS, LOAD_BUTTONS,
                        STACK_BUTTONS, CURVE_BUTTONS, MATH_BUTTONS,
                        DATA_PROCESSING_BUTTONS, WINDOW_BUTTONS, 
                        SMOOTHER_FIT_BUTTONS, TREND_BUTTONS, PLUGIN_BUTTONS,
                        AXES_BUTTONS)
from utility import ICONPATH, setIcon
from help_cmds import HELPTEXT
#@+node:tom.20211211170819.10: ** Declarations
COLS = 6
BG_KEY = 'bg' if platform.lower().startswith('win') else 'activebackground'

BUTTONWIDTH = 11
BUTTON_BG = 'white'
BUTTON_HOVER = 'yellow'
BUTTON_HOVER_WITH_EXTENDED_HELP = 'cyan'
BUTTON_HORIZ_BG = 'lightcyan'
BUTTON_RECORD_COLOR = 'RosyBrown3'

ENCODING = 'utf-8'
EXTENDED_HELP_TEXT = (
    'Right click on button for extended help if button hover color is '
   f'{BUTTON_HOVER_WITH_EXTENDED_HELP}')
HELP_PANEL_BG = 'lightblue'
MACRO_TEXT = 'Record'
MACRO_FULLTEXT = 'Record Macro'
MACRO_RECORDING_TEXT = 'Recording'
MACRO_ON_MSG = 'Macro Recording Started'
MACRO_OFF_MSG = 'Macro Recording Ended'
PADY = 2

entry = None
is_recording = False
macro = ''
NEWFONT = None

RST_ERROR_BODY_STYLE = ('color:#606060;'
                        'background: aliceblue;'
                        'padding-left:1em;'
                        'padding-right:1em;'
                        'border:thin solid gray;'
                        'border-radius:.4em;')

RST_ERROR_MSG_STYLE = ('color:red;'
                       'background:white;'
                       'padding-left:1em;'
                       'padding-right:1em;'
                       'border:thin solid gray;'
                       'border-radius:.4em;')

#@+others
#@+node:tom.20221210000710.1: *3* Temp Directory
# Works for all platforms
TEMPDIR = normpath(expanduser('~/Downloads'))

#@+node:tom.20221108022001.1: *3* Docutils Params
MATHJAX_URL = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
RST_NO_WARNINGS = 5

docutil_args = {'output_encoding': 'utf-8',
                'report_level': RST_NO_WARNINGS,
                'math_output': 'mathjax ' + MATHJAX_URL}
#@-others
    # if sys.platform.startswith('win'):
#@+node:tom.20221108023317.1: ** html_from_rst
def html_from_rst(rst, got_docutils, plotmgr = None):
    """Convert ReStructured Text to HTML.
    
    ARGUMENT
    rst -- the string of ReStructured Text to be converted.
    
    RETURNS
    An encoded HTML bytestring.
    """

    if not got_docutils:
        msg = 'No docutils - cannot show extended help for commands'
        if plotmgr:
            plotmgr.announce(msg)
            plotmgr.flashit()
        else:
            print('====', msg)
        return b''

    html = ''
    try:
        html = publish_string(rst, writer_name='html', settings_overrides=docutil_args)
    except SystemMessage as sm:
        msg = sm.args[0]
        if 'SEVERE' in msg or 'FATAL' in msg:
            output = f'<pre style="{RST_ERROR_MSG_STYLE}">RST error: {msg}\n</pre><b><b>'
            output += f'<pre style="{RST_ERROR_BODY_STYLE}">{html}</pre>'
        html = output.encode(ENCODING)

    return html
#@+node:tom.20221108094726.1: ** flash_button
def flash_button(w):
    """Flash a button more visibly than the Tk default flash()."""
    w.config(relief='sunken')
    w.flash()
    w.config(relief='raised')
#@+node:tom.20211211170819.11: ** click
def click(event): 
    global is_recording, macro
    w = event.widget
    flash_button(w)
    if w.cget('text') in (MACRO_TEXT, MACRO_RECORDING_TEXT):
        if is_recording:
            is_recording = False
            w.config(bg = BUTTON_BG)
            w['text'] = MACRO_TEXT
        else:
            w.config(bg=BUTTON_RECORD_COLOR)
            is_recording = True
            w['text'] = MACRO_RECORDING_TEXT
            macro = ''

#@+node:tom.20211211170819.12: ** on_enter
def on_enter(event):
    global entry
    global is_recording

    w = event.widget
    cmd = w.cmd
    try:
        t = w.fulltext
        w.old_bg = w.cget('bg')
        entry.configure(text=t)
        if w.cget('text') != MACRO_TEXT:
            if HELPTEXT.get(cmd, ''):
                w[BG_KEY] = BUTTON_HOVER_WITH_EXTENDED_HELP
            else:
                w[BG_KEY] = BUTTON_HOVER
        elif not is_recording:
            w[BG_KEY] = BUTTON_HOVER

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
        w[BG_KEY] = _bg
    else:
        if not is_recording:
            w[BG_KEY] = BUTTON_BG

#@+node:tom.20221107220544.1: ** on_rclick
def on_rclick(event, plotmgr = None):
    """Display help text for cmd in system browser."""
    w = event.widget
    cmd = w.cmd
    flash_button(w)

    if not plotmgr:  # We are running stand-alone for testing
        print(cmd)

    help = HELPTEXT.get(cmd, '')
    if not help:
        if plotmgr:
            plotmgr.announce(f'No help for {cmd}')
            plotmgr.fadeit()
        return

    html = html_from_rst(help, got_docutils, plotmgr)
    if html:
        with NamedTemporaryFile(suffix = '.html',
                dir = TEMPDIR, delete = False) as f:
            f.write(html)
        webbrowser.open(f.name)

#@+node:tom.20221212135221.1: ** on_click_help
def on_click_help(event):
    global entry
    if got_docutils:
        msg = EXTENDED_HELP_TEXT
    else:
        msg = 'docutils is needed to display extended help on right click'
    entry.configure(text = msg)
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
            _b = Tk.Button(parent, text = text, relief = 'raised', width = BUTTONWIDTH,
                           bg = BUTTON_BG, font = NEWFONT, padx = 8, pady = PADY,
                           command = lambda x=cmd: default_command(x, plotmgr))
            _b.pack(fill=Tk.X)
            _b.cmd = cmd
            _b.bind('<Button-1>', click)
            _b.bind('<Enter>', on_enter)
            _b.bind('<Leave>', on_leave)
            _b.bind('<Button-3>', lambda x: on_rclick(x, plotmgr))
            _b.fulltext = fulltext

#@+node:tom.20211211170819.18: ** configure_horizontal_button_list
def configure_horizontal_button_list(parent, button_list, plotmgr):
    global NEWFONT
    cols = 0
    for b in button_list:
        if cols % COLS == 0:
            _frame = Tk.Frame(parent, bd=1, relief='groove')
            _frame.pack(fill=Tk.BOTH)
        text, cmd, fulltext = b
        but = Tk.Button(_frame, text = text, width = BUTTONWIDTH + 1, bg = BUTTON_HORIZ_BG,
                font = NEWFONT, pady = PADY,
                command = lambda x=cmd: default_command(x, plotmgr))
        but.pack(side='left')
        but.cmd = cmd
        but.bind('<Button-1>', click)
        but.bind('<Enter>', on_enter)
        but.bind('<Leave>', on_leave)
        but.bind('<Button-3>', lambda x: on_rclick(x, plotmgr))
        but.fulltext = fulltext

        cols += 1

#@+node:tom.20211211170819.19: ** configure_macro_buttons
def configure_macro_buttons(parent, plotmgr):
    global NEWFONT
    global macro

    _frame = Tk.LabelFrame(parent, text='Macro', bd=3, bg='lightgrey')
    _frame.pack(fill=Tk.BOTH)

    but_record = Tk.Button(_frame, text = MACRO_TEXT, width = BUTTONWIDTH+1,
                    bg = BUTTON_BG, pady = PADY, font = NEWFONT)
    but_record.pack(side='left')
    but_record.bind('<Button-1>', click)
    but_record.bind('<Enter>', on_enter)
    but_record.bind('<Leave>', on_leave)
    but_record.bind('<Button-3>', lambda x: on_rclick(x, plotmgr))
    but_record.fulltext = MACRO_FULLTEXT
    but_record.cmd = 'record-macro'

    but_play = Tk.Button(_frame, text='Play', width = BUTTONWIDTH + 1, pady = PADY,
                command=lambda x=plotmgr:play_macro(x), bg = BUTTON_BG, font = NEWFONT)
    but_play.pack(side='left')
    but_play.bind('<Enter>', on_enter)
    but_play.bind('<Leave>', on_leave)
    but_play.bind('<Button-3>', lambda x: on_rclick(x, plotmgr))
    but_play.fulltext = 'Play Back Macro'
    but_play.cmd = 'play-macro'

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
    # Custom font for smaller button font size
    global entry, NEWFONT

    #@+<< Make new Tk font >>
    #@+node:tom.20220402001046.1: *3* << Make new Tk font >>
    available_fonts = tkFont.families()
    phantom = Tk.Button(text='phantom')
    _font =  tkFont.nametofont(phantom['font'])
    sz = _font['size']

    # Find a preferred font, if installed
    ffamily = ''
    for f in ("Segoe UI", "Open Sans", "Noto Sans", "Corbel"):
        if f in available_fonts:
            ffamily = f
            break

    ascender = 9.6  # Default when no case matches if statement
    if ffamily:
        if platform.startswith('win'):
            ascender = 10.6
        else:
            if ffamily in ('Open Sans', 'Noto Sans'):
                ascender = 11
            elif ffamily == 'DejaVu Sans':
                ascender = 9
            else:
                ascender = 9.6

        # Create a Tk font for this family
        NEWFONT = tkFont.Font(
                            family = ffamily, name = 'cmdButtonFont',
                            size = int(sz), weight = 'bold')

        sz = adjust_font_size(NEWFONT, ascender)
        NEWFONT.config(size = sz)
        # _font will be the font of the group labels and the help text
        _font.config(**NEWFONT.config())
    else:
        ascender = 9.6
        NEWFONT = tkFont.nametofont(_font.name)
        sz = adjust_font_size(NEWFONT, ascender)
        NEWFONT.config(size = sz, weight = 'bold')

    _font_linespace = _font.metrics()['linespace']
    phantom = None
    #@-<< Make new Tk font >>
    #@+<< Create Control Containers >>
    #@+node:tom.20220402001714.1: *3* << Create Control Containers >>
    # Help panel at top
    lineheight = _font_linespace + 10
    entryframe = Tk.Frame(host, height = lineheight, bd = 3,
                          relief = 'groove', bg = HELP_PANEL_BG)
    entryframe.pack_propagate(0)
    entryframe.pack(fill = Tk.X)

    help_button = Tk.Button(entryframe, text = '?')
    help_button.pack(side = Tk.RIGHT)
    help_button.bind('<Button-1>', on_click_help)

    entry = Tk.Label(entryframe, padx = 5, bg = HELP_PANEL_BG,  anchor = Tk.CENTER)
    entry.pack(side = Tk.LEFT, expand = True)

    # Frame for all the command buttons
    cmd_frame = Tk.Frame(host, bd = 1, relief = 'sunken', bg = 'red')
    cmd_frame.pack(fill = Tk.Y)

    configure_horizontal_button_list(host, GENERATOR_BUTTONS, plotmgr)
    configure_macro_buttons(host, plotmgr)

    #@-<< Create Control Containers >>

    def create_button_group(frame, text, button_group, pack = 'side'):
        but_frame = Tk.LabelFrame(frame, text = text, bd=3, bg='lightgrey')
        if pack == 'side':
            but_frame.pack(side=Tk.LEFT, fill=Tk.BOTH)
        else:
            but_frame.pack(fill=Tk.BOTH)
        configure_button_list(but_frame, button_group, plotmgr)
        return but_frame

    # Create Button Groups
    but_frame_plot = create_button_group(cmd_frame, 'Plot', PLOT_BUTTONS)
    create_button_group(but_frame_plot, 'Axes', AXES_BUTTONS, 'fill')
    create_button_group(but_frame_plot, 'Load/Save', LOAD_BUTTONS, 'fill')

    but_frame_stack = create_button_group(cmd_frame, 'Stack', STACK_BUTTONS)
    create_button_group(but_frame_stack, 'Plugins', PLUGIN_BUTTONS)

    create_button_group(cmd_frame, 'Curve', CURVE_BUTTONS)
    create_button_group(cmd_frame, 'Math', MATH_BUTTONS)

    but_frame_dp = create_button_group(cmd_frame, 'Data Processing', DATA_PROCESSING_BUTTONS)
    create_button_group(but_frame_dp, 'Windowing', WINDOW_BUTTONS, 'fill')
    create_button_group(but_frame_dp, 'Trend', TREND_BUTTONS, 'fill')

    but_frame_fit = create_button_group(cmd_frame, 'Fit', CURVE_FIT_BUTTONS)
    create_button_group(but_frame_fit, 'Smooth', SMOOTHER_FIT_BUTTONS, 'fill')
    create_button_group(but_frame_fit, 'Statistics', STATS_BUTTONS, 'fill')


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
    setIcon(win, ICONPATH)

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
        w_width = win.winfo_width() + 50
        w_height = win.winfo_height()
        if w_height < int(root_height):
            w_height = int(root_height)

        #win.geometry('+%s+%s' %(xoffset, yoffset))  # Can just set offsets
        win.geometry(f'{w_width}x{w_height}+{xoffset}+{yoffset}')
    else:
        pass
        #win.geometry('700x700')

if __name__ == '__main__':
    cmdwindow(None)
    Tk.mainloop()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
