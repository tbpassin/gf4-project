<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="tom.20220507132007.1"><vh>Docs</vh>
<v t="tom.20220507132007.2"><vh>@clean ../README.md</vh>
<v t="tom.20220507132007.3"><vh>gf4-project</vh></v>
</v>
<v t="tom.20220509230416.1"><vh>@clean ../DEVELOPERS_READ_THIS.md</vh>
<v t="tom.20220509230545.1"><vh>Leo-Editor, Or Those Strange Comment Lines</vh></v>
</v>
<v t="tom.20220507132007.4"><vh>@path doc</vh>
<v t="tom.20220507132007.5"><vh>@button Build HTML</vh></v>
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
<v t="tom.20220507180611.1"><vh>@rst basics</vh>
<v t="tom.20220507132007.17"><vh>Data Format</vh></v>
<v t="tom.20220507132007.18"><vh>The Waveform Stack</vh>
<v t="tom.20220507135125.1"><vh>Stack Operations</vh></v>
<v t="tom.20220507140739.1"><vh>Direct Access</vh></v>
</v>
<v t="tom.20220507143340.1"><vh>Non-Stack Storage</vh></v>
<v t="tom.20220507132007.22"><vh>Loading And Saving Data</vh></v>
<v t="tom.20220507132007.19"><vh>Plotting Curves</vh>
<v t="tom.20220507132007.20"><vh>Changing Colors, Symbols, and Line Styles</vh></v>
</v>
</v>
<v t="tom.20220507185750.1"><vh>@rst waveforms</vh>
<v t="tom.20220507190615.1"><vh>Generating And Operating on Waveforms</vh>
<v t="tom.20220507132007.25"><vh>The Waveform Generators</vh></v>
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
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="tom.20220507132007.1"></t>
<t tx="tom.20220507132007.10">Typical uses of GF4 include curve fitting and observing the fit quality, comparing observed cdf curves against a gaussian of the same mean and standard distribution, smoothing noisy time series data, and creating FFT transforms to try to identify prominent frequencies in a waveform.

GF4 would make an excellent educational tool since it makes exploring the data so easy, which would help the student come to understand basic statistical limitations that are hard to convey otherwise.

The effect of zero-padding and windowing a waveform before running an FFT is quite illuminating and easy to study.  Cumulative data, such as total covid case counts vs time, can be converted into daily rates by differentiating.  This leads to a very noisy dataset, and that can be smoothed with, for example, a LOWESS smoothing routine. The study of the shape of residuals after fitting a function is interesting and easy to do.

No code need be written to perform any of these operations on datasets.</t>
<t tx="tom.20220507132007.11">GF4 is not a rigorous tool for statistical calculations.  Although the mathematical operations are done as carefully as possible, usually using well-established scientific libraries such as numpy and scipy, various subtleties are not taken into account.  For example, error bars can be shown for a LOWESS smooth, but they do not take into account possible autocorrelation in the dataset.  FFTs, and correlations and convolutions between waveforms, are not normalized according to usual conventions.  This generally makes no practical difference to exploratory use, since it is the relative shapes and features that are normally of interest.  In addition, although processed data sets can be saved to files, and image files of the curves seen on the screen can be saved as well, error bars, regression coefficients, and the like cannot be output.

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

With the original line safely stored in **Y**, now create a dataform of noise.  Click on the "Gaussian Noise" button.  In the dialog box that pops up, change the "Sigma" value to 0.3. If we leave it at the default value of 1.0, there will be too much noise.  Even with the smaller value of sigma, there will be a lot of noise.  Accept the values by clicking the OK button or pressing the &lt;ENTER&gt; key.  The noise waveform will display in the plot window.

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
row. If there is only one column, GF4 inserts an imputed first column with
values being consecutive integers beginning with 1. The "first" column becomes
the "x", or horizontal, axis. If there are more than two columns, a dialog is
displayed so the user can choose the two desired columns. The number of columns
is derived based on the first non-comment, non-blank line whose first field is a
legal floating point number.

Data fields must be numeric.  GF4 cannot make use of non-numeric data.  Data
fields are converted to floating point numbers.

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

All operations that change data operate on the data in the stack bottom (the X position). All operations between two datasets, such as addition and correlation, use the X and Y positions (Y is the next position up from X);  the result of these operations only change data in the X position.

The state of the stack can be viewed by using the *Help/ Show Stack* menu item in the main window.  This opens a small window that shows the name of the dataset 
currently in each stack position. It is helpful to keep this window open while
one gains experience with GF4.  The image below depicts the stack viewer window:

.. image:: images/stack_viewer_window.png
    :scale: 50

The most common stack operations in practice are "Swap" and direct access.  The
T position is often used as a temporary data cache.</t>
<t tx="tom.20220507132007.19"></t>
<t tx="tom.20220507132007.2">@language md
@tabwidth -4
@others
</t>
<t tx="tom.20220507132007.20"></t>
<t tx="tom.20220507132007.22">All data is saved from and loaded to the X stack position.</t>
<t tx="tom.20220507132007.23"></t>
<t tx="tom.20220507132007.24"></t>
<t tx="tom.20220507132007.25">We encountered one of GF4's waveform generators in the `Quick Start &lt;quickstart&gt;`_ section.</t>
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

How To Run GF4
===============
No installation is required.  You may need to install some python libraries from Pypi.
Navigate to the gf4-project, which has a file named `requirements.txt`. Run pip 
to install them:

    python3 -m pip -r requirements.txt.

Your Python may have a different name, so use that.

To run the program, navigate to the gf4-project/gf4 directory and
run the file `gf4.pyw` with either python or pythonw.  Make sure the python
version is same as you used to install the libraries.
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
        '-D', 'copyright=Thomas B. Passin 2022',
        '-D', "html_theme_options.sidebarwidth=20em",

        # sourcedir, outputdir:
        r'.', r'html']

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
    basics
    waveforms
    curvefitting
    windowing
    macros
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

.. [1] That is, the discrete differencing equivalent of these operations.

</t>
<t tx="tom.20220507132007.8">Figure IN-1 depicts a fairly typical view of GF4 in action.  The ramp curve generator has produced a straight line, which was copied to the second stack position.  Then a Gaussian noise series was generated and added to the straight line to produce a very noisy ramp.  The underlying straight line, which still was available in its stack position, was then overlayed onto the noisy version.

Of note is the title of the graph.  It was generated automatically, capturing a description of each processing step as a reminder for the user.  This is one of many "affordances" the program provides to reduce demands on the user.  The title can be changed by clicking on it, which turns the title line into an edit box.

.. figure:: images/GF4_Screen_Example.png

    Figure IN-1. Screen Shot Of GF4 In Action.

    The main plotting window is on the left, and the command window is on the right.
</t>
<t tx="tom.20220507132007.9">GF4 is a fifth generation implementation of the basic waveform calculator concept (the first generation - implemented on a 64K Z-80 CP/M machine - was not named).  The implementation language has changed from FORTH to Turbo Pascal to Delphi to the current Python.  Over this time the basic concept has not been changed, while the user interface has evolved and been refined, and more math operations added.</t>
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
<t tx="tom.20220507140739.1">The data element in X, the stack bottom, can be copied to the Y and T positions.
The Y and T data elements can be copied to the X position.  All the stack
operations are carried out by clicking buttons in the auxiliary command window.

.. image:: images/stack_ops.png</t>
<t tx="tom.20220507143340.1">In addition to the stack, there are several other data storage locations:

1. A single slot accessed by the "Store 1" and "Recall 1" buttons.
These store from and retrieve to the X position.

2. The system clipboard, accessed by the "Copy To Clipboard" and "Load From Dialog"
buttons. The latter opens an editing window into which the clipboard can be
copied.

These buttons are marked in the image below:

.. image:: images/loadsave.png
</t>
<t tx="tom.20220507175416.1"></t>
<t tx="tom.20220507175950.1">:tocdepth: 2
</t>
<t tx="tom.20220507180306.1"></t>
<t tx="tom.20220507180611.1"></t>
<t tx="tom.20220507185750.1"></t>
<t tx="tom.20220507190251.1"></t>
<t tx="tom.20220507190615.1"></t>
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
normal comment lines;  here are a few examples::

    #@+leo-ver=5-thin
    #@+node:tom.20211207165051.2: * @file gf4.pyw
    #@+others
    #@+node:tom.20211207165051.3: ** Imports
    #@+node:tom.20211207165051.4: ** class PlotManager(AbstractPlotManager)

All these lines start with the prefix **#@**. What in the world are these? These
special comment lines are metadata inserted by the Leo-Editor IDE (Leo for
short). Leo is much more than an IDE. As an IDE, Leo lets you overlay structure
onto a file or project beyond the usual breakdown into classes, methods, and
functions. This along with Leo's structure handling abilities (among other
capabilities) makes understanding and managing large and complex code bases much
easier than most other programs. These metadata comment lines are called
*sentinels*.

The sentinel lines tell Leo, when it reads a file, how to create the overlay
structure.  **Do not move or change them!**

Since these lines are comments, they will not affect execution in any way.
But they can be annoying when reading the code outside of Leo.  It is possible
for Leo to write these files without sentinels.  Leo can load the files and 
re-apply the overlay structure.  But the results will be less robust against
significant restructuring, since Leo may not be able to match up old and new
material as intended.  This could lead to a loss of some of the overlay structure.

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
</tnodes>
</leo_file>
