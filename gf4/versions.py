#@+leo-ver=5-thin
#@+node:tom.20220506081351.1: * @file versions.py
#@@language python
"""Return the git branch and changeset id as a tuple."""

import os.path
from subprocess import run

APPVERSION = '1.62'
ENCODING = 'utf-8'

def getGitInfo():
    branch = version = ''
    rootdir = os.path.dirname(os.path.dirname(__file__))

    # pylint: disable = subprocess-run-check
    try:
        cmd = 'git rev-parse --short HEAD'.split()
        gitlog = run(cmd, cwd=rootdir, capture_output = True)
        version = gitlog.stdout.decode(ENCODING)

        cmd = 'git branch --show-current'.split()
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
