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
draft_folders = [c for c in drafts_home.iterdir() if c.is_dir()]
most_recent = max(draft_folders, key=lambda f: f.stat().st_mtime)

fs = os.listdir(most_recent)
print(f"{most_recent.name}: {len(fs)} drafts")

no_ext = (f.split(".")[0] for f in fs)
splits = (f.split("-") for f in no_ext)
scores = list((int(s[-2]), int(s[-1])) for s in splits)
wins = sum((s[0] for s in scores))
losses = sum((s[1] for s in scores))
percent = (wins / (wins + losses)) * 100
print(f"{wins} - {losses} ({percent:.2f}%)")
