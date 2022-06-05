#@+leo-ver=5-thin
#@+node:tom.20220511095316.1: * @file stackview.py
#@@language python
#@+others
#@+node:tom.20220511095404.1: ** imports
import tkinter as Tk

from AbstractPlotMgr import MAIN, BUFFER, STACKDEPTH

TOP = STACKDEPTH - 1
MONO = ('Courier', 10, 'normal')
SANS = ('sans-serif', 10, 'normal')

#@+node:tom.20220511095552.1: ** class Stackwin
class Stackwin(Tk.Toplevel):

    #@+others
    #@+node:tom.20220511233803.1: *3* __init__
    def __init__(self, plotmgr = None):
        if plotmgr:
            self.parent = parent = plotmgr.root
        else:
            parent = None

        _geom = ''
        Tk.Toplevel.__init__(self, parent)
        if parent:
            self.transient(plotmgr.root)
            _geom = plotmgr.root.geometry()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.stopped = False
        self.last_stack_str = ''
        self.plotmgr = plotmgr
        self.title("Stack Contents")

        self.text_box = text_box = Tk.Text(self, padx = 15, width = 100, height = 50)
        self.text_box.height = 3  # lines
        self.text_box.pack()
        text_box.configure(font = SANS, wrap = Tk.NONE)

        if not plotmgr:
            TEXT = "This is a test\nand now for something completely different"
            text_box.insert(Tk.END, TEXT)

        self.update_idletasks()
        if plotmgr:
            plotmgr.root.update_idletasks()

        # Set initial window position in screen
        if _geom:
            #902x670+182+182
            root_dims, root_xoffset, root_yoffset = _geom.split('+')
            root_width, root_height = root_dims.split('x')
            xoffset = int(root_xoffset) + int(root_width) - 50
            yoffset = 50
            self.geometry('700x70')
            self.geometry('+%s+%s' %(xoffset, yoffset))
        else:
            self.geometry('600x100')

        if plotmgr:
            # self.timer = Timer(.5, self.getstack, [])
            # self.timer.start()
            parent.after(500, self.getstack)
        else:
            # self testing
            phrase = 'something completely'
            rng = text_box.search(phrase, '1.0')
            l1, idx_1 = rng.split('.')
            idx_1 = int(idx_1)
            print('idx_1:', idx_1)
            idx1 = f'{l1}.{idx_1}'
            idx2 = f'{l1}.{idx_1 + len(phrase)}'
            text_box.tag_add('t1', idx1, idx2)
            #text_box.tag_add('t2', rng, idx2)
            text_box.tag_config('t1', background = 'red')
            print(idx1, idx2, '===', text_box.get(idx1, idx2))
    #@+node:tom.20220604115230.1: *3* cancel
    def cancel(self):
        self.destroy()
    #@+node:tom.20220511100559.1: *3* getstack
    def getstack(self):
        if not self.plotmgr:
            return

        def set_tag(textbox, name, l, r):
            textbox.tag_add(name, l, r)
            textbox.tag_config(name, font = MONO)

        X_INTRO = 'X ==> |'
        Y_INTRO = 'Y ==> |'
        T_INTRO = 'T ==> |'
        tb = self.text_box

        stack_str = ''
        x_label = self.plotmgr.stack[MAIN].figurelabel or ''
        y_label = self.plotmgr.stack[BUFFER].figurelabel or ''
        t_label = self.plotmgr.stack[TOP].figurelabel or ''

        stack_str = (f'T ==> | {t_label}\n'
                   + f'{Y_INTRO} {y_label}\n'
                   + f'{X_INTRO} {x_label}')

        if self.stopped:
            return

        try:
            if stack_str != self.last_stack_str:
                tb['state'] = 'normal'
                tb.delete('1.0', Tk.END)
                tb.insert('1.0', stack_str)
                tb['state'] = 'disabled'
                self.last_stack_str = stack_str

                for i, phrase in enumerate((X_INTRO, Y_INTRO, T_INTRO)):
                    left = tb.search(phrase, "1.0")
                    l, idx_1 = left.split('.')
                    idx_1 = int(idx_1)
                    idx2 = idx_1 + len(phrase)
                    set_tag(tb, f't{i}', left, f'{l}.{idx2}')
            self.parent.after(500, self.getstack)
        # Tk may throw an exception if our window is closing
        except Tk._tkinter.TclError as e:
            print(e)
            # hope we don't leak resources here

    #@-others
#@-others

if __name__ == '__main__':
    Stackwin()
    Tk.mainloop()
#@-leo
