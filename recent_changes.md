
### Release 1.4 12-29-2022
- Plugin names in the file use_plugins.txt can now optionally include the ".py"
extension.

- Improvements to fonts and window sizes in Linux.

- After restoring a snapshot, clicking in the plot area no longer reverts
the displayed graph to the previous one.

### Devel branch 1.4b3  12-12-2022
- Added a Help button (marked with a "?") that explains that a different hover
color indicates that extended help is available.

- Command button hover color is now different when a command has extended help
(accessed by a right mouse click) so user can know which buttons to right click on.

- Command button hover colors now work correctly in Linux as well as Windows.

- Added the ability to read entries in a .ini file.  Initially, this will allow a user to override the startup line colors for [X], [Y] plots.

- Temporary files for the extended help system are now written to the user's Downloads directory.  This works around the problem that on some Linux systems, Python's default location was not readable by the system browser.

- Fonts and command window size adjusted for better appearance in Linux.

- Some operations now set or clear error bands more sensibly.

- Least Squares Linear changed to fit with Nth degree polynomial.

### Release 1.3   11-16-2022
- Better normalization of Correlate, Convolve.

- New Plugins:
    - local polynomial regression (requires "localreg" package).
    - read out y value given x
    - simple calculator

- Improvements to Gaussian PDF, CDF waveform generators.

- Improved fitting normal CDF.

### Devel branch 1.3b3
- Save/Restore plot bitmap, stack state.

    The bitmap of the plot, along with the contents of the waveform stack,
can now by saved and restored.

- Autocorrelation function now centered on zero-lag, is normalized
to 1.0.

- New extended Help facility for GF4 commands

    Extended help for the command buttons is available by right-clicking on the buttons in the Commands window.  At this time only a few commands have help text; over time more of them will be written.

### Devel branch v1.3b2
- New "partial autocorrelation" command.

- "Phasespace" plot

    Lag can be specified (previously: only lag = 1). 

- Startup Window Location, Size, Icons

- Tweak initial vertical position of main window: 

- Improve command window fonts and window height, especially on Linux.

- Show program icon in main window.

### Devel branch v1.2
- Icons for desktop launchers

    A new _icons_ directory contains icons for Linux and Windows desktop launchers.

- Plugins command buttons

    Plugins can add their command button to an existing button group.

- New plugin Capability

    Added a plugin feature. A plugin defines a new command button and a new
    function to implement the command.  An existing command can optionally be
    overridden with a new function without adding a new button.

### Devel branch v1.1b4
- Read Comma Separated Files.

    We can now read comma-separated files.  This is a fairly naive implementation:
    columns can be separated by comma characters.  There is no flexibility; either
    all columns are separated by tabs, or by commas.

    For CSV data, GF4 will try to get column names from the first non-numeric line
    immediately before the first line that contains only numerical columns.

