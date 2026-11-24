from __future__ import annotations

"""P0 content-route probes for a code W gain.

Scratch successors of published core v103. Each route is one of: an input
question for the adjustment fact the block reads, a declared missing name
on the synthesized validation rule, a closure question, or a line-1b
successor that tries to put a name where the page walk already looks.
Nothing in packages/ is edited. Family bytes are copied and left unchanged.

Run: python3 routes.py <new-scratch-directory> --out <results.json>

The scratch directory must not exist. Its parent must not be a symlink,
because package successor installation refuses a symlinked parent.
"""

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"core": "v103", "registry": "v101", "release": "v101"}
TO = {"core": "v104", "registry": "v102", "release": "v102"}
P = "tax.us.2025."
LINE = P + "rule.schedule-d-line1b"
ADJ = P + "f1099b.covered-w-st-txn.adjustment"
PROCEEDS = P + "f1099b.covered-w-st-proceeds-subtotal"
BASIS = P + "f1099b.covered-w-st-basis-subtotal"
ADJ_SUB = P + "f1099b.covered-w-st-adjustment-subtotal"
FAMILY = P + "f1099b.covered-w-st"
QUESTION_ID = P + "input-question.f1099b-covered-w-st-adjustment"
CLOSURE_ID = P + "closure-mapping.cwg-code-w-on-gain"
PROBE_RULE = P + "rule.cwg-p0-validation-probe"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
FAMILIES = (
    "family.f1099b-covered-w-st.v2.json",
    "family.f1099b-covered-w-lt.v2.json",
    "family.f1099b-noncovered-st.json",
    "family.f1099b-noncovered-lt.json",
)
CASES = ("covered/st/gain", "covered/st/loss")
LOSS_BASELINE = (
    "covered/st/loss",
    "covered/lt/loss",
    "noncovered/st/loss",
    "noncovered/lt/loss",
)


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


trace = _load("cwg_p0_trace", HERE / "trace.py")
sizes = _load("cwg_p0_content_file_sizes", REPO / "tests/test_content_file_sizes.py")

from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.kernel.schema_registry import SchemaValidationError  # noqa: E402
from tools.package_successor import SuccessorError, generate_to_directory  # noqa: E402


def _scrub(text: str) -> str:
    return re.sub(r"/(?:Users|private|tmp|var|opt)/\S+", "<path>", text)


def _dump(body: dict[str, Any]) -> str:
    return json.dumps(body, indent=2) + "\n"


def _question() -> dict[str, Any]:
    return {
        "schema": "input-question.v1",
        "id": QUESTION_ID,
        "version": "v1",
        "fact_type": {"id": ADJ, "version": "v1"},
        "question": (
            "What is the nondeductible wash-sale loss for this covered short-term sale "
            "(Form 1099-B box 1g), as a positive number, or 0 if no part of the loss is a wash sale?"
        ),
    }


def _line(kind: str) -> dict[str, Any]:
    body = json.loads((REPO / "packages/content/tax/2025/rule.schedule-d-line1b.v3.json").read_text())
    body["version"] = "v4"
    body["notes"] = body["notes"] + " Scratch probe: " + kind + "."
    if kind == "blocked-missing":
        body["blocked"]["missing"] = [*body["blocked"]["missing"], ADJ]
        return body
    body["schema"] = "rule-artifact.v17"
    body.pop("accounts_for", None)
    if kind == "expression-block":
        body["when"] = {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": [ADJ]}
    elif kind == "conditional-block":
        original = body["when"]
        body["when"] = {
            "op": "choose",
            "when": {
                "op": "all",
                "args": [
                    {"op": "compare", "cmp": "gte", "left": {"op": "ref", "name": PROCEEDS}, "right": {"op": "ref", "name": BASIS}},
                    {"op": "compare", "cmp": "gt", "left": {"op": "ref", "name": ADJ_SUB}, "right": 0},
                ],
            },
            "then": {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": [ADJ]},
            "else": original,
        }
    elif kind == "closure-family-on-line":
        body["when"] = {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": [FAMILY]}
    else:
        raise ValueError(kind)
    return body


def _closure(content: Path) -> dict[str, Any]:
    source = json.loads((content / "closure-mapping.f1099b-covered-w-st.v3.json").read_text())
    return {
        "schema": "source-closure-mapping.v3",
        "id": CLOSURE_ID,
        "version": "v1",
        "family": {"id": "CODE_W_ON_GAIN", "version": "v1"},
        "member_fact_type": source["member_fact_type"],
        "closure_fact_type": source["closure_fact_type"],
        "closure_horizon_key": source["closure_horizon_key"],
        "closure_question": (
            "If this sale is not a loss, what should column (g) be for the wash-sale "
            "amount: 0, or only the nondeductible wash-sale loss?"
        ),
        "admits_symbol": P + "cwg.p0.code-w-on-gain",
        "admission": {"condition": "current-literal-true"},
    }


def _probe_rule() -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v5",
        "id": PROBE_RULE,
        "version": "v1",
        "role": "computation",
        "scope": SCOPE,
        "publishes": FAMILY + ".member-validation",
        "requires": [],
        "pins": [],
        "when": True,
        "value": True,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [ADJ]},
    }


def _pin(body: dict[str, Any], role: str) -> dict[str, str]:
    return {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}


def _changes(written: dict[str, tuple[dict[str, Any], str]], replace_line: dict[str, Any] | None) -> dict[str, Any]:
    members: list[dict[str, Any]] = []
    entrypoints: list[dict[str, Any]] = []
    if replace_line is not None:
        old = {"id": LINE, "version": "v3", "schema": "rule-artifact.v5", "role": "computation"}
        members.append({"op": "replace", "old": old, "new": _pin(replace_line, "computation")})
        entrypoints.append({
            "op": "replace",
            "old": {"id": LINE, "version": "v3"},
            "new": {"id": LINE, "version": "v4"},
        })
    for body, role in written.values():
        if body["id"] == LINE:
            continue
        members.append({"op": "add", "new": _pin(body, role)})
        entrypoints.append({"op": "add", "value": {"id": body["id"], "version": body["version"]}})
    return {
        "package_version": TO["core"],
        "release_version": TO["release"],
        "members": members,
        "entrypoints": entrypoints,
        "registry_sort": "id_version",
    }


def _family_hashes(content: Path) -> dict[str, str]:
    found = {}
    for name in FAMILIES:
        found[name] = hashlib.sha256((content / name).read_bytes()).hexdigest()
    return found


def _install(route: Path, content: Path, releases: Path) -> dict[str, Any]:
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['core']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{STEM}.{FROM['release']}.json",
        content,
        route / "changes.json",
        route / "generated",
    )
    for src, dst in (
        ("package.json", content / f"package.core-calculations.{TO['core']}.json"),
        ("registry.json", content / f"published-packages.{TO['registry']}.json"),
        ("release.json", releases / f"{STEM}.{TO['release']}.json"),
    ):
        shutil.copyfile(route / "generated" / src, dst)
    kept = {key: value for key, value in report.items() if isinstance(value, (str, int, bool))}
    kept["package_version"] = report["package"]["version"]
    kept["registry_sha256"] = report["registry_sha256"]
    return kept


def _brief(result: dict[str, Any]) -> dict[str, Any]:
    if "error" in result or "refusal" in result:
        return {key: result[key] for key in ("error", "message", "refusal", "detail") if key in result}
    page = [
        row for row in result.get("page") or []
        if row.get("field") in {"schedule-d.line-1b", "schedule-d.line-2"}
    ]
    line_row = next((row for row in result.get("blocked_focus") or [] if str(row.get("artifact")).endswith("schedule-d-line1b")), None)
    return {
        "stop": result.get("stop"),
        "question_group_count": result.get("question_group_count"),
        "line_page": page,
        "line_blocked": line_row,
        "validation": result.get("validation"),
        "roots": result.get("roots"),
        "lines": result.get("lines"),
    }


def _rule_sizes(content: Path) -> list[dict[str, Any]]:
    caps = sizes.covered_caps()
    rows = []
    for path in sorted(content.glob("rule.*.json")):
        if path.name in {"rule.schedule-d-line1b.v4.json", "rule.cwg-p0-validation-probe.v1.json"} or path.name.startswith("rule.cwg-"):
            rows.append({
                "name": path.name,
                "bytes": path.stat().st_size,
                "cap": caps.get(path.name),
                "covered": path.name in caps,
            })
    return rows


def _schema_probe() -> dict[str, Any]:
    family = json.loads((REPO / "packages/content/tax/2025/family.f1099b-covered-w-st.v2.json").read_text())
    family["member_constraints"][1]["missing"] = [ADJ]
    try:
        DerivationSchemas().validate_declared(family)
    except SchemaValidationError as exc:
        return {"accepted": False, "error": type(exc).__name__, "message": _scrub(str(exc))[:500]}
    return {"accepted": True}


def _prepare(scratch: Path) -> None:
    source = REPO / "packages/content/tax/2025"
    releases = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
    base = scratch / "base"
    shutil.copytree(source, base / "content")
    shutil.copytree(releases, base / "releases")


def _route_specs() -> list[dict[str, Any]]:
    question = _question()
    return [
        {"name": "input-question", "files": {"input-question.f1099b-covered-w-st-adjustment.json": (question, "input-question")}},
        {"name": "blocked-missing", "line": "blocked-missing", "files": {"input-question.f1099b-covered-w-st-adjustment.json": (question, "input-question")}},
        {"name": "expression-block", "line": "expression-block", "files": {"input-question.f1099b-covered-w-st-adjustment.json": (question, "input-question")}},
        {"name": "conditional-block", "line": "conditional-block", "files": {"input-question.f1099b-covered-w-st-adjustment.json": (question, "input-question")}},
        {"name": "closure-code", "closure": True},
        {"name": "ambiguous-producer", "probe": True},
        {"name": "closure-family-on-line", "line": "closure-family-on-line"},
    ]


def _build_one(scratch: Path, spec: dict[str, Any], published_hashes: dict[str, str]) -> dict[str, Any]:
    route = scratch / spec["name"]
    shutil.copytree(scratch / "base", route)
    content, releases = route / "content", route / "releases"
    written: dict[str, tuple[dict[str, Any], str]] = {}
    replace_line = None
    if spec.get("line"):
        replace_line = _line(spec["line"])
        written["rule.schedule-d-line1b.v4.json"] = (replace_line, "computation")
    if spec.get("closure"):
        written["closure-mapping.cwg-code-w-on-gain.v1.json"] = (_closure(content), "source-closure-mapping")
    if spec.get("probe"):
        written["rule.cwg-p0-validation-probe.v1.json"] = (_probe_rule(), "computation")
    written.update(spec.get("files") or {})
    for name, (body, _role) in written.items():
        (content / name).write_text(_dump(body))
    (route / "changes.json").write_text(_dump(_changes(written, replace_line)))
    hashes = _family_hashes(content)
    row: dict[str, Any] = {
        "name": spec["name"],
        "family_bytes_unchanged": hashes == published_hashes,
        "rule_sizes": _rule_sizes(content),
    }
    try:
        row["generation"] = _install(route, content, releases)
        row["status"] = "valid"
    except (SuccessorError, SchemaValidationError, OSError, ValueError) as exc:
        row["status"] = "rejected"
        row["failure"] = _scrub(str(exc))[:1500]
        return row
    core = trace.h.Core(TO["core"], TO["registry"], TO["release"], content=content, releases=releases, loader_from=FROM["core"])
    runs = {}
    for key in CASES:
        try:
            runs[key] = _brief(trace.observe(key, core))
        except Exception as exc:  # noqa: BLE001 - a rejected return is a result
            runs[key] = {"error": type(exc).__name__, "message": _scrub(str(exc))[:800]}
    row["runs"] = runs
    gain = runs.get("covered/st/gain") or {}
    loss = runs.get("covered/st/loss") or {}
    gain_questions = [
        question
        for page in gain.get("line_page") or []
        for question in page.get("questions") or []
    ]
    loss_line = next((item for item in loss.get("lines") or [] if item.get("field") == "schedule-d.line-1b"), None)
    row["gain_question_count"] = len(gain_questions)
    row["gain_questions"] = gain_questions
    row["loss_line_1b"] = loss_line
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    scratch = args.scratch
    if scratch.exists():
        raise SystemExit("scratch directory already exists")
    parent = scratch.parent.absolute()
    if parent.resolve(strict=True) != parent:
        raise SystemExit("scratch parent contains a symlink")
    scratch.mkdir(parents=True)
    published = REPO / "packages/content/tax/2025"
    published_hashes = _family_hashes(published)
    _prepare(scratch)
    baseline = {}
    for key in LOSS_BASELINE:
        try:
            baseline[key] = _brief(trace.observe(key))
        except Exception as exc:  # noqa: BLE001
            baseline[key] = {"error": type(exc).__name__, "message": _scrub(str(exc))[:800]}
    rows = [_build_one(scratch, spec, published_hashes) for spec in _route_specs()]
    body = {
        "from": FROM,
        "to": TO,
        "schema_probe_constraint_missing": _schema_probe(),
        "published_family_sha256": published_hashes,
        "baseline_loss": baseline,
        "routes": rows,
    }
    text = json.dumps(body, indent=2) + "\n"
    assert not re.search(r"/(?:Users|private|tmp|var)/", text), "local path in results"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text)
    summary = []
    for row in rows:
        summary.append({
            "name": row["name"],
            "status": row["status"],
            "family_bytes_unchanged": row["family_bytes_unchanged"],
            "gain_question_count": row.get("gain_question_count"),
            "loss_line_1b": row.get("loss_line_1b"),
            "failure": (row.get("failure") or "")[:240],
        })
    print(json.dumps({"baseline_loss": baseline, "routes": summary}, indent=2))


if __name__ == "__main__":
    main()
