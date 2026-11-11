"""Published core v85 runs the Form 1099-B no-sale box 4 Track 0 grid, and the 298 recorded v83 runs.

v85 is package core-calculations v85, registry v83 and release v83. Hand values
come from track0.py (``probe.hand_return``), not from the publication. The 298
recorded v83 runs are compared with
``tests/fixtures/f1099b_backup_withholding_v83/expected.json`` in place.

Twelve of the 58 Track 0 rows repeat another row's act list, so the live grid
runs the survivor once and that run asserts the duplicate rows. The grid is 46
published-v85 runs, 11 reuse runs on published v84, and the 298 recorded runs
(207 identical, 91 restored with present=no, and one of those 91 also run
unanswered).

The Track 0 pin is Form 1040 lines 25a-25d, 33, 34 and 37, each blocked line's
reason sentences and (disposition, code, missing), and the question asked.
``python3 tests/test_f1099b_box4_only_v85.py`` rewrites the Track 0 fixture from
the survivor runs and prints the run count and wall time. It does not rewrite
the 298-run fixture.

Each survivor is one live_coordinate_run. One run is several seconds, over the
3.0 s fast-lane budget, so this module is live.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

from tests import evidence_loader

# One live_coordinate_run is several seconds, over the 3.0 s fast-lane budget.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence"
FIXTURE_PATH = REPO / "tests/fixtures/f1099b_box4_only_v85/expected.json"
RECORDED_PATH = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TRACK0_NAME = "f1099b_box4_only_v85_live_track0"
RECORDED_NAME = "f1099b_box4_only_v85_recorded"
CHARTER_LINES = (
    "form1040.line-25a", "form1040.line-25b", "form1040.line-25c", "form1040.line-25d",
    "form1040.line-33", "form1040.line-34", "form1040.line-37",
)
PRESENT = "tax.us.2025.f1099b.no-sale-box4-present"


def _module(name: str, path: Path) -> ModuleType:
    module = sys.modules.get(name)
    if module is None:
        if str(REPO) not in sys.path:
            sys.path.insert(0, str(REPO))
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def load_track0() -> ModuleType:
    """The no-sale box 4 Track 0 harness, under a name no other test uses. Nothing on it is assigned."""
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    return evidence_loader.load(EVIDENCE / "track0.py", TRACK0_NAME)


def load_recorded() -> ModuleType:
    """The published v83 live module, under a name no other test uses. Nothing on it is assigned."""
    return _module(RECORDED_NAME, REPO / "tests/test_f1099b_backup_withholding_v83.py")


def published(probe: Any) -> Any:
    """Published core v85. The loader entries live in packages/tax/loader.py."""
    core = probe.h.Core("v85", "v83", "v83")
    assert core.loader_from is None and core.content == REPO / "packages/content/tax/2025"
    return core


def _line_of_row(row: dict[str, Any]) -> str | None:
    """The charter line a disposition row belongs to."""
    symbol = row.get("symbol")
    if symbol in CHARTER_LINES:
        return str(symbol)
    artifact = str(row.get("artifact") or "")
    if not artifact.startswith("rule."):
        return None
    rest = artifact[len("rule."):]
    marker = "-line"
    index = rest.rfind(marker)
    if index < 0:
        return None
    line = rest[:index] + ".line-" + rest[index + len(marker):]
    return line if line in CHARTER_LINES else None


def charter_view(result: dict[str, Any]) -> dict[str, Any]:
    """The charter pin: the named lines, each blocked line's reasons and row, and the question."""
    if result.get("outcome") != "success":
        return {"error": result.get("error") or result.get("outcome"),
                "message": str(result.get("message") or result.get("reason") or "")[:160]}
    present = result.get("lines") or {}
    reasons = result.get("reasons") or {}
    rows_by_line: dict[str, list[dict[str, Any]]] = {}
    for row in result.get("rows") or []:
        line = _line_of_row(row)
        if line is not None and isinstance(row.get("disposition"), str) and "blocked" in row["disposition"]:
            rows_by_line.setdefault(line, []).append(row)
    lines: dict[str, Any] = {}
    blocked: dict[str, list[dict[str, Any]]] = {}
    for line in CHARTER_LINES:
        lines[line] = present.get(line, "missing")
        value = lines[line]
        if isinstance(value, str) and "blocked" in value:
            blocked[line] = [
                {
                    "disposition": row.get("disposition"),
                    "code": row.get("code"),
                    "missing": row.get("missing") or [],
                    "reasons": list(reasons.get(line) or []),
                }
                for row in sorted(rows_by_line.get(line) or [],
                                  key=lambda item: (str(item.get("artifact")), str(item.get("subject") or "")))
            ]
    return {
        "lines": lines,
        "blocked": blocked,
        "questions": list(result.get("questions") or []),
        "presentation_valid": result.get("presentation_valid"),
    }


@lru_cache(maxsize=1)
def box4_cases() -> dict[str, Any]:
    track0 = load_track0()
    probe = track0.load_probe()
    core = published(probe)
    present_q, amount_q, box4_q = track0.question_texts(core)
    authority = {case["id"]: case for case in track0.build_authority(probe, core)}
    matrix = {case["id"]: case for case in track0.build_matrix(probe, core)}
    surface = {case["id"]: case for case in track0.build_surface(probe, core)}
    reuse = {case["id"]: case for case in track0.build_reuse(probe, core)}
    late = track0.build_late(probe, core)
    return {
        "track0": track0,
        "probe": probe,
        "core": core,
        "present_q": present_q,
        "amount_q": amount_q,
        "box4_q": box4_q,
        "authority": authority,
        "matrix": matrix,
        "surface": surface,
        "reuse": reuse,
        "late": late,
    }


def _fixture() -> dict[str, Any]:
    if not FIXTURE_PATH.exists():
        return {"counts": {}, "cases": {}}
    return cast(dict[str, Any], json.loads(FIXTURE_PATH.read_text(encoding="utf-8")))


def _recorded() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(RECORDED_PATH.read_text(encoding="utf-8")))


def _neighbour() -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((EVIDENCE / "track0-neighbour.json").read_text(encoding="utf-8")))


FIXTURE = _fixture()
RECORDED = _recorded()
NEIGHBOUR = _neighbour()
ASKS = tuple(NEIGHBOUR["asks_no_sale_present_ids"])
IDENTICAL = tuple(NEIGHBOUR["identical_ids"])

AUTHORITY_IDS = (
    "alc_present_unanswered", "alc_present_no", "alc_present_yes_amount",
    "alc_present_yes_amount_unanswered", "alc_stmt_with_sale", "alc_stmt_without_sale",
    "alc_stmt_identity", "alc_double_count",
)
AUTHORITY_RUN_IDS = ("alc_double_count",)
MATRIX_IDS = (
    "m_none_unanswered", "m_none_no", "m_none_yes_amount", "m_none_yes_amount_unanswered",
    "m_sale_unanswered_stmt200", "m_sale_no_stmt200", "m_sale_yes_amount_stmt200",
    "m_sale_yes_amount_unanswered_stmt200", "m_sale_no_stmt0", "m_sale_unanswered_stmt0",
    "m_nosale_unanswered", "m_nosale_no", "m_nosale_yes_amount", "m_nosale_yes_amount_unanswered",
    "m_nosale_no_stmt150", "m_nosale_yes_amount0_stmt150", "m_nosale_no_stmt0",
    "m_nosale_yes_amount_stmt0", "m_both_unanswered_sale200", "m_both_no_sale200",
    "m_both_yes_amount_sale200", "m_both_yes_amount_unanswered_sale200",
    "m_both_no_sale200_stmt150", "m_both_no_sale200_stmt0", "m_both_yes_amount0_sale200_stmt150",
)
SURFACE_IDS = (
    "surface_published_no", "surface_published_yes", "surface_published_sale",
    "surface_blocked_present", "surface_blocked_amount", "surface_blocked_sale_box4",
)
SURFACE_RUN_IDS = ("surface_blocked_sale_box4",)
REUSE_IDS = (
    "reuse_int_alone", "reuse_div_alone", "reuse_ira_alone", "reuse_unemp_alone",
    "reuse_ssa_alone", "reuse_all_five_alone", "reuse_all_with_b4", "reuse_b4_subtotal",
    "reuse_box4_question", "reuse_box7_check", "reuse_no_equals_v84",
)
LATE_IDS = (
    "late_yes_then_sale_then_no_before", "late_yes_then_sale_then_no_after",
    "late_sale_removed_before", "late_sale_removed_after",
    "late_amount_corrected_before", "late_amount_corrected_after",
    "late_yes_to_no_before", "late_yes_to_no_after",
)
DUPLICATE_OF = {
    "authority/alc_present_no": "matrix/m_none_no",
    "authority/alc_present_unanswered": "matrix/m_none_unanswered",
    "authority/alc_present_yes_amount": "matrix/m_none_yes_amount",
    "authority/alc_present_yes_amount_unanswered": "matrix/m_none_yes_amount_unanswered",
    "authority/alc_stmt_identity": "matrix/m_both_yes_amount_sale200",
    "authority/alc_stmt_with_sale": "matrix/m_sale_no_stmt200",
    "authority/alc_stmt_without_sale": "matrix/m_nosale_yes_amount0_stmt150",
    "surface/surface_published_no": "matrix/m_none_no",
    "surface/surface_blocked_present": "matrix/m_none_unanswered",
    "surface/surface_published_yes": "matrix/m_none_yes_amount",
    "surface/surface_blocked_amount": "matrix/m_none_yes_amount_unanswered",
    "surface/surface_published_sale": "matrix/m_sale_no_stmt200",
}
BLOCKED_SAMPLE = (
    "track0/s0/b4_yes_covered",
)


def _reuse_acts(track0: ModuleType, probe: Any, core: Any, acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return cast(
        list[dict[str, Any]],
        track0.with_present(probe, core, copy.deepcopy(acts), "no", None, tag="reuse"),
    )


def _run_v85(track0: ModuleType, case_id: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
    probe = track0.load_probe()
    return cast(dict[str, Any], track0.execute(published(probe), acts, "demo.b4only.v85." + case_id))


def _assert_hand(case: dict[str, Any], result: dict[str, Any], pinned: dict[str, Any], track0: ModuleType) -> None:
    hand = case.get("hand")
    assert pinned["hand"] == hand
    if not hand:
        return
    assert track0.hand_failures(result, hand) == []


def _assert_box4_case(group: str, case_id: str, case: dict[str, Any], result: dict[str, Any]) -> None:
    found = box4_cases()
    failures = found["track0"].contract_failures(
        case, result, found["present_q"], found["amount_q"], found["box4_q"])
    assert failures == [], (case_id, failures)
    view = charter_view(result)
    pinned = FIXTURE["cases"][f"{group}/{case_id}"]
    assert view == pinned["view"], case_id
    assert view["presentation_valid"] is True
    for line in CHARTER_LINES:
        assert line in view["lines"], (case_id, line)
        if isinstance(view["lines"][line], str) and "blocked" in view["lines"][line]:
            assert view["blocked"][line], (case_id, line)
            for row in view["blocked"][line]:
                assert set(row) == {"disposition", "code", "missing", "reasons"}
    _assert_hand(case, result, pinned, found["track0"])


def _assert_survivor(group: str, case_id: str, case: dict[str, Any], result: dict[str, Any]) -> None:
    """Assert this run, then every fixture row whose act list is this same list."""
    _assert_box4_case(group, case_id, case, result)
    found = box4_cases()
    survivor = f"{group}/{case_id}"
    for dropped, owner in DUPLICATE_OF.items():
        if owner != survivor:
            continue
        other_group, other_id = dropped.split("/", 1)
        other = found[other_group][other_id]
        assert other["acts"] == case["acts"], dropped
        _assert_box4_case(other_group, other_id, other, result)


@pytest.mark.parametrize("case_id", AUTHORITY_RUN_IDS)
def test_authority_case(case_id: str) -> None:
    found = box4_cases()
    case = found["authority"][case_id]
    _assert_survivor("authority", case_id, case, _run_v85(found["track0"], case_id, case["acts"]))


@pytest.mark.parametrize("case_id", MATRIX_IDS)
def test_matrix_case(case_id: str) -> None:
    found = box4_cases()
    case = found["matrix"][case_id]
    _assert_survivor("matrix", case_id, case, _run_v85(found["track0"], case_id, case["acts"]))


@pytest.mark.parametrize("case_id", SURFACE_RUN_IDS)
def test_surface_case(case_id: str) -> None:
    found = box4_cases()
    case = found["surface"][case_id]
    _assert_survivor("surface", case_id, case, _run_v85(found["track0"], case_id, case["acts"]))


def test_late_traces() -> None:
    found = box4_cases()
    track0 = found["track0"]
    for trace in found["late"]:
        steps = []
        for step in trace["steps"]:
            result = _run_v85(track0, step["id"], step["acts"])
            case = {**step, "note": trace["paper"]}
            _assert_box4_case("late", step["id"], case, result)
            steps.append({
                "passed": True,
                "result": result,
                "snapshot": track0.snapshot(found["probe"], step["acts"]),
            })
        extra = track0.late_failures(trace, steps)
        assert extra == [], (trace["id"], extra)


def test_sale_removed_honest_one_copy() -> None:
    """After the sale is gone, the leftover box 4 is one copy if the filer does not re-enter it."""
    found = box4_cases()
    track0 = found["track0"]
    probe = found["probe"]
    core = found["core"]
    pinned = FIXTURE["cases"]["late/late_sale_removed_after"]
    assert pinned["view"]["lines"]["form1040.line-25b"] == 200
    assert pinned["hand"]["form1040.line-25b"] == 200
    late = next(trace for trace in found["late"] if trace["id"] == "late_sale_removed")
    after = next(step for step in late["steps"] if step["id"] == "late_sale_removed_after")
    leftover = track0.with_present(probe, core, copy.deepcopy(after["acts"]), "yes", 0, tag="repair")
    result = _run_v85(track0, "repair_sale_removed_leftover_not_reentered", leftover)
    view = charter_view(result)
    assert view["presentation_valid"] is True
    assert view["lines"]["form1040.line-25b"] == 200
    assert view["lines"]["form1040.line-25d"] == 4700
    assert view["lines"]["form1040.line-33"] == 4700
    assert view["lines"]["form1040.line-34"] == 825
    assert view["lines"]["form1040.line-37"] == 0
    assert view["questions"] == []
    assert track0.hand_failures(result, after["hand"]) == []
    failures = track0.contract_failures(
        {**after, "kind": "published"}, result, found["present_q"], found["amount_q"], found["box4_q"])
    assert failures == []


def test_reuse_against_published_v84() -> None:
    found = box4_cases()
    track0 = found["track0"]
    probe = found["probe"]
    v84 = probe.h.Core("v84", "v82", "v82")
    assert v84.loader_from is None
    for case_id, case in found["reuse"].items():
        v85_acts = _reuse_acts(track0, probe, found["core"], case["acts"])
        v85_result = _run_v85(track0, case_id, v85_acts)
        v84_result = track0.execute(v84, case["acts"], "demo.b4only.v84." + case_id)
        failures = track0.reuse_failures(
            case, {"v85": v85_result, "v84": v84_result},
            found["present_q"], found["amount_q"], found["box4_q"])
        assert failures == [], (case_id, failures)
        _assert_box4_case("reuse", case_id, case, v85_result)


def test_track0_case_counts() -> None:
    found = box4_cases()
    counts = {
        "authority": len(found["authority"]),
        "matrix": len(found["matrix"]),
        "late": sum(len(trace["steps"]) for trace in found["late"]),
        "reuse": len(found["reuse"]),
        "surface": len(found["surface"]),
    }
    assert counts == {"authority": 8, "matrix": 25, "late": 8, "reuse": 11, "surface": 6}
    assert sorted(found["authority"]) == sorted(AUTHORITY_IDS)
    assert sorted(found["matrix"]) == sorted(MATRIX_IDS)
    assert sorted(found["surface"]) == sorted(SURFACE_IDS)
    assert sorted(found["reuse"]) == sorted(REUSE_IDS)
    assert [step["id"] for trace in found["late"] for step in trace["steps"]] == list(LATE_IDS)
    assert counts == FIXTURE["counts"]
    assert sum(counts.values()) == len(FIXTURE["cases"]) == 58
    assert len(DUPLICATE_OF) == 12
    assert set(DUPLICATE_OF) <= set(FIXTURE["cases"])
    runs = (
        [f"authority/{case_id}" for case_id in AUTHORITY_RUN_IDS]
        + [f"matrix/{case_id}" for case_id in MATRIX_IDS]
        + [f"late/{case_id}" for case_id in LATE_IDS]
        + [f"reuse/{case_id}" for case_id in REUSE_IDS]
        + [f"surface/{case_id}" for case_id in SURFACE_RUN_IDS]
    )
    assert len(runs) == 46
    assert set(runs).isdisjoint(DUPLICATE_OF)
    for dropped, survivor in DUPLICATE_OF.items():
        assert survivor in {f"matrix/{case_id}" for case_id in MATRIX_IDS}
        other_group, other_id = dropped.split("/", 1)
        owner_group, owner_id = survivor.split("/", 1)
        assert found[other_group][other_id]["acts"] == found[owner_group][owner_id]["acts"]
        assert FIXTURE["cases"][dropped]["view"] == FIXTURE["cases"][survivor]["view"]
        assert FIXTURE["cases"][dropped]["hand"] == FIXTURE["cases"][survivor]["hand"]


def test_recorded_split_is_207_identical_and_91_asks() -> None:
    assert len(IDENTICAL) == 207
    assert len(ASKS) == 91
    assert len(set(IDENTICAL) & set(ASKS)) == 0
    fixture_ids = (
        [f"track0/{key}" for key in RECORDED["track0"]]
        + [f"returns/{key}" for key in RECORDED["returns"]]
        + [f"zero/{key}" for key in RECORDED["zero_sample"]]
    )
    assert len(fixture_ids) == 298
    assert set(fixture_ids) == set(IDENTICAL) | set(ASKS)
    assert set(BLOCKED_SAMPLE) <= set(ASKS)


def _neighbour_acts(catalog: dict[str, Any], neighbour_id: str) -> list[dict[str, Any]]:
    test = catalog["test"]
    if neighbour_id.startswith("track0/"):
        return cast(list[dict[str, Any]], catalog["track0"][neighbour_id[len("track0/"):]])
    if neighbour_id.startswith("returns/"):
        return cast(list[dict[str, Any]], catalog["returns"][neighbour_id[len("returns/"):]])
    if neighbour_id.startswith("zero/"):
        key = neighbour_id[len("zero/"):]
        return cast(list[dict[str, Any]], test.with_zero(catalog["harness"], catalog["returns"][key], catalog["core"]))
    raise AssertionError(neighbour_id)


def _recorded_pin(catalog: dict[str, Any], neighbour_id: str) -> dict[str, Any]:
    if neighbour_id.startswith("track0/"):
        return cast(dict[str, Any], RECORDED["track0"][neighbour_id[len("track0/"):]])
    if neighbour_id.startswith("returns/"):
        return cast(dict[str, Any], RECORDED["returns"][neighbour_id[len("returns/"):]]["v83"])
    if neighbour_id.startswith("zero/"):
        return cast(dict[str, Any], RECORDED["zero_sample"][neighbour_id[len("zero/"):]]["v83"])
    raise AssertionError(neighbour_id)


@pytest.fixture(scope="module")
def recorded_acts(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    test = load_recorded()
    harness = test.track0()
    exported = test.export_returns(tmp_path_factory.mktemp("f1099b-box4-only-v85"))
    probe = load_track0().load_probe()
    return {
        "test": test,
        "harness": harness,
        "track0": dict(test.decided_cases(harness)),
        "returns": test.return_acts(harness, exported),
        "core": published(probe),
        "probe": probe,
    }


def _assert_recorded(catalog: dict[str, Any], neighbour_id: str, acts: list[dict[str, Any]],
                     pinned: dict[str, Any]) -> None:
    test = catalog["test"]
    got = test.pin(test.track0().run_coordinate(
        catalog["core"], acts, "demo.b4only.v85.recorded." + neighbour_id.replace("/", ".")))
    assert got == pinned, neighbour_id


@pytest.mark.parametrize("neighbour_id", [key for key in IDENTICAL if key.startswith("track0/")])
def test_recorded_track0_identical(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _neighbour_acts(recorded_acts, neighbour_id),
                     _recorded_pin(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in IDENTICAL if key.startswith("returns/")])
def test_recorded_return_identical(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    _assert_recorded(recorded_acts, neighbour_id, _neighbour_acts(recorded_acts, neighbour_id),
                     _recorded_pin(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("track0/")])
def test_recorded_track0_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    probe = recorded_acts["probe"]
    acts = probe.say_return(
        copy.deepcopy(_neighbour_acts(recorded_acts, neighbour_id)),
        recorded_acts["core"], probe.PRESENT, "no", "t1.restore")
    _assert_recorded(recorded_acts, neighbour_id, acts, _recorded_pin(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("returns/")])
def test_recorded_return_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    probe = recorded_acts["probe"]
    acts = probe.say_return(
        copy.deepcopy(_neighbour_acts(recorded_acts, neighbour_id)),
        recorded_acts["core"], probe.PRESENT, "no", "t1.restore")
    _assert_recorded(recorded_acts, neighbour_id, acts, _recorded_pin(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", [key for key in ASKS if key.startswith("zero/")])
def test_recorded_zero_restore_present_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    probe = recorded_acts["probe"]
    acts = probe.say_return(
        copy.deepcopy(_neighbour_acts(recorded_acts, neighbour_id)),
        recorded_acts["core"], probe.PRESENT, "no", "t1.restore")
    _assert_recorded(recorded_acts, neighbour_id, acts, _recorded_pin(recorded_acts, neighbour_id))


@pytest.mark.parametrize("neighbour_id", BLOCKED_SAMPLE)
def test_one_of_the_91_blocks_on_the_yes_no(recorded_acts: dict[str, Any], neighbour_id: str) -> None:
    test = recorded_acts["test"]
    found = box4_cases()
    got = test.pin(test.track0().run_coordinate(
        recorded_acts["core"], _neighbour_acts(recorded_acts, neighbour_id),
        "demo.b4only.v85.blocked." + neighbour_id.replace("/", ".")))
    assert got.get("presentation_valid") is True, neighbour_id
    line = (got.get("lines") or {}).get("form1040.line-25b")
    assert isinstance(line, str) and "block" in line, (neighbour_id, line)
    blob = json.dumps(got)
    assert "no closed sale" in blob, neighbour_id
    assert PRESENT in blob or "f1099b.no-sale-box4-present" in blob, neighbour_id
    questions = [str(item) for item in (got.get("questions") or [])]
    reasons = [str(item) for item in ((got.get("reasons") or {}).get("form1040.line-25b") or [])]
    reasons += [str(item) for item in ((got.get("blocked_reasons") or {}).get("form1040.line-25b") or [])]
    assert found["present_q"] in questions or any("no closed sale" in item for item in reasons + questions), (
        neighbour_id, questions, reasons)


def _worker(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    group, case_id, acts = item
    track0 = load_track0()
    result = _run_v85(track0, case_id, acts)
    return f"{group}/{case_id}", result


def main() -> None:
    started = time.perf_counter()
    found = box4_cases()
    track0 = found["track0"]
    probe = found["probe"]
    core = found["core"]
    items: list[tuple[str, str, list[dict[str, Any]]]] = []
    for group in ("authority", "matrix", "surface"):
        for case_id, case in found[group].items():
            if f"{group}/{case_id}" in DUPLICATE_OF:
                continue
            items.append((group, case_id, case["acts"]))
    for case_id, case in found["reuse"].items():
        items.append(("reuse", case_id, _reuse_acts(track0, probe, core, case["acts"])))
    for trace in found["late"]:
        for step in trace["steps"]:
            items.append(("late", step["id"], step["acts"]))
    print(f"running {len(items)} Track 0 cases", flush=True)
    results: dict[str, dict[str, Any]] = {}
    workers = min(6, os.cpu_count() or 2)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, result in pool.map(_worker, items):
            results[key] = result
            done += 1
            if done % 10 == 0 or done == len(items):
                print(f"  {done}/{len(items)} {key} {result.get('outcome')}", flush=True)
    cases: dict[str, Any] = {}

    def _view_for(key: str) -> dict[str, Any]:
        source = DUPLICATE_OF.get(key, key)
        return charter_view(results[source])

    for group in ("authority", "matrix", "surface", "reuse"):
        for case_id, case in found[group].items():
            key = f"{group}/{case_id}"
            cases[key] = {"hand": case.get("hand"), "view": _view_for(key)}
    for trace in found["late"]:
        for step in trace["steps"]:
            key = f"late/{step['id']}"
            cases[key] = {"hand": step.get("hand"), "view": _view_for(key)}
    counts = {
        "authority": len(found["authority"]),
        "matrix": len(found["matrix"]),
        "late": sum(len(trace["steps"]) for trace in found["late"]),
        "reuse": len(found["reuse"]),
        "surface": len(found["surface"]),
    }
    payload = {"counts": counts, "cases": cases}
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"fixture contains {needle}")
    FIXTURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FIXTURE_PATH.write_text(text, encoding="utf-8")
    elapsed = time.perf_counter() - started
    problems = [key for key, result in results.items() if result.get("outcome") != "success"]
    for key, case in cases.items():
        view = case["view"]
        for line, value in (view.get("lines") or {}).items():
            if isinstance(value, str) and "blocked" in value and not (view.get("blocked") or {}).get(line):
                problems.append(f"{key} blocked {line} has no row")
    print(json.dumps({
        "cases": len(cases),
        "counts": counts,
        "runs": len(items),
        "problems": problems,
        "seconds": round(elapsed, 1),
        "fixture_bytes": FIXTURE_PATH.stat().st_size,
    }, indent=2))


if __name__ == "__main__":
    main()
