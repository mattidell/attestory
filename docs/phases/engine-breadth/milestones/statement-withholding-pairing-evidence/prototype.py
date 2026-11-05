"""P0 prototype: pair each statement with shared_key_count, in a scratch copy.

Nothing is written under packages/. The script copies the committed content
and release directories to a temporary directory, adds a scratch vocabulary,
ten subject rules, and a line 25b v5 selection there, and builds package v77 /
registry / release v75 with tools/package_successor.py. An in-process wrapper
gives v77 the companion declaration v76 already has. It does not edit the loader.

    python3 docs/phases/engine-breadth/milestones/statement-withholding-pairing-evidence/prototype.py [case id ...]

Writes prototype-output.json and the rule files under prototype-rules/.
Run probe.py first. Synthetic demo.* data only.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import probe  # noqa: E402
from packages.tax import loader  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
# (slug, subject fact, withholding fact, family used only as the count op's unused source_set)
GUARDS = (
    ("f1099int-box1", "f1099int.box1-interest", "f1099int.box4-withholding", "f1099int.b1"),
    ("f1099int-box3", "f1099int.box3-interest", "f1099int.box4-withholding", "f1099int.b3"),
    ("f1099int-box8", "f1099int.box8-tax-exempt-interest", "f1099int.box4-withholding", "f1099int.b8"),
    ("f1099int-box10", "f1099int.box10-market-discount", "f1099int.box4-withholding", "f1099int.b10"),
    ("f1099div-box1a", "f1099div.box1a-ordinary", "f1099div.box4-withholding", "f1099div.1a"),
    ("f1099div-box2a", "f1099div.box2a-capital-gain-distribution", "f1099div.box4-withholding", "f1099div.2a"),
    ("f1099div-box12", "f1099div.box12-exempt-interest-dividends", "f1099div.box4-withholding", "f1099div.12"),
    ("f1099r-box1", "f1099r.ira-box1-taxable-distribution", "f1099r.ira-box4-withholding", "f1099r.ira-fully-taxable"),
    ("f1099g-box1", "f1099g.box1-unemployment", "f1099g.box4-withholding", "f1099g.1"),
    ("ssa1099-box5", "ssa1099.box5-net-benefits", "ssa1099.box6-voluntary-withholding", "ssa1099.benefits"),
)
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
ANSWER = P + "withholding.pairing.answer"
ANSWERED = {
    "op": "category_literal",
    "fact_type": {"id": ANSWER, "version": "v1"},
    "value": "answered",
}


def _vocabulary() -> dict[str, Any]:
    """Scratch fact type for the one favorable category. Never recorded as a finding."""
    return {
        "schema": "bundle.v2",
        "id": P + "withholding.pairing.vocabulary",
        "version": "v1",
        "label": "Scratch vocabulary for a statement withholding answer",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": ANSWER,
                "version": "v1",
                "title": "A statement has its own withholding answer",
                "nature": "determinable",
                "identity_keys": [{"name": "marker", "kind": "literal", "values": ["unused"]}],
                "value_schema": {"type": "string", "enum": ["answered"]},
                "supersession": {"policy": "free"},
            }
        ],
    }


def _guard(slug: str, subject: str, withholding: str) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v14",
        "id": P + "rule.withholding-pairing." + slug,
        "version": "v1",
        "scope": SCOPE,
        "role": "computation",
        "subject": {"id": P + subject, "version": "v1"},
        "requires": [],
        "pins": [],
        "when": True,
        "value": {
            "op": "choose",
            "when": {
                "op": "compare",
                "cmp": "gte",
                "left": {"op": "shared_key_count", "fact_type": P + withholding, "key": "statement"},
                "right": 1,
            },
            "then": ANSWERED,
            "else": {"op": "block", "code": "DEPENDENCY_ABSENT"},
        },
        "publishes": P + "withholding.pairing." + slug,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "notes": (
            "PROTOTYPE, not a citizen. One current withholding row on this statement's "
            "statement key is an answer, including 0. Absence blocks this subject. "
            "The published category is the favorable value presentation reads."
        ),
    }


def _dependency_pins(names: list[str]) -> list[dict[str, str]]:
    return [{"id": name, "role": "input", "version": "v1", "origin": "assertion"} for name in names]


def _sum_requires(total: dict[str, Any]) -> list[str]:
    """Ref names in the v4 sum, in the order a selection dependency walk yields them."""
    found: list[str] = []

    def walk(expr: Any) -> None:
        if isinstance(expr, dict):
            if expr.get("op") == "ref" and isinstance(expr.get("name"), str) and expr["name"] not in found:
                found.append(expr["name"])
            for value in expr.values():
                walk(value)
        elif isinstance(expr, list):
            for item in expr:
                walk(item)

    walk(total)
    return found


def _line(total: dict[str, Any], citations: list[dict[str, Any]]) -> dict[str, Any]:
    reads = [
        {
            "symbol": P + "withholding.pairing." + slug,
            "subject": {"id": P + subject, "version": "v1"},
        }
        for slug, subject, _withholding, _family in GUARDS
    ]
    checks = {
        "op": "all",
        "args": [
            {
                "op": "choose",
                "when": {
                    "op": "compare",
                    "cmp": "gt",
                    "left": {
                        "op": "count",
                        "name": P + "withholding.pairing." + slug,
                        "source_set": P + family,
                    },
                    "right": 0,
                },
                "then": {
                    "op": "collect_categorical_all_equal",
                    "name": P + "withholding.pairing." + slug,
                    "value": ANSWERED,
                },
                "else": True,
            }
            for slug, _subject, _withholding, family in GUARDS
        ],
    }
    requires = _sum_requires(total)
    pins = _dependency_pins(requires)
    statement_value = {"op": "choose", "when": checks, "then": total, "else": {"op": "block", "code": "DEPENDENCY_ABSENT"}}
    summing = {"requires": requires, "pins": pins, "when": True}
    return {
        "schema": "rule-artifact.v14",
        "id": P + "rule.form1040-line25b",
        "version": "v5",
        "scope": SCOPE,
        "role": "computation",
        "requires": [],
        "pins": [],
        "when": True,
        "selection": {
            "mode": "exclusive_presence",
            "conflict": "refuse",
            "paths": [
                {
                    "id": "statements",
                    "activity": {
                        "kind": "source_nonempty",
                        "member_fact_types": [
                            {"id": P + subject, "version": "v1"}
                            for _slug, subject, _withholding, _family in GUARDS
                        ],
                    },
                    "reads_subject_results": reads,
                    **summing,
                    "value": statement_value,
                },
                {
                    "id": "domain",
                    "activity": {
                        "kind": "source_nonempty",
                        "member_fact_types": [{"id": ANSWER, "version": "v1"}],
                    },
                    "reads_subject_results": [],
                    "requires": [],
                    "pins": [],
                    "when": True,
                    "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
                },
                {
                    "id": "inert",
                    "activity": {
                        "kind": "source_nonempty",
                        "member_fact_types": [
                            {"id": P + "f1099k.inert-path-unwritten", "version": "v1"}
                        ],
                    },
                    "reads_subject_results": [],
                    "requires": [],
                    "pins": [],
                    "when": True,
                    "value": {"op": "block", "code": "DEPENDENCY_ABSENT"},
                },
            ],
            "default": {
                "id": "neither",
                "reads_subject_results": [],
                **summing,
                "value": total,
            },
            "refusal": {
                "code": "DEPENDENCY_INVALID",
                "missing": ["withholding-pairing-inert-path-conflict"],
                "pins": [],
            },
        },
        "publishes": P + "payments.line25b",
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": citations,
        "notes": (
            "PROTOTYPE, not a citizen. The value is still the five withholding subtotals. "
            "A statement path reads each subject rule first. An empty guard is true. A "
            "blocked subject fails closed before the sum, and the favorable category is "
            "what presentation expects. The domain path names the scratch fact type so "
            "the package graph reaches it. Nothing writes that fact, so the path stays "
            "inactive. The sum itself is unchanged, so an answered return, including a "
            "withholding-only extra and a 0 answer, matches v4."
        ),
    }


def _write_rules(content: Path, rules_dir: Path) -> None:
    v4 = json.loads((content / "rule.form1040-line25b.v4.json").read_text(encoding="utf-8"))
    rules_dir.mkdir(parents=True, exist_ok=True)
    written: list[dict[str, str]] = []
    vocabulary = _vocabulary()
    text = json.dumps(vocabulary, indent=2) + "\n"
    (content / "withholding.pairing.vocabulary.v1.json").write_text(text, encoding="utf-8")
    (rules_dir / "withholding.pairing.vocabulary.v1.json").write_text(text, encoding="utf-8")
    written.append({
        "id": vocabulary["id"], "version": "v1", "schema": vocabulary["schema"], "role": "fact-type-bundle",
    })
    for slug, subject, withholding, _family in GUARDS:
        rule = _guard(slug, subject, withholding)
        name = f"rule.withholding-pairing.{slug}.v1.json"
        text = json.dumps(rule, indent=2) + "\n"
        (content / name).write_text(text, encoding="utf-8")
        (rules_dir / name).write_text(text, encoding="utf-8")
        written.append({"id": rule["id"], "version": "v1", "schema": rule["schema"], "role": "computation"})
    line = _line(v4["value"], v4["citations"])
    text = json.dumps(line, indent=2) + "\n"
    (content / "rule.form1040-line25b.v5.json").write_text(text, encoding="utf-8")
    (rules_dir / "rule.form1040-line25b.v5.json").write_text(text, encoding="utf-8")
    (rules_dir / "_members.json").write_text(json.dumps(written, indent=2) + "\n", encoding="utf-8")


def _declare_v77() -> None:
    original = loader.domain_package_companion_declarations

    def with_v77() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(original())
        declarations[(P + "package.core-calculations", "v77")] = declarations[(P + "package.core-calculations", "v76")]
        return declarations

    loader.domain_package_companion_declarations = with_v77  # type: ignore[method-assign]


def build(scratch: Path) -> None:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(probe.CONTENT, content)
    shutil.copytree(probe.RELEASE_DIR, releases)
    _write_rules(content, HERE / "prototype-rules")
    members: list[dict[str, Any]] = [
        {
            "op": "add",
            "new": {
                "id": P + "withholding.pairing.vocabulary",
                "version": "v1",
                "schema": "bundle.v2",
                "role": "fact-type-bundle",
            },
        },
        *[
            {
                "op": "add",
                "new": {"id": P + "rule.withholding-pairing." + slug, "version": "v1", "schema": "rule-artifact.v14", "role": "computation"},
            }
            for slug, _subject, _withholding, _family in GUARDS
        ],
    ]
    members.append({
        "op": "replace",
        "old": {"id": P + "rule.form1040-line25b", "role": "computation", "schema": "rule-artifact.v4", "version": "v4"},
        "new": {"id": P + "rule.form1040-line25b", "role": "computation", "schema": "rule-artifact.v14", "version": "v5"},
    })
    changes = {
        "package_version": "v77",
        "release_version": "v75",
        "members": members,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v76.json",
        content / "published-packages.v74.json",
        releases / "demo.release.sli-worksheet-integration.2025.v74.json",
        content,
        scratch / "changes.json",
        scratch / "out",
    )
    print("successor", report["package"]["version"], "inherited:", report["inherited_inconsistencies"], flush=True)
    for name, (folder, target) in {
        "package.json": ("content", "package.core-calculations.v77.json"),
        "registry.json": ("content", "published-packages.v75.json"),
        "release.json": ("releases", "demo.release.sli-worksheet-integration.2025.v75.json"),
    }.items():
        shutil.copy(scratch / "out" / name, scratch / folder / target)
    probe.CONTENT = content
    probe.RELEASE_DIR = releases
    probe.CORE = (
        "package.core-calculations.v77.json",
        "v77",
        "demo.release.sli-worksheet-integration.2025.v75.json",
        "v75",
        "published-packages.v75.json",
    )
    _declare_v77()


def _expect(case_id: str, right: str) -> str:
    if case_id.startswith("w2.") or "same-statement" in case_id:
        return "match-v76"
    if right == "block":
        return "block"
    return "match-v76"


def _met(expect: str, v76: dict[str, Any], new: dict[str, Any]) -> bool:
    if expect == "match-v76":
        return v76.get("reachable") == new.get("reachable") and v76.get("lines") == new.get("lines") and v76.get("refusal") == new.get("refusal")
    published = (new.get("lines") or {}).get("line25b")
    return bool(new.get("reachable")) and published is None and bool(new.get("line_blocks"))


def _survey() -> dict[str, Any]:
    needles = [P + subject for _slug, subject, _withholding, _family in GUARDS]
    hits: list[dict[str, Any]] = []
    for root in (REPO / "packages/sample_data", REPO / "tests"):
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            found = [needle for needle in needles if needle in text]
            if not found:
                continue
            hits.append({"path": str(path.relative_to(REPO)), "facts": found})
    return {"files": len(hits), "hits": hits}


def main() -> None:
    selected = sys.argv[1:]
    v76_path = HERE / "probe-output.json"
    v76 = {row["id"]: row for row in json.loads(v76_path.read_text(encoding="utf-8"))["cases"]}
    out_path = HERE / "prototype-output.json"
    done: dict[str, Any] = {}
    if out_path.exists() and not selected:
        done = {row["id"]: row for row in json.loads(out_path.read_text(encoding="utf-8")).get("cases", [])}
    cases: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as tmp:
        build(Path(tmp).resolve() / "s")
        for case_id, form, label, right, builder in probe.case_table():
            if selected and not any(token in case_id for token in selected):
                continue
            if case_id in done:
                cases.append(done[case_id])
                continue
            print("run", case_id, flush=True)
            new = probe.execute_case(case_id, form, label, right, builder)
            old = v76.get(case_id, {})
            expect = _expect(case_id, right)
            cases.append({
                "id": case_id,
                "form": form,
                "case": label,
                "right_answer": right,
                "expect": expect,
                "met": _met(expect, old, new),
                "v76_line": (old.get("lines") or {}).get("line25a" if case_id.startswith("w2.") else "line25b"),
                "v76_blocks": old.get("line_blocks"),
                "v76_refusal": old.get("refusal"),
                "prototype_line": (new.get("lines") or {}).get("line25a" if case_id.startswith("w2.") else "line25b"),
                "prototype_blocks": new.get("line_blocks"),
                "prototype_refusal": new.get("refusal"),
                "lines_identical": old.get("lines") == new.get("lines"),
                "prototype": new,
            })
            out_path.write_text(json.dumps({"core": "v77-scratch", "cases": cases}, indent=2) + "\n", encoding="utf-8")
            print(" ", case_id, "met" if cases[-1]["met"] else "MISS", cases[-1]["prototype_line"], flush=True)
    summary = {
        "cases": len(cases),
        "met": sum(1 for row in cases if row["met"]),
        "lines_identical": sum(1 for row in cases if row["lines_identical"]),
        "answered_changed": [
            row["id"] for row in cases
            if str(row["right_answer"]).startswith("publish") and not row["lines_identical"]
        ],
    }
    body = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {"cases": cases}
    body["summary"] = summary
    body["fixture_survey"] = _survey()
    out_path.write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    print("summary", json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
