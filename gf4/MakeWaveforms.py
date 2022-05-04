#@+leo-ver=5-thin
#@+node:tom.20211211171304.65: * @file MakeWaveforms.py
#@+others
#@+node:tom.20211211171304.66: ** Imports
"""Plotting routines for gf4. This code was removed from the
PlotManager class to reduce the size of the class.  The name
of the parameter "self" has been retained to simplify this
refactoring."""

from curve_generators import (generateExponential, generateSine, generateDampedSine,
                   generateRectangle, generateRamp, generateSquarewave,
                   generateGaussian,generateGaussianCdf)
from entry import GetSingleFloat, GetTwoFloats

from AbstractPlotMgr import MAIN
from Dataset import Dataset
from randnum import rand_vals, uniform_vals, gaussian_vals

#@+node:tom.20211211171304.67: ** makeExponential
def makeExponential(self):
    _id = str(self.makeExponential)
    lastparm = self.parmsaver.get(_id, 3.0)

    dia = GetSingleFloat(self.root, 'Parameter', 'Decay', lastparm)
    if not dia.result: return
    self.parmsaver[_id] = dia.result

    decay = dia.result
    N = self.num
    _ds = Dataset(*generateExponential(N, decay))
    _ds.figurelabel = 'Exponential'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.68: ** makeSine
def makeSine(self):
    _id = str(self.makeSine)
    lastparm = self.parmsaver.get(_id, 5)

    dia = GetSingleFloat(self.root, 'Number Of Cycles', 'Cycles', lastparm)
    if not dia.result:
        return
    self.parmsaver[_id] = dia.result

    cycles = dia.result
    n = self.num
    _ds = Dataset(*generateSine(n, cycles))
    _ds.figurelabel = 'Sine Wave'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.69: ** makeDampedSine
def makeDampedSine(self):
    _id = str(self.makeDampedSine)
    lastc, lastd = self.parmsaver.get(_id, (5, 3.0))

    dia = GetTwoFloats(self.root, 'Parameters', 'Cycles',
                       'Decay', lastc, lastd)
    if not dia.result: return

    cycles, decay = self.parmsaver[_id] = dia.result
    N = self.num
    _ds = Dataset(*generateDampedSine(N, cycles, decay))
    _ds.figurelabel = 'Damped Sine'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.70: ** makeStep
def makeStep(self):
    N = self.num
    _ds = Dataset()
    _ds.xdata, _ds.ydata = generateRectangle(N)
    _ds.figurelabel = 'Rectangular Step'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.71: ** makeDelta
def makeDelta(self):
    '''Generate a delta function of amplitude 1, located at the start
    of the waveform
    '''

    N = self.num
    _ds = Dataset()
    _ds.xdata = list(range(N))
    _ds.ydata = [0.0] * N
    _ds.ydata[1] = 1.0
    _ds.figurelabel = 'Delta Function'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.72: ** makeRamp
def makeRamp(self):
    N = self.num
    _ds = Dataset()
    _ds.xdata, _ds.ydata = generateRamp(N)
    _ds.figurelabel = 'Linear Ramp'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.73: ** makeSquarewave
def makeSquarewave(self):
    _id = str(self.makeSquarewave)
    lastparm = self.parmsaver.get(_id, 5)

    dia = GetSingleFloat(self.root, 'Number Of Cycles', 'Cycles', lastparm)
    if not dia.result:
        return
    self.parmsaver[_id] = dia.result

    cycles = dia.result
    N = self.num
    _ds = Dataset()
    _ds.xdata, _ds.ydata = generateSquarewave(N, cycles)
    _ds.figurelabel = 'Squarewave'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.74: ** makeRandomNoise
def makeRandomNoise(self):
    _x, _y = rand_vals(self.num)
    _ds = Dataset()
    _ds.xdata = _x
    _ds.ydata = _y
    _ds.figurelabel = 'Random Noise'
    _ds.yaxislabel = 'Value'
    _ds.xaxislabel = 'n'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.75: ** makeUniformNoise
def makeUniformNoise(self):
    _x, _y = uniform_vals(-0.5, 0.5, self.num)
    _ds = Dataset()
    _ds.xdata = _x
    _ds.ydata = _y
    _ds.figurelabel = 'Uniform Noise'
    _ds.yaxislabel = 'Value'
    _ds.xaxislabel = 'n'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.76: ** makeGaussianNoise
def makeGaussianNoise(self):
    _id = str(self.makeGaussianNoise)
    lastm, lasts = self.parmsaver.get(_id, (0.0, 1.0))

    dia = GetTwoFloats(self.root, 'Parameters', 'Mean',
                       'Sigma', lastm, lasts)
    if not dia.result: return
    self.parmsaver[_id] = dia.result

    m, sig = dia.result
    _x, _y = gaussian_vals(m, sig, self.num)
    _ds = Dataset()
    _ds.xdata = _x
    _ds.ydata = _y
    _ds.figurelabel = 'Gaussian Noise m=%0.3f, s=%0.3f' % (m, sig)
    _ds.yaxislabel = 'Value'
    _ds.xaxislabel = 'n'

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.77: ** pdfGaussian
def pdfGaussian(self):
    _id = str(self.pdfGaussian)
    lastm, lasts = self.parmsaver.get(_id, (0.0, 2.0))

    dia = GetTwoFloats(self.root, 'Parameters', 'Mean',
                       'Sigma', lastm, lasts)
    if not dia.result: return
    self.parmsaver[_id] = dia.result

    m, sig = dia.result
    _xdata, _ydata = generateGaussian(self.num, m, sig)
    _ds = Dataset()
    _ds.xdata = _xdata
    _ds.ydata = _ydata
    _ds.figurelabel = 'Gaussian PDF m=%0.3f, s=%0.3f' % (m, sig)

    self.set_data(_ds, MAIN)
    self.plot()

#@+node:tom.20211211171304.78: ** cdfGaussian
def cdfGaussian(self):
    _id = str(self.cdfGaussian)
    lastm, lasts = self.parmsaver.get(_id, (0.0, 2.0))

    dia = GetTwoFloats(self.root, 'Parameters', 'Mean',
                       'Sigma', lastm, lasts)
    if not dia.result: return
    self.parmsaver[_id] = dia.result

    m, sig = dia.result
    _xdata, _ydata = generateGaussianCdf(self.num, m, sig)
    _ds = Dataset()
    _ds.xdata = _xdata
    _ds.ydata = _ydata
    _ds.figurelabel = 'Gaussian CDF m=%0.3f, s=%0.3f' % (m, sig)

    self.set_data(_ds, MAIN)
    self.plot()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
