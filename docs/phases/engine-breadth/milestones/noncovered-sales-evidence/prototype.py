"""Scratch successor for a sale whose basis was not reported.

Copies content and the v76 release into a temporary directory, adds successor
artifacts, and builds package v79 with tools/package_successor.py. Nothing is
written under packages/. The companion table is wrapped in process so v79
shares v78's declaration. Synthetic demo.* findings only.

    python3 docs/phases/engine-breadth/milestones/noncovered-sales-evidence/prototype.py [case ...]

Writes prototype-rules/ and prototype-output.json beside this file.
"""

from __future__ import annotations

import copy
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
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
NONCOVERED = P + "schedule-d-boundary.noncovered-in-class"
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
TERMS = ("st", "lt")
KINDS = ("proceeds", "basis", "adjustment")
TERM_WORD = {"st": "short-term", "lt": "long-term"}

BUILT: dict[str, Any] = {}


def _questions() -> dict[tuple[str, str | None], str]:
    found: dict[tuple[str, str | None], str] = {}
    for term, word in TERM_WORD.items():
        found[(term, None)] = (
            f"Have you recorded every {word} sale whose basis was not reported to the IRS?"
        )
        found[(term, "proceeds")] = (
            f"What are the proceeds of this {word} sale whose basis was not reported to the IRS?"
        )
        found[(term, "basis")] = (
            f"What is the basis of this {word} sale whose basis was not reported to the IRS?"
        )
        found[(term, "adjustment")] = (
            f"What wash-sale adjustment applies to this {word} sale whose basis was not reported "
            f"to the IRS? Use zero when none of the loss is a wash sale."
        )
    return found


QUESTIONS = _questions()


def _sale_keys() -> list[dict[str, Any]]:
    return [
        {"name": "broker", "kind": "entity", "entity_kind": "tax.us.f1099b-broker"},
        {"name": "statement", "kind": "entity", "entity_kind": "tax.us.f1099b-statement"},
        {"name": "transaction", "kind": "entity", "entity_kind": "tax.us.f1099b-transaction"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _closure_keys() -> list[dict[str, Any]]:
    return [
        {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
        {"name": "tax-year", "kind": "literal", "values": ["2025"]},
    ]


def _fact(fact_id: str, title: str, value_schema: dict[str, Any], keys: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": "fact-type.v2",
        "id": fact_id,
        "version": "v1",
        "title": title,
        "nature": "determinable",
        "identity_keys": keys,
        "value_schema": value_schema,
        "supersession": {"policy": "free"},
    }


def _family_id(term: str, kind: str | None) -> str:
    stem = f"{P}f1099b.noncovered-{term}"
    return stem if kind is None else f"{stem}-{kind}"


def _member_fact(term: str, kind: str | None) -> str:
    stem = f"{P}f1099b.noncovered-{term}-txn"
    return stem if kind is None else f"{stem}.{kind}"


def _object_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["proceeds", "basis", "basis_reported_to_irs", "long_term"],
        "properties": {
            "proceeds": {"type": "number", "minimum": 0},
            "basis": {"type": "number", "minimum": 0},
            "basis_reported_to_irs": {"enum": ["yes", "no"]},
            "long_term": {"enum": ["yes", "no"]},
        },
    }


def _bundle(term: str) -> dict[str, Any]:
    word = TERM_WORD[term]
    facts = [
        _fact(
            _member_fact(term, None),
            f"One {word} sale whose basis was not reported to the IRS. The filer supplies the basis.",
            _object_schema(),
            _sale_keys(),
        ),
        _fact(
            _family_id(term, None) + ".source-closure",
            f"Closure of the {word} basis-not-reported sale family.",
            {"type": "boolean"},
            _closure_keys(),
        ),
    ]
    for kind in KINDS:
        facts.append(
            _fact(
                _member_fact(term, kind),
                f"Scalar {kind} for a {word} sale whose basis was not reported to the IRS.",
                {"type": "number", "minimum": 0},
                _sale_keys(),
            )
        )
        facts.append(
            _fact(
                _family_id(term, kind) + ".source-closure",
                f"Closure of the {word} basis-not-reported {kind} family.",
                {"type": "boolean"},
                _closure_keys(),
            )
        )
    return {
        "schema": "bundle.v2",
        "id": f"{P}f1099b.noncovered-{term}.vocabulary",
        "version": "v1",
        "label": f"Vocabulary for {word} sales whose basis was not reported to the IRS",
        "fact_types": facts,
    }


def _boundary_bundle() -> dict[str, Any]:
    return {
        "schema": "bundle.v2",
        "id": P + "schedule-d-boundary.noncovered-in-class.vocabulary",
        "version": "v1",
        "label": "Whether Form 8949 work beyond covered sales and code W is only boxes B and E",
        "fact_types": [
            {
                "schema": "fact-type.v2",
                "id": NONCOVERED,
                "version": "v1",
                "title": (
                    "Whether this return's Form 8949 work beyond covered sales and code W is only "
                    "boxes B and E (a filer-supplied basis and an optional wash-sale adjustment). "
                    "yes or no."
                ),
                "nature": "determinable",
                "identity_keys": [{"name": "tax-year", "kind": "literal", "values": ["2025"]}],
                "value_schema": {"enum": ["yes", "no"]},
                "supersession": {"policy": "free"},
            }
        ],
    }


def _family(term: str, kind: str | None) -> dict[str, Any]:
    word = TERM_WORD[term]
    if kind is None:
        title = f"{word} sales whose basis was not reported to the IRS, tax year 2025"
        claim = f"Every {word} sale whose basis was not reported to the IRS is recorded as of the keyed horizon."
    else:
        title = f"{word} basis-not-reported {kind}, tax year 2025"
        claim = f"Every {kind} amount of a {word} sale whose basis was not reported to the IRS is recorded as of the keyed horizon."
    family_id = _family_id(term, kind)
    return {
        "schema": "source-family.v1",
        "id": family_id,
        "version": "v1",
        "title": title,
        "scope": dict(SCOPE),
        "closure_claim": claim,
        "member_predicate": {"fact_type": _member_fact(term, kind)},
        "authorizes_subtotal": family_id + "-subtotal",
    }


def _mapping(term: str, kind: str | None) -> dict[str, Any]:
    family_id = _family_id(term, kind)
    suffix = "" if kind is None else f"-{kind}"
    return {
        "schema": "source-closure-mapping.v3",
        "id": f"{P}closure-mapping.f1099b.noncovered-{term}{suffix}",
        "version": "v1",
        "family": {"id": family_id, "version": "v1"},
        "member_fact_type": {"id": _member_fact(term, kind), "version": "v1"},
        "closure_fact_type": {"id": family_id + ".source-closure", "version": "v1"},
        "closure_horizon_key": "family-horizon",
        "closure_question": QUESTIONS[(term, kind)],
        "admits_symbol": family_id + "-subtotal",
        "admission": {"condition": "current-literal-true"},
    }


def _subtotal(term: str, kind: str) -> dict[str, Any]:
    family_id = _family_id(term, kind)
    return {
        "schema": "rule-artifact.v2",
        "id": f"{P}rule.f1099b-noncovered-{term}-{kind}-subtotal",
        "version": "v1",
        "notes": "PROTOTYPE. Sums one basis-not-reported scalar family. A closed empty family publishes 0.",
        "pins": [],
        "publishes": family_id + "-subtotal",
        "requires": [],
        "role": "computation",
        "scope": {
            "effective_from": "2025-01-01",
            "family": "individual-income-tax",
            "jurisdiction": "US-federal",
            "tax_year": 2025,
        },
        "value": {
            "op": "add",
            "args": [{"name": _member_fact(term, kind), "op": "collect", "source_set": family_id}],
        },
        "blocked": {"code": "SOURCE_SET_UNCLOSED", "missing": [family_id]},
        "when": True,
    }


def _yes(symbol: str) -> dict[str, Any]:
    return {
        "cmp": "eq",
        "left": {"name": symbol, "op": "ref"},
        "op": "categorical_compare",
        "right": {
            "fact_type": {"id": symbol, "version": "v1"},
            "op": "category_literal",
            "value": "yes",
        },
    }


def _line(line: str, term: str) -> dict[str, Any]:
    proceeds = _family_id(term, "proceeds") + "-subtotal"
    basis = _family_id(term, "basis") + "-subtotal"
    adjustment = _family_id(term, "adjustment") + "-subtotal"
    families = [_family_id(term, None), _family_id(term, "proceeds"), _family_id(term, "basis"), _family_id(term, "adjustment")]
    zero = {
        "op": "all",
        "args": [
            {"op": "compare", "cmp": "eq", "left": {"op": "ref", "name": name}, "right": 0}
            for name in (proceeds, basis, adjustment)
        ],
    }
    amount = {
        "op": "add",
        "args": [
            {
                "op": "subtract",
                "left": {"op": "ref", "name": proceeds},
                "right": {"op": "ref", "name": basis},
            },
            {"op": "ref", "name": adjustment},
        ],
    }
    return {
        "schema": "rule-artifact.v4",
        "id": f"{P}rule.schedule-d-line{line}",
        "version": "v1",
        "notes": (
            "PROTOTYPE. Column (h) is proceeds minus basis plus the wash-sale adjustment. "
            "Closed-empty subtotals publish 0 and do not read the noncovered boundary. "
            "A recorded sale publishes only when that boundary is yes."
        ),
        "role": "computation",
        "scope": dict(SCOPE),
        "publishes": f"{P}schedule-d.line-{line}",
        "requires": [proceeds, basis, adjustment],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [proceeds, basis, adjustment]},
        "citations": [{"id": f"{P}citation.schedule-d.line-{line}", "version": "v1"}],
        "pins": [],
        "when": {"op": "all", "args": [{"op": "require_closed", "source_set": family} for family in families]},
        "value": {
            "op": "choose",
            "when": {"op": "any", "args": [zero, _yes(NONCOVERED)]},
            "then": amount,
            "else": {"op": "block", "code": "DEPENDENCY_ABSENT"},
        },
    }


def _insert_ref(args: list[dict[str, Any]], after: str, name: str) -> list[dict[str, Any]]:
    found = False
    out: list[dict[str, Any]] = []
    for arg in args:
        out.append(arg)
        if arg.get("op") == "ref" and arg.get("name") == after:
            out.append({"op": "ref", "name": name})
            found = True
    if not found:
        raise SystemExit(f"ref {after} not in sum")
    return out


def _sum_successor(source_name: str, version: str, after: str, added: str, note: str) -> dict[str, Any]:
    rule = json.loads((probe.CONTENT / source_name).read_text(encoding="utf-8"))
    rule["version"] = version
    rule["requires"] = _insert_names(rule["requires"], after, added)
    rule["blocked"]["missing"] = _insert_names(rule["blocked"]["missing"], after, added)
    rule["value"]["args"] = _insert_ref(rule["value"]["args"], after, added)
    rule["notes"] = rule.get("notes", "") + " " + note
    return rule


def _insert_names(names: list[str], after: str, added: str) -> list[str]:
    if after not in names:
        raise SystemExit(f"{after} not in {names}")
    out: list[str] = []
    for name in names:
        out.append(name)
        if name == after:
            out.append(added)
    return out


def _ne(symbol: str) -> dict[str, Any]:
    return {
        "cmp": "ne",
        "left": {"name": symbol, "op": "ref"},
        "op": "compare",
        "right": 0,
    }


def _patch_preferential(rule: dict[str, Any]) -> dict[str, Any]:
    """Third gate arm, and line 2 / line 9 as Schedule D activity. Do not touch other anys."""
    gate: list[dict[str, Any]] = []
    activity: list[dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("op") == "any" and isinstance(node.get("args"), list):
                args = node["args"]
                names = [
                    (arg.get("left") or {}).get("name")
                    for arg in args
                    if isinstance(arg, dict) and arg.get("op") == "categorical_compare"
                ]
                if names == [
                    P + "schedule-d-boundary.no-form8949-sources",
                    P + "schedule-d-boundary.no-other-form8949-adjustments",
                ]:
                    gate.append(node)
                compared = [
                    (arg.get("left") or {}).get("name")
                    for arg in args
                    if isinstance(arg, dict) and arg.get("op") == "compare"
                ]
                if (
                    P + "schedule-d.line-1b" in compared
                    and P + "schedule-d.line-8b" in compared
                    and P + "schedule-d.line-2" not in compared
                ):
                    activity.append(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(rule)
    if len(gate) != 1:
        raise SystemExit(f"expected one boundary gate, found {len(gate)}")
    if len(activity) < 2:
        raise SystemExit(f"expected the line 1b/8b activity checks, found {len(activity)}")
    gate[0]["args"].append(_yes(NONCOVERED))
    for node in activity:
        node["args"].extend([_ne(P + "schedule-d.line-2"), _ne(P + "schedule-d.line-9")])
    for key in ("requires",):
        rule[key] = list(rule[key]) + [P + "schedule-d.line-2", P + "schedule-d.line-9"]
    rule["blocked"]["missing"] = list(rule["blocked"]["missing"]) + [
        P + "schedule-d.line-2",
        P + "schedule-d.line-9",
    ]
    rule["version"] = "v7"
    rule["notes"] = (
        rule.get("notes", "")
        + " PROTOTYPE v7: line 2 and line 9 count as Schedule D activity, and the "
        "basis-not-reported boundary is a third arm after Path A and Path B."
    )
    rule["_prototype_activity_anys"] = len(activity)
    return rule


def _part(box: str, term: str, kind: str, label: str) -> dict[str, Any]:
    family_id = _family_id(term, kind)
    subtotal = family_id + "-subtotal"
    return {
        "part_id": f"box-{box}-{kind}",
        "label": label,
        "authority": {"kind": "single_family", "source_family": {"id": family_id, "version": "v1"}},
        "row_sets": [
            {
                "rows": {
                    "op": "collect_members",
                    "member_fact_type": {"id": _member_fact(term, kind), "version": "v1"},
                    "source_family": {"id": family_id, "version": "v1"},
                },
                "subtotal_symbol": subtotal,
            }
        ],
        "adjustment_rows": [],
        "tie_out": {
            "line_symbol": subtotal,
            "operation": "subtract",
            "positive_subtotals": [subtotal],
            "adjustment_subtotals": [],
        },
    }


def _attachment() -> dict[str, Any]:
    rule = json.loads((probe.CONTENT / "attachment.f8949.v2.json").read_text(encoding="utf-8"))
    rule["version"] = "v3"
    rule["title"] = (
        "PROTOTYPE Form 8949 attachment: box A/D kept, plus box B and box E for a filer-supplied basis."
    )
    rule["requirement"]["subtotals"] = list(rule["requirement"]["subtotals"]) + [
        _family_id("st", "proceeds") + "-subtotal",
        _family_id("lt", "proceeds") + "-subtotal",
    ]
    rule["itemizations"] = list(rule["itemizations"]) + [
        _part("b", "st", "proceeds", "Part I box B column (d): short-term basis-not-reported proceeds"),
        _part("b", "st", "basis", "Part I box B column (e): short-term basis the filer supplies"),
        _part("b", "st", "adjustment", "Part I box B column (g): short-term wash-sale adjustment"),
        _part("e", "lt", "proceeds", "Part II box E column (d): long-term basis-not-reported proceeds"),
        _part("e", "lt", "basis", "Part II box E column (e): long-term basis the filer supplies"),
        _part("e", "lt", "adjustment", "Part II box E column (g): long-term wash-sale adjustment"),
    ]
    return rule


def _form_field(line: str, label: str, explain: dict[str, str]) -> dict[str, Any]:
    field = json.loads((probe.CONTENT / "schedule-d.line-1b.form-field.v2.json").read_text(encoding="utf-8"))
    field["id"] = f"{P}schedule-d.line-{line}"
    field["version"] = "v1"
    field["line"] = f"{line}-h"
    field["label"] = label
    field["description"] = f"Schedule D (2025) line {line} column (h). PROTOTYPE."
    field["binds_symbol"] = f"{P}schedule-d.line-{line}"
    field["citation"] = {"id": f"{P}citation.schedule-d.line-{line}", "version": "v1"}
    for key, text in explain.items():
        field["dispositions"][key]["explain"] = text
    return field


def _citation(line: str) -> dict[str, Any]:
    body = json.loads((probe.CONTENT / "citation.schedule-d.line-1b.json").read_text(encoding="utf-8"))
    body["id"] = f"{P}citation.schedule-d.line-{line}"
    return body


def _retitle(source_name: str, version: str, replacements: dict[str, str]) -> dict[str, Any]:
    field = json.loads((probe.CONTENT / source_name).read_text(encoding="utf-8"))
    field["version"] = version
    for bucket in field["dispositions"].values():
        text = bucket.get("explain")
        if isinstance(text, str):
            for old, new in replacements.items():
                text = text.replace(old, new)
            bucket["explain"] = text
    return field


def _write(content: Path, rules: Path, name: str, body: dict[str, Any]) -> dict[str, str]:
    text = json.dumps(body, indent=2) + "\n"
    (content / name).write_text(text, encoding="utf-8")
    (rules / name).write_text(text, encoding="utf-8")
    role = {
        "bundle.v2": "fact-type-bundle",
        "source-family.v1": "source-family",
        "source-closure-mapping.v3": "source-closure-mapping",
        "citation.v1": "citation",
        "form-field.v3": "form-field",
        "attachment-rule.v8": "attachment-rule",
    }.get(body["schema"], "computation")
    return {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role}


def _declare_v79() -> None:
    original = loader.domain_package_companion_declarations

    def with_v79() -> dict[tuple[str, str], dict[str, Any]]:
        declarations = dict(original())
        declarations[(P + "package.core-calculations", "v79")] = declarations[
            (P + "package.core-calculations", "v78")
        ]
        return declarations

    loader.domain_package_companion_declarations = with_v79  # type: ignore[method-assign]


def build(scratch: Path) -> dict[str, Any]:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(probe.CONTENT, content)
    shutil.copytree(probe.RELEASE_DIR, releases)
    rules = HERE / "prototype-rules"
    if rules.exists():
        shutil.rmtree(rules)
    rules.mkdir()
    written: list[dict[str, str]] = []
    bundles = {"st": _bundle("st"), "lt": _bundle("lt"), "boundary": _boundary_bundle()}
    facts = {fact["id"]: fact for bundle in bundles.values() for fact in bundle["fact_types"]}
    families = [_family(term, kind) for term in TERMS for kind in (None, *KINDS)]
    mapping_bodies = [_mapping(term, kind) for term in TERMS for kind in (None, *KINDS)]
    artifacts: list[tuple[str, dict[str, Any]]] = [
        ("f1099b-noncovered-st.bundle.json", bundles["st"]),
        ("f1099b-noncovered-lt.bundle.json", bundles["lt"]),
        ("schedule-d-boundary-noncovered.bundle.json", bundles["boundary"]),
    ]
    for family in families:
        artifacts.append((f"family.{family['id'].split('.')[-1]}.json", family))
    for mapping in mapping_bodies:
        artifacts.append((f"{mapping['id'].split('.')[-1]}.json", mapping))
    for term in TERMS:
        for kind in KINDS:
            rule = _subtotal(term, kind)
            artifacts.append((f"rule.f1099b-noncovered-{term}-{kind}-subtotal.json", rule))
    line2 = _line("2", "st")
    line9 = _line("9", "lt")
    line7 = _sum_successor(
        "rule.schedule-d-line7.v3.json",
        "v4",
        P + "schedule-d.line-1b",
        P + "schedule-d.line-2",
        "PROTOTYPE v4 adds line 2.",
    )
    line15 = _sum_successor(
        "rule.schedule-d-line15.v5.json",
        "v6",
        P + "schedule-d.line-8b",
        P + "schedule-d.line-9",
        "PROTOTYPE v6 adds line 9.",
    )
    preferential = json.loads((probe.CONTENT / "rule.selected-preferential-base.v6.json").read_text(encoding="utf-8"))
    preferential = _patch_preferential(preferential)
    activity_count = preferential.pop("_prototype_activity_anys")
    attachment = _attachment()
    field2 = _form_field(
        "2",
        "Line 2 column (h)",
        {
            "published_value": "Schedule D line 2, column (h), is your short-term Form 8949 box B gain or loss, proceeds minus basis plus adjustments.",
            "computed_zero": "Schedule D line 2, column (h), is zero because your box B proceeds, basis, and adjustments net to zero.",
            "closure_backed_zero": "You said you have no short-term sales whose basis was not reported, so Schedule D line 2, column (h), is zero.",
            "blocked": "Schedule D line 2, column (h), has no value yet. It is waiting for the basis of a short-term sale whose basis was not reported to the IRS.",
        },
    )
    field9 = _form_field(
        "9",
        "Line 9 column (h)",
        {
            "published_value": "Schedule D line 9, column (h), is your long-term Form 8949 box E gain or loss, proceeds minus basis plus adjustments.",
            "computed_zero": "Schedule D line 9, column (h), is zero because your box E proceeds, basis, and adjustments net to zero.",
            "closure_backed_zero": "You said you have no long-term sales whose basis was not reported, so Schedule D line 9, column (h), is zero.",
            "blocked": "Schedule D line 9, column (h), has no value yet. It is waiting for the basis of a long-term sale whose basis was not reported to the IRS.",
        },
    )
    field7 = _retitle(
        "schedule-d.line-7.form-field.v2.json",
        "v3",
        {
            "lines 1a, 1b, and 6": "lines 1a, 1b, 2, and 6",
            "lines 1a, 1b, and 6 is still open": "lines 1a, 1b, 2, and 6 is still open",
        },
    )
    field15 = _retitle(
        "schedule-d.line-15.form-field.v2.json",
        "v3",
        {"lines 8a, 8b, 13, and 14": "lines 8a, 8b, 9, 13, and 14"},
    )
    field15["dispositions"]["published_value"]["explain"] = (
        "Schedule D line 15 adds lines 8a, 8b, 9, 13, and 14."
    )
    field15["dispositions"]["blocked"]["explain"] = (
        "Schedule D line 15 has no value yet. It is waiting for whichever of lines 8a, 8b, 9, 13, and 14 is still open."
    )
    artifacts.extend(
        [
            ("rule.schedule-d-line2.json", line2),
            ("rule.schedule-d-line9.json", line9),
            ("rule.schedule-d-line7.v4.json", line7),
            ("rule.schedule-d-line15.v6.json", line15),
            ("rule.selected-preferential-base.v7.json", preferential),
            ("attachment.f8949.v3.json", attachment),
            ("schedule-d.line-2.form-field.json", field2),
            ("schedule-d.line-9.form-field.json", field9),
            ("schedule-d.line-7.form-field.v3.json", field7),
            ("schedule-d.line-15.form-field.v3.json", field15),
            ("citation.schedule-d.line-2.json", _citation("2")),
            ("citation.schedule-d.line-9.json", _citation("9")),
        ]
    )
    for name, body in artifacts:
        written.append(_write(content, rules, name, body))
    (rules / "_members.json").write_text(json.dumps(written, indent=2) + "\n", encoding="utf-8")
    members: list[dict[str, Any]] = []
    replaced = {
        (P + "rule.schedule-d-line7", "v4"),
        (P + "rule.schedule-d-line15", "v6"),
        (P + "rule.selected-preferential-base", "v7"),
        (P + "rule.attachment.f8949", "v3"),
        (P + "schedule-d.line-7", "v3"),
        (P + "schedule-d.line-15", "v3"),
    }
    old = {
        (P + "rule.schedule-d-line7", "v4"): {"version": "v3", "schema": "rule-artifact.v3", "role": "computation"},
        (P + "rule.schedule-d-line15", "v6"): {"version": "v5", "schema": "rule-artifact.v3", "role": "computation"},
        (P + "rule.selected-preferential-base", "v7"): {"version": "v6", "schema": "rule-artifact.v3", "role": "computation"},
        (P + "rule.attachment.f8949", "v3"): {"version": "v2", "schema": "attachment-rule.v8", "role": "attachment-rule"},
        (P + "schedule-d.line-7", "v3"): {"version": "v2", "schema": "form-field.v3", "role": "form-field"},
        (P + "schedule-d.line-15", "v3"): {"version": "v2", "schema": "form-field.v3", "role": "form-field"},
    }
    for member in written:
        key = (member["id"], member["version"])
        if key in replaced:
            prior = old[key]
            members.append({
                "op": "replace",
                "old": {"id": member["id"], "version": prior["version"], "schema": prior["schema"], "role": prior["role"]},
                "new": member,
            })
        else:
            members.append({"op": "add", "new": member})
    pinned = json.loads((content / "package.core-calculations.v78.json").read_text(encoding="utf-8"))
    entry_keys = {(entry["id"], entry["version"]) for entry in pinned["entrypoints"]}
    entrypoints: list[dict[str, Any]] = []
    for edit in members:
        if edit["op"] == "replace" and (edit["old"]["id"], edit["old"]["version"]) in entry_keys:
            entrypoints.append({
                "op": "replace",
                "old": {"id": edit["old"]["id"], "version": edit["old"]["version"]},
                "new": {"id": edit["new"]["id"], "version": edit["new"]["version"]},
            })
        elif edit["op"] == "add":
            entrypoints.append({
                "op": "add",
                "value": {"id": edit["new"]["id"], "version": edit["new"]["version"]},
            })
    changes = {
        "package_version": "v79",
        "release_version": "v77",
        "members": members,
        "entrypoints": entrypoints,
        "registry_sort": "id_version",
        "registry_new_key_order": ["checksum", "id", "version"],
    }
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v78.json",
        content / "published-packages.v76.json",
        releases / "demo.release.sli-worksheet-integration.2025.v76.json",
        content,
        scratch / "changes.json",
        scratch / "out",
    )
    for name, folder, target in (
        ("package.json", content, "package.core-calculations.v79.json"),
        ("registry.json", content, "published-packages.v77.json"),
        ("release.json", releases, "demo.release.sli-worksheet-integration.2025.v77.json"),
    ):
        shutil.copy(scratch / "out" / name, folder / target)
    probe.CONTENT = content
    probe.PACKAGE = "package.core-calculations.v79.json"
    probe.PACKAGE_VERSION = "v79"
    probe.REGISTRY = "published-packages.v77.json"
    probe.RELEASE_DIR = releases
    probe.RELEASE = "demo.release.sli-worksheet-integration.2025.v77.json"
    probe.RELEASE_VERSION = "v77"
    _declare_v79()
    report["activity_anys"] = activity_count
    report["members"] = len(members)
    member_of = {
        _family_id(term, kind): _member_fact(term, kind)
        for term in TERMS
        for kind in (None, *KINDS)
    }
    BUILT.clear()
    BUILT.update({
        "bundles": bundles,
        "facts": facts,
        "families": [family["id"] for family in families],
        "member_of": member_of,
    })
    return report


def _adopt(acts: list[dict[str, Any]], bundle: dict[str, Any]) -> None:
    wanted = {fact["id"] for fact in bundle["fact_types"]}
    for act in acts:
        if act.get("kind") != "bundle-adoption":
            continue
        payload = act.get("payload")
        existing = payload.get("bundle") if isinstance(payload, dict) else None
        if isinstance(existing, dict) and wanted & {fact["id"] for fact in existing.get("fact_types") or []}:
            return
    probe._add(acts, "bundle-adoption", {"bundle": bundle})


def _known_entity(acts: list[dict[str, Any]], entity_id: str) -> bool:
    for act in acts:
        if act.get("kind") != "entity-introduced":
            continue
        payload = act.get("payload")
        entity = payload.get("entity") if isinstance(payload, dict) else None
        if isinstance(entity, dict) and entity.get("id") == entity_id:
            return True
    return False


def _open_families(acts: list[dict[str, Any]], skip_close: set[str]) -> None:
    for family_id in BUILT["families"]:
        slug = family_id.removeprefix(P + "f1099b.")
        horizon = f"demo.ns.open.{slug}.h0"
        probe._add(acts, "horizon-genesis", {
            "family": {"id": family_id, "version": "v1"},
            "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
            "horizon_id": horizon,
        })
        if family_id not in skip_close:
            probe._close(acts, family_id + ".source-closure", horizon, f"demo.ns.open.{slug}.closure")


def _record(acts: list[dict[str, Any]], family_id: str, value: object, tag: str) -> None:
    fact = BUILT["facts"][BUILT["member_of"][family_id]]
    out_index = acts
    stripped = probe._strip_closure(out_index, family_id + ".source-closure")
    if stripped is not out_index:
        out_index[:] = stripped
    declared: list[tuple[str, str]] = []
    for key in fact["identity_keys"]:
        if key["kind"] == "entity":
            entity_id = f"demo.ns.{tag}.{key['name']}"
            if not _known_entity(out_index, entity_id):
                probe._introduce(out_index, entity_id, key["entity_kind"])
            declared.append((key["name"], entity_id))
        else:
            declared.append((key["name"], key["values"][0]))
    from packages.kernel.facts import fact_id_for
    from tests.test_refund_or_amount_owed_track1 import _attested

    head = probe.horizons(out_index, family_id)[-1]
    slug = family_id.removeprefix(P + "f1099b.")
    successor = f"demo.ns.{tag}.{slug}.h1"
    probe._add(out_index, "member-transition", {
        "family": {"id": family_id, "version": "v1"},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {
            "action": "assert",
            "finding": _attested(
                f"demo.ns.{tag}.{slug}.member",
                fact_id_for(fact["id"], tuple(declared)),
                value,
            ),
        },
        "successor": {"id": successor, "predecessor": head},
    })
    probe._close(out_index, family_id + ".source-closure", successor, f"demo.ns.{tag}.{slug}.closure")


def _sale(acts: list[dict[str, Any]], term: str, proceeds: float, basis: float | None, tag: str, adjustment: float | None = None) -> None:
    value: dict[str, Any] = {
        "proceeds": proceeds,
        "basis_reported_to_irs": "no",
        "long_term": "yes" if term == "lt" else "no",
    }
    if basis is not None:
        value["basis"] = basis
    _record(acts, _family_id(term, None), value, tag)
    _record(acts, _family_id(term, "proceeds"), proceeds, tag)
    if basis is not None:
        _record(acts, _family_id(term, "basis"), basis, tag)
    if adjustment is not None:
        _record(acts, _family_id(term, "adjustment"), adjustment, tag)


def _with_boundaries(acts: list[dict[str, Any]], answer: str) -> list[dict[str, Any]]:
    done = probe.boundary(acts, "no", "no")
    return probe.answer(done, NONCOVERED, answer, "inclass")


def _prepared(skip_close: set[str] | None = None) -> list[dict[str, Any]]:
    acts = copy.deepcopy(ccr.base_return())
    for bundle in BUILT["bundles"].values():
        _adopt(acts, bundle)
    _open_families(acts, skip_close or set())
    return acts


def cases() -> dict[str, list[dict[str, Any]]]:
    raw = copy.deepcopy(ccr.base_return())
    closed = _prepared()
    gain = _prepared()
    _sale(gain, "lt", 6000.0, 2000.0, "ltgain")
    loss = _prepared()
    _sale(loss, "st", 2000.0, 8000.0, "stloss")
    mixed = _prepared()
    _sale(mixed, "lt", 6000.0, 2000.0, "mxlt")
    covered = probe.txn(proceeds=5000.0, basis=4000.0, long_term="no", reported="yes", covered="yes")
    mixed = probe.record(mixed, P + "f1099b.covered-st", covered, "mxst")
    mixed = probe.record(mixed, P + "f1099b.covered-st-proceeds", 5000.0, "mxstp")
    mixed = probe.record(mixed, P + "f1099b.covered-st-basis", 4000.0, "mxstb")
    washed = _prepared()
    _sale(washed, "lt", 4000.0, 7000.0, "wash", adjustment=1000.0)
    unclosed = _prepared({_family_id("lt", "basis")})
    _record(unclosed, _family_id("lt", None), {
        "proceeds": 6000.0,
        "basis": 2000.0,
        "basis_reported_to_irs": "no",
        "long_term": "yes",
    }, "openb")
    _record(unclosed, _family_id("lt", "proceeds"), 6000.0, "openb")
    omitted = _prepared()
    _sale(omitted, "lt", 6000.0, None, "omit")
    return {
        "wage_unclosed": raw,
        "wage_closed_empty": ccr._renumbered(closed),
        "lt_gain": ccr._renumbered(_with_boundaries(gain, "yes")),
        "st_loss": ccr._renumbered(_with_boundaries(loss, "yes")),
        "mixed": ccr._renumbered(_with_boundaries(mixed, "yes")),
        "wash": ccr._renumbered(_with_boundaries(washed, "yes")),
        "basis_unclosed": ccr._renumbered(_with_boundaries(unclosed, "yes")),
        "basis_omitted": ccr._renumbered(_with_boundaries(omitted, "yes")),
        "boundary_no": ccr._renumbered(_with_boundaries(gain, "no")),
    }


def _line_value(result: dict[str, Any], field_id: str) -> Any:
    for row in result.get("lines") or []:
        if row.get("id") == field_id:
            return row.get("value"), row.get("disposition")
    return None, None


def _blocked_codes(result: dict[str, Any], token: str) -> list[dict[str, Any]]:
    return [row for row in result.get("blocked") or [] if token in str(row.get("artifact_id", ""))]


def _reasons(result: dict[str, Any], field_id: str) -> list[str]:
    for row in result.get("lines") or []:
        if row.get("id") == field_id:
            return list(row.get("reasons") or [])
    return []


def _survey() -> list[dict[str, Any]]:
    needles = (
        "lines 1a, 1b, and 6 add to zero",
        "lines 8a, 8b, 13, and 14 add to zero",
    )
    hits: list[dict[str, Any]] = []
    for root in (REPO / "tests", REPO / "packages" / "sample_data"):
        for path in root.rglob("*"):
            if path.suffix not in {".json", ".py", ".md"} or not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            found = [needle for needle in needles if needle in text]
            if found:
                hits.append({"path": str(path.relative_to(REPO)), "needles": found})
    return hits


def _expect(name: str, result: dict[str, Any]) -> dict[str, Any]:
    def value(field_id: str) -> Any:
        return _line_value(result, field_id)[0]

    summary: dict[str, Any] = {
        "error": result.get("error"),
        "message": result.get("message"),
        "line2": value(P + "schedule-d.line-2"),
        "line9": value(P + "schedule-d.line-9"),
        "line1a": value(P + "schedule-d.line-1a"),
        "line7": value(P + "schedule-d.line-7"),
        "line15": value(P + "schedule-d.line-15"),
        "line16": value(P + "schedule-d.line-16"),
        "line21": value(P + "schedule-d.line-21"),
        "line7a": value(P + "form1040.line-7a"),
        "taxable": value(P + "form1040.line-15"),
        "tax": value(P + "form1040.line-16"),
        "preferential": value(P + "capital-gains.selected-preferential-base"),
        "attachments": result.get("attachments"),
        "groups": result.get("groups"),
        "line9_reasons": _reasons(result, P + "schedule-d.line-9")[:2],
        "line2_reasons": _reasons(result, P + "schedule-d.line-2")[:2],
    }
    if name == "wage_closed_empty":
        summary["met"] = (
            summary["taxable"] == 34250
            and summary["tax"] == 3875
            and summary["line7a"] == 0
            and summary["preferential"] == 0
            and summary["line7"] == 0
            and summary["line15"] == 0
        )
    return summary


def main() -> None:
    selected = set(sys.argv[1:])
    with tempfile.TemporaryDirectory() as tmp:
        report = build(Path(tmp).resolve() / "s")
        print("successor", report["package"]["version"], "members", report["members"], "activity", report["activity_anys"], flush=True)
        print("inherited", report["inherited_inconsistencies"], flush=True)
        built = cases()
        results: dict[str, Any] = {}
        for name, acts in built.items():
            if selected and name not in selected:
                continue
            print("run", name, flush=True)
            try:
                results[name] = probe.run_one(acts, f"demo.ns.proto.{name}")
            except Exception as exc:  # noqa: BLE001 — record the failure
                results[name] = {
                    "error": type(exc).__name__,
                    "message": probe.scrub(str(exc))[:800],
                }
            print(name, results[name].get("error") or results[name].get("refusal") or "ok", flush=True)
    digest = {name: _expect(name, result) for name, result in results.items()}
    payload = {
        "successor": {
            "package": report["package"]["version"],
            "release": report["release"]["version"],
            "members": report["members"],
            "activity_anys": report["activity_anys"],
            "inherited_inconsistencies": report["inherited_inconsistencies"],
        },
        "digest": digest,
        "sentence_files": _survey(),
        "cases": results,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    text = probe.scrub(text)
    out = HERE / "prototype-output.json"
    out.write_text(text, encoding="utf-8")
    print(f"wrote {out.name} ({out.stat().st_size} bytes)", flush=True)
    for name, row in digest.items():
        print(name, {key: row[key] for key in ("error", "line2", "line9", "line7", "line7a", "line21", "tax", "preferential", "met") if key in row and row[key] is not None}, flush=True)


if __name__ == "__main__":
    main()
