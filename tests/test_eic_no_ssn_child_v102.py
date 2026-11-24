"""Live coordinator credits for a qualifying child without a valid SSN, on core v102.

Each traced P0 case, plus single, qualifying surviving spouse, married filing
jointly, and unmarried head of household, matches a hand credit from the 2025
table. The run goes through live_coordinate_run. Dropping the SSN test from
rule.eic-child.counts, or adding it to rule.eic-child.qualifies, changes the
credit of hoh/nossn/apart/more away from the self-only column.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from packages.derivation.live import live_coordinate_run
from tests import evidence_loader

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-no-ssn-child-evidence"
probe = evidence_loader.load(EVIDENCE / "probe.py", "ens_t1_live_probe")
hand = evidence_loader.load(EVIDENCE / "hand.py", "ens_t1_live_hand")
SSN = "demo-ens-child-ssn"
NOSSN = "demo-ens-child-nossn"


def _widened() -> list[str]:
    found = []
    for status in ("single", "qss", "mfj", "uhoh"):
        for kids in ("ssn", "nossn"):
            for sep in ("apart", "no"):
                for lived in ("more", "less"):
                    found.append(f"{status}/{kids}/{sep}/{lived}")
        found.append(f"{status}/both/apart/lm")
        found.append(f"{status}/both/apart/mm")
        found.append(f"{status}/nossn/apart/more/age-no")
    return found


KEYS = [*probe.KEYS, *_widened()]


def _core() -> Any:
    return probe.h.Core("v102", "v100", "v100")


def _run(key: str) -> Any:
    assert live_coordinate_run is probe.live_coordinate_run
    row = probe.observe(_core(), key)
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    return row


@pytest.mark.parametrize("key", KEYS)
def test_credit_matches_the_2025_table(key: str) -> None:
    row = _run(key)
    source = hand.decide(key)
    assert row["credit"] == source["credit"]
    assert row["symbols"]["eic.column-count"] == source["column"]
    assert row["symbols"]["eic.qualifying-child-present"] == source["qualifying_children"]
    assert row["symbols"]["eic.table-key"] == source["table_key"]
    asked_of = {
        "separated-spouse": "ask_separated",
        "not-married": "ask_not_married",
        "age": "ask_age",
        "main-home": "ask_main_home",
        "not-qc": "ask_not_qc",
        "not-claimable": "ask_not_claimable",
    }
    for label, field in asked_of.items():
        assert row["asked"][label] is source[field], (key, label, row["asked"], source)


def test_ssn_test_stays_on_the_amount_and_off_the_qualifying_child() -> None:
    """hoh/nossn/apart/more is the self-only column only while counts requires an SSN and qualifies does not."""
    row = _run("hoh/nossn/apart/more")
    assert row["credit"] == hand.lookup(0) == 537
    child = row["children"][NOSSN]
    assert child["eic.child.counts"] == 0
    assert child["eic.child.qualifies"] == 1
    counted = _run("hoh/ssn/apart/more")
    assert counted["credit"] == hand.lookup(1) == 2389
    assert counted["children"][SSN] == {"eic.child.counts": 1, "eic.child.qualifies": 1}
    joint = _run("mfj/nossn/apart/more")
    assert joint["credit"] == hand.lookup(0, joint=True) == 537
    assert joint["symbols"]["eic.table-key"] == "joint-0"
