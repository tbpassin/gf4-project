#@+leo-ver=5-thin
#@+node:tom.20230203111004.1: * @file test_dialogs.py
if __name__ == '__main__':
    import os.path
    import sys
    dir_ = os.path.dirname(__file__)
    dir_ = os.path.dirname(dir_)
    sys.path.insert(0, dir_)

from tkinter import END
import entry
entry.unittesting = True

INIT = 10

#@+others
#@+node:tom.20230203131034.1: ** test_single_number_dialogs
def test_GetSingleInt():
    """GetSingleInt dialog should return an integer cast of the entry value."""
    SET = 25.5
    EXPECTED = 25
    dia = entry.GetSingleInt(None, title = '', label = 'Integer', initval = INIT)
    dia.e1.delete(0, END)
    dia.e1.insert(0, SET)
    dia.ok()

    assert isinstance(dia.result, int), 'Result should be an integer'
    assert dia.result == EXPECTED

def test_GetSingleFloat():
    """GetSingleFloat dialog should return an float cast of the entry value."""
    SET = 25
    EXPECTED = SET
    dia = entry.GetSingleFloat(None, title = '', label = 'Float', initval = INIT)
    dia.e1.delete(0, END)
    dia.e1.insert(0, SET)
    dia.ok()

    assert isinstance(dia.result, float), 'Result should be an float'
    assert dia.result == EXPECTED
#@+node:tom.20230203131249.1: ** test_two_number_dialogs
def test_GetTwoInts():
    """GetTwoIntw dialog should return integer casts of the entry values."""
    SET = 25.5
    EXPECTED1 = EXPECTED2 = 25
    dia = entry.GetTwoInts(None, title = '', label1 = 'Integer',
                label2 = 'Integer', initval1=INIT, initval2 = INIT)
    dia.e1.delete(0, END)
    dia.e1.insert(0, SET)
    dia.e2.delete(0, END)
    dia.e2.insert(0, SET)
    dia.ok()

    res1, res2 = dia.result
    assert isinstance(res1, int), 'Result should be an integer'
    assert isinstance(res2, int), 'Result should be an integer'
    assert dia.result == (EXPECTED1, EXPECTED2)

def test_GetTwoFloats():
    """GetSingleFloats dialog should return float casts of the entry value."""
    SET = 25
    EXPECTED1 = EXPECTED2 = SET
    dia = entry.GetTwoFloats(None, title = '', label1 = 'Integer',
                label2 = 'Integer', initval1=INIT, initval2 = INIT)
    dia.e1.delete(0, END)
    dia.e1.insert(0, SET)
    dia.e2.delete(0, END)
    dia.e2.insert(0, SET)
    dia.ok()

    res1, res2 = dia.result
    assert isinstance(res1, float), 'Result should be an float'
    assert isinstance(res2, float), 'Result should be an float'
    assert dia.result == (EXPECTED1, EXPECTED2)

def test_GetTwoNumbers():
    """GetTwoNumbers dialog should return both integers if possible, else both floats."""
    SET1, SET2 = 25, 30.3
    EXPECTED1, EXPECTED2 = float(SET1), SET2
    dia = entry.GetTwoFloats(None, title = '', label1 = 'Integer',
                label2 = 'Integer', initval1=INIT, initval2 = INIT)
    dia.e1.delete(0, END)
    dia.e1.insert(0, SET1)
    dia.e2.delete(0, END)
    dia.e2.insert(0, SET2)
    dia.ok()

    res1, res2 = dia.result

    assert isinstance(res1, float), 'Result should be a float'
    assert isinstance(res2, float), 'Result should be an float'
    assert dia.result == (EXPECTED1, EXPECTED2)
#@-others

test_GetSingleInt()
test_GetSingleFloat()
test_GetTwoInts()
test_GetTwoFloats()
test_GetTwoNumbers()
#@-leo
