#@+leo-ver=5-thin
#@+node:tom.20220506081351.1: * @file versions.py
#@@language python
"""Return the git branch and changeset id as a tuple."""

import os.path
from subprocess import run

APPVERSION = '1.4 b3'
ENCODING = 'utf-8'

def getGitInfo():
    branch = version = ''
    rootdir = os.path.dirname(os.path.dirname(__file__))

# pylint: disable = subprocess-run-check
    try:
        cmd = ['git', 'log']
        gitlog = run(cmd, cwd=rootdir, capture_output = True)
        log = gitlog.stdout.decode(ENCODING)[:30]
        version = log.split()[1][:9]

        cmd = 'git symbolic-ref --short HEAD'.split()
        git_result = run(cmd, cwd=rootdir, capture_output = True)
        branch = git_result.stdout.decode(ENCODING).strip()
    except Exception:
        # Most likely because git isn't available
        pass
    return branch, version

gitInfo = getGitInfo()

if __name__ == '__main__':
    print(gitInfo)

#@-leo
