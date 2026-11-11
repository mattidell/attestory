"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import cast

ROOT = repo_root()

FIXTURES = ROOT / "packages" / "sample_data" / "f1098_mortgage_interest_line12e"

def _load_fixture_adoption() -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v29-current.json").read_text("utf-8")),
    )
