#!/usr/bin/python

""" Display the record for the most recent draft set

Relies on draft files (screenshots) being stored in
/home/will/Pictures/Screenshots/drafts, with filenames ending '{W}-{L}.{ext}'
where {W} and {L} are the number of wins/losses achieved.

Doesn't currently handle nested directories.
"""

import os
from pathlib import Path

drafts_home = Path("/home/will/Pictures/Screenshots/drafts")

def get_most_recent_folder():
    dirs_of_interest = []
    for path, dirs, files in os.walk(drafts_home):
        if not dirs:
            dirs_of_interest.append(drafts_home / path)

    return max(dirs_of_interest, key=lambda f: f.stat().st_mtime)

most_recent = get_most_recent_folder()

bits = [most_recent.name]
p = most_recent.parent
while p != drafts_home:
    bits.append(p.name)
    p = p.parent
# The bit of the path starting at drafts_home
partial_path = "/".join(reversed(bits))

fs = os.listdir(most_recent)
print(f"{partial_path}: {len(fs)} drafts")

no_ext = (f.split(".")[0] for f in fs)
splits = (f.split("-") for f in no_ext)
scores = list((int(s[-2]), int(s[-1])) for s in splits)
wins = sum((s[0] for s in scores))
losses = sum((s[1] for s in scores))
percent = (wins / (wins + losses)) * 100
print(f"{wins} - {losses} ({percent:.2f}%)")
