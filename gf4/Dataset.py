# pylint: disable = consider-using-f-string
from __future__ import print_function

import sys
import math
import copy
import numpy as np

ENCODING = 'utf-8'
class Dataset:
    '''Class to represent a 2D curve.

    ATTRIBUTES
    xdata, ydata -- sequences holding the x or y data sets.  
                    Must be the same length.  May be lists or numpy
                    ndarrays.
    auxDataset -- dictionary of auxiliary data sets (e.g., for holding 
                  statistical information)
    errorBands -- List of Datasets to hold errors
    orig_filename -- file path, if any,  used to load data (before 
                     any transformations have been applied).
    xaxislabel -- label text for the X axis label
    yaxislabel -- label text for the Y axis label
    figurelabel -- label text for the graph of this data
    ymin -- minimum value for Y axis
    ymax -- maximum value for Y axis
    parms -- dictionary of parameters,  Meant to store the current values
             so they can be written to a file.
    '''
    # pylint: disable = too-many-public-methods
    def __init__(self, xdata=None, ydata=None, figurelabel=''):
        self.xdata = xdata
        self.ydata = ydata
        self.subgraphs = []
        self.errorBands = []
        self.auxDataset = {}
        self.orig_filename = ''
        self.xaxislabel = ''
        self.yaxislabel = ''
        self.figurelabel = figurelabel
        self.parms = {}

    def __len__(self):
        if self.xdata is None:
            return False

        if self.isNumpyArray(self.xdata):
            return len(self.xdata.tolist())

        return len(self.xdata)

    def copy(self):
        return copy.deepcopy(self)

    def clearErrorBands(self):
        self.errorBands = []

    def normalize(self):
        '''Rescale to y data to a maximum of 1.0.
        '''
        _max = max(self.ydata)
        if _max == 0.0: return

        self.ydata = [1.0*y/_max for y in self.ydata]

    def setAsciiData(self, lines, filename=''):
        """
        Get data from a sequence of ASCII text lines - normally read from a file.
        Blank lines and lines that start with a ';' or '#' are ignored. 
        If the first non-ignorable line has only a single field, then
        the file is assumed to contain single-column data, and the X-axis data
        equals the data row count.  Otherwise, the first two columns are used,
        split into floating point numbers.

        The x- and y- data sequences are assigned to the data set

        Metadata such as labels are each on a single line starting with 
        two or more ';' characters.  The name of the metadata follows, 
        separated by a ':' or a space from the value.  Example:

        ;;FIGURELABEL:Damped Sine

        Current metadata names are:
            FIGURELABEL
            XLABEL
            YLABEL
            YMIN
            YMAX

        As a special case, a line that starts with the XLABEL meta comment may
        also contain a "YLABEL" tag embedded in the line.  In this case,
        the text before the YLABEL tag will be assigned to the figure's
        X axis label, and the text following the YLABEL tag will be assigned 
        to the figure's Y axis label.

        ARGUMENT
        lines -- a sequence of text lines, with whitespace-separated data columns
        filename -- The file that sourced the data, if it came from a file.

        RETURNS
        the exception if data can't be converted, else None
        """

        # pylint: disable = too-many-branches
        self.orig_filename = filename
        _x = []
        _y = []
        count = 0
        _rowcount = 0
        _datalines = 0
        _isSingleCol = False
        _firstline = True
        e = None
        retval = ''

        for line in lines:
            _rowcount += 1
            line = line.strip()
            if line and line[0] in (';', '#') and line[:2] != ';;': continue
            if not line or line == ';' or line == ';;': continue
            if line[0] == ';' and line[1] != ';': continue

            if line[0] == ';' and line[1] == ';':
                _line = line.lstrip(';')
                _line = _line.lstrip()
                if _line.strip()  == ';;':
                    continue
                try:
                    key, val = _line.split(':',1)
                    key = key.strip()
                    val = val.strip()
                except ValueError:
                    try:
                        key, val = _line.split(' ',1)
                        key = key.strip()
                        val = val.strip()
                    except ValueError:
                        key, val = ('', '')

                if not (key and val): continue

                if key == 'FIGURELABEL': self.figurelabel = val
                elif key == 'XLABEL': 
                    _label_parts = val.split('YLABEL')
                    self.xaxislabel = _label_parts[0].strip()
                    if len(_label_parts) > 1:
                        _ylabel = _label_parts[1].replace(':', ' ', 1)
                        _ylabel = _ylabel.lstrip()
                        self.yaxislabel = _ylabel
                elif key == 'YLABEL': self.yaxislabel = val
                elif key == 'YMIN': 
                    try:
                        self.ymin = float(val)
                    except Exception: pass
                elif key == 'YMAX': 
                    try:
                        self.ymax = float(val)
                    except Exception: pass

                continue
            fields = line.split()

            # Use first non-blank, non-comment line to decide one or 2 column data
            if _firstline and len(fields) == 1:
                _isSingleCol = True
            _firstline = False

            #retval = None
            try:
                if _isSingleCol:
                    count = count + 1
                    _x.append(count)
                    _y.append(float(fields[0]))
                else:
                    _x.append(float(fields[0]))
                    _y.append(float(fields[1]))
                _datalines += 1
            except Exception:
                sys.stderr.write('%s at line %s\n' % (e, _rowcount))
                retained_length = min(len(_x), len(_y))
                _x = _x[:retained_length]
                _y = _y[:retained_length]
                self.figurelabel = 'Data truncated: error  at line %s; %s' % (_rowcount, e)
                #retval = f'{e}'
                #break

        if _datalines:
            self.xdata = _x or [0]
            self.ydata = _y or [0]
        else:
            retval = 'Dataset: No data'
        return retval

    def dedup(self):
        """Remove data point if its value equals the previous value."""
        dedup = []
        last = None
        for i, y in enumerate(self.ydata):
            if y != last:
                last = y
                dedup.append((self.xdata[i], y))
        self.xdata, self.ydata = zip(*dedup)

    def data2String(self):
        '''Return dataset data as string.'''
        _data = ['%s\t%s' % (self.xdata[i], self.ydata[i]) for i in range(len(self.xdata))]
        _str = '\n'.join(_data)
        _header = ''
        if self.figurelabel:
            _header += ';; FIGURELABEL: %s\n' % (self.figurelabel)
        if self.xaxislabel:
            _header += ';; XLABEL: %s\n' % (self.xaxislabel)
        if self.yaxislabel:
            _header += ';; YLABEL: %s\n' % (self.yaxislabel)

        if self.parms:
            for parm, val in self.parms.items():
                _header += ';;%s: %s\n' % (parm, val)

        return _header + _str


    def writeAsciiData(self, filename):
        if not filename: return

        try:
            with open(filename, 'w', encoding = ENCODING) as f:
                f.write(self.data2String())
        except Exception as e:
            print (e)

    def isNumpyArray(self, a):
        return 'shape' in dir(a)

    def pad_truncate(self, num):
        '''Change number of data points in data to num.  if num is > than
        existing number of points, pad the end with zero for the y 
        values.  The padded values are they same type as the existing 
        ones (int or float).  The x values will be incremented by
        the mean x spacing.  This obviously makes most sense when the
        x values are evenly spaced.
        
        If num is < existing number, then truncate the data.  If num
        is the same, do nothing.

        If num < 1, do nothing

        ARGUMENT
        num -- the new number of points for the data.

        RETURNS
        nothing
        '''

        if num < 1: return

        _len = len(self)
        if num == _len: return

        diff = num - _len
        if self.isNumpyArray(self.xdata):
            _x = self.xdata.tolist()
        else:
            _x = self.xdata[:]

        if self.isNumpyArray(self.ydata):
            _y = self.ydata.tolist()
        else:
            _y = self.ydata[:]

        if diff > 0:
            xdelta = (max(_x) - min(_x)) /(_len - 1)
            nextx = _x[-1]
            if isinstance(_y[0], float):
                zero = 0.0
            else:
                zero = int(0)
            for i in range(diff):
                nextx += xdelta
                _x.append(nextx)
                _y.append(zero)
            self.xdata = _x
            self.ydata = _y
        else:
            self.xdata = _x[0:num]
            self.ydata = _y[0:num]
            
    def shift(self, dist):
        '''Shift data along the X axis.  For a shift of 0 length, do nothing.

        ARGUMENT
        dist -- number of points to shift.  Positive means shift right.

        RETURNS
        nothing
        '''

        dist = int(dist)
        if dist == 0: return

        N = len(self.xdata)
        _y = [0] * N

        if dist > 0:
            for i in range(dist, N):
                _y[i] = self.ydata[i - dist]
        else:
            for i in range(0, N + dist):
                _y[i] = self.ydata[i - dist]

        self.ydata = _y

    def transpose(self):
        '''Swap X and Y data.'''
        temp = self.xdata
        self.xdata = self.ydata
        self.ydata = temp
        temp = self.yaxislabel
        self.yaxislabel = self.xaxislabel
        self.xaxislabel = temp

    def sortX(self):
        '''Sort the data points in order of ascending x-axis values.'''

        temp = list(zip(self.xdata, self.ydata))
        temp.sort()
        self.xdata = [x for x,y in temp]
        self.ydata = [y for x,y in temp]
        self.figurelabel = self.figurelabel + '(sorted)'

    def scale(self, c):
        '''Scale Y data point by point by a (floating point) constant.

        ARGUMENT
        c -- the constant to scale by

        RETURNS
        nothing
        '''

        self.ydata = [c*y for y in self.ydata]

    def addConstant(self, c):
        '''Add a (floating point) constant to Y axis data,
        point by point.

        ARGUMENT
        c -- the constant to add

        RETURNS
        nothing
        '''

        self.ydata = [c + y for y in self.ydata]
      
    def differentiate2(self):
        '''Differentiate the data, using central differencing (except at
        the ends, where we must use one-sided differencing).
        '''

        result = []
        _x = self.xdata
        _y = self.ydata
        N = len(_x)
        for i in range(N):
            if i == 0:
                delx = _x[1] - _x[0]
                dely = _y[1] - _y[0]
            elif i == N - 1:
                delx = _x[i] - _x[i - 1]
                dely = _y[i] - _y[i - 1]
            else:
                dely = float(_y[i + 1] - _y[i - 1])
                delx = float(_x[i + 1] - _x[i - 1])
            result.append(float(dely) / float(delx))

        self.ydata = result

    def differentiate(self):
        '''Differentiate the data, using one-sided differencing.
        '''

        result = []
        _x = self.xdata
        _y = self.ydata
        N = len(_x)
        for i in range(1, N):
            delx = _x[i] - _x[i - 1]
            dely = _y[i] - _y[i - 1]
            result.append(float(dely) / float(delx))

        self.ydata = result
        self.xdata = _x[1:]


    def integrate(self):
        '''Integrate the data, using the average of current and next 
        Y values at each step.  Note that we end up with one less point
        than we started with.
        '''

        result = []
        _x = self.xdata
        _y = self.ydata
        N = len(_x)

        sum = 0
        for i in range(N - 1):
            sum += 0.5*(_y[i+1] + _y[i]) * (_x[i+1] - _x[i])
            result.append(sum)
        
        self.ydata = result
        del(self.xdata[N-1])

    def square(self):
        '''Square the y values of the data sequence.'''

        self.ydata = [y**2 for y in self.ydata]

    def absolute(self):
        '''Absolute values of the y values of the data sequence.'''

        self.ydata = [abs(y) for y in self.ydata]

    def log(self):
        '''Take the natural logarithm of the y values of the data sequence.
        If any of the values = 0.0, don't change the data, and return False,
        else change the data and return True.

        RETURNS
        False if any y values are <= 0.0, True otherwise
        '''

        for y in self.ydata:
            if y <= 0.0: return False

        self.ydata = [math.log(y) for y in self.ydata]
        return True

    def log10(self):
        '''Take the logarithm base 10 of the y values of the data sequence.
        If any of the values = 0.0, don't change the data, and return False,
        else change the data and return True.

        RETURNS
        False if any y values are 0.0, True otherwise
        '''

        for y in self.ydata:
            if y <= 0.0: return False

        self.ydata = [math.log(y, 10) for y in self.ydata]
        return True

    def multiply(self, ds):
        '''Multiply each Y value by the corresponding Y value in another
        Dataset.  The two Datasets must have the same number of points, but
        the values of the X values are ignored and don't have to be the same.
        Do nothing if the number of points is not the same. Return False
        if the number of points doesn't match, or True otherwise.

        ARGUMENT
        ds -- the data set whose points will be used to multiply the Y data by.

        RETURNS
        False if the two Datasets have different lengths, otherwise True.
        '''

        if len(self.xdata) != len(ds.xdata): return False

        _y = self.ydata
        _y1 = ds.ydata
        self.ydata = [_y[v] * _y1[v] for v in range(len(_y))]
        return True

    def divide(self, ds):
        '''Divide each Y value into the corresponding Y value in another
        Dataset.  That is, the other dataset will be the numerator.
        The two Datasets must have the same number of points, but
        the values of the X values are ignored and don't have to be the same.
        Do nothing if the number of points is not the same. Return False
        if the number of points doesn't match or if any point in the denominator
        dataset is zero, True otherwise. The denominator dataset has its
        y values changed.

        ARGUMENT
        ds -- the data set whose points will be used as the numerator.

        RETURNS
        False if the two Datasets have different lengths or the denominator
        contains a point with value 0.0, otherwise True.
        '''

        if len(self.xdata) != len(ds.xdata): return False

        _yd = self.ydata[:]
        if 0.0 in _yd: return False

        _yn = ds.ydata[:]
        num = len(self.xdata)
        self.ydata = [1.0 * _yn[v] / _yd[v] for v in range(num)]

        return True

    def rfft(self):
        '''Calculate the (amplitude of the) FFT of a real sequence.  The data
        is assumed to be equally spaced on the X axis.  Note that the number
        of points will be changed.'''

        self.ydata = np.abs(np.fft.rfft(self.ydata))
        # The maximum frequency is 0.5  / (delta_x)
        # The minimum frequency step is max / N = 0.5 / (n * delta_x)
        max_f = 0.5 / (self.xdata[1] - self.xdata[0])
        min_f = max_f / len(self.ydata)
        self.xdata = [(1 + i) * min_f for i in range(len(self.ydata))]
        #self.xdata = [i for i in range(len(self.ydata))]

    def halfSupergaussian(self, order=6):
        '''Apply a half-sided supergaussian window to the ydata.
        The data is smoothly attenuated to the right, and unchanged at 
        the left end.  Return False if there is no data, else return True.

        The supergaussian is defined as exp(-(x/2s)^n),
         where n is the order (n=2 for an ordinary gaussian) (yes, I know,
         the numerical factor should by sqrt(2), but this doesn't change
         anything for our purposes).  The value of the windowing function 
         is here aribrarily defined  as 0.01 at the rightmost data point.

         ARGUMENT
         order -- the exponent for the supergaussian

         RETURNS
         False if no data, True otherwise.
        '''

        if not self.xdata:
            return False

        endstep = 0.01  # height of window at right edge
        numPts = len(self.xdata)

        sigma = 0.5 * (numPts-1) * math.exp(-math.log(-math.log(endstep))/order)
        _y = self.ydata
        self.ydata = [_y[i] * math.exp(-math.pow((0.5*i/sigma), order)) \
            for i in range(0,  numPts)]

        return True

    def fullSuperGaussian(self, order=6):
        '''Apply a full gaussian window to the ydata.
        Return False if there is no data, else return True.

        The supergaussian is defined as exp(-(x/s*sqrt(2))^n)(yes, I know,
        the numerical factor should by sqrt(2), but this doesn't change
        anything for our purposes). 
        
        The value of the windowing function is here aribrarily defined  
        as 0.01 at the rightmost data point..

         ARGUMENT
         order -- the exponent for the supergaussian

         RETURNS
         False if no data, True otherwise.
        '''

        if not self.xdata:
            return False

        endstep = 0.01  # height of window at left and right edges.
        #sqrt2 = math.sqrt(2)
        numPts = len(self.xdata)
        mid = numPts / 2

        sigma = 0.5 * (numPts-1) * math.exp(-math.log(-math.log(endstep))/order)
        #s = sigma / sqrt2
        _y = self.ydata
        self.ydata = [_y[i] * math.exp(-math.pow(((i-mid)/sigma), order)) \
            for i in range(0,  numPts)]

        return True

    def halfCosine(self):
        '''Apply a half-sided cosine window to the ydata.
        The data is smoothly attenuated to the right, and unchanged at 
        the left end.  Return False if there is no data, else return True.

         RETURNS
         False if no data, True otherwise.
        '''

        if not self.xdata:
            return False

        # Argument = pi/2 at right hand end of data
        N = len(self.ydata)
        delta = 0.5 * math.pi /(N-1)

        angle = 0.0
        _y = self.ydata
        for i in range(N):
            _y[i] = _y[i] * math.cos(angle)
            angle += delta

        return True

    def fullCosine(self):
        '''Apply a cosine window to the ydata.
        The data is smoothly attenuated to the left and right, and 
        unchanged at the middle end.  Return False if there is no 
        data, else return True.

         RETURNS
         False if no data, True otherwise.
        '''

        if not self.xdata:
            return False

        # Argument ranges from -pi/2 to pi/2 
        N = len(self.ydata)
        delta = math.pi /(N-1)

        angle = -.5 * math.pi
        _y = self.ydata
        for i in range(N):
            _y[i] = _y[i] * math.cos(angle)
            angle += delta

        return True

    def convolve(self, ds):
        '''Convolve the Y data with the Ydata of the Dataset passed in.
        Replace the Y data with the convolution values.  The length
        of the result is the longer of the two data sets.  Replace the 
        X data with the X data of the longer of the two data sets.     
        Return False if neither of the data sets has data.

        There can be boundary effects, since there may be areas where
        the two data sets don't overlap properly.

        ARGUMENT
        ds -- the other Dataset to use in the convolution.

        RETURNS
        False if either of the Datasets has no points, True otherwise.
        '''

        if (self.ydata is None or ds.ydata is None
           or len(self.ydata) == 0 or  len(ds.ydata) == 0):
            return False

        self.ydata = np.convolve(self.ydata, ds.ydata, mode='same')
        if len(self.xdata) != len(self.ydata):
            if len(self.xdata) == len(ds.xdata):
                self.xdata = ds.xdata[:]
            else:
                self.xdata = list(range(len(self.ydata)))

        return True

    def correlate(self, ds):
        '''Correlate the Y data with the Ydata of the Dataset passed in.
        Replace the Y data with the convolution values.  The length
        of the result is the longer of the two data sets.  Replace the 
        X data with the X data of the longer of the two data sets.     
        Return False if neither of the data sets has data.

        Note that this operation is the signal processing kind of
        correlation, not a statistical type.  There can be boundary 
        effects, since there may be areas where the two data sets 
        don't overlap properly.

        ARGUMENT
        ds -- the other Dataset to use in the convolution.

        RETURNS
        False if either of the Datasets has no points, True otherwise.
        '''

        if self.isNumpyArray(self.ydata):
            if not self.ydata.any():
                return False
        elif self.isNumpyArray(ds.ydata):
            if not ds.ydata.any():
                return False
        else:
            if not self.ydata or not ds.ydata:
                return False

        self.ydata = np.correlate(self.ydata, ds.ydata, mode='same')
        if len(self.xdata) != len(self.ydata):
            if len(self.xdata) == len(ds.xdata):
                self.xdata = ds.xdata[:]
            else:
                self.xdata = list(range(len(self.ydata)))

        return True


    def lopass(self, a):
        '''Perform a single-pole low-pass filter on the Y data of the
        data set. Return True if the value of a is < 1.0 and the dataset
        has some points, False otherwise.
        
        The parameter a is a smoothing parameter, and equals
        t/d where t = the time constant (e.g., the RC time constant), 
        and d = the time step.  So a is the time constant in time steps.

        This filter emulates a simple RC circuit. 

        ARGUMENT
        a -- a smoothing parameter, must be > 0.

        RETURNS
        True if the value of a is < 0 and the dataset
        has some points,, False otherwise.

        '''
        
        if a <= 0.0: return False
        if self.isNumpyArray(self.ydata):
            if not self.ydata.any():
                return False
        else:
            if not self.ydata:
                return False
        
        #aa = a / (1.0 + a)
        aa = math.exp(-1.0 / a)
        b = 1.0 - aa
        lasty = 0
        filtered = []
        for i in range(len(self.ydata[0:])):
            newy = aa * lasty + b * self.ydata[i]
            filtered.append(newy)
            lasty = newy

        self.ydata = filtered

        return True


    def hipass(self, a, limit=0.1):
        '''Perform a single-pole high-pass filter on the Y data of the
        data set. Return True if the value of a is < 1.0 and the dataset
        has some points, False otherwise.
        
        The parameter a is a smoothing parameter, and equals
        t/d where t = the time constant (e.g., the RC time constant), 
        and d = the time step.  So a is the time constant in time steps.

        This filter emulates a simple RC circuit.

        ARGUMENT
        a -- a smoothing parameter, must be > 1.
        limit -- smallest allowed value for a

        RETURNS
        True if the value of a is < limit and the dataset
        has some points, False otherwise.

        '''

        if a < limit: return False
        if self.isNumpyArray(self.ydata):
            if not self.ydata.any():
                return False
        else:
            if not self.ydata:
                return False

        aa = math.exp(-1.0/a)
        lasty = 0
        lastyo = 0
        filtered = []
        for y in self.ydata:
            newy = aa * lasty + aa * (y - lastyo)
            filtered.append(newy)
            lasty = newy
            lastyo = y

        self.ydata = filtered

        return True

    def var_ratio(self, w):
        '''Compute ratio of short-term to long-term variance.  Replace
        the Y data of the data set with the variance ratio.

        The long-term variance uses all the data from time t=0 to the 
        current point.  The short-term variance uses only the data from the 
        current point back to w steps earlier.

        ARGUMENT
        w -- width in x steps for the short-term data window.

        RETURNS
        False if the Dataset has no points, or w < 2. True otherwise.
        '''

        if w < 2: return False
        if self.isNumpyArray(self.ydata):
            if not self.ydata.any():
                return False
        elif not self.ydata:
            return False

        sy = 0.0
        syy = 0.0
        varlong = []

        for N, _y in enumerate(self.ydata):
            if N == 0:
                varlong.append(1.0)
                syy = math.pow(self.ydata[0], 2)
                sy = self.ydata[0]
                continue

            syy += _y * _y
            sy += _y
            var = syy / N - math.pow(sy / N, 2)
            varlong.append(max(var, 0.0))

        varshort = []

        for N in range(len(self.ydata)):
            if N == 0:
                varshort.append(1.0)
                continue
            if N <= w:
                _dat = self.ydata[:N+1]
            else:
                _dat = self.ydata[N-w:N+1]
            sumshort = 0.0
            sumsqr_short = 0.0
            for _y in _dat:
                sumshort += _y
                sumsqr_short += math.pow(_y,2)
            _n = len(_dat) - 1
            var = sumsqr_short / _n - math.pow(sumshort / _n, 2)
            varshort.append(var)

        result = []
        for n, varl in enumerate(varlong):
            if varl > 0.0:
                result.append(varshort[n] / varl)
            else:
                result.append(1.0)

        self.ydata = result

        return True

    def var_ratio2(self, w):
        '''Compute ratio of short-term to long-term variance.  Replace
        the Y data of the data set with the variance ratio.

        The long-term variance uses all the data from time t=0 to the 
        current point.  The short-term variance uses only the data from the 
        current point back to w steps earlier.

        ARGUMENT
        w -- width in x steps for the short-term data window.

        RETURNS
        False if the Dataset has no points, or w < 2. True otherwise.
        '''

        if w < 2: return False
        if self.isNumpyArray(self.ydata):
            if not self.ydata.any():
                return False
        elif not self.ydata:
            return False

        sumlong = 0.0
        sumsqr_long = 0.0
        varlong = []

        for N in range(len(self.ydata)):
            if N == 0:
                varlong.append(1.0)
                continue
            sumlong = 0.0
            sumsqr_long = 0.0
            _dat = self.ydata[:N+1]
            for _y in _dat:
                sumlong += _y
                sumsqr_long += math.pow(_y, 2)
            _n = len(_dat) - 1
            var = sumsqr_long / _n - math.pow(sumlong / _n, 2)
            varlong.append(var)

        varshort = []

        for N in range(len(self.ydata)):
            if N == 0:
                varshort.append(1.0)
                continue
            if N <= w:
                _dat = self.ydata[:N+1]
            else:
                _dat = self.ydata[N-w:N+1]
            sumshort = 0.0
            sumsqr_short = 0.0
            for _y in _dat:
                sumshort += _y
                sumsqr_short += math.pow(_y,2)
            _n = len(_dat) - 1
            var = sumsqr_short / _n - math.pow(sumshort / _n, 2)
            varshort.append(var)

        result = []
        for n, varl in enumerate(varlong):
            if varl > 0.0:
                result.append(varshort[n] / varl)
            else:
                result.append(0.0)

        self.ydata = result

        return True

    def sliding_var(self, w):
        '''Compute the variance of the y data over a window that slide across the data.
        The x value of the variance is assigned to be the center of the window. Return
        a sequence containing the computed standard deviations, and the s.d. of
        the entire data set.  There will be fewer points than for the original data.

        Assumes that the data points are equally spaced in the x axis.

        ARGUMENT
        w -- the window width in number of data points. Must be < N - 3.

        RETURNS
        (x, s, stddev), where x, vare  sequences where x are the new x values 
        and s are the std devs in the window, or None if w is too large.
        '''

        N = len(self.xdata)
        if w >= N - 3:
            return None

        newx = []
        vars = []
        delta = w * (self.xdata[1] - self.xdata[0]) / 2.0
        factor = 1.0 / (w - 1)

        for i in range(len(self.xdata) - w):
            _y = self.ydata[i:i+w]
            newx.append(self.xdata[i] + delta)
            mean = 1.0* sum(_y) / w
            var = sum([factor * (y - mean)**2 for y in _y]) 
            vars.append(var**0.5)

        mean = 1.0* sum(self.ydata) / N
        var = sum([(1.0 / (N-1)) * (y - mean)**2 for y in self.ydata]) 

        return newx, vars, var**0.5

    def thin(self, stride=4):
        '''Thin a data set by keeping every nth point. Return the 
        original data set with the x and y data thinned.

        ARGUMENT
        stride -- an integer to thin by.

        RETURNS
        a new thinned data set
        '''

        xdata = self.xdata
        ydata = self.ydata

        new_xdata = []
        new_ydata = []
        for i in range(0, len(xdata), stride):
            new_xdata.append(xdata[i])
            new_ydata.append(ydata[i])

        self.xdata = new_xdata
        self.ydata = new_ydata
        return self
        
if __name__ == '__main__':
    import random 
    import matplotlib.pyplot as plt
    #from pylab import rcParams,  gcf

    passfail = {True:'Pass', False:'Fail'}
    base_xdata = [1,2,3,4,5,6,7,8,9,10]
    base_ydata = base_xdata[:]

    def self_printer(f):
        def new_f():
            print (f.func_name)
            print (f.func_doc or '')
            f()
            print()
        return new_f

    def test_pad():
        '''Test padding'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.pad_truncate(13)

        expected = ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 0, 0])
        if expected == (ds.xdata, ds.ydata):
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (ds.ydata, ds.xdata)
            print ('====Fail=====')
        print()

    def test_truncate():
        '''Test truncation'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.pad_truncate(3)

        expected = ([1, 2, 3],
                    [1, 2, 3])
        if expected == (ds.xdata, ds.ydata):
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print ((ds.ydata, ds.xdata))
            print ('====Fail=====')
        print()

    def shift_right():
        '''Test shifting right by 3'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.shift(3)

        expected = [0,0,0,1,2,3,4,5,6,7]
        if expected == ds.ydata:
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (ds.ydata)
            print ('====Fail=====')
        print()

    def shift_left():
        '''Test shifting left by 3'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.shift(-3)

        expected = [4,5,6,7,8,9,10,0,0,0]
        if expected == ds.ydata:
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (ds.ydata)
            print ('====Fail=====')
        print()

    def shift_right_many():
        '''Test shift right by too many points'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.shift(20)

        expected = [0,0,0,0,0,0,0,0,0,0]
        if expected == ds.ydata:
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (ds.ydata)
            print ('====Fail=====')
        print()

    def test_scale():
        '''Test Scaling by factor 2'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.scale(2)

        expected = [2,4,6,8,10,12,14,16,18,20]
        if expected == ds.ydata:
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (ds.ydata)
            print ('====Fail=====')
        print()

    def test_transpose():
        '''Test Transposing Axes'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.transpose()

        expected = (base_ydata, base_xdata)
        if expected == (ds.ydata, ds.xdata):
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print ((ds.ydata, ds.xdata))
            print ('====Fail=====')
        print()

    def test_add_constant():
        '''Test Adding constant 2.5 to Y axis data'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = base_ydata[:]
        ds.addConstant(2.5)

        expected = [2.5 + y for y in base_ydata]
        if expected == ds.ydata:
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (ds.ydata)
            print ('====Fail=====')
        print()

    def test_halfsupergauss():
        '''Test half Supergaussian window of order 6'''
        ds = Dataset()
        _x = []; _y = []
        for i in range(20):
            _x.append(i)
            _y.append(1.0)
        _y[0] = 0.0

        ds.xdata = _x
        ds.ydata = _y

        ds.halfSupergaussian(6)
        print (''.join(['%0.4f\n' % (ds.ydata[i]) for i in range(len(ds.ydata))]))
        print()

    def test_supergauss():
        '''Test Supergaussian window of order 2'''
        ds = Dataset()
        _x = []; _y = []
        for i in range(100):
            _x.append(i)
            _y.append(1.0)
        #_y[0] = 0.0

        ds.xdata = _x
        ds.ydata = _y

        ds.fullSuperGaussian(2)
        print (''.join(['%0.4f\n' % (ds.ydata[i]) for i in range(len(ds.ydata))]))
        print()

    def test_len_method():
        '''Test len() function on Dataset'''

        ds = Dataset()
        passed = False

        ds.xdata = np.array([1,2,3])
        ds.ydata = [4,5,6]

        print ('  ds with data')
        print ('    if ds:', )
        passed = bool(ds)
        print (passfail[passed])
        print()

        ds.xdata = np.array([])
        passed = False
        print ('  Empty data array')
        print ('    if len(ds):', )
        if len(ds): passed = False
        else: passed =  True
        print (passfail[passed])
        print()

        ds = Dataset()
        print ('  New ds' )
        print ('    if ds:',)
        if ds: passed =  False
        else: passed =  True
        print (passfail[passed])
        print()

    def test_lopass():
        '''Test Low-pass filter lopass()'''
        ds = Dataset()
        ds.xdata = base_xdata[:]
        ds.ydata = [0,1,1,1,1,1,1,1,1,1]
        a = 5
        ds.lopass(a)
        results =  ','.join('%0.3f' % (x) for x in ds.ydata)
        expected = ','.join('%0.3f' % (x) for x in (0.000,0.181,
            0.330,0.451,0.551,0.632,0.699,0.753,0.798,0.835))
        if results == expected:
            print ('Pass')
        else:
            print ('Expected:')
            print (expected)
            print ('Actual:')
            print (results)
            print ('====Fail====')
        print()

    @self_printer
    def test_sliding_var():
        '''Sliding variances'''
        ds = Dataset()

        N = 100
        ds.xdata = x = [0.05*i for i in range(0, N)]
        ds.ydata = [random.uniform(-.5, .5) for z in x]

        _newx, stds, sigma = ds.sliding_var(15)

        plt.plot(_newx, stds, 'b')
        plt.plot(ds.xdata, ds.ydata, 'ro')
        plt.plot((ds.xdata[0], ds.xdata[-1]), (sigma, sigma), 'black')
        plt.show()

                                                   
    Tests = [test_halfsupergauss, test_supergauss]#test_sliding_var, test_lopass]
    for f in Tests:
        #print f.__doc__ or ''
        f()
