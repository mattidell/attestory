"""The four closure allowlist entries, confirmed live on the latest core (v66).

``tests/test_collect_closure_regression.py`` allows Form 1099-INT box 8, Form 1099-DIV
box 7 and Form 1098-E (and the Form 1099-INT box 8 attachment path) on the static claim
that a guarded rule downstream holds each set. Here each is run: a complete current-core
return with one member recorded, once with the family's closure answered and once with it
unanswered (the closure attestation removed, the member kept). Hand-worked expectations:

- Box 8 of 100.40: Form 1040 line 2a rounds to 100. Box 7 of 50.00: Schedule 3 line 1 is 50
  (below the tax). Form 1098-E of 100.40: Schedule 1 line 21 rounds to 100.
- Unanswered, the rule that reads the subtotal blocks with SOURCE_SET_UNCLOSED; nothing it
  feeds publishes. No published value differs between the two runs (a partial amount would
  show as a changed value): every symbol is either identical or absent when unanswered.

Attachment: with a Form 1098-E in the return Schedule 1 is required, so its attachment
(``schedule1.disposition``) publishes; the same return plus an unanswered box 8 or box 7
family shows what each does to that attachment. Synthetic ``demo.*`` data only.
"""

from __future__ import annotations

import json
from decimal import Decimal
from typing import Callable

import pytest

from tests import test_collect_closure as cc
from tests.helpers import current_core_returns as c
from tests.helpers.current_core_returns import CurrentRun, P
from tests.test_withholding_closure import _strip_closure

# Each case drives the real coordinator twice through the current-core helper, which the
# conftest import scan does not see; the lane is stated here.
pytestmark = pytest.mark.live

Builder = Callable[[], list[dict[str, object]]]

ATTACHMENT = P + "schedule1.disposition"

# name -> (build the return, family, target symbol, expected answered value, rule that blocks)
ENTRIES: dict[str, tuple[Builder, str, str, str, str]] = {
    "f1099int.b8": (lambda: c.add_tax_exempt_interest_1099int(c.base_return(), [100.40]),
                    "f1099int.b8", c.LINE2A, "100", "rule.form1040-line2a"),
    "f1099div.7": (lambda: c.add_foreign_tax_1099div(c.base_return(), [50.0]),
                   "f1099div.7", c.SCH3_LINE1, "50", "rule.schedule3-line1-direct-ftc"),
    "f1098e.1": (lambda: c.add_student_loan_interest_1098e(c.base_return(), [100.40]),
                 "f1098e.1", c.SCH1_LINE21, "100", "rule.sli-worksheet"),
}


def _unanswered(acts: list[dict[str, object]], family: str) -> list[dict[str, object]]:
    closure = cc._package_index()[1][P + family]["closure_fact_type"]["id"]
    return _strip_closure(list(acts), closure)


def _pair(acts: list[dict[str, object]], family: str, name: str) -> tuple[CurrentRun, CurrentRun]:
    return (c.run_current_core(acts, f"demo.ccr.live.ans.{name}"),
            c.run_current_core(_unanswered(acts, family), f"demo.ccr.live.un.{name}"))


@pytest.mark.parametrize("entry", sorted(ENTRIES))
def test_unanswered_family_publishes_no_partial_amount_on_any_line(entry: str) -> None:
    build, family, target, expected, rule = ENTRIES[entry]
    answered, unanswered = _pair(build(), family, entry)
    # Answered: a complete return, the target line publishes the hand value.
    assert answered.blocked_names() == set()
    assert answered.value(target) == Decimal(expected)
    # Unanswered: the target is held, and the rule that reads the subtotal says why.
    assert target not in unanswered.pubs
    assert (rule, "SOURCE_SET_UNCLOSED") in unanswered.blocked_names()
    # No published value moved; nothing appeared that the answered run lacks.
    assert set(unanswered.pubs) < set(answered.pubs)
    changed = {s for s in unanswered.pubs if unanswered.pubs[s]["value"] != answered.pubs[s]["value"]}
    assert changed == set()


def test_box_8_reaches_no_attachment_so_the_return_without_schedule_1_publishes_none() -> None:
    build, family, _, _, _ = ENTRIES["f1099int.b8"]
    answered, unanswered = _pair(build(), family, "b8-att")
    assert ATTACHMENT not in answered.pubs and ATTACHMENT not in unanswered.pubs
    # The box 8 amount appears in no published attachment-bearing value in either run.
    for run in (answered, unanswered):
        assert not [s for s in run.pubs if "attachment" in s and "100.4" in json.dumps(run.pubs[s]["value"])]


def test_unanswered_box_8_withholds_the_schedule_1_attachment_rather_than_changing_it() -> None:
    # Schedule 1 is required by the Form 1098-E; box 8 does not itemize on it, but the
    # unanswered box 8 reaches it through the line 2a / deduction chain and holds it whole.
    acts = c.add_tax_exempt_interest_1099int(
        c.add_student_loan_interest_1098e(c.base_return(), [100.40]), [100.40])
    answered, unanswered = _pair(acts, "f1099int.b8", "b8-sch1")
    assert ATTACHMENT in answered.pubs
    assert "f1099int.b8" not in json.dumps(answered.pubs[ATTACHMENT]["value"])
    assert ATTACHMENT not in unanswered.pubs
    assert ("rule.attachment.schedule-1", "DEPENDENCY_ABSENT") in unanswered.blocked_names()


def test_unanswered_1098e_withholds_the_schedule_1_attachment() -> None:
    # The Form 1098-E requires Schedule 1; its unanswered family holds the attachment
    # whole (the claim in the regression test's f1098e.1 comment), never a partial row.
    build, family, _, _, _ = ENTRIES["f1098e.1"]
    answered, unanswered = _pair(build(), family, "1098e-sch1")
    assert ATTACHMENT in answered.pubs
    assert ATTACHMENT not in unanswered.pubs
    assert ("rule.attachment.schedule-1", "DEPENDENCY_ABSENT") in unanswered.blocked_names()


def test_unanswered_box_7_leaves_the_schedule_1_attachment_unchanged() -> None:
    acts = c.add_foreign_tax_1099div(c.add_student_loan_interest_1098e(c.base_return(), [100.40]), [50.0])
    answered, unanswered = _pair(acts, "f1099div.7", "b7-sch1")
    assert "f1099div.7" not in json.dumps(answered.pubs[ATTACHMENT]["value"])
    assert unanswered.pubs[ATTACHMENT]["value"] == answered.pubs[ATTACHMENT]["value"]
