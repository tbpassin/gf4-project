#@+leo-ver=5-thin
#@+node:tom.20251115091050.1: * @file add_spacer.py
"""Add spacer to Plugins button list.  Can be added several times."""
BUTTON_DEF = (None, None, None)
OVERRIDE = False  # Override default location.

plotmgr = None

# plotmgr will have been injected into the module by the time this is called
# This function must exist even though it does nothing.
def proc():
    ...
#@-leo
