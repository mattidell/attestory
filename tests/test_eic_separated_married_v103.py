"""Live coordinator credits for Step 3 question 3 on core v103.

Every traced case matches a hand credit from the 2025 table and the asked
flags. A recorded separated-spouse yes still passes without the new answer.
A recorded no from a head of household with a qualifying child asks the new
question. The run goes through live_coordinate_run.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, cast

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


def _row(key: str) -> dict[str, Any]:
    row = cast(dict[str, Any], probe.observe(_core(), key))
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    return row


def test_interlocutory_decree_answers_yes_and_the_credit_stops() -> None:
    """Question 3 yes, question 4 yes, question 5 no. The instructions stop the credit."""
    row = _row("q3-yes-no/ssn")
    assert row["credit"] == 0
    assert row["asked"]["married-taxpayer"] is True
    assert row["asked"]["separated-spouse"] is True


def test_final_decree_shared_household_answers_no_and_keeps_the_table() -> None:
    """A final decree means not married for question 3, so questions 4 and 5 are not reached."""
    row = _row("q3-no/ssn")
    assert row["credit"] == hand.lookup(1) == 2389
    assert row["asked"]["married-taxpayer"] is True
    assert row["asked"]["separated-spouse"] is False


def test_lived_apart_and_considered_unmarried_answers_yes() -> None:
    """Rule 3 still treats that head of household as married. Question 4 no keeps the table credit."""
    row = _row("hoh-married/ssn/apart")
    assert row["credit"] == hand.lookup(1) == 2389
    assert row["asked"]["married-taxpayer"] is False
    assert row["asked"]["separated-spouse"] is True


def test_question_6_no_stops_the_credit_after_a_married_no() -> None:
    """Question 3 no continues to question 6. Question 6 no does not keep the table credit."""
    core = _core()
    not_qc = probe.p0.P + "eic.not-qualifying-child-of-another"
    acts = probe.h.renumber(probe.h.say(probe.build("q3-no/ssn", core.content), not_qc, "no", "esm-q6", core.content))
    row = cast(dict[str, Any], probe.run(core, acts, "q6-no/ssn"))
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    assert row["credit"] == 0
    assert row["asked"]["separated-spouse"] is False
    assert row["asked"]["not-qc"] is True


def test_stored_inert_fact_is_refused_with_and_without_a_separated_answer() -> None:
    """A stored inert fact is refused at assertion, so it cannot block line 27a or trip two paths."""
    core = _core()
    inert = probe.p0.P + "eic.married-taxpayer-inert"
    for key in ("q3-no/ssn", "hoh-unmarried/ssn/apart"):
        legal = probe.observe(core, key)
        assert legal["credit"] == 2389
        assert "eic-married-taxpayer-two-paths" not in (legal.get("blocked_missing") or [])
        acts = probe.h.renumber(probe.h.say(probe.build(key, core.content), inert, "yes", "esm-inert", core.content))
        try:
            probe.run(core, acts, "inert-" + key)
        except Exception as exc:  # noqa: BLE001 - the assertion boundary is the result
            assert type(exc).__name__ == "FindingModelError"
            assert "eic.married-taxpayer-inert" in str(exc)
            continue
        raise AssertionError(key)
