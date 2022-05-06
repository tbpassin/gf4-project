#@+leo-ver=5-thin
#@+node:tom.20220505114147.1: * @file gitVersion.py
#@@language python
"""Return the git branch and changset id."""

import sys
import os.path

def getGitInfo():
    branch = version = ''
    rootdir = os.path.dirname(os.path.dirname(__file__))
    gitbase = os.path.join(rootdir, '.git')

    try:
        head = os.path.join(gitbase, 'HEAD')
        with open(head) as f:
            ref, br = f.readline().split()
            branch = br.split('/')[-1]
        if ref == 'ref:':
            if sys.platform.startswith('win'):
                br = br.replace('/', '\\')
            refspath = os.path.join(gitbase, br)
            with open(refspath) as f:
                version = f.readline().strip()
    except Exception:
        pass
    return branch, version

gitInfo = getGitInfo()

if __name__ == '__main__':
    print(gitInfo)
#@-leo
