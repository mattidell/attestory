"""The four earned income credit answers that had no question, on published core v100.

P0's probe returns go through live_coordinate_run, the real presentation
projection and the saved page model, on published v99 (registry v97, release
v97) and published v100 (registry v98, release v98). Where a test is about an
answer, the return leaves that answer out of the record: nothing is pre-filled
for it. Hand values use the 2025 earned income credit tables and the probe's
5% withholding (wages 7,000 -> 350 withheld; 16,000 -> 500):

- single, no children, wages 7,000: credit 537, refund 887;
- married filing jointly, no children, wages 16,000: credit 649, refund 1,149
  (the joint phase-out starts higher than the single one).

Measured reason for the live marker: each live_coordinate_run with page
rendering took about 20 s, above the 3.0 s fast-lane budget.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import pytest

from tests import evidence_loader

pytestmark = pytest.mark.live
REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/eic-answer-questions-evidence"
CONTENT = REPO / "packages/content/tax/2025"
EIC = "form1040.line-27a"
REFUND = "form1040.line-34"
# The lines the probe reads from the saved page; line 32 is covered by the "no blocked page line without a sentence" check.
BLOCKED_LINES = (EIC, "form1040.line-33", REFUND, "form1040.line-35a", "form1040.line-37")

# short name -> (fact id, question file, polarity: how the filer's yes is recorded)
ANSWERS = {
    "age": ("tax.us.2025.eic.age-25-under-65", "input-question.eic-age-25-under-65.v1.json"),
    "home": ("tax.us.2025.eic.main-home-in-us", "input-question.eic-main-home-in-us.v1.json"),
    "notdep": ("tax.us.2025.eic.not-claimable-as-dependent", "input-question.eic-not-claimable-as-dependent.v1.json"),
    "spssn": ("tax.us.2025.eic.spouse-valid-ssn", "input-question.eic-spouse-valid-ssn.v1.json"),
}
# (return, answer left out) where the answer is required, so its absence blocks the credit.
REQUIRED = {
    "age": ("single/none/7000", "qss/none/16000", "hoh/parent/7000/yes", "mfj/none/16000"),
    "home": ("single/none/7000", "qss/none/16000", "hoh/parent/7000/yes", "mfj/none/16000"),
    "notdep": ("single/none/7000", "qss/none/16000", "hoh/parent/7000/yes"),
    "spssn": ("mfj/none/16000", "mfj/child/30000"),
}
CASES = sorted((name, key) for name, keys in REQUIRED.items() for key in keys)
# (line 27a, line 34) of a return that answers everything, on v99 and on v100.
ANSWERED = {"single/none/7000": (537, 887), "mfj/none/16000": (649, 1149)}


@lru_cache(maxsize=1)
def _probe() -> Any:
    return evidence_loader.load(EVIDENCE / "probe.py", "eicq_t1_probe")


@lru_cache(maxsize=None)
def _run(key: str, removed: str, core: str) -> dict[str, Any]:
    probe = _probe()
    n = int(core[1:])
    published = probe.h.Core(core, f"v{n - 2}", f"v{n - 2}")
    assert published.package_path.name == f"package.core-calculations.{core}.json"
    return dict(probe.observe(published, key, removed))


def _question(name: str) -> str:
    """The published sentence, cut as the probe cuts a recorded sentence (300 characters)."""
    question: str = json.loads((CONTENT / ANSWERS[name][1]).read_text(encoding="utf-8"))["question"]
    return question[:300]


def _line(run: dict[str, Any], name: str) -> tuple[Any, Any]:
    row = run["lines"][name]
    return row["disposition"], row["value"]


@pytest.mark.parametrize(("name", "key"), CASES)
def test_a_missing_answer_shows_its_question_and_blocks_what_v99_blocked(name: str, key: str) -> None:
    before = _run(key, name, "v99")
    after = _run(key, name, "v100")
    for run in (before, after):
        assert run["stop"] == "saturated"
        for line in BLOCKED_LINES:
            assert _line(run, line) == ("blocked", None), line
    assert after["blocked_rules"] == before["blocked_rules"]
    assert after["missing_answers_named"] == before["missing_answers_named"] == [ANSWERS[name][0].removeprefix("tax.us.2025.")]
    # v99 blocked the same lines with no sentence at all; v100 says the question on each.
    assert not before["sentences"]
    assert before["blocked_page_lines_without_sentence"]
    assert after["blocked_page_lines_without_sentence"] == []
    assert after["sentences"] == [_question(name)]
    for line in BLOCKED_LINES:
        assert _question(name)[:160] in after["lines"][line]["said"], line


def test_several_missing_answers_show_every_question() -> None:
    run = _run("single/none/7000", "age,home,notdep", "v100")
    assert all(_line(run, line) == ("blocked", None) for line in BLOCKED_LINES)
    assert run["blocked_page_lines_without_sentence"] == []
    assert sorted(run["sentences"]) == sorted(_question(n) for n in ("age", "home", "notdep"))
    run = _run("mfj/none/16000", "age,home,spssn", "v100")
    assert run["blocked_page_lines_without_sentence"] == []
    assert sorted(run["sentences"]) == sorted(_question(n) for n in ("age", "home", "spssn"))


@pytest.mark.parametrize("key", sorted(ANSWERED))
def test_an_answered_return_computes_exactly_as_v99(key: str) -> None:
    before = _run(key, "-", "v99")
    after = _run(key, "-", "v100")
    assert after["stop"] == "saturated" and after["blocked_rules"] == []
    assert (_line(after, EIC)[1], _line(after, REFUND)[1]) == ANSWERED[key]
    assert after["lines"] == before["lines"]
    assert after["symbols"] == before["symbols"]
    assert after["sentences"] == before["sentences"] == []


@pytest.mark.parametrize("key", ("single/none/50000", "mfs/none/7000", "single/child/30000", "hoh/parent/7000/no"))
def test_answers_that_are_not_required_are_not_asked(key: str) -> None:
    """Credit zero anyway, married filing separately, a counted child, or a married head of household: nothing is asked."""
    before = _run(key, "age,home,notdep", "v99")
    run = _run(key, "age,home,notdep", "v100")
    assert run["blocked_rules"] == before["blocked_rules"] == []
    assert run["sentences"] == before["sentences"] == []
    assert run["lines"] == before["lines"]


def _run_recording_dependent(value: str) -> dict[str, Any]:
    """A single filer with every answer given, the dependent fact recorded as ``value`` (what the filer's answer records)."""
    probe = _probe()
    original = probe.build
    fact = probe.FACTS["notdep"] + "|"

    def build(key: str, removed: str, content: Any = probe.h.CONTENT) -> Any:
        acts = original(key, removed, content)
        hit = 0
        for act in acts:
            finding = (act.get("payload") or {}).get("finding") or {}
            if str(finding.get("fact_id", "")).startswith(fact):
                finding["value"] = value
                hit += 1
        assert hit == 1
        return acts

    probe.build = build
    try:
        core = probe.h.Core("v100", "v98", "v98")
        return dict(probe.observe(core, "single/none/7000", "-"))
    finally:
        probe.build = original


def test_dependent_question_polarity_live() -> None:
    """EAQ-R2: "can you be claimed" answered yes records not-claimable = no, which stops the credit; no continues it.

    The question's text is pinned in the package test; here the fact value each answer records is run through
    the real coordinator and page.
    """
    stopped = _run_recording_dependent("no")  # what a filer's "yes, I can be claimed" records
    assert stopped["stop"] == "saturated" and stopped["blocked_rules"] == []
    assert _line(stopped, EIC) == ("computed_zero", 0)
    assert _line(stopped, REFUND) == ("published_value", 350)  # withholding only, no credit
    continued = _run_recording_dependent("yes")  # what "no, I cannot be claimed" records
    assert _line(continued, EIC) == ("published_value", 537)
    assert _line(continued, REFUND) == ("published_value", 887)
