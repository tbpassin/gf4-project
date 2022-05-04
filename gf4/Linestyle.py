#@+leo-ver=5-thin
#@+node:tom.20211211171304.51: * @file Linestyle.py
#@+others
#@+node:tom.20211211171304.52: ** Organizer: Declarations (Linestyle.py)
'''Define line and symbol (i.e., "marker") characteristics for plotting data.
Mostly as defined by the Matplotlib axis class.
'''

CIRCLE = 'o'; HEXAGON = 'H'; DIAMOND = 'D'
SQUARE = 's'; TRIANGLE = '^'; TRIANGLE_LEFT = '<'
SYM_NONE = 'None'
LINE_NONE = 'None'; LINE_SOLID = '-'
LINETHIN = 0.5; LINEMED = 1.2; LINETHICK = 2.5

#@+node:tom.20211211171304.53: ** class Linestyle
class Linestyle:
    #@+others
    #@+node:tom.20211211171304.54: *3* Linestyle.__init__
    def __init__(self):
        self.useSym = False
        self.useLine = True
        self.linewidth = LINETHIN
        self.linecolor = 'black'
        self.linestyle = LINE_SOLID
        self.symbol = CIRCLE
        self.sym_mec = 'black'  # symbol outline
        self.sym_mfc = 'black'  # symbol interior
        self.sym_mew = 0.5

    #@+node:tom.20211211171304.55: *3* Linestyle.set_linewidth
    def set_linewidth(self, width):
        self.linewidth = width
        
    #@+node:tom.20211211171304.56: *3* Linestyle.set_sym_style
    def set_sym_style(self, shape):
        self.symbol = shape

    #@+node:tom.20211211171304.57: *3* Linestyle.set_sym_color
    def set_sym_color(self, color):
        self.sym_mec = 'black' #color
        self.sym_mfc = color
        
    #@+node:tom.20211211171304.58: *3* Linestyle.set_linecolor
    def set_linecolor(self, color):
        self.linecolor = color
        
    #@+node:tom.20211211171304.59: *3* Linestyle.get_vals
    def get_vals(self):
        return 'useSym: %s\nuseLine: %s\nlinewidth: %s\nlinecolor: %s\nlinestyle: %s\n'\
            % (self.useSym, self.useLine, self.linewidth, self.linecolor,
                self.linestyle) \
            + 'symbol: %s\nsym_mec: %s\nsym_mfc: %s\nsym_mew: %s' \
            % (self.symbol, self.sym_mec, self.sym_mfc,
                self.sym_mew)
    #@-others
#@-others
#@@language python
#@@tabwidth -4
#@-leo
