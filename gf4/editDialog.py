#@+leo-ver=5-thin
#@+node:tom.20211211170820.45: * @file editDialog.py
"""A dialog with an editing pane, an accept button, and a cancel button.
When closed, returns the text of the editing pane or an empty string.
"""
# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211170820.46: ** Imports
#import Tkinter as Tk
try:
    import Tkinter as Tk
except:
    import tkinter as Tk

#@+node:tom.20211211170820.47: ** class editDialog(Tk.Toplevel)
class editDialog(Tk.Toplevel):
    # pylint: disable = too-many-ancestors
    #@+others
    #@+node:tom.20211211170820.48: *3* editDialog.__init__
    def __init__(self, parent=None, title = None):
        Tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.transient(parent)
        self.title(title)
        self.result = ''
        self.geometry('500x600+400+200')
        self.window = self

        scrollbar = Tk.Scrollbar(self)
        scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        editor = Tk.Text(self, wrap=Tk.NONE, yscrollcommand=scrollbar.set)
        editor.pack(padx=20, pady=20)#, side=Tk.LEFT, fill=Tk.BOTH )
        editor.config(height=20)
        self.editor = editor

        scrollbar.config(command=editor.yview)

        frm = Tk.Frame(self, borderwidth=5, relief=Tk.GROOVE,
                width=200, height=150)
        Tk.Button(frm, text="Accept", padx=5, command=self.accept).pack(side=Tk.LEFT)
        Tk.Button(frm, text="Cancel", padx=5, command=self.cancel).pack()
        frm.pack(pady=20)

        editor.focus_set()
        self.wait_window(self)


    #@+node:tom.20211211170820.49: *3* editDialog.accept
    def accept(self, event=None):
        self.result = self.editor.get('1.0', Tk.END)
        if self.parent:
            self.parent.focus_set()
        self.window.destroy()


    #@+node:tom.20211211170820.50: *3* editDialog.cancel
    def cancel(self, event=None):
        # put focus back to the parent window
        self.result = ''
        if self.parent: self.parent.focus_set()
        self.window.destroy()
        return ''

    #@-others
#@+node:tom.20211211170820.51: ** if __name__ == '__main__':
if __name__ == '__main__':
    editDialog('Data Input')

    Tk.mainloop()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
