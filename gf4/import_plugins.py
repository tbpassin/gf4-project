#@+leo-ver=5-thin
#@+node:tom.20220829232158.1: * @file import_plugins.py
"""Import all modules in the plugins directory.

    Returns a list of the imported modules.
"""

import os.path, os
import importlib

our_dir = os.path.dirname(__file__)
plugin_dir = os.path.join(our_dir, 'plugins')

has_plugin_dir = os.path.exists(plugin_dir)
if not has_plugin_dir:
    print('No plugins directory')

def import_all_plugins():
    modules = []
    if not has_plugin_dir:
        return modules
    for root, dirs, files in os.walk(plugin_dir):
        if root == plugin_dir:
            break
    for f in files:
        f = os.path.splitext(f)[0]
        try:
            mod = importlib.import_module(f'plugins.{f}')
            modules.append(mod)
        except ImportError:
            continue
    return modules

if __name__ == '__main__':
    if has_plugin_dir:
        modules = import_all_plugins()
        for m in modules:
            print(getattr(m, 'BUTTON_DEF'))
#@-leo
