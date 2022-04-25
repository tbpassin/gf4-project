'''Define line and symbol (i.e., "marker") characteristics for plotting data.
Mostly as defined by the Matplotlib axis class.
'''

CIRCLE = 'o'; HEXAGON = 'H'; DIAMOND = 'D'
SQUARE = 's'; TRIANGLE = '^'; TRIANGLE_LEFT = '<'
SYM_NONE = 'None'
LINE_NONE = 'None'; LINE_SOLID = '-'
LINETHIN = 0.5; LINEMED = 1.2; LINETHICK = 2.5

class Linestyle:
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

    def set_linewidth(self, width):
        self.linewidth = width
        
    def set_sym_style(self, shape):
        self.symbol = shape

    def set_sym_color(self, color):
        self.sym_mec = 'black' #color
        self.sym_mfc = color
        
    def set_linecolor(self, color):
        self.linecolor = color
        
    def get_vals(self):
        return 'useSym: %s\nuseLine: %s\nlinewidth: %s\nlinecolor: %s\nlinestyle: %s\n'\
            % (self.useSym, self.useLine, self.linewidth, self.linecolor,
                self.linestyle) \
            + 'symbol: %s\nsym_mec: %s\nsym_mfc: %s\nsym_mew: %s' \
            % (self.symbol, self.sym_mec, self.sym_mfc,
                self.sym_mew)
