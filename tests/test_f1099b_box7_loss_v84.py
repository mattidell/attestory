"""Published core v84 runs the Form 1099-B box 7 Track 0 grid, and the 298 recorded v83 runs.

v84 is package core-calculations v84, registry v82 and release v82. Hand values
come from track0.py (``probe.hand_return``), not from the publication. The 298
recorded v83 runs are compared with
``tests/fixtures/f1099b_backup_withholding_v83/expected.json`` in place.

The fixture still holds all 89 Track 0 rows. Twenty-eight of those rows repeat
another row's act list, so the live grid runs the survivor once and that run
asserts the duplicate rows. ``reuse_covered_flag`` stays: no other row shares
its acts or its view. The grid is 61 published-v84 runs, 4 reuse runs on
published v83, and the 298 recorded runs.

The Track 0 pin is Schedule D lines 1a through 16 and line 21, Form 1040 lines
7a, 15, 16, 24, 33, 34 and 37, and each blocked line's reason sentences and
(disposition, code, missing). Lines 4, 5, 11 and 12 have no form field.
``python3 tests/test_f1099b_box7_loss_v84.py`` rewrites the Track 0 fixture from
the survivor runs and prints the run count and wall time. It does not rewrite
the 298-run fixture.

Each survivor is one live_coordinate_run. Measured while writing the Track 0
fixture: 61 runs finished in 86.2 s with 6 workers. That is over the 3.0 s
fast-lane budget, so this module is live.
"""

from __future__ import annotations

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

# One live_coordinate_run is several seconds, over the 3.0 s fast-lane budget.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-box7-loss-evidence"
FIXTURE_PATH = REPO / "tests/fixtures/f1099b_box7_loss_v84/expected.json"
RECORDED_PATH = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TRACK0_NAME = "f1099b_box7_v84_live_track0"
RECORDED_NAME = "f1099b_box7_v84_recorded"
SCHEDULE_D = tuple(
    f"schedule-d.line-{name}"
    for name in (
        "1a", "1b", "2", "3", "4", "5", "6", "7", "8a", "8b", "9", "10",
        "11", "12", "13", "14", "15", "16", "21",
    )
)
FORM_1040 = (
    "form1040.line-7a", "form1040.line-15", "form1040.line-16", "form1040.line-24",
    "form1040.line-33", "form1040.line-34", "form1040.line-37",
)
CHARTER_LINES = SCHEDULE_D + FORM_1040
ABSENT = frozenset({
    "schedule-d.line-4", "schedule-d.line-5", "schedule-d.line-11", "schedule-d.line-12",
})
EXTRA_LINES = ("schedule-d.line-6", "schedule-d.line-13", "schedule-d.line-14")


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
    """The box 7 Track 0 harness, under a name no other test uses. Nothing on it is assigned."""
    return _module(TRACK0_NAME, EVIDENCE / "track0.py")


def load_recorded() -> ModuleType:
    """The published v83 live module, under a name no other test uses. Nothing on it is assigned."""
    return _module(RECORDED_NAME, REPO / "tests/test_f1099b_backup_withholding_v83.py")


def published(probe: Any) -> Any:
    """Published core v84. The loader entries live in packages/tax/loader.py."""
    core = probe.h.Core("v84", "v82", "v82")
    assert core.loader_from is None and core.content == REPO / "packages/content/tax/2025"
    return core


def _line_of_row(row: dict[str, Any]) -> str | None:
    """The charter line a disposition row belongs to.

    A published row names its symbol. A blocked row does not, so the line is
    read off the rule artifact (``rule.schedule-d-line16`` is ``schedule-d.line-16``).
    """
    symbol = row.get("symbol")
    if symbol in CHARTER_LINES:
        return str(symbol)
    if isinstance(symbol, str) and symbol.endswith("-gain") and symbol.removesuffix("-gain") in CHARTER_LINES:
        return symbol.removesuffix("-gain")
    artifact = str(row.get("artifact") or "")
    if not artifact.startswith("rule."):
        return None
    rest = artifact[len("rule."):]
    marker = "-line"
    index = rest.rfind(marker)
    if index < 0:
        return None
    line = rest[:index] + ".line-" + rest[index + len(marker):]
    if line.endswith("-gain") and line.removesuffix("-gain") in CHARTER_LINES:
        return line.removesuffix("-gain")
    return line if line in CHARTER_LINES else None


def charter_view(result: dict[str, Any]) -> dict[str, Any]:
    """The charter pin: the named lines, and each blocked line's reasons and row."""
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
        if line in ABSENT:
            lines[line] = "absent"
            continue
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


def _hand_failures(result: dict[str, Any], hand: dict[str, Any]) -> list[str]:
    found = []
    lines = result.get("lines") or {}
    for line, expected in hand.items():
        if lines.get(line) != expected:
            found.append(f"{line}: hand {expected} got {lines.get(line)}")
    return found


@lru_cache(maxsize=1)
def box7_cases() -> dict[str, Any]:
    track0 = load_track0()
    probe = track0.load_probe()
    core = published(probe)
    authority = {case["id"]: case for case in track0.build_authority(probe, core)}
    matrix = {case["id"]: case for case in track0.build_matrix(probe, core)}
    surface = {case["id"]: case for case in track0.build_surface(probe, core)}
    reuse = {case["id"]: case for case in track0.build_reuse(probe, core)}
    late = track0.build_late(probe, core)
    return {
        "track0": track0,
        "probe": probe,
        "question": track0.question_text(),
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


FIXTURE = _fixture()
RECORDED = _recorded()


AUTHORITY_IDS = (
    "alc_closed_empty", "alc_code-b-lt_gain", "alc_code-b-lt_loss", "alc_code-b-st_gain",
    "alc_code-b-st_loss", "alc_count_two", "alc_covered-lt_gain", "alc_covered-lt_loss",
    "alc_covered-st_gain", "alc_covered-st_loss", "alc_covered-w-lt_gain", "alc_covered-w-lt_loss",
    "alc_covered-w-st_gain", "alc_covered-w-st_loss", "alc_covered_st_unanswered",
    "alc_noncovered-lt_gain", "alc_noncovered-lt_loss", "alc_noncovered-st_gain",
    "alc_noncovered-st_loss", "alc_same_statement", "alc_statement_scope",
)
# These three have no twin in the matrix. The other eighteen authority rows repeat one.
AUTHORITY_RUN_IDS = ("alc_count_two", "alc_same_statement", "alc_statement_scope")
MATRIX_IDS = (
    "m_absence_code-b-lt", "m_absence_code-b-st", "m_absence_covered-lt", "m_absence_covered-st",
    "m_absence_covered-w-lt", "m_absence_covered-w-st", "m_absence_noncovered-lt",
    "m_absence_noncovered-st", "m_closed_empty",
    "m_code-b-lt_no", "m_code-b-lt_unanswered", "m_code-b-lt_yes_gain", "m_code-b-lt_yes_loss",
    "m_code-b-lt_yes_zero", "m_code-b-st_no", "m_code-b-st_unanswered", "m_code-b-st_yes_gain",
    "m_code-b-st_yes_loss", "m_code-b-st_yes_zero", "m_covered-lt_no", "m_covered-lt_unanswered",
    "m_covered-lt_yes_gain", "m_covered-lt_yes_loss", "m_covered-lt_yes_zero", "m_covered-st_no",
    "m_covered-st_unanswered", "m_covered-st_yes_gain", "m_covered-st_yes_loss", "m_covered-st_yes_zero",
    "m_covered-w-lt_no", "m_covered-w-lt_unanswered", "m_covered-w-lt_yes_gain", "m_covered-w-lt_yes_loss",
    "m_covered-w-lt_yes_zero", "m_covered-w-st_no", "m_covered-w-st_unanswered", "m_covered-w-st_yes_gain",
    "m_covered-w-st_yes_loss", "m_covered-w-st_yes_zero", "m_noncovered-lt_no", "m_noncovered-lt_unanswered",
    "m_noncovered-lt_yes_gain", "m_noncovered-lt_yes_loss", "m_noncovered-lt_yes_zero", "m_noncovered-st_no",
    "m_noncovered-st_unanswered", "m_noncovered-st_yes_gain", "m_noncovered-st_yes_loss",
    "m_noncovered-st_yes_zero",
)
SURFACE_IDS = (
    "surface_blocked_count", "surface_blocked_unanswered", "surface_blocked_yes_loss",
    "surface_no_box7_activity", "surface_published_gain", "surface_published_loss",
    "surface_published_zero",
)
REUSE_IDS = ("reuse_box7_no", "reuse_covered_flag", "reuse_no_sale", "reuse_yes_gain")
LATE_IDS = (
    "late_gain_then_loss_before", "late_gain_then_loss_after", "late_loss_removed_before",
    "late_loss_removed_after", "late_yes_to_no_before", "late_yes_to_no_after",
    "late_new_statement_before", "late_new_statement_after",
)
_SALE_SLUGS = (
    "covered-st", "covered-lt", "covered-w-st", "covered-w-lt",
    "noncovered-st", "noncovered-lt", "code-b-st", "code-b-lt",
)
# Twenty-eight v84 rows whose act list is identical to a matrix row. The matrix
# run asserts both fixture rows. reuse_covered_flag is not here: its view is unique.
DUPLICATE_OF = {
    **{f"authority/alc_{slug}_gain": f"matrix/m_{slug}_yes_gain" for slug in _SALE_SLUGS},
    **{f"authority/alc_{slug}_loss": f"matrix/m_{slug}_yes_loss" for slug in _SALE_SLUGS},
    "authority/alc_closed_empty": "matrix/m_closed_empty",
    "authority/alc_covered_st_unanswered": "matrix/m_covered-st_unanswered",
    "surface/surface_published_gain": "matrix/m_covered-st_yes_gain",
    "surface/surface_published_loss": "matrix/m_covered-st_no",
    "surface/surface_published_zero": "matrix/m_covered-st_yes_zero",
    "surface/surface_blocked_yes_loss": "matrix/m_covered-st_yes_loss",
    "surface/surface_blocked_unanswered": "matrix/m_covered-st_unanswered",
    "surface/surface_no_box7_activity": "matrix/m_closed_empty",
    "surface/surface_blocked_count": "matrix/m_absence_covered-st",
    "reuse/reuse_box7_no": "matrix/m_covered-st_no",
    "reuse/reuse_no_sale": "matrix/m_closed_empty",
    "reuse/reuse_yes_gain": "matrix/m_covered-st_yes_gain",
}


def _run_box7(track0: ModuleType, case_id: str, acts: list[dict[str, Any]]) -> dict[str, Any]:
    probe = track0.load_probe()
    return cast(
        dict[str, Any],
        track0.execute(published(probe), acts, "demo.b7.v84." + case_id, extra_lines=EXTRA_LINES),
    )


def _assert_hand(case: dict[str, Any], result: dict[str, Any], pinned: dict[str, Any]) -> None:
    hand = case.get("hand")
    assert pinned["hand"] == hand
    if hand is None:
        return
    assert _hand_failures(result, hand) == []


def _assert_box7_case(group: str, case_id: str, case: dict[str, Any], result: dict[str, Any]) -> None:
    found = box7_cases()
    failures = found["track0"].contract_failures(case, result, found["question"])
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
    _assert_hand(case, result, pinned)


def _assert_survivor(group: str, case_id: str, case: dict[str, Any], result: dict[str, Any]) -> None:
    """Assert this run, then every fixture row whose act list is this same list."""
    _assert_box7_case(group, case_id, case, result)
    found = box7_cases()
    survivor = f"{group}/{case_id}"
    for dropped, owner in DUPLICATE_OF.items():
        if owner != survivor:
            continue
        other_group, other_id = dropped.split("/", 1)
        other = found[other_group][other_id]
        assert other["acts"] == case["acts"], dropped
        _assert_box7_case(other_group, other_id, other, result)


@pytest.mark.parametrize("case_id", AUTHORITY_RUN_IDS)
def test_authority_case(case_id: str) -> None:
    found = box7_cases()
    case = found["authority"][case_id]
    _assert_survivor("authority", case_id, case, _run_box7(found["track0"], case_id, case["acts"]))


@pytest.mark.parametrize("case_id", MATRIX_IDS)
def test_matrix_case(case_id: str) -> None:
    found = box7_cases()
    case = found["matrix"][case_id]
    _assert_survivor("matrix", case_id, case, _run_box7(found["track0"], case_id, case["acts"]))


def test_late_traces() -> None:
    found = box7_cases()
    track0 = found["track0"]
    for trace in found["late"]:
        steps = []
        for step in trace["steps"]:
            result = _run_box7(track0, step["id"], step["acts"])
            case = {**step, "slug": trace["slug"], "note": trace["paper"]}
            _assert_box7_case("late", step["id"], case, result)
            steps.append({
                "passed": True,
                "result": result,
                "snapshot": track0.snapshot(found["probe"], step["acts"], trace["slug"]),
            })
        extra = track0.late_failures(trace, steps)
        assert extra == [], (trace["id"], extra)


def test_reuse_against_published_v83() -> None:
    """Four v83 runs stay. Three v84 halves repeat a matrix row. The covered-flag row does not."""
    found = box7_cases()
    track0 = found["track0"]
    probe = found["probe"]
    v83 = probe.h.Core("v83", "v81", "v81")
    assert v83.loader_from is None
    for case_id, case in found["reuse"].items():
        v83_result = track0.execute(v83, case["acts"], "demo.b7.v83." + case_id, extra_lines=EXTRA_LINES)
        assert v83_result.get("outcome") == "success", case_id
        pinned = FIXTURE["cases"][f"reuse/{case_id}"]
        if case_id == "reuse_covered_flag":
            v84_result = _run_box7(track0, case_id, case["acts"])
            failures = track0.reuse_failures(case, {"v84": v84_result, "v83": v83_result}, found["question"])
            assert failures == [], (case_id, failures)
            _assert_box7_case("reuse", case_id, case, v84_result)
            continue
        mode = case["compare"]
        view = charter_view(v83_result)
        if mode == "identical":
            assert track0.hand_failures(v83_result, case["hand"]) == [], case_id
            assert view["lines"] == pinned["view"]["lines"], case_id
            assert view["presentation_valid"] is True
        elif mode == "line7_line15_counts":
            for line in ("schedule-d.line-7", "schedule-d.line-15"):
                assert view["lines"][line] == pinned["view"]["lines"][line], (case_id, line)
            assert view["lines"]["schedule-d.line-16"] != pinned["view"]["lines"]["schedule-d.line-16"]
            assert track0.count_failures(v83_result, case["counts"]) == [], case_id
        else:
            raise AssertionError(case["compare"])


def test_track0_case_counts() -> None:
    found = box7_cases()
    counts = {
        "authority": len(found["authority"]),
        "matrix": len(found["matrix"]),
        "late": sum(len(trace["steps"]) for trace in found["late"]),
        "reuse": len(found["reuse"]),
        "surface": len(found["surface"]),
    }
    assert counts == {"authority": 21, "matrix": 49, "late": 8, "reuse": 4, "surface": 7}
    assert sorted(found["authority"]) == sorted(AUTHORITY_IDS)
    assert sorted(found["matrix"]) == sorted(MATRIX_IDS)
    assert sorted(found["surface"]) == sorted(SURFACE_IDS)
    assert sorted(found["reuse"]) == sorted(REUSE_IDS)
    assert [step["id"] for trace in found["late"] for step in trace["steps"]] == list(LATE_IDS)
    assert counts == FIXTURE["counts"]
    assert sum(counts.values()) == len(FIXTURE["cases"]) == 89
    assert len(DUPLICATE_OF) == 28
    assert set(DUPLICATE_OF) <= set(FIXTURE["cases"])
    runs = (
        [f"authority/{case_id}" for case_id in AUTHORITY_RUN_IDS]
        + [f"matrix/{case_id}" for case_id in MATRIX_IDS]
        + [f"late/{case_id}" for case_id in LATE_IDS]
        + ["reuse/reuse_covered_flag"]
    )
    assert len(runs) == 61
    assert set(runs).isdisjoint(DUPLICATE_OF)
    for dropped, survivor in DUPLICATE_OF.items():
        assert survivor in {f"matrix/{case_id}" for case_id in MATRIX_IDS}
        other_group, other_id = dropped.split("/", 1)
        owner_group, owner_id = survivor.split("/", 1)
        assert found[other_group][other_id]["acts"] == found[owner_group][owner_id]["acts"]
        assert FIXTURE["cases"][dropped]["view"] == FIXTURE["cases"][survivor]["view"]
        assert FIXTURE["cases"][dropped]["hand"] == FIXTURE["cases"][survivor]["hand"]


def _return_keys(prefix: str) -> list[str]:
    return sorted(key for key in RECORDED["returns"] if key.startswith(prefix))


@pytest.fixture(scope="module")
def recorded_acts(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    test = load_recorded()
    harness = test.track0()
    exported = test.export_returns(tmp_path_factory.mktemp("f1099b-box7-v84"))
    return {
        "test": test,
        "harness": harness,
        "track0": dict(test.decided_cases(harness)),
        "returns": test.return_acts(harness, exported),
        "core": published(harness),
    }


def _assert_recorded(catalog: dict[str, Any], key: str, acts: list[dict[str, Any]], pinned: dict[str, Any]) -> None:
    test = catalog["test"]
    got = test.pin(test.track0().run_coordinate(
        catalog["core"], acts, "demo.b7.v84.recorded." + key.replace("/", ".")))
    assert got == pinned, key


@pytest.mark.parametrize("key", sorted(RECORDED["track0"]))
def test_recorded_track0_matches_v84(recorded_acts: dict[str, Any], key: str) -> None:
    _assert_recorded(recorded_acts, "track0/" + key, recorded_acts["track0"][key], RECORDED["track0"][key])


@pytest.mark.parametrize("key", _return_keys("case/"))
def test_recorded_return_case_matches_v84(recorded_acts: dict[str, Any], key: str) -> None:
    _assert_recorded(recorded_acts, "returns/" + key, recorded_acts["returns"][key], RECORDED["returns"][key]["v83"])


@pytest.mark.parametrize("key", _return_keys("v80/"))
def test_recorded_return_v80_matches_v84(recorded_acts: dict[str, Any], key: str) -> None:
    _assert_recorded(recorded_acts, "returns/" + key, recorded_acts["returns"][key], RECORDED["returns"][key]["v83"])


@pytest.mark.parametrize("key", _return_keys("neighbour/"))
def test_recorded_return_neighbour_matches_v84(recorded_acts: dict[str, Any], key: str) -> None:
    _assert_recorded(recorded_acts, "returns/" + key, recorded_acts["returns"][key], RECORDED["returns"][key]["v83"])


@pytest.mark.parametrize("key", sorted(RECORDED["zero_sample"]))
def test_recorded_zero_sample_matches_v84(recorded_acts: dict[str, Any], key: str) -> None:
    test = recorded_acts["test"]
    acts = test.with_zero(recorded_acts["harness"], recorded_acts["returns"][key], recorded_acts["core"])
    _assert_recorded(recorded_acts, "zero/" + key, acts, RECORDED["zero_sample"][key]["v83"])


def _worker(item: tuple[str, str, list[dict[str, Any]]]) -> tuple[str, dict[str, Any]]:
    group, case_id, acts = item
    track0 = load_track0()
    result = _run_box7(track0, case_id, acts)
    return f"{group}/{case_id}", result


def main() -> None:
    started = time.perf_counter()
    found = box7_cases()
    items: list[tuple[str, str, list[dict[str, Any]]]] = []
    for group in ("authority", "matrix", "surface", "reuse"):
        for case_id, case in found[group].items():
            if f"{group}/{case_id}" in DUPLICATE_OF:
                continue
            items.append((group, case_id, case["acts"]))
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
