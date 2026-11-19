"""Head of household and qualifying surviving spouse ask their tests, on published core v98.

P0's probe returns go through live_coordinate_run, the real presentation
projection and the saved page model on published v98 (registry v96, release
v96). A head of household or qualifying surviving spouse who answers yes keeps
every number v97 gave (hand values below: wages 50,000, 4,500 withheld,
standard deduction); answered no, line 12e refuses and the page shows the
question; unanswered, the page asks it. Single, married filing jointly and
married filing separately read nothing new and keep their numbers.

Measured reason for the live marker: each live_coordinate_run with page
rendering took about 20 s, above the 3.0 s fast-lane budget.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/hoh-qualifying-person-evidence"
CONTENT = REPO / "packages/content/tax/2025"
STATUS_LINES = ("form1040.line-12e", "form1040.line-16", "form1040.line-34", "form1040.line-35a")
# (line 12e, line 16, line 34) for wages 50,000 with 4,500 withheld, from the 2025 tables.
KEPT = {
    "hoh/none": (23625, 2825, 1675),
    "hoh/child": (23625, 2825, 3940),
    "hoh/relative": (23625, 2825, 2175),
    "qss/none": (31500, 1853, 2647),
    "qss/child": (31500, 1853, 4912),
}
CONTROLS = {
    "single/none": (15750, 3875, 625),
    "mfj/none": (31500, 1853, 2647),
}


@lru_cache(maxsize=1)
def _probe() -> Any:
    probe = evidence_loader.load(EVIDENCE / "probe.py", "hoh_t1_probe")
    probe.STATUS.setdefault("mfs", "married_filing_separately")
    return probe


@lru_cache(maxsize=1)
def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "design.py", "hoh_t1_design")


@lru_cache(maxsize=None)
def _run(key: str, answer: str = "none") -> dict[str, Any]:
    probe = _probe()
    core = probe.h.Core("v98", "v96", "v96")
    assert core.package_path.name == "package.core-calculations.v98.json"
    return dict(probe.observe(core, key, answer))


def _line(run: dict[str, Any], name: str) -> tuple[Any, Any]:
    row = run["lines"][name]
    return row["disposition"], row["value"]


def _expected_question(key: str) -> str:
    design = _design()
    return str(design.HOH_QUESTION if key.startswith("hoh/") else design.QSS_QUESTION)


def test_the_published_questions_carry_the_designed_wording() -> None:
    import json

    design = _design()
    for name, wording in (("hoh-tests-met", design.HOH_QUESTION), ("qss-tests-met", design.QSS_QUESTION)):
        body = json.loads((CONTENT / f"input-question.{name}.v1.json").read_text(encoding="utf-8"))
        assert body["question"] == wording
        assert body["fact_type"]["id"] == f"tax.us.2025.{name.replace('-tests-met', '.tests-met')}"


@pytest.mark.parametrize("key", sorted(KEPT))
def test_answered_yes_keeps_the_v97_numbers(key: str) -> None:
    run = _run(key, "yes")
    deduction, tax, refund = KEPT[key]
    assert run["stop"] == "saturated"
    assert run["blocked_rules"] == []
    assert _line(run, "form1040.line-12e") == ("published_value", deduction)
    assert _line(run, "form1040.line-16") == ("published_value", tax)
    assert _line(run, "form1040.line-34") == ("published_value", refund)
    assert _line(run, "form1040.line-35a") == ("published_value", refund)
    assert not any(_expected_question(key) in s for s in run["sentences"])


@pytest.mark.parametrize("key", ("hoh/none", "hoh/child", "qss/none", "qss/child"))
def test_answered_no_refuses_line_12e_and_shows_the_question(key: str) -> None:
    run = _run(key, "no")
    assert run["stop"] == "saturated"
    assert _line(run, "form1040.line-12e") == ("blocked", None)
    for name in ("form1040.line-16", "form1040.line-34", "form1040.line-35a"):
        assert _line(run, name) == ("blocked", None), name
    assert "dependents-worksheet-line-3:DEPENDENCY_INVALID" in run["blocked_rules"]
    assert _expected_question(key) in run["sentences"]
    assert _expected_question(key) in run["lines"]["form1040.line-12e"]["said"]


@pytest.mark.parametrize("key", ("hoh/none", "hoh/child", "qss/none", "qss/child"))
def test_unanswered_asks_the_question(key: str) -> None:
    run = _run(key, "none")
    assert run["stop"] == "saturated"
    assert _line(run, "form1040.line-12e") == ("blocked", None)
    for name in ("form1040.line-16", "form1040.line-34", "form1040.line-35a"):
        assert _line(run, name) == ("blocked", None), name
    assert "dependents-worksheet-line-3:DEPENDENCY_ABSENT" in run["blocked_rules"]
    assert _expected_question(key) in run["sentences"]
    other = _design().QSS_QUESTION if key.startswith("hoh/") else _design().HOH_QUESTION
    assert other not in run["sentences"]


@pytest.mark.parametrize("key", sorted(CONTROLS))
def test_single_and_joint_read_nothing_new_and_keep_their_numbers(key: str) -> None:
    run = _run(key)
    deduction, tax, refund = CONTROLS[key]
    assert run["blocked_rules"] == []
    assert _line(run, "form1040.line-12e") == ("published_value", deduction)
    assert _line(run, "form1040.line-16") == ("published_value", tax)
    assert _line(run, "form1040.line-34") == ("published_value", refund)
    assert not any(q in s for s in run["sentences"] for q in (_design().HOH_QUESTION, _design().QSS_QUESTION))


def test_married_filing_separately_reads_nothing_new() -> None:
    """The probe's married filing separately return does not answer the two separate-return questions, so it
    stops at them on v97 and v98 alike; the two cores give the same blocked rules, lines and sentences, and
    neither new question is asked."""
    probe = _probe()
    before = dict(probe.observe(probe.h.Core("v97", "v95", "v95"), "mfs/none"))
    after = _run("mfs/none")
    assert after["blocked_rules"] == before["blocked_rules"] and after["blocked_rules"]
    assert after["lines"] == before["lines"]
    assert after["sentences"] == before["sentences"]
    assert not any(q in s for s in after["sentences"] for q in (_design().HOH_QUESTION, _design().QSS_QUESTION))
    assert not any("dependents-worksheet-line-3" in r for r in after["blocked_rules"])
