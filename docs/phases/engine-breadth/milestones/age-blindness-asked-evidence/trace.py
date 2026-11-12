"""Trace the four age and blindness facts on core v86, scratch v87 and scratch v88.

Evidence for docs/phases/engine-breadth/milestones/age-blindness-asked.md.
Charter: docs/reviews/age-blindness-asked/charter-p0.md.

For each core, from its package and the citizens it pins:

- the input binding of each fact and its mode;
- the fact type the adopted vocabulary bundle declares (title, default);
- the default parameter's value;
- every member rule that names a fact or its binding symbol, and how;
- every rule that consumes those rules' publications, transitively, up to
  the lines a filer sees, and every form field that shows any of them;
- every input question naming a fact;
- every Python module under packages/ and tools/, and every committed act
  list under packages/sample_data/, that records a value for a fact.

    python3 trace.py <scratch>/core-v88.json
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.package_successor import load_corpus  # noqa: E402

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
FACTS = {
    P + "taxpayer-over-65": "taxpayer_over_65",
    P + "taxpayer-blind": "taxpayer_blind",
    P + "spouse-over-65": "spouse_over_65",
    P + "spouse-blind": "spouse_blind",
}


def _names(expr: Any, out: set[str]) -> None:
    if isinstance(expr, dict):
        for key in ("name",):
            if isinstance(expr.get(key), str):
                out.add(expr[key])
        for value in expr.values():
            _names(value, out)
    elif isinstance(expr, list):
        for item in expr:
            _names(item, out)


def _cds_members(expr: Any, out: set[str]) -> None:
    if isinstance(expr, dict):
        if expr.get("op") == "conditional_dependency_set":
            _names(expr.get("members"), out)
        for value in expr.values():
            _cds_members(value, out)
    elif isinstance(expr, list):
        for item in expr:
            _cds_members(item, out)


def trace(content: Path, version: str) -> dict[str, Any]:
    corpus, _ = load_corpus(content)
    package = json.loads((content / f"package.core-calculations.{version}.json").read_text(encoding="utf-8"))
    bodies = [(m, corpus[(m["id"], m["version"])]) for m in package["members"]]
    bindings = {b["symbol"]: b for b in package["input_bindings"]}
    out: dict[str, Any] = {"package": version, "facts": {}}
    vocab = next(b for m, b in bodies if m["id"] == P + "core_calculations.vocabulary")
    params = {(b["id"], b["version"]): b for m, b in bodies if m["schema"] == "parameter-declaration.v1"}
    for fact, symbol in FACTS.items():
        declared = next(f for f in vocab["fact_types"] if f["id"] == fact)
        default = declared.get("optional_default", {}).get("parameter")
        param = params.get((default["id"], default["version"])) if default else None
        out["facts"][fact.removeprefix(P)] = {
            "binding": {"symbol": symbol, "mode": bindings[symbol]["mode"],
                        "fact_type_version": bindings[symbol]["fact_type"]["version"]},
            "declared_in": f"{vocab['id'].removeprefix(P)} {vocab['version']}",
            "fact_type_version": declared["version"],
            "value_schema": declared["value_schema"],
            "title": declared["title"],
            "declared_default": (f"{default['id'].removeprefix(P)} {default['version']}" if default else None),
            "default_value": param.get("values") if param else None,
            "default_applies": bindings[symbol]["mode"] == "optional_default",
            "input_questions": [
                {"id": b["id"].removeprefix(P), "version": b["version"], "question": b["question"]}
                for m, b in bodies if m["schema"] == "input-question.v1" and b["fact_type"]["id"] == fact
            ],
        }
    rules = [(m, b) for m, b in bodies if str(m["schema"]).startswith("rule-artifact.")]
    readers = []
    watched = set(FACTS) | set(FACTS.values())
    for m, b in rules:
        names: set[str] = set()
        _names([b.get("when"), b.get("value"), b.get("selection")], names)
        cds: set[str] = set()
        _cds_members([b.get("when"), b.get("value")], cds)
        pins = {p["id"] for p in b.get("pins") or []}
        hit = sorted((names | set(b.get("requires") or []) | pins) & watched)
        if hit:
            readers.append({
                "id": b["id"].removeprefix(P), "version": b["version"], "publishes": b["publishes"].removeprefix(P),
                "names": hit,
                "requires": sorted(set(b.get("requires") or []) & watched),
                "conditional_dependency_set_members": sorted(cds & watched),
                "read_in_expression": sorted(names & watched),
            })
    out["readers"] = readers
    produced = {r["publishes"] for r in readers}
    consumers: list[dict[str, Any]] = []
    frontier = {P + p for p in produced}
    seen = set(frontier)
    while frontier:
        nxt: set[str] = set()
        for m, b in rules:
            names: set[str] = set()
            _names([b.get("when"), b.get("value"), b.get("selection")], names)
            names |= set(b.get("requires") or [])
            if names & frontier and b["publishes"] not in seen:
                consumers.append({"id": b["id"].removeprefix(P), "version": b["version"],
                                  "publishes": b["publishes"].removeprefix(P)})
                nxt.add(b["publishes"])
                seen.add(b["publishes"])
        frontier = nxt
    out["downstream_rule_count"] = len(consumers)
    out["downstream_sample"] = sorted(c["publishes"] for c in consumers)[:60]
    fields = []
    for m, b in bodies:
        if str(m["schema"]).startswith("form-field.") and b.get("binds_symbol") in seen | watched:
            fields.append({"id": b["id"].removeprefix(P), "binds": str(b["binds_symbol"]).removeprefix(P),
                           "direct": b.get("binds_symbol") in watched or b.get("binds_symbol") in {P + p for p in produced}})
    out["form_fields"] = sorted(fields, key=lambda row: row["id"])
    out["form_fields_showing_a_fact_or_reader"] = [f for f in out["form_fields"] if f["direct"]]
    return out


def recording_surfaces() -> dict[str, Any]:
    pattern = "|".join(re.escape(f) for f in FACTS) + "|" + "|".join(FACTS.values())
    code = subprocess.run(["git", "grep", "-l", "-E", pattern, "--", "packages/*.py", "packages/**/*.py",
                           "tools/*.py"], cwd=REPO, text=True, capture_output=True).stdout.split()
    tests = subprocess.run(["git", "grep", "-l", "-E", pattern, "--", "tests"], cwd=REPO, text=True,
                           capture_output=True).stdout.split()
    data = subprocess.run(["git", "grep", "-l", "-E", pattern, "--", "packages/sample_data"], cwd=REPO,
                          text=True, capture_output=True).stdout.split()
    asserting = []
    symbol_inputs = []
    for path in data:
        text = (REPO / path).read_text(encoding="utf-8", errors="replace")
        if re.search(r'"fact_id":\s*"(' + "|".join(re.escape(f) for f in FACTS) + r')\|', text):
            asserting.append(path)
        if re.search(r'"symbol":\s*"(' + "|".join(FACTS.values()) + r')"', text):
            symbol_inputs.append(path)
    return {
        "python_modules_naming_a_fact": code,
        "test_modules_naming_a_fact": tests,
        "sample_data_files_naming_a_fact": len(data),
        "sample_data_files_recording_a_value": asserting,
        "sample_data_files_supplying_a_symbol_input": symbol_inputs,
    }


def history() -> dict[str, list[str]]:
    found = {}
    for name in ("core_calculations.bundle.json", "core_calculations.bundle.v2.json",
                 "rule.dependents-worksheet-line-1.json", "rule.schedule1a-part-v-line-36a.json",
                 "rule.schedule1a-part-v-line-36b.json", "rule.form1040-standard-deduction.v3.json"):
        out = subprocess.run(["git", "log", "--format=%h %s", "--", f"packages/content/tax/2025/{name}"],
                             cwd=REPO, text=True, capture_output=True).stdout.splitlines()
        found[name] = out[-1:] + (out[:1] if len(out) > 1 else [])
    return found


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    scratch = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    content = Path(scratch["content"])
    payload = {
        "cores": {
            "v86": trace(CONTENT, "v86"),
            "v87": trace(content, "v87"),
            "v88": trace(content, "v88"),
        },
        "recording": recording_surfaces(),
        "introduced_by": history(),
    }
    text = json.dumps(payload, indent=2) + "\n"
    for needle in ("/Users/", "/private/", "/tmp/", "/var/"):
        if needle in text:
            raise SystemExit(f"trace output contains {needle}")
    (HERE / "trace.json").write_text(text, encoding="utf-8")
    for name, body in payload["cores"].items():
        print(name, {k: (v["binding"]["mode"], len(v["input_questions"])) for k, v in body["facts"].items()},
              [(r["id"], r["version"]) for r in body["readers"]], body["downstream_rule_count"],
              len(body["form_fields"]), body["form_fields_showing_a_fact_or_reader"])
    print(json.dumps(payload["recording"], indent=1))


if __name__ == "__main__":
    main()
