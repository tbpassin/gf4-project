.. rst3: filename: GF4_Users_Guide

:tocdepth: 3

===================
GF4 User's Guide
===================

This User's Guide Covers the Use and Capabilities of the GF4 Waveform Calculator.

What Is GF4?
++++++++++++

GF4 - "GF" being short for "Graphics Framework" - is a program to display
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


.. rubric:: Footnote

.. [1] That is, the discrete differencing equivalent of these operations.

Typical Screen Shot
*******************

Figure IN-1 depicts a fairly typical view of GF4 in action.  The ramp curve generator has produced a straight line, which was copied to the second stack position.  Then a Gaussian noise series was generated and added to the straight line to produce a very noisy ramp.  The underlying straight line, which still was available in its stack position, was then overlayed onto the noisy version.

Of note is the title of the graph.  It was generated automatically, capturing a description of each processing step as a reminder for the user.  This is one of many "affordances" the program provides to reduce demands on the user.  The title can be changed by clicking on it, which turns the title line into an edit box.

.. figure:: images/GF4_Screen_Example.png

    Figure IN-1. Screen Shot Of GF4 In Action.

    The main plotting window is on the left, and the command window is on the right.

A Historical Note
*****************

GF4 is a fifth generation implementation of the basic waveform calculator concept (the first generation - implemented on a 64K Z-80 CP/M machine - was not named).  The implementation language has changed from FORTH to Turbo Pascal to Delphi to the current Python.  Over this time the basic concept has not been changed, while the user interface has evolved and been refined, and more math operations added.

Some Typical Uses
*****************

Typical uses of GF4 include curve fitting and observing the fit quality, comparing observed cdf curves against a gaussian of the same mean and standard distribution, smoothing noisy time series data, and creating FFT transforms to try to identify prominent frequencies in a waveform.
GF4 would make an excellent educational tool since it makes exploring the data so easy, which would help the student come to understand basic statistical limitations that are hard to convey otherwise.

The effect of zero-padding and windowing a waveform before running an FFT is quite illuminating and easy to study.  Cumulative data, such as total covid case counts vs time, can be converted into daily rates by differentiating.  This leads to a very noisy dataset, and that can be smoothed with, for example, a LOWESS smoothing routine. The study of the shape of residuals after fitting a function is interesting and easy to do.

No code need be written to perform any of these operations on datasets.

What GF4 Is Not
***************

GF4 is not a rigorous tool for statistical calculations.  Although the mathematical operations are done as carefully as possible, usually using well-established scientific libraries such as numpy and scipy, various subtleties are not taken into account.  For example, error bars can be shown for a LOWESS smooth, but they do not take into account possible autocorrelation in the dataset.  FFTs, and correlations and convolutions between waveforms, are not normalized according to usual conventions.  This generally makes no practical difference to exploratory use, since it is the relative shapes and features that are normally of interest.  In addition, although processed data sets can be saved to files, and image files of the curves seen on the screen can be saved as well, error bars, regression coefficients, and the like cannot be output.

GF4 is best used for understanding the features of a 2D dataset, and working out how effective various kinds of processing will be.  Is it too noisy or too contaminated to get useful results? Does a linear least squares fit make sense? Does this kind of a correlation seem to be meaningful? Is a smoothing window of 50 too wide?  Will a cosine or a supergaussian window produce a cleaner FFT for this particular data?  Will zero-padding the dataset improve the resolution?  Is this increase really "exponential"?  What will be the effect of a D.C offset on the FFT?

If more than this is needed, the user should take that understanding and use it with other tools to produce a more complete analysis in depth.  The "R" language might be one suitable tool, for example.  After that is done, GF4 can again be used to assess the results as a kind of quality check.

Quick Start
+++++++++++

For a quick introduction, we will work through an example. GF4 will generate the data for us. The file to launch is named gf4.pyw.  It can be launched with pythonw as a GUI application with no console, or with python to also have a console.  The console is not needed except it could display error messages, which are unlikely.  GF4 should be run with some version of python 3.6+.

To launch the program, you can double-click on its icon in the Windows Explorer file manager or the Linux equivalent, or run with python from the directory that contains gf4::

    python3 gf4.pyw

or, for systems with the "py" launcher, either of::

    pyw gf4.pyw
    py gf4.pyw

With a data file name also on the command line, GF4 will open and plot that file on launch.

The "Noisy Ramp" Example
************************

In this example, we will create a dataset that consists of a straight line with Gaussian noise added.  We will fit a line to the noisy data.  Then we will display the fitted line, and overlay the noisy data, the original line, and the error bars for the fit.

Create And Plot The Noisy Line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Create a Straight Line**
---------------------------
To generate the line, click the "Ramp" button. The line will be plotted in the left hand plotting window. this line has been placed in the bottom position of the stack, which is always called "**X**". Copy it to the "**Y**" position (the next one up in the stack) by clicking on the "Copy2Y" button in the "Stack" group.

**Create a Noise Dataset**
---------------------------
With the original line safely stored in **Y**, now create a dataform of noise.  Click on the "Gaussian Noise" button.  In the dialog box that pops up, change the "Sigma" value to 0.3. If we leave it at the default value of 1.0, there will be too much noise.  Even with the smaller value of sigma, there will be a lot of noise.  Accept the values by clicking the OK button or pressing the <ENTER> key.  The noise waveform will display in the plot window.

**Add The Noise To the Original Line**
---------------------------------------
Next we will add the noise to the straight line we saved in **Y**.  In the "Math" column, click on "X + Y".  This will add the two curves together point-by-point and leave the result in the **X** stack position.  The original straight line is unchanged in **Y**.

The sum of the two datasets is a noisy line in **X**, and it has been automatically plotted in the plot window.  In one last touch, click on the "Overplot Y" button in the "Plot" column.  This will overlay the original straight line which is still in **Y**. The result is shown in Figure EX-1a.  Your result may be a little different because you will have gotten a different noise dataset.

.. figure:: images/gf4_example_1_noisy.png

    Figure EX-1a. The Noisy Ramp With Original (Clean) Curve Overlaid.

**Plot the Noisy Data With Point Symbols Instead Of Lines**
------------------------------------------------------------
The Gaussian noise data points don't really form a curve because they are independent.  Perhaps it would be better to plot the noisy ramp with points instead of lines.  Try this out by using the "Plot" menu on the left-hand plot window. Select Plot/Main Marker Style/Symbol.  Then click on the "Plot" item in the "Plot" Menu or the "Plot X" button in the commands window.  Then overplot the original ramp in **Y** using the "Overplot Y" button.

The results will resemble Figure EX-1b.

.. Figure:: images/gf4_example_1_noisy_symbols.png

    Figure EX-1b. The Noisy Ramp Plotted With Symbols Instead Of Lines.

Finally, set the main marker style back to "Line"

**Save The Noisy Line For Later Viewing**
------------------------------------------
For this example, at the end we will overlay this noisy line on the plot of the fitted line.  Copy it to the **T** stack position by clicking the "Copy2T" button in the "Stack" group (see `Direct Access`_).

Fit and Plot The Noisy Line
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To fit a linear least squares fit to the noisy ramp, click on the "Lst Sqr Lin" button in the upper right of the commands window.  The best fit straight line will plot in the plotting window.

**Overplot The Other Datasets For Comparison**
----------------------------------------------
For this example we will overplot the original ramp and the noisy version of the ramp.  These datasets are still in **Y** and **T** where we put them.

Click on the "Overplot Y" button in the "Plot" group at the left of the command window. The original straight line will be plotted in a light cyan color.  It will probably be a little different from the fitted line.  That is normal, because the noisy sample we used is unlikely to have exactly the same properties as the original.

Click on the "Overplot T" button to overplot the noisy dataset.

**Overlay Error Bands For The Fit**
-----------------------------------
Error bands for the fit are available for most of the fitting routines.  Click the "Error Bands" button to see them.  Each time this button is clicked, the error band area gets less transparent, so you can adjust the visibility if needed.

The results are shown in Figure EX-1c.

.. figure:: images/gf4_example_1_fitted.png

    Figure EX-1c. The Least Squares Fitted Line With Error Bands And Original Data.

Encouraging Remarks
*******************

Examples like this are usually much harder to describe than to do.  With a little practice, these kinds of operations become familiar and they go very quickly.  One gets used to the location of the command buttons that are commonly used, and the stack positions stop feeling strange.  Just like a physical calculator, in fact.

Data Format
+++++++++++

Input Data Format
------------------
GF4 accepts text files with whitespace-separated columns, one data point per
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

The Waveform Stack
++++++++++++++++++

The waveform stack is the primary organizing concept of GF4.  Modeled after
the stack in Hewlett-Packard RPN calculators, the stack is an array with positions
that can hold data elements.  Conceptually, the stack is arranged as a vertical 
column with a "bottom" and a "top".  Items on the stack can be "pushed" upwards,
"dropped" downwards, "rotated" and "swapped". These operations are illustrated
in the next section.

The most common stack oprations in practice are "Swap" and direct access.  The
T position is often used as a temporary data cache.

Stack Operations
****************

The stack can be "pushed", causing the existing
elements to be moved one slot "higher"::

    Stack populated with data elements A, B, and C

    |   A   |   <-- "T": stack top
    |   B   |   <-- "Y"
    |   C   |   <-- "X": stack bottom

    "Pushing" stack duplicates "X" element (top element is lost)

    |   B   |   <-- "T": stack top
    |   C   |   <-- "Y"
    |   C   |   <-- "X": stack bottom


"Dropping" the stack moves elements one slot lower::

    Stack populated with data elements A, B, and C

    |   A   |   <-- "T": stack top
    |   B   |   <-- "Y"
    |   C   |   <-- "X": stack bottom

    "Dropping" stack duplicates "T" element (bottom element is lost)

    |   A   |   <-- "T": stack top
    |   A   |   <-- "Y"
    |   B   |   <-- "X": stack bottom

The stack can also be cyclically rotated up or down::

    Stack populated with data elements A, B, and C

    |   A   |   <-- "T": stack top
    |   B   |   <-- "Y"
    |   C   |   <-- "X": stack bottom

    Rotated "up" (T -> X, X -> Y, Y -> T)

    |   B   |   <-- "T": stack top
    |   C   |   <-- "Y"
    |   A   |   <-- "X": stack bottom

    Stack populated with data elements A, B, and C

    |   A   |   <-- "T": stack top
    |   B   |   <-- "Y"
    |   C   |   <-- "X": stack bottom

    Rotated "down" (T -> Y, Y -> X, X -> T)

    |   C   |   <-- "T": stack top
    |   A   |   <-- "Y"
    |   B   |   <-- "X": stack bottom

"Swap" exchanges the X and Y data elements::

    Stack populated with data elements A, B, and C

    |   A   |   <-- "T": stack top
    |   B   |   <-- "Y"
    |   C   |   <-- "X": stack bottom

    Stack after a "Swap"

    |   A   |   <-- "T": stack top
    |   C   |   <-- "Y"
    |   B   |   <-- "X": stack bottom

Direct Access
*************

The data element in X, the stack bottom, can be copied to the Y and T positions.
The Y and T data elements can be copied to the X postion.  All the stack
operations are carried out by clicking buttons in the auxiliary command window.

.. image:: images/stack_ops.png

Non-Stack Storage
+++++++++++++++++

In addition to the stack, there are several other data storage locations:

1. A single slot accessed by the "Store 1" and "Recall 1" buttons.
These store from and retrieve to the X position.

2. The system clipboard, accessed by the "Copy To Clipboard" and "Load From Dialog"
buttons. The latter opens an editing window into which the clipboard can be
copied.

These buttons are marked in the image below:

.. image:: images/loadsave.png

Plotting Curves
+++++++++++++++

Changing Colors, Symbols, and Line Styles
*****************************************

Loading And Saving Data
+++++++++++++++++++++++

All data is saved from and loaded to the X stack position.

Operations On One Waveform
++++++++++++++++++++++++++

Operations On Two Waveforms
+++++++++++++++++++++++++++

The Waveform Generators
+++++++++++++++++++++++

We encountered one of GF4's waveform generators in the `Quick Start`_ section.

Curve Fitting
+++++++++++++

Curve Smoothing
+++++++++++++++

Windowing and FFTs
++++++++++++++++++

Using Macros
++++++++++++

