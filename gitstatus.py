#!/usr/bin/python3
"""
Search current directory for git repositories and print their status.
"""

import os
import subprocess as sp
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="Directory to search for repositories.",
    nargs='?', default=os.getcwd())
args = parser.parse_args()

class col:
    RED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    GREEN = '\033[0;32m'
    PURPLE = '\033[0;35m'
    ENDC = '\033[0m'

# Patterns to parse output of git status
pattern_uptodate = re.compile('Your branch is up to date with')
pattern_nochanges = re.compile('nothing to commit, working tree clean')

for root,dirs,files in os.walk(args.dir):
    if '.git' in dirs:
        up_to_date = False
        no_changes = False

        repo_name = os.path.basename(os.path.normpath(root))
        print(col.PURPLE + repo_name + col.ENDC)

        result = sp.run(['git', 'status'], cwd=root, stdout=sp.PIPE)
        output = result.stdout.decode('utf-8')

        if pattern_uptodate.search(output):
            up_to_date = True
        if pattern_nochanges.search(output):
            no_changes = True

        if up_to_date and no_changes:
            print(col.GREEN + "Up to date with remote. Nothing to commit.\n" +
                col.ENDC)
            continue
        if not no_changes:
            print(col.RED + "Changed since last commit.\n" + col.ENDC)
            continue
        if not up_to_date:
            print(col.YELLOW + "Has changes to push to remote.\n" + col.ENDC)
            continue
