#@+leo-ver=5-thin
#@+node:tom.20211211171304.61: * @file logger.py
#@+others
#@+node:tom.20211211171304.62: ** Organizer: Declarations (logger.py)
FNAME = r'c:\test\gf4.log'

#@+node:tom.20211211171304.63: ** logit (logger.py)
def logit(txt):
    f = open(FNAME, 'a')
    f.write(txt + '\n')
    f.close()
#@-others
#@@language python
#@@tabwidth -4
#@-leo
