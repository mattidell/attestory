"""The earned income credit for a head of household, on published core v99.

P0's probe returns go through live_coordinate_run, the real presentation
projection and the saved page model on published v99 (registry v97, release
v97). Hand values use the 2025 earned income credit tables and the probe's
5% withholding (wages 7,000 -> 350 withheld; 16,000 -> 500; 30,000 -> 500):

- no-child credit, single amounts: wages 7,000 -> 537, wages 16,000 -> 236,
  and married filing jointly at 16,000 -> 649 (its phase-out starts higher);
- a head of household with no counted child answering yes gets the single
  amounts (line 27a 537 / 236, refund 887 / 736); answering no gets $0
  (refund 350 / 500, the withholding); unanswered, line 27a and every line
  downstream block and the page asks the question;
- a head of household with a counted child is unchanged (2,389 at 7,000,
  3,261 at 30,000);
- single, married filing jointly, qualifying surviving spouse and married
  filing separately read nothing new and keep their numbers.

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
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/hoh-eic-evidence"
CONTENT = REPO / "packages/content/tax/2025"
EIC = "form1040.line-27a"
REFUND = "form1040.line-34"
DOWNSTREAM = (EIC, REFUND, "form1040.line-35a")
RULE_BLOCKED = "eic-answer.not-married:DEPENDENCY_ABSENT"

# (line 27a, line 34) for the no-counted-child head of household who answers yes: the single amounts.
YES = {"hoh/parent/7000": (537, 887), "hoh/parent/16000": (236, 736),
       "hoh/oldchild/7000": (537, 887), "hoh/oldchild/16000": (236, 736)}
# (line 27a, line 34) for the same returns answering no: $0 credit, only the withholding refunds.
NO = {"hoh/parent/7000": (0, 350), "hoh/parent/16000": (0, 500),
      "hoh/oldchild/7000": (0, 350), "hoh/oldchild/16000": (0, 500)}
KEPT = {"hoh/child/7000": (2389, 3414), "hoh/child/30000": (3261, 5323)}
CONTROLS = {"single/none/7000": (537, 887), "single/none/16000": (236, 710), "single/parent/16000": (236, 736),
            "single/child/30000": (3261, 4486), "mfj/none/16000": (649, 1149), "qss/none/16000": (236, 736),
            "mfs/none/7000": (0, 350), "mfs/child/30000": (3261, 4486)}


@lru_cache(maxsize=1)
def _probe() -> Any:
    return evidence_loader.load(EVIDENCE / "probe.py", "hoh_eic_t1_probe")


@lru_cache(maxsize=1)
def _design() -> Any:
    return evidence_loader.load(EVIDENCE / "design.py", "hoh_eic_t1_design")


@lru_cache(maxsize=None)
def _run(key: str, answer: str = "none", core: str = "v99") -> dict[str, Any]:
    probe = _probe()
    n = int(core[1:])
    published = probe.h.Core(core, f"v{n - 2}", f"v{n - 2}")
    assert published.package_path.name == f"package.core-calculations.{core}.json"
    return dict(probe.observe(published, key, answer))


def _line(run: dict[str, Any], name: str) -> tuple[Any, Any]:
    row = run["lines"][name]
    return row["disposition"], row["value"]


def _amounts(run: dict[str, Any]) -> tuple[Any, Any]:
    assert run["stop"] == "saturated"
    assert run["blocked_rules"] == []
    assert _line(run, EIC)[0] in ("published_value", "computed_zero")
    return _line(run, EIC)[1], _line(run, REFUND)[1]


def test_the_published_questions_carry_the_designed_wording() -> None:
    design = _design()
    body = json.loads((CONTENT / "input-question.eic-not-married.v1.json").read_text(encoding="utf-8"))
    assert body["question"] == design.QUESTION
    assert body["fact_type"]["id"] == "tax.us.2025.eic.not-married"
    body = json.loads((CONTENT / "input-question.eic-separated-spouse.v1.json").read_text(encoding="utf-8"))
    assert body["question"] == design.SEP_QUESTION
    assert body["fact_type"]["id"] == "tax.us.2025.eic.separated-spouse"


@pytest.mark.parametrize("key", sorted(YES))
def test_unmarried_head_of_household_without_a_counted_child_gets_the_single_amounts(key: str) -> None:
    run = _run(key, "yes")
    assert _amounts(run) == YES[key]
    assert _design().QUESTION not in run["sentences"]
    # The same wages on a single return give the same credit.
    single = _run("single/none/" + key.split("/")[2], "none")
    assert _line(single, EIC)[1] == YES[key][0]


@pytest.mark.parametrize("key", sorted(NO))
def test_married_head_of_household_without_a_counted_child_gets_zero(key: str) -> None:
    run = _run(key, "no")
    assert _amounts(run) == NO[key]
    assert _line(run, EIC)[1] == 0


def test_the_answer_changes_nothing_when_the_credit_is_zero_anyway() -> None:
    """Wages 50,000 are above every no-child amount: not asked, and $0 either way."""
    for answer in ("none", "yes", "no"):
        run = _run("hoh/parent/50000", answer)
        assert run["blocked_rules"] == []
        assert _line(run, EIC)[1] == 0
        assert _design().QUESTION not in run["sentences"]


@pytest.mark.parametrize("key", sorted(YES))
def test_unanswered_asks_the_question(key: str) -> None:
    run = _run(key, "none")
    assert run["stop"] == "saturated"
    for name in DOWNSTREAM:
        assert _line(run, name) == ("blocked", None), name
    assert RULE_BLOCKED in run["blocked_rules"]
    assert _design().QUESTION in run["sentences"]
    assert _design().QUESTION in run["lines"][EIC]["said"]


@pytest.mark.parametrize("key", ("hoh/parent/7000", "hoh/oldchild/16000"))
def test_changing_the_answer_from_yes_to_no_gives_zero(key: str) -> None:
    """The same return answered yes and then superseded by a no: the credit goes from the single amounts to $0."""
    yes = _run(key, "yes")
    changed = _run(key, "yes>no")
    assert _amounts(yes) == YES[key]
    assert _amounts(changed) == NO[key]
    assert changed["lines"] == _run(key, "no")["lines"]
    assert changed["blocked_rules"] == []


@pytest.mark.parametrize("key", sorted(KEPT))
def test_head_of_household_with_a_counted_child_is_unchanged(key: str) -> None:
    for answer in ("none", "yes", "no"):
        run = _run(key, answer)
        assert _amounts(run) == KEPT[key]
        assert not any(_design().QUESTION in s for s in run["sentences"])
    before = _run(key, "none", "v98")
    assert before["lines"] == _run(key, "none")["lines"]
    after = _run(key, "none")["symbols"]
    assert before["symbols"] == {**after, "eic.answer.not-married": None}  # the new answer publishes 1 (not required)
    assert after["eic.answer.not-married"] == 1


def test_head_of_household_with_a_counted_child_and_no_separated_spouse_answer_sees_the_question() -> None:
    key = "hoh/childnosep/7000"
    run = _run(key)
    assert run["stop"] == "saturated"
    assert _line(run, EIC) == ("blocked", None)
    assert "eic-answer.separated-spouse:DEPENDENCY_ABSENT" in run["blocked_rules"]
    assert _design().SEP_QUESTION in run["sentences"]
    assert _design().SEP_QUESTION in run["lines"][EIC]["said"]
    assert _design().QUESTION not in run["sentences"]
    # v98 blocked the same lines with no sentence at all.
    before = _run(key, "none", "v98")
    assert before["blocked_rules"] == run["blocked_rules"]
    assert not before["sentences"]
    assert not before["lines"][EIC]["said"]


@pytest.mark.parametrize("key", sorted(CONTROLS))
def test_other_statuses_keep_their_numbers_and_ask_nothing_new(key: str) -> None:
    run = _run(key)
    assert _amounts(run) == CONTROLS[key]
    assert not any(q in s for s in run["sentences"] for q in (_design().QUESTION, _design().SEP_QUESTION))
    before = _run(key, "none", "v98")
    assert before["lines"] == run["lines"]
    assert before["blocked_rules"] == run["blocked_rules"]
