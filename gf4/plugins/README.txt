GF4 has a plugin mechanism that can load plugin files located in the "plugins"
directory.  This README provides some basic information for developers of plugins.

WHAT A PLUGIN PROVIDES
-----------------------
Each plugin can supply a single command together with a matching command
button for the button window.

WHAT A PLUGIN SHOULD IMPORT
---------------------------
In addition to whatever modules the plugin may need for its operation, if it
will work with datasets that are managed by the PlotManager, it should import
helper attributes, usually MAIN and BUFFER, which identify the key stack
positions. Typically:

from AbstractPlotMgr import MAIN, BUFFER

If you want to make sure there is a dataset in the MAIN or MAIN+BUFFER positions,
then import them from the module "require_dataset" in the plugins directory:

from .require_datasets import needs_main
# and possibly:
from .require_datasets import needs_main_buffer

These functions perform the same jobs as the PlotManager decorators
@REQUIRE_MAIN and @REQUIRE_MAIN_BUFF.  Other useful declarations may be found
in the "AbstractPlotMgr" module.

WHAT A PLUGIN MUST INCLUDE
---------------------------
Each plugin must provide a tuple named "BUTTON_DEF".  The tuple must contain
three elements: Button label, the command name, and an explanatory help text.
The help text will appear in the top information band when the mouse hovers
over the button.  Example:

#                Label       Cmd name          Help text
BUTTON_DEF  = ('Double X', 'double-x', 'Double y values of the X dataset')

Each plugin must also provide a function that will perform its operation.
This function must be named "proc" and take no parameters. The function is not
expected to return anything.  For example:

# plotmgr will have been injected into the module by the time this is called
def proc():
    if not needs_main(plotmgr):  # see below
        return
    _ds = plotmgr.stack[MAIN]
    _ds.scale(2)
    plotmgr.plot()

The "plotmgr" attribute represents the active PlotManager instance. Do not try
to import it; it will be automatically injected into the module's attributes
when the command is created.

Optionally the plugin may define

OVERRIDE = True

If this attribute exists in the module and has the value True, no button will be
added.  The command will still be registered, and if that name alreade exists
in the command dictionary, the previous assignment will be replace by the new one.
This provides a way to override an existing command (though the label and help
message of the button will not be chagned).

HOW TO SPECIFY WHICH PLUGINS TO USE
-----------------------------------
By default, GF4 will load all plugins (i.e., python files) in the "plugins"
directory.  You can override this by including a file named "use_plugins.txt".
The file should contain the desired plugins by file name, one to a line.
Do *not* include the ".py" file extension.  Blank lines and lines that
start with a "#" or ";" character will be ignored.


