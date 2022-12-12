#@+leo-ver=5-thin
#@+node:tom.20221027233021.1: * @file utility.py
#@@language python
"""Misc. utility functions that may be used by several modules."""
#@+others
#@+node:tom.20221027233140.1: ** Imports
from pathlib import PurePath
from configparser import ConfigParser

import tkinter as Tk
#@+node:tom.20221027233311.1: ** Declarations
HOMEPATH = PurePath(__file__).parent
ICONFILE = 'linechart1.png'
# Legal syntax for PurePath
ICONPATH = HOMEPATH / 'icons' / ICONFILE

CONFIGDIR = 'config'
CONFIGFILE = 'gf4.ini'
CONFIGPATH = HOMEPATH / CONFIGDIR / CONFIGFILE
#@+node:tom.20221211134841.1: ** Create Config Parser
config=ConfigParser()
config.read(CONFIGPATH)
#@+node:tom.20221027233350.1: ** setIcon
def setIcon(win, icon):
    """Set a Tk windows's icon.
    
    Thanks to:
    https://stackoverflow.com/questions/33137829/how-to-replace-the-icon-in-a-tkinter-app

    
    ARGUMENTS
    win -- the Tk window
    icon -- a string path or a PurePath for the icon's file (e.g., a .png file)

    RETURNS
    nothing
    """

    photo = Tk.PhotoImage(file = icon)
    win.wm_iconphoto(False, photo)
#@-others
#@-leo
