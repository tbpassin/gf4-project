#@+leo-ver=5-thin
#@+node:tom.20211211170819.6: * @file buttondefs.py
# pylint: disable = consider-using-f-string
#@@language python
#@@tabwidth -4


#@+others
#@+node:tom.20220829183038.1: ** imports
from import_plugins import import_all_plugins
plugin_modules = import_all_plugins()

#@+node:tom.20211211170819.7: ** Declarations (buttondefs.py)
# encoding: utf-8
'''Button definitions for GF4.  Format:
    (button label, command string, help message)
    
    The command string is sent to the command interpreter when the
    button is pressed.
    '''

SPACER = (None, None)

PLOT_BUTTONS = (
    ('Plot X', 'plot', 'Plot X'),
    ('Plot T', 'plottop', 'Plot Top'),
    SPACER, SPACER,
    ('Overplot X', 'overplot', 'Overplot X'),
    ('Overplot Y', 'overplotbuf', 'Overplot Y'),
    ('Overplot T', 'overplottop', 'Overplot Top'),
    SPACER, SPACER,
    ('Error Bands', 'overploterr', 'Overplot X Error Bands if any'),
    ('Timehack', 'timehack', 'Vertical Marker At Specified X Position'),
)

AXES_BUTTONS = (
    ('Linear', 'linear', 'Linear Plot'),
    ('Semilog Y', 'semilogy', 'Semilog Plot on Y Axis'),
    ('Semilog X', 'semilogx', 'Semilog Plot on X Axis'),
    ('Loglog', 'loglog', 'Log-log Plot'),
)

LOAD_BUTTONS = (
    ('Load From\nDialog', 'loadclip', 'Load/Edit Data From Clipboard'),
    ('Copy To\nClipboard', 'save2clip', 'Save X Data To Clipboard'),
    ('Store 1', 'stox', 'Store X Dataset'),
    ('Recall 1', 'rclx', 'Recall Stored Data Set to X'),
    ('Snapshot', 'take-snapshot', 'Save state of the plot and stack'),
    ('Restore\nSnapshot', 'get-snapshot', 'Restore saved state of the plot and stack'),
)

STACK_BUTTONS = (
    ('Copy2Y', 'copy2buff', 'Copy X to Y'),
    ('Copy2T', 'copy2top', 'Copy To Top from X'),
    ('Swap', 'swap', 'Swap X, Y'),
    SPACER, SPACER,
    ('Y → X', 'copyfrom', 'Copy From Y to X'),
    ('T → X', 'copyfromtop', 'Copy from Top to X'),
    SPACER, SPACER,
    ('Push', 'push', 'Copy X then Push Stack'),
    ('Drop', 'drop', 'Y -> X'),
    ('Rot Up', 'rotateup', 'Rotate Stack Up'),
    ('Rot Down', 'rotatedn', 'Rotate Stack Down')
)

CURVE_BUTTONS = (
    ('Pad/Truncate', 'pad', 'Pad or Truncate x Axis'),
    ('Shift', 'shift', 'Shift x Axis Left or Right'),
    ('Dedup', 'dedup', 'Delete Points With Value Equal To Previous Value'),
    ('Thin', 'thin', 'Thin x Axis (Reduce number of points)'),
    ('Trim', 'trim', 'Delete Points From Left Or Right of Data (negative ==> left)'),
    ('Transpose', 'transpose', 'Transpose x and y axes'),
    ('SortX', 'sortx', 'Sort on x Axis'),
    ('PhaseSpc', 'phase', 'Create Phase Space Plot: y(t+N) vs y(t)'),
    ( 'Y vs X', 'YvsX', 'New data set having y data of Y vs y data of X'),
    SPACER, SPACER,
    ('NumPts', 'numpts', 'Change/Set Number of Points When Generating Waveforms'),
    ('NewX', 'newX', 'Replace x Axis Values')
)

MATH_BUTTONS = (
    ('Y + X', 'addbuf', 'Add X values to Y: X + Y -> X'),
    ('Y - X', 'subbuf', 'Subtract X values from Y: Y - X -> X'),
    ('Y * X', 'mulbuf', 'Multiply X Values by Y: X*Y -> X'),
    ('Y / X', 'divbuf', 'Divide X Values Into Y: Y / X -> X'),
    SPACER, SPACER,
    ('Diff', 'diff', 'Differentiate X using one-sided differencing'),
    ('Central Diff', 'diff2', 'Differentiate X using central differencing'),
    ('Integrate', 'int', 'Integrate X'),
    SPACER, SPACER,
    ('Add Const', 'addcnst', 'Add Constant To Each Value'),
    ('Invert', 'invert', 'Invert Y values'),
    ('Scale', 'scale', 'Scale: Multipy Each Value by a Constant'),
    ('Log 10', 'log', 'Replace values with their Logs Base 10'),
    ('Ln', 'ln',  'Replace values with their Natural Logs'),
    ('Square', 'sqr', 'Square Values'),
    SPACER, SPACER,
    ('Full Rectify', 'rectify', 'Full-wave Rectify Values'),
    ('Half Rectify', 'halfrect', 'Half-wave Rectify Values'),
    ('Clip', 'clip', 'Clip Values'),
    ('Normalize', 'normalize', 'Normalize curve values to 1.0'),
    ('Zero', 'zero_data', 'Center curve by subtracting its mean'),
)

CURVE_FIT_BUTTONS = (
    ('Cubic Spline\nInterpolation', 'cubicspln', 'Interpolate Between Points with Cubic Spline'),
    # ('Lst Sqr Lin', 'lstsqrlin', 'Fit Points with Linear Least Squares (2 s.e. error bands)'),
    ('Lst Sqr Poly', 'lstsqrpoly', 'Fit Points with N-degree Polynomial Using Least Squares (2 s.e. error bands)'),
    ('Thiel-Sen', 'thiel_sen', 'Fit Line Robustly Using Thiel-Sen Method (median slopes)'),
    ('Piecewise', 'piecewise', 'Piecewise Linear Least Squares Fit'),
)

SMOOTHER_FIT_BUTTONS = (
    ('LOWESS Lin', 'lowess', 'Smooth Data with Linear LOWESS Fit (2 s.e. error bands)'),
    #('LOWESS Poly', 'lowess_poly', 'Smooth Data with nth Order LOWESS Fit'),
    ('LOWESS Adapt', 'lowessadapt', 'Smooth Data Adaptively with LOWESS: Find best span for a specified smoothness (2 s.e. error bands)'),
    ('LOW Correl', 'lowesscorrel', 
        'Minimize Lag-1 Autocorrelation of Residuals: remove highest frequencies (2 s.e. error bands)'),
    SPACER, SPACER,
    ('Poisson', 'poisson', 'Smooth Data Using Poisson Smooth: Assumes Data Are Poisson-distributed Counts'),
    SPACER, SPACER,
    ('Splin Smooth', 'splinesmooth', 'Smooth Data With Splines')
)

DATA_PROCESSING_BUTTONS = (
    ('FFT', 'fft', 'Calculate FFT of Data.  Data length need not be a power of 2'),
    ('Convolve', 'convolve', 'Convolve X Data with Y.  Y is unchanged'),
    ('Correl', 'correl', 'Correlate X Data with Y.  Y is unchanged'),
    ('Autocorr', 'autocor', 'Autocorrelation of X Data'),
    ('Low Pass', 'lopass', 'Low Pass Filter of X Data.  Time Constant is fraction of x axis'),
    ('Hi Pass', 'hipass','High Pass Filter of X Data.  Time Constant is fraction of x axis'),
    ('Moving Median', 'move-median', 'Moving Median of X Data'),
    )

WINDOW_BUTTONS = (
    ('Half Cosine', 'halfcoswin', 'Window Data With Half-Cosine Window'),
    ('Cosine', 'coswin', 'Window Data With Full Cosine Window'),
    ('Gaussian', 'gaussianwin', 'Window data with Gaussian'),
    ('Supergaussian', 'supergausswin', 'Window data with 6th order supergaussian'),
    ('Half SuperGauss', 'halfsupergwin', 'Window Data With 6th Order Supergaussian Window'),
)

STATS_BUTTONS = (
    ('CDF', 'cdf', 'Calculate CDF of [X] data'),
    ('Normal CDF', 'fitcdf', 'Fit a Normal CDF to [X] Data'),
    #('CDF Adapt', 'fitcdfadapt', 'Fit a CDF in [X] with a Normal CDF, Adaptively'),
    ('Histogram', 'hist', 'Calculate Histogram of [X] Data'),
    SPACER, SPACER,
    ('Mean, STD', 'meanstd', 'Display Mean, Sample Standard Deviation Corrected For Autocorrelation, Lag-1 autocorrelation, and Area of X Data'),
    # ('Corr Coeff', 'corrcoeff', "Calculate Correlation Coefficient Between X and Y"),
    ('Spearman', 'spearman', 'Calculate the Spearman Rank Correlation Coefficient between X and Y'),
    ('Pearson', 'pearson', "Calculate the Pearson's Correlation Coefficient r between X and Y"),
    SPACER, SPACER,
    ('Partial Autocorr', 'partial-autocorr',
               'Partial autocorrelation of the X dataset (assumes stationary data)'))

GENERATOR_BUTTONS = (
    ('Sine', 'sine', 'Generate Sine Wave.  Period is in multiples of x-axis length'),
    ('Damp Sin', 'dsin', 'Generate Damped Sine Wave.  Period is in multiples of x-axis length'),
    ('Expon', 'expon', 'Generate Decaying Exponential.  Time constant is in multiples of x-axis length'),
    ('Delta', 'delta', 'Generate Delta Function'),
    ('Step', 'step', 'Generate Rectangular Step'),
    ('Ramp', 'ramp', 'Generate Linear Ramp'),
    ('Square\nWave', 'sqw', 'Generate Square Wave'),
    ('Gaussian\nPDF', 'pdfgaus', 'Generate Gaussian PDF'),
    ('Gaussian\nCDF', 'cdfgaus', 'Generate Gaussian CDF'),
    ('Uniform\nNoise', 'uninoise', 'Generate Uniform Noise'),
    ('Gaussian\nNoise', 'gausnoise', 'Generate Gaussian Noise')
)

TREND_BUTTONS = (
    ('Mann-Kendall', 'mann_kendall', 'Compute Mann-Kendall Trend'),
    ('Windowed Dev', 'sliding_var', 'Standard Deviations for a LOWESS Fit'),
)
#@+node:tom.20220829181647.1: ** Plugins
PLUGIN_BUTTONS = []
for m in plugin_modules:
    # If we are overriding an existing command, don't create a plugin button
    newbtn = getattr(m, 'BUTTON_DEF', '')
    if not newbtn:
        print(f'==== Warning: {m.__name__} is missing its BUTTON_DEF')
        continue

    if getattr(m, 'OVERRIDE', False):
        # If plugin wants its button added to an existing group
        OWNER_GROUP = getattr(m, 'OWNER_GROUP', '')
        if OWNER_GROUP:
            exec(f'{OWNER_GROUP} = list({OWNER_GROUP});{OWNER_GROUP}.append({newbtn})')
        else:
            print(f'{m.__name__} is missing optional OWNER_GROUP')
            PLUGIN_BUTTONS.append(newbtn)
    else:
        PLUGIN_BUTTONS.append(newbtn)

#@-others
if __name__ == '__main__':
    for m in plugin_modules:
        print(getattr(m, 'BUTTON_DEF'))
#@-leo
