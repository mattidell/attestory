"""Scratch core v82: the content fixes the sale family audit (P0) proposes.

Evidence for docs/phases/engine-breadth/milestones/sale-family-audit.md.
Copies the production content and release directories into a temporary
directory outside the repository, writes the successor members there,
generates package v82 / registry v80 / release v80 from v81 with
``tools.package_successor``, and prints the scratch core's location as a
``Core`` (JSON) for ``probe.py --core=...`` and ``rerun_v81.py``. Nothing
under packages/ is written. Imports no other evidence module.

    python3 docs/phases/engine-breadth/milestones/sale-family-audit-evidence/prototype.py <scratch-dir> [fix ...]

With no fix named, every fix in ``FIXES`` and every Track 0 repair in ``REPAIRS`` is
built; name ``decided`` to build ``FIXES`` alone. Writes
prototype-build.json beside this file (the member list; the scratch path is
not recorded). The loader entries a scratch core needs are applied per run by
``audit_harness.loader_entries`` (v82 copies v81's).

Fixes (each a switch):

- ``tax_activity``: Form 1040 line 16 v7. v6 computed the tax only when
  Exception 1 holds (Schedule D not required) unless a line 1a or 8a sale
  had proceeds. Any recorded sale or carryover now selects the Schedule D
  route, so a return whose sales are on Form 8949 computes its tax when
  the Exception 1 question is answered truthfully.
- ``no1099b_count``: return-level counts of the box C and box F sales,
  read by both attachments, so a box C or F sale for 0 with basis 0 still
  requires Form 8949 and Schedule D.
- ``base_activity``: the preferential base v10 and Form 1040 line 7a v9
  treat any recorded sale (the eight sale counts and the two box C and F
  counts) as Schedule D activity, as line 16 v7 does.
- ``admission_reads``: the covered and code W admission rules v2 also read
  the sale's long_term flag (a sale on the other term's family is refused),
  box 1g on a line 1a or 8a sale (refused: it is a code W sale), and its
  own amount rows (a row that differs from the sale is refused). Lines 1a,
  8a, 1b and 8b name the new reasons.
- ``paired_rows``: the admission checks require each sale's own amount rows
  (require_paired), so a sale recorded without its rows, or rows recorded
  on another transaction, is refused. Off, a missing row still publishes the
  line without that sale (d8).
- ``box4_question``: a new question, read only when a Form 1099-B sale is
  recorded: does any Form 1099-B show federal income tax withheld in box 4?
  "yes" blocks Form 1040 line 25b and says why.
- ``box7_question``: a new question, read only when a Form 1099-B sale is
  recorded: is box 7 (loss not allowed) checked on any Form 1099-B? "yes"
  blocks Schedule D line 16 and says why.

Track 0 repairs (each needs the fix it repairs):

- ``statement_box4`` (repairs ``box4_question``): the box 4 answer is one
  answer per recorded Form 1099-B statement, not one per return. Line 25b
  requires an answer for the statement of every recorded Form 1099-B sale
  (require_paired on the statement key), so a sale from a statement the
  answer did not cover blocks the line and asks again. A "yes" on any
  statement blocks the line. A single return-level "no" stayed current when
  a sale from a new statement arrived, and line 25b published without that
  statement's withholding.
- ``statement_box7`` (repairs ``box7_question``): the same for box 7 and
  Schedule D line 16.
- ``field_words`` (repairs the words of ``tax_activity`` and
  ``base_activity``): Form 1040 line 16 (field v3) and line 7a (field v2)
  say that they also wait for the answers about each kind of sale, which
  their v7 and v9 producers now read. Their v2 and v1 blocked sentences
  named only the inputs the earlier producers read.
"""

from __future__ import annotations

import copy
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.package_successor import generate_to_directory  # noqa: E402

P = "tax.us.2025."
CONTENT = REPO / "packages/content/tax/2025"
RELEASES = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
RELEASE_STEM = "demo.release.sli-worksheet-integration.2025"
FROM = {"package": "v81", "registry": "v79", "release": "v79"}
TO = {"package": "v82", "registry": "v80", "release": "v80"}
FIXES = ("tax_activity", "no1099b_count", "base_activity", "admission_reads", "paired_rows", "box4_question",
         "box7_question")
# Track 0 repairs (track0-closure.md). Each is a switch on top of FIXES; ``main`` builds them all by default,
# and ``FIXES`` alone builds the decided design.
REPAIRS = ("statement_box4", "statement_box7", "field_words")
SWITCHES = FIXES + REPAIRS
TERMS = ("st", "lt")
ROLE = {"bundle.v2": "fact-type-bundle", "input-question.v1": "input-question", "form-field.v3": "form-field",
        "form-field.v2": "form-field",
        "attachment-rule.v8": "attachment-rule"}
SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}

# ---- reading v81 --------------------------------------------------------------------


def _index() -> dict[tuple[str, str], tuple[str, dict[str, Any]]]:
    out: dict[tuple[str, str], tuple[str, dict[str, Any]]] = {}
    for path in CONTENT.glob("*.json"):
        try:
            body = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(body, dict) and "id" in body and "version" in body:
            out[(str(body["id"]), str(body["version"]))] = (path.name, body)
    return out


INDEX = _index()
PACKAGE = json.loads((CONTENT / f"package.core-calculations.{FROM['package']}.json").read_text(encoding="utf-8"))
MEMBERS = {m["id"]: m for m in PACKAGE["members"]}


def current(member_id: str) -> tuple[str, dict[str, Any]]:
    """The v81 member: (file name, body)."""
    m = MEMBERS[P + member_id]
    name, body = INDEX[(m["id"], m["version"])]
    return name, copy.deepcopy(body)


def bump(version: str) -> str:
    return f"v{int(version[1:]) + 1}"


def successor_name(name: str, version: str) -> str:
    """rule.x.v3.json -> rule.x.v4.json; rule.x.json -> rule.x.v2.json."""
    stem = name.removesuffix(".json")
    parts = stem.rsplit(".", 1)
    if len(parts) == 2 and parts[1].startswith("v") and parts[1][1:].isdigit():
        stem = parts[0]
    return f"{stem}.{version}.json"


# ---- expression helpers -------------------------------------------------------------


def ref(name: str, field: str | None = None) -> dict[str, Any]:
    node: dict[str, Any] = {"op": "ref", "name": P + name}
    if field is not None:
        node["field"] = field
    return node


def cmp(op: str, left: Any, right: Any) -> dict[str, Any]:
    return {"op": "compare", "cmp": op, "left": left, "right": right}


def count(member: str, family: str) -> dict[str, Any]:
    return {"op": "count", "name": P + member, "source_set": P + family}


def cat(fact: str, version: str, value: str) -> dict[str, Any]:
    return {"op": "category_literal", "fact_type": {"id": P + fact, "version": version}, "value": value}


def is_yes(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": ref(fact), "right": cat(fact, "v1", "yes")}


def choose(when: Any, then: Any, otherwise: Any) -> dict[str, Any]:
    return {"op": "choose", "when": when, "then": then, "else": otherwise}


def walk(node: Any) -> Any:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


SALE_COUNTS = [f"f1099b.{k}-{t}-count" for k in ("covered", "covered-w", "noncovered", "code-b") for t in TERMS]
NO1099B_COUNTS = [f"f8949.no1099b-{t}-count" for t in TERMS]


def counts(fixes: set[str], *, form_1099b_only: bool = False) -> list[str]:
    return SALE_COUNTS + ([] if form_1099b_only or "no1099b_count" not in fixes else NO1099B_COUNTS)


def any_count(names: list[str]) -> list[dict[str, Any]]:
    return [cmp("gt", ref(name), 0) for name in names]


def widen_activity(node: Any, extra: list[dict[str, Any]]) -> int:
    """Append ``extra`` to every ``any`` whose first argument is 'covered-st proceeds > 0'."""
    hits = 0
    for item in walk(node):
        if item.get("op") != "any":
            continue
        args = item.get("args") or []
        first = args[0] if args else None
        if isinstance(first, dict) and first.get("op") == "compare" and first.get("cmp") == "gt" \
                and first.get("left") == ref("f1099b.covered-st-proceeds-subtotal"):
            item["args"] = args + copy.deepcopy(extra)
            hits += 1
    return hits


def add_requires(body: dict[str, Any], names: list[str]) -> None:
    for name in names:
        if P + name not in body["requires"]:
            body["requires"].append(P + name)


# ---- the fixes ----------------------------------------------------------------------

Out = list[tuple[str, dict[str, Any]]]


def fix_tax_activity(fixes: set[str]) -> Out:
    name, body = current("rule.form1040-line16")
    names = counts(fixes)
    hits = widen_activity(body["when"], any_count(names))
    assert hits == 1, hits
    add_requires(body, names)
    body["version"] = bump(body["version"])
    body["notes"] += (" v7: any recorded sale (a sale count above zero) also selects the Schedule D route, so a "
                      "return whose sales are on Form 8949 computes its tax when Exception 1 does not hold.")
    return [(successor_name(name, body["version"]), body)]


def count_rule(term: str) -> dict[str, Any]:
    _, body = current("rule.f1099b-covered-st-count")
    body.update({
        "id": P + f"rule.f8949-no1099b-{term}-count", "version": "v1",
        "publishes": P + f"f8949.no1099b-{term}-count",
        "blocked": {"code": "SOURCE_SET_UNCLOSED", "missing": [P + f"f8949.no1099b-{term}"]},
        "value": count(f"f8949.no1099b-{term}-txn", f"f8949.no1099b-{term}"),
        "notes": f"The number of {'short' if term == 'st' else 'long'}-term sales recorded without a Form 1099-B "
                 f"(Form 8949 box {'C' if term == 'st' else 'F'}). Both attachments are required when it is above "
                 "zero, so a sale for 0 with basis 0 is still reported.",
    })
    return body


def fix_no1099b_count(fixes: set[str]) -> Out:
    out: Out = [(f"rule.f8949-no1099b-{t}-count.json", count_rule(t)) for t in TERMS]
    for member in ("rule.attachment.f8949", "rule.attachment.schedule-d"):
        name, body = current(member)
        body["requirement"]["subtotals"] += [P + c for c in NO1099B_COUNTS]
        body["version"] = bump(body["version"])
        form = "Form 8949" if member.endswith("f8949") else "Schedule D"
        body["title"] = (f"{form} attachment {body['version']}: the previous requirement, plus the box C and box F "
                         "sale counts, so a box C or F sale for 0 with basis 0 requires it.")
        out.append((successor_name(name, body["version"]), body))
    return out


def fix_base_activity(fixes: set[str]) -> Out:
    out: Out = []
    names = counts(fixes)
    for member, expected in (("rule.selected-preferential-base", 5), ("rule.form1040-line7a", 1)):
        name, body = current(member)
        hits = widen_activity(body["value"], any_count(names)) + widen_activity(body.get("when"), any_count(names))
        assert hits == expected, (member, hits)
        add_requires(body, names)
        if "blocked" in body:
            body["blocked"]["missing"] = list(body["requires"])
        body["version"] = bump(body["version"])
        body["notes"] += (f" {body['version']}: any recorded sale (a sale count above zero) is Schedule D activity, "
                          "so a sale whose column (h) is zero, or a direct sale with zero proceeds, reaches it.")
        out.append((successor_name(name, body["version"]), body))
    return out


# Admission: the covered and code W sales.
ADMISSION_KINDS = ("covered", "covered-w")
NEW_VALUES = [
    {"const": "term-mismatch",
     "description": "The sale says it is of the other term (box 2), so it is recorded on the wrong line."},
    {"const": "needs-form-8949",
     "description": "The sale shows a wash-sale loss disallowed (box 1g), so it is reported on Form 8949 with "
                    "code W, not directly on Schedule D."},
    {"const": "amounts-disagree",
     "description": "A proceeds, basis or wash-sale row differs from the amount on the sale."},
]


def admission_bundle() -> tuple[str, dict[str, Any]]:
    name, body = current("f1099b.covered-admission.vocabulary")
    body["version"] = "v2"
    body["label"] += " (v2: term, box 1g and amount checks)"
    for fact in body["fact_types"]:
        if fact["id"].endswith(".admission"):
            fact["version"] = "v2"
            fact["value_schema"]["oneOf"] += copy.deepcopy(NEW_VALUES)
    return successor_name(name, "v2"), body


def row_agrees(kind: str, term: str, scalar: str, field: str) -> dict[str, Any]:
    row, family = f"f1099b.{kind}-{term}-txn.{scalar}", f"f1099b.{kind}-{term}-{scalar}"
    return {"op": "any", "args": [
        cmp("eq", count(row, family), 0),
        {"op": "all", "args": [
            {"op": "all", "args": [cmp("gt", count(row, family), 0),
                                   {"op": "conditional_dependency_set", "condition": True, "members": [ref(row)]}]},
            cmp("eq", ref(row), ref(f"f1099b.{kind}-{term}-txn", field))]}]}


def admission_rule(kind: str, term: str) -> tuple[str, dict[str, Any]]:
    name, body = current(f"rule.f1099b.{kind}-{term}-txn.admission")
    fact = f"f1099b.{kind}-{term}-txn.admission"
    sale = f"f1099b.{kind}-{term}-txn"
    for node in walk(body["value"]):
        if node.get("op") == "category_literal":
            node["fact_type"]["version"] = "v2"
    flagged = [n for n in walk(body["value"]) if n.get("op") == "choose"
               and (n.get("then") or {}).get("value") == "flagged-outside-class"]
    assert len(flagged) == 1
    rest = flagged[0]["else"]

    def flag(field: str, value: int) -> dict[str, Any]:
        return cmp("eq", {"op": "parameter", "parameter_id": P + "parameter.f1099b-yes-no-flag",
                          "key": ref(sale, field)}, value)

    agree = [row_agrees(kind, term, "proceeds", "proceeds"), row_agrees(kind, term, "basis", "basis")]
    if kind == "covered-w":
        agree.append(row_agrees(kind, term, "adjustment", "box_1g_wash_sale_disallowed_amount"))
    chain = choose({"op": "not", "value": {"op": "all", "args": agree}}, cat(fact, "v2", "amounts-disagree"), rest)
    if kind == "covered":
        chain = choose(flag("box_1g_wash_sale_adjustment", 1), cat(fact, "v2", "needs-form-8949"), chain)
    chain = choose(flag("long_term", 1 if term == "st" else 0), cat(fact, "v2", "term-mismatch"), chain)
    flagged[0]["else"] = chain
    body["version"] = "v2"
    body["notes"] += (" v2: a sale whose long_term flag names the other term, a line 1a or 8a sale with box 1g "
                      "checked, and a sale whose own proceeds, basis or wash-sale row differs from the sale are "
                      "refused.")
    return successor_name(name, "v2"), body


def admission_check(kind: str, term: str, fixes: set[str]) -> tuple[str, dict[str, Any]]:
    """The return-level check reads the v2 admission and requires each sale's own amount rows.

    The lines (1a, 8a: rule-artifact.v4; 1b, 8b: v5) cannot carry require_paired,
    which only rule-artifact.v15 has; the check they already require can, on
    the path it takes when a sale is recorded.
    """
    name, body = current(f"rule.f1099b.{kind}-{term}-txn.admission-check")
    for node in walk(body):
        if node.get("op") == "category_literal":
            node["fact_type"]["version"] = "v2"
    scalars = ("proceeds", "basis") + (("adjustment",) if kind == "covered-w" else ())
    sales_path = body["selection"]["paths"][0]
    assert sales_path["id"] == "sales" and sales_path["when"] is True
    if "paired_rows" not in fixes:
        body["version"] = "v2"
        body["notes"] += " v2: reads the v2 admission (term, box 1g and amount checks)."
        return successor_name(name, "v2"), body
    sales_path["when"] = {"op": "all", "args": [
        {"op": "require_paired", "key": "transaction", "withholding": P + f"f1099b.{kind}-{term}-txn.{s}",
         "income": [P + f"f1099b.{kind}-{term}-txn"]} for s in scalars]}
    body["version"] = "v2"
    body["notes"] += (" v2: reads the v2 admission (term, box 1g and amount checks), and every sale needs its own "
                      "amount rows (require_paired).")
    return successor_name(name, "v2"), body


LINE_OF = {("covered", "st"): ("rule.schedule-d-line1a-gain", "schedule-d.line-1a"),
           ("covered", "lt"): ("rule.schedule-d-line8a-gain", "schedule-d.line-8a"),
           ("covered-w", "st"): ("rule.schedule-d-line1b", "schedule-d.line-1b"),
           ("covered-w", "lt"): ("rule.schedule-d-line8b", "schedule-d.line-8b")}
NEW_REASONS = (" A sale whose own proceeds, basis or wash-sale row is missing or differs from the sale, a sale that "
               "says it is of the other term, and a line 1a or 8a sale with a wash-sale loss disallowed in box 1g "
               "(record it as a code W sale) are also outside what this return computes.")


def line_words(kind: str, term: str) -> tuple[str, dict[str, Any]]:
    _member, field_id = LINE_OF[(kind, term)]
    fname, field = current(field_id)
    field["version"] = bump(field["version"])
    field["dispositions"]["blocked"]["explain"] += NEW_REASONS
    return successor_name(fname, field["version"]), field


def fix_admission_reads(fixes: set[str]) -> Out:
    out: Out = [admission_bundle()]
    for kind in ADMISSION_KINDS:
        for term in TERMS:
            out += [admission_rule(kind, term), admission_check(kind, term, fixes), line_words(kind, term)]
    return out


# New questions: Form 1099-B boxes the sale records do not carry.
BOX4 = "f1099b.box4-withholding-reported"
BOX7 = "f1099b.box7-loss-not-allowed"
QUESTIONS = {
    BOX4: ("Did any Form 1099-B or substitute statement you received show federal income tax withheld in box 4?",
           "Whether any 2025 Form 1099-B shows federal income tax withheld (backup withholding) in box 4. yes or no."),
    BOX7: ("Is box 7 (\"If checked, loss is not allowed based on amount in 1d\") checked on any Form 1099-B or "
           "substitute statement you received?",
           "Whether box 7 (loss not allowed based on the box 1d amount) is checked on any 2025 Form 1099-B. yes or no."),
}


# statement_box4 / statement_box7: one answer per recorded Form 1099-B statement.
BOX4_STATEMENT = "f1099b.statement-box4-withholding-reported"
BOX7_STATEMENT = "f1099b.statement-box7-loss-not-allowed"
QUESTIONS.update({
    BOX4_STATEMENT: (
        "For each Form 1099-B or substitute statement you recorded a sale from, does it show federal income tax "
        "withheld in box 4?",
        "Whether one recorded 2025 Form 1099-B statement shows federal income tax withheld (backup withholding) in "
        "box 4. yes or no."),
    BOX7_STATEMENT: (
        "For each Form 1099-B or substitute statement you recorded a sale from, is box 7 (\"If checked, loss is not "
        "allowed based on amount in 1d\") checked for any sale on it?",
        "Whether box 7 (loss not allowed based on the box 1d amount) is checked for any sale on one recorded 2025 "
        "Form 1099-B statement. yes or no."),
})
STATEMENT_KEYS = [{"name": "statement", "kind": "entity", "entity_kind": "tax.us.f1099b-statement"},
                  {"name": "tax-year", "kind": "literal", "values": ["2025"]}]
# The Form 1099-B sale objects: every one carries the broker, statement and transaction keys.
SALE_OBJECTS = [f"f1099b.{k}-{t}-txn" for k in ("covered", "covered-w", "noncovered", "code-b") for t in TERMS]


def box_fact(box: int, fixes: set[str]) -> str:
    """The fact the box 4 or box 7 answer is recorded as under ``fixes``."""
    if box == 4:
        return BOX4_STATEMENT if "statement_box4" in fixes else BOX4
    return BOX7_STATEMENT if "statement_box7" in fixes else BOX7


def boxes_bundle(fixes: set[str]) -> tuple[str, dict[str, Any]]:
    facts = []
    for box, fix in ((4, "box4_question"), (7, "box7_question")):
        if fix not in fixes:
            continue
        fact = box_fact(box, fixes)
        per_statement = fact in (BOX4_STATEMENT, BOX7_STATEMENT)
        keys = STATEMENT_KEYS if per_statement else [{"name": "tax-year", "kind": "literal", "values": ["2025"]}]
        facts.append({"schema": "fact-type.v2", "id": P + fact, "version": "v1", "title": QUESTIONS[fact][1],
                      "nature": "determinable", "identity_keys": copy.deepcopy(keys),
                      "value_schema": {"enum": ["yes", "no"]}, "supersession": {"policy": "free"}})
    return "f1099b-statement-boxes.bundle.json", {
        "schema": "bundle.v2", "id": P + "f1099b.statement-boxes.vocabulary", "version": "v1",
        "label": "Form 1099-B boxes the sale records do not carry: box 4 withholding and box 7", "fact_types": facts}


def question(fact: str) -> tuple[str, dict[str, Any]]:
    slug = fact.removeprefix("f1099b.")
    return f"input-question.f1099b-{slug}.json", {
        "schema": "input-question.v1", "id": P + f"input-question.f1099b-{slug}", "version": "v1",
        "fact_type": {"id": P + fact, "version": "v1"}, "question": QUESTIONS[fact][0]}


def statement_block(body: dict[str, Any], fact: str, fixes: set[str]) -> None:
    """Every recorded Form 1099-B sale's statement needs an answer; "yes" on any statement blocks the value.

    require_paired (key ``statement``) is vacuous when no Form 1099-B sale is
    recorded, and blocks DEPENDENCY_ABSENT naming ``fact`` when a sale's
    statement has no answer, so the page asks ``fact``'s question. The answers
    are read (collect_categorical_all_equal) only when a sale is recorded,
    so a return with none needs no answer.
    """
    names = counts(fixes, form_1099b_only=True)
    active = {"op": "any", "args": any_count(names)}
    paired = {"op": "require_paired", "key": "statement", "withholding": P + fact,
              "income": [P + sale for sale in SALE_OBJECTS]}
    when = body["when"]
    body["when"] = {"op": "all", "args": [when, paired]} if when is not True else {"op": "all", "args": [paired]}
    every_no = {"op": "collect_categorical_all_equal", "name": P + fact, "value": cat(fact, "v1", "no")}
    body["value"] = choose({"op": "all", "args": [copy.deepcopy(active), {"op": "not", "value": every_no}]},
                           {"op": "block", "code": "DEPENDENCY_ABSENT"}, body["value"])
    add_requires(body, names)
    body["schema"] = "rule-artifact.v15"


def gated_block(body: dict[str, Any], fact: str, fixes: set[str]) -> None:
    """Read ``fact`` only when a Form 1099-B sale is recorded; "yes" blocks the rule's value."""
    names = counts(fixes, form_1099b_only=True)
    active = {"op": "any", "args": any_count(names)}
    gate = {"op": "conditional_dependency_set", "condition": copy.deepcopy(active), "members": [ref(fact)]}
    when = body["when"]
    body["when"] = {"op": "all", "args": [when, gate]} if when is not True else {"op": "all", "args": [gate]}
    body["value"] = choose({"op": "all", "args": [copy.deepcopy(active), is_yes(fact)]},
                           {"op": "block", "code": "DEPENDENCY_ABSENT"}, body["value"])
    add_requires(body, names)
    body["schema"] = "rule-artifact.v15"


def fix_box_questions(fixes: set[str]) -> Out:
    out: Out = [boxes_bundle(fixes)]
    if "box4_question" in fixes:
        fact = box_fact(4, fixes)
        out.append(question(fact))
        name, body = current("rule.form1040-line25b")
        body["version"] = bump(body["version"])
        if fact == BOX4_STATEMENT:
            statement_block(body, fact, fixes)
            body["notes"] += (" v6: every recorded Form 1099-B sale's statement needs a box 4 answer (require_paired "
                              "on the statement key), so a sale from a statement not yet answered blocks the line and "
                              "asks; a yes on any statement blocks the line, because Form 1099-B box 4 withholding "
                              "is not added yet.")
            words = (" It is also blocked while a recorded Form 1099-B statement has no answer about box 4, and when "
                     "a Form 1099-B shows federal income tax withheld in box 4: this return does not add Form 1099-B "
                     "withholding yet.")
        else:
            gated_block(body, fact, fixes)
            body["notes"] += (" v6: when a Form 1099-B sale is recorded, the box 4 answer is read; yes blocks the "
                              "line, because Form 1099-B box 4 withholding is not added yet.")
            words = (" It is also blocked when a Form 1099-B shows federal income tax withheld in box 4: this return "
                     "does not add Form 1099-B withholding yet.")
        out.append((successor_name(name, body["version"]), body))
        fname, field = current("form1040.line-25b")
        field["version"] = bump(field["version"])
        field["dispositions"]["blocked"]["explain"] += words
        out.append((successor_name(fname, field["version"]), field))
    if "box7_question" in fixes:
        fact = box_fact(7, fixes)
        out.append(question(fact))
        name, body = current("rule.schedule-d-line16")
        body["version"] = bump(body["version"])
        if fact == BOX7_STATEMENT:
            statement_block(body, fact, fixes)
            body["notes"] += (" v3: every recorded Form 1099-B sale's statement needs a box 7 answer (require_paired "
                              "on the statement key), so a sale from a statement not yet answered blocks the line and "
                              "asks; a yes on any statement blocks the line, because a loss based on the box 1d "
                              "amount of a reportable change in control is not allowed and this return does not "
                              "compute it.")
            words = (" It is also blocked while a recorded Form 1099-B statement has no answer about box 7, and when "
                     "box 7 (loss not allowed) is checked on a Form 1099-B: this return does not compute that sale.")
        else:
            gated_block(body, fact, fixes)
            body["notes"] += (" v3: when a Form 1099-B sale is recorded, the box 7 answer is read; yes blocks the "
                              "line, because a loss based on the box 1d amount of a reportable change in control is "
                              "not allowed and this return does not compute it.")
            words = (" It is also blocked when box 7 (loss not allowed) is checked on a Form 1099-B: this return does "
                     "not compute that sale.")
        out.append((successor_name(name, body["version"]), body))
        fname, field = current("schedule-d.line-16")
        field["version"] = bump(field["version"])
        field["dispositions"]["blocked"]["explain"] += words
        out.append((successor_name(fname, field["version"]), field))
    return out


FIELD_WORDS = {
    "form1040.line-16": ("tax_activity", " It also waits for your answers about each kind of sale, because whether "
                         "you recorded any sale decides whether your tax is figured with Schedule D."),
    "form1040.line-7a": ("base_activity", " It also waits for your answers about each kind of sale and for Schedule "
                         "D, because any recorded sale puts line 7a on the Schedule D route."),
}


def fix_field_words(fixes: set[str]) -> Out:
    out: Out = []
    for field_id, (needs, words) in FIELD_WORDS.items():
        if needs not in fixes:
            continue
        fname, field = current(field_id)
        field["version"] = bump(field["version"])
        field["dispositions"]["blocked"]["explain"] += words
        out.append((successor_name(fname, field["version"]), field))
    return out


BUILDERS: dict[str, Callable[[set[str]], Out]] = {
    "tax_activity": fix_tax_activity, "no1099b_count": fix_no1099b_count, "base_activity": fix_base_activity,
    "admission_reads": fix_admission_reads,
}


def artifacts(fixes: set[str]) -> Out:
    out: Out = []
    for fix in FIXES:
        if fix in BUILDERS and fix in fixes:
            out += BUILDERS[fix](fixes)
    if fixes & {"box4_question", "box7_question"}:
        out += fix_box_questions(fixes)
    if "field_words" in fixes:
        out += fix_field_words(fixes)
    names = [n for n, _ in out]
    assert len(names) == len(set(names)), names
    return out


# ---- build ----------------------------------------------------------------------------


def role(body: dict[str, Any]) -> str:
    schema = str(body["schema"])
    if schema.startswith("rule-artifact"):
        return "computation"
    if schema.startswith("attachment-rule"):
        return "attachment-rule"
    return ROLE[schema]


def build(scratch: Path, fixes: set[str]) -> dict[str, Any]:
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(CONTENT, content)
    shutil.copytree(RELEASES, releases)
    for name in (f"package.core-calculations.{TO['package']}.json", f"published-packages.{TO['registry']}.json"):
        assert not (content / name).exists(), name
    assert not (releases / f"{RELEASE_STEM}.{TO['release']}.json").exists()
    members, entrypoints = [], []
    entry_keys = {(e["id"], e["version"]) for e in PACKAGE["entrypoints"]}
    for name, body in artifacts(fixes):
        if (content / name).exists():
            raise AssertionError(f"{name} already exists")
        (content / name).write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role(body)}
        old = MEMBERS.get(body["id"])
        if old is not None:
            members.append({"op": "replace", "old": dict(old), "new": new})
            if (old["id"], old["version"]) in entry_keys:
                entrypoints.append({"op": "replace", "old": {"id": old["id"], "version": old["version"]},
                                    "new": {"id": body["id"], "version": body["version"]}})
        else:
            members.append({"op": "add", "new": new})
            entrypoints.append({"op": "add", "value": {"id": body["id"], "version": body["version"]}})
    changes = {"package_version": TO["package"], "release_version": TO["release"], "members": members,
               "entrypoints": entrypoints, "registry_sort": "id_version",
               "registry_new_key_order": ["checksum", "id", "version"]}
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / f"package.core-calculations.{FROM['package']}.json",
        content / f"published-packages.{FROM['registry']}.json",
        releases / f"{RELEASE_STEM}.{FROM['release']}.json",
        content, scratch / "changes.json", scratch / "out")
    for src, folder, target in (
        ("package.json", content, f"package.core-calculations.{TO['package']}.json"),
        ("registry.json", content, f"published-packages.{TO['registry']}.json"),
        ("release.json", releases, f"{RELEASE_STEM}.{TO['release']}.json"),
    ):
        shutil.copy(scratch / "out" / src, folder / target)
    return {
        "fixes": [f for f in FIXES if f in fixes], "repairs": [r for r in REPAIRS if r in fixes], "package": report["package"]["version"],
        "registry": TO["registry"], "release": report["release"]["version"],
        "members_edited": len(members), "added": sum(1 for m in members if m["op"] == "add"),
        "replaced": sum(1 for m in members if m["op"] == "replace"),
        "members": [[m["op"], m["new"]["id"].removeprefix(P), m["new"]["version"]] for m in members],
        "inherited_inconsistencies": [list(r) for r in report.get("inherited_inconsistencies") or ()],
    }


def main() -> None:
    scratch = Path(sys.argv[1]).resolve()
    named = sys.argv[2:]
    fixes = set(FIXES) if named == ["decided"] else (set(named) or set(SWITCHES))
    unknown = fixes - set(SWITCHES)
    assert not unknown, unknown
    assert not ({"statement_box4"} & fixes) or "box4_question" in fixes
    assert not ({"statement_box7"} & fixes) or "box7_question" in fixes
    if REPO in scratch.parents or scratch == REPO:
        raise SystemExit("the scratch directory must be outside the repository")
    summary = build(scratch, fixes)
    (HERE / "prototype-build.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8")
    core = {"version": TO["package"], "registry": TO["registry"], "release_version": TO["release"],
            "content": str(scratch / "content"), "releases": str(scratch / "releases"), "loader_from": FROM["package"]}
    (scratch / "core.json").write_text(json.dumps(core) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("core:", json.dumps(core))


if __name__ == "__main__":
    main()
