#@+leo-ver=5-thin
#@+node:tom.20211211170819.2: * @file BuildCommands.py
# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211170819.4: ** buildCommands
def buildCommands(self):
    '''Create a dictionary of commands keyed by strings.
    Intended for use in macros and by an auxilary command
    window.
    '''

    self.commands = {
       'sine': self.makeSine,
       'dsin': self.makeDampedSine,
       'expon': self.makeExponential,
       'delta': self.makeDelta,
       'step': self.makeStep,
       'ramp': self.makeRamp,
       'sqw': self.makeSquarewave,

       'pdfgaus': self.pdfGaussian,
       'cdfgaus': self.cdfGaussian,
       'uninoise': self.makeUniformNoise,
       'gausnoise': self.makeGaussianNoise,

       'plot': self.plot,
       'plottop': self.plot_stack_top,
       'overplot': self.overplot,
       'overplotbuf': self.overplotbuff,
       'overplottop': self.overplot_stack_top,
       'overploterr': self.overplot_errorbands,

       'loadclip': self.load_data_from_popup,
       'save2clip': self.copy_data_to_clipboard,
       'stox': self.store1,
       'rclx': self.recall1,

       'linear': self.setLinLin,
       'semilogy': self.setSemilogY,
       'semilogx': self.setSemilogX,
       'loglog': self.setLogLog,

       'copy2buff': self.copyToBuffer,
       'swap': self.swap_data,
       'copyfrom': self.paste_data,
       'copyfromtop': self.copy_from_top,
       'copy2top': self.copy_to_top,
       'push': self.push_with_copy,
       'drop': self.drop_stack,
       'rotateup': self.rotate_stack_up,
       'rotatedn': self.rotate_stack_down,

       'dedup': self.dedup,
       'pad': self.pad_truncate,
       'shift': self.shift,
       'thin': self.decimate,
       'trim': self.trim, 
       'transpose': self.transpose,
       'sortx': self.sortX,
       'phase': self.make_phasespace,
       'YvsX': self.YvsX,
       'numpts': self.setNumPoints,
       'newX': self.replaceX,

       'addbuf': self.addBuffer,
       'subbuf': self.subFromBuffer,
       'mulbuf': self.mulBuffer,
       'divbuf': self.divBuffer,
       'diff': self.differentiate,
       'diff2': self.differentiate2,
       'int': self.integrate,
       'addcnst': self.add_constant,
       'scale': self.scale,
       'log': self.log10,
       'ln': self.log,
       'sqr': self.square,

       'rectify': self.rectify,
       'halfrect': self.half_rectify, 
       'clip': self.clip,
       'normalize': self.normalize,
       'zero_data': self.zero,

       'cubicspln': self.cubicSpline,
       'lstsqrlin': self.leastsqr,
       'lstsqrquad': self.leastsqr_quad,
       'lowess': self.lowess,
       'lowessquad': self.lowess2Quad,
       'lowessadapt': self.lowess_adaptive,
       'lowesscorrel': self.lowess_adaptive_ac,
       'splinesmooth': self.spline_smooth,
       'poisson': self.poissonSmooth,
       'thiel_sen': self.thiel,

       'fft': self.fft,
       'convolve': self.convolveWithBuffer,
       'correl': self.correlateWithBuffer,
       'autocor': self.autocorrelate,
       'lopass': self.lopass,
       'hipass': self.hipass,
       'move-median': self.moving_median,

       'halfcoswin': self.h_cosine,
       'coswin': self.full_cosine,
       'halfsupergwin': self.h_super_gaussian,
       'gaussianwin': self.gaussian_window,
       'supergausswin': self.super_gaussian,

       'cdf': self.cdf,
       'fitcdf': self.fitCdfWithNormal,
       'fitcdfadapt': self.fitCdfNormalAdaptive,
       'hist': self.histogram,
       'meanstd': self.mean_std,
       'corrcoeff': self.correlationCoeff,
       'spearman': self.spearman,
       'pearson': self.pearson,
       'sliding_var': self.sliding_var,

       'mann_kendall': self.trend_mann_kendall,
       'piecewise': self.fit_piecewise,
       'timehack': self.addTimehack,
    }
#@-others
#@@language python
#@@tabwidth -4
#@-leo
