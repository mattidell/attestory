"""Replay the recorded core v83 returns on published v86 and scratch v87.

Evidence for docs/phases/engine-breadth/milestones/question-wording.md.
Charter: docs/reviews/question-wording/charter-p0.md.

The 298 act lists are the ones
tests/test_f1099b_selection_keyed_collect_v86.py replays from
tests/fixtures/f1099b_backup_withholding_v83/expected.json. The 207
identical lists are used as recorded. The 91 that core v85 asks for a
no-sale box 4 statement are restored with present=no, which is how that
test replays them on v86. No answer is rewritten for the new sentences.

Each list runs once on published v86 and once on the scratch core. A change
is identical, numbers_identical_sentences_changed, or numbers_changed. Each
v86 pin is also compared with the recorded fixture pin.

    python3 rerun.py shard <scratch>/core.json <i> <n> <scratch>/part-<i>.json
    python3 rerun.py merge <scratch>/part-*.json
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

EXPECTED = REPO / "tests/fixtures/f1099b_backup_withholding_v83/expected.json"
TEST = REPO / "tests/test_f1099b_backup_withholding_v83.py"
HARNESS = REPO / "docs/phases/engine-breadth/milestones/sale-family-audit-evidence/audit_harness.py"
NEIGHBOUR = REPO / "docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/track0-neighbour.json"
PRESENT = "tax.us.2025.f1099b.no-sale-box4-present"
SENTENCE_FIELDS = ("questions", "reasons", "blocked_reasons")


def _module(name: str, path: Path) -> Any:
    module = sys.modules.get(name)
    if module is None:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return module


def load_test() -> Any:
    return _module("qw_p0_rerun_v83_test", TEST)


def load_harness() -> Any:
    return _module("qw_p0_rerun_harness", HARNESS)


def scratch_core(test: Any, core_path: Path) -> Any:
    body = json.loads(core_path.read_text(encoding="utf-8"))
    return test.track0().h.Core(
        body["version"], body["registry"], body["release_version"],
        content=Path(body["content"]), releases=Path(body["releases"]),
        loader_from=body.get("loader_from"),
    )


def published_v86(test: Any) -> Any:
    return test.track0().h.Core("v86", "v84", "v84")


def _diff(left: Any, right: Any) -> list[str]:
    if left == right:
        return []
    if not isinstance(left, dict) or not isinstance(right, dict):
        return ["pin"]
    found = []
    for key in sorted(set(left) | set(right)):
        if left.get(key) == right.get(key):
            continue
        if isinstance(left.get(key), dict) and isinstance(right.get(key), dict):
            for name in sorted(set(left[key]) | set(right[key])):
                if left[key].get(name) != right[key].get(name):
                    found.append(f"{key}.{name}")
        else:
            found.append(str(key))
    return found


def _view(pin: dict[str, Any], fields: tuple[str, ...], keep: bool) -> dict[str, Any]:
    if keep:
        return {key: pin.get(key) for key in fields}
    return {key: value for key, value in pin.items() if key not in fields}


def _scalar(value: Any) -> Any:
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return type(value).__name__


def classify(v86: dict[str, Any], v87: dict[str, Any]) -> dict[str, Any]:
    if v86 == v87:
        return {"class": "identical"}
    number_fields = _diff(_view(v86, SENTENCE_FIELDS, False), _view(v87, SENTENCE_FIELDS, False))
    sentence_fields = _diff(_view(v86, SENTENCE_FIELDS, True), _view(v87, SENTENCE_FIELDS, True))
    if number_fields or "error" in v86 or "error" in v87:
        lines = []
        left = v86.get("lines") or {}
        right = v87.get("lines") or {}
        if isinstance(left, dict) and isinstance(right, dict):
            for name in sorted(set(left) | set(right)):
                if left.get(name) != right.get(name):
                    lines.append({"line": name, "v86": _scalar(left.get(name)), "v87": _scalar(right.get(name))})
        return {
            "class": "numbers_changed",
            "number_fields": number_fields[:40],
            "sentence_fields": sentence_fields[:40],
            "lines": lines[:30],
            "v86_error": _scalar(v86.get("error")),
            "v87_error": _scalar(v87.get("error")),
        }
    if sentence_fields:
        return {"class": "numbers_identical_sentences_changed", "sentence_fields": sentence_fields[:40]}
    return {"class": "numbers_changed", "number_fields": ["unclassified"]}


def _pin_run(test: Any, core: Any, acts: list[dict[str, Any]], run_id: str) -> dict[str, Any]:
    track = test.track0()
    with track.h.loader_entries(core):
        return test.pin(track.run_coordinate(core, acts, run_id))


def _pair(test: Any, v86: Any, v87: Any, key: str, acts: list[dict[str, Any]],
          recorded: dict[str, Any]) -> dict[str, Any]:
    slug = key.replace("/", ".")
    pin87 = _pin_run(test, v87, acts, "demo.qw.p0.v87." + slug)
    pin86 = _pin_run(test, v86, acts, "demo.qw.p0.v86." + slug)
    row = classify(pin86, pin87)
    # The v86 replay must reproduce the recorded pin, as the v86 test asserts.
    row["v86_matches_fixture"] = pin86 == recorded
    return row


def recorded_pin(expected: dict[str, Any], key: str) -> dict[str, Any]:
    group, _, name = key.partition("/")
    if group == "track0":
        return expected["track0"][name]
    if group == "returns":
        return expected["returns"][name]["v83"]
    return expected["zero_sample"][name]["v83"]


def tasks(test: Any, harness: Any, expected: dict[str, Any], asks: set[str]) -> list[tuple[str, list[dict[str, Any]]]]:
    track = test.track0()
    print("building track 0 act lists", flush=True)
    cases = dict(test.decided_cases(track))
    print("exporting the recorded returns", flush=True)
    with tempfile.TemporaryDirectory() as tmp:
        exported = test.export_returns(Path(tmp))
    returns = test.return_acts(track, exported)
    core = published_v86(test)
    out: list[tuple[str, list[dict[str, Any]]]] = []
    for key in expected["track0"]:
        out.append((f"track0/{key}", cases[key]))
    for key in expected["returns"]:
        out.append((f"returns/{key}", returns[key]))
    for key in expected["zero_sample"]:
        out.append((f"zero/{key}", test.with_zero(track, returns[key], core)))
    restored = []
    for key, acts in out:
        if key in asks:
            acts = harness.say(acts, PRESENT, "no", "qw.restore")
        restored.append((key, acts))
    return restored


def _redact(text: str) -> str:
    return re.sub(r"(?:/Users|/private|/tmp|/var)/\S+", "[path]", text)


def run_shard(core_path: Path, shard: int, count: int, out_path: Path) -> None:
    """Run every ``count``-th recorded list from ``shard`` and write its rows to ``out_path``."""
    neighbour = json.loads(NEIGHBOUR.read_text(encoding="utf-8"))
    asks = set(neighbour["asks_no_sale_present_ids"])
    test = load_test()
    harness = load_harness()
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    work = tasks(test, harness, expected, asks)
    fixture_ids = [key for key, _acts in work]
    if len(fixture_ids) != 298 or len(set(fixture_ids)) != 298:
        raise SystemExit(f"expected 298 recorded ids, found {len(fixture_ids)}")
    if asks - set(fixture_ids) or len(asks) != 91:
        raise SystemExit("restore ids do not match the recorded fixture")
    only = {item for item in os.environ.get("QW_RERUN_ONLY", "").split(",") if item}
    if only:
        work = [item for item in work if item[0] in only]
    work = work[shard::count]
    v87 = scratch_core(test, core_path)
    v86 = published_v86(test)
    # A part file left by an interrupted shard is resumed, not redone.
    found: dict[str, Any] = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    for index, (key, acts) in enumerate(work, 1):
        if key in found:
            continue
        found[key] = _pair(test, v86, v87, key, acts, recorded_pin(expected, key))
        found[key]["restored_present_no"] = key in asks
        out_path.write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
        print(f"shard {shard}: {index}/{len(work)} {key} {found[key]['class']}", flush=True)


def merge(parts: list[Path]) -> None:
    found: dict[str, Any] = {}
    for part in parts:
        found.update(json.loads(part.read_text(encoding="utf-8")))
    counts = dict(Counter(row["class"] for row in found.values()))
    changes = [{"id": key, **found[key]} for key in sorted(found) if found[key]["class"] != "identical"]
    payload = {
        "fixture": "tests/fixtures/f1099b_backup_withholding_v83/expected.json",
        "replay": (
            "298 act lists from tests/test_f1099b_selection_keyed_collect_v86.py: "
            "207 as recorded, 91 restored with no-sale box 4 present=no"
        ),
        "cores": "published core v86 and scratch core v87, answered as recorded",
        "classes_defined": {
            "identical": "the v86 and v87 pins are equal",
            "numbers_identical_sentences_changed": "only questions, reasons or blocked reasons differ",
            "numbers_changed": "a line, attachment, base or row differs, or one core errors",
        },
        "runs": len(found),
        "live_runs": len(found) * 2,
        "restored_present_no": sum(1 for row in found.values() if row.get("restored_present_no")),
        "v86_matches_fixture": sum(1 for row in found.values() if row.get("v86_matches_fixture")),
        "counts": counts,
        "classes": {key: found[key]["class"] for key in sorted(found)},
        "changes": changes,
        "change_count": len(changes),
    }
    text = _redact(json.dumps(payload, indent=2) + "\n")
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"rerun output contains {needle}")
    (HERE / "rerun-output.json").write_text(text, encoding="utf-8")
    print(json.dumps({"runs": len(found), "counts": counts, "v86_matches_fixture": payload["v86_matches_fixture"],
                      "output": "rerun-output.json"}, indent=2))


def main() -> None:
    """``rerun.py shard <core.json> <i> <n> <part.json>`` or ``rerun.py merge <part.json>...``.

    The evidence loader's module table refuses a process pool, so shards are
    separate processes. Part files belong outside the repository.
    """
    if len(sys.argv) >= 2 and sys.argv[1] == "merge":
        merge([Path(arg) for arg in sys.argv[2:]])
        return
    if len(sys.argv) != 6 or sys.argv[1] != "shard":
        raise SystemExit(main.__doc__)
    run_shard(Path(sys.argv[2]).resolve(), int(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))


if __name__ == "__main__":
    main()
