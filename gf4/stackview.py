#@+leo-ver=5-thin
#@+node:tom.20220511095316.1: * @file stackview.py
#@@language python
#@+others
#@+node:tom.20220511095404.1: ** imports
import tkinter as Tk
# import tkinter.font as tkFont

from AbstractPlotMgr import MAIN, BUFFER, STACKDEPTH
from utility import ICONPATH, setIcon

#@+node:tom.20250924085520.1: ** declarations
TOP = STACKDEPTH - 1
MONO = ('Courier', 10, 'normal')
SANS = ('sans-serif', 10, 'normal')

X_INTRO = 'X ==> '
Y_INTRO = 'Y ==> '
T_INTRO = 'T ==> '
STO1_INTRO = 'STO 1 ==> '

MONO_TAG = 'mono'
NORMAL_TAG = 'normal'
#@+node:tom.20220511095552.1: ** class Stackwin
class Stackwin(Tk.Toplevel):

    #@+others
    #@+node:tom.20220511233803.1: *3* __init__
    def __init__(self, plotmgr = None):
        if plotmgr:
            self.parent = parent = plotmgr.root
            self.plotmgr = plotmgr
        else:
            parent = None

        _geom = ''
        Tk.Toplevel.__init__(self, parent)
        if parent:
            self.transient(parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        setIcon(self, ICONPATH)

        self.stopped = False
        self.last_stack_labels = ()
        self.title("Stack and Stored Data Sets")

        self.text_box = text_box = Tk.Text(self, padx=15, pady=4,
                                    spacing3=3, width=90, height=4)
        self.text_box.pack()

        #@+<< configure text box >>
        #@+node:tom.20250924085744.1: *4* << configure text box >>
        text_box.configure(font=SANS, wrap=Tk.NONE)
        text_box.tag_config(NORMAL_TAG, font=SANS)
        text_box.tag_config(MONO_TAG, font=MONO)

        #@-<< configure text box >>

        self.update_idletasks()
        if parent:
            parent.update_idletasks()
            _geom = parent.geometry()

        #@+<< set initial position >>
        #@+node:tom.20250924090028.1: *4* << set initial position >>
        # Set initial window position in screen
        if _geom:
            root_dims, root_xoffset, _ = _geom.split('+')
            root_width, root_height = root_dims.split('x')
            xoffset = int(root_xoffset) + int(root_width) - 70
            yoffset = 6

            self_width = self.winfo_width()  
            self_height = self.winfo_height() + 4  # extra padding at bottom
            self.geometry(f'{self_width}x{self_height}')
            self.geometry(f'+{xoffset}+{yoffset}')
        else:
            self.geometry('600x100')
        #@-<< set initial position >>

        if parent:
            parent.after(250, self.getstack)
        else:
            #@+<< self-test >>
            #@+node:tom.20250924090604.1: *4* << self-test >>
            TEXT = "This is a test\nand now for something completely different"
            text_box.insert(Tk.END, TEXT)

            phrase = 'something completely'
            rng = text_box.search(phrase, '1.0')
            l1, idx_1 = rng.split('.')
            idx_1 = int(idx_1)

            idx1 = f'{l1}.{idx_1}'
            idx2 = f'{l1}.{idx_1 + len(phrase)}'
            text_box.tag_add('t1', idx1, idx2)
            #text_box.tag_add('t2', rng, idx2)
            text_box.tag_config('t1', background = 'red')
            #@-<< self-test >>
    #@+node:tom.20220604115230.1: *3* cancel
    def cancel(self):
        self.destroy()
    #@+node:tom.20251110224102.1: *3* getstack
    def getstack(self):
        """Display stack positions and their labels."""
        if not self.plotmgr:
            return

        tb = self.text_box

        stack_labels = ()
        stack = self.plotmgr.stack

        x_label = stack[MAIN] and stack[MAIN].figurelabel or ''
        y_label = stack[BUFFER] and stack[BUFFER].figurelabel or ''
        t_label = stack[TOP] and stack[TOP].figurelabel or ''
        sto1 = self.plotmgr.storage
        sto1_label = sto1 and sto1.figurelabel or ''

        if self.stopped:
            return

        stack_labels = ((T_INTRO, t_label),
                        (Y_INTRO, y_label),
                        (X_INTRO, x_label),
                        (STO1_INTRO, sto1_label))

        try:
            if stack_labels != self.last_stack_labels:
                tb['state'] = 'normal'
                tb.delete('1.0', Tk.END)

                for stack_pos, label in stack_labels:
                    tb.insert(Tk.END, stack_pos, MONO_TAG)
                    tb.insert(Tk.END, label + '\n', NORMAL_TAG)
                tb['state'] = 'disabled'
                self.last_stack_labels = stack_labels

            self.parent.after(250, self.getstack)
        # Tk may throw an exception if our window is closing
        except Tk._tkinter.TclError:
            ...
            #print(e)

    #@-others
#@-others

if __name__ == '__main__':
    Stackwin()
    Tk.mainloop()
#@-leo
