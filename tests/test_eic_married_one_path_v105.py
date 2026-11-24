"""The eic-separated-married live cases on core v105.

Every case from the v103 module runs again through live_coordinate_run.
The credits and asked flags stay on the hand values. A stored inert fact
is still refused at assertion.
"""
from __future__ import annotations

from typing import Any, cast

import pytest

from packages.derivation.live import live_coordinate_run
from tests.test_eic_separated_married_v103 import _matches, hand, probe


def _core() -> Any:
    return probe.h.Core("v105", "v103", "v103")


def _row(key: str) -> dict[str, Any]:
    row = cast(dict[str, Any], probe.observe(_core(), key))
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    return row


@pytest.mark.parametrize("key", probe.KEYS)
def test_credit_and_asked_flags_match_the_hand(key: str) -> None:
    assert live_coordinate_run is probe.live_coordinate_run
    row = probe.observe(_core(), key)
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    _matches(row, hand.expect(key))


def test_spouse_died_in_2025_answers_yes_and_the_credit_stops() -> None:
    row = _row("q3-yes-no/ssn")
    assert row["credit"] == 0
    assert row["asked"]["married-taxpayer"] is True
    assert row["asked"]["separated-spouse"] is True


def test_interlocutory_decree_answers_yes_and_the_credit_stops() -> None:
    row = _row("q3-yes-no/ssn")
    assert row["credit"] == 0
    assert row["asked"]["married-taxpayer"] is True
    assert row["asked"]["separated-spouse"] is True


def test_final_decree_shared_household_answers_no_and_keeps_the_table() -> None:
    row = _row("q3-no/ssn")
    assert row["credit"] == hand.lookup(1) == 2389
    assert row["asked"]["married-taxpayer"] is True
    assert row["asked"]["separated-spouse"] is False


def test_lived_apart_and_considered_unmarried_answers_yes() -> None:
    row = _row("hoh-married/ssn/apart")
    assert row["credit"] == hand.lookup(1) == 2389
    assert row["asked"]["married-taxpayer"] is False
    assert row["asked"]["separated-spouse"] is True


def test_question_6_no_stops_the_credit_after_a_married_no() -> None:
    core = _core()
    not_qc = probe.p0.P + "eic.not-qualifying-child-of-another"
    acts = probe.h.renumber(probe.h.say(probe.build("q3-no/ssn", core.content), not_qc, "no", "esm-q6", core.content))
    row = cast(dict[str, Any], probe.run(core, acts, "q6-no/ssn"))
    assert "error" not in row and "refusal" not in row, row.get("error") or row.get("refusal")
    assert row["credit"] == 0
    assert row["asked"]["separated-spouse"] is False
    assert row["asked"]["not-qc"] is True


def test_stored_inert_fact_is_refused_with_and_without_a_separated_answer() -> None:
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
