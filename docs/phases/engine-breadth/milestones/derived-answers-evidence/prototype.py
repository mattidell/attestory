"""Scratch core v74 for derived answers. Evidence only.

Nothing is written under packages/. The script copies the committed content
and release directories to a temporary directory, writes the successor rules
there, builds package v74 / registry v72 / release v72, and runs the probe's
cases through live_coordinate_run. An answered return is also run on the
copied v73 so the presentation can be compared after the successor rule
versions are rewritten to the v73 versions.

    python3 docs/phases/engine-breadth/milestones/derived-answers-evidence/prototype.py

Writes prototype-output.json and one JSON file per successor rule beside
itself. Synthetic demo.* data only. Cases already recorded as ran are kept.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import probe  # noqa: E402
from packages.tax import loader  # noqa: E402
from tests import test_input_questions as miq  # noqa: E402
from tests import test_w2g_gambling as w2g  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
V74 = "v74"
SCOPE = P + "f1098-scope.no-mortgage-statement"
INT = P + "line2a-scope.no-f1099int-tax-exempt"
OD = P + "ctc.no-other-dependent"
F1116 = P + "direct-ftc-scope.no-form-1116-required"
BOX8 = P + "interest.b8-tax-exempt-subtotal"
LINE8A = P + "schedule-a.line8a"
LINE16 = P + "schedule-a.line16"
CHILD_BOX = P + "odc.child.other-dependent-box"
CHILD_ROSTER = P + "odc.child-roster"
REL_BOX = P + "odc.dependent.other-dependent-box"
REL_ROSTER = P + "odc.relative-roster"
NOTE = "Scratch evidence for derived-answers P0. Not a citizen."

# Successor version, rewritten back to this for the presentation comparison.
VERSIONS = {
    P + "rule.form1040-line12e": ("v4", "v3"),
    P + "rule.form1040-line2a": ("v5", "v4"),
    P + "rule.schedule3-line1-direct-ftc": ("v4", "v3"),
    P + "rule.odc-dependent-present": ("v2", "v1"),
    P + "rule.ctc-sch8812-line-6": ("v3", "v2"),
    P + "rule.odc-child-marked-conflict": ("v2", "v1"),
    P + "rule.odc-relative-marked-conflict": ("v2", "v1"),
}
# Answered returns, where v74 should compute as v73.
ANSWERED = ("base", "m1-agreed", "l2a-agreed", "ctc-agreed", "ftc-under-yes", "ftc-over-yes")
# Proved and unanswered, compared with the answered return that has the same record.
PROVED = {
    "m1-proved-unanswered": "m1-agreed",
    "m1-joint-proved-unanswered": None,
    "l2a-proved-unanswered": "l2a-agreed",
    "ctc-proved-unanswered": "ctc-agreed",
    "ftc-over-unanswered": "ftc-over-yes",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _drop_fact(rule: dict[str, Any], fact: str) -> None:
    rule["requires"] = [name for name in rule["requires"] if name != fact]
    rule["pins"] = [pin for pin in rule["pins"] if pin.get("id") != fact]
    missing = rule.get("blocked", {}).get("missing")
    if isinstance(missing, list):
        rule["blocked"]["missing"] = [name for name in missing if name != fact]


def _count_gt(fact: str, source: str) -> dict[str, Any]:
    return {
        "op": "compare", "cmp": "gt",
        "left": {"op": "count", "name": fact, "source_set": source},
        "right": 0,
    }


def _marked() -> dict[str, Any]:
    return {"op": "any", "args": [
        _count_gt(CHILD_BOX, CHILD_ROSTER),
        _count_gt(REL_BOX, REL_ROSTER),
    ]}


def _gt_subtotal() -> dict[str, Any]:
    return {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": BOX8}, "right": 0}


def _line12e(content: Path) -> dict[str, Any]:
    rule = _load(content / "rule.form1040-line12e.v3.json")
    _drop_fact(rule, SCOPE)
    itemized = rule["value"]["then"]
    if itemized.get("op") != "max":
        raise SystemExit("line 12e itemized side is not the max")
    rule["value"]["then"]["args"][1] = {
        "op": "choose",
        "when": _count_gt(P + "f1098.box1-mortgage-interest", P + "f1098"),
        "then": {"op": "add", "args": [
            {"op": "ref", "name": LINE8A}, {"op": "ref", "name": LINE16},
        ]},
        "else": itemized["args"][1],
    }
    rule["version"] = "v4"
    rule["notes"] = NOTE + " Count of Form 1098 box 1 greater than 0 takes the statement path and does not read the scope answer."
    return rule


def _line2a(content: Path) -> dict[str, Any]:
    rule = _load(content / "rule.form1040-line2a.v4.json")
    _drop_fact(rule, INT)
    choose = rule["when"]["args"][-1]
    if choose.get("op") != "choose":
        raise SystemExit("line 2a when does not end in the scope choose")
    rule["when"]["args"][-1] = {
        "op": "choose", "when": _gt_subtotal(), "then": True, "else": choose,
    }
    add = rule["value"]["value"]
    if add.get("op") != "add" or add["args"][1].get("op") != "choose":
        raise SystemExit("line 2a value is not the subtotal choose")
    add["args"][1] = {
        "op": "choose", "when": _gt_subtotal(),
        "then": {"op": "ref", "name": BOX8}, "else": add["args"][1],
    }
    rule["version"] = "v5"
    rule["notes"] = NOTE + " A closed box 8 subtotal greater than 0 is the 1099-INT contribution and the scope answer is not read."
    return rule


def _direct_ftc(content: Path) -> dict[str, Any]:
    rule = _load(content / "rule.schedule3-line1-direct-ftc.v3.json")

    def strip(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "conditional_dependency_set":
                node["members"] = [member for member in node["members"] if member.get("name") != F1116]
            for value in node.values():
                strip(value)
        elif isinstance(node, list):
            for value in node:
                strip(value)

    strip(rule["when"])
    rule["version"] = "v4"
    rule["notes"] = NOTE + " Form 1116 is not read when box 7 is over the cap; under the cap it is still read."
    return rule


def _silence_marked(rule: dict[str, Any]) -> None:
    hits = [path for path in rule["selection"]["paths"] if OD in path.get("requires", [])]
    if len(hits) != 1:
        raise SystemExit(f"{rule['id']} marked paths: {len(hits)}")
    hits[0]["requires"] = []
    hits[0]["pins"] = []
    hits[0]["value"] = 0


def _dependent_present(content: Path) -> dict[str, Any]:
    rule = _load(content / "rule.odc-dependent-present.json")
    _drop_fact(rule, OD)
    current = rule["value"]
    if current.get("op") != "choose" or current["else"].get("op") != "choose":
        raise SystemExit("dependent-present shape changed")
    rule["value"] = {
        "op": "choose", "when": _marked(),
        "then": copy.deepcopy(current["else"]["then"]),
        "else": current,
    }
    rule["version"] = "v2"
    rule["notes"] = NOTE + " A marked other-dependent box takes the counted branch and does not read the return answer."
    return rule


def _line6(content: Path) -> dict[str, Any]:
    rule = _load(content / "rule.ctc-sch8812-line-6.v2.json")
    _drop_fact(rule, OD)
    inner = rule["value"]["then"]
    if inner.get("op") != "choose" or inner["else"].get("op") != "choose":
        raise SystemExit("line 6 shape changed")
    rule["value"]["then"] = {
        "op": "choose", "when": _marked(),
        "then": copy.deepcopy(inner["else"]["then"]),
        "else": inner,
    }
    rule["version"] = "v3"
    rule["notes"] = NOTE + " A marked other-dependent box sums the roster counts and does not read the return answer."
    return rule


def _conflict(content: Path, filename: str) -> dict[str, Any]:
    rule = _load(content / filename)
    _silence_marked(rule)
    rule["version"] = "v2"
    rule["notes"] = NOTE + " A marked row publishes 0 and does not read the return answer."
    return rule


def _rules(content: Path) -> list[tuple[str, dict[str, Any]]]:
    return [
        ("rule.form1040-line12e.v4.json", _line12e(content)),
        ("rule.form1040-line2a.v5.json", _line2a(content)),
        ("rule.schedule3-line1-direct-ftc.v4.json", _direct_ftc(content)),
        ("rule.odc-dependent-present.v2.json", _dependent_present(content)),
        ("rule.ctc-sch8812-line-6.v3.json", _line6(content)),
        ("rule.odc-child-marked-conflict.v2.json", _conflict(content, "rule.odc-child-marked-conflict.json")),
        ("rule.odc-relative-marked-conflict.v2.json", _conflict(content, "rule.odc-relative-marked-conflict.json")),
    ]


def _member(package: dict[str, Any], rule_id: str, version: str) -> dict[str, Any]:
    hits = [member for member in package["members"] if member.get("id") == rule_id and member.get("version") == version]
    if len(hits) != 1:
        raise SystemExit(f"member {rule_id}@{version}: {len(hits)}")
    return hits[0]


def build(scratch: Path) -> None:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(ccr.CONTENT, content)
    shutil.copytree(ccr.RELEASE_DIR, releases)
    package = _load(content / "package.core-calculations.v73.json")
    edits = []
    entrypoints = []
    for filename, rule in _rules(content):
        text = json.dumps(rule, indent=2) + "\n"
        (content / filename).write_text(text, encoding="utf-8")
        (HERE / filename).write_text(text, encoding="utf-8")
        old_version = VERSIONS[rule["id"]][1]
        old = _member(package, rule["id"], old_version)
        edits.append({
            "op": "replace", "old": old,
            "new": {"id": rule["id"], "role": "computation", "schema": rule["schema"], "version": rule["version"]},
        })
        old_entry = {"id": rule["id"], "version": old_version}
        if old_entry in package.get("entrypoints", []):
            entrypoints.append({"op": "replace", "old": old_entry, "new": {"id": rule["id"], "version": rule["version"]}})
    changes = {
        "package_version": "v74", "release_version": "v72",
        "members": edits,
        "entrypoints": entrypoints,
        "registry_sort": "id_version", "registry_new_key_order": ["checksum", "id", "version"],
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v73.json",
        content / "published-packages.v71.json",
        releases / "demo.release.sli-worksheet-integration.2025.v71.json",
        content, scratch / "changes.json", scratch / "out")
    inherited = report.get("inherited_inconsistencies")
    print("successor", report["package"]["version"], "inherited", inherited, flush=True)
    for name, folder, target in (
        ("package.json", "content", "package.core-calculations.v74.json"),
        ("registry.json", "content", "published-packages.v72.json"),
        ("release.json", "releases", "demo.release.sli-worksheet-integration.2025.v72.json"),
    ):
        shutil.copy(scratch / "out" / name, scratch / folder / target)
    probe.swa.CONTENT = content
    probe.swa.RELEASE_DIR = releases
    probe.swa.CORES[V74] = (
        "package.core-calculations.v74.json", "v74",
        "demo.release.sli-worksheet-integration.2025.v72.json", "v72",
        "published-packages.v72.json",
    )
    # The copied v73 files answer under the same content root.
    probe.swa.CORES["v73"] = (
        "package.core-calculations.v73.json", "v73",
        "demo.release.sli-worksheet-integration.2025.v71.json", "v71",
        "published-packages.v71.json",
    )
    original = loader.domain_package_companion_declarations

    def with_v74() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(original())
        key = ("tax.us.2025.package.core-calculations", "v73")
        declarations[("tax.us.2025.package.core-calculations", "v74")] = declarations[key]
        return declarations

    loader.domain_package_companion_declarations = with_v74  # type: ignore[assignment]


def _same(left: Any, right: Any) -> bool:
    if left == right:
        return True
    try:
        return Decimal(str(left)) == Decimal(str(right))
    except Exception:
        return False


def _summarize(run: probe.swa.Run, question: str) -> dict[str, Any]:
    blocked = miq.blocked(run.model)
    asked = sorted(
        line for line, reasons in blocked.items()
        if reasons and any(question in sentence for sentence in reasons)
    ) if question else []
    pubs = {}
    for symbol, finding in run.pubs.items():
        short = symbol.replace(P, "")
        if short in probe.WATCH:
            pubs[short] = finding.get("value")
    rows = []
    for row in run.dispositions:
        artifact = str(row.get("artifact_id", "")).replace(P + "rule.", "")
        if artifact in probe.RULES and row.get("disposition") != "computed":
            rows.append({
                "rule": artifact,
                "disposition": row.get("disposition"),
                "code": row.get("code"),
                "missing": [str(item).replace(P, "") for item in row.get("missing", []) or []],
            })
    return {"blocked": len(blocked), "blocked_ids": sorted(blocked), "asked": asked, "lines": pubs, "held": rows}


def _normalize(node: Any) -> Any:
    if isinstance(node, dict):
        out = {key: _normalize(value) for key, value in node.items()}
        pair = VERSIONS.get(str(out.get("id")))
        if pair is not None and out.get("version") == pair[0]:
            out["version"] = pair[1]
        return out
    if isinstance(node, list):
        return [_normalize(value) for value in node]
    return node


def _pins(model: Any) -> list[str]:
    found: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("role") == "input" and isinstance(node.get("id"), str):
                found.add(node["id"].replace(P, ""))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(model)
    return sorted(found)


def _run(acts: list[dict[str, object]], run_id: str, question: str, core: str) -> dict[str, Any]:
    try:
        result = probe.swa.run(acts, f"demo.p0.da.{core}.{run_id}", core)
    except Exception as exc:
        return {"run_id": run_id, "status": "error", "error": f"{type(exc).__name__}: {exc}"}
    summary = _summarize(result, probe.QUESTIONS.get(question, "___"))
    summary["run_id"] = run_id
    summary["status"] = "ran"
    summary["presentation"] = result.model
    return summary


def _public(row: dict[str, Any]) -> dict[str, Any]:
    """Drop the presentation from what is written. It is only compared in memory."""
    return {key: value for key, value in row.items() if key != "presentation"}


def _compare_values(left: dict[str, Any], right: dict[str, Any]) -> list[str]:
    keys = sorted(set(left) | set(right))
    return [key for key in keys if not _same(left.get(key), right.get(key))]


def extra_cases() -> list[tuple[str, str, Callable[[], list[dict[str, object]]]]]:
    """Joint box 7 around the $600 cap. The probe's foreign-tax cases are single."""
    def build(amount: float) -> list[dict[str, object]]:
        return probe._drop(
            ccr.add_foreign_tax_1099div(w2g._w2g_return([], joint=True), [amount]),
            probe.F1116)
    return [
        ("ftc-joint-500-unanswered", "ftc", lambda: build(500.0)),
        ("ftc-joint-700-unanswered", "ftc", lambda: build(700.0)),
    ]


def main() -> None:
    v73 = {row["run_id"]: row for row in json.loads((HERE / "probe-output.json").read_text(encoding="utf-8"))["cases"]}
    out_path = HERE / "prototype-output.json"
    done: dict[str, Any] = {}
    if out_path.exists():
        done = {row["run_id"]: row for row in json.loads(out_path.read_text(encoding="utf-8")).get("cases", [])}
    table = list(probe.case_table()) + extra_cases()
    cases: list[dict[str, Any]] = []
    presentations: dict[str, Any] = {}
    with tempfile.TemporaryDirectory() as tmp:
        build(Path(tmp).resolve() / "s")
        for run_id, question, builder in table:
            if run_id in done and done[run_id].get("status") == "ran":
                cases.append(done[run_id])
                print(run_id, "kept", flush=True)
                continue
            acts = None
            try:
                acts = builder()
                row = _run(acts, run_id, question, V74)
            except Exception as exc:
                row = {"run_id": run_id, "status": "error", "error": f"{type(exc).__name__}: {exc}"}
            if acts is not None and row.get("status") == "ran" and (run_id in ANSWERED or run_id.startswith("ftc-joint")):
                other = _run(acts, run_id, question, "v73")
                if other.get("status") == "ran" and run_id in ANSWERED:
                    left = _pins(row["presentation"])
                    right = _pins(other["presentation"])
                    presentations[run_id] = {
                        "values_equal": _compare_values(row["lines"], other["lines"]) == [],
                        "value_diffs": _compare_values(row["lines"], other["lines"]),
                        "normalized_equal": _normalize(row["presentation"]) == _normalize(other["presentation"]),
                        "pins_only_v73": sorted(set(right) - set(left)),
                        "pins_only_v74": sorted(set(left) - set(right)),
                    }
                elif other.get("status") == "ran":
                    presentations[run_id] = {
                        "v73_asked": other.get("asked"),
                        "v74_asked": row.get("asked"),
                        "v73_blocked": other.get("blocked"),
                        "v74_blocked": row.get("blocked"),
                        "direct_ftc_v73": (other.get("lines") or {}).get("schedule3.line1-direct-ftc"),
                        "direct_ftc_v74": (row.get("lines") or {}).get("schedule3.line1-direct-ftc"),
                    }
                else:
                    presentations[run_id] = {"v73_status": other.get("status"), "v73_error": other.get("error")}
            public = _public(row)
            print(run_id, public.get("status"), public.get("asked"), public.get("lines"), flush=True)
            cases.append(public)
            _write(out_path, cases, presentations, v73)
    _write(out_path, cases, presentations, v73)
    print("wrote", out_path.name, flush=True)


def _released(v74: dict[str, Any], prior: dict[str, Any]) -> dict[str, Any]:
    asked = prior.get("asked") or []
    blocked_ids = set(v74.get("blocked_ids") or [])
    cleared = [line for line in asked if line not in blocked_ids]
    drop = None
    if isinstance(prior.get("blocked"), int) and isinstance(v74.get("blocked"), int):
        drop = prior["blocked"] - v74["blocked"]
    return {"question_lines_cleared": cleared, "blocked_drop": drop}


def _write(path: Path, cases: list[dict[str, Any]], presentations: dict[str, Any], v73: dict[str, Any]) -> None:
    by_id = {row["run_id"]: row for row in cases}
    released = {}
    proved_match = {}
    for run_id, prior in v73.items():
        if run_id not in by_id or by_id[run_id].get("status") != "ran" or prior.get("status") != "ran":
            continue
        released[run_id] = _released(by_id[run_id], prior)
    for run_id, agreed_id in PROVED.items():
        if agreed_id is None or run_id not in by_id or agreed_id not in v73:
            continue
        if by_id[run_id].get("status") != "ran":
            continue
        proved_match[run_id] = _compare_values(by_id[run_id].get("lines") or {}, v73[agreed_id].get("lines") or {})
    payload = {
        "core": V74,
        "predecessor": "v73",
        "rules": {rule_id.replace(P, ""): new for rule_id, (new, _old) in VERSIONS.items()},
        "cases": cases,
        "lines_released": released,
        "proved_versus_agreed_diffs": proved_match,
        "presentation": presentations,
        "fixtures_moved": 0,
    }
    path.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
