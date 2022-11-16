#@+leo-ver=5-thin
#@+node:tom.20220829232158.1: * @file import_plugins.py
"""Import all modules in the plugins directory.

   If there is a file named use_plugins.txt, only import modules listed
   there, otherwise import all modules in the plugins directory.
   
   The plugins list file must contain one plugin name per line.  The name
   must not contain the file extension (e.g., ".py").  Blank lines and lines
   starting with "#" are ignored.  Plugins named in the file but which do not
   exist are ignored.
   
   Returns a list of the imported modules.
"""

import os.path, os
import importlib

USE_PLUGINS = 'use_plugins.txt'  # List of plugins to import  (optional)

our_dir = os.path.dirname(__file__)
plugin_dir = os.path.join(our_dir, 'plugins')

has_plugin_dir = os.path.exists(plugin_dir)
if not has_plugin_dir:
    print('No plugins directory')

use_plugins_file = os.path.join(plugin_dir, USE_PLUGINS)
use_plugins_import_list = os.path.exists(use_plugins_file)

#@+others
#@+node:tom.20220830112606.1: ** Get Plugins List
plugins_import_list = []
if use_plugins_import_list:
    with open(use_plugins_file, encoding = 'utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
        plugins_import_list = [p for p in lines if p[0] not in '#;']
#@+node:tom.20220830113113.1: ** import_all_plugins
def import_all_plugins():
    """Import modules from the plugins directory and return a list of them.

    If there is a file USE_PLUGINS, only import the ones listed there.
    Otherwise import all ".py" files.
    
    RETURNS
    a list of successfully imported modules.
    """
    global plugins_import_list
    modules = []
    if not has_plugin_dir:
        return modules

    if not use_plugins_import_list:
        plugins_import_list = []
        for root, dirs, files in os.walk(plugin_dir):
            if root == plugin_dir:
                break
        for f in files:
            f, ext = os.path.splitext(f)
            if ext == '.py':
                plugins_import_list.append(f)

    for f in plugins_import_list:
        try:
            mod = importlib.import_module(f'plugins.{f}')
            if hasattr(mod, 'BUTTON_DEF'):
                modules.append(mod)
        except ImportError as e:
            print(f'{__name__}: {f} plugin: {e}')
            continue
    return modules
#@-others

if __name__ == '__main__':
    if has_plugin_dir:
        modules = import_all_plugins()
        for m in modules:
            print(getattr(m, 'BUTTON_DEF'))
#@-leo
