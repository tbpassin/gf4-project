### Devel branch 1.3b3
- Save/Restore plot bitmap, stack state.

    The bitmap of the plot, along with the contents of the waveform stack,
can now by saved and restored.

- Autocorrelation function now centered on zero-lag, is normalized
to 1.0.

- New exended Help facility for GF4 commands

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

