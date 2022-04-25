import sys
import pyperclip
try:
    import smoother
except ImportError:
    path = r'C:/Tom/devel/matplotlib/gf4'
    sys.path.append(path)
DATA = [f'{i}   0' for i in range(10)]
DATA.extend([f'{i}   1' for i in range(10, 100)])

SPAN = 10
SRANGE = (5,10,15,20,30)

if __name__ == '__main__':

    INTERNAL_DATA = False
    if len(sys.argv) == 1: 
        INTERNAL_DATA = True
        #print('No file on command line')
        #sys.exit(0)

    if not INTERNAL_DATA:
        basename = 'dat.txt'   
        if len(sys.argv) > 2:
            ofilenames  = [sys.argv[2] + '_%s.txt' % (s) for s in SRANGE]
        else:
            ofilenames  = (basename + '_%s.txt' % (s) for s in SRANGE)

        fname = sys.argv[1]
        with open(fname) as f:
            lines = f.readlines()
        if not lines: sys.exit(0)
    else:
        lines = DATA

    x = []
    y = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if line[0] == ';': continue
        splits = line.split()
        try:
            x.append(float(splits[0]))
            y.append(float(splits[1]))
        except Exception as e:
            print(e)
            continue

    if INTERNAL_DATA:
        output = f';; FIGURELABEL: LOWESS Test, Span = {SPAN}\n'
        xi, yi = smoother.lowess(x,y,SPAN)
        output += '\n'.join(['%s  %s' % (xi[n], yi[n]) for n in range(len(xi))])
        pyperclip.copy(output)
    else:
        for i, _ in enumerate(SRANGE):
            s = SRANGE[i]
            xi, yi = smoother.lowess(x,y,s)
            result = ['%s  %s\n' % (xi[n], yi[n]) for n in range(len(xi))]

            oname = ofilenames[i]
            header = ';;FIGURELABEL: %s\n' % oname
            with open(oname, 'w') as of:
                of.write(header)
                of.write(''.join(result)) 
