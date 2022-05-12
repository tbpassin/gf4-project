#@+leo-ver=5-thin
#@+node:tom.20211211170819.26: * @file createMenus.py
# pylint: disable = consider-using-f-string, undefined-variable
#@+others
#@+node:tom.20211211170819.27: ** Imports
try:
    import Tkinter as Tk
except:
    import tkinter as Tk

from Linestyle import (LINETHIN, LINEMED, LINETHICK, CIRCLE, DIAMOND,
                       HEXAGON, SQUARE, TRIANGLE, TRIANGLE_LEFT)
from colors import (WHITE, BLACK, LIGHTBLUE, DEEPSKYBLUE, CORNFLOWERBLUE,
                    MEDGRAY)

from help import about, tutorial, blog
from stackview import stackwin

#@+node:tom.20211211170819.28: ** setMenus
def setMenus(self):
    """Create the menus for gf4.

    This code was moved here from the main gf4.pyw file.  Since there is no 
    class involved here, the use of "self" seems strange.  But the calling
    object uses its own "self" value for the call.  Perhaps I should 
    have changed the name of the parameter, but this was easier since
    nothing needed to be changed in the code.
    
    ARGUMENT
    self -- the "self" variable of the calling object.

    RETURNS
    the menu structure.
    """
    # pylint: disable = too-many-locals
    # pylint: disable = too-many-statements
    # Create a toplevel menu
    mainMenu = Tk.Menu(self.root)

    #@+others
    #@+node:tom.20220401195652.1: *3* Plot
    plotSubmenu = Tk.Menu(self.root)

    commands = (
        ("Plot", self.plotmain, 0),
        ("Overplot Main", self.overplot, 10),
        ("Overplot Buffer", self.overplotbuff, 9)
    )

    for label, command, underline in commands:
        plotSubmenu.add_command(label = label, command = command, underline = underline)

    plotSubmenu.add_separator()


    commands = (
        ('Lin-lin', self.setLinLin),
        ('Semilog(Y)', self.setSemilogY),
        ('Semilog(X)', self.setSemilogX),
        ('Log-log', self.setLogLog)
    )

    for label, command in commands:
        plotSubmenu.add_radiobutton(label = label, command = command)

    #@+node:tom.20220401201301.1: *4* Marker Submenu
    plotSubmenu.add_separator()

    mainMarkerSubmenu = Tk.Menu(self.root)
    plotSubmenu.add_cascade(label='Main Marker Style',
        menu=mainMarkerSubmenu)

    self.main_marker_style = Tk.StringVar()
    mainMarkerSubmenu.add_radiobutton(
        label='Line', variable=self.main_marker_style, value=1,
        command=self.setMainMarkerStyle)
    mainMarkerSubmenu.add_radiobutton(
        label='Symbol', variable=self.main_marker_style, value=2,
        command=self.setMainMarkerStyle)
    mainMarkerSubmenu.add_radiobutton(
        label='Both', variable=self.main_marker_style, value=3,
        command=self.setMainMarkerStyle)

    bufferMarkerSubmenu = Tk.Menu(self.root)
    plotSubmenu.add_cascade(label='Buffer Marker Style',
        menu=bufferMarkerSubmenu)
    self.buffer_marker_style = Tk.StringVar()
    bufferMarkerSubmenu.add_radiobutton(
        label='Line', variable=self.buffer_marker_style, value=1,
        command=self.setBufferMarkerStyle)
    bufferMarkerSubmenu.add_radiobutton(
        label='Symbol', variable=self.buffer_marker_style, value=2,
        command=self.setBufferMarkerStyle)
    bufferMarkerSubmenu.add_radiobutton(
        label='Both', variable=self.buffer_marker_style, value=3,
        command=self.setBufferMarkerStyle)
    #@+node:tom.20220401201342.1: *4* Linestyles Submenu
    lineStyleSubmenu = Tk.Menu(self.root)
    plotSubmenu.add_cascade(label='Linestyles', menu=lineStyleSubmenu)
    mainLinestyleSubmenu = Tk.Menu(self.root)
    bufferLinestyleSubmenu = Tk.Menu(self.root)
    lineStyleSubmenu.add_cascade(label='Main', menu=mainLinestyleSubmenu)
    lineStyleSubmenu.add_cascade(label='Buffer',
        menu=bufferLinestyleSubmenu)

    plotSubmenu.add_separator()

    for _label, _width in (
            ('Thin', str(LINETHIN)),
            ('Medium', str(LINEMED)),
            ('Thick', str(LINETHICK))):
        mainLinestyleSubmenu.add_radiobutton(
                label=_label,
                variable=self.radio_main_linestyle, value=_width,
                command=self.setMainLineWidth, underline=0)
        bufferLinestyleSubmenu.add_radiobutton(
                label=_label,
                variable=self.radio_buffer_linestyle, value=_width,
                command=self.setBufferLineWidth, underline=0)
    #@+node:tom.20220401201409.1: *4* Symbol Submenu
    symbolStyleSubmenu = Tk.Menu(self.root)
    plotSubmenu.add_cascade(label='Symbol Shapes', menu=symbolStyleSubmenu)
    mainSymbolstyleSubmenu = Tk.Menu(self.root)
    bufferSymbolstyleSubmenu = Tk.Menu(self.root)
    symbolStyleSubmenu.add_cascade(label='Main', menu=mainSymbolstyleSubmenu)
    symbolStyleSubmenu.add_cascade(label='Buffer', menu=bufferSymbolstyleSubmenu)

    mainSymbolstyleSubmenu.add_radiobutton(
        label='circle', variable=self.main_symbol_shape,
        value=CIRCLE, command=self.setSymShapeMain)
    mainSymbolstyleSubmenu.add_radiobutton(
        label='diamond', variable=self.main_symbol_shape,
        value=DIAMOND, command=self.setSymShapeMain)
    mainSymbolstyleSubmenu.add_radiobutton(
        label='hexagon', variable=self.main_symbol_shape,
        value=HEXAGON, command=self.setSymShapeMain)
    mainSymbolstyleSubmenu.add_radiobutton(
        label='square', variable=self.main_symbol_shape,
        value=SQUARE, command=self.setSymShapeMain)
    mainSymbolstyleSubmenu.add_radiobutton(
        label='triangle', variable=self.main_symbol_shape,
        value=TRIANGLE, command=self.setSymShapeMain)
    mainSymbolstyleSubmenu.add_radiobutton(
        label='triangle-left', variable=self.main_symbol_shape,
        value=TRIANGLE_LEFT, command=self.setSymShapeMain)

    bufferSymbolstyleSubmenu.add_radiobutton(
        label='circle', variable=self.buffer_symbol_shape,
        value=CIRCLE, command=self.setSymShapeBuffer)
    bufferSymbolstyleSubmenu.add_radiobutton(
        label='diamond', variable=self.buffer_symbol_shape,
        value=DIAMOND, command=self.setSymShapeBuffer)
    bufferSymbolstyleSubmenu.add_radiobutton(
        label='hexagon', variable=self.buffer_symbol_shape,
        value=HEXAGON, command=self.setSymShapeBuffer)
    bufferSymbolstyleSubmenu.add_radiobutton(
        label='square', variable=self.buffer_symbol_shape,
        value=SQUARE, command=self.setSymShapeBuffer)
    bufferSymbolstyleSubmenu.add_radiobutton(
        label='triangle', variable=self.buffer_symbol_shape,
        value=TRIANGLE, command=self.setSymShapeBuffer)
    bufferSymbolstyleSubmenu.add_radiobutton(
        label='triangle-left', variable=self.buffer_symbol_shape,
        value=TRIANGLE_LEFT, command=self.setSymShapeBuffer)
    #@+node:tom.20220401201458.1: *4* Color Submenu
    colorSubmenu = Tk.Menu(self.root)
    plotSubmenu.add_cascade(label='Colors', menu=colorSubmenu)

    # Menu to change plot background color
    bgColorSubmenu = Tk.Menu(self.root)
    colorSubmenu.add_cascade(label='Plot BG Color', menu=bgColorSubmenu)
    for _label, _color in (
            ('White', WHITE), 
            ('Black', BLACK),
            ('Light Blue', LIGHTBLUE),
            ('Deep Sky Blue', DEEPSKYBLUE),
            ('Cornflower Blue', CORNFLOWERBLUE),
            ('Medium Gray', MEDGRAY)):
        bgColorSubmenu.add_radiobutton(
                label=_label, variable=self.graph_bg_color, value=_color,
                command=self.setBgColor)

    mainSymColorSubmenu = Tk.Menu(self.root)
    colorSubmenu.add_cascade(label='Main Symbol Color',
        menu = mainSymColorSubmenu)
    bufferSymColorSubmenu = Tk.Menu(self.root)
    colorSubmenu.add_cascade(label='Buffer Symbol Color',
        menu=bufferSymColorSubmenu)
    mainLineColorSubmenu = Tk.Menu(self.root)
    colorSubmenu.add_cascade(label='Main Line Color',
        menu=mainLineColorSubmenu)
    bufferLineColorSubmenu = Tk.Menu(self.root)
    colorSubmenu.add_cascade(label='Buffer Line Color',
        menu=bufferLineColorSubmenu)

    for _label, _color in (
            ('White', WHITE),
            ('Black', BLACK),
            ('Blue', 'blue'),
            ('Cyan', 'cyan'),
            ('Green', 'green'),
            ('Magenta', 'Magenta'),
            ('Red', 'red'),
            ('Yellow', 'Yellow'),
            ('Gray', 'gray')):
        mainSymColorSubmenu.add_radiobutton(
                label=_label, variable=self.main_symbol_color,
                value=_color, command=self.setSymColorMain)
        bufferSymColorSubmenu.add_radiobutton(
                label=_label, variable=self.buffer_symbol_color,
                value=_color, command=self.setSymColorBuffer)
        mainLineColorSubmenu.add_radiobutton(
                label=_label, variable=self.main_line_color,
                value=_color, command=self.setLineColorMain)
        bufferLineColorSubmenu.add_radiobutton(
                label=_label, variable=self.buffer_line_color,
                value=_color, command=self.setLineColorBuffer)
    #@+node:tom.20220401195940.1: *3* fileSubmenu
    fileSubmenu = Tk.Menu(self.root)
    fileSubmenu.add_command(label='Open',
        command=self.load_data,
        underline=0)
    fileSubmenu.add_command(label='Load From Dialog', 
        command=self.load_data_from_popup, underline=0)
    fileSubmenu.add_command(label='Save',
        command=self.save_data,
        underline=0, state=Tk.ACTIVE)
    fileSubmenu.add_separator()
    fileSubmenu.add_command(label="eXit", command=self.quit,
        accelerator='<Alt-F4>', underline=1)
    #@+node:tom.20220401195954.1: *3* stackSubmenu
    stackSubmenu = Tk.Menu(self.root)
    stackSubmenu.add_command(label='Copy To Buffer', 
                command=self.copyToBuffer, underline=0)
    stackSubmenu.add_command(label='Swap Main and Buffer', 
                command=self.swap_data, underline=1)
    stackSubmenu.add_command(label='Copy From Buffer', 
                command=self.paste_data, underline=0)
    stackSubmenu.add_separator()
    stackSubmenu.add_command(label='Copy From Top',
                command=self.copy_from_top, underline=5)
    stackSubmenu.add_command(label='Copy To Top',
                command=self.copy_to_top, underline=3)
    stackSubmenu.add_separator()
    stackSubmenu.add_command(label='Push with Copy',
                command=self.push_with_copy, underline=3)
    stackSubmenu.add_command(label='Drop', 
                command=self.drop_stack, underline=0)
    stackSubmenu.add_command(label='Rotate Up', 
                command=self.rotate_stack_up, underline=7)
    stackSubmenu.add_command(label='Rotate Down', 
                command=self.rotate_stack_down, underline=7)
    #@+node:tom.20220401200034.1: *3* curveSubmenu
    curveSubmenu = Tk.Menu(self.root)
    curveSubmenu.add_command(label='Pad/Truncate',
        command=self.pad_truncate,
        underline=4)
    curveSubmenu.add_command(label='Shift Left/Right',
        command=self.shift, underline=1)
    curveSubmenu.add_command(label='Thin',
        command=self.decimate, underline=0)
    curveSubmenu.add_command(label='Transpose', 
        command=self.transpose, underline=1)
    curveSubmenu.add_command(label='Sort On X',
        command=self.sortX, underline=2)
    curveSubmenu.add_command(label='Make Phase Space', 
        command=self.make_phasespace, underline=1)
    curveSubmenu.add_command(label='Y vs X',
        command=self.YvsX, underline=1)
    curveSubmenu.add_separator()
    curveSubmenu.add_command(label='Set Number Of Points',
        command=self.setNumPoints, underline=4)
    curveSubmenu.add_command(label='Replace X Axis',
        command=self.replaceX, underline=8)
    #@+node:tom.20220401200047.1: *3* waveformMathSubmenu
    waveformMathSubmenu = Tk.Menu(self.root)

    waveformMathSubmenu.add_command(label='Add Buffer',
        command=self.addBuffer, underline=0)
    waveformMathSubmenu.add_command(label='Subtract From Buffer',
        command=self.subFromBuffer, underline=0)
    waveformMathSubmenu.add_command(label='Multiply By Buffer',
        command=self.mulBuffer, underline=0)
    waveformMathSubmenu.add_command(label='Divide Into Buffer',
        command=self.divBuffer, underline=0)

    waveformMathSubmenu.add_separator()

    waveformMathSubmenu.add_command(label='Differentiate',
        command=self.differentiate, underline=0)
    waveformMathSubmenu.add_command(label='Integrate',
        command=self.integrate, underline=0)

    waveformMathSubmenu.add_separator()

    waveformMathSubmenu.add_command(label='Add Constant',
        command=self.add_constant, underline=4)
    waveformMathSubmenu.add_command(label='Scale', command=self.scale,
        underline=3)
    waveformMathSubmenu.add_command(label='Log10', command=self.log10,
        underline=2)
    waveformMathSubmenu.add_command(label='Natural Log', 
        command=self.log, underline=0)

    waveformMathSubmenu.add_separator()

    waveformMathSubmenu.add_command(label='Square', command=self.square,
        underline=1)
    waveformMathSubmenu.add_command(label='Rectify', command=self.rectify,
        underline=0)
    waveformMathSubmenu.add_command(label='Normalize', command=self.normalize,
        underline=0)
    #@+node:tom.20220401200120.1: *3* dataProcessingSubmenu 
    dataProcessingSubmenu = Tk.Menu(self.root)
    dataProcessingSubmenu.add_command(label='FFT', command=self.fft,
        underline=0)
    dataProcessingSubmenu.add_command(label='Convolve With Buffer',
        command=self.convolveWithBuffer, underline=2)
    dataProcessingSubmenu.add_command(label='Correlate With Buffer',
        command=self.correlateWithBuffer, underline=0)
    dataProcessingSubmenu.add_command(label='AutoCorrelation',
        command=self.autocorrelate, underline=0)
    dataProcessingSubmenu.add_command(label='Moving Median',
        command=self.moving_median, underline=0)

    dataProcessingSubmenu.add_command(label='Low Pass RC Filter',
        command=self.lopass, underline=0)
    dataProcessingSubmenu.add_command(label='High Pass RC Filter',
        command=self.hipass, underline=0)
    #@+node:tom.20220401200152.1: *3* windowSubmenu 
    windowSubmenu = Tk.Menu(self.root)
    dataProcessingSubmenu.add_cascade(label='Window', menu=windowSubmenu)
    windowSubmenu.add_command(label='Half Cos Window',
        command=self.h_cosine, underline=0)
    windowSubmenu.add_command(label='Full Cosine Window',
        command=self.full_cosine, underline=0)
    windowSubmenu.add_command(label='Half Supergaussian Window',
        command=self.h_super_gaussian, underline=0)
    windowSubmenu.add_command(label='Gaussian Window',
        command=self.gaussian_window, underline=0)
    windowSubmenu.add_command(label='Supergaussian Window',
        command=self.super_gaussian, underline=0)
    #@+node:tom.20220401200202.1: *3* smoothSubmenu
    smoothSubmenu = Tk.Menu(self.root)
    smoothSubmenu.add_command(label='Cubic Spline Fit',
        command=self.cubicSpline)
    smoothSubmenu.add_command(label='Linear Least Squares Fit',
        command=self.leastsqr)
    smoothSubmenu.add_command(label='Least Square Quadratic Fit',
        command=self.leastsqr_quad)
    smoothSubmenu.add_separator()
    smoothSubmenu.add_command(label='Lowess Linear', command=self.lowess,
                     underline=0)
    smoothSubmenu.add_command(label='Lowess Quadratic', command=self.lowess2Quad,
                     underline=7)
    smoothSubmenu.add_command(label='Lowess Adaptive',
        command=self.lowess_adaptive, underline=7)
    smoothSubmenu.add_command(label='Adaptive LOWESS by Autocorrelation',
        command=self.lowess_adaptive_ac, underline=23)
    smoothSubmenu.add_separator()

    smoothSubmenu.add_command(label='Poisson Smooth', command=self.poissonSmooth,
                    underline=1)
    smoothSubmenu.add_separator()

    smoothSubmenu.add_command(label='Spline Smooth',
        command=self.spline_smooth, underline=0)
    #@+node:tom.20220401200248.1: *3* generateSubmenu
    generateSubmenu = Tk.Menu(self.root)
    generateSubmenu.add_command(label='Exponential',
        command=self.makeExponential, underline=0)
    generateSubmenu.add_command(label='Sine Wave',
        command = self.makeSine, underline=0)
    generateSubmenu.add_command(label='Damped Sine',
        command = self.makeDampedSine, underline=0)
    generateSubmenu.add_separator()

    generateSubmenu.add_command(label='Delta Function', 
        command=self.makeDelta, underline=0)
    generateSubmenu.add_command(label='Step',
        command = self.makeStep, underline=0)
    generateSubmenu.add_command(label='Ramp',
        command = self.makeRamp, underline=3)
    generateSubmenu.add_command(label='Square Wave', 
        command=self.makeSquarewave, underline=2)

    generateSubmenu.add_separator()
    generateSubmenu.add_command(label='Gaussian PDF', 
        command = self.pdfGaussian, underline=0)
    generateSubmenu.add_command(label='Gaussian CDF', 
        command = self.cdfGaussian, underline=10)
    generateSubmenu.add_separator()

    generateSubmenu.add_command(label='Random Noise',
        command=self.makeRandomNoise, underline=0)
    generateSubmenu.add_command(label='Uniform Noise',
        command=self.makeUniformNoise, underline=0)
    generateSubmenu.add_command(label='Gaussian Noise',
        command=self.makeGaussianNoise, underline=0)

    #@+node:tom.20220401200234.1: *3* statsSubmenu
    statsSubmenu = Tk.Menu(self.root)
    statsSubmenu.add_command(label='CDF', command=self.cdf, underline=1)
    statsSubmenu.add_command(label='Fit CDF With Normal', 
        command=self.fitCdfWithNormal, underline=0)
    statsSubmenu.add_command(label='Fit CDF With Normal Adaptive',
        command=self.fitCdfNormalAdaptive, underline=20)
    statsSubmenu.add_command(label='Histogram', command=self.histogram,
        underline=0)
    statsSubmenu.add_separator()
    statsSubmenu.add_command(label='Mean, Std Dev', underline = 0,
        command=self.mean_std)
    statsSubmenu.add_command(label='Correlation Coefficient',
        command=self.correlationCoeff, underline=15)
    statsSubmenu.add_command(label='Spearman Rank Correlation',
        command=lambda x='spearman': self.interpret(x), underline=4)

    statsSubmenu.add_command(label='Sliding Variance',
        command = self.sliding_var)
    #@+node:tom.20220411201602.1: *3* helpSubmenu
    helpSubmenu = Tk.Menu(self.root)
    helpSubmenu.add_command(label='About',
        command=lambda: about(self), underline=0)
    helpSubmenu.add_command(label = "User's Guide",
        command=tutorial, underline = 0)
    helpSubmenu.add_command(label = "GF4 Blog",
        command=blog, underline = 0)

    helpSubmenu.add_command(label='Show Stack',
        command=lambda: stackwin(self), underline=0)
    #@+node:tom.20220401200301.1: *3* mainMenu.add_cascade
    mainMenu.add_cascade(label='File', menu=fileSubmenu)

    mainMenu.add_cascade(label='Plot', menu=plotSubmenu)
    # mainMenu.add_cascade(label='Stack', menu=stackSubmenu, underline=4)
    # mainMenu.add_cascade(label='Curve', menu=curveSubmenu)
    # mainMenu.add_cascade(label='Waveform Math', menu=waveformMathSubmenu,
        # state=Tk.NORMAL)
    # mainMenu.add_cascade(label='Data Processing',
        # menu=dataProcessingSubmenu)
    # mainMenu.add_cascade(label='Fit/Smooth',
        # menu=smoothSubmenu, underline=1)
    # mainMenu.add_cascade(label='Statistics', menu=statsSubmenu,
        # state=Tk.ACTIVE, underline=0)
    # mainMenu.add_cascade(label='Generate', menu=generateSubmenu)
    mainMenu.add_cascade(label='Help', menu = helpSubmenu)
    #@+node:tom.20220401200321.1: *3* Test Menu
    # ========== Test Only ==================================
    testMenu = Tk.Menu(self.root)
    testMenu.add_command(label='Open Aux Window', command=self.openAuxWin)
    testMenu.add_command(label='Overplot Y (lambda)', 
        command=lambda x='overplotbuf': self.interpret(x))
    testMenu.add_command(label='Variance Ratio', command=self.var_ratio)
    #        testMenu.add_command(label='Change Background Color', command=self.set_axis_bg)
    testMenu.add_command(label='Overplot Error Bands', command=self.overplot_errorbands)
    testMenu.add_command(label='Y vs X', command=self.y_vs_y)
    testMenu.add_command(label='Run Macro', command=self.testMacro)
    testMenu.add_command(label='Copy Data To Clipboard', command=self.copy_data_to_clipboard)
    testMenu.add_command(label='Make Sine', command=self.commands['sine'])
    testMenu.add_command(label='Mann-Kendall Trend', command=self.commands['mann_kendall'])

    testMenu.add_separator()

    testMenu.add_command(label='Timehack', command=self.addTimehack)

    #mainMenu.add_cascade(label='Test', menu=testMenu)#, state=Tk.DISABLED)
    #@-others

    return mainMenu
#@-others
#@@language python
#@@tabwidth -4
#@-leo
