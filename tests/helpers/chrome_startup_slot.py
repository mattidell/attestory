"""The test-session startup slot, shared with Node browser launchers.

One-shot CLI renderers expose no readiness event, so they hold the slot until
that command exits. The slot never covers model construction or the test case.
"""
from __future__ import annotations

import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


@contextmanager
def browser_startup_slot(timeout: float = 120.0) -> Iterator[None]:
    root = os.environ.get("DEMO_CHROME_STARTUP_DIR")
    if not root:
        yield
        return
    slot = Path(root) / "chrome-startup-slot"
    deadline = time.monotonic() + timeout
    while True:
        try:
            slot.mkdir()
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise RuntimeError("Chrome startup queue timed out") from None
            time.sleep(0.025)
        except OSError:
            raise RuntimeError("Chrome startup queue unavailable") from None
    try:
        yield
    finally:
        prior = sys.exc_info()[0] is not None
        try:
            slot.rmdir()
        except OSError:
            if not prior:
                raise RuntimeError("Chrome startup queue release failed") from None
