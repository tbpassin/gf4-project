
### New "partial autocorrelation" command
#### Devel branch v1.3b2

### "Phasespace" plot
#### Devel branch, 11/2/202 v1.3 b1
Lag can be specified (previously: only lag-1). 

### Startup Window Location, Size, Icons
#### Devel branch

10/7/2022, v1.3 b1:

- Tweak initial vertical position of main window: 
- Improve command window fonts and window height, especially on Linux.

10/26/2008 v1.3 b1

-Show program icon in main window.

### Icons for desktop launchers
#### Devel branch. 10/3/2022, v1.2
A new _icons_ directory contains icons for Linux and Windows desktop launchers.

### Plugins command buttons
#### Devel branch, 9/4/2022, v 1.2
Plugins can add their command button to an existing button group.

### New plugin Capability
#### Devel branch, 9/1/2022, v 1.2
Added a plugin feature. A plugin defines a new command button and a new
function to implement the command.  An existing command can optionally be
overridden with a new function without adding a new button.

### Read Comma Separated Files
#### Devel branch, 8/19/2022, v 1.1b4
We can now read comma-separated files.  This is a fairly naive implementation:
columns can be separated by comma characters.  There is no flexibility; either
all columns are separated by tabs, or by commas.

For CSV data, GF4 will try to get column names from the first non-numeric line
immediately before the first line that contains only numerical columns.

