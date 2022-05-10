
GF4 is written in Python.  A look at any of the GF4 source files will show
a number of comment lines scattered throughout the file.  These are not
normal comment lines;  here are a few examples::

    #@+leo-ver=5-thin
    #@+node:tom.20211207165051.2: * @file gf4.pyw
    # pylint: disable = consider-using-f-string
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

