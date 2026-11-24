"""Live coordinator credits for Step 3 question 3 on core v103.

Every traced case matches a hand credit from the 2025 table and the asked
flags. A recorded separated-spouse yes still passes without the new answer.
A recorded no from a head of household with a qualifying child asks the new
question. The run goes through live_coordinate_run.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from packages.derivation.live import live_coordinate_run
from tests import evidence_loader

EVIDENCE = Path(__file__).resolve().parents[1] / "docs/phases/engine-breadth/milestones/eic-separated-married-evidence"
probe = evidence_loader.load(EVIDENCE / "probe_p0b.py", "esm_t1_live_probe")
hand = evidence_loader.load(EVIDENCE / "hand.py", "esm_t1_live_hand")


def _core() -> Any:
    return probe.h.Core("v103", "v101", "v101")


def _matches(row: dict[str, Any], source: dict[str, Any]) -> None:
    blocked = bool(row.get("blocked_rules"))
    assert row["credit"] == source["credit"]
    assert blocked is source["blocked"]
    assert row["asked"]["separated-spouse"] is source["ask_separated"]
    assert row["asked"]["married-taxpayer"] is source["ask_married"]
    assert row["asked"]["not-married"] is source["ask_not_married"]


@pytest.mark.parametrize("key", probe.KEYS)
def test_credit_and_asked_flags_match_the_hand(key: str) -> None:
    assert live_coordinate_run is probe.live_coordinate_run
    row = probe.observe(_core(), key)
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    _matches(row, hand.expect(key))
