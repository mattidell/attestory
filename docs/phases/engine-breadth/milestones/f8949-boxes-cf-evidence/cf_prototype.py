"""Scratch core v80: sales of securities with no Form 1099-B (boxes C and F).

P0 prototype for docs/phases/engine-breadth/milestones/f8949-boxes-cf.md.
Copies the production content and release directories to a temporary
directory, writes the successor set there, generates package v80 / registry
v78 / release v78 from v79 with tools.package_successor, and runs each case
through live_coordinate_run. Nothing under packages/ is written. The only
in-process patch is the per-package companion declaration and covered-flag
refusal map in packages/tax/loader.py, which Track 1 would add as two
entries for v80.

    python3 docs/phases/engine-breadth/milestones/f8949-boxes-cf-evidence/cf_prototype.py [case ...]

Writes cf-prototype-output.json beside this file, and the small JSON of each
new or successor member under cf-prototype-rules/.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cf_probe as cp  # noqa: E402

from packages.kernel.facts import fact_id_for  # noqa: E402
from packages.tax import loader  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _attested  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

P = cp.P
probe, p0b = cp.probe, cp.p0b
OUT = HERE / "cf-prototype-output.json"
RULES = HERE / "cf-prototype-rules"
PKG = P + "package.core-calculations"

OLD_IC = P + "schedule-d-boundary.noncovered-in-class"
NEW_IC = P + "schedule-d-boundary.form8949-in-class"
NO8949 = P + "schedule-d-boundary.no-form8949-sources"
PATH_B = P + "schedule-d-boundary.no-other-form8949-adjustments"
Q1 = P + "f1099b.noncovered-sold.source-closure"
Q2 = P + "f8949.no1099b-sold.source-closure"
# Track 0 repairs (track0-closure.md). All are on by default; track0.py turns
# them off to show the counterexample each one fixes.
#   q1_unbacked_yes: lines 3 and 10 are zero only if the v79 noncovered answer
#     is "no" or a box B/E sale is recorded, so a v79 "yes" with nothing behind
#     it blocks (check 2 for the v79 question). Lines 2 and 9 keep the v79 zero
#     path, so their closure-backed zero sentence is unchanged.
#   old_ic_backed: the v79 in-class "yes" admits a Form 8949 "no" on lines 3
#     and 10 only beside a v79 "yes".
#   sale_needs_8949_no: lines 2, 3, 9 and 10 publish a recorded sale only
#     beside a Form 8949 "no". A Form 8949 "yes" says there are no Form 8949
#     transactions; with a sale recorded it published Form 1040 while the Form
#     8949 attachment blocked.
#   f8949_reads_lines_2_9: the Form 8949 attachment requirement reads lines 2
#     and 9, so a box B/E sale missing an amount blocks the attachment too.
#   nc_count_pairing: lines 2 and 9 also need as many proceeds rows and basis
#     rows as sale objects. require_paired reads one key, and a box B/E sale is
#     keyed by broker, statement and transaction; two sales on different
#     statements can share a transaction entity. The ADR-0082 presence pairs
#     refuse a scalar without its own sale object, so equal counts mean every
#     sale has its own rows.
#   amounts_agree: each sale's own proceeds, basis and wash-sale rows must
#     equal the amounts on its sale object, whose member constraints (code W
#     on a gain, adjustment above the loss, holding period) are the only
#     checks. A per-sale rule (the sale object is the subject) publishes agree
#     or disagree, and a return-level selection rule publishes 0 only when
#     every sale agrees. Lines 2, 3, 9 and 10 require it. Same shape as the
#     Form 1099-K statement-loss-reason / unresolved pair.
REPAIRS: set[str] = {"q1_unbacked_yes", "old_ic_backed", "sale_needs_8949_no", "f8949_reads_lines_2_9",
                     "nc_count_pairing", "amounts_agree"}
Q2_TEXT = "Did you sell any stocks or other securities for which you did not receive a Form 1099-B or substitute statement?"
SALE_KIND = "tax.us.f8949-sale"
TERMS = ("st", "lt")
KINDS = ("proceeds", "basis", "adjustment")
WORD = {"st": "short-term", "lt": "long-term"}
BOX = {"st": "C", "lt": "F"}
LINE = {"st": "3", "lt": "10"}
NC_LINE = {"st": "2", "lt": "9"}


# ---- small JSON helpers --------------------------------------------------


def read(name: str) -> dict[str, Any]:
    return json.loads((cp.probe.CONTENT / name).read_text(encoding="utf-8"))


def ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def eq0(name: str) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": ref(name), "right": 0}


def ne0(name: str) -> dict[str, Any]:
    return {"op": "compare", "cmp": "ne", "left": ref(name), "right": 0}


def cat(fact: str, value: str) -> dict[str, Any]:
    return {
        "op": "categorical_compare", "cmp": "eq", "left": ref(fact),
        "right": {"op": "category_literal", "fact_type": {"id": fact, "version": "v1"}, "value": value},
    }


def guarded() -> dict[str, Any]:
    return {"op": "all", "args": [cat(Q2, "yes"), cat(NEW_IC, "yes")]}


def is_cat(node: Any, fact: str) -> bool:
    return (isinstance(node, dict) and node.get("op") == "categorical_compare"
            and (node.get("left") or {}).get("name") == fact)


def mentions(node: Any, symbol: str) -> bool:
    if isinstance(node, dict):
        return any(mentions(v, symbol) for v in node.values())
    if isinstance(node, list):
        return any(mentions(v, symbol) for v in node)
    return node == symbol


def swap(node: Any, old: str, new: str) -> Any:
    if isinstance(node, dict):
        return {k: swap(v, old, new) for k, v in node.items()}
    if isinstance(node, list):
        return [swap(v, old, new) for v in node]
    return new if node == old else node


def widen(node: Any, pairs: list[tuple[str, str]], arm: bool) -> Any:
    """The successor edit, applied the same way everywhere.

    In a list of strings (requires, missing) and in an expression ``args``
    list, every entry that names ``old`` gets a sibling naming ``new`` right
    after it. With ``arm``, every ``any`` arm testing the v79 in-class answer
    gets a sibling placed before it: ``all(no-1099-B answer is yes, new
    in-class answer is yes)``. ``any`` stops at the first true arm and blocks
    at the first missing answer, so a v79 return (which answers the new
    question no) falls through to its own in-class answer, and a box C/F
    filer never needs the v79 in-class answer.
    """
    if isinstance(node, dict):
        out = {k: widen(v, pairs, arm) for k, v in node.items()}
        return out
    if isinstance(node, list):
        result: list[Any] = []
        for item in node:
            item = widen(item, pairs, arm)
            if arm and is_cat(item, OLD_IC):
                result.append(copy.deepcopy(GUARDED))
            result.append(item)
            for old, new in pairs:
                if item == old or (isinstance(item, dict) and mentions(item, old) and not mentions(item, new)
                                   and item.get("op") in {"ref", "compare"}):
                    result.append(swap(item, old, new))
        return result
    return node


GUARDED = guarded()


# ---- new content ---------------------------------------------------------


def fam(term: str, kind: str | None) -> str:
    return P + f"f8949.no1099b-{term}" + (f"-{kind}" if kind else "")


def member_fact(term: str, kind: str | None) -> str:
    return P + f"f8949.no1099b-{term}-txn" + (f".{kind}" if kind else "")


def subtotal(term: str, kind: str) -> str:
    return P + f"f8949.no1099b-{term}-{kind}-subtotal"


SALE_KEYS = [
    {"name": "sale", "kind": "entity", "entity_kind": SALE_KIND},
    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
]
CLOSURE_KEYS = [
    {"name": "family-horizon", "kind": "entity", "entity_kind": "kernel.family-horizon"},
    {"name": "tax-year", "kind": "literal", "values": ["2025"]},
]


def fact(fact_id: str, title: str, value_schema: dict[str, Any], keys: list[dict[str, Any]]) -> dict[str, Any]:
    return {"schema": "fact-type.v2", "id": fact_id, "version": "v1", "title": title, "nature": "determinable",
            "identity_keys": copy.deepcopy(keys), "value_schema": value_schema, "supersession": {"policy": "free"}}


def bundle(term: str) -> dict[str, Any]:
    w = WORD[term]
    sale = {
        "type": "object", "additionalProperties": False,
        "required": ["proceeds", "basis", "long_term", "wash_disallowed"],
        "properties": {
            "proceeds": {"type": "number", "minimum": 0},
            "basis": {"type": "number", "minimum": 0},
            "long_term": {"enum": ["yes", "no"]},
            "wash_disallowed": {"type": "number", "minimum": 0},
        },
    }
    facts = [fact(member_fact(term, None),
                  f"One {w} sale of securities you received no Form 1099-B or substitute statement for. "
                  "You supply the net proceeds and the basis.", sale, SALE_KEYS),
             fact(fam(term, None) + ".source-closure", f"Closure of the {w} no-Form-1099-B sale family.",
                  {"type": "boolean"}, CLOSURE_KEYS)]
    words = {"proceeds": "net proceeds (gross proceeds minus selling expenses)", "basis": "basis",
             "adjustment": "wash-sale adjustment"}
    for kind in KINDS:
        facts.append(fact(member_fact(term, kind),
                          f"The {words[kind]} of a {w} sale you received no Form 1099-B for.",
                          {"type": "number", "minimum": 0}, SALE_KEYS))
        facts.append(fact(fam(term, kind) + ".source-closure",
                          f"Closure of the {w} no-Form-1099-B {kind} family.", {"type": "boolean"}, CLOSURE_KEYS))
    if "amounts_agree" in REPAIRS:
        facts += agree_facts(member_fact(term, None), SALE_KEYS, f"{w} sale you received no Form 1099-B for")
    return {"schema": "bundle.v2", "id": P + f"f8949.no1099b-{term}.vocabulary", "version": "v1",
            "label": f"Vocabulary for {w} sales of securities with no Form 1099-B", "fact_types": facts}


# ---- Track 0 repair amounts_agree ------------------------------------------


def agree_fact(sale_fact: str) -> str:
    return sale_fact + ".amounts-agree"


def check_symbol(sale_fact: str) -> str:
    return sale_fact + ".amounts-check"


def inert_fact(sale_fact: str) -> str:
    return sale_fact + ".amounts-check-inert-path-unwritten"


def agree_facts(sale_fact: str, keys: list[dict[str, Any]], what: str) -> list[dict[str, Any]]:
    domain = {"oneOf": [
        {"const": "agree", "description": "The sale's own proceeds, basis and wash-sale rows equal the amounts on the sale."},
        {"const": "disagree", "description": "A proceeds, basis or wash-sale row differs from the amount on the sale."},
    ]}
    return [fact(agree_fact(sale_fact), f"Whether each amount row of one {what} equals the amount on the sale.",
                 domain, keys),
            fact(inert_fact(sale_fact), "Never recorded; the second selection path the selection shape requires.",
                 {"type": "boolean"}, [{"name": "tax-year", "kind": "literal", "values": ["2025"]}])]


def nc_keys() -> list[dict[str, Any]]:
    return copy.deepcopy(BUILT_NC_KEYS)


BUILT_NC_KEYS: list[dict[str, Any]] = []


def nc_check_bundle() -> dict[str, Any]:
    if not BUILT_NC_KEYS:
        BUILT_NC_KEYS.extend(read("f1099b-noncovered-st.bundle.json")["fact_types"][0]["identity_keys"])
    facts: list[dict[str, Any]] = []
    for term in TERMS:
        facts += agree_facts(P + f"f1099b.noncovered-{term}-txn", nc_keys(),
                             f"{WORD[term]} sale whose basis was not reported to the IRS")
    return {"schema": "bundle.v2", "id": P + "f1099b.noncovered-amounts-check.vocabulary", "version": "v1",
            "label": "Whether each sale whose basis was not reported has amount rows equal to the sale", "fact_types": facts}


def agree_rule(sale_fact: str, family_stem: str) -> dict[str, Any]:
    """Per sale: the amount rows equal the sale object's own amounts."""
    proceeds, basis, adj = (sale_fact + "." + k for k in KINDS)
    subject = {"op": "ref", "name": sale_fact}
    field = lambda f: {**subject, "field": f}  # noqa: E731
    eq = lambda left, right: {"op": "compare", "cmp": "eq", "left": left, "right": right}  # noqa: E731
    rows = lambda name, kind: {"op": "count", "name": name, "source_set": family_stem + "-" + kind}  # noqa: E731
    present = lambda name, kind: {"op": "all", "args": [  # noqa: E731
        {"op": "compare", "cmp": "gt", "left": rows(name, kind), "right": 0},
        {"op": "conditional_dependency_set", "condition": True, "members": [ref(name)]}]}

    def amount_ok(name: str, kind: str) -> dict[str, Any]:
        # A missing row is not compared here: the line's require_paired asks for it.
        return {"op": "any", "args": [eq(rows(name, kind), 0),
                                      {"op": "all", "args": [present(name, kind), eq(ref(name), field(kind))]}]}

    wash_ok = {"op": "any", "args": [
        {"op": "all", "args": [eq(rows(adj, "adjustment"), 0), eq(field("wash_disallowed"), 0)]},
        {"op": "all", "args": [present(adj, "adjustment"), eq(ref(adj), field("wash_disallowed"))]},
    ]}
    lit = lambda v: {"op": "category_literal", "fact_type": {"id": agree_fact(sale_fact), "version": "v1"}, "value": v}  # noqa: E731
    return {
        "schema": "rule-artifact.v15", "id": sale_fact.replace(P, P + "rule.") + ".amounts-agree", "version": "v1",
        "scope": read("rule.schedule-d-line2.json")["scope"], "role": "computation",
        "subject": {"id": sale_fact, "version": "v1"},
        "requires": [sale_fact], "pins": [], "when": True,
        "value": {"op": "choose", "when": {"op": "all", "args": [
            amount_ok(proceeds, "proceeds"), amount_ok(basis, "basis"), wash_ok]},
            "then": lit("agree"), "else": lit("disagree")},
        "publishes": agree_fact(sale_fact), "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}, "citations": [],
        "notes": "Track 0: the line reads the amount rows; the member constraints read the sale. They must agree.",
    }


def check_rule(sale_fact: str, family_id: str) -> dict[str, Any]:
    """Return level: 0 when every sale agrees or none is recorded; else block."""
    agree = {"op": "category_literal", "fact_type": {"id": agree_fact(sale_fact), "version": "v1"}, "value": "agree"}
    path = lambda pid, activity, reads, value: {"id": pid, "activity": activity, "reads_subject_results": reads,  # noqa: E731
                                                 "requires": [], "pins": [], "when": True, "value": value}
    return {
        "schema": "rule-artifact.v15", "id": sale_fact.replace(P, P + "rule.") + ".amounts-check", "version": "v1",
        "scope": read("rule.schedule-d-line2.json")["scope"], "role": "computation", "requires": [], "pins": [],
        "when": True,
        "selection": {"mode": "exclusive_presence", "conflict": "refuse", "paths": [
            path("sales", {"kind": "source_nonempty", "source_family": {"id": family_id, "version": "v1"},
                           "member_fact_types": [{"id": sale_fact, "version": "v1"}]},
                 [{"symbol": agree_fact(sale_fact), "subject": {"id": sale_fact, "version": "v1"}}],
                 {"op": "choose", "when": {"op": "collect_categorical_all_equal", "name": agree_fact(sale_fact),
                                           "value": agree},
                  "then": 0, "else": {"op": "block", "code": "DEPENDENCY_INVALID"}}),
            path("inert", {"kind": "source_nonempty", "member_fact_types": [{"id": inert_fact(sale_fact), "version": "v1"}]},
                 [], {"op": "block", "code": "DEPENDENCY_ABSENT"}),
        ], "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [], "when": True, "value": 0},
            "refusal": {"code": "DEPENDENCY_INVALID", "missing": [sale_fact.removeprefix(P) + "-amounts-check-conflict"],
                        "pins": []}},
        "publishes": check_symbol(sale_fact), "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}, "citations": [],
        "notes": "Track 0: blocks unless every recorded sale's amount rows equal the sale's own amounts.",
    }


def agreement_members() -> list[tuple[str, dict[str, Any]]]:
    out: list[tuple[str, dict[str, Any]]] = [("f1099b-noncovered-amounts-check.bundle.json", nc_check_bundle())]
    for term in TERMS:
        for sale, family_id, stem in ((member_fact(term, None), fam(term, None), fam(term, None)),
                                      (nc_fact(term, None), P + f"f1099b.noncovered-{term}", P + f"f1099b.noncovered-{term}")):
            slug = sale.removeprefix(P)
            out.append((f"rule.{slug}.amounts-agree.json", agree_rule(sale, stem)))
            out.append((f"rule.{slug}.amounts-check.json", check_rule(sale, family_id)))
    return out


def boundary_bundle() -> dict[str, Any]:
    yes_no = {"enum": ["yes", "no"]}
    year = [{"name": "tax-year", "kind": "literal", "values": ["2025"]}]
    return {
        "schema": "bundle.v2", "id": P + "schedule-d-boundary.form8949-in-class.vocabulary", "version": "v1",
        "label": "Whether Form 8949 work beyond covered sales and code W is only boxes B, C, E and F",
        "fact_types": [
            fact(NEW_IC, "Whether this return's Form 8949 work beyond covered sales and code W is only boxes B, C, "
                 "E and F: sales of stocks or other securities with a basis you supply (and, on boxes C and F, net "
                 "proceeds you supply) and an optional wash-sale adjustment. yes or no.", yes_no, year),
            fact(Q2, Q2_TEXT, yes_no, year),
        ],
    }


def family(term: str, kind: str | None) -> dict[str, Any]:
    source = read(f"family.f1099b-noncovered-{term}" + (f"-{kind}" if kind else "") + ".json")
    w = WORD[term]
    body: dict[str, Any] = {
        "schema": "source-family.v2", "id": fam(term, kind), "version": "v1",
        "title": f"{w} sales of securities with no Form 1099-B" + (f", {kind}" if kind else "") + ", tax year 2025",
        "scope": source["scope"],
        "closure_claim": f"Every {w} sale of securities you received no Form 1099-B for is recorded"
                         + (f" with its {kind}" if kind else "") + " as of the keyed horizon.",
        "member_predicate": {"fact_type": member_fact(term, kind)},
        "authorizes_subtotal": (subtotal(term, kind) if kind else P + f"f8949.no1099b-{term}-subtotal"),
    }
    if kind is None:
        constraints = []
        for row in source["member_constraints"]:
            if row["block_code"] == "BASIS_WAS_REPORTED":
                continue  # no statement, so nothing reported
            row = copy.deepcopy(row)
            row["id"] = row["id"].replace("constraint.noncovered-", "constraint.no1099b-")
            constraints.append(row)
        body["member_constraints"] = constraints
    return body


def mapping() -> dict[str, Any]:
    rows = []
    for term in TERMS:
        for kind in (None, *KINDS):
            rows.append({"family": {"id": fam(term, kind), "version": "v1"},
                         "member_fact_type": {"id": member_fact(term, kind), "version": "v1"},
                         "admits_symbol": subtotal(term, kind) if kind else P + f"f8949.no1099b-{term}-subtotal"})
    return {"schema": "source-closure-mapping.v4", "id": P + "closure-mapping.f8949.no1099b", "version": "v1",
            "closure_fact_type": {"id": Q2, "version": "v1"}, "closure_question": Q2_TEXT,
            "admission": {"no": "closed-empty", "yes": "until-later-member"}, "families": rows}


def question() -> dict[str, Any]:
    return {"schema": "input-question.v1", "id": P + "input-question.f8949-no1099b-sold", "version": "v1",
            "fact_type": {"id": Q2, "version": "v1"}, "question": Q2_TEXT}


NEW_IC_TEXT = ("Apart from sales your broker reported with their basis, is every sale on your Form 8949 a sale of stocks "
               "or other securities, with a basis you supply, net proceeds you supply when you got no Form 1099-B, "
               "and no adjustment other than a wash-sale loss?")


def amount_questions() -> list[tuple[str, dict[str, Any]]]:
    """What the page asks when a recorded sale lacks its own proceeds or basis row (require_paired)."""
    out = [("input-question.schedule-d-boundary-form8949-in-class.json",
            {"schema": "input-question.v1", "id": P + "input-question.schedule-d-boundary-form8949-in-class",
             "version": "v1", "fact_type": {"id": NEW_IC, "version": "v1"}, "question": NEW_IC_TEXT})]
    words = {"proceeds": "net proceeds", "basis": "basis"}
    for term in TERMS:
        for kind in ("proceeds", "basis"):
            out.append((f"input-question.f8949-no1099b-{term}-{kind}.json", {
                "schema": "input-question.v1", "id": P + f"input-question.f8949-no1099b-{term}-{kind}",
                "version": "v1", "fact_type": {"id": member_fact(term, kind), "version": "v1"},
                "question": f"What are the {words[kind]} of each {WORD[term]} sale you recorded without a Form 1099-B?"
                if kind == "proceeds" else
                f"What is the basis of each {WORD[term]} sale you recorded without a Form 1099-B?"}))
    return out


def renamed(term: str, kind: str) -> dict[str, Any]:
    """The v79 box B/E subtotal rule with the box C/F names and the new in-class answer."""
    body = read(f"rule.f1099b-noncovered-{term}-{kind}-subtotal.json")
    body = swap(body, P + f"f1099b.noncovered-{term}-txn.{kind}", member_fact(term, kind))
    body = swap(body, P + f"f1099b.noncovered-{term}-{kind}", fam(term, kind))
    body = swap(body, P + f"f1099b.noncovered-{term}", fam(term, None))
    body = swap(body, P + f"f1099b.noncovered-{term}-{kind}-subtotal", subtotal(term, kind))
    body = swap(body, OLD_IC, NEW_IC)
    body["id"] = P + f"rule.f8949-no1099b-{term}-{kind}-subtotal"
    body["publishes"] = subtotal(term, kind)
    body["notes"] = ("Sums one no-Form-1099-B scalar family. A closed empty family publishes 0 and does not read the "
                     "boundary. A recorded amount publishes only when the form8949-in-class answer is yes.")
    assert "noncovered" not in json.dumps(body), body["id"]
    return body


def line_rule(term: str) -> dict[str, Any]:
    """Schedule D line 3 or 10. rule-artifact.v15 for require_paired.

    when: the four families are closed, and every recorded sale has its own
    proceeds and its own basis row (require_paired on the sale key).
    value: zero when the three subtotals are zero and (a) some Form 8949
    answer admits the return, and (b) the no-1099-B answer is no or the other
    term has a sale; otherwise proceeds minus basis plus adjustment when the
    new in-class answer is yes and a sale of this term is recorded; else block.
    """
    other = "lt" if term == "st" else "st"
    p, b, a = (subtotal(term, k) for k in KINDS)
    sale = member_fact(term, None)
    old_arm = (cat(OLD_IC, "yes") if "old_ic_backed" not in REPAIRS
               else {"op": "all", "args": [cat(Q1, "yes"), cat(OLD_IC, "yes")]})
    admitted = {"op": "any", "args": [cat(NO8949, "yes"), cat(PATH_B, "yes"), GUARDED, old_arm]}
    answered = {"op": "any", "args": [cat(Q2, "no"), ne0(subtotal(other, "proceeds")), ne0(subtotal(other, "basis"))]}
    nc_subs = [P + f"f1099b.noncovered-{t}-{k}-subtotal" for t in TERMS for k in ("proceeds", "basis")]
    zero_args = [eq0(p), eq0(b), eq0(a), admitted, answered]
    if "q1_unbacked_yes" in REPAIRS:
        zero_args.append({"op": "any", "args": [cat(Q1, "no"), *(ne0(n) for n in nc_subs)]})
    zero = {"op": "all", "args": zero_args}
    present_args = [cat(NEW_IC, "yes"), {"op": "any", "args": [ne0(p), ne0(b)]}]
    if "sale_needs_8949_no" in REPAIRS:
        present_args.insert(0, cat(NO8949, "no"))
    present = {"op": "all", "args": present_args}
    when = {"op": "all", "args": [
        *({"op": "require_closed", "source_set": fam(term, kind)} for kind in (None, *KINDS)),
        {"op": "require_paired", "key": "sale", "withholding": member_fact(term, "proceeds"), "income": [sale]},
        {"op": "require_paired", "key": "sale", "withholding": member_fact(term, "basis"), "income": [sale]},
    ]}
    return {
        "schema": "rule-artifact.v15", "id": P + f"rule.schedule-d-line{LINE[term]}", "version": "v1",
        "notes": (f"Schedule D line {LINE[term]}, column (h): Form 8949 box {BOX[term]} proceeds minus basis plus "
                  "the wash-sale adjustment. Every recorded sale needs its own proceeds and basis rows. A closed "
                  "empty set is zero only when a Form 8949 answer admits the return and the no-Form-1099-B answer "
                  "is not an unbacked yes."),
        "role": "computation", "scope": read("rule.schedule-d-line2.json")["scope"],
        "publishes": P + f"schedule-d.line-{LINE[term]}",
        "requires": [p, b, a, subtotal(other, "proceeds"), subtotal(other, "basis"),
                     *(nc_subs if "q1_unbacked_yes" in REPAIRS else []),
                     *([check_symbol(sale)] if "amounts_agree" in REPAIRS else [])],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [p, b, a]},
        "citations": [{"id": P + f"citation.schedule-d.line-{LINE[term]}", "version": "v1"}],
        "pins": [], "when": when,
        "value": {"op": "choose", "when": {"op": "any", "args": [zero, present]},
                  "then": {"op": "add", "args": [{"op": "subtract", "left": ref(p), "right": ref(b)}, ref(a)]},
                  "else": {"op": "block", "code": "DEPENDENCY_ABSENT"}},
    }


def form_field(term: str) -> dict[str, Any]:
    body = read(f"schedule-d.line-{NC_LINE[term]}.form-field.json")
    n, w, box = LINE[term], WORD[term], BOX[term]
    body = swap(body, P + f"schedule-d.line-{NC_LINE[term]}", P + f"schedule-d.line-{n}")
    body = swap(body, P + f"citation.schedule-d.line-{NC_LINE[term]}", P + f"citation.schedule-d.line-{n}")
    body["line"] = f"{n}-h"
    body["label"] = f"Line {n} column (h)"
    body["description"] = f"Schedule D (2025) line {n} column (h)."
    d = body["dispositions"]
    d["published_value"]["explain"] = (f"Schedule D line {n}, column (h), is your {w} Form 8949 box {box} gain or "
                                       "loss, proceeds minus basis plus adjustments.")
    d["computed_zero"]["explain"] = (f"Schedule D line {n}, column (h), is zero. Either no {w} sale you received "
                                     "no Form 1099-B for is recorded and your Form 8949 answers confirm it, or your "
                                     f"box {box} proceeds, basis, and adjustments net to zero.")
    d["closure_backed_zero"]["explain"] = (f"Schedule D line {n}, column (h), is zero. No {w} sale you received no "
                                           "Form 1099-B for is recorded, and your answer about those sales confirms "
                                           "the list is complete.")
    d["blocked"]["explain"] = (f"Schedule D line {n}, column (h), has no value yet. It waits for your answers about "
                               "sales you received no Form 1099-B for, sales whose basis was not reported, and Form "
                               "8949 to agree with the sales you recorded, or for each recorded "
                               f"{w} sale of that kind to have its proceeds and basis and pass its checks.")
    return body


def citation(term: str) -> dict[str, Any]:
    body = read("citation.schedule-d.line-2.json")
    body["id"] = P + f"citation.schedule-d.line-{LINE[term]}"
    return body


# ---- successors of v79 members --------------------------------------------


def successor(name: str, version: str, *, pairs: list[tuple[str, str]], arm: bool, notes: str) -> dict[str, Any]:
    body = widen(read(name), pairs, arm)
    body["version"] = version
    if "notes" in body:
        body["notes"] = body["notes"] + " " + notes
    return body


def nc_fact(term: str, kind: str | None) -> str:
    return P + f"f1099b.noncovered-{term}-txn" + (f".{kind}" if kind else "")


def paired_nc_line(body: dict[str, Any], term: str) -> dict[str, Any]:
    """Decision 3: lines 2 and 9 take the missing-amount check lines 3 and 10 carry.

    rule-artifact.v15 for require_paired. The v79 sale is keyed by broker,
    statement and transaction; the pairing key is the transaction entity.
    v15 has no ``accounts_for`` and gets no synthesized member-validation
    edge (package_validation compiles that edge for v1-v11 only), so the
    family's checks reach the line only through the v5 subtotals it requires.
    Track 0 builds a case for that (``b_code_w_on_gain``).
    """
    body = copy.deepcopy(body)
    body["schema"] = "rule-artifact.v15"
    body.pop("accounts_for", None)
    body["when"]["args"] += [
        {"op": "require_paired", "key": "transaction", "withholding": nc_fact(term, kind), "income": [nc_fact(term, None)]}
        for kind in ("proceeds", "basis")
    ]
    body["notes"] += " v2 (Decision 3): every recorded sale needs its own proceeds and basis rows (require_paired)."
    if "sale_needs_8949_no" in REPAIRS:
        zero, *admit = body["value"]["when"]["args"]
        present = {"op": "all", "args": [cat(NO8949, "no"), {"op": "any", "args": admit}]}
        body["value"]["when"]["args"] = [zero, present]
        body["notes"] += (" A recorded sale publishes only beside a Form 8949 no: a sale is a Form 8949 transaction "
                          "(Track 0).")
    if "amounts_agree" in REPAIRS:
        body["requires"].append(check_symbol(nc_fact(term, None)))
    if "nc_count_pairing" in REPAIRS:
        def count(kind: str | None) -> dict[str, Any]:
            return {"op": "count", "name": nc_fact(term, kind),
                    "source_set": P + f"f1099b.noncovered-{term}" + (f"-{kind}" if kind else "")}
        same = [{"op": "compare", "cmp": "eq", "left": count(None), "right": count(kind)} for kind in ("proceeds", "basis")]
        body["value"] = {"op": "choose", "when": {"op": "all", "args": same}, "then": body["value"],
                         "else": {"op": "block", "code": "DEPENDENCY_ABSENT"}}
        body["notes"] += (" As many proceeds and basis rows as sales: the pairing key is one of three identity keys "
                          "(Track 0).")
    return body


def nc_amount_questions() -> list[tuple[str, dict[str, Any]]]:
    """What the page asks when a box B or E sale lacks its own proceeds or basis row."""
    out = []
    for term in TERMS:
        for kind in ("proceeds", "basis"):
            text = (f"What are the proceeds of each {WORD[term]} sale you recorded whose basis was not reported to the IRS?"
                    if kind == "proceeds" else
                    f"What is the basis of each {WORD[term]} sale you recorded whose basis was not reported to the IRS?")
            out.append((f"input-question.f1099b-noncovered-{term}-{kind}.json", {
                "schema": "input-question.v1", "id": P + f"input-question.f1099b-noncovered-{term}-{kind}",
                "version": "v1", "fact_type": {"id": nc_fact(term, kind), "version": "v1"}, "question": text}))
    return out


LINE_PAIRS = [(P + "schedule-d.line-2", P + "schedule-d.line-3"), (P + "schedule-d.line-9", P + "schedule-d.line-10")]


def attachment_f8949() -> dict[str, Any]:
    body = read("attachment.f8949.v3.json")
    body["version"] = "v4"
    parts = list(body["itemizations"])
    for part in body["itemizations"]:
        pid = part["part_id"]
        if not (pid.startswith("box-b-") or pid.startswith("box-e-")):
            continue
        term = "st" if pid.startswith("box-b-") else "lt"
        kind = pid.split("-")[-1]
        clone = swap(copy.deepcopy(part), P + f"f1099b.noncovered-{term}-{kind}", fam(term, kind))
        clone = swap(clone, P + f"f1099b.noncovered-{term}-txn.{kind}", member_fact(term, kind))
        clone = swap(clone, P + f"f1099b.noncovered-{term}-{kind}-subtotal", subtotal(term, kind))
        clone["part_id"] = f"box-{BOX[term].lower()}-{kind}"
        letter = BOX[term]
        label = {"proceeds": "net proceeds", "basis": "basis you supply", "adjustment": "wash-sale adjustment"}[kind]
        col = {"proceeds": "d", "basis": "e", "adjustment": "g"}[kind]
        clone["label"] = f"Part {'I' if term == 'st' else 'II'} box {letter} column ({col}): {WORD[term]} {label}, no Form 1099-B"
        assert "noncovered" not in json.dumps(clone), clone
        parts.append(clone)
    body["itemizations"] = parts
    subs = list(body["requirement"]["subtotals"])
    for term in TERMS:
        subs += [subtotal(term, "proceeds"), subtotal(term, "basis"), P + f"schedule-d.line-{LINE[term]}"]
    if "f8949_reads_lines_2_9" in REPAIRS:
        subs += [P + f"schedule-d.line-{NC_LINE[term]}" for term in TERMS if P + f"schedule-d.line-{NC_LINE[term]}" not in subs]
    body["requirement"]["subtotals"] = subs
    return body


def attachment_schedule_d() -> dict[str, Any]:
    body = read("attachment.schedule-d.v7.json")
    body["version"] = "v8"
    subs = list(body["requirement"]["subtotals"])
    for term in TERMS:
        subs += [subtotal(term, "proceeds"), subtotal(term, "basis"), P + f"schedule-d.line-{LINE[term]}"]
    body["requirement"]["subtotals"] = subs
    return body


def retitled(name: str, version: str, old: str, new: str) -> dict[str, Any]:
    body = read(name)
    body["version"] = version
    text = json.dumps(body).replace(old, new)
    return json.loads(text)


# ---- build ----------------------------------------------------------------


ROLE = {"bundle.v2": "fact-type-bundle", "source-family.v2": "source-family",
        "source-closure-mapping.v4": "source-closure-mapping", "citation.v1": "citation",
        "form-field.v3": "form-field", "attachment-rule.v8": "attachment-rule", "input-question.v1": "input-question"}


def artifacts() -> tuple[list[tuple[str, dict[str, Any]]], dict[tuple[str, str], tuple[str, str]]]:
    """(file name, body) for every new or successor member; and successor -> (old version, old schema)."""
    out: list[tuple[str, dict[str, Any]]] = [
        ("f8949-no1099b-st.bundle.json", bundle("st")),
        ("f8949-no1099b-lt.bundle.json", bundle("lt")),
        ("schedule-d-boundary-form8949-in-class.bundle.json", boundary_bundle()),
        ("closure-mapping.f8949-no1099b.json", mapping()),
        ("input-question.f8949-no1099b-sold.json", question()),
        *amount_questions(),
    ]
    for term in TERMS:
        for kind in (None, *KINDS):
            out.append((f"family.f8949-no1099b-{term}" + (f"-{kind}" if kind else "") + ".json", family(term, kind)))
        for kind in KINDS:
            out.append((f"rule.f8949-no1099b-{term}-{kind}-subtotal.json", renamed(term, kind)))
        out.append((f"rule.schedule-d-line{LINE[term]}.json", line_rule(term)))
        out.append((f"schedule-d.line-{LINE[term]}.form-field.json", form_field(term)))
        out.append((f"citation.schedule-d.line-{LINE[term]}.json", citation(term)))
    old: dict[tuple[str, str], tuple[str, str]] = {}

    def succ(name: str, new_name: str, version: str, prior: str, **kw: Any) -> None:
        body = successor(name, version, **kw)
        old[(body["id"], version)] = (prior, read(name)["schema"])
        out.append((new_name, body))

    arm_note = "v80: the form8949-in-class answer (boxes B, C, E and F) admits the return as the v79 answer does."
    for term in TERMS:
        for kind in KINDS:
            succ(f"rule.f1099b-noncovered-{term}-{kind}-subtotal.json",
                 f"rule.f1099b-noncovered-{term}-{kind}-subtotal.v2.json", "v2", "v1", pairs=[], arm=True, notes=arm_note)
    for term in TERMS:
        name = f"rule.schedule-d-line{NC_LINE[term]}.json"
        body = paired_nc_line(successor(name, "v2", pairs=[], arm=True, notes=arm_note), term)
        old[(body["id"], "v2")] = ("v1", read(name)["schema"])
        out.append((f"rule.schedule-d-line{NC_LINE[term]}.v2.json", body))
    out.extend(nc_amount_questions())
    if "amounts_agree" in REPAIRS:
        out.extend(agreement_members())
    succ("rule.schedule-d-line1a-gain.v4.json", "rule.schedule-d-line1a-gain.v5.json", "v5", "v4", pairs=[], arm=True, notes=arm_note)
    succ("rule.schedule-d-line8a-gain.v5.json", "rule.schedule-d-line8a-gain.v6.json", "v6", "v5", pairs=[], arm=True, notes=arm_note)
    succ("rule.selected-preferential-base.v7.json", "rule.selected-preferential-base.v8.json", "v8", "v7",
         pairs=LINE_PAIRS, arm=True, notes="v8: line 3 and line 10 are Schedule D activity; " + arm_note)
    succ("rule.form1040-line7a.v6.json", "rule.form1040-line7a.v7.json", "v7", "v6", pairs=LINE_PAIRS, arm=False,
         notes="v7: line 3 and line 10 are Schedule D activity.")
    succ("rule.schedule-d-line7.v4.json", "rule.schedule-d-line7.v5.json", "v5", "v4",
         pairs=[(P + "schedule-d.line-2", P + "schedule-d.line-3")], arm=False, notes="v5 adds line 3.")
    succ("rule.schedule-d-line15.v6.json", "rule.schedule-d-line15.v7.json", "v7", "v6",
         pairs=[(P + "schedule-d.line-9", P + "schedule-d.line-10")], arm=False, notes="v7 adds line 10.")
    for name, new_name, version, prior, body in (
        ("attachment.f8949.v3.json", "attachment.f8949.v4.json", "v4", "v3", attachment_f8949()),
        ("attachment.schedule-d.v7.json", "attachment.schedule-d.v8.json", "v8", "v7", attachment_schedule_d()),
        ("schedule-d.line-7.form-field.v3.json", "schedule-d.line-7.form-field.v4.json", "v4", "v3",
         retitled("schedule-d.line-7.form-field.v3.json", "v4", "lines 1a, 1b, 2, and 6", "lines 1a, 1b, 2, 3, and 6")),
        ("schedule-d.line-15.form-field.v3.json", "schedule-d.line-15.form-field.v4.json", "v4", "v3",
         retitled("schedule-d.line-15.form-field.v3.json", "v4", "lines 8a, 8b, 9, 13, and 14", "lines 8a, 8b, 9, 10, 13, and 14")),
    ):
        old[(body["id"], version)] = (prior, read(name)["schema"])
        out.append((new_name, body))
    return out, old


def companion_v80() -> None:
    """Track 1's two loader entries for v80, applied in process."""
    original_decl = loader.domain_package_companion_declarations
    original_refusal = loader.named_covered_flag_refusal_maps

    def declarations() -> dict[tuple[str, str], dict[str, Any]]:
        found = dict(original_decl())
        v79 = found[(PKG, "v79")]
        pairs = dict(v79["presence_pairs"])
        for term in TERMS:
            for kind in KINDS:
                pairs[member_fact(term, kind)] = member_fact(term, None)
        found[(PKG, "v80")] = {"presence_pairs": pairs, "value_domains": dict(v79["value_domains"])}
        return found

    def refusal() -> dict[tuple[str, str], dict[str, str]]:
        found = dict(original_refusal())
        found[(PKG, "v80")] = dict(found[(PKG, "v79")])
        return found

    if getattr(loader, "_cf_patched", False):
        return
    loader.domain_package_companion_declarations = declarations  # type: ignore[assignment]
    loader.named_covered_flag_refusal_maps = refusal  # type: ignore[assignment]
    loader._cf_patched = True  # type: ignore[attr-defined]


def digest(folder: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob("*.json"))}


def build(scratch: Path, *, write_rules: bool = True) -> dict[str, Any]:
    source_content, source_releases = probe.CONTENT, probe.RELEASE_DIR
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(source_content, content)
    shutil.copytree(source_releases, releases)
    before = digest(content)
    if write_rules:
        if RULES.exists():
            shutil.rmtree(RULES)
        RULES.mkdir()
    bodies, old = artifacts()
    members, entrypoints = [], []
    pinned = json.loads((content / "package.core-calculations.v79.json").read_text(encoding="utf-8"))
    entry_keys = {(e["id"], e["version"]) for e in pinned["entrypoints"]}
    for name, body in bodies:
        if (content / name).exists():
            raise AssertionError(f"{name} already exists")
        text = json.dumps(body, indent=2) + "\n"
        (content / name).write_text(text, encoding="utf-8")
        if write_rules:
            (RULES / name).write_text(text, encoding="utf-8")
        new = {"id": body["id"], "version": body["version"], "schema": body["schema"],
               "role": ROLE.get(body["schema"], "computation")}
        key = (body["id"], body["version"])
        if key in old:
            prior, prior_schema = old[key]
            members.append({"op": "replace", "old": {**new, "version": prior, "schema": prior_schema}, "new": new})
            if (body["id"], prior) in entry_keys:
                entrypoints.append({"op": "replace", "old": {"id": body["id"], "version": prior},
                                    "new": {"id": body["id"], "version": body["version"]}})
        else:
            members.append({"op": "add", "new": new})
            entrypoints.append({"op": "add", "value": {"id": body["id"], "version": body["version"]}})
    changes = {"package_version": "v80", "release_version": "v78", "members": members, "entrypoints": entrypoints,
               "registry_sort": "id_version", "registry_new_key_order": ["checksum", "id", "version"]}
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v79.json",
        content / "published-packages.v77.json",
        releases / "demo.release.sli-worksheet-integration.2025.v77.json",
        content, scratch / "changes.json", scratch / "out",
    )
    for name, folder, target in (
        ("package.json", content, "package.core-calculations.v80.json"),
        ("registry.json", content, "published-packages.v78.json"),
        ("release.json", releases, "demo.release.sli-worksheet-integration.2025.v78.json"),
    ):
        shutil.copy(scratch / "out" / name, folder / target)
    after = digest(content)
    changed = sorted(n for n in before if after.get(n) != before[n])
    added = sorted(n for n in after if n not in before)
    if write_rules:
        (RULES / "_members.json").write_text(json.dumps(members, indent=2) + "\n", encoding="utf-8")
    companion_v80()
    probe.CONTENT, probe.RELEASE_DIR = content, releases
    return {
        "package": report.get("package"), "release": report.get("release"),
        "members_edited": len(members), "added_members": sum(1 for m in members if m["op"] == "add"),
        "replaced_members": sum(1 for m in members if m["op"] == "replace"),
        "inherited_inconsistencies": [list(r) for r in (report.get("inherited_inconsistencies") or ())],
        "existing_files_changed": changed, "files_added": len(added),
    }


def pin(version: str) -> None:
    if version == "v80":
        probe.PACKAGE, probe.PACKAGE_VERSION = "package.core-calculations.v80.json", "v80"
        probe.REGISTRY, probe.RELEASE, probe.RELEASE_VERSION = (
            "published-packages.v78.json", "demo.release.sli-worksheet-integration.2025.v78.json", "v78")
    else:
        cp.pin_v79()


# ---- recording ------------------------------------------------------------


BUNDLES: dict[str, dict[str, Any]] = {}


def open_cf(acts: list[dict[str, Any]]) -> None:
    for term in TERMS:
        b = BUNDLES.setdefault(term, bundle(term))
        cp.proto._adopt(acts, b)
    cp.proto._adopt(acts, BUNDLES.setdefault("boundary", boundary_bundle()))
    if "amounts_agree" in REPAIRS:
        cp.proto._adopt(acts, BUNDLES.setdefault("nc_check", nc_check_bundle()))
    for term in TERMS:
        for kind in (None, *KINDS):
            slug = fam(term, kind).removeprefix(P + "f8949.")
            probe._add(acts, "horizon-genesis", {
                "family": {"id": fam(term, kind), "version": "v1"},
                "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
                "horizon_id": f"demo.cf.{slug}.h0",
            })


def record(acts: list[dict[str, Any]], term: str, kind: str | None, value: object, tag: str) -> None:
    family_id = fam(term, kind)
    entity = f"demo.cf.{tag}.sale"
    if not cp.proto._known_entity(acts, entity):
        probe._introduce(acts, entity, SALE_KIND)
    head = probe.horizons(acts, family_id)[-1]
    slug = family_id.removeprefix(P + "f8949.")
    successor_id = f"demo.cf.{tag}.{slug}.h{len(probe.horizons(acts, family_id))}"
    probe._add(acts, "member-transition", {
        "family": {"id": family_id, "version": "v1"},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.cf.{tag}.{slug}.member", fact_id_for(member_fact(term, kind), (("sale", entity), ("tax-year", probe.YEAR))),
            value)},
        "successor": {"id": successor_id, "predecessor": head},
    })


def cf_sale(acts: list[dict[str, Any]], term: str, proceeds: float, basis: float | None, tag: str,
            adjustment: float | None = None, *, scalars: tuple[str, ...] = KINDS, long_term: str | None = None) -> None:
    value: dict[str, Any] = {"proceeds": proceeds, "long_term": long_term or ("yes" if term == "lt" else "no"),
                             "wash_disallowed": adjustment or 0}
    if basis is not None:
        value["basis"] = basis
    record(acts, term, None, value, tag)
    amounts = {"proceeds": proceeds, "basis": basis, "adjustment": adjustment}
    for kind in KINDS:
        if kind in scalars and amounts[kind] is not None:
            record(acts, term, kind, amounts[kind], tag)


def say(acts: list[dict[str, Any]], fact_type: str, value: str, tag: str) -> list[dict[str, Any]]:
    probe._add(acts, "assertion", {"finding": _attested(
        f"demo.cf.{tag}", fact_id_for(fact_type, (("tax-year", probe.YEAR),)), value)})
    return acts


def v80_return(*, q1: str | None = "no", q2: str | None = "no", form8949: str | None = None, path_b: str | None = None,
               old_ic: str | None = None, new_ic: str | None = None,
               sales: Callable[[list[dict[str, Any]]], list[dict[str, Any]] | None] | None = None) -> list[dict[str, Any]]:
    """A harness return with both noncovered and no-1099-B families open.

    Sales are recorded first, then every answer, so neither group answer is stale.
    """
    acts = copy.deepcopy(ccr.base_return())
    p0b._open(acts, None)
    open_cf(acts)
    if sales is not None:
        replaced = sales(acts)
        if replaced is not None:
            acts = replaced
    if q1 is not None:
        acts = say(acts, P + "f1099b.noncovered-sold.source-closure", q1, "q1")
    if q2 is not None:
        acts = say(acts, Q2, q2, "q2")
    acts = ccr._renumbered(acts)
    if form8949 is not None:
        acts = probe.boundary(acts, form8949, path_b)
    if old_ic is not None:
        acts = probe.answer(acts, OLD_IC, old_ic, "oldic")
    if new_ic is not None:
        acts = probe.answer(acts, NEW_IC, new_ic, "newic")
    return ccr._renumbered(acts)


# ---- cases ----------------------------------------------------------------


def new_cases() -> dict[str, Callable[[], list[dict[str, Any]]]]:
    def with_sales(fn: Callable[[list[dict[str, Any]]], Any], **kw: Any) -> Callable[[], list[dict[str, Any]]]:
        return lambda: v80_return(sales=fn, **kw)

    cls = {"q1": "no", "q2": "yes", "form8949": "no", "path_b": "no", "new_ic": "yes"}

    def mixed(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        cp.on_be(acts, "st", 3000.0, 3500.0, "mxb")
        cf_sale(acts, "st", 2500.0, 1000.0, "mxc")
        cf_sale(acts, "lt", 6000.0, 2000.0, "mxf")
        return cp.covered_a(ccr._renumbered(acts), 5000.0, 4000.0, "mxa")

    def late(acts: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return acts

    def late_member(answer_after: str | None) -> Callable[[], list[dict[str, Any]]]:
        def build() -> list[dict[str, Any]]:
            acts = v80_return(q2="no", form8949="no", path_b="no", new_ic="yes")
            cf_sale(acts, "lt", 6000.0, 2000.0, "late")
            if answer_after is not None:
                acts = say(acts, Q2, answer_after, "q2again")
            return ccr._renumbered(acts)
        return build

    return {
        "wage_q2_no": lambda: v80_return(),
        "wage_q2_unanswered": lambda: v80_return(q2=None),
        "f_gain": with_sales(lambda a: cf_sale(a, "lt", 6000.0, 2000.0, "fgain"), **cls),
        "c_loss": with_sales(lambda a: cf_sale(a, "st", 2000.0, 8000.0, "closs"), **cls),
        "c_wash": with_sales(lambda a: cf_sale(a, "st", 4000.0, 7000.0, "cwash", adjustment=1000.0), **cls),
        "mixed_abcf": with_sales(mixed, **{**cls, "q1": "yes", "old_ic": "no"}),
        "mixed_abcf_old_ic_unanswered": with_sales(mixed, **{**cls, "q1": "yes"}),
        "f_gain_new_ic_no": with_sales(lambda a: cf_sale(a, "lt", 6000.0, 2000.0, "fno"), **{**cls, "new_ic": "no"}),
        "f_gain_new_ic_unanswered": with_sales(lambda a: cf_sale(a, "lt", 6000.0, 2000.0, "fun"), **{**cls, "new_ic": None}),
        "f_gain_q2_no_with_member": with_sales(lambda a: cf_sale(a, "lt", 6000.0, 2000.0, "fq2no"), **{**cls, "q2": "no"}),
        "c_basis_missing": with_sales(lambda a: cf_sale(a, "st", 2000.0, 8000.0, "nob", scalars=("proceeds",)), **cls),
        "c_proceeds_missing": with_sales(lambda a: cf_sale(a, "st", 2000.0, 8000.0, "nop", scalars=("basis",)), **cls),
        "c_basis_object_missing": with_sales(lambda a: cf_sale(a, "st", 2000.0, None, "noobj", scalars=("proceeds",)), **cls),
        "c_code_w_on_gain": with_sales(lambda a: cf_sale(a, "st", 6000.0, 2000.0, "wgain", adjustment=500.0), **cls),
        "f_holding_mismatch": with_sales(lambda a: cf_sale(a, "lt", 6000.0, 2000.0, "hold", long_term="no"), **cls),
        "q2_yes_nothing_recorded": with_sales(late, **cls),
        "unrecorded_out_of_class": lambda: v80_return(q2="no", form8949="no", path_b="no", new_ic="no"),
        "unrecorded_8949_no_only": lambda: v80_return(q2="no", form8949="no"),
        "late_member_after_no": late_member(None),
        "late_member_reanswered_yes": late_member("yes"),
    }


def v79_cases() -> dict[str, list[dict[str, Any]]]:
    """Every case tests/test_noncovered_sales_v79.py pins on v79, plus the P0 probe's v79 cases."""
    cases = p0b._cases()
    cases.pop("_part_ii_b_build_error", None)
    for name, build in cp.cases().items():
        try:
            cases["probe_" + name] = build()
        except Exception:  # noqa: BLE001 — the schema-rejected case has no act list
            continue
    return cases


def with_q2(acts: list[dict[str, Any]], answer: str | None) -> list[dict[str, Any]]:
    out = copy.deepcopy(acts)
    open_cf(out)
    if answer is not None:
        say(out, Q2, answer, "q2carry")
    return ccr._renumbered(out)


# ---- expectations (hand values, see p0-law-state-design.md) ---------------


def form1040(result: dict[str, Any]) -> tuple[Any, Any]:
    lines = result.get("lines") or {}
    return tuple((lines.get(k) or [None, None])[1] for k in ("form1040.line-15", "form1040.line-16"))  # type: ignore[return-value]


HAND = {
    "wage_q2_no": {"form1040.line-15": 34250, "form1040.line-16": 3875, "form1040.line-7a": 0,
                   "schedule-d.line-3": 0, "schedule-d.line-10": 0, "attachments": ("guard_inapplicable", "guard_inapplicable")},
    "f_gain": {"schedule-d.line-10": 4000, "schedule-d.line-15": 4000, "schedule-d.line-16": 4000,
               "form1040.line-7a": 4000, "form1040.line-15": 38250, "form1040.line-16": 3875,
               "preferential": 4000, "attachments": ("published", "published")},
    "c_loss": {"schedule-d.line-3": -6000, "schedule-d.line-7": -6000, "schedule-d.line-16": -6000,
               "schedule-d.line-21": 3000, "form1040.line-7a": -3000, "form1040.line-15": 31250,
               "form1040.line-16": 3515, "preferential": 0, "attachments": ("published", "published")},
    "c_wash": {"schedule-d.line-3": -2000, "schedule-d.line-7": -2000, "schedule-d.line-16": -2000,
               "schedule-d.line-21": 2000, "form1040.line-7a": -2000, "form1040.line-15": 32250,
               "form1040.line-16": 3635, "preferential": 0, "attachments": ("published", "published")},
    "mixed_abcf": {"schedule-d.line-1a": 1000, "schedule-d.line-2": -500, "schedule-d.line-3": 1500,
                   "schedule-d.line-7": 2000, "schedule-d.line-10": 4000, "schedule-d.line-15": 4000,
                   "schedule-d.line-16": 6000, "form1040.line-7a": 6000, "form1040.line-15": 40250,
                   "form1040.line-16": 4115, "preferential": 4000, "attachments": ("published", "published")},
}
HAND["mixed_abcf_old_ic_unanswered"] = HAND["mixed_abcf"]
HAND["late_member_reanswered_yes"] = HAND["f_gain"]
BLOCKED = {  # Form 1040 line 15 and 16 blocked; attachments (f8949, schedule-d)
    "wage_q2_unanswered": ("blocked", "blocked"),
    "f_gain_new_ic_no": ("blocked", "blocked"),
    "f_gain_new_ic_unanswered": ("blocked", "blocked"),
    "f_gain_q2_no_with_member": ("blocked", "blocked"),
    "c_basis_missing": ("blocked", "blocked"),
    "c_proceeds_missing": ("blocked", "blocked"),
    "c_code_w_on_gain": ("blocked", "blocked"),
    "f_holding_mismatch": ("blocked", "blocked"),
    "q2_yes_nothing_recorded": ("blocked", "blocked"),
    "unrecorded_out_of_class": ("blocked", "blocked"),
    "unrecorded_8949_no_only": ("blocked", "blocked"),
    "late_member_after_no": ("blocked", "blocked"),
}


def check(name: str, result: dict[str, Any]) -> dict[str, Any]:
    """Compare a v80 run with the hand values. Returns the mismatches (empty is a pass)."""
    if name == "c_basis_object_missing":
        return {} if result.get("error") == "FindingModelError" else {"error": result.get("error")}
    if result.get("error"):
        return {"error": result.get("error")}
    lines = result.get("lines") or {}
    att = result.get("attachments") or {}
    got_att = (att.get("f8949"), att.get("schedule-d"))
    bad: dict[str, Any] = {}
    if not result.get("presentation_valid"):
        bad["presentation_valid"] = result.get("presentation_valid")
    if name in HAND:
        for key, want in HAND[name].items():
            if key == "attachments":
                got: Any = got_att
            elif key == "preferential":
                raw = (result.get("symbols") or {}).get("capital-gains.selected-preferential-base")
                got = None if raw is None else float(raw)
            else:
                got = (lines.get(key) or [None, None])[1]
            if got != want and not (isinstance(want, (int, float)) and got is not None and float(got) == float(want)):
                bad[key] = {"want": want, "got": got}
    elif name in BLOCKED:
        for key in ("form1040.line-15", "form1040.line-16"):
            if (lines.get(key) or [None])[0] != "blocked":
                bad[key] = lines.get(key)
        if got_att != BLOCKED[name]:
            bad["attachments"] = {"want": BLOCKED[name], "got": got_att}
    return bad


def compare(v79: dict[str, Any], v80: dict[str, Any]) -> dict[str, Any]:
    """Every line and attachment v79 shows, on v80. Lines 3 and 10 are new and listed separately."""
    diff: dict[str, Any] = {}
    if v79.get("error") or v80.get("error"):
        if v79.get("error") != v80.get("error"):
            diff["error"] = [v79.get("error"), v80.get("error")]
        return diff
    for key, value in (v79.get("lines") or {}).items():
        if (v80.get("lines") or {}).get(key) != value:
            diff[key] = [value, (v80.get("lines") or {}).get(key)]
    if v79.get("attachments") != v80.get("attachments"):
        diff["attachments"] = [v79.get("attachments"), v80.get("attachments")]
    return diff


def trim(result: dict[str, Any]) -> dict[str, Any]:
    keep = ("error", "message", "stop_reason", "presentation_valid", "presentation_error", "duplicate_field_ids",
            "lines", "line_text", "symbols", "attachments", "blocked", "questions", "f8949_parts", "seconds")
    out = {k: result.get(k) for k in keep if result.get(k) not in (None, [], {})}
    if "blocked" in out:
        out["blocked"] = out["blocked"][:14]
    return out


def main() -> None:
    selected = set(sys.argv[1:])
    cp.pin_v79()
    cp.install_v79_noncovered()
    payload: dict[str, Any] = {"source_ref": "79448842", "scratch": "v80 / registry v78 / release v78 from v79"}
    with tempfile.TemporaryDirectory() as tmp:
        payload["build"] = build(Path(tmp).resolve() / "scratch")
        print("built", payload["build"]["package"], flush=True)
        pin("v80")
        new_results: dict[str, Any] = {}
        for name, builder in new_cases().items():
            if selected and name not in selected and "new" not in selected:
                continue
            result = cp.execute(builder, f"demo.cf.v80.{name}")
            new_results[name] = {"result": trim(result), "mismatch": check(name, result)}
            print(name, result.get("error") or result.get("stop_reason"), form1040(result),
                  new_results[name]["mismatch"] or "ok", flush=True)
        payload["v80_cases"] = new_results
        chunk = next((tok for tok in selected if tok.startswith("carry")), None)
        if not selected or chunk is not None:
            carried: dict[str, Any] = {}
            items = sorted(v79_cases().items())
            if chunk and "/" in chunk:  # carryK/N runs the K-th of N slices
                k, n = (int(x) for x in chunk.removeprefix("carry").split("/"))
                items = items[k - 1::n]
            for name, acts in items:
                pin("v79")
                before = cp.execute(lambda acts=acts: acts, f"demo.cf.c79.{name}")
                pin("v80")
                after = cp.execute(lambda acts=acts: with_q2(acts, "no"), f"demo.cf.c80.{name}")
                untouched = cp.execute(lambda acts=acts: with_q2(acts, None), f"demo.cf.u80.{name}")
                carried[name] = {
                    "v79": {"form1040": form1040(before), "attachments": before.get("attachments"),
                            "error": before.get("error")},
                    "v80_q2_no_diff": compare(before, after),
                    "v80_q2_no_lines_3_10": {k: (after.get("lines") or {}).get(k)
                                             for k in ("schedule-d.line-3", "schedule-d.line-10")},
                    "v80_q2_unanswered_form1040": form1040(untouched),
                }
                print("carry", name, form1040(before), carried[name]["v80_q2_no_diff"] or "same", flush=True)
            payload["v79_returns_on_v80"] = carried
    if selected and OUT.exists():
        merged = json.loads(OUT.read_text(encoding="utf-8"))
        merged.setdefault("v80_cases", {}).update(payload.get("v80_cases") or {})
        if "v79_returns_on_v80" in payload:
            merged.setdefault("v79_returns_on_v80", {}).update(payload["v79_returns_on_v80"])
        merged["build"] = payload["build"]
        payload = merged
    OUT.write_text(probe.scrub(json.dumps(payload, indent=1, sort_keys=True)) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
