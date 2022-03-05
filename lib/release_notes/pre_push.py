#!/usr/bin/env python

import os
import sys

from git import Repo
import re
from release_notes import sections_data

if os.getenv("CHECK_COMMIT_FORMAT"):
    sections = {k: re.compile(v, flags=re.M) for k, v in sections_data.items()}

    remote = sys.argv[1]  # origin
    url = sys.argv[2]  # git@github.com:jalbertcruz/releases.git
    params = sys.stdin.readlines()[0].strip().split(" ")

    local_ref = params[0]  # 'refs/heads/dev'
    local_oid = params[1]  # local commit sha
    # local_oid =  "" # local commit sha
    remote_ref = params[2]  # 'refs/heads/dev'
    remote_oid = params[3]  # remote commit sha
    # remote_oid =  "" # remote commit sha

    repo = Repo(".")
    rev = f"{remote_oid}..{local_oid}"
    ok = False
    for commit in repo.iter_commits(rev=rev):
        temp = False
        for k, v in sections.items():
            res = re.findall(v, commit.message)
            if len(res) > 0:
                ok = True
                temp = True
        if not temp:
            print(
                f"The commit '{commit.hexsha[:6]}' do not has its message in the correct format"
            )
    if not ok:
        sys.exit(1)


def put_as_pre_push_githook():
    import shutil

    shutil.copy(__file__, ".git/hooks/")
    shutil.move(".git/hooks/pre_push.py", ".git/hooks/pre-push")
