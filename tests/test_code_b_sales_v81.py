"""Core v81 runs the code B Track 0 cases and every v80 return through the real coordinator.

v81 is package core-calculations v81, registry v79 and release v79: Form
1099-B sales whose reported basis is wrong (Form 8949 boxes A and D, code
B), and the four inherited v80 fixes of Decision 6. Every case is built by
the Track 0 harness (``codeb_track0.py``, which builds through
``codeb_prototype.py``) and run here on the published v81 through
``live_coordinate_run`` and the presentation model.

- ``case``: each Track 0 case, held to the harness's hand values and
  blocked states (``codeb_track0.check``).
- ``v80``: every v80 return Track 0 carried, with the code B answer "no".
  Form 1040 lines 15 and 16 are the v80 dollars, and the projection is the
  v80 projection except the blocked rows ``ROW_MISSING_CHANGES`` lists.
- ``neighbour``: the Decision 6 probes, held to their v81 expectations
  (``codeb_track0.check_neighbour``).

Each projection pins the lines, the attachment dispositions, the questions,
each blocked Schedule D line's reason sentences, the (disposition, code,
missing) of every row Track 0 watches and, when Form 8949 is published, the
tie-out text of each of its parts that is not zero. The table is
``tests/fixtures/code_b_sales_v81/expected.json``; ``python3
tests/test_code_b_sales_v81.py [workers]`` regenerates it. Exact duplicate
cases (the same act list) are run once, under the first name. A v80 return
whose v81 projection and v80 difference another v80 return already pins is
run when the table is regenerated and then dropped (``SAME_PROJECTION``).

Synthetic demo.* data only.
"""

from __future__ import annotations

import hashlib
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, cast

import pytest

from tests import evidence_loader

# Each case is one full live_coordinate_run (about 5 to 20 s), so the module
# is an integration test and runs in the live lane.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f8949-code-b-evidence"
EXPECTED_PATH = REPO / "tests/fixtures/code_b_sales_v81/expected.json"
PROTOTYPE_MODULE = "f8949_code_b_prototype"
TRACK0_MODULE = "f8949_code_b_track0"
P = "tax.us.2025."
GROUPS = ("case", "v80", "neighbour")
# The v80 returns whose v81 projection differs from v80's, and the rows that
# differ. Each row is blocked on both and only its missing list grows, by a
# symbol that waits on the same unclosed or refused family: the box B or E count
# (repair b_zero_proceeds), the line 1a or 8a count on Schedule D, or line 1a or
# 8a on Form 1040 line 7a (repair direct_zero_proceeds, review B1). No line,
# value, disposition or question changes.
ATTACHMENTS = ["row:attachment.f8949", "row:attachment.schedule-d"]
DIRECT = ["row:attachment.schedule-d", "row:form1040-line7a"]
ROW_MISSING_CHANGES: dict[str, list[str]] = {
    "carried_boundary_no_with_member": ATTACHMENTS, "carried_late_member_unclosed": ATTACHMENTS,
    "carried_late_yes_stale": ATTACHMENTS, "carried_yes_then_no_with_member": ATTACHMENTS,
    "v80_m_b_q1_no_with_member": ATTACHMENTS,
    "carried_covered_both_boundaries_no": DIRECT, "carried_covered_flag_corrected_to_no": DIRECT,
    "carried_covered_flag_no_path_a": DIRECT, "carried_covered_flag_no_st": DIRECT,
    "probe_a_high_direct_broker_honest": ["row:form1040-line7a"],
    "probe_a_high_direct_fixed_honest": ["row:form1040-line7a"],
    "probe_d_low_direct_broker_honest": ["row:form1040-line7a"],
}
GROWN_BY = {f"f1099b.{kind}-{term}-count" for kind in ("covered", "noncovered") for term in ("st", "lt")} | {
    "schedule-d.line-1a-gain", "schedule-d.line-8a-gain"}
# Rejected before a run: on v80 and on v81 alike.
REJECTED = {
    "a_corrected_basis_missing": "corrected_basis",
    # The sale removed while its amount rows stay: a row without its sale (ADR-0082).
    "x_remove_sale_keep_rows": "companion presence violated",
    "carried_duplicate_horizon": "horizon id already recorded",
    "carried_probe_e_basis_object_missing": "'basis' is a required property",
    "v80_c_basis_object_missing": "'basis' is a required property",
    "v80_d3_b_orphan_basis": "companion presence violated",
}
# Track 0 cases not run here: each has the same act list as the case named.
DUPLICATES = {
    "case": {"t1_stage0": "wage_q3_no"},
    "v80": {
        "v80_m_no_no": "v80_wage_q2_no", "v80_t1_stage0": "v80_wage_q2_no", "probe_wage": "v80_wage_q2_no",
        "v80_m_no_unanswered": "v80_wage_q2_unanswered", "v80_m_b_yes_no": "v80_d3_b_loss",
        "v80_m_c_8949_yes": "v80_m_c_8949_yes_pathb_no", "carried_one_wage": "carried_one_finding",
        "carried_probe_wage_one_no": "carried_one_finding",
    },
    "neighbour": {},
}
# v80 returns dropped from the table (review S7): each has the v81 projection, v80
# difference and Form 1040 lines of the return named. Regeneration runs every one
# and fails if this list no longer matches.
SAME_PROJECTION: dict[str, str] = {
    "carried_covered_flag_yes": "carried_covered_flag_corrected_to_yes",
    "carried_late_yes_reanswered": "carried_late_member_reopened",
    "carried_lt_gain": "carried_late_member_reopened",
    "carried_one_exempt_interest": "carried_one_exempt_dividend",
    "carried_one_finding": "carried_one_exempt_dividend",
    "carried_one_gambling_loss": "carried_one_exempt_dividend",
    "carried_one_itemized": "carried_one_exempt_dividend",
    "carried_one_mortgage": "carried_one_exempt_dividend",
    "carried_probe_c_unrecorded_8949_no_other_no": "carried_boundary_no_without_member",
    "carried_probe_c_unrecorded_all_no": "carried_boundary_no_without_member",
    "carried_probe_f_gain_on_e_in_class_yes": "carried_late_member_reopened",
    "carried_st_loss": "carried_probe_c_loss_on_b_in_class_yes",
    "carried_t0_8949no_old_ic_yes_q1_no": "carried_boundary_no_without_member",
    "carried_t0_q1_yes_nothing": "carried_boundary_no_without_member",
    "probe_d_low_direct_broker_no8949": "carried_covered_flag_corrected_to_yes",
    "probe_e_code_b_on_e": "carried_late_member_reopened",
    "v80_d3_b_loss": "carried_probe_c_loss_on_b_in_class_yes",
    "v80_d3_b_shared_transaction": "carried_t0_b_loss_8949_yes",
    "v80_d3_c_two_sales_one_missing": "v80_c_basis_missing",
    "v80_d3_e_basis_missing": "carried_probe_e_basis_scalar_missing",
    "v80_d3_e_proceeds_missing": "carried_probe_e_proceeds_scalar_missing",
    "v80_late_member_after_no": "v80_f_gain_q2_no_with_member",
    "v80_late_member_reanswered_yes": "v80_f_gain",
    "v80_m_b_8949_yes": "carried_t0_b_loss_8949_yes",
    "v80_m_b_old_ic_no": "carried_probe_c_loss_on_b_in_class_no",
    "v80_m_c_no_yes": "v80_c_loss",
    "v80_m_no_no_8949no": "carried_boundary_no_without_member",
    "v80_m_no_no_8949no_new_ic_yes": "carried_boundary_no_without_member",
    "v80_m_no_no_8949no_old_ic_yes": "carried_boundary_no_without_member",
    "v80_m_no_no_8949no_pathb_yes": "carried_one_exempt_dividend",
    "v80_m_no_yes_nothing": "carried_boundary_no_without_member",
    "v80_m_unanswered_no": "carried_wage_unclosed",
    "v80_m_yes_nothing_no": "carried_boundary_no_without_member",
    "v80_m_yes_nothing_no_8949no_old_ic_yes": "carried_boundary_no_without_member",
    "v80_m_yes_nothing_no_old_ic_yes": "carried_boundary_no_without_member",
    "v80_m_yes_yes_nothing": "carried_boundary_no_without_member",
    "v80_mixed_abcf_old_ic_unanswered": "v80_mixed_abcf",
    "v80_q2_yes_nothing_recorded": "carried_boundary_no_without_member",
    "v80_t1_stage1": "v80_f_gain_q2_no_with_member",
    "v80_t1_stage4": "v80_f_gain",
    "v80_t2_stage3_old_ic_no": "v80_t2_stage3",
    "v80_unrecorded_8949_no_only": "carried_probe_c_unrecorded_8949_no",
    "v80_unrecorded_out_of_class": "carried_boundary_no_without_member",
    "v80_w_b_scalar_only_on_gain": "carried_t0_b_w_scalar_only_on_gain",
    "v80_w_c_object_wash_no_row": "v80_w_c_amounts_disagree",
    "v80_w_c_scalar_only_on_gain": "v80_w_c_amounts_disagree",
    "v80_wage_q2_no": "carried_one_exempt_dividend",
}
Acts = list[dict[str, Any]]


def _load(name: str, path: Path) -> Any:
    """An evidence module, loaded once under its own name (f8949-boxes-cf retrospective)."""
    return evidence_loader.load(path, name)


def build_world() -> SimpleNamespace:
    """The Track 0 harness on the published v81 and its published vocabularies."""
    sys.path.insert(0, str(REPO))
    cbp = _load(PROTOTYPE_MODULE, EVIDENCE / "codeb_prototype.py")
    t0 = _load(TRACK0_MODULE, EVIDENCE / "codeb_track0.py")
    assert cbp.REPAIRS == set(cbp.ALL_REPAIRS)
    codeb_probe, probe = cbp.codeb_probe, cbp.probe
    codeb_probe.pin_v80()
    content = probe.CONTENT
    assert content == REPO / "packages/content/tax/2025"
    cbp.ORIGIN[:] = [content, probe.RELEASE_DIR]
    for key, name in (("st", "f1099b-code-b-st.bundle.json"), ("lt", "f1099b-code-b-lt.bundle.json"),
                      ("boundary", "schedule-d-boundary-form8949-code-b-in-class.bundle.json")):
        cbp.BUNDLES[key] = json.loads((content / name).read_text(encoding="utf-8"))
    codeb_probe.SUMMARIZE[0] = _summarizer(t0, codeb_probe.summary)
    builds: dict[str, dict[str, Callable[[], Acts]]] = {
        "case": {**cbp.new_cases(), **t0.track0_cases()},
        "v80": {name: _with_q3_no(cbp, build) for name, build in cbp.v80_world().items()},
        "neighbour": {name: _with_q3_no(cbp, build) for name, build in t0.NEIGHBOUR.items()},
    }
    return SimpleNamespace(cbp=cbp, t0=t0, builds=builds)


def _with_q3_no(cbp: Any, build: Callable[[], Acts]) -> Callable[[], Acts]:
    return lambda: cast(Acts, cbp.with_q3(build(), "no"))


def _summarizer(t0: Any, base: Callable[[Any], dict[str, Any]]) -> Callable[[Any], dict[str, Any]]:
    publishers = tuple(t0.PUBLISHERS)

    def summarize(outcome: Any) -> dict[str, Any]:
        summary = base(outcome)
        if outcome.refusal is not None:
            return summary
        report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
        model = json.loads(outcome.presentation_path.read_text(encoding="utf-8"))
        counts: dict[str, int] = {}
        for row in report.get("dispositions") or []:
            artifact = str(row.get("artifact_id", ""))
            if artifact in publishers:
                counts[artifact] = counts.get(artifact, 0) + 1
        summary["row_counts"] = counts
        reasons: dict[str, list[str]] = {}
        fields: dict[str, Any] = {}
        no_reason: list[str] = []
        for section in model.get("sections") or []:
            field = section.get("field") or {}
            resolved = section.get("resolved") or {}
            field_id = str(field.get("id") or "")
            disposition = str(resolved.get("disposition"))
            explain = str(((field.get("dispositions") or {}).get(disposition) or {}).get("explain") or "").strip()
            sentences = [str(r.get("sentence") or "").strip() for r in resolved.get("reasons") or []
                         if isinstance(r, dict)]
            if disposition == "blocked" and field_id.startswith(P + "schedule-d."):
                reasons[field_id.removeprefix(P)] = [s for s in sentences if s and not s.endswith("?")]
            if disposition == "blocked" and not explain and not any(sentences):
                no_reason.append(field_id)
            if field_id.removeprefix(P) in t0.NEIGHBOUR_FIELD.values():
                fields[field_id.removeprefix(P)] = {"disposition": disposition, "explain": explain}
        tie_outs: dict[str, str] = {}
        for group in model.get("citationGroups") or []:
            if "8949" in str(group.get("id")):
                for part in group.get("parts") or []:
                    text = str(part.get("tieOutText") or "")
                    if text and text != "Reported subtotal: 0":
                        tie_outs[str(part.get("heading"))] = text
        summary["f8949_tie_outs"] = tie_outs
        summary["reasons"] = reasons
        summary["fields"] = fields
        summary["blocked_without_reason"] = no_reason
        return summary

    return summarize


def run(world: SimpleNamespace, group: str, name: str) -> dict[str, Any]:
    world.cbp.pin("v81")
    probe = world.cbp.probe
    assert (probe.PACKAGE, probe.REGISTRY, probe.RELEASE) == (
        "package.core-calculations.v81.json", "published-packages.v79.json",
        "demo.release.sli-worksheet-integration.2025.v79.json")
    return cast(dict[str, Any], world.cbp.codeb_probe.execute(world.builds[group][name], f"demo.codeb.t1.{group}.{name}"))


PUBLISHED_ROW: list[Any] = ["published", None, []]


def projection(result: dict[str, Any]) -> dict[str, Any]:
    """The parts of a run the expectation table pins.

    ``rows`` holds each watched row that is not a plain publication, as
    (disposition, code, missing). Every other watched row the run records is
    a plain publication; ``watched_rows`` checks the run records each one.
    """
    if result.get("error"):
        return {"error": result["error"]}
    out = {key: result.get(key) for key in ("lines", "attachments", "questions", "reasons")}
    out["rows"] = {name: row for name, row in sorted((result.get("rows") or {}).items()) if row != PUBLISHED_ROW}
    # Review S6: the Form 8949 columns themselves, so a correct basis moved into column (e) is seen on the form.
    if (result.get("attachments") or {}).get("f8949") == "published":
        out["f8949_tie_outs"] = result.get("f8949_tie_outs")
    return out


def watched_rows(world: SimpleNamespace) -> set[str]:
    """Every row the harness watches, as the summary names it."""
    return {name.removeprefix(P + "rule.") for name in world.cbp.codeb_probe.WHY_ROWS}


# The rows a v81 run records and a v80 run has no publisher for.
NEW_ROWS = {
    "f1099b-code-b-st-gain", "f1099b-code-b-lt-gain", "f1099b-code-b-st-count", "f1099b-code-b-lt-count",
    "f1099b.code-b-st-txn.amounts-check", "f1099b.code-b-lt-txn.amounts-check",
    *(f"f1099b.{k}-{t}-txn.admission-check" for k in ("covered", "covered-w") for t in ("st", "lt")),
    *(f"f1099b-{k}-{t}-count" for k in ("covered", "covered-w", "noncovered") for t in ("st", "lt")),
}


def all_rows(view: dict[str, Any], recorded: set[str]) -> dict[str, Any]:
    return {**{name: PUBLISHED_ROW for name in recorded}, **(view.get("rows") or {})}


def v80_difference(v80: dict[str, Any], v81: dict[str, Any], recorded80: set[str], recorded81: set[str]) -> dict[str, Any]:
    """What the v80 run shows that the v81 run does not.

    Every pinned key whose value differs, and each v80 row whose v81 value
    differs. The v81 rows v80 has no publisher for (the code B and Track 1
    rules, ``NEW_ROWS``) are not compared.
    """
    out: dict[str, Any] = {key: v80.get(key) for key in ("error", "lines", "attachments", "questions", "reasons")
                           if v80.get(key) != v81.get(key)}
    rows80, rows81 = all_rows(v80, recorded80), all_rows(v81, recorded81)
    assert set(rows81) - set(rows80) <= NEW_ROWS, sorted(set(rows81) - set(rows80))
    rows = {name: row for name, row in rows80.items() if rows81.get(name) != row}
    if rows:
        out["rows"] = rows
    return out


def assert_sound(world: SimpleNamespace, name: str, result: dict[str, Any]) -> None:
    assert result.get("presentation_valid") is True, result.get("presentation_error")
    assert result.get("stop_reason") == "saturated"
    assert result.get("duplicate_field_ids") == []
    assert result.get("missing_lines") == [], result.get("missing_lines")
    assert result.get("blocked_without_reason") == [], (name, result.get("blocked_without_reason"))
    assert result.get("row_counts") == {artifact: 1 for artifact in world.t0.PUBLISHERS}, result.get("row_counts")
    assert set(result.get("rows") or {}) == watched_rows(world), sorted(watched_rows(world) ^ set(result.get("rows") or {}))


def _expected() -> dict[str, Any]:
    if not EXPECTED_PATH.exists():  # only while the table is being regenerated
        return {group: {} for group in GROUPS}
    return cast(dict[str, Any], json.loads(EXPECTED_PATH.read_text(encoding="utf-8")))


EXPECTED = _expected()


@pytest.fixture(scope="module")
def world() -> SimpleNamespace:
    return build_world()


def _check(world: SimpleNamespace, group: str, name: str, result: dict[str, Any]) -> None:
    if name in REJECTED:
        assert result.get("error") in ("FindingModelError", "HorizonModelError"), result
        assert REJECTED[name] in str(result.get("message")), result.get("message")
        return
    assert result.get("error") is None, result.get("message")
    assert_sound(world, name, result)
    if group == "case":
        assert world.t0.check(name, result) == {}
    elif group == "neighbour":
        assert world.t0.check_neighbour(name, result) == {}


@pytest.mark.parametrize("name", sorted(EXPECTED["case"]))
def test_v81_matches_track0(world: SimpleNamespace, name: str) -> None:
    result = run(world, "case", name)
    _check(world, "case", name, result)
    assert projection(result) == EXPECTED["case"][name]


@pytest.mark.parametrize("name", sorted(EXPECTED["v80"]))
def test_v80_returns_on_v81_under_the_code_b_no(world: SimpleNamespace, name: str) -> None:
    result = run(world, "v80", name)
    _check(world, "v80", name, result)
    assert projection(result) == EXPECTED["v80"][name]["v81"]


@pytest.mark.parametrize("name", sorted(EXPECTED["neighbour"]))
def test_decision_6_probes_on_v81(world: SimpleNamespace, name: str) -> None:
    result = run(world, "neighbour", name)
    _check(world, "neighbour", name, result)
    assert projection(result) == EXPECTED["neighbour"][name]["v81"]


def _differences(difference: dict[str, Any]) -> list[str]:
    out = [key for key in ("error", "lines", "attachments", "questions", "reasons") if key in difference]
    return out + [f"row:{row}" for row in sorted(difference.get("rows") or {})]




def test_every_v80_return_computes_the_same_on_v81() -> None:
    """The table's v80 side: the same act list run on v80 when the table was made.

    Every Form 1040 line and every line, attachment and question is v80's.
    Only the returns ``ROW_MISSING_CHANGES`` names differ, each in a blocked
    row's missing list.
    A v81 row v80 has no publisher for (the code B and Track 1 rules) is not
    compared.
    """
    changed = {}
    for name, case in EXPECTED["v80"].items():
        differences = _differences(case["v80"])
        if differences:
            changed[name] = differences
        assert case["v80_form1040"] == case["v81_form1040"], name
    assert changed == ROW_MISSING_CHANGES
    for name, rows in ROW_MISSING_CHANGES.items():
        case = EXPECTED["v80"][name]
        for row in rows:
            row = row.removeprefix("row:")
            before, after = case["v80"]["rows"][row], case["v81"]["rows"][row]
            assert before[0] == after[0] == "blocked" and before[1] == after[1], (name, row)
            assert after[2][:len(before[2])] == before[2], (name, row)
            added = after[2][len(before[2]):]
            assert len(added) == 1 and added[0] in GROWN_BY, (name, row, added)


def test_the_table_covers_every_case_once() -> None:
    assert len(EXPECTED["case"]) + len(DUPLICATES["case"]) == 99
    assert len(EXPECTED["v80"]) + len(DUPLICATES["v80"]) + len(SAME_PROJECTION) == 143
    for dropped, kept in SAME_PROJECTION.items():
        assert dropped not in EXPECTED["v80"] and kept in EXPECTED["v80"], dropped
        assert dropped not in ROW_MISSING_CHANGES and dropped not in REJECTED, dropped
    assert len(EXPECTED["neighbour"]) == 27
    for group in GROUPS:
        for duplicate, kept in DUPLICATES[group].items():
            kept = SAME_PROJECTION.get(kept, kept) if group == "v80" else kept
            assert duplicate not in EXPECTED[group] and kept in EXPECTED[group], (duplicate, kept)
    assert {name for group in GROUPS for name in EXPECTED[group] if name in REJECTED} == set(REJECTED)


def test_the_decision_6_probes_change_exactly_as_decided() -> None:
    """Each probe of the four patterns, on v80 and on v81."""
    probes = EXPECTED["neighbour"]
    published = ("published", "published")
    for name in ("n_w_zero_proceeds", "n_w_lt_zero_proceeds", "n_b_zero_proceeds", "n_e_zero_proceeds",
                 "n_b_zero_proceeds_zero_basis"):
        difference, v81 = probes[name]["v80"], probes[name]["v81"]
        assert "lines" not in difference, name
        assert tuple(difference["attachments"].values()) != published
        assert (v81["attachments"]["f8949"], v81["attachments"]["schedule-d"]) == published
    for name in ("n_dup_b_and_covered_lt", "n_dup_b_and_e", "n_dup_e_and_covered_st",
                 "n_dup_covered_st_and_covered_lt", "n_dup_w_st_and_covered_lt", "n_dup_covered_st_and_w_lt",
                 "n_dup_w_st_and_w_lt", "n_covered_tsa_yes_no8949", "n_covered_lt_tsa_yes", "n_w_st_tsa_yes",
                 "n_covered_st_ordinary_yes", "n_covered_lt_market_discount_yes", "n_covered_lt_qof_yes",
                 "n_covered_lt_collectibles_yes", "n_w_lt_collectibles_yes"):
        v80_lines = {**probes[name]["v81"]["lines"], **probes[name]["v80"]["lines"]}
        assert v80_lines["form1040.line-15"][0] == "published_value", name
        assert probes[name]["v81"]["lines"]["form1040.line-15"] == ["blocked", None], name
    for name in ("n_two_b_and_covered_lt", "n_two_covered_st_and_covered_lt", "n_two_w_st_and_w_lt",
                 "n_covered_tsa_no"):
        assert _differences(probes[name]["v80"]) == [], name
    # Review B1: v80 published Form 1040 line 7a as 0 beside a Schedule D loss, and required neither attachment.
    for name, line in (("n_covered_st_zero_proceeds", "schedule-d.line-1a"),
                       ("n_covered_lt_zero_proceeds", "schedule-d.line-8a")):
        difference, v81 = probes[name]["v80"], probes[name]["v81"]
        assert difference["lines"]["form1040.line-7a"] == ["computed_zero", 0], name
        assert v81["lines"]["form1040.line-7a"] == ["published_value", -500], name
        assert v81["lines"][line] == ["published_value", -500], name
        assert (v81["attachments"]["f8949"], v81["attachments"]["schedule-d"]) == ("guard_inapplicable", "published")
    zero = probes["n_covered_st_zero_proceeds_zero_basis"]
    assert "lines" not in zero["v80"]
    assert (zero["v81"]["attachments"]["f8949"], zero["v81"]["attachments"]["schedule-d"]) == (
        "guard_inapplicable", "published")


def test_form_8949_shows_the_basis_shown_and_the_correction() -> None:
    """Review S6: column (e) is the basis the Form 1099-B shows and column (g) the correction, on the form."""
    def parts(name: str) -> dict[str, str]:
        return cast(dict[str, str], EXPECTED["case"][name]["f8949_tie_outs"])

    assert parts("a_high") == {
        "Part I box A column (d), code B: short-term proceeds": "Reported subtotal: 10000",
        "Part I box A column (e), code B: short-term basis shown on Form 1099-B": "Reported subtotal: 7000",
        "Part I box A column (g), code B: short-term basis correction plus any wash-sale adjustment":
            "Reported subtotal: 3000",
    }
    assert parts("d_low") == {
        "Part II box D column (d), code B: long-term proceeds": "Reported subtotal: 6000",
        "Part II box D column (e), code B: long-term basis shown on Form 1099-B": "Reported subtotal: 2000",
        "Part II box D column (g), code B: long-term basis correction plus any wash-sale adjustment":
            "Reported subtotal: -1000",
    }
    assert parts("a_bw")["Part I box A column (g), code B: short-term basis correction plus any wash-sale adjustment"] \
        == "Reported subtotal: -500"


def test_a_refused_direct_sale_says_why_on_its_line() -> None:
    """Covered sales flagged yes on an eligibility flag, or recorded twice, block lines 1a and 8a.

    The rule refuses with no question (the Decision 7 limit), so the line's
    blocked text is the reason, and it names every cause and the route to code B.
    """
    for name, line in (("n_covered_tsa_yes_no8949", "schedule-d.line-1a"), ("n_covered_lt_tsa_yes", "schedule-d.line-8a"),
                       ("n_dup_covered_st_and_covered_lt", "schedule-d.line-1a"),
                       ("n_covered_st_ordinary_yes", "schedule-d.line-1a"),
                       ("n_covered_lt_collectibles_yes", "schedule-d.line-8a")):
        v81 = EXPECTED["neighbour"][name]["v81"]
        assert v81["lines"][line] == ["blocked", None], name
        assert v81["questions"] == [], name
        explain = EXPECTED["neighbour"][name]["field_explain"][line]
        for words in ("are outside what this return computes", "So is a sale with an adjustment you make yourself",
                      "ordinary income, market discount, a qualified opportunity fund investment",
                      "record that sale as a sale whose reported basis is wrong"):
            assert words in explain, (name, words)


# ---- regeneration ---------------------------------------------------------------


_WORLD: list[SimpleNamespace] = []


def _worker(task: tuple[str, str, str]) -> tuple[tuple[str, str, str], dict[str, Any]]:
    if not _WORLD:
        _WORLD.append(build_world())
    world = _WORLD[0]
    group, name, package = task
    if package == "v81":
        return task, run(world, group, name)
    world.cbp.pin("v80")
    build = world.cbp.v80_world()[name] if group == "v80" else world.t0.NEIGHBOUR[name]
    return task, cast(dict[str, Any], world.cbp.codeb_probe.execute(build, f"demo.codeb.t1c80.{group}.{name}"))


def _form1040(result: dict[str, Any]) -> list[Any]:
    lines = result.get("lines") or {}
    return [(lines.get(k) or [None, None])[1] for k in ("form1040.line-15", "form1040.line-16")]


def _unique(world: SimpleNamespace, group: str) -> list[str]:
    seen: dict[str, str] = {}
    kept: list[str] = []
    for name, build in world.builds[group].items():
        try:
            key = hashlib.sha256(json.dumps(build(), sort_keys=True).encode()).hexdigest()
        except Exception as exc:  # noqa: BLE001 — a rejected recording is its own case
            key = f"{type(exc).__name__}:{exc}"
        if key in seen:
            assert DUPLICATES[group].get(name) == seen[key], (group, name, seen[key])
            continue
        seen[key] = name
        kept.append(name)
    return kept


def _same_projection(entries: dict[str, Any]) -> dict[str, str]:
    """Each v80 return whose table entry another one already has, and the return it shares it with."""
    keep = set(ROW_MISSING_CHANGES) | set(REJECTED)
    first: dict[str, str] = {}
    out: dict[str, str] = {}
    for name in sorted(entries, key=lambda n: (n not in keep, n)):
        key = json.dumps(entries[name], sort_keys=True)
        if key in first and name not in keep:
            out[name] = first[key]
        else:
            first.setdefault(key, name)
    return dict(sorted(out.items()))


def regenerate(workers: int) -> None:
    world = build_world()
    names = {group: _unique(world, group) for group in GROUPS}
    tasks = [(group, name, "v81") for group in GROUPS for name in names[group]]
    tasks += [(group, name, "v80") for group in ("v80", "neighbour") for name in names[group]]
    results: dict[tuple[str, str, str], dict[str, Any]] = {}
    with ProcessPoolExecutor(workers) as pool:
        for task, result in pool.map(_worker, tasks):
            results[task] = result
            print(*task, result.get("error") or "", _form1040(result), flush=True)
    table: dict[str, Any] = {"case": {}, "v80": {}, "neighbour": {}}
    for name in names["case"]:
        table["case"][name] = projection(results[("case", name, "v81")])
    for group in ("v80", "neighbour"):
        for name in names[group]:
            v80, v81 = results[(group, name, "v80")], results[(group, name, "v81")]
            entry: dict[str, Any] = {"v80": v80_difference(projection(v80), projection(v81), set(v80.get("rows") or {}),
                                                           set(v81.get("rows") or {})), "v81": projection(v81)}
            if group == "v80":
                entry["v80_form1040"], entry["v81_form1040"] = _form1040(v80), _form1040(v81)
            else:
                entry["field_explain"] = {k: f["explain"] for k, f in (v81.get("fields") or {}).items()
                                          if f["disposition"] == "blocked"}
            table[group][name] = entry
    same = _same_projection(table["v80"])
    for name in same:
        del table["v80"][name]
    lines = ["{"]
    for i, group in enumerate(GROUPS):
        lines.append(f" {json.dumps(group)}: {{")
        keys = sorted(table[group])
        for j, name in enumerate(keys):
            comma = "," if j < len(keys) - 1 else ""
            lines.append(f"  {json.dumps(name)}: {json.dumps(table[group][name], sort_keys=True)}{comma}")
        lines.append(" }" + ("," if i < len(GROUPS) - 1 else ""))
    lines.append("}")
    text = world.cbp.probe.scrub("\n".join(lines)) + "\n"
    EXPECTED_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPECTED_PATH.write_text(text, encoding="utf-8")
    print(f"wrote {EXPECTED_PATH.relative_to(REPO)}", flush=True)
    if same != SAME_PROJECTION:
        print("SAME_PROJECTION is out of date; it should be:", json.dumps(same, indent=4), sep="\n", flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    regenerate(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
