<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="tom.20211211170510.1"><vh>GF4 Files</vh>
<v t="tom.20220411232217.1"><vh>Administrative and License</vh>
<v t="tom.20220411133313.1"><vh>@clean Copyright_and_Authorship.txt</vh></v>
<v t="tom.20220411133954.1"><vh>@clean Software_License.txt</vh></v>
<v t="tom.20220411171338.1"><vh>@clean ABOUT.txt</vh></v>
</v>
<v t="tom.20211211170532.1"><vh>Program files</vh>
<v t="tom.20211207165051.2"><vh>@file gf4.pyw</vh></v>
<v t="tom.20211211170701.2"><vh>@file AbstractPlotMgr.py</vh></v>
<v t="tom.20211211170819.2"><vh>@file BuildCommands.py</vh></v>
<v t="tom.20211211170819.6"><vh>@file buttondefs.py</vh></v>
<v t="tom.20211211170819.23"><vh>@file colors.py</vh></v>
<v t="tom.20211211170819.26"><vh>@file createMenus.py</vh></v>
<v t="tom.20211211170819.9"><vh>@file cmdwin.py</vh></v>
<v t="tom.20211211170820.45"><vh>@file editDialog.py</vh></v>
<v t="tom.20211211170819.30"><vh>@file curve_generators.py</vh></v>
<v t="tom.20211211170820.2"><vh>@file Dataset.py</vh></v>
<v t="tom.20211211171304.2"><vh>@file entry.py</vh></v>
<v t="tom.20211211181438.12"><vh>@file fits.py</vh></v>
<v t="tom.20211211181438.2"><vh>@file fit_test.py</vh></v>
<v t="tom.20220411202149.1"><vh>@file help.py</vh></v>
<v t="tom.20211211171304.51"><vh>@file Linestyle.py</vh></v>
<v t="tom.20211211171304.65"><vh>@file MakeWaveforms.py</vh></v>
<v t="tom.20211211171913.2"><vh>@file Plot.py</vh></v>
<v t="tom.20211211171913.6"><vh>@file randnum.py</vh></v>
<v t="tom.20211211171913.12"><vh>@file smoother.py</vh></v>
<v t="tom.20220511095316.1"><vh>@file stackview.py</vh></v>
<v t="tom.20220604113315.1"><vh>@@file stackviewx.py</vh>
<v t="tom.20220604113315.2"><vh>imports</vh></v>
<v t="tom.20220604113315.3"><vh>class stackwin</vh>
<v t="tom.20220604113315.4"><vh>__init__</vh></v>
<v t="tom.20220604113315.5"><vh>__del__</vh></v>
<v t="tom.20220604113315.6"><vh>getstack</vh></v>
</v>
</v>
<v t="tom.20211211171913.40"><vh>@file stats.py</vh></v>
<v t="tom.20211211171913.51"><vh>@file Timehack.py</vh></v>
<v t="tom.20211211171913.55"><vh>@file trend.py</vh></v>
<v t="tom.20220506081351.1"><vh>@file versions.py</vh></v>
</v>
<v t="tom.20220506082557.1"><vh>Tests</vh>
<v t="tom.20211207165011.1"><vh>Smoother and Tests</vh>
<v t="tom.20211211171913.12"></v>
<v t="tom.20211206195731.2"><vh>@file test_smooth.py</vh></v>
<v t="tom.20211206205420.2"><vh>@file testing/smoother_tests.py</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="tom.20211207165011.1"></t>
<t tx="tom.20211211170510.1"></t>
<t tx="tom.20211211170532.1"></t>
<t tx="tom.20220411133313.1">The software in this GF4 project is writtten by and copyrighted by: Thomas B. Passin 2014 - 2022.
</t>
<t tx="tom.20220411133954.1">The GF4 software package is covered by the standard MIT license, reproduced below:

The MIT License (MIT)
Copyright © 2022 Thomas B. Passin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</t>
<t tx="tom.20220411171338.1">GF4 is a computer program for visualizing and processing two-dimensional data
such as X-Y and time series data. The user interface is modeled after a
reverse-polish notation (RPN) style of desk calculator, with the roles of
numbers being replaced by 2D data sets.

As in Hewlett-Packard RPN calculators, the stack bottom is called "X", the stack
position above that is called "Y", and the top of the stack is called "T". Data
sets may be pushed, popped, or rotated on the stack. GF4's stack has a depth of
three.

The main program is called "gf4.pyw".</t>
<t tx="tom.20220411232217.1"></t>
<t tx="tom.20220506082557.1"></t>
<t tx="tom.20220604113315.1">@language python
@others

if __name__ == '__main__':
    stackwin()
    Tk.mainloop()
</t>
<t tx="tom.20220604113315.2">from threading import Timer
import tkinter as Tk

from AbstractPlotMgr import MAIN, BUFFER, STACKDEPTH

TOP = STACKDEPTH - 1
MONO = ('Courier', 10, 'normal')
SANS = ('sans-serif', 10, 'normal')

</t>
<t tx="tom.20220604113315.3">class stackwin:

    @others
</t>
<t tx="tom.20220604113315.4">def __init__(self, plotmgr = None):
    _geom = ''
    self.stopped = False
    self.last_stack_str = ''
    self.plotmgr = plotmgr
    if plotmgr:
        win = Tk.Toplevel(plotmgr.root)
        win.transient(plotmgr.root)
        _geom = plotmgr.root.geometry()
    else:
        win = Tk.Tk()
    self.win = win
    win.title("Stack Contents")

    self.text_box = text_box = Tk.Text(win, padx = 15, width = 100, height = 50)
    self.text_box.pack()
    text_box.configure(font = SANS, wrap = Tk.NONE)

    if not plotmgr:
        TEXT = "This is a test\nand now for something completely different"
        text_box.insert(Tk.END, TEXT)

    win.update_idletasks()
    if plotmgr:
        plotmgr.root.update_idletasks()

    # Set initial window position in screen
    if _geom:
        #902x670+182+182
        root_dims, root_xoffset, root_yoffset = _geom.split('+')
        root_width, root_height = root_dims.split('x')
        xoffset = int(root_xoffset) + int(root_width) - 50
        yoffset = 50
        win.geometry('800x100')
        win.geometry('+%s+%s' %(xoffset, yoffset))
    else:
        win.geometry('600x100')

    if plotmgr:
        self.timer = Timer(.5, self.getstack, [])
        self.timer.start()
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
</t>
<t tx="tom.20220604113315.5">def x__del__(self):
    if self.plotmgr:
        print('__del__')
        self.stopped = True
        if hasattr(self, 'timer') and self.timer is not None:
            self.timer.cancel()

</t>
<t tx="tom.20220604113315.6">def getstack(self):
    if not self.plotmgr:
        return

    def set_tag(textbox, name, l, r):
        textbox.tag_add(name, l, r)
        textbox.tag_config(name, font = MONO)

    self.timer = None

    X_INTRO = 'X ==&gt; |'
    Y_INTRO = 'Y ==&gt; |'
    T_INTRO = 'T ==&gt; |'
    tb = self.text_box

    stack_str = ''
    x_label = self.plotmgr.stack[MAIN].figurelabel or ''
    y_label = self.plotmgr.stack[BUFFER].figurelabel or ''
    t_label = self.plotmgr.stack[TOP].figurelabel or ''

    stack_str = (f'T ==&gt; | {t_label}\n'
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
        self.timer = Timer(.5, self.getstack, [])
        self.timer.start()
    # Tk may throw an exception if our window is closing
    except Tk._tkinter.TclError as e:
        print(e)
        # hope we don't leak resources here
    # except Exception as e:
        # print('Unexpected exception during stack string handling:', type(e), e)

</t>
</tnodes>
</leo_file>
