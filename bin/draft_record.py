#!/usr/bin/python

""" Display the record for the most recent draft set

Relies on draft files (screenshots) being stored in
/home/will/Pictures/Screenshots/drafts, with filenames ending '{W}-{L}.{ext}'
where {W} and {L} are the number of wins/losses achieved.

Gets drafts from the most recently updated subdirectory if no argument provided.

Provide an argument to get that specific directory.
"""

import os
import sys
from pathlib import Path

drafts_home = Path("/home/will/Pictures/Screenshots/drafts")

def get_draft_dir():
    def get_most_recent_dir(root):
        dirs_of_interest = []
        for path, dirs, files in os.walk(root):
            if not dirs:
                dirs_of_interest.append(drafts_home / path)

        return max(dirs_of_interest, key=lambda f: f.stat().st_mtime)

    if len(sys.argv) <= 1:
        return get_most_recent_dir(drafts_home)
    else:
        d = drafts_home / sys.argv[1]
        _, dirs, fs = next(os.walk(d))
        if dirs:
            return get_most_recent_dir(d)
        else:
            return d


draft_dir = get_draft_dir()

# The bit of the path starting at drafts_home
p = draft_dir.parts[len(drafts_home.parts):]

fs = os.listdir(draft_dir)
print(f"{"/".join(p)}: {len(fs)} drafts")

no_ext = (f.split(".")[0] for f in fs)
splits = (f.split("-") for f in no_ext)
scores = list((int(s[-2]), int(s[-1])) for s in splits)
wins = sum((s[0] for s in scores))
losses = sum((s[1] for s in scores))
percent = (wins / (wins + losses)) * 100
print(f"{wins} - {losses} ({percent:.2f}%)")
