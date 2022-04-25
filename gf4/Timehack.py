"""Draw vertical marker at specified x-axis position.

This method will be imported by the PlotManager class, hence
the use of the "self" argument.
"""
from colors import CORNFLOWERBLUE
from Linestyle import LINETHIN

def timehack(self, x=118):
    """Draw vertical line at the specified location on the x-axis.

    Used to mark a specific x-axis value.
    """
    ax = self.axes
    # This calculation could be improved.  It should use the graph pane
    # limits, but instead it uses the data limits.
    ax.plot((x, x), ax.get_ylim(), CORNFLOWERBLUE, linewidth=LINETHIN)
    self.canvas.draw()

    return 'break'
