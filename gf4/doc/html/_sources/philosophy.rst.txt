.. rst3: filename: philosophy

GF4's Design Philosophy
=======================

There are some definite guiding principles that underline the design of GF4.
In general, common user actions should be made as similar and simple as possible.
So for example, operations that need input for parameters from the user (such as a scale factor)
always use the same dialogs, and each operation remembers the values that were
used the last time.

The program should try to remove aggravations for the user.  So there are no
modal error message boxes.  Instead, important messages flash gently at the
bottom of the window, then fade away so the user needs to do nothing to get 
rid of them.  Since dialog boxes that flash out of existence can be annoying,
GF4 dialog boxes fade away gently (system dialogs like the file save dialog
do whatever the underlying system wants to do).

As another example of convenience for the user, GF4's parameter input dialogs accept Python 
numerical expressions so that the user may not have to calculate a value
separately.

There can be conflicts between the principles, or between the principles and
ease of programming.  GF4 tries for simplicity in programming too, but user
ease and consistency are given priority.  Many potentially interesting features 
have never been implemented because they would complicate the user interface.

