'''Open a Tk window from some other window.'''
#import Tkinter as Tk
from Tkinter import *
import tkFont

commands = None

def onclick(event): 
        w = event.widget
        w.config(relief='sunken')
        w.flash()
        w.config(relief='raised')

def enter(event): event.widget.config(bg='yellow')
def leave(event): event.widget.config(bg='white')


def add_configure_button(frame, label, command):
    b = Button(frame, text='%s' % label, command=command, bg='white',
        relief='raised', height=1)
    b.pack(fill=BOTH)
    b.bind('<Button-1>', onclick)

def messageWindow(plotmgr):
    global commands
    global runMacro

    commands = {
        'overplot': plotmgr.overplotbuff,
        'addbuff': plotmgr.addBuffer,
        'plot': plotmgr.plot,
        'swap': plotmgr.swap_data
        }
        
    BUTTONDEFS = (
      ('Plot Main',commands['plot']),  
      ('Overplot', commands['overplot']),
      ('Add Buffer', commands['addbuff']),
      (None, None), # spacer,
      ('Swap', commands['swap']),
      (None, None), # spacer,
      ('Run Macro', runMacro)
      )


    # create child window
    win = Toplevel()

    # display message
    message = "This is the child window"
    Label(win, text=message).pack()

    fr = Frame(win,  height=400, width=200)
    fr.pack_propagate(0) # don't shrink
    fr.pack()

    # quit child window and return to root window
    # the button is optional here, simply use the corner x of the child window
    bq = Button(fr, text='OK', command=win.destroy, relief='raised', height=1)
    bq.pack(fill=BOTH)
    #ht = bq.config('height')
    #pixo = ht[3]
    #print bq.winfo_reqheight ()
   

    for text, cmd in BUTTONDEFS:
        if text is None and cmd is None:  # spacer
            Frame(fr, height=10).pack()
        else:    
            add_configure_button(fr, text, cmd)

    but_ht = 35
    num_buts = len(BUTTONDEFS) + 1
    fr.config(height=but_ht*num_buts)
    win.attributes('-topmost', 1)
    win.geometry('+400+50')
    #return win


MACRO = '''
    overplot
    addbuff
    plot
    '''

def runMacro():
        global commands
        global MACRO
        commandlist = MACRO.split('\n')
        for c in commandlist:
            c = c.strip()
            if not c: continue
            if c[0] is ';' or c[0] is '#': continue
            cmd = commands.get(c, None)
            if cmd:
                cmd()
            else:
                break

        