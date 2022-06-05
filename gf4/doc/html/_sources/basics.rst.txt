.. rst3: filename: basics

Data Format
+++++++++++

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

The state of the stack can be viewed by using the *Help/ Show Stack* menu item in the main window.  This opens a small window that shows the name of the dataset 
currently in each stack position. It is helpful to keep this window open while
one gains experience with GF4.  The image below depicts the stack viewer window:

.. image:: images/stack_viewer_window.png
    :scale: 50

The most common stack operations in practice are "Swap" and direct access.  The
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
The Y and T data elements can be copied to the X position.  All the stack
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

Loading And Saving Data
+++++++++++++++++++++++

All data is saved from and loaded to the X stack position.

Plotting Curves
+++++++++++++++

Changing Colors, Symbols, and Line Styles
*****************************************

