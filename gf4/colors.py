#@+leo-ver=5-thin
#@+node:tom.20211211170819.23: * @file colors.py
#@+others
#@+node:tom.20211211170819.24: ** Color Definitions
"""Color definitions for gf4."""

BLACK = 'black';
CORNFLOWERBLUE = 'CornFlowerBlue'
CYAN = 'cyan';
DEEPSKYBLUE = 'deepskyblue'
DEFAULTGRIDCOLOR = 'lightgrey';
GRAY = 'gray';
LIGHTBLUE = 'lightblue'
MEDIUMLIGHTGRAY = '0.9'
LIGHTGRAY = '0.95';
MEDGRAY='0.6';
NEARBLACK = '0.2';
WHITE = 'white'

# Grid colors to use for various background colors
ColorBgPairs = {  # background: grid
    CORNFLOWERBLUE:  (0.529,  0.376,  0.376),
    DEEPSKYBLUE: (0.529,  0.376,  0.376),
    LIGHTBLUE: MEDGRAY,
    MEDGRAY: MEDIUMLIGHTGRAY,
    BLACK: LIGHTGRAY,
    WHITE: DEFAULTGRIDCOLOR
}
#@-others
#@@language python
#@@tabwidth -4
#@-leo
