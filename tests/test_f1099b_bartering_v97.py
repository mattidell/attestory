"""A Form 1099-B box 13 bartering amount is not lost, on published core v97.

P0's nine probe returns go through live_coordinate_run, the real presentation
projection and the saved page model, once each on published v97 (registry v95,
release v95). The engine cannot see box 13 (no fact type carries it), so the
filer's honest answers decide the outcome: answered no, the return computes
exactly as a return with no Form 1099-B; answered yes (or left unanswered) the
return refuses at Schedule 1 line 10 and the page asks the new sentence.

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
MILESTONES = REPO / "docs/phases/engine-breadth/milestones"
EVIDENCE = MILESTONES / "f1099b-bartering-evidence"
SENTENCE = ("Also answer yes if a Form 1099-B you received shows an amount above zero in box 13 (Bartering), "
            "even if you do not think of it as a business.")
COMPUTES = ("alone/as-asked", "zero/as-asked", "control/base", "sale/as-asked")
REFUSES = ("alone/business", "alone/business-all", "alone/other-income", "sale/business")
REFUSED_LINES = ("form1040.line-8", "form1040.line-9", "form1040.line-34", "form1040.line-37")


@lru_cache(maxsize=1)
def _probe() -> Any:
    return evidence_loader.load(EVIDENCE / "probe.py", "bart_t1_probe")


@lru_cache(maxsize=None)
def _run(key: str) -> dict[str, Any]:
    probe = _probe()
    core = probe.h.Core("v97", "v95", "v95")
    assert core.package_path.name == "package.core-calculations.v97.json"
    return dict(probe.observe(core, key))


def _line(run: dict[str, Any], name: str) -> tuple[Any, Any]:
    row = run["lines"][name]
    return row["disposition"], row["value"]


def test_the_probe_names_the_nine_returns() -> None:
    assert set(_probe().KEYS) == set(COMPUTES) | set(REFUSES) | {"alone/unanswered"}


@pytest.mark.parametrize("key", COMPUTES)
def test_box_13_answered_no_still_computes_as_the_questions_are_worded(key: str) -> None:
    run = _run(key)
    assert run["stop"] == "saturated"
    assert run["blocked_rules"] == []
    assert run["reason_sentences"] == []
    assert _line(run, "schedule1.line-10") == ("computed_zero", 0)
    assert run["attachments"]["schedule-1"] == "guard_inapplicable"
    if key == "sale/as-asked":
        assert _line(run, "form1040.line-9") == ("published_value", 70000)
        assert _line(run, "form1040.line-37") == ("published_value", 2355)
    else:
        assert _line(run, "form1040.line-9") == ("published_value", 50000)
        assert _line(run, "form1040.line-34") == ("published_value", 625)
        assert _line(run, "form1040.line-37") == ("computed_zero", 0)


def test_a_box_13_statement_answered_no_equals_a_return_with_no_form_1099b() -> None:
    control = _run("control/base")
    for key in ("alone/as-asked", "zero/as-asked"):
        assert _run(key)["lines"] == control["lines"]


@pytest.mark.parametrize("key", REFUSES)
def test_box_13_answered_yes_refuses_line_10_and_blocks_lines_8_through_37(key: str) -> None:
    run = _run(key)
    assert run["stop"] == "saturated"
    assert _line(run, "schedule1.line-10") == ("guard_inapplicable", None)
    for name in REFUSED_LINES:
        assert _line(run, name) == ("blocked", None), name
    assert run["blocked_rules"], key
    assert run["guard_sentences"]["schedule1.line-10"]


def test_box_13_unanswered_shows_the_new_sentence_on_the_page() -> None:
    run = _run("alone/unanswered")
    assert _line(run, "schedule1.line-10") == ("blocked", None)
    for name in REFUSED_LINES:
        assert _line(run, name) == ("blocked", None), name
    questions = [s for s in run["reason_sentences"] if SENTENCE in s]
    assert questions and all(s.startswith("In 2025, did you receive alimony, or have income or loss") for s in questions)
    for answered in COMPUTES:
        assert not any(SENTENCE in s for s in _run(answered)["reason_sentences"])
