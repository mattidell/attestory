"""Core v83 runs the decided Form 1099-B box 4 cases and every pinned return through the coordinator.

v83 is package core-calculations v83, registry v81 and release v81. The bridge
repair is not taken: a recorded v82 box 4 yes/no does not close the amount.
Every run goes through ``live_coordinate_run`` and the presentation model on
the published v83. The v82 sibling of a case is not run again, and the repair
scratch is not run.

- ``track0``: each decided-design Track 0 case (scopes 0, 1, 2, 3, 4, 5 and 7).
  Scope 0 uses the v83 act list. Scope 1 runs once, on published v83. The
  published-v82 authority case is omitted.
- ``returns``: each of the 213 returns pinned by the sale-family audit, with
  the same act-list corrections that audit uses, compared with its committed
  v82 projection. Answering box 4 as $0 on a sample of the changed returns
  restores that projection's lines.

The pin is lines 25b, 25d, 33, 34, 35a and 37 (25d and 35a overlaid from the
full form; the sale-family watch list does not carry them), the other watched
lines, the attachments, each blocked line's reason sentences, and the watched
rows.
Act lists that are the same are run once. The table is
``tests/fixtures/f1099b_backup_withholding_v83/expected.json``.
``python3 tests/test_f1099b_backup_withholding_v83.py`` regenerates it.

Synthetic demo.* data only.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import pytest

# Each case is one full live_coordinate_run (about 5 to 20 s), so the module is an
# integration test and runs in the live lane.
pytestmark = pytest.mark.live

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence"
EXPECTED_PATH = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
V82_FIXTURE = REPO / "tests/fixtures/sale_family_audit_v82/expected.json"
TRACK0_MODULE = "f1099b_b4_v83_live_track0"
EXPORT = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/export_v81_returns.py"
LINE_25D = "form1040.line-25d"
LINE_35A = "form1040.line-35a"
AMOUNT_PROMPT = "box 4 of each Form 1099-B"
NAMED_SAMPLE = "case/a_8949_yes/recorded"
CHARTER_LINES = (
    "form1040.line-25b", LINE_25D, "form1040.line-33", "form1040.line-34", LINE_35A, "form1040.line-37",
)
# The sale-family projection does not carry these. pin() overlays them from the full form.
OVERLAY_LINES = (LINE_25D, LINE_35A)
PAYMENT_LINES = frozenset({
    "form1040.line-25b", "form1040.line-25d", "form1040.line-33",
    "form1040.line-34", "form1040.line-35a", "form1040.line-37",
})
PAYMENT_ROWS = frozenset({
    "form1040-line25b", "form1040-line25d", "form1040-line33",
    "form1040-line34", "form1040-line35a", "form1040-line36", "form1040-line37",
})
CLASSES = {"box4_unanswered_asks_amount": 150, "identical": 63}
Acts = list[dict[str, Any]]


def track0() -> ModuleType:
    """The Form 1099-B Track 0 harness, under a name no other test uses. Nothing on it is assigned."""
    module = sys.modules.get(TRACK0_MODULE)
    if module is None:
        if str(REPO) not in sys.path:
            sys.path.insert(0, str(REPO))
        spec = importlib.util.spec_from_file_location(TRACK0_MODULE, EVIDENCE / "track0.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[TRACK0_MODULE] = module
        spec.loader.exec_module(module)
    return module


def published(t: ModuleType) -> Any:
    """Published core v83. No scratch loader entries: packages/tax/loader.py carries them."""
    core = t.h.Core("v83", "v81", "v81")
    assert core.loader_from is None and core.content == REPO / "packages/content/tax/2025"
    return core


def _cases(t: ModuleType, name: str) -> list[dict[str, Any]]:
    found = getattr(t, name)()
    assert isinstance(found, list)
    return cast(list[dict[str, Any]], found)


def decided_cases(t: ModuleType) -> list[tuple[str, Acts]]:
    """Every decided-design Track 0 case, once. The v82 run and the repair scratch are not included."""
    out: list[tuple[str, Acts]] = []
    for case in _cases(t, "build_scope0_cases"):
        out.append(("s0/" + str(case["case_id"]), cast(Acts, case["acts_v83"])))
    for case in _cases(t, "build_scope1_cases"):
        out.append(("s1/" + str(case["case_id"]), cast(Acts, case["acts"])))
    for case in _cases(t, "build_scope2_cases"):
        if case.get("core") == "v82":
            continue
        out.append(("s2/" + str(case["case_id"]), cast(Acts, case["acts"])))
    for prefix, name in (
            ("s3", "build_scope3_cases"), ("s4", "build_scope4_cases"),
            ("s5", "build_scope5_cases"), ("s7", "build_scope7_cases")):
        for case in _cases(t, name):
            out.append((prefix + "/" + str(case["case_id"]), cast(Acts, case["acts"])))
    return out


def export_returns(directory: Path) -> dict[str, dict[str, Acts]]:
    out = directory / "v81-acts.json"
    subprocess.run([sys.executable, str(EXPORT), str(out)], check=True, cwd=REPO, stdout=subprocess.DEVNULL)
    exported: dict[str, dict[str, Acts]] = json.loads(out.read_text(encoding="utf-8"))
    return exported


def return_acts(t: ModuleType, exported: dict[str, dict[str, Acts]]) -> dict[str, Acts]:
    """The 213 returns, corrected the way the sale-family audit corrects them, with box 4 and box 7 answered no."""
    fixes = set(t.sfa_t0.DESIGNS["final"])
    out: dict[str, Acts] = {}
    for group in ("case", "v80", "neighbour"):
        for name in sorted(exported.get(group, {})):
            acts = t.rows_removed_first(t.own_rows(exported[group][name]))
            acts = t.sfa_t0.box_answers(acts, t.V82, fixes, "no", "no")
            out[f"{group}/{name}/recorded"] = cast(Acts, acts)
    return out


def digest(acts: Acts) -> str:
    return hashlib.sha256(json.dumps(acts, sort_keys=True).encode("utf-8")).hexdigest()


def split(items: list[tuple[str, Acts]]) -> tuple[list[tuple[str, Acts]], dict[str, str]]:
    """Run each distinct act list once, under the first key."""
    seen: dict[str, str] = {}
    tasks: list[tuple[str, Acts]] = []
    duplicates: dict[str, str] = {}
    for key, acts in items:
        name = digest(acts)
        found = seen.get(name)
        if found is None:
            seen[name] = key
            tasks.append((key, acts))
        else:
            duplicates[key] = found
    return tasks, duplicates


def _shown(disposition: Any, value: Any) -> Any:
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    if value is None or (isinstance(disposition, str) and "blocked" in disposition):
        return disposition
    return value


def pin(result: dict[str, Any]) -> dict[str, Any]:
    """The watched projection, plus lines 25d and 35a and every blocked line's reason sentences."""
    if result.get("outcome") != "success":
        return {"error": result.get("error") or result.get("outcome"), "message": str(result.get("message") or "")[:160]}
    proj = result.get("projection") or {}
    if "error" in proj:
        return cast(dict[str, Any], proj)
    lines = dict(proj.get("lines") or {})
    reasons = dict(proj.get("reasons") or {})
    for line in OVERLAY_LINES:
        disposition = (result.get("dispositions") or {}).get(line)
        if disposition is None:
            continue
        lines[line] = _shown(disposition, (result.get("lines") or {}).get(line))
        if isinstance(disposition, str) and "blocked" in disposition:
            reasons[line] = list((result.get("blocked_reasons") or {}).get(line) or [])
        else:
            reasons.pop(line, None)
    blocked = result.get("blocked_reasons") or {}
    return {
        "lines": lines,
        "attachments": proj.get("attachments"),
        "questions": proj.get("questions"),
        "reasons": {name: sentences for name, sentences in reasons.items() if name in lines},
        "base": proj.get("base"),
        "rows": proj.get("rows"),
        "blocked_reasons": {name: blocked[name] for name in sorted(blocked)},
        "presentation_valid": result.get("presentation_valid"),
    }


def _run_one(item: tuple[str, Acts]) -> tuple[str, dict[str, Any]]:
    key, acts = item
    t = track0()
    result = t.run_coordinate(published(t), acts, "demo.b4.v83." + key.replace("/", "."))
    return key, pin(cast(dict[str, Any], result))


def classify(v82: dict[str, Any], v83: dict[str, Any]) -> tuple[str, list[str]]:
    """How the v83 pin differs from the committed v82 projection.

    Lines 25d and 35a are absent from that projection, so their presence is not a difference.
    Payment lines and their rows may change, and the page may gain the amount question.
    """
    if "error" in v82 or "error" in v83:
        same = v82 == v83
        return ("identical" if same else "counterexample:error", [] if same else ["error"])
    diffs: list[tuple[str, str]] = []
    v82_lines = cast(dict[str, Any], v82.get("lines") or {})
    v83_lines = cast(dict[str, Any], v83.get("lines") or {})
    for name in sorted(set(v82_lines) | set(v83_lines)):
        if name in OVERLAY_LINES and name not in v82_lines:
            continue
        if v82_lines.get(name) != v83_lines.get(name):
            diffs.append(("line", name))
    if v82.get("attachments") != v83.get("attachments"):
        diffs.append(("attachment", ""))
    if v82.get("base") != v83.get("base"):
        diffs.append(("base", ""))
    v82_reasons = cast(dict[str, Any], v82.get("reasons") or {})
    v83_reasons = cast(dict[str, Any], v83.get("reasons") or {})
    for name in sorted(set(v82_reasons) | set(v83_reasons)):
        if name in OVERLAY_LINES and name not in v82_lines:
            continue
        if v82_reasons.get(name) != v83_reasons.get(name):
            diffs.append(("reasons", name))
    v82_rows = cast(dict[str, Any], v82.get("rows") or {})
    v83_rows = cast(dict[str, Any], v83.get("rows") or {})
    for name in sorted(set(v82_rows) | set(v83_rows)):
        if v82_rows.get(name) != v83_rows.get(name):
            diffs.append(("row", name))
    v82_questions = [str(q) for q in v82.get("questions") or []]
    v83_questions = [str(q) for q in v83.get("questions") or []]
    if v82_questions != v83_questions:
        diffs.append(("questions", ""))
    unexpected = [
        f"{kind}:{name}" if name else kind for kind, name in diffs
        if not (
            (kind in ("line", "reasons") and name in PAYMENT_LINES)
            or (kind == "row" and name in PAYMENT_ROWS)
            or (kind == "questions" and (
                any(AMOUNT_PROMPT in q for q in v82_questions) or any(AMOUNT_PROMPT in q for q in v83_questions)))
        )
    ]
    reasons = [str(s) for s in (v83_reasons.get("form1040.line-25b") or [])]
    reasons += [str(s) for s in ((v83.get("blocked_reasons") or {}).get("form1040.line-25b") or [])]
    asks = v83_lines.get("form1040.line-25b") == "blocked" and any(AMOUNT_PROMPT in sentence for sentence in reasons)
    if not diffs:
        return "identical", []
    if not unexpected and asks:
        return "box4_unanswered_asks_amount", []
    return "counterexample:" + ",".join(unexpected), unexpected


def lines_restored(v82: dict[str, Any], pinned: dict[str, Any]) -> bool:
    """Answering box 4 as $0 republishes every line the v82 projection recorded."""
    if "error" in v82 or "error" in pinned:
        return False
    if v82.get("attachments") != pinned.get("attachments") or v82.get("base") != pinned.get("base"):
        return False
    v82_lines = cast(dict[str, Any], v82.get("lines") or {})
    pin_lines = cast(dict[str, Any], pinned.get("lines") or {})
    return all(pin_lines.get(line) == value for line, value in v82_lines.items())


def with_zero(t: ModuleType, acts: Acts, core: Any) -> Acts:
    out = copy.deepcopy(acts)
    statements = cast(list[str], t.sale_statements(out))
    assert statements
    for statement in statements:
        out = cast(Acts, t.say_b4_amount(out, core, statement, 0.0))
    return out


def choose_sample(changed: list[str]) -> list[str]:
    ordered = sorted(changed)
    if not ordered:
        return []
    last = len(ordered) - 1
    picks = {ordered[int(i * last / 5)] for i in range(6)}
    if NAMED_SAMPLE in ordered:
        picks.add(NAMED_SAMPLE)
    return sorted(picks)


def _expected() -> dict[str, Any]:
    if not EXPECTED_PATH.exists():
        return {"track0": {}, "returns": {}, "zero_sample": {}, "duplicates": {"track0": {}, "returns": {}},
                "classes": {}, "no_sales_changed": []}
    return cast(dict[str, Any], json.loads(EXPECTED_PATH.read_text(encoding="utf-8")))


def _keys(group: str) -> list[str]:
    found = EXPECTED.get(group) or {}
    assert isinstance(found, dict)
    return sorted(str(key) for key in found)


EXPECTED = _expected()


_V82_RETURNS: dict[str, Any] | None = None


def _v82(key: str) -> dict[str, Any]:
    global _V82_RETURNS
    if _V82_RETURNS is None:
        table = json.loads(V82_FIXTURE.read_text(encoding="utf-8"))
        _V82_RETURNS = cast(dict[str, Any], table["v81"])
    return cast(dict[str, Any], _V82_RETURNS[key]["v82"])


def run_pin(t: ModuleType, acts: Acts, run_id: str) -> dict[str, Any]:
    return pin(cast(dict[str, Any], t.run_coordinate(published(t), acts, run_id)))


@pytest.fixture(scope="module")
def catalog(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    t = track0()
    return {
        "t": t,
        "track0": dict(decided_cases(t)),
        "returns": return_acts(t, export_returns(tmp_path_factory.mktemp("f1099b-v83"))),
    }


@pytest.mark.parametrize("key", _keys("track0"))
def test_track0_case_on_v83(catalog: dict[str, Any], key: str) -> None:
    pinned = run_pin(catalog["t"], catalog["track0"][key], "demo.b4.v83.track0." + key.replace("/", "."))
    assert pinned.get("presentation_valid") is True, key
    for line in CHARTER_LINES:
        assert line in pinned["lines"], (key, line)
    assert pinned == EXPECTED["track0"][key]


@pytest.mark.parametrize("key", _keys("returns"))
def test_return_on_v83(catalog: dict[str, Any], key: str) -> None:
    pinned = run_pin(catalog["t"], catalog["returns"][key], "demo.b4.v83.return." + key.replace("/", "."))
    assert pinned == EXPECTED["returns"][key]["v83"]
    assert classify(_v82(key), pinned)[0] == EXPECTED["returns"][key]["class"]
    # Six returns are rejected at entry on v82 and on v83, so they have no form lines.
    if "error" in pinned:
        return
    assert pinned.get("presentation_valid") is True, key
    for line in CHARTER_LINES:
        assert line in pinned["lines"], (key, line)


@pytest.mark.parametrize("key", _keys("zero_sample"))
def test_zero_box4_restores_the_v82_lines(catalog: dict[str, Any], key: str) -> None:
    acts = with_zero(catalog["t"], catalog["returns"][key], published(catalog["t"]))
    pinned = run_pin(catalog["t"], acts, "demo.b4.v83.zero." + key.replace("/", "."))
    assert pinned.get("presentation_valid") is True, key
    for line in CHARTER_LINES:
        assert line in pinned["lines"], (key, line)
    assert pinned == EXPECTED["zero_sample"][key]["v83"]
    assert lines_restored(_v82(key), pinned)
    assert EXPECTED["zero_sample"][key]["restores_v82_lines"] is True


def test_every_decided_case_and_return_is_run_once(catalog: dict[str, Any]) -> None:
    case_tasks, case_dups = split(list(catalog["track0"].items()))
    assert case_dups == EXPECTED["duplicates"]["track0"]
    assert {key for key, _acts in case_tasks} == set(EXPECTED["track0"])
    assert set(catalog["track0"]) == set(EXPECTED["track0"]) | set(case_dups)
    assert not any(key.endswith("alc_v82_answer_on_v82") for key in catalog["track0"])
    for case_id in (
            "d2_single_v82_no", "d2_two_statements_both_v82_no", "d2_mixed_statements", "d2_unanswered_statement"):
        assert "s1/" + case_id in catalog["track0"]
    return_tasks, return_dups = split(list(catalog["returns"].items()))
    assert return_dups == EXPECTED["duplicates"]["returns"]
    assert {key for key, _acts in return_tasks} == set(EXPECTED["returns"])
    assert len(catalog["returns"]) == 213
    assert NAMED_SAMPLE in catalog["returns"]


def test_return_classes_are_the_decided_design() -> None:
    got: dict[str, int] = {}
    returns = cast(dict[str, Any], EXPECTED["returns"])
    duplicates = cast(dict[str, str], EXPECTED["duplicates"]["returns"])
    for entry in returns.values():
        label = str(entry["class"])
        got[label] = got.get(label, 0) + 1
    for kept in duplicates.values():
        label = str(returns[kept]["class"])
        got[label] = got.get(label, 0) + 1
    assert got == CLASSES == EXPECTED["classes"]
    assert EXPECTED["no_sales_changed"] == []
    no_sales = [key for key, entry in returns.items() if not entry["has_sales"]]
    no_sales += [key for key, kept in duplicates.items() if not returns[kept]["has_sales"]]
    assert len(no_sales) == 39
    assert NAMED_SAMPLE in EXPECTED["zero_sample"]
    assert all(entry["restores_v82_lines"] is True for entry in EXPECTED["zero_sample"].values())


def _execute(tasks: list[tuple[str, Acts]]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    if not tasks:
        return found
    total = len(tasks)
    workers = min(8, os.cpu_count() or 4)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        done = 0
        for key, pinned in pool.map(_run_one, tasks):
            found[key] = pinned
            done += 1
            if done % 20 == 0 or done == total:
                print(f"  {done}/{total} {key}", flush=True)
    return found


def main() -> None:
    t = track0()
    print("building decided cases", flush=True)
    cases = decided_cases(t)
    with tempfile.TemporaryDirectory() as tmp:
        exported = export_returns(Path(tmp))
    returns = return_acts(t, exported)
    assert len(returns) == 213, len(returns)
    case_tasks, case_dups = split(cases)
    return_tasks, return_dups = split(list(returns.items()))
    print(f"running {len(case_tasks)} track0 cases and {len(return_tasks)} returns "
          f"({len(case_dups) + len(return_dups)} duplicate act lists skipped)", flush=True)
    ran = _execute(case_tasks + return_tasks)
    v82_table = json.loads(V82_FIXTURE.read_text(encoding="utf-8"))["v81"]
    classes: dict[str, int] = {}
    return_rows: dict[str, Any] = {}
    problems: list[dict[str, Any]] = []
    missing_lines: list[str] = []
    for key, _acts in return_tasks:
        pinned = ran[key]
        label, unexpected = classify(cast(dict[str, Any], v82_table[key]["v82"]), pinned)
        classes[label] = classes.get(label, 0) + 1
        has_sales = bool(t.sale_statements(returns[key]))
        return_rows[key] = {"class": label, "has_sales": has_sales, "v83": pinned}
        if label.startswith("counterexample"):
            problems.append({"key": key, "class": label, "unexpected": unexpected})
        if pinned.get("presentation_valid") is not True or any(line not in (pinned.get("lines") or {}) for line in CHARTER_LINES):
            missing_lines.append(key)
    no_sales_changed: list[str] = []
    for key, row in return_rows.items():
        if not row["has_sales"] and row["class"] != "identical":
            no_sales_changed.append(key)
    for key, kept in return_dups.items():
        label = str(return_rows[kept]["class"])
        classes[label] = classes.get(label, 0) + 1
        if not return_rows[kept]["has_sales"] and label != "identical":
            no_sales_changed.append(key)
    changed = [key for key, row in return_rows.items() if row["class"] == "box4_unanswered_asks_amount"]
    changed += [key for key, kept in return_dups.items() if return_rows[kept]["class"] == "box4_unanswered_asks_amount"]
    sample = choose_sample(changed)
    print(f"zero sample {len(sample)}", flush=True)
    core = published(t)
    zero_ran = _execute([(key, with_zero(t, returns[key], core)) for key in sample])
    zero_rows: dict[str, Any] = {}
    restore_failures: list[str] = []
    for key in sample:
        pinned = zero_ran[key]
        restored = lines_restored(cast(dict[str, Any], v82_table[key]["v82"]), pinned)
        zero_rows[key] = {"restores_v82_lines": restored, "v83": pinned}
        if not restored or pinned.get("presentation_valid") is not True or any(
                line not in (pinned.get("lines") or {}) for line in CHARTER_LINES):
            restore_failures.append(key)
    for key, pinned in ran.items():
        if key in return_rows:
            continue
        if pinned.get("presentation_valid") is not True or any(line not in (pinned.get("lines") or {}) for line in CHARTER_LINES):
            missing_lines.append(key)
    table = {
        "classes": classes,
        "duplicates": {"returns": return_dups, "track0": case_dups},
        "no_sales_changed": sorted(no_sales_changed),
        "returns": return_rows,
        "track0": {key: ran[key] for key, _acts in case_tasks},
        "zero_sample": zero_rows,
    }
    text = cast(str, t.h.scrub(json.dumps(table, indent=2, sort_keys=True) + "\n"))
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"fixture contains {needle}")
    EXPECTED_PATH.parent.mkdir(parents=True, exist_ok=True)
    EXPECTED_PATH.write_text(text, encoding="utf-8")
    summary = {
        "classes": classes,
        "track0": len(case_tasks),
        "track0_duplicates": len(case_dups),
        "returns": len(return_tasks),
        "return_duplicates": len(return_dups),
        "problems": problems[:20],
        "missing_lines": missing_lines[:20],
        "missing_line_count": len(missing_lines),
        "restore_failures": restore_failures,
        "no_sales_changed": sorted(no_sales_changed),
        "zero_sample": sample,
    }
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    # Spawned workers re-import this file as __main__. The env var stops them from regenerating.
    if os.environ.get("F1099B_V83_WORKER") != "1":
        os.environ["F1099B_V83_WORKER"] = "1"
        main()
