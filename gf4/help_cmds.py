#@+leo-ver=5-thin
#@+node:tom.20221107232208.1: * @file help_cmds.py
"""Contains explanatory text about commands in the Command Window."""

HELPTEXT = {
#@+others
#@+node:tom.20221108025620.1: ** autocor
'autocor': '''

autocor
=======

Operates on: [MAIN]

Calculate the autocorrelation of the dataset in [MAIN].  The result is normalized
to 1.0, and is centered on 0 on the horizontal axis.  The horizontal axis
represents the lags.

The autocorrelation is defined as the sum over the dataset of

.. math:: 

    c_k = \sum_n v_{n+k} \cdot \overline{v_n}

GF4 always works with real numbers, so this is equivalent to

.. math::

    c_k = \sum_n v_{n+k} \cdot v_n

This command uses the NumPy function `correlate` with full overlap.  See
`numpy.correlate <https://numpy.org/doc/stable/reference/generated/numpy.correlate.html>`_

''',

#@+node:tom.20221107232937.1: ** dedup
'dedup':'''

dedup
======
Operates on: [MAIN]

If a point is followed immediately by one or more points with the same value,
remove all but the first.

''',
#@+node:tom.20221108001524.1: ** fft
'fft': '''

fft
===
Operates on: [MAIN]

Perform a (discrete) Fast Fourier Transform (FFT) on [MAIN].  Dataset length does not
need to be a power of two.  This is a real FFT: only the magnitude of the
transform is computed.

Points are assumed to be equally spaced on the horizontal axis.

This command uses the RFFT function from the NumPy package. See 
`numpy.fft.rfft <https://numpy.org/doc/stable/reference/generated/numpy.fft.rfft.html>`_

.. Note:: There are several conventions for normalizing an FFT.  This command uses the normalization provided by the NumPy function.

''',
#@+node:tom.20221108000124.1: ** pad
'pad':'''

pad
====
Change the number of points in [MAIN].

If the target length is larger, pad the dataset with zeros.  If the target 
length is shorter, truncate the dataset by removing points from the right.

.. Note:: This is different from the *Trim* command, which removes points from either the start or the end of the dataset.

''',
#@-others
}
#@-leo
