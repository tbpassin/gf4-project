.. rst3: filename: plugins

The Plugin System
+++++++++++++++++

GF4 has a plugin capability. A plugin is a Python program that defines both a
new command and a new command button to launch it.  It is also possible to override
an existing command without creating a new button.

Plugins must be placed in the *gf4/plugins* directory. Their file name must have
the standard Python extension of ".py".  This directory also includes a
*README.txt* file that explains how the plugin system works.

A plugin must contain a button definition and a function that does the computation
and display.

Defining a Command Button
*************************

The button definition must be a variable named *BUTTON_DEF*
that assigns a tuple with three strings, like this:

.. code:: python

    #             Button Label  Cmd name          Help text
    BUTTON_DEF  = ('Double X', 'double-x', 'Double y values of the X dataset')

The command name can be arbitrary, but if it is the same as an existing command,
the original command will be over-ridden by the new one.  The standard commands
are defined in the GF4 file *BuildCommands.py*.  For example, the command string
"pdfgaus" is linked to a function that creates a Gaussian probability
distribution.

The Implementing Function
*************************

The function for implementing the new command must be named *proc()*.
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

Over-riding An Existing Command
*******************************

To override an existing command, you must first know its command string.  Use
this command name in the *BUTTON_DEF* declaration. Then add the following declaration
to the plugin file:

.. code:: python

    OVERRIDE = True

Any other value, or if *OVERRIDE* is not defined, will still override the command
but a new button will also be created in the command window in the *plugins* group.

If you use a command name different from any existing name but set ``OVERRIDE = True``,
the command will be created without a matching button.  This leaves you with no
way to access the new command.

Adding a Button To an Existing Group
************************************

A plugin can have its command button added to an existing button group instead
of the *Plugins* group.  To do this, look up the name of the group in 
*buttondefs.py*. Assign that name to the attribute *OWNER_GROUP*, and set
*OVERRIDE* to *True*.  Example:

.. code:: python

    OVERRIDE = True
    OWNER_GROUP = 'DATA_PROCESSING_BUTTONS'

Controlling Which Plugins Get Loaded
************************************

GF4 will load all plugins listed in the file *use_plugins.txt* located in the
*plugins* directory.  Each plugin's name must be on a separate line, without
the ".py" extension.  Blank lines and lines that start with either ";" or "#"
are ignored.

If the *use_plugins.txt* file is not present, then all .py files in the plugins
directory will be loaded.

