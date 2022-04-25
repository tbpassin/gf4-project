FNAME = r'c:\test\gf4.log'

def logit(txt):
    f = open(FNAME, 'a')
    f.write(txt + '\n')
    f.close()
