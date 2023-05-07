<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: https://leo-editor.github.io/leo-editor/leo_toc.html -->
<leo_file xmlns:leo="http://leo-editor.github.io/leo-editor/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="tom.20220507132007.1"><vh>Docs</vh>
<v t="tom.20220507132007.2"><vh>@clean README.md</vh>
<v t="tom.20220507132007.3"><vh>gf4-project</vh>
<v t="tom.20220816202839.1"><vh>Installing</vh>
<v t="tom.20220816202850.1"><vh>Linux Issues</vh></v>
</v>
<v t="tom.20220816202934.1"><vh>Running GF4</vh></v>
</v>
</v>
<v t="tom.20220509230416.1"><vh>@clean DEVELOPERS_READ_THIS.md</vh>
<v t="tom.20220509230545.1"><vh>Leo-Editor, Or Those Strange Comment Lines</vh></v>
</v>
<v t="tom.20220820141745.1"><vh>@clean requirements.txt</vh></v>
<v t="tom.20220901223400.1"><vh>@clean recent_changes.md</vh></v>
<v t="tom.20220507132007.5"><vh>@button Build HTML</vh></v>
<v t="tom.20220507132007.4"><vh>@path sphinx</vh>
<v t="tom.20220507180306.1"><vh>GF4 User's Guide</vh>
<v t="tom.20220507132007.6"><vh>@rst GF4_Users_Guide</vh></v>
<v t="tom.20220507175416.1"><vh>@rst whatis</vh>
<v t="tom.20220507132007.7"><vh>What Is GF4?</vh>
<v t="tom.20220507132007.8"><vh>Typical Screen Shot</vh></v>
<v t="tom.20220507132007.9"><vh>A Historical Note</vh></v>
<v t="tom.20220507132007.10"><vh>Some Typical Uses</vh></v>
<v t="tom.20220507132007.11"><vh>What GF4 Is Not</vh></v>
</v>
</v>
<v t="tom.20220507175950.1"><vh>@rst quickstart</vh>
<v t="tom.20220507132007.12"><vh>Quick Start</vh>
<v t="tom.20220507132007.13"><vh>The "Noisy Ramp" Example</vh>
<v t="tom.20220507132007.14"><vh>Create And Plot The Noisy Line</vh></v>
<v t="tom.20220507132007.15"><vh>Fit and Plot The Noisy Line</vh></v>
</v>
<v t="tom.20220507132007.16"><vh>Encouraging Remarks</vh></v>
</v>
</v>
<v t="tom.20220820134816.1"><vh>@rst philosophy</vh></v>
<v t="tom.20220507180611.1"><vh>@rst basics</vh>
<v t="tom.20220507132007.17"><vh>Data Format</vh>
<v t="tom.20220821142158.1"><vh>Invalid or Missing Data</vh></v>
<v t="tom.20220821142224.1"><vh>Editing and Censoring of Data Points</vh></v>
</v>
<v t="tom.20220507132007.18"><vh>The Waveform Stack</vh>
<v t="tom.20220507135125.1"><vh>Stack Operations</vh></v>
<v t="tom.20220507140739.1"><vh>Direct Access</vh></v>
</v>
<v t="tom.20220507143340.1"><vh>Non-Stack Storage</vh></v>
<v t="tom.20220507132007.22"><vh>Loading And Saving Data</vh></v>
<v t="tom.20220820114259.1"><vh>Saving Graphs</vh></v>
<v t="tom.20220507132007.19"><vh>Plotting Curves</vh>
<v t="tom.20220821142540.1"><vh>Default Plotting Settings</vh></v>
<v t="tom.20220507132007.20"><vh>Changing Colors, Symbols, and Line Styles</vh></v>
</v>
<v t="tom.20221108033233.1"><vh>Help For Commands</vh></v>
</v>
<v t="tom.20220507185750.1"><vh>@rst waveforms</vh>
<v t="tom.20220507190615.1"><vh>Generating And Operating on Waveforms</vh>
<v t="tom.20220507132007.25"><vh>The Waveform Generators</vh>
<v t="tom.20220820182510.1"><vh>Meaning of Parameters For Some Waveforms</vh></v>
</v>
<v t="tom.20220507132007.23"><vh>Operations On One Waveform</vh></v>
<v t="tom.20220507132007.24"><vh>Operations On Two Waveforms</vh></v>
</v>
</v>
<v t="tom.20220507190251.1"><vh>@rst curvefitting</vh>
<v t="tom.20220507191549.1"><vh>Curve Fitting and Smoothing</vh>
<v t="tom.20220507132007.26"><vh>Curve Fitting</vh></v>
<v t="tom.20220507132007.27"><vh>Curve Smoothing</vh></v>
</v>
</v>
<v t="tom.20220507191015.1"><vh>@rst windowing</vh>
<v t="tom.20220507132007.28"><vh>Windowing and FFTs</vh></v>
</v>
<v t="tom.20220507191131.1"><vh>@rst macros</vh>
<v t="tom.20220507132007.29"><vh>Using Macros</vh></v>
</v>
<v t="tom.20220902112346.1"><vh>@rst plugins</vh>
<v t="tom.20220902120822.1"><vh>The Plugin System</vh>
<v t="tom.20220902114333.1"><vh>Defining a Command Button</vh></v>
<v t="tom.20220902114404.1"><vh>The Implementing Function</vh></v>
<v t="tom.20220902115843.1"><vh>Over-riding An Existing Command</vh></v>
<v t="tom.20220904145245.1"><vh>Adding a Button To an Existing Group</vh></v>
<v t="tom.20220902121203.1"><vh>Controlling Which Plugins Get Loaded</vh></v>
</v>
</v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="tom.20220507132007.1"></t>
<t tx="tom.20220507132007.10">Typical uses of GF4 include curve fitting and observing the fit quality, comparing observed cdf curves against a Gaussian of the same mean and standard distribution, smoothing noisy time series data, and creating FFT transforms to try to identify prominent frequencies in a waveform.

GF4 would make an excellent educational tool since it makes exploring the data so easy, which would help the student come to understand basic statistical limitations that are hard to convey otherwise.

The effect of zero-padding and windowing a waveform before running an FFT is quite illuminating and easy to study.  Cumulative data, such as total covid case counts vs time, can be converted into daily rates by differentiating.  This leads to a very noisy dataset, and that can be smoothed with, for example, a LOWESS smoothing routine. The study of the shape of residuals after fitting a function is interesting and easy to do.

No code need be written to perform any of these operations on datasets.</t>
<t tx="tom.20220507132007.11">GF4 is not a rigorous tool for statistical calculations.  Although the mathematical operations are done as carefully as possible, usually using well-established scientific libraries such as numpy and scipy, various subtleties are not taken into account.  For example, error bars can be shown for a LOWESS smooth, but they do not take into account possible autocorrelation in the dataset.  FFTs, and correlations and convolutions between waveforms, may not normalized according to usual conventions.  This generally makes no practical difference to exploratory use, since it is the relative shapes and features that are normally of interest.  In addition, although processed data sets can be saved to files, and image files of the curves seen on the screen can be saved as well, error bars, regression coefficients, and the like cannot be output.

GF4 is best used for understanding the features of a 2D dataset, and working out how effective various kinds of processing will be.  Is it too noisy or too contaminated to get useful results? Does a linear least squares fit make sense? Does this kind of a correlation seem to be meaningful? Is a smoothing window of 50 too wide?  Will a cosine or a supergaussian window produce a cleaner FFT for this particular data?  Will zero-padding the dataset improve the resolution?  Is this increase really "exponential"?  What will be the effect of a D.C offset on the FFT?

If more than this is needed, the user should take that understanding and use it with other tools to produce a more complete analysis in depth.  The "R" language might be one suitable tool, for example.  After that is done, GF4 can again be used to assess the results as a kind of quality check.</t>
<t tx="tom.20220507132007.12">For a quick introduction, we will work through an example. GF4 will generate the data for us. The file to launch is named gf4.pyw.  It can be launched with pythonw as a GUI application with no console, or with python to also have a console.  The console is not needed except it could display error messages, which are unlikely.  GF4 should be run with some version of python 3.6+.

To launch the program, you can double-click on its icon in the Windows Explorer file manager or the Linux equivalent, or run with python from the directory that contains gf4::

    python3 gf4.pyw

or, for systems with the "py" launcher, either of::

    pyw gf4.pyw
    py gf4.pyw

With a data file name also on the command line, GF4 will open and plot that file on launch.</t>
<t tx="tom.20220507132007.13">In this example, we will create a dataset that consists of a straight line with
Gaussian noise added. We will fit a line to the noisy data. Then we will display
the fitted line, and overlay the noisy data, the original line, and the error
bars for the fit.

It will be helpful to open the stack viewer window before starting.  This will
make it easier to grasp how the stack works and what data set is in which stack
position.  Open the stack viewer from the Help menu.
</t>
<t tx="tom.20220507132007.14">**Create a Straight Line**
~~~~~~~~~~~~~~~~~~~~~~~~~~~
To generate the line, click the "Ramp" button. The line will be plotted in the left hand plotting window. this line has been placed in the bottom position of the stack, which is always called "**X**". Copy it to the "**Y**" position (the next one up in the stack) by clicking on the "Copy2Y" button in the "Stack" group.

**Create a Noise Dataset**
~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the original line safely stored in **Y**, now create a dataset of noise.  Click on the "Gaussian Noise" button.  In the dialog box that pops up, change the "Sigma" value to 0.3. If we leave it at the default value of 1.0, there will be too much noise.  Even with the smaller value of sigma, there will be a lot of noise.  Accept the values by clicking the OK button or pressing the &lt;ENTER&gt; key.  The noise waveform will display in the plot window.

**Add The Noise To the Original Line**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next we will add the noise to the straight line we saved in **Y**.  In the "Math" column, click on "X + Y".  This will add the two curves together point-by-point and leave the result in the **X** stack position.  The original straight line is unchanged in **Y**.

The sum of the two datasets is a noisy line in **X**, and it has been automatically plotted in the plot window.  In one last touch, click on the "Overplot Y" button in the "Plot" column.  This will overlay the original straight line which is still in **Y**. The result is shown in Figure EX-1a.  Your result may be a little different because you will have gotten a different noise dataset.

.. figure:: images/gf4_example_1_noisy.png

    Figure EX-1a. The Noisy Ramp With Original (Clean) Curve Overlaid.

**Plot the Noisy Data With Point Symbols Instead Of Lines**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Gaussian noise data points don't really form a curve because they are independent.  Perhaps it would be better to plot the noisy ramp with points instead of lines.  Try this out by using the "Plot" menu on the left-hand plot window. Select Plot/Main Marker Style/Symbol.  Then click on the "Plot" item in the "Plot" Menu or the "Plot X" button in the commands window.  Then overplot the original ramp in **Y** using the "Overplot Y" button.

The results will resemble Figure EX-1b.

.. Figure:: images/gf4_example_1_noisy_symbols.png

    Figure EX-1b. The Noisy Ramp Plotted With Symbols Instead Of Lines.

Finally, set the main marker style back to "Line"

**Save The Noisy Line For Later Viewing**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this example, at the end we will overlay this noisy line on the plot of the fitted line.  Copy it to the **T** stack position by clicking the "Copy2T" button in the "Stack" group (see `Direct Access &lt;basics.html#direct-access&gt;`_).
</t>
<t tx="tom.20220507132007.15">To fit a linear least squares fit to the noisy ramp, click on the "Lst Sqr Lin" button in the upper right of the commands window.  The best fit straight line will plot in the plotting window.

**Overplot The Other Datasets For Comparison**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For this example we will overplot the original ramp and the noisy version of the ramp.  These datasets are still in **Y** and **T** where we put them.

Click on the "Overplot Y" button in the "Plot" group at the left of the command window. The original straight line will be plotted in a light cyan color.  It will probably be a little different from the fitted line.  That is normal, because the noisy sample we used is unlikely to have exactly the same properties as the original.

Click on the "Overplot T" button to overplot the noisy dataset.

**Overlay Error Bands For The Fit**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Error bands for the fit are available for most of the fitting routines.  Click the "Error Bands" button to see them.  Each time this button is clicked, the error band area gets less transparent, so you can adjust the visibility if needed.

The results are shown in Figure EX-1c.

.. figure:: images/gf4_example_1_fitted.png

    Figure EX-1c. The Least Squares Fitted Line With Error Bands And Original Data.

</t>
<t tx="tom.20220507132007.16">Examples like this are usually much harder to describe than to do.  With a little practice, these kinds of operations become familiar and they go very quickly.  One gets used to the location of the command buttons that are commonly used, and the stack positions stop feeling strange.  Just like a physical calculator, in fact.</t>
<t tx="tom.20220507132007.17">GF4 accepts text files with whitespace-separated columns, one data point per
row. It also accepts comma-separated columns (CSV files); these are converted 
internally to TAB-separated columns.  If the input file is a CSV file, GF4
tries to identify the column headers by looking at the row just before the first
data row.

If there is only one column, GF4 inserts an imputed first column with
values being consecutive integers beginning with 1. The "first" column becomes
the "x", or horizontal, axis. If there are more than two columns, a dialog is
displayed so the user can choose the two desired columns. The number of columns
is derived based on the first non-comment, non-blank line whose first field is a
legal floating point number.

Data fields must be numeric.  GF4 cannot make use of non-numeric data.  Data
fields are converted to floating point numbers.  Date fields are not understood nor displayed.  Date columns should be converted to serial numbers, such as months or years, beginning with the beginning epoch.  The conversion should be done outside of GF4.  Alternatively, a leading data column could be deleted.  Once GF4 has loaded the data, its horizontal axis can be changed to reflect the starting point and increment by  using the *NewX* command button.

Here is an example data file::

    # A comment line
    ; Another comment line.  Also, blank lines are ignored.
    # x  y
    1  1
    2  4
    3  9
    # etc 

Data points do not need to be equally spaced on the x axis.

There are specially formatted (optional) comments to specify a title, axis labels, and a break between data sets::

    ;; FIGURELABEL: The Title
    ;; XLABEL: The x axis label
    ;; YLABEL: the y axis label
    1    3.0
    2    4.0
    3    6.0
    4    7.0
    ;; ENDDATASET

The special comment key words are case sensitive.  If there is more than one dataset, the second one goes into the **Y** position in the stack, and so on up to the stack depth.  Beyond that additional data sets are ignored.

</t>
<t tx="tom.20220507132007.18">The waveform stack is the primary organizing concept of GF4.  Modeled after
the stack in Hewlett-Packard RPN calculators, the stack is an array with positions
that can hold data elements.  Conceptually, the stack is arranged as a vertical 
column with a "bottom" and a "top".  Items on the stack can be "pushed" upwards,
"dropped" downwards, "rotated" and "swapped". These operations are illustrated
in the next section.

All operations that change data operate on the data in the stack bottom (the **X** position). All operations between two datasets, such as addition and correlation, use the **X** and **Y** positions (**Y** is the next position up from **X** [1]_). the result of these operations only change data in the **X** position. The data in **Y** remains unchanged.

The state of the stack can be viewed by using the *Help/ Show Stack* menu item in the main window.  This opens a small window that shows the name of the dataset 
currently in each stack position. It is helpful to keep this window open while
one gains experience with GF4.  The image below depicts the stack viewer window:

.. image:: images/stack_viewer_window.png
    :scale: 50

The most common stack operations in practice are "Swap" and direct access.  The
**T** position is often used as a temporary data cache.

.. [1] For historical reasons, the **Y** stack position is also called the *Buffer* and the **X** position is also called *Main*.</t>
<t tx="tom.20220507132007.19">Plotting commands are grouped together in the Command Window:

.. figure:: images/plot_cmd_buttons.png

    Figure BA-1. Plotting Buttons in the Command Window.

These same commands are also available in the *Plot* menu in the main GF4
window.  This menu is also the only place where the graph properties can be
changed.  These properties include line width and color, whether to use symbols
instead of lines and if so, which symbol shape to use.

Data in any of the three stack positions **X**, **Y**, and **T** can be overplotted;
Only **X** and **T** can be plotted. These terms mean the following:

- Plot -- create a new graph at displays the specified data set;

- Overplot -- plot a dataset on top of an existing graph.  The axes may rescale if the new data would overflow the previous bounds of the graph.

Overplotting is essential to getting the most out of GF4, since it provides a way 
to compare several data sets, or several ways of processing the same data.

</t>
<t tx="tom.20220507132007.2">@language md
@tabwidth -4
@others

</t>
<t tx="tom.20220507132007.20">Curve plotting options can be changed for plotting/overplotting data in the
**X** and **Y** stack positions. The line and color styles of the *T** position
cannot be changed. In practice, this is rarely a problem. Technically there
would be no problem in providing for changes in the **T** appearance, but up
until now it has seemed not to be worth the extra complexity for the user.
Changing these properties using menus is a little tedious, but adding buttons to
the command window would be bad for its readability and usability.

Figure BA-2 depicts the Plot menu items that can change the appearance of
**X** and **Y** data:

.. figure:: images/line_style_options.png

    Figure BA-2. Plot Menu Items For Changing Plotting Options.

These menu items are reasonably self-explanatory.  For example, Figure BA-3 shows
one of the menus expanded:

.. figure:: images/selecting_marker_style.png

    Figure BA-3.  Selecting the "Buffer" (**Y**) Plotting Style [2]_.

.. [2] As mentioned in :ref:`The Waveform Stack`, the **Y** position is also called the *Buffer*, and the **X** position may be called *Main*.</t>
<t tx="tom.20220507132007.22">All data is saved from and loaded to the **X** stack position. This will overwrite
the previous contents.  If you want to keep the previous data set, push or copy 
it to one of the other positions.  Most often, the **Y** position is used for this.

The data format is described in :ref:`Data Format`.  Data is saved in TAB-separated
format (even if it was originally in CSV format) and includes the special comments 
that will recreate the title and axis labels.  Error bars are not saved.

Data can be saved to a file (using the *File/Save* menu item) or copied to the
system clipboard (using the *Copy To Clipboard* button).  A data file can be read
using the *File/Open* menu item.  Data, including CSV-format
data, can also be loaded into the X position from the system clipboard using the
*Load From Dialog* button.  Note that this dialog's entry panel is a basic text editor,
so the data from the clipboard can be edited before it is processed.
</t>
<t tx="tom.20220507132007.23">All operations on one waveform operate on the **X** (or *Main*) dataset.
No other datasets are modified. The new or modified dataset is plotted. Some
examples, among many others, are

    - Add Const
    - Differentiate
    - Full Rectify
    - Ln (the natural logarithm)
    - Log 10 (logarithm base 10)
    - LOWESS Lin
    - Scale
    - Transpose
    - Truncate

The *Mean, STD* button does not change the dataset.  Instead, it displays some
basic statistic values in a message band below the main plotting pane.  The
message reports the data maximum, mean, standard deviation, standard error,
area, lag-one correlation coefficient [1]_, and number of data points.  The values can be
highlighted with the mouse and copied to the clipboard with &lt;CTRL-C&gt;

Here is a typical message::

    Max: 0.500 at x=4.000  Mean: -0.0319  Span: 0.999  Std Dev: 0.2802  SE: 0.0175  area: -8.48e+00  rho: 0.047  N = 256

.. [1] Gives an indication of short-range correlation in the data.</t>
<t tx="tom.20220507132007.24">Operations on two waveforms operate on the **X** and **Y** datasets. The results
replace the **X** dataset. No other datasets are modified. The result dataset is
plotted. Currently the two-dataset operations are

    - Convolve (form the convolution of **X** and **Y**)
    - Correl (correlate **X** and **Y**)
    - Y + X (pointwise sum)
    - Y - X (pointwise difference)
    - Y * X (pointwise product)
    - Y / X (pointwise division)

Note that the four pointwise arithmetical operations require that both datasets
have the same number of points.  Pointwise division cannot succeed if any of the
divisor's points has a zero value: the operation is canceled, an error messsage
is shown, and the original contents of **X** are unchanged.

There are three other operations between **X** and **Y** datasets that do not
change the **X** dataset, because they result in a plain number -

    - Pearson (Pearson's Correlation Coefficient)
    - Spearman (Spearman Rank Correlation Coefficient)

These display their results in a message bar below the plotting pane.
The values can be highlighted with the mouse and copied to the clipboard with
*&lt;CTRL-C&gt;*.
</t>
<t tx="tom.20220507132007.25">We encountered two of GF4's waveform generators in the `Quick Start &lt;quickstart.html&gt;`_ section.
There we used the ramp and Gaussian noise generators.  Figure WA-1 depicts the
generator command buttons:

.. figure:: images/generator_buttons.png

    Figure WA-1. Waveform Generators.

The generated waveforms will contain a number of equally-spaced data points.  The
default number is 256. There is no provision for setting the x-axis scale: it can 
be changed afterwards using the *NewX* button. The number of points in a generated
waveform can be set using the *NumPts* button.  There is no specific limit to
the number of points, but if it is too large, some operations on the dataset
might take a long time.
</t>
<t tx="tom.20220507132007.26"></t>
<t tx="tom.20220507132007.27"></t>
<t tx="tom.20220507132007.28"></t>
<t tx="tom.20220507132007.29"></t>
<t tx="tom.20220507132007.3">GF4 - "GF" being short for "Graphics Framework" - is a Python program to display
two-dimensional data, such as time series data, and to perform mathematical
operations on the data or between two related data sets. The program aims to
make data exploration easy and enjoyable.

The program's interface is modeled after hand-held calculators of the "reverse
polish notation" (RPN) style. This kind of calculator was made famous by
Hewlett-Packard, starting with their HP-35 and HP-45 calculators. GF4 works with
waveforms in place of the numbers manipulated by the hand calculators.

We sometimes call the 2D data sets "waveforms" because the data often represents
time domain waveforms. Otherwise we generally call the data by the term
"datasets".

Thus, a waveform can be scaled, squared, have its logarithm taken, integrated
and differentiated, be normalized and rectified, and so on. A discrete Fast
Fourier Transform is provided that is not limited to powers of two in data
length. Data can be trimmed or padded. Curve fitting and smoothing of several
varieties can be done. Two waveforms can be added, subtracted, multiplied, and
divided (where possible), correlated or convolved together, among others. A
smoothed waveform can be overplotted on the unsmoothed original. Linear,
semilog, and log-log plots are available.

A certain number of basic waveforms can be generated, including a delta
function, step, ramp, sine and damped sine, Gaussian PDF and CDF distributions,
and more. Altogether there are nearly 80 different operations available.

A basic macro facility is provided to automate a sequence of repeated
operations.

Like RPN calculators, GF4 operations are organized around a stack of data sets.
Unlike those calculators, the various stack levels can be accessed directly as
well.

The current version of the program is somewhat uneven in the degree of polish of
the various operations. This reflects its evolution under the interests and
changing needs of the author. Mathematically, many operations are implemented by
numpy or scipy computations; others are algorithms implemented by the author.

You can read the [User's Guide](http://tompassin.net/gf4/docs/GF4_Users_Guide.html).
There is a [blog](http://tompassin.net/gf4/blogsite/).

Here is a screenshot: ![Screenshot](gf4/doc/images/GF4_Screen_Example.png)

How To Get GF4
===============
1. Clone this Github repository; or

2. Select a branch, such as `Master`.  Download a zip file from this Github page:
Press the `Code` button on this page, then select `Download Zip`.  When the file
has downloaded, unzip it to some convenient location.

</t>
<t tx="tom.20220507132007.4"></t>
<t tx="tom.20220507132007.5">@language python
from sys import executable
import subprocess

c.k.simulateCommand('rst3')

# Other likely themes: 
#'-D', 'html_theme=sphinx_book_theme',
#'-D', 'html_theme=bizstyle',

cmd = [executable, '-m', 'sphinx', '-C',
        '-b', 'html',
        '-D', "master_doc=GF4_Users_Guide",
        '-D', 'source_suffix=.rst',
        '-D', 'html_theme=pyramid',
        '-D', 'project=GF4',
        '-D', 'extensions=sphinx.ext.autosectionlabel',
        '-D', 'copyright=Thomas B. Passin 2022',
        '-D', "html_theme_options.sidebarwidth=20em",

        # sourcedir, outputdir:
        r'.', r'..\docs']

subprocess.call(cmd)</t>
<t tx="tom.20220507132007.6">:tocdepth: 3

===================
GF4 User's Guide
===================

This User's Guide Covers the Use and Capabilities of the GF4 Waveform Calculator.

Table of Contents
==================

.. toctree::
    :maxdepth: 2
    :glob:

    whatis
    quickstart
    philosophy
    basics
    waveforms
    curvefitting
    windowing
    macros
    plugins

 </t>
<t tx="tom.20220507132007.7">GF4 - "GF" being short for "Graphics Framework" - is a program to display
two-dimensional data, such as time series data, and to perform mathematical
operations on the data or between two related data sets. We will often call the
2D data sets "waveforms" for historical reasons, and because the data often
represents time domain waveforms. Otherwise we generally call the data by the
term "datasets". The program aims to make data exploration easy and enjoyable.

The program's interface is modeled after hand-held calculators of the "reverse
polish notation" (RPN) style. This kind of calculator was made famous by
Hewlett-Packard, starting with their HP-35 and HP-45 calculators. GF4 works with
waveforms in place of the numbers manipulated by the hand calculators.

Thus, a waveform can be scaled, squared, have its logarithm taken, integrated
and differentiated [1]_, be normalized and rectified, and so on. A discrete Fast
Fourier Transform is provided that is not limited to powers of two in data
length. Data can be trimmed or padded. Curve fitting and smoothing of several
varieties can be done. Two waveforms can be added, subtracted, multiplied, and
divided (where possible), correlated or convolved together, among others.

A certain number of basic waveforms can be generated, including a delta
function, step, ramp, sine and damped sine, Gaussian PDF and CDF distributions,
and more. Altogether there are nearly 80 different operations available.

A basic macro facility is provided to automate a sequence of repeated
operations.

Like RPN calculators, GF4 operations are organized around a stack of data sets.
Unlike those calculators, the various stack levels can be accessed directly as
well.

GF4 is written in Python 3, and makes use of MatPlotLib, NumPy, Scipy, and
some other standard libraries.

.. [1] That is, the discrete differencing equivalent of these operations.
</t>
<t tx="tom.20220507132007.8">Figure IN-1 depicts a fairly typical view of GF4 in action.  The ramp curve generator has produced a straight line, which was copied to the second stack position.  Then a Gaussian noise series was generated and added to the straight line to produce a very noisy ramp.  The underlying straight line, which still was available in its stack position, was then overlayed onto the noisy version.

Of note is the title of the graph.  It was generated automatically, capturing a description of each processing step as a reminder for the user.  This is one of many "affordances" the program provides to reduce demands on the user.  The title can be changed by clicking on it, which turns the title line into an edit box.

.. figure:: images/GF4_Screen_Example.png

    Figure IN-1. Screen Shot Of GF4 In Action.

    The main plotting window is on the left, and the command window is on the right. An optional window that shows the state of the waveform stack is at the upper right.
</t>
<t tx="tom.20220507132007.9">GF4 is a fifth generation implementation of the basic waveform calculator concept (the first generation - implemented on a 64K Z-80 CP/M machine - was not named).  The implementation language has changed from FORTH to Turbo Pascal to Delphi to the current Python.  Over this time the basic concept has not been changed, while the user interface has evolved, and more math operations added.</t>
<t tx="tom.20220507135125.1">
The stack can be "pushed", causing the existing
elements to be moved one slot "higher"::

    Stack populated with data elements A, B, and C

    |   A   |   &lt;-- "T": stack top
    |   B   |   &lt;-- "Y"
    |   C   |   &lt;-- "X": stack bottom

    "Pushing" stack duplicates "X" element (top element is lost)

    |   B   |   &lt;-- "T": stack top
    |   C   |   &lt;-- "Y"
    |   C   |   &lt;-- "X": stack bottom


"Dropping" the stack moves elements one slot lower::

    Stack populated with data elements A, B, and C

    |   A   |   &lt;-- "T": stack top
    |   B   |   &lt;-- "Y"
    |   C   |   &lt;-- "X": stack bottom

    "Dropping" stack duplicates "T" element (bottom element is lost)

    |   A   |   &lt;-- "T": stack top
    |   A   |   &lt;-- "Y"
    |   B   |   &lt;-- "X": stack bottom

The stack can also be cyclically rotated up or down::

    Stack populated with data elements A, B, and C

    |   A   |   &lt;-- "T": stack top
    |   B   |   &lt;-- "Y"
    |   C   |   &lt;-- "X": stack bottom

    Rotated "up" (T -&gt; X, X -&gt; Y, Y -&gt; T)

    |   B   |   &lt;-- "T": stack top
    |   C   |   &lt;-- "Y"
    |   A   |   &lt;-- "X": stack bottom

    Stack populated with data elements A, B, and C

    |   A   |   &lt;-- "T": stack top
    |   B   |   &lt;-- "Y"
    |   C   |   &lt;-- "X": stack bottom

    Rotated "down" (T -&gt; Y, Y -&gt; X, X -&gt; T)

    |   C   |   &lt;-- "T": stack top
    |   A   |   &lt;-- "Y"
    |   B   |   &lt;-- "X": stack bottom

"Swap" exchanges the X and Y data elements::

    Stack populated with data elements A, B, and C

    |   A   |   &lt;-- "T": stack top
    |   B   |   &lt;-- "Y"
    |   C   |   &lt;-- "X": stack bottom

    Stack after a "Swap"

    |   A   |   &lt;-- "T": stack top
    |   C   |   &lt;-- "Y"
    |   B   |   &lt;-- "X": stack bottom
</t>
<t tx="tom.20220507140739.1">The data element in **X**, the stack bottom, can be copied to the **Y** and **T** positions.
The **Y** and **T** data elements can be copied to the **X** position.  All the stack
operations are carried out by clicking buttons in the auxiliary command window.

.. image:: images/stack_ops.png</t>
<t tx="tom.20220507143340.1">In addition to the stack, there are several other data storage locations:

1. A single slot accessed by the *Store 1** and *Recall 1* buttons.
These store from and retrieve to the **X** position.

2. The system clipboard, accessed by the *Copy To Clipboard* and *Load From Dialog*
buttons. The latter opens an editing window into which the clipboard can be
copied.

These buttons are marked in the image below:

.. image:: images/loadsave.png
</t>
<t tx="tom.20220507175416.1"> </t>
<t tx="tom.20220507175950.1">:tocdepth: 2
</t>
<t tx="tom.20220507180306.1">@nocolor
</t>
<t tx="tom.20220507180611.1"></t>
<t tx="tom.20220507185750.1"></t>
<t tx="tom.20220507190251.1">
</t>
<t tx="tom.20220507190615.1">Operations on waveforms operate in a pointwise manner. For the most part, the
actual values of the x-axis (horizontal) are ignored.  Exceptions are differentiation, integration, smoothing, and curve fitting, because the step size is significant.  Some operations such as
the FFT (Fast Fourier Transform) assume that the points are uniformly spaced.</t>
<t tx="tom.20220507191015.1"></t>
<t tx="tom.20220507191131.1"></t>
<t tx="tom.20220507191549.1"></t>
<t tx="tom.20220509230416.1">@language md
@tabwidth -4
@others
</t>
<t tx="tom.20220509230545.1">@language md

GF4 is written in Python.  A look at any of the GF4 source files will show
a number of comment lines scattered throughout the file.  These are not
normal comment lines;  here are a few examples:

```
#@+leo-ver=5-thin
#@+node:tom.20211207165051.2: * @file gf4.pyw
#@+others
#@+node:tom.20211207165051.3: ** Imports
#@+node:tom.20211207165051.4: ** class PlotManager(AbstractPlotManager)
```

All these lines start with the prefix `#@`. What in the world are these? These
special comment lines are metadata inserted by the Leo-Editor IDE (Leo for
short). Leo is much more than an IDE. As an IDE, Leo lets you overlay structure
onto a file or project beyond the usual breakdown into classes, methods, and
functions. This along with Leo's structure handling abilities (among other
capabilities) makes understanding and managing large and complex code bases much
easier than most other editors and IDEs. These metadata comment lines are called
*sentinels*.

The sentinel lines tell Leo, when it reads a file, how to create the overlay
structure.  **Do not move or change them!**

Since these lines are comments, they will not affect execution in any way. But
they can be annoying when reading the code outside of Leo. It is possible for
Leo to write these files without sentinels. Leo can load the files and re-apply
the overlay structure. But the results will be less robust against significant
restructuring, since Leo may not be able to match up old and new material as
intended. This could lead to a loss of some of the overlay structure (not the
code itself).

The creator of GF4 has elected to keep the sentinel lines in the files.  This
decision could be revisited at some point.  In the meantime, files can be edited
outside of Leo as long as the sentinels are not moved or changed.

Ideally developers would install Leo and use it for all work on GF4.  But Leo
has a significant learning curve, and if GF4 is to be the only use for Leo,
the effort may not be worthwhile.

For those interested in taking a look at Leo - and Leo is a very fine tool
for development and producing documentation - it is
[on Github](https://github.com/leo-editor/leo-editor).

</t>
<t tx="tom.20220816202839.1">You may need to install some python libraries from Pypi.
Navigate to the gf4-project, which has a file named `requirements.txt`. Run pip 
to install them:

    python3 -m pip -r requirements.txt.

Your Python program may have a different name, so use that.

If one of the pre-requisites has not been installed, GF4 will emit a message about
the missing library, which you can then install (see below for possible Linux-specific
issues).</t>
<t tx="tom.20220816202850.1">Some Linux operating systems, including Debian and Ubuntu, require that
certain libraries must be installed with the OS's package manager and not with 
the usual pip utility.  On Debian/Ubuntu, tkinter has to be installed by 
the package manager:

    sudo apt-get install python3-tk

This may also be the case with some non-Debian systems.
The package manager command will be different.  For the Yum package manager 
(you might have to use sudo, su root, or its equivalent to get administrative
permissions):

    yum install tkinter

You may also need to install ImageTk.  On Debian-based systems:

    sudo apt-get install python3-pil.imagetk

On CentOS/RHEL, the PIL-related packages to install with the package manager 
are (*pillow* has replaced the older *PIL* imaging library):

    python3-pillow
    python3-pillow-tk
</t>
<t tx="tom.20220816202934.1">To run the program, navigate to the gf4-project/gf4 directory and
run the file `gf4.pyw` with either python or pythonw.  Or you can supply the 
entire path to gf4.pyw without changing to its directory. Make sure the python
version is same as you used to install the libraries.

If you put the path to a data file or files on the command line, GF4 will attempt to loaf them.
</t>
<t tx="tom.20220820114259.1">The visible graph can be saved as an image file, such as a .png file.  The
standard MatPlotLib toolbar that GF4 displays near the bottom of the main window
includes a button with an icon of a floppy disk.  Clicking this button opens
the image save dialog.  There is no provision for loading an image into GF4, since
it would not contain the numeric data in a form that GF4 could use.

</t>
<t tx="tom.20220820134816.1">GF4's Design Philosophy
=======================

There are some definite guiding principles that underline the design of GF4.
In general, common user actions should be made as similar and simple as possible.
So for example, operations that need input for parameters from the user (such as a scale factor)
always use the same dialogs, and each operation remembers the values that were
used the last time.

The program should try to remove aggravations for the user.  So there are no
modal error message boxes.  Instead, important messages flash gently at the
bottom of the window, then fade away so the user needs to do nothing to get 
rid of them.  Since dialog boxes that flash out of existence can be annoying,
GF4 dialog boxes fade away gently (system dialogs like the file save dialog
do whatever the underlying system wants to do).

As another example of convenience for the user, GF4's parameter input dialogs accept Python 
numerical expressions so that the user may not have to calculate a value
separately.

There can be conflicts between the principles, or between the principles and
ease of programming.  GF4 tries for simplicity in programming too, but user
ease and consistency are given priority.  Many potentially interesting features 
have never been implemented because they would complicate the user interface.
</t>
<t tx="tom.20220820141745.1">csaps
docutils
matplotlib &lt;= 3.6.3
numpy
pillow &gt;= 9.1.0
pwlf
pyperclip
scipy
statsmodels

</t>
<t tx="tom.20220820182510.1">
.. csv-table:: Waveform Generator Parameters
    :header: "Command", "Param", "Meaning or Scale"
    :widths: 18, 10, 35

    "Sine", "Cycles", "Number of cycles across the screen"
    "Damp Sin", "Cycles", "Number of cycles across the screen"
    "Damp Sin", "Decay", "Decay time constants across the screen"
    "Expon", "Decay", "Decay time constants across the screen"
    "Square Wave", "Cycles", "Number of cycles across the screen"
    "Gaussian PDF", "Mean", "Mean of the generated Gaussian distribution"
    "Gaussian PDF", "Sigma", "Standard Deviation of the generated Gaussian distribution"
    "Gaussian CDF", "Same as", "for Gaussian PDF"
    "Gaussian Noise", "Same as", "for Gaussian PDF"

The *Uniform Noise* command draws a random sample with equal probabilities in the 
range of  0 - 1.0. When not specified, the maximum height of a waveform is 1.0.
If a different value is needed, the waveform can be scaled using the *Scale*
button.</t>
<t tx="tom.20220821142158.1">GF4 has no provision for handling invalid or missing data, except that a line
in the data file that fails the attempt to convert its fields into floating
point numbers will be ignored.

</t>
<t tx="tom.20220821142224.1">The only way that individual data points can be modified within GF4 is to copy
the dataset to the system clipboard and then paste it into the *Load From Dialog*
edit pane.  In the edit pane, individual rows can be corrected or commented out.
</t>
<t tx="tom.20220821142540.1">When GF4 starts up, it sets the following values for the plotting attributes:

.. csv-table:: Default Plot Settings
    :header: "Stack Position", "Color", "Line Thickness", "Line/Symbol"

    "X", black, medium, line
    "Y", cyan, medium, line
    "T", black, thin, line

These values are chosen to make it easy to distinguish between the data sets
when overplotted.  The lighter color of the medium cyan line of the **Y** dataset is 
easy to distinguish from the medium weight black of the X dataset, while the lighter
appearance of the cyan does not distract much from the heavier weight black line.
The thin black line of the **T** dataset is easy to distinguish from the other two.

When GF4 starts up, no stack position has data, so there is nothing to plot.
When the first data set is read, it is automatically plotted.  When other datasets
are read, GF4 notices that there is already data in the **X** stack position, and it
does not plot the new data.  This allows the user to keep reading data files and
overplotting them - possibly in different colors - without destroying an existing
graph.  This can be a very useful capability.
</t>
<t tx="tom.20220901223400.1">@language md
@tabwidth -4

### Devel Branch 1.5b5  4-23-2023, 4-28-2023
- Fix "no data" bug when the last non-comment line is a ENDDATASET special comment.
- Ignore trailing comments while checking whether data is csv.

### Devel Branch 1.5b4 3-23-2023
- Add command button to invert a dataset.

### Devel branch 1.5b3  3-2-2023
- Data input: Allow trailing in-line comments

### Devel branch 1.5b1 2-20-2023
- Add statsmodels to requirements

### Version 1.4 branch 12-29-2022
- Allow extension names in the use_plugins file to have or omit a 'py' extension.

- Added a few unit tests.

### Devel branch 1.4b3  12-12-2022
- Added a Help button (marked with a "?") that explains that a different hover
color indicates that extended help is available.

- Command button hover color is now different when a command has extended help
(accessed by a right mouse click) so user can know which buttons to right click on.

- Command button hover colors now work correctly in Linux as well as Windows.

- Added the ability to read entries in a .ini file.  Initially, this will allow a user to override the startup line colors for [X], [Y] plots.

- Temporary files for the extended help system are now written to the user's Downloads directory.  This works around the problem that on some Linux systems, Python's default location was not readable by the system browser.

- Fonts and command window size adjusted for better appearance in Linux.

- Some operations now set or clear error bands more sensibly.

- Least Squares Linear changed to fit with Nth degree polynomial.

### Release 1.3   11-16-2022
- Better normalization of Correlate, Convolve.

- New Plugins:
    - local polynomial regression (requires "localreg" package).
    - read out y value given x
    - simple calculator

- Improvements to Gaussian PDF, CDF waveform generators.

- Improved fitting normal CDF.

### Devel branch 1.3b3
- Save/Restore plot bitmap, stack state.

    The bitmap of the plot, along with the contents of the waveform stack,
can now by saved and restored.

- Autocorrelation function now centered on zero-lag, is normalized
to 1.0.

- New extended Help facility for GF4 commands

    Extended help for the command buttons is available by right-clicking on the buttons in the Commands window.  At this time only a few commands have help text; over time more of them will be written.
</t>
<t tx="tom.20220902112346.1">
</t>
<t tx="tom.20220902114333.1">The button definition must be a variable named *BUTTON_DEF*
that assigns a tuple with three strings, like this:

.. code:: python

    #             Button Label  Cmd name          Help text
    BUTTON_DEF  = ('Double X', 'double-x', 'Double y values of the X dataset')

The command name can be arbitrary, but if it is the same as an existing command,
the original command will be over-ridden by the new one.  The standard commands
are defined in the GF4 file *BuildCommands.py*.  For example, the command string
"pdfgaus" is linked to a function that creates a Gaussian probability
distribution.</t>
<t tx="tom.20220902114404.1">The function for implementing the new command must be named *proc()*.
It takes no arguments.  For example, to rescale an existing curve by the factor
of two:

.. code:: python

    from AbstractPlotMgr import MAIN
    from .require_datasets import needs_main

    # plotmgr will have been injected into the module by the time this is called
    def proc():
        # Return without trying to do anything if there is no X dataset.
        # This could happen on startup.
        if not has_main(plotmgr):  # see below
            return
        _ds = plotmgr.stack[MAIN]  # The dataset in the X position
        _ds.scale(2)
        plotmgr.plot()

The "plotmgr" attribute represents the active PlotManager instance. Do not try
to import it; it will be automatically injected into the module's attributes
when the command is created.

.. NOTE:: Leo users will notice that Leo complains about an ``undefined name 'plotmgr'`` before the *proc()* function.  This happens because the *plotmgr* object is injected into the module's later when the command is instantiated.  The message can be removed by adding a line ``plotmgr = None`` before *proc()* is defined.

The function *has_main()* performs the same job as the decorator *@REQUIRE_MAIN*
that is used in the *PlotManager* class.  There is also a similar function
*has_main_buffer* corresponding to *@REQUIRE_MAIN_BUFF*.  Other common imports
from the *AbstractPlotManager* class are *BUFFER* and *STACKDEPTH.*

New command functions should use the same techniques for accessing the data and
stack, and for plotting the results, as existing commands.

</t>
<t tx="tom.20220902115843.1">To override an existing command, you must first know its command string.  Use
this command name in the *BUTTON_DEF* declaration. Then add the following declaration
to the plugin file:

.. code:: python

    OVERRIDE = True

Any other value, or if *OVERRIDE* is not defined, will still override the command
but a new button will also be created in the command window in the *plugins* group.

If you use a command name different from any existing name but set ``OVERRIDE = True``,
the command will be created without a matching button.  This leaves you with no
way to access the new command.

</t>
<t tx="tom.20220902120822.1">GF4 has a plugin capability. A plugin is a Python program that defines both a
new command and a new command button to launch it.  It is also possible to override
an existing command without creating a new button.

Plugins must be placed in the *gf4/plugins* directory. Their file name must have
the standard Python extension of ".py".  This directory also includes a
*README.txt* file that explains how the plugin system works.

A plugin must contain a button definition and a function that does the computation
and display.
</t>
<t tx="tom.20220902121203.1">GF4 will load all plugins listed in the file *use_plugins.txt* located in the
*plugins* directory.  Each plugin's name must be on a separate line, without
the ".py" extension.  Blank lines and lines that start with either ";" or "#"
are ignored.

If the *use_plugins.txt* file is not present, then all .py files in the plugins
directory will be loaded.</t>
<t tx="tom.20220904145245.1">A plugin can have its command button added to an existing button group instead
of the *Plugins* group.  To do this, look up the name of the group in 
*buttondefs.py*. Assign that name to the attribute *OWNER_GROUP*, and set
*OVERRIDE* to *True*.  Example:

.. code:: python

    OVERRIDE = True
    OWNER_GROUP = 'DATA_PROCESSING_BUTTONS'

</t>
<t tx="tom.20221108033233.1">For the commands that have buttons in the Command Window, hovering the mouse over
the button causes a brief summary to display in the band at the top of the
Command window.  Right-clicking on a button displays a more detailed
explanation in the system browser.

If an extended help message does not exist for the button, this will be
announced in the announcement bar at the bottom of the main window.</t>
</tnodes>
</leo_file>
