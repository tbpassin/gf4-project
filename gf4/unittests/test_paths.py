#@+leo-ver=5-thin
#@+node:tom.20230131195511.1: * @file test_paths.py
#@@language python
"""Check if some standard paths exist."""

from pathlib import Path
from gf4.gf4 import GF4_DIR
from gf4.utility import ICONPATH

class TestPaths:
    def test_plugins_path(self):
        """Check that the plugin directory exists."""
        plugins_dir = Path(GF4_DIR) / Path('plugins')
        assert plugins_dir.exists()

    def test_icon_path(self):
        """Check that the icon file exists."""
        iconfile = Path(ICONPATH)
        assert iconfile.exists()

#@-leo
