GF4 - "GF" being short for "Graphics Functions" - is a Python program to
display two-dimensional data, such as time series data, and to perform
mathematical operations on the data or between two related data sets. We
sometimes call the 2D data sets "waveforms" because the data often
represents time domain waveforms. Otherwise we generally call the data by
the term "datasets". The program aims to make data exploration easy and
enjoyable.

The program's interface is modeled after hand-held calculators of the
"reverse polish notation" (RPN) style. This kind of calculator was made
famous by Hewlett-Packard, starting with their HP-35 and HP-45 calculators.
GF4 works with waveforms in place of the numbers manipulated by the hand
calculators.

Thus, a waveform can be scaled, squared, have its logarithm taken,
integrated and differentiated, be normalized and rectified, and so on. A
discrete Fast Fourier Transform is provided that is not limited to powers
of two in data length. Data can be trimmed or padded. Curve fitting and
smoothing of several varieties can be done. Two waveforms can be added,
subtracted, multiplied, and divided (where possible), correlated or
convolved together, among others.  A smoothed waveform can be overplotted
on the unsmoothed original.  Linear, semilog, and log-log plots are 
available.

A certain number of basic waveforms can be generated, including a delta
function, step, ramp, sine and damped sine, Gaussian PDF and CDF
distributions, and more. Altogether there are nearly 80 different
operations available.

A basic macro facility is provided to automate a sequence of repeated
operations.

Like RPN calculators, GF4 operations are organized around a stack of data
sets. Unlike those calculators, the various stack levels can be accessed
directly as well.

The current version of the program is somewhat uneven in the degree of
polish of the various operations. This reflects its evolution under the
interests and changing needs of the author.  Mathematically, many operations
are implemented by numpy or scipy computations;  others are algorithms
implemented by the author.
