"""Build and exercise a scratch successor whose block expressions name questions.

The scratch carrier keeps the rules on their current schema id while validating
an unmodified copy of each rule. Production needs a rule-artifact successor;
the carrier exists only to exercise the proposed additive ``block.missing``
runtime behavior through ``live_coordinate_run`` without editing packages/.
"""

from __future__ import annotations

import contextlib
import copy
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterator

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import common  # noqa: E402
import probe  # noqa: E402
from packages.derivation import evaluator, runner  # noqa: E402
from packages.derivation.evaluator import EvalBlocked  # noqa: E402
from packages.derivation.loader import DerivationSchemas  # noqa: E402
from packages.derivation.package_validation import citizen_checksum  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = common.P
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v87", "registry": "v85", "release": "v85"}
TO = {"package": "v88", "registry": "v86", "release": "v86"}

NO_8949 = P + "schedule-d-boundary.no-form8949-sources"
PATH_B = P + "schedule-d-boundary.no-other-form8949-adjustments"
Q1 = P + "f1099b.noncovered-sold.source-closure"
Q2 = P + "f8949.no1099b-sold.source-closure"
Q3 = P + "f1099b.code-b-sold.source-closure"
IC80 = P + "schedule-d-boundary.form8949-in-class"
IC81 = P + "schedule-d-boundary.form8949-code-b-in-class"


def load(name: str) -> dict[str, Any]:
    return json.loads((CONTENT / name).read_text(encoding="utf-8"))


def question(slug: str, fact: str, words: str) -> tuple[str, dict[str, Any]]:
    body = {
        "schema": "input-question.v1",
        "id": P + "input-question." + slug,
        "version": "v1",
        "fact_type": {"id": fact, "version": "v1"},
        "question": words,
    }
    return "input-question." + slug + ".v1.json", body


def successor(name: str, version: str) -> tuple[str, dict[str, Any]]:
    body = load(name)
    body["version"] = version
    stem = name.rsplit(".v", 1)[0] if re.search(r"\.v\d+\.json$", name) else name[:-5]
    return f"{stem}.{version}.json", body


def artifacts() -> list[tuple[str, dict[str, Any]]]:
    rows = [
        question("schedule-d-boundary-no-form8949-sources", NO_8949,
                 "Is it true that you had no transaction or adjustment to report on Form 8949?"),
        question("schedule-d-boundary-no-other-form8949-adjustments", PATH_B,
                 "Is it true that every Form 8949 adjustment code is W, no row has more than one code, and no Form 8949 sale has basis that was not reported to the IRS?"),
    ]
    rows += [successor("rule.schedule-d-line3.v2.json", "v3"),
             successor("rule.schedule-d-line10.v2.json", "v3"),
             successor("rule.form1040-line16.v7.json", "v8")]
    for term in ("st", "lt"):
        rows += [successor(f"rule.f1099b-code-b-{term}-gain.json", "v2"),
                 successor(f"rule.f8949.no1099b-{term}-txn.amounts-check.json", "v2"),
                 successor(f"rule.f1099b.code-b-{term}-txn.amounts-check.json", "v2"),
                 successor(f"rule.f1099b.covered-w-{term}-txn.admission-check.v2.json", "v3")]
    return rows


def role_for(schema: str) -> str:
    return "input-question" if schema == "input-question.v1" else "computation"


def changes(rows: list[tuple[str, dict[str, Any]]]) -> dict[str, Any]:
    package = load(f"package.core-calculations.{FROM['package']}.json")
    current = {m["id"]: m for m in package["members"]}
    entries = {(e["id"], e["version"]) for e in package["entrypoints"]}
    members = []
    entrypoints = []
    for _name, body in rows:
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"],
               "role": role_for(body["schema"])}
        old = current.get(body["id"])
        if old is None:
            members.append({"op": "add", "new": new})
            entrypoints.append({"op": "add", "value": {"id": new["id"], "version": new["version"]}})
        else:
            members.append({"op": "replace", "old": dict(old), "new": new})
            if (old["id"], old["version"]) in entries:
                entrypoints.append({"op": "replace", "old": {"id": old["id"], "version": old["version"]},
                                    "new": {"id": new["id"], "version": new["version"]}})
    return {"package_version": TO["package"], "release_version": TO["release"],
            "members": members, "entrypoints": entrypoints,
            "registry_sort": "id_version", "registry_new_key_order": ["checksum", "id", "version"]}


def node(body: dict[str, Any], path: str) -> dict[str, Any]:
    current: Any = body
    for part in path.split("/"):
        current = current[int(part)] if isinstance(current, list) else current[part]
    if not isinstance(current, dict) or current.get("op") != "block":
        raise SystemExit(f"prototype path is not a block: {path}")
    return current


def _cat(name: str, cmp: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare",
        "cmp": cmp,
        "left": {"op": "ref", "name": name},
        "right": {
            "op": "category_literal",
            "fact_type": {"id": name, "version": "v1"},
            "value": value,
        },
    }


def _named_block(names: list[str]) -> dict[str, Any]:
    return {"op": "block", "code": "DEPENDENCY_ABSENT", "missing": names}


def _choose(when: dict[str, Any], then: dict[str, Any], otherwise: dict[str, Any]) -> dict[str, Any]:
    return {"op": "choose", "when": when, "then": then, "else": otherwise}


def applicable_boundary_block() -> dict[str, Any]:
    """Name only the boundary question that applies to the recorded sales."""
    return _choose(
        _cat(NO_8949, "eq", "yes"),
        _named_block([NO_8949]),
        _choose(
            {"op": "all", "args": [_cat(Q2, "eq", "yes"), _cat(IC80, "ne", "yes")]},
            _named_block([IC80]),
            _choose(
                {"op": "all", "args": [_cat(Q3, "eq", "yes"), _cat(IC81, "ne", "yes")]},
                _named_block([IC81]),
                _named_block([NO_8949, IC80, IC81]),
            ),
        ),
    )


def inject(body: dict[str, Any]) -> None:
    rid = body["id"]
    if rid in (P + "rule.schedule-d-line3", P + "rule.schedule-d-line10"):
        body["value"]["then"]["else"] = applicable_boundary_block()
        node(body, "value/else/else")["missing"] = [Q1, Q2, NO_8949, PATH_B]
    elif rid == P + "rule.form1040-line16":
        body["when"] = {
            "op": "choose",
            "when": body["when"],
            "then": True,
            "else": {"op": "block", "code": "DEPENDENCY_ABSENT",
                     "missing": [Q1, Q2, NO_8949, PATH_B]},
        }
    elif "rule.f1099b-code-b-" in rid and rid.endswith("-gain"):
        node(body, "value/then/then/else")["missing"] = [NO_8949, IC81]
        node(body, "value/then/else/else")["missing"] = [Q3]
        term = "st" if "-st-" in rid else "lt"
        node(body, "value/else")["missing"] = [P + f"f1099b.code-b-{term}-txn.adjustment"]
    elif "rule.f8949.no1099b-" in rid and rid.endswith("-txn.amounts-check"):
        term = "st" if "-st-" in rid else "lt"
        node(body, "selection/paths/0/value/else")["missing"] = [P + f"f8949.no1099b-{term}-txn.basis"]
    elif "rule.f1099b.code-b-" in rid and rid.endswith("-txn.amounts-check"):
        term = "st" if "-st-" in rid else "lt"
        node(body, "selection/paths/0/value/else")["missing"] = [P + f"f1099b.code-b-{term}-txn.adjustment"]
    elif "rule.f1099b.covered-w-" in rid and rid.endswith("-txn.admission-check"):
        term = "st" if "-st-" in rid else "lt"
        path = body["selection"]["paths"][0]
        closure = P + f"f1099b.covered-w-{term}-adjustment.closure-check"
        family = P + f"f1099b.covered-w-{term}-adjustment"
        path["requires"] = [closure]
        path["pins"] = [{"role": "input", "id": closure, "version": "v1", "origin": "assertion"}]
        path["value"] = {
            "op": "choose",
            "when": {"op": "ref", "name": closure},
            "then": path["value"],
            "else": {"op": "block", "code": "SOURCE_SET_UNCLOSED", "missing": [family]},
        }


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(scratch: Path) -> dict[str, Any]:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    rows = artifacts()
    for name, body in rows:
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    changes_path = scratch / "changes.json"
    changes_path.write_text(json.dumps(changes(rows), indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['package']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{RELEASE_STEM}.{FROM['release']}.json", content, changes_path, scratch / "out")
    for src, folder, target in (("package.json", content, f"package.core-calculations.{TO['package']}.json"),
                                ("registry.json", content, f"published-packages.{TO['registry']}.json"),
                                ("release.json", releases, f"{RELEASE_STEM}.{TO['release']}.json")):
        shutil.copy(scratch / "out" / src, folder / target)
    changed = []
    for name, body in rows:
        if body["schema"] == "input-question.v1":
            continue
        path = content / name
        body = json.loads(path.read_text(encoding="utf-8"))
        inject(body)
        path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
        changed.append((body["id"], body["version"], path))
    registry_path = content / f"published-packages.{TO['registry']}.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    lookup = {(r["id"], r["version"]): r for r in registry["citizens"]}
    for cid, version, path in changed:
        lookup[(cid, version)]["checksum"] = citizen_checksum(json.loads(path.read_text(encoding="utf-8")))
    registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    release_path = releases / f"{RELEASE_STEM}.{TO['release']}.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["package_registry_sha256"] = sha(registry_path)
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    core = {"version": TO["package"], "registry": TO["registry"], "release_version": TO["release"],
            "content": str(content), "releases": str(releases), "loader_from": FROM["package"]}
    (scratch / "core.json").write_text(json.dumps(core, indent=2) + "\n", encoding="utf-8")
    return {"from": FROM, "to": TO, "package": report["package"]["version"],
            "added_questions": 2, "rule_successors": len(changed),
            "prototype_carrier": "copied current rule schema with additive block.missing validation shim",
            "production_contract": "new rule-artifact successor whose block expression permits missing names"}


class PrototypeSchemas(DerivationSchemas):
    def validate_declared(self, instance: dict[str, Any]) -> str:
        clean = copy.deepcopy(instance)
        def strip(value: Any) -> None:
            if isinstance(value, dict):
                if value.get("op") == "block":
                    value.pop("missing", None)
                for child in value.values():
                    strip(child)
            elif isinstance(value, list):
                for child in value:
                    strip(child)
        strip(clean)
        return super().validate_declared(clean)


@contextlib.contextmanager
def block_missing_runtime() -> Iterator[None]:
    original_eval = evaluator.evaluate
    original_runner = runner.evaluate
    def patched(expr: Any, env: Any, access: Any) -> Any:
        if isinstance(expr, dict) and expr.get("op") == "block" and "missing" in expr:
            raise EvalBlocked(expr["code"], list(expr["missing"]))
        return original_eval(expr, env, access)
    evaluator.evaluate = patched  # type: ignore[assignment]
    runner.evaluate = patched  # type: ignore[assignment]
    try:
        yield
    finally:
        evaluator.evaluate = original_eval  # type: ignore[assignment]
        runner.evaluate = original_runner  # type: ignore[assignment]


def exercise(core_path: Path) -> dict[str, Any]:
    core = common.scratch(core_path)
    schemas = PrototypeSchemas()
    cases = {}
    with block_missing_runtime():
        for case_id, (_group, build_case, _note) in probe.CASES.items():
            result = common.run(core, build_case(), "demo.bnq.prototype." + case_id, schemas=schemas)
            result.pop("_publications", None)
            cases[case_id] = {"outcome": result["outcome"], "questions": result.get("questions", []),
                              "silent_blocked": result.get("silent_blocked", []), "lines": result.get("lines", {}),
                              "error": result.get("error")}
    return cases


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: prototype.py <scratch-directory-outside-the-repo>")
    scratch = Path(sys.argv[1]).resolve()
    if scratch == REPO or REPO in scratch.parents:
        raise SystemExit("scratch directory must be outside the repository")
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    summary = build(scratch)
    cases = exercise(scratch / "core.json")
    summary["case_count"] = len(cases)
    summary["cases_with_questions"] = sorted(k for k, v in cases.items() if v["questions"])
    summary["errors"] = {k: v["error"] for k, v in cases.items() if v["outcome"] != "success"}
    common.write("prototype-build.json", summary)
    common.write("prototype-output.json", {"core": TO, "cases": cases})
    print(json.dumps({"core": TO["package"], "cases": len(cases),
                      "with_questions": len(summary["cases_with_questions"]), "errors": len(summary["errors"])}, indent=2))


if __name__ == "__main__":
    main()
