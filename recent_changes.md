
### Devel Branch 2.5b5  4-23-3023
- Fix "no data" bug when the last non-comment line is a ENDDATASET special comment.

### Devel Branch 1.5b4 3-23-2023
- Add command button to invert a dataset.

### Devel branch 1.5b3  3-2-2023
- Data input: Allow trailing in-line comments

### Devel branch 1.5b1 2-20-2023
- Add statsmodels to requirements

### Version 1.4 branch 12-29-2022
- Allow extension names in the use_plugins file to have or omit a 'py' extension.

- Added a few unit tests.

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
