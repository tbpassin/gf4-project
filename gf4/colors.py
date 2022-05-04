#@+leo-ver=5-thin
#@+node:tom.20211211170819.23: * @file colors.py
#@+others
#@+node:tom.20211211170819.24: ** Color Definitions
"""Color definitions for gf4."""

NEARBLACK = '0.2'; BLACK = 'black'; LIGHTGRAY = '0.95'; WHITE = 'white'
CYAN = 'cyan'; GRAY = 'gray'; MEDGRAY='0.6'; LIGHTBLUE = 'lightblue'
DEFAULTGRIDCOLOR = 'lightgrey'; CORNFLOWERBLUE = 'CornFlowerBlue'
DEEPSKYBLUE = 'deepskyblue'

# Grid color to use for various background colors
ColorBgPairs = {
    CORNFLOWERBLUE:  (0.529,  0.376,  0.376),
    DEEPSKYBLUE: (0.529,  0.376,  0.376),
    LIGHTBLUE: MEDGRAY,
    BLACK: LIGHTGRAY,
    WHITE: DEFAULTGRIDCOLOR
}
#@-others
#@@language python
#@@tabwidth -4
#@-leo
