GF4 - "GF" being short for "Graphics Framework" - is a Python program to display
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

You may need to install some python libraries from Pypi.
Navigate to the gf4-project, which has a file named `requirements.txt`. Run pip 
to install them:

    python3 -m pip -r requirements.txt.

Your Python program may have a different name, so use that.

If one of the pre-requisites has not been installed, GF4 will emit a message about
the missing library, which you can then install (see below for possible Linux-specific
issues).
Some Linux operating systems, including Debian and Ubuntu, require that
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
To run the program, navigate to the gf4-project/gf4 directory and
run the file `gf4.pyw` with either python or pythonw.  Or you can supply the 
entire path to gf4.pyw without changing to its directory. Make sure the python
version is same as you used to install the libraries.
