import math

def sqr(x):
    return x*x

def SmoothPoint(xdata, ydata, wt, i, cliplevel=2.0, causal=False):
    '''    ARGUMENTS
    xdata, ydata -- lists of the x and y data.  Must be the same length.
    wt -- a WtStats instance that has the weight table filled in.
    i -- the index of the point (x,y) to be smoothed.
    cliplevel -- threshold for designating points as fliers
    causal -- If True, use only neighbors to left of specified point.  Otherwise,
              use neighbors on both sides.

    RETURNS
    a tuple (s, d, is_flier), where s is the smoothed value of the point, 
    d is the variance at the point, and is_flier is boolean that is True if
    the point lies farther than cliplevel standard deviations
    from the fitted point.
    '''
    
    Swt = 0 # sum of weights 
    Swx = 0 # weighted sum of x
    Swy = 0 # weighted sum of y
    Swxy = 0 # weighted sum of xy
    Swxx = 0 # weighted sum of xx
    Swyy = 0 # weighted sum of yy
    var = 0 # variance at this point
    a = 0 # y = ax + b
    b = 0
    SqrDev = 0
    clips = []

    sz = wt.smoothzone
#    if not causal:
#        tail = min(i + smoothzone, len(xdata))
#    else:
#        tail = i;

    N = len(xdata)
    x = xdata[i]
    window_left = max(0, i - sz + 1)
    window_right = min(N - 1, i + sz - 1)
    num = window_right - window_left # number of points in weight window
    for j in range(window_left, window_right + 1):
        weight_index = abs(i - j)
        wj = wt.weights[weight_index]
        xtemp = xdata[j]
        ytemp = ydata[j]
        Swx = Swx +  wj*xtemp
        Swy = Swy +  wj*ytemp
        Swxy = Swxy +  wj* xtemp*ytemp
        Swxx = Swxx + wj* sqr(xtemp)
        Swyy = Swyy + wj * sqr(ytemp)
        Swt = Swt + wj
    
    a = (Swt*Swxy - Swx*Swy)/(Swt*Swxx - sqr(Swx));
    b = (Swy - a*Swx)/(Swt);

    if True:#i > 0:
        y = a*x + b
        SqrDev = (Swyy - 2*a*Swxy - 2*b*Swy + sqr(a)*Swxx +\
                  2*a*b*Swx)/Swt + sqr(b)
    else:
        y = ydata[i]
        SqrDev = 0

    if SqrDev < 0:
        SqrDev = 0

    is_flier = (abs(ydata[i] - y) > cliplevel * math.sqrt(SqrDev))
    print '%s %0.3f' % (xdata[i], cliplevel*math.sqrt(SqrDev) + ydata[i])
    return (y, SqrDev, is_flier)

if __name__ == '__main__':
    import string
    import sys
    from smoother import WtStats

    if len(sys.argv) > 1:
        data = open(sys.argv[1]).readlines()
        xdata = []
        ydata = []
        for i in range(len(data)):
            line = data[i]
            line = line.strip()
            if line[0] == ';': continue
            xstr,ystr = line.split()
            x = float(xstr)
            y = float(ystr)
            xdata.append(x)
            ydata.append(y)
    else:
        xdata = [1,2,3,4,5,6,7,8] 
        ydata = [1,3,4,7,9,3,2,2]

    wt = WtStats()
    smoothzone = 15
    smoothzone = min(smoothzone, len(xdata)/2 - 1)
    print 'smoothzone:', smoothzone
    wt.MakeGaussianWeights(smoothzone)

    fliers = []
    smooths = []
    for i in range(len(xdata)):
        y,v, is_flier = SmoothPoint(xdata, ydata, wt, i)
        smooths.append('%s  %0.3f' % (xdata[i], y))
        if is_flier:
            fliers.append((xdata[i], ydata[i]))

    print ';Smoothed Data'
    print string.join(smooths, '\n')
    print

    print ';Unsmoothed Data'
    for i in range(len(xdata)):
        print xdata[i], ydata[i]

    print
    if fliers:
        print ';Fliers'
        for x,y in fliers:
            print x, y
