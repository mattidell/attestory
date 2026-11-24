"""Track 1 replay entry. Workers import the process script, so this replaces
itself with replay.py before any pool starts.

Run: python3 track1_replay.py v102 --part <part-file-outside-repo>
     python3 track1_replay.py v102 --summarize <part> --out track1-replay.json
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

replay = Path(__file__).resolve().parent / "replay.py"
argv = [sys.executable, str(replay), *sys.argv[1:]]
if "--widened" not in argv:
    argv.append("--widened")
os.execv(sys.executable, argv)
