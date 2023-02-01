#@+leo-ver=5-thin
#@+node:tom.20221107232208.1: * @file help_cmds.py
"""Contains explanatory text about commands having buttons in the Command Window.

The text is assumed to be written in RestructuredText, and that it will
be converted by docutils before being displayed.

Each entry is keyed by the command string used to dispatch it.
"""
HELPTEXT = {
#@+others
#@+node:tom.20221115112809.1: ** Data Processing
#@+node:tom.20221108025620.1: *3* autocor
'autocor': r'''

autocor
=======

Operates on: [X]

Calculate the autocorrelation of the dataset in [X].  The result is normalized
to 1.0, and is centered on 0 on the horizontal axis.  The horizontal axis
represents the lags.

The autocorrelation coefficient at lag k is defined as a sum over the dataset:

.. math:: 

    c_k = \sum_n v_{n+k} \cdot \overline{v_n}

GF4 always works with real numbers, so this is equivalent to

.. math::

    c_k = \sum_n v_{n+k} \cdot v_n

This command uses the NumPy function `correlate` with full overlap.  See
`numpy.correlate <https://numpy.org/doc/stable/reference/generated/numpy.correlate.html>`_

For a more detailed discussion of the autocorrelation, see `Autocorrelation <https://en.wikipedia.org/wiki/Autocorrelation>`_.

''',

#@+node:tom.20221108001524.1: *3* fft
'fft': '''

FFT
===
Operates on: [X]

Perform a (discrete) Fast Fourier Transform (FFT) on [MAIN].  Dataset length does not
need to be a power of two.  This is a real FFT: only the magnitude of the
transform is computed.

Points are assumed to be equally spaced on the horizontal axis.

This command uses the RFFT function from the NumPy package. See 
`numpy.fft.rfft <https://numpy.org/doc/stable/reference/generated/numpy.fft.rfft.html>`_

.. Note:: There are several conventions for normalizing an FFT.  This command uses the normalization provided by the NumPy function.

''',
#@+node:tom.20221115112905.1: ** Curve
#@+node:tom.20221107232937.1: *3* dedup
'dedup':'''

dedup
======
Operates on: [X]

If a point is followed immediately by one or more points with the same value,
remove all but the first.

''',
#@+node:tom.20221108000124.1: *3* pad
'pad':'''

pad
====
Change the number of points in [X].

If the target length is larger, pad the dataset with zeros.  If the target 
length is shorter, truncate the dataset by removing points from the right.

.. Note:: This is different from the *Trim* command, which removes points from either the start or the end of the dataset.

''',
#@+node:tom.20221115112952.1: ** Math
#@+node:tom.20221108194935.1: *3* diff
'diff': r'''

Diff
=====

Operates on: [X]

Differentiate the [X] dataset using the simplest possible algorithm:

.. math::

    \frac{dy_k}{dx} = \frac{y_{k+1} - y_k}{x_{k+1} - x_k}

The result has one less point than the original dataset because there is no point
:math:`y_{N+1}` where N is the index of the last point in the dataset.

''',
#@+node:tom.20221108201916.1: *3* diff2
'diff2': r'''

Central Diff
============

Operates on: [X]

Differentiate the [X] dataset using the central differencing:

.. math::

    \frac{dy_k}{dx} = \frac{y_{k+1} - y_{k-1}}{x_{k+1} - x_{k-1}}

At either end of the datset, the central difference cannot be computed because
there are no points for :math:`x_{-1}` and :math:`x_{N+1}`, so the first and last point are computed using one-sided differencing.  The last point is calculated using
the one-sided calculation :math:`(y_N - y_{N-1})/(x_{N} - x_{N-1})`, so the
number of points equals the original number of points.

Whether to use central or one-sided differencing depends in part on whether
changes from one point to the next are important. If not, central differencing
would usually be the better choice.  Also, one-sided differencing produces
values that are offset by half a step for their index number, while central
differencing has no such offset.
''',
#@+node:tom.20221108165543.1: ** play-macro
'play-macro': '''

play-macro
===========

Plays back a recorded macro if there is one.

When a macro is played back, all the recorded operations will be performed in the order they
were recorded.  Any data entry dialog that a recorded command
uses will open again during playback.  Since these dialogs remember their previous
values, usually pressing the <ENTER> key - to accept the previous values - will 
be the only user action needed.


''',
#@+node:tom.20221108163336.1: ** record-macro
'record-macro': '''

record-macro
=============

When pressed once, the Macro *Record* button changes its color, indicating that
it is in the "record" state.  All command button presses will be recorded
until the *Record* button is pressed again.  After the second press, the button
will return to its normal color.

When a macro is played back, all the recorded operations will be performed in the order they
were recorded.  Any data entry dialog that a recorded command
uses will open again during playback.  Since these dialogs remember their previous
values, usually pressing the <ENTER> key - to accept the previous values - will 
be the only user action needed.

Pressing the Macro *Record* button again will clear the current macro and
start recording a new one.

''',

#@-others
}
#@-leo
