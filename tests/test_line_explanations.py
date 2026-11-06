"""Line explanation cases through live_coordinate_run and the presentation projection.

Same findings on core v77 and core v78. Values and dispositions match.
The v78 section shows the new sentence.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface
from tests.helpers import current_core_returns as ccr
from tests.test_form_1099_k_income import _handover
from tests.test_form_1099_withholding import YEAR
from tests.test_refund_or_amount_owed_track1 import _finish
from tests.test_w2g_gambling import _set_answer, _w2g_return

V77 = (
    "package.core-calculations.v77.json",
    "v77",
    "published-packages.v75.json",
    "demo.release.sli-worksheet-integration.2025.v75.json",
    "v75",
)
V78 = (
    "package.core-calculations.v78.json",
    "v78",
    "published-packages.v76.json",
    "demo.release.sli-worksheet-integration.2025.v76.json",
    "v76",
)
LINE_9 = "tax.us.2025.form1040.line-9"
LINE_13A = "tax.us.2025.form1040.line-13a"
LINE_1A_H = "tax.us.2025.schedule-d.line-1a"
LINE_7 = "tax.us.2025.schedule-d.line-7"
QBI = "tax.us.2025.qbi.no-qbi-deduction-declared"
NEW = {
    LINE_9: "Your total income: lines 1a, 2b, 3b, 4b, 6b, 7, and 8 added together.",
    LINE_13A + ":blocked": "Your qualified business income deduction has no value yet. It is waiting for whether you have a qualified business income deduction.",
    LINE_13A + ":guard": (
        "This line is computed only when you have no qualified business income, "
        "qualified REIT dividends, or publicly traded partnership income. "
        "You have not answered that question, or you said you have one."
    ),
    LINE_1A_H: "You said you have no short-term sales reported directly on Schedule D, so line 1a, column (h), is zero.",
    LINE_7: "Schedule D line 7 is zero because lines 1a, 1b, and 6 add to zero.",
}


def _run(acts: list[dict[str, object]], run_id: str, core: tuple[str, str, str, str, str]) -> dict[str, Any]:
    package_name, package_version, registry_name, release_name, release_version = core
    surface = PublicationSurface(ccr.RELEASE_DIR, ccr.CONTENT / registry_name, ccr.CONTENT)
    finished = _handover(
        _finish(
            copy.deepcopy(acts),
            package_path=ccr.CONTENT / package_name,
            package_version=package_version,
            release_path=ccr.RELEASE_DIR / release_name,
            release_version=release_version,
            note=run_id,
        ),
        surface=surface,
        reconfirm=True,
    )
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ccr.ROOT,
            authoritative_acts=finished,
            workspace_revision=len(finished),
            run_scope={"jurisdiction": "us", "year": YEAR},
            scope_user=ccr.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        assert outcome.refusal is None
        assert outcome.presentation_path is not None
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
    assert isinstance(model, dict)
    return model


def _rows(model: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    found: dict[str, list[dict[str, Any]]] = {}
    for section in model.get("sections", []):
        field = section.get("field") or {}
        citizen_id = field.get("id")
        if not isinstance(citizen_id, str):
            continue
        resolved = section.get("resolved") or {}
        disposition = resolved.get("disposition")
        key = "published_value" if disposition == "published_categorical" else disposition
        explain = ((field.get("dispositions") or {}).get(key) or {}).get("explain")
        found.setdefault(citizen_id, []).append({
            "disposition": disposition,
            "value": resolved.get("value"),
            "explain": explain,
            "version": field.get("version"),
        })
    return found


def _equal(left: dict[str, Any], right: dict[str, Any]) -> None:
    assert _rows(left).keys() == _rows(right).keys()
    for citizen_id in _rows(left):
        a, b = _rows(left)[citizen_id], _rows(right)[citizen_id]
        assert [(row["disposition"], row["value"]) for row in a] == [
            (row["disposition"], row["value"]) for row in b
        ]


def _one(model: dict[str, Any], citizen_id: str) -> dict[str, Any]:
    rows = _rows(model)[citizen_id]
    assert len(rows) == 1
    return rows[0]


def _drop(acts: list[dict[str, object]], fact_type: str) -> list[dict[str, object]]:
    kept = [
        act for act in acts
        if str(act["payload"].get("finding", {}).get("fact_id", "")).split("|")[0] != fact_type  # type: ignore[attr-defined]
    ]
    assert len(kept) < len(acts)
    return ccr._renumbered(copy.deepcopy(kept))


def test_wages_schedule_d_and_closed_empty_match_v77_and_show_the_new_sentences() -> None:
    """Wages-only, the closed-empty Schedule D lines, and Schedule D line 7.

    The wages return has no capital-sale statements. Schedule D still
    publishes: line 1a is a closed-empty zero and line 7 is a computed zero.
    """
    acts = ccr.base_return()
    old = _run(acts, "demo.le.t1.wages.v77", V77)
    new = _run(acts, "demo.le.t1.wages.v78", V78)
    _equal(old, new)
    assert _one(old, LINE_9)["explain"] == "published total income"
    assert _one(old, LINE_9)["version"] == "v1"
    income = _one(new, LINE_9)
    assert income["disposition"] == "published_value"
    assert income["value"] == 50000
    assert income["version"] == "v2"
    assert income["explain"] == NEW[LINE_9]
    empty = _one(new, LINE_1A_H)
    assert empty["disposition"] == "closure_backed_zero"
    assert empty["value"] == 0
    assert empty["explain"] == NEW[LINE_1A_H]
    assert _one(old, LINE_1A_H)["explain"] == "Closure-backed zero."
    line7 = _one(new, LINE_7)
    assert line7["disposition"] == "computed_zero"
    assert line7["value"] == 0
    assert line7["explain"] == NEW[LINE_7]


def test_unanswered_qbi_input_shows_the_new_blocked_sentence() -> None:
    acts = _drop(ccr.base_return(), QBI)
    old = _run(acts, "demo.le.t1.unanswered.v77", V77)
    new = _run(acts, "demo.le.t1.unanswered.v78", V78)
    _equal(old, new)
    row = _one(new, LINE_13A)
    assert row["disposition"] == "blocked"
    assert row["explain"] == NEW[LINE_13A + ":blocked"]


def test_qbi_guard_that_does_not_apply_shows_the_new_sentence() -> None:
    acts = copy.deepcopy(ccr.base_return())
    _set_answer(acts, QBI, "no")
    old = _run(acts, "demo.le.t1.guard.v77", V77)
    new = _run(acts, "demo.le.t1.guard.v78", V78)
    _equal(old, new)
    row = _one(new, LINE_13A)
    assert row["disposition"] == "guard_inapplicable"
    assert row["explain"] == NEW[LINE_13A + ":guard"]


LINE_1A = "tax.us.2025.form1040.line-1a"
LINE_16 = "tax.us.2025.form1040.line-16"
LINE_13B = "tax.us.2025.form1040.line-13b"
LINE_22 = "tax.us.2025.form1040.tax-after-credits"
SCH1_7 = "tax.us.2025.schedule1.line-7"
SCH1_8B = "tax.us.2025.schedule1.line-8b"
SCHD_16 = "tax.us.2025.schedule-d.line-16"
SCH3_1 = "tax.us.2025.schedule3.line-1"
SCH3_8 = "tax.us.2025.schedule3.line-8"
PARTS = "tax.us.2025.schedule1a.no-parts-ii-iv-deductions-declared"
LINE17 = "tax.us.2025.direct-ftc-scope.no-line17-schedule2-additional"
SCH3_LINE2 = "tax.us.2025.direct-ftc-scope.no-sch3-line2"
ROUND_1A = "Line 1a is zero because your Form W-2 box 1 amounts round to zero."
ROUND_7 = "Your unemployment compensation is zero because your Form 1099-G box 1 amounts round to zero."
ROUND_8B = "Your gambling winnings are zero because your Form W-2G box 1 amounts round to zero."
BLOCKED_1A = (
    "Line 1a has no value yet. It is waiting for a Form W-2 box 1 amount "
    "or confirmation that the wage record is complete."
)
BLOCKED_16 = (
    "Your tax has no value yet. It is waiting for your taxable income, your filing status, "
    "your qualified dividends and capital gain, or your covered sale proceeds."
)
BLOCKED_D16 = "Schedule D line 16 has no value yet. It is waiting for line 7 or line 15."
BLOCKED_9 = (
    "Your total income has no value yet. It is waiting for whichever of lines "
    "1a, 2b, 3b, 4b, 6b, 7, and 8 is still open."
)
BLOCKED_D7 = (
    "Schedule D line 7 has no value yet. It is waiting for whichever of lines 1a, 1b, and 6 is still open."
)
GUARD_13B = (
    "This line is computed only when you have no qualified tips, overtime, or new-car-loan interest "
    "to deduct. You have not answered that question, or you said you have one."
)
GUARD_22 = (
    "This line is computed only when you have no Form 4972 tax on line 16 and no additional tax "
    "from Schedule 2. You have not answered that question, or you said you have one."
)
GUARD_SCH3_8 = (
    "This line is computed only when you have no other nonrefundable credit on lines 2 through 6. "
    "You have not answered that question, or you said you have one."
)
GUARD_SCH3_1 = (
    "Schedule 3 line 1 shows no value because this return is not one where the foreign tax credit "
    "can be claimed without Form 1116. The questions on that page say which condition is not met."
)


def _pair(acts: list[dict[str, object]], name: str) -> dict[str, Any]:
    old = _run(acts, f"demo.le.t1.{name}.v77", V77)
    new = _run(acts, f"demo.le.t1.{name}.v78", V78)
    _equal(old, new)
    return new


def _open_wage_record(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """Drop the W-2 box 1 member and the wage-record closure."""
    kept: list[dict[str, object]] = []
    for act in acts:
        payload = act["payload"]
        if not isinstance(payload, dict):
            kept.append(act)
            continue
        finding = payload.get("finding")
        member = payload.get("member")
        fid = str(finding.get("fact_id", "")) if isinstance(finding, dict) else ""
        mfind = member.get("finding") if isinstance(member, dict) else None
        mfid = str(mfind.get("fact_id", "")) if isinstance(mfind, dict) else ""
        if fid.startswith("tax.us.2025.w2.source-closure") or mfid.startswith("tax.us.2025.w2.box1-wages"):
            continue
        kept.append(act)
    assert len(kept) < len(acts)
    return ccr._renumbered(copy.deepcopy(kept))


def _guard(fact_type: str) -> list[dict[str, object]]:
    acts = copy.deepcopy(ccr.base_return())
    _set_answer(acts, fact_type, "no")
    return acts


def test_rounded_box_amounts_say_they_round_to_zero() -> None:
    """A box 1 of 0.40 rounds to a zero. The sentence names the rounding."""
    wages = _pair(_w2g_return([], wages=0.40), "round-wages")
    row = _one(wages, LINE_1A)
    assert row["disposition"] == "computed_zero"
    assert row["value"] == 0
    assert row["explain"] == ROUND_1A
    unemployment = _pair(
        ccr._record_members(ccr.base_return(), "tax.us.2025.f1099g.1", [0.40], tag="ug"),
        "round-unemployment",
    )
    row = _one(unemployment, SCH1_7)
    assert row["disposition"] == "computed_zero"
    assert row["value"] == 0
    assert row["explain"] == ROUND_7
    gambling = _pair(_w2g_return([(0.40, None)]), "round-w2g")
    row = _one(gambling, SCH1_8B)
    assert row["disposition"] == "computed_zero"
    assert row["value"] == 0
    assert row["explain"] == ROUND_8B


def test_open_wage_record_shows_the_blocked_sentence() -> None:
    row = _one(_pair(_open_wage_record(ccr.base_return()), "open-wages"), LINE_1A)
    assert row["disposition"] == "blocked"
    assert row["explain"] == BLOCKED_1A


def test_open_covered_proceeds_show_the_blocked_sentences() -> None:
    """Removing the covered short-term proceeds closure blocks the lines that read it."""
    model = _pair(
        _drop(ccr.base_return(), "tax.us.2025.f1099b.covered-st-proceeds.source-closure"),
        "open-proceeds",
    )
    tax = _one(model, LINE_16)
    assert tax["disposition"] == "blocked"
    assert tax["explain"] == BLOCKED_16
    total = _one(model, SCHD_16)
    assert total["disposition"] == "blocked"
    assert total["explain"] == BLOCKED_D16
    income = _one(model, LINE_9)
    assert income["disposition"] == "blocked"
    assert income["explain"] == BLOCKED_9
    short_term = _one(model, LINE_7)
    assert short_term["disposition"] == "blocked"
    assert short_term["explain"] == BLOCKED_D7


def test_tips_guard_shows_what_the_filer_said() -> None:
    row = _one(_pair(_guard(PARTS), "guard-13b"), LINE_13B)
    assert row["disposition"] == "guard_inapplicable"
    assert row["explain"] == GUARD_13B


def test_tax_after_credits_guard_names_form_4972() -> None:
    row = _one(_pair(_guard(LINE17), "guard-22"), LINE_22)
    assert row["disposition"] == "guard_inapplicable"
    assert row["explain"] == GUARD_22


def test_schedule3_line8_guard_shows_what_the_filer_said() -> None:
    row = _one(_pair(_guard(SCH3_LINE2), "guard-sch3-8"), SCH3_8)
    assert row["disposition"] == "guard_inapplicable"
    assert row["explain"] == GUARD_SCH3_8


def test_schedule3_line1_guard_does_not_name_a_condition_that_holds() -> None:
    """Foreign tax of 601 is over the cap. The election is yes and the tax is above zero."""
    row = _one(_pair(ccr.add_foreign_tax_1099div(ccr.base_return(), [601.0]), "guard-sch3-1"), SCH3_1)
    assert row["disposition"] == "guard_inapplicable"
    assert row["explain"] == GUARD_SCH3_1
