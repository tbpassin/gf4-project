#@+leo-ver=5-thin
#@+node:tom.20220829181057.1: * @file test_plugin.py
#@@language python
"""Demo plugin - does nothing useful."""

BUTTON_DEF  = ('Plugin Test', 'plugin-test', 'A dummy plugin for development')

# plotmgr will have been injected into the module by the time this is called
def proc():
    print('I am the plugin procedure.  I do nothing', plotmgr)

#@-leo
