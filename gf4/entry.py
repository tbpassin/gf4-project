#@+leo-ver=5-thin
#@+node:tom.20211211171304.2: * @file entry.py
# pylint: disable = consider-using-f-string
#@+others
#@+node:tom.20211211171304.3: ** Imports
'''Various data input dialogs, based on Fred Lundt's examples at

http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
'''

from __future__ import print_function

try:
    import Tkinter as Tk
except:
    import tkinter as Tk
try:
    import tkMessageBox
except:
    from tkinter import messagebox as tkMessageBox

#from math import *


#@+node:tom.20211211171304.4: ** class Dialog(Tk.Toplevel)
# pylint: disable = too-many-ancestors
class Dialog(Tk.Toplevel):
    """Base class for the dialogs.  From 
        http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
    """

    #@+others
    #@+node:tom.20211211171304.5: *3* Dialog.__init__
    def __init__(self, parent, title = None):

        Tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.result = None
        body = Tk.Frame(self)

        # pylint: disable = assignment-from-no-return
        # This method will be overridden and return a widget
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        if hasattr(self, 'geometry'):
            try:
                self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                          parent.winfo_rooty()+50))
            except:
                pass

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks
    #@+node:tom.20211211171304.6: *3* Dialog.body
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    #@+node:tom.20211211171304.7: *3* Dialog.buttonbox
    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Tk.Frame(self)

        w = Tk.Button(box, text="OK", width=10, command=self.ok, default=Tk.ACTIVE)
        w.pack(side=Tk.LEFT, padx=5, pady=5)
        w = Tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=Tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics
    #@+node:tom.20211211171304.8: *3* Dialog.ok
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.fade()
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()


    #@+node:tom.20211211171304.9: *3* Dialog.cancel
    def cancel(self, event=None):
        # put focus back to the parent window
        self.fade()
        if self.parent:
            self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    #@+node:tom.20211211171304.10: *3* Dialog.validate
    def validate(self):
        return 1 # override

    #@+node:tom.20211211171304.11: *3* Dialog.apply
    def apply(self):
        pass # override

    #@+node:tom.20211211171304.12: *3* Dialog.fade
    def fade(self):
        alpha = self.attributes('-alpha')
        while alpha > 0:
            alpha = alpha - 0.05
            self.attributes("-alpha", alpha)
            self.update()
            #time.sleep(0.02)
            self.after(1)
    #@-others
#@+node:tom.20211211171304.13: ** class TwoLineInput(Dialog)
class TwoLineInput(Dialog):
    #@+others
    #@+node:tom.20211211171304.14: *3* TwoLineInput.__init__
    def __init__(self, parent, title=''):
        Dialog.__init__(self, parent, title)

    #@+node:tom.20211211171304.15: *3* TwoLineInput.body
    def body(self, master):

        Tk.Label(master, font='size 12', text="First:").grid(row=0)
        Tk.Label(master, font='size 12', text="Second:").grid(row=1)

        self.e1 = Tk.Entry(master, font='size 12')
        self.e2 = Tk.Entry(master, font='size 12')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        # self.e1.insert(0,'0') # how to preload
        return self.e1 # initial focus

    #@+node:tom.20211211171304.16: *3* TwoLineInput.validate
    def validate(self):
        try:
            first= self.e1.get()
            second = self.e2.get()
            self.result = first, second
            return True
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal values, please try again"
            )
            return False

    #@+node:tom.20211211171304.17: *3* TwoLineInput.apply
    def apply(self):
        pass#print self.result

    #@-others
#@+node:tom.20211211171304.18: ** class GetSingleInt(Dialog)
class GetSingleInt(Dialog):
    #@+others
    #@+node:tom.20211211171304.19: *3* GetSingleInt(Dialog).__init__
    def __init__(self, parent, title='', label='Integer', initval=0):
        self.initval = initval
        self.label = label
        Dialog.__init__(self, parent, title)

    #@+node:tom.20211211171304.20: *3* GetSingleInt(Dialog).body
    def body(self, master):
        Tk.Label(master, font='size 12', text="%s:" % (self.label)).grid(row=0)
        self.e1 = Tk.Entry(master, font='size 12')
        self.e1.grid(row=0, column=1)

        self.e1.insert(0,str(self.initval)) # preload value
        #self.e1.configure(font='size 10')
        return self.e1 # initial focus

    #@+node:tom.20211211171304.21: *3* GetSingleInt(Dialog).validate
    def validate(self):
        try:
            first= int(eval(self.e1.get()))  # pylint: disable = eval-used
            self.result = first
            return True
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error',
                "Try again ...%s" % e
            )
            return False

    #@-others
#@+node:tom.20211211171304.22: ** class GetSingleFloat(GetSingleInt)
class GetSingleFloat(GetSingleInt):
    #@+others
    #@+node:tom.20211211171304.23: *3* GetSingleFloat(GetSingleInt).__init__
    def __init__(self, parent, title='', label='Float', initval=0.0):
        GetSingleInt.__init__(self, parent, title, label, float(initval))  

    #@+node:tom.20211211171304.24: *3* GetSingleFloat(GetSingleInt).validate
    def validate(self):
        try:
            first= float(eval(self.e1.get()))  # pylint: disable = eval-used
            self.result = first
            return True
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error',
                "Try again ...%s" % e
            )
            return False

    #@-others
#@+node:tom.20211211171304.25: ** class GetTwoFloats(TwoLineInput)
class GetTwoFloats(TwoLineInput):
    #@+others
    #@+node:tom.20211211171304.26: *3* GetTwoFloats(TwoLineInput).__init__
    # pylint: disable = too-many-arguments
    def __init__(self, parent, title='', label1='Float', label2='Float', 
            initval1=0.0, initval2=0.0):
        self.initval1 = initval1
        self.initval2 = initval2
        self.label1 = label1
        self.label2 = label2
        TwoLineInput.__init__(self, parent, title)

    #@+node:tom.20211211171304.27: *3* GetTwoFloats(TwoLineInput).body
    def body(self, master):
        Tk.Label(master, font='size 12', text=self.label1).grid(row=0)
        Tk.Label(master, font='size 12', text=self.label2).grid(row=1)

        self.e1 = Tk.Entry(master, font='size 12')
        self.e2 = Tk.Entry(master, font='size 12')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        self.e1.insert(0,str(self.initval1)) # preload values
        self.e2.insert(0,str(self.initval2)) 

        return self.e1 # initial focus

    #@+node:tom.20211211171304.28: *3* GetTwoFloats(TwoLineInput).validate
    def validate(self):
        self.result = None
        try:
            first= float(eval(self.e1.get()))  # pylint: disable = eval-used
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input in first parameter",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error in first parameter",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error in first parameter',
                "Try again ...%s" % e
            )
            return False

        try:
            second = float(eval(self.e2.get()))  # pylint: disable = eval-used
            self.result = first, second
            return True
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input in second parameter",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error in second parameter",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error in second parameter',
                "Try again ...%s" % e
            )
            return False
        
    #@-others
#@+node:tom.20211211171304.29: ** class GetTwoInts(TwoLineInput)
class GetTwoInts(TwoLineInput):
    #@+others
    #@+node:tom.20211211171304.30: *3* GetTwoInts(TwoLineInput).__init__
    # pylint: disable = too-many-arguments
    def __init__(self, parent, title='', label1='Integer', label2='Integer', 
            initval1=0, initval2=0):
        self.initval1 = initval1
        self.initval2 = initval2
        self.label1 = label1
        self.label2 = label2
        TwoLineInput.__init__(self, parent, title)

    #@+node:tom.20211211171304.31: *3* GetTwoInts(TwoLineInput).body
    def body(self, master):
        Tk.Label(master, font='size 12', text=self.label1).grid(row=0)
        Tk.Label(master, font='size 12', text=self.label2).grid(row=1)

        self.e1 = Tk.Entry(master, font='size 12')
        self.e2 = Tk.Entry(master, font='size 12')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        self.e1.insert(0,str(self.initval1)) # preload values
        self.e2.insert(0,str(self.initval2)) 

        return self.e1 # initial focus

    #@+node:tom.20211211171304.32: *3* GetTwoInts(TwoLineInput).validate
    def validate(self):
        self.result = None
        try:
            first= int(eval(self.e1.get()))  # pylint: disable = eval-used
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input in first parameter",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error in first parameter",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error in first parameter',
                "Try again ...%s" % e
            )
            return False

        try:
            second = int(eval(self.e2.get()))  # pylint: disable = eval-used
            self.result = first, second
            return True
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input in second parameter",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error in second parameter",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error in second parameter',
                "Try again ...%s" % e
            )
            return False

    #@-others
#@+node:tom.20211211171304.33: ** class GetTwoNumbers(TwoLineInput)
class GetTwoNumbers(TwoLineInput):
    '''Get two numbers from user.  Try to make the first an integer.
    If fail, try to make it a float.  If first is an integer,
    try to make the second an integer.  Otherwise, make second
    a float, too.
    '''
    #@+others
    #@+node:tom.20211211171304.34: *3* GetTwoNumbers(TwoLineInput).__init__
    # pylint: disable = too-many-arguments
    def __init__(self, parent, title='', label1='Integer', label2='Integer', 
            initval1=0, initval2=0):
        self.initval1 = initval1
        self.initval2 = initval2
        self.label1 = label1
        self.label2 = label2
        self.isint = True
        TwoLineInput.__init__(self, parent, title)

    #@+node:tom.20211211171304.35: *3* GetTwoNumbers(TwoLineInput).body
    def body(self, master):
        Tk.Label(master, font='size 12', text=self.label1).grid(row=0)
        Tk.Label(master, font='size 12', text=self.label2).grid(row=1)

        self.e1 = Tk.Entry(master, font='size 12')
        self.e2 = Tk.Entry(master, font='size 12')

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        self.e1.insert(0,str(self.initval1)) # preload values
        self.e2.insert(0,str(self.initval2)) 

        return self.e1 # initial focus

    #@+node:tom.20211211171304.36: *3* GetTwoNumbers(TwoLineInput).validate
    def validate(self):
        self.result = None
        try:
            first = eval(self.e1.get())  # pylint: disable = eval-used
            if not isinstance(first, int):
                first= float(first)
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input in first parameter",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error in first parameter",
                "Fix syntax"
            )
            return False
        except Exception as  e:
            tkMessageBox.showwarning(
                'Error in first parameter',
                "Try again ...%s" % e
            )
            return False

        try:
            second = eval(self.e2.get())  # pylint: disable = eval-used
            if type(second) == type(first):
                self.isint = False
                first = float(first)
                second = float(second)

            self.result = first, second
            return True

        except ValueError:
            tkMessageBox.showwarning(
                "Bad input in second parameter",
                "Illegal value, try again"
            )
            return False
        except SyntaxError:
            tkMessageBox.showwarning(
                "Syntax Error in second parameter",
                "Fix syntax"
            )
            return False
        except Exception as e:
            tkMessageBox.showwarning(
                'Error in second parameter',
                "Try again ...%s" % e
            )
            return False

    # ============================================================================
    #@-others
#@+node:tom.20211211171304.37: ** class TextFade(Tk.Text)
class TextFade(Tk.Text):
    #@+others
    #@+node:tom.20211211171304.38: *3* TextFade(Tk.Text).incr_in_range
    @staticmethod
    def incr_in_range(color, base, delta):
        if not delta or color == base: return color
        c = color + delta
        if delta > 0:
            return min(c, base)

        return max(c, base)

    #@+node:tom.20211211171304.39: *3* TextFade(Tk.Text).colr_str
    @staticmethod
    def colr_str(r, g, b):
        """Format an r,g,b color group into the right format to set a Tk.Text widget.

        The color values are each scaled to 0xff.  This is necessary because the 
        queries self.winfo_rgb(self.cget('fg')) and self.winfo_rgb(self.cget('bg'))
        return tuples that are scaled to 0xFFFF, but the method to set a color
         - configure(fg=fg_base_color_str) for example - requires them to
         be a string with values scaled to 0xFF instead.

         RETURNS
         a formatted string.
        """
        return '#{:02x}{:02x}{:02x}'.format(r//256, g//256, b//256)


    #@+node:tom.20211211171304.40: *3* TextFade(Tk.Text).fade
    def fade(self, dwell=150):        
        '''Fade text to invisibility, then delete it. Then restore
        the text color.

        ARGUMENT
        dwell -- integer dwell time for each increment
        '''

        #colr_str = lambda r,g,b: '#{:02x}{:02x}{:02x}'.format(r//256, g//256, b//256)

        # Initial color values
        r0, g0, b0  = self.winfo_rgb(self.cget('fg'))
        #rb0, gb0, bb0 = bg_base_color = self.winfo_rgb(self.cget('bg'))
        rb0, gb0, bb0 = self.winfo_rgb(self.cget('bg'))
        fg_base_color_str = TextFade.colr_str(r0, g0, b0)

        # Color increments
        delr = (rb0 - r0) // 10
        delg = (gb0 - g0) // 10
        delb = (bb0 - b0) // 10

        self.config(state=Tk.NORMAL)

        r,g,b = (r0, g0, b0)
        while not (r == rb0 and g == gb0 and b == bb0):
            r = TextFade.incr_in_range(r, rb0, delr)
            g = TextFade.incr_in_range(g, gb0, delg)
            b = TextFade.incr_in_range(b, bb0, delb)

            _color_str = TextFade.colr_str(r,g,b)
            self.config(fg=_color_str)
            self.update()
            self.after(dwell)

        self.delete(1.0, Tk.END)
        self.update()
        self.configure(fg=fg_base_color_str)
        self.update()
        self.config(state=Tk.DISABLED)

    #@+node:tom.20211211171304.41: *3* TextFade(Tk.Text).flash
    def flash(self, flashcolor):
        '''Flash text background to attract attention to a message.
        '''

        bg0_rgb = self.winfo_rgb(self.cget('bg'))
        bg0_r, bg0_g, bg0_b = bg0_rgb[0]//256, bg0_rgb[1]//256, bg0_rgb[2]//256
        # rgb_f = self.winfo_rgb(flashcolor)
        # r_f, g_f, b_f = rgb_f[0]//256, rgb_f[1]//256, rgb_f[2]//256

        # delr = 0.1*(bg0_r - r_f)
        # delg = 0.1*(bg0_g - g_f)
        # delb = 0.1*(bg0_b - b_f)

        self.config(state=Tk.NORMAL)
        bg_color_str = '#{:02x}{:02x}{:02x}'.format(bg0_r, bg0_g, bg0_b)

        for n in range(4):
            self.config(bg=flashcolor)
            self.update()
            self.after(70)
            self.config(bg=bg_color_str)
            self.update()
            self.after(70)

        self.config(state=Tk.DISABLED)
    #@-others
#@+node:tom.20211211171304.42: ** if __name__ == '__main__'
if __name__ == '__main__':

    root = Tk.Tk()
    root.option_add('*tearOff', False) #Tk specific menu option

    root.wm_title('Dialog Testbed')
    root.bind('<Alt-F4>', quit)

    tf = TextFade(root, height=7, font='size 12', bg='LightBlue')
    tf.insert(1.0, 'this is a test')
    tf.pack()

    #@+<< test defs >>
    #@+node:tom.20220402080844.1: *3* << test defs >>
    def two_line():
        dia = TwoLineInput(root, 'Test Dialog')
        print (dia.result)

    def one_line_int():
        dia = GetSingleInt(root, 'Single Line Input', 'width', 2)
        print (dia.result)

    def one_line_float():
        dia = GetSingleFloat(root, 'Single Line Input', 'width', 2)
        print (dia.result)

    def two_line_float():
        dia = GetTwoFloats(root, 'Two Line Float Input', 'width', 'height', 2.0, 3.2)
        print (dia.result)

    def two_line_int():
        dia = GetTwoInts(root, 'Two Line Float Input', 'width', 'height', 2, 3)
        print (dia.result)

    def two_number():
        dia = GetTwoNumbers(root,' Two Number Input', 'start', 'delta', 0, 1)
        print (dia.result)

    def test_flash():
        tf.flash('yellow')

    def test_fade():
        tf.fade(150)

    def test_flash_fade():
        tf.flash('yellow')
        tf.fade(150)
    #@-<< test defs >>

    mainMenu = Tk.Menu(root)
    mainMenu.add_command(label='Pop Up Dialog', command=two_line)
    mainMenu.add_command(label='Single Line Integer Dialog', command=one_line_int)
    mainMenu.add_command(label='Single Line Float  Dialog', command=one_line_float)
    mainMenu.add_command(label='Two Line Float Dialog', command=two_line_float)
    mainMenu.add_command(label='Two Line Integer Dialog', command=two_line_int)
    mainMenu.add_command(label='Two Number Dialog', command=two_number)
    mainMenu.add_command(label='Flash Test', command=test_flash)
    mainMenu.add_command(label='Fade Test', command=test_fade)
    mainMenu.add_command(label='Flash - Fade Test', command=test_flash_fade)
    root.config(menu=mainMenu)



    Tk.mainloop()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
