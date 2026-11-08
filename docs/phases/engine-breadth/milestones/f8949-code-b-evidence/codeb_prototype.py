"""Scratch core v81: Form 1099-B sales whose reported basis is wrong (code B).

P0 prototype for docs/phases/engine-breadth/milestones/f8949-code-b.md.
Copies the production content and release directories to a temporary
directory, writes the successor set there, generates package v81 / registry
v79 / release v79 from v80 with tools.package_successor, and runs each case
through live_coordinate_run. Nothing under packages/ is written. The only
in-process patch is the per-package companion declaration and covered-flag
refusal map in packages/tax/loader.py, which Track 1 would add as two
entries for v81.

    python3 docs/phases/engine-breadth/milestones/f8949-code-b-evidence/codeb_prototype.py [workers] [case ...]

Writes codeb-prototype-output.json beside this file. Its ``build.members``
lists every new or successor member. The bodies are not committed, to keep
the output small; ``python3 ... codeb_prototype.py rules <dir>`` writes them
to a directory outside the repository for inspection.

Track 0 added the switchable repairs in ``REPAIRS`` (all on by default; an
empty set builds the decided design). codeb-prototype-output.json is P0's
record of the design before them; codeb_track0.py and
codeb-track0-output.json supersede it for every case they rerun.

The f8949-boxes-cf harness (track0 and through it cf_prototype, cf_probe and
the noncovered-sales helpers) is loaded once, under a unique module name, as
tests/test_no1099b_sales_v80.py loads it.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CF_EVIDENCE = HERE.parent / "f8949-boxes-cf-evidence"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(CF_EVIDENCE))
OUT = HERE / "codeb-prototype-output.json"
Acts = list[dict[str, Any]]


def load(name: str, path: Path) -> Any:
    """Load an evidence module under a unique name (f8949-boxes-cf retrospective)."""
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


track0: Any = load("f8949_boxes_cf_track0", CF_EVIDENCE / "track0.py")
cfp, cp = track0.cfp, track0.cp
probe = cp.probe
P = cfp.P
codeb_probe: Any = load("f8949_code_b_probe", HERE / "codeb_probe.py")

from packages.kernel.facts import fact_id_for  # noqa: E402
from packages.tax import loader  # noqa: E402
from tests.helpers import current_core_returns as ccr  # noqa: E402
from tests.test_refund_or_amount_owed_track1 import _attested  # noqa: E402
from tools.package_successor import generate_to_directory  # noqa: E402

# Track 0 repairs (track0-closure.md). Each is a switch; all are on by default.
# An empty set builds the decided design (Decisions 1-4), which is P0's design.
#
# - cross_term_exclusive: a code B sale family also excludes the other term's
#   covered, code W and box B/E families, so one transaction cannot be counted
#   once as a code B sale and again on the other term's line.
# - check_closes_first: the return-level amounts check closes over the code B
#   families before it reads any sale's agreement, so a code B answer made
#   stale by a later member blocks it SOURCE_SET_UNCLOSED, and the page asks
#   that answer again even when both terms have members.
# - attachments_read_count: a return-level count of code B sales per term
#   (f1099b.code-b-{st,lt}-count), and both attachments are required when it is
#   above zero, so a code B row whose proceeds and shown basis are both zero
#   still requires Form 8949 and Schedule D.
# - field_words: the line 1b and 8b blocked sentence names what the line waits
#   for (the column (g) row), not the correct basis, which is refused at entry.
#
# Track 1 (Decision 6) adds four switches that fix inherited v80 gaps. Each one
# changes returns v80 computes; codeb_track0.py lists every one that changes.
#
# - w_zero_proceeds: a return-level count of code W sales per term
#   (f1099b.covered-w-{st,lt}-count), and both attachments are required when it
#   is above zero, so a code W row with zero proceeds requires Form 8949 and
#   Schedule D.
# - b_zero_proceeds: the same count for the box B and box E sales
#   (f1099b.noncovered-{st,lt}-count), so a box B or E row with zero proceeds
#   requires Form 8949.
# - v80_cross_term_exclusive: one transaction recorded on a Form 1099-B sale
#   family of one term and on one of the other term is refused, never counted
#   twice. Each family checks the other term's families at or before it in the
#   order covered (line 1a/8a), code W, noncovered (box B/E), so every pair is
#   checked and no covered or code W check reads the noncovered closure. The
#   noncovered amounts-agree rule takes the check (v2); the covered and code W
#   sales get a new per-sale admission rule and a return-level check that lines
#   1a, 8a, 1b and 8b require.
# - covered_tsa_blocks: a covered or code W sale flagged
#   taxpayer_side_adjustment "yes" is refused by the same admission rule (the
#   flag is read through a yes/no parameter, since a rule cannot compare a text
#   field), and lines 1a and 8a say why (form fields v3 and v2).
#
# The fresh-reader review repair (docs/reviews/f8949-code-b/review.md) adds two
# more, and rewords the line fields and the two new questions:
#
# - direct_zero_proceeds (B1): a return-level count of the line 1a and 8a sales
#   per term (f1099b.covered-{st,lt}-count), read by the Schedule D attachment,
#   and Form 1040 line 7a v8, which treats a nonzero line 1a or 8a as Schedule D
#   activity. A direct sale with zero proceeds then requires Schedule D and
#   reaches line 7a.
# - covered_flags_block (S5): the admission rule also refuses a covered or code
#   W sale flagged ordinary_indicated, box_1f_market_discount, qof_indicated or
#   collectibles_or_special_rate "yes" (ADR-0052 Decision 1 lists all five flags
#   in the eligible-sale predicate).
TRACK1_REPAIRS: frozenset[str] = frozenset({"w_zero_proceeds", "b_zero_proceeds", "v80_cross_term_exclusive",
                                            "covered_tsa_blocks", "direct_zero_proceeds", "covered_flags_block"})
TRACK0_REPAIRS: frozenset[str] = frozenset({"cross_term_exclusive", "check_closes_first", "attachments_read_count",
                                            "field_words"})
ALL_REPAIRS: frozenset[str] = TRACK0_REPAIRS | TRACK1_REPAIRS
REPAIRS: set[str] = set(ALL_REPAIRS)

PKG = P + "package.core-calculations"
IC2 = cfp.NEW_IC  # schedule-d-boundary.form8949-in-class (v80)
IC3 = P + "schedule-d-boundary.form8949-code-b-in-class"
Q1, Q2 = cfp.Q1, cfp.Q2
Q3 = P + "f1099b.code-b-sold.source-closure"
NO8949, PATH_B = cfp.NO8949, cfp.PATH_B
TERMS = ("st", "lt")
KINDS = ("proceeds", "basis", "adjustment")
WORD = {"st": "short-term", "lt": "long-term"}
BOX = {"st": "A", "lt": "D"}
LINE = {"st": "1b", "lt": "8b"}
PART = {"st": "I", "lt": "II"}
Q3_TEXT = ("Did any Form 1099-B or substitute statement you received show a cost or other basis, reported to the IRS, "
           "that is wrong?")
IC3_TITLE = (
    "Whether this return's Form 8949 work is only (1) sales your broker reported to the IRS with their basis, with "
    "no adjustment other than a wash-sale loss or a correction of a wrong reported basis (code B, column (e) the "
    "basis shown and column (g) the correction), and (2) sales of stocks or other securities in boxes B, C, E and "
    "F, each recorded once under the one box its statement gives it, with a basis you supply that is the correct "
    "basis even where a Form 1099-B showed another (and, on boxes C and F, net proceeds you supply), and an "
    "optional wash-sale adjustment. yes or no.")
IC3_TEXT = (
    "Each sale on your Form 8949 should be one of two kinds. (1) A sale your broker reported to the IRS with its "
    "basis, with no adjustment other than a wash-sale loss or a correction of that basis. (2) A sale of stocks or "
    "other securities, entered only once and in the one box its statement gives it, with a basis you supply (the "
    "correct basis, even if your Form 1099-B showed a different one), net proceeds you supply when you got no Form "
    "1099-B, and no adjustment other than a wash-sale loss. Is every sale on your Form 8949 one of these two kinds?")


# ---- small helpers ---------------------------------------------------------


def read(name: str) -> dict[str, Any]:
    return json.loads((ORIGIN[0] / name).read_text(encoding="utf-8"))


ORIGIN: list[Path] = []
ref, eq0, cat, has_sale, swap = cfp.ref, cfp.eq0, cfp.cat, cfp.has_sale, cfp.swap
G2 = cfp.GUARDED  # all(no-1099-B answer yes, v80 in-class yes)
G3 = {"op": "all", "args": [cat(Q3, "yes"), cat(IC3, "yes")]}


def fam(term: str, kind: str | None) -> str:
    return P + f"f1099b.code-b-{term}" + (f"-{kind}" if kind else "")


def member_fact(term: str, kind: str | None) -> str:
    return P + f"f1099b.code-b-{term}-txn" + (f".{kind}" if kind else "")


def subtotal(term: str, kind: str) -> str:
    return P + f"f1099b.code-b-{term}-{kind}-subtotal"


def gain(term: str) -> str:
    return P + f"f1099b.code-b-{term}-gain"


def sale_keys() -> list[dict[str, Any]]:
    return copy.deepcopy(read("f1099b-noncovered-st.bundle.json")["fact_types"][0]["identity_keys"])


CLOSURE_KEYS = cfp.CLOSURE_KEYS


# ---- vocabulary --------------------------------------------------------------


def bundle(term: str) -> dict[str, Any]:
    w = WORD[term]
    keys = sale_keys()
    sale = {
        "type": "object", "additionalProperties": False,
        "required": ["proceeds", "basis", "corrected_basis", "long_term", "wash_disallowed"],
        "properties": {
            "proceeds": {"type": "number", "minimum": 0},
            "basis": {"type": "number", "minimum": 0},
            "corrected_basis": {"type": "number", "minimum": 0},
            "long_term": {"enum": ["yes", "no"]},
            "wash_disallowed": {"type": "number", "minimum": 0},
        },
    }
    facts = [cfp.fact(member_fact(term, None),
                      f"One {w} Form 1099-B sale whose basis the broker reported to the IRS and which is wrong (Form "
                      f"8949 box {BOX[term]}, code B). basis is the basis the Form 1099-B shows (column (e)); "
                      "corrected_basis is the correct basis you supply; wash_disallowed is any wash-sale loss "
                      "disallowed (code W).", sale, keys),
             cfp.fact(fam(term, None) + ".source-closure", f"Closure of the {w} code B sale family.",
                      {"type": "boolean"}, CLOSURE_KEYS)]
    words = {"proceeds": "proceeds shown on the Form 1099-B (column (d))",
             "basis": "basis shown on the Form 1099-B (column (e))",
             "adjustment": "column (g) adjustment (the basis shown minus the correct basis, plus any wash-sale loss "
                           "disallowed)"}
    for kind in KINDS:
        schema: dict[str, Any] = {"type": "number"} if kind == "adjustment" else {"type": "number", "minimum": 0}
        facts.append(cfp.fact(member_fact(term, kind), f"The {words[kind]} of a {w} code B sale.", schema, keys))
        facts.append(cfp.fact(fam(term, kind) + ".source-closure", f"Closure of the {w} code B {kind} family.",
                              {"type": "boolean"}, CLOSURE_KEYS))
    facts += cfp.agree_facts(member_fact(term, None), keys, f"{w} code B sale")
    return {"schema": "bundle.v2", "id": P + f"f1099b.code-b-{term}.vocabulary", "version": "v1",
            "label": f"Vocabulary for {w} Form 1099-B sales whose reported basis is wrong (code B)",
            "fact_types": facts}


def boundary_bundle() -> dict[str, Any]:
    yes_no = {"enum": ["yes", "no"]}
    year = [{"name": "tax-year", "kind": "literal", "values": ["2025"]}]
    return {"schema": "bundle.v2", "id": P + "schedule-d-boundary.form8949-code-b-in-class.vocabulary",
            "version": "v1", "label": "Whether Form 8949 work is in the class with code B corrections",
            "fact_types": [cfp.fact(IC3, IC3_TITLE, yes_no, year), cfp.fact(Q3, Q3_TEXT, yes_no, year)]}


def family(term: str, kind: str | None) -> dict[str, Any]:
    source = read(f"family.f1099b-noncovered-{term}" + (f"-{kind}" if kind else "") + ".json")
    w = WORD[term]
    body: dict[str, Any] = {
        "schema": "source-family.v2", "id": fam(term, kind), "version": "v1",
        "title": f"{w} Form 1099-B sales whose reported basis is wrong (code B)" + (f", {kind}" if kind else "")
                 + ", tax year 2025",
        "scope": source["scope"],
        "closure_claim": f"Every {w} sale whose basis a Form 1099-B reported to the IRS and which is wrong is recorded"
                         + (f" with its {kind}" if kind else "") + " as of the keyed horizon.",
        "member_predicate": {"fact_type": member_fact(term, kind)},
        "authorizes_subtotal": subtotal(term, kind) if kind else P + f"f1099b.code-b-{term}-subtotal",
    }
    if kind is not None:
        return body
    field = lambda f: {"op": "field", "field": f}  # noqa: E731
    wash = {"op": "field", "field": "wash_disallowed", "default": 0}
    stem = P + f"constraint.code-b-{term}."
    constraints = [row for row in copy.deepcopy(source["member_constraints"]) if row["block_code"] == "HOLDING_PERIOD_MISMATCH"]
    for row in constraints:
        row["id"] = stem + "holding-period"
    constraints += [
        {"id": stem + "no-correction", "block_code": "CODE_B_WITHOUT_CORRECTION",
         "meaning": "The correct basis equals the basis the Form 1099-B shows, so there is nothing to correct. "
                    "Record the sale as a sale with no adjustment (or with code W only).",
         "violated_when": {"op": "compare", "comparison": "eq", "left": field("basis"), "right": field("corrected_basis")}},
        {"id": stem + "code-w-on-gain", "block_code": "CODE_W_ON_GAIN",
         "meaning": "A wash-sale disallowance is recorded on a sale that is not a loss once its basis is corrected.",
         "violated_when": {"op": "all", "args": [
             {"op": "compare", "comparison": "gt", "left": wash, "right": {"op": "literal", "arg": 0}},
             {"op": "compare", "comparison": "ge", "left": field("proceeds"), "right": field("corrected_basis")}]}},
        {"id": stem + "adjustment-exceeds-loss", "block_code": "ADJUSTMENT_EXCEEDS_LOSS",
         "meaning": "The wash-sale disallowance exceeds this sale's own loss once its basis is corrected.",
         "violated_when": {"op": "compare", "comparison": "gt", "left": wash, "right": {"op": "floor_zero", "value": {
             "op": "subtract", "left": field("corrected_basis"), "right": field("proceeds")}}}},
    ]
    body["member_constraints"] = constraints
    exclusive = []
    terms = TERMS if "cross_term_exclusive" in REPAIRS else (term,)
    neighbours = [(f"{name}-{t}", version) for t in terms for name, version in
                  (("covered", "v1"), ("covered-w", "v2"), ("noncovered", "v1"))]
    for other, version in neighbours:
        exclusive.append({"id": P + f"block.code-b-{term}-txn.excludes.{other}",
                          "incompatible_family": {"id": P + f"f1099b.{other}", "version": version},
                          "components": [{"fact_id_bound_key": k} for k in ("broker", "statement", "transaction", "tax-year")]})
    body["identity_exclusivity"] = exclusive
    return body


def mapping() -> dict[str, Any]:
    rows = []
    for term in TERMS:
        for kind in (None, *KINDS):
            rows.append({"family": {"id": fam(term, kind), "version": "v1"},
                         "member_fact_type": {"id": member_fact(term, kind), "version": "v1"},
                         "admits_symbol": subtotal(term, kind) if kind else P + f"f1099b.code-b-{term}-subtotal"})
    return {"schema": "source-closure-mapping.v4", "id": P + "closure-mapping.f1099b.code-b", "version": "v1",
            "closure_fact_type": {"id": Q3, "version": "v1"}, "closure_question": Q3_TEXT,
            "admission": {"no": "closed-empty", "yes": "until-later-member"}, "families": rows}


def questions() -> list[tuple[str, dict[str, Any]]]:
    def q(slug: str, fact: str, text: str) -> tuple[str, dict[str, Any]]:
        return (f"input-question.{slug}.json", {"schema": "input-question.v1", "id": P + f"input-question.{slug}",
                                                 "version": "v1", "fact_type": {"id": fact, "version": "v1"},
                                                 "question": text})
    out = [q("f1099b-code-b-sold", Q3, Q3_TEXT), q("schedule-d-boundary-form8949-code-b-in-class", IC3, IC3_TEXT)]
    for term in TERMS:
        what = f"each {WORD[term]} sale you recorded whose reported basis is wrong"
        out += [
            q(f"f1099b-code-b-{term}-proceeds", member_fact(term, "proceeds"),
              f"What are the proceeds shown on your Form 1099-B for {what}?"),
            q(f"f1099b-code-b-{term}-basis", member_fact(term, "basis"),
              f"What basis does your Form 1099-B show for {what}?"),
            q(f"f1099b-code-b-{term}-adjustment", member_fact(term, "adjustment"),
              f"What is the column (g) adjustment for {what}: the basis shown minus the correct basis, plus any "
              "wash-sale loss disallowed?"),
        ]
    return out


# ---- rules -------------------------------------------------------------------


def subtotal_rule(term: str, kind: str) -> dict[str, Any]:
    body = read(f"rule.f8949-no1099b-{term}-{kind}-subtotal.json")
    body = swap(body, P + f"f8949.no1099b-{term}-txn.{kind}", member_fact(term, kind))
    body = swap(body, P + f"f8949.no1099b-{term}-{kind}", fam(term, kind))
    body = swap(body, P + f"f8949.no1099b-{term}", fam(term, None))
    body = swap(body, P + f"f8949.no1099b-{term}-{kind}-subtotal", subtotal(term, kind))
    body = swap(body, IC2, IC3)
    body["id"] = P + f"rule.f1099b-code-b-{term}-{kind}-subtotal"
    body["publishes"] = subtotal(term, kind)
    body["notes"] = ("Sums one code B scalar family. A closed empty family publishes 0 and does not read the boundary. "
                     "A nonzero sum publishes only when the form8949-code-b-in-class answer is yes.")
    assert "no1099b" not in json.dumps(body), body["id"]
    return body


def agree_rule(term: str) -> dict[str, Any]:
    """Per sale: the proceeds and basis rows equal the sale's, and the column (g) row is the worksheet result.

    Worksheet for Basis Adjustments in Column (g): basis shown minus correct
    basis (positive when the shown basis is larger, negative when smaller),
    plus the wash-sale loss disallowed (More than one code: the net).
    """
    sale_fact = member_fact(term, None)
    proceeds, basis, adj = (member_fact(term, k) for k in KINDS)
    subject = {"op": "ref", "name": sale_fact}
    field = lambda f: {**subject, "field": f}  # noqa: E731
    eq = lambda left, right: {"op": "compare", "cmp": "eq", "left": left, "right": right}  # noqa: E731
    rows = lambda name, kind: {"op": "count", "name": name, "source_set": fam(term, kind)}  # noqa: E731
    present = lambda name, kind: {"op": "all", "args": [  # noqa: E731
        {"op": "compare", "cmp": "gt", "left": rows(name, kind), "right": 0},
        {"op": "conditional_dependency_set", "condition": True, "members": [ref(name)]}]}

    def ok(name: str, kind: str, expected: Any) -> dict[str, Any]:
        # A missing row is not compared here: the line's require_paired asks for it.
        return {"op": "any", "args": [eq(rows(name, kind), 0),
                                      {"op": "all", "args": [present(name, kind), eq(ref(name), expected)]}]}

    worksheet = {"op": "add", "args": [{"op": "subtract", "left": field("basis"), "right": field("corrected_basis")},
                                       field("wash_disallowed")]}
    other = "lt" if term == "st" else "st"
    checks = [ok(proceeds, "proceeds", field("proceeds")), ok(basis, "basis", field("basis")),
              ok(adj, "adjustment", worksheet),
              # One sale recorded under both terms is the same sale counted twice (v80 review S2).
              eq({"op": "count", "name": member_fact(other, None), "source_set": fam(other, None)}, 0)]
    lit = lambda v: {"op": "category_literal", "fact_type": {"id": cfp.agree_fact(sale_fact), "version": "v1"}, "value": v}  # noqa: E731
    return {
        "schema": "rule-artifact.v15", "id": sale_fact.replace(P, P + "rule.") + ".amounts-agree", "version": "v1",
        "scope": read("rule.schedule-d-line2.json")["scope"], "role": "computation",
        "subject": {"id": sale_fact, "version": "v1"}, "requires": [sale_fact], "pins": [], "when": True,
        "value": {"op": "choose", "when": {"op": "all", "args": checks}, "then": lit("agree"), "else": lit("disagree")},
        "publishes": cfp.agree_fact(sale_fact), "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}, "citations": [],
        "notes": "The line sums the rows; the member constraints read the sale. The proceeds and basis rows equal the "
                 "sale's, and the column (g) row equals the basis shown minus the correct basis plus the wash-sale "
                 "loss disallowed (the Worksheet for Basis Adjustments in Column (g), netted under More than one code).",
    }


def count_symbol(term: str) -> str:
    return P + f"f1099b.code-b-{term}-count"


def count_rule(term: str) -> dict[str, Any]:
    """The number of code B sales of one term (repair attachments_read_count).

    Every valid code B row has a shown or a correct basis above zero, but both
    proceeds and the shown basis can be zero (a broker that reports $0 for
    each), and then no amount the attachments read is above zero. The count
    is.
    """
    return {
        "schema": "rule-artifact.v15", "id": P + f"rule.f1099b-code-b-{term}-count", "version": "v1",
        "notes": (f"The number of {WORD[term]} code B sales recorded (Form 8949 box {BOX[term]} rows with code B). "
                  "Both attachments are required when it is above zero."),
        "role": "computation", "scope": read("rule.schedule-d-line2.json")["scope"],
        "publishes": count_symbol(term), "requires": [],
        "blocked": {"code": "SOURCE_SET_UNCLOSED", "missing": [fam(term, None), Q3]},
        "citations": [], "pins": [], "when": True,
        "value": {"op": "count", "name": member_fact(term, None), "source_set": fam(term, None)},
    }


def check_rule(term: str) -> dict[str, Any]:
    """The v80 return-level amounts check over the per-sale agreement (cfp.check_rule).

    With check_closes_first, the sales path first requires every family the
    agreement reads to be closed: this term's four and the other term's sale
    family. On an unclosed family the check then blocks SOURCE_SET_UNCLOSED
    naming those families, whose closure question the page asks, instead of
    DEPENDENCY_INVALID naming the sale, which has no question and hides the
    closure question from every line that reads the check.
    """
    body = cfp.check_rule(member_fact(term, None), fam(term, None))
    if "check_closes_first" in REPAIRS:
        other = "lt" if term == "st" else "st"
        closed = [*({"op": "require_closed", "source_set": fam(term, kind)} for kind in (None, *KINDS)),
                  {"op": "require_closed", "source_set": fam(other, None)}]
        for path in body["selection"]["paths"]:
            if path["id"] == "sales":
                path["when"] = {"op": "all", "args": closed}
        body["notes"] += (" The sales path first requires the code B families the agreement reads to be closed, so "
                          "an unclosed family asks its closure question.")
    return body


def gain_rule(term: str) -> dict[str, Any]:
    """Column (h) of the code B rows of Form 8949 box A or D: proceeds minus basis shown plus column (g).

    when: the four families are closed, and every recorded sale has its own
    proceeds, basis and column (g) rows (require_paired on the transaction
    key, with equal counts because the sale is keyed by three entities).

    value: a sale of this term is recorded: the total when the other term's
    family is confirmed, Form 8949 is answered no and the code B in-class
    answer is yes; else block. None is recorded: zero when the three
    subtotals are zero and the code B answer is no or the other term has a
    sale; else block (an unbacked yes).
    """
    other = "lt" if term == "st" else "st"
    p, b, a = (subtotal(term, k) for k in KINDS)
    sale = member_fact(term, None)
    total = {"op": "add", "args": [{"op": "subtract", "left": ref(p), "right": ref(b)}, ref(a)]}
    block = {"op": "block", "code": "DEPENDENCY_ABSENT"}
    count = lambda kind: {"op": "count", "name": member_fact(term, kind), "source_set": fam(term, kind)}  # noqa: E731
    paired = {"op": "all", "args": [{"op": "compare", "cmp": "eq", "left": count(None), "right": count(kind)} for kind in KINDS]}
    other_confirmed = {"op": "compare", "cmp": "gte", "right": 0,
                       "left": {"op": "count", "name": member_fact(other, None), "source_set": fam(other, None)}}
    present = {"op": "all", "args": [other_confirmed, cat(NO8949, "no"), cat(IC3, "yes")]}
    zero = {"op": "all", "args": [eq0(p), eq0(b), eq0(a),
                                  {"op": "any", "args": [has_sale(member_fact(other, None), fam(other, None)), cat(Q3, "no")]}]}
    when = {"op": "all", "args": [
        *({"op": "require_closed", "source_set": fam(term, kind)} for kind in (None, *KINDS)),
        *({"op": "require_paired", "key": "transaction", "withholding": member_fact(term, kind), "income": [sale]}
          for kind in KINDS),
    ]}
    return {
        "schema": "rule-artifact.v15", "id": P + f"rule.f1099b-code-b-{term}-gain", "version": "v1",
        "notes": (f"Form 8949 box {BOX[term]} rows with code B (and code W when both apply), column (h): proceeds "
                  "minus the basis shown plus the column (g) correction. Every recorded sale needs its own proceeds, "
                  "basis and column (g) rows. A closed empty set is zero unless the code B answer is an unbacked yes. "
                  f"Schedule D line {LINE[term]} adds it to the code W rows."),
        "role": "computation", "scope": read("rule.schedule-d-line2.json")["scope"],
        "publishes": gain(term),
        "requires": [p, b, a, cfp.check_symbol(sale)],
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": [p, b, a]},
        "citations": [{"id": P + f"citation.schedule-d.line-{LINE[term]}", "version": "v1"}],
        "pins": [], "when": when,
        "value": {"op": "choose", "when": paired, "then": {
            "op": "choose", "when": has_sale(sale, fam(term, None)),
            "then": {"op": "choose", "when": present, "then": total, "else": block},
            "else": {"op": "choose", "when": zero, "then": copy.deepcopy(total), "else": copy.deepcopy(block)}},
            "else": copy.deepcopy(block)},
    }


def line_successor(term: str) -> dict[str, Any]:
    body = read(f"rule.schedule-d-line{LINE[term]}.v2.json")
    body["version"] = "v3"
    body["value"] = {"op": "add", "args": [body["value"], ref(gain(term))]}
    body["requires"] = [*body["requires"], gain(term)]
    body["blocked"]["missing"] = [*body["blocked"]["missing"], gain(term)]
    if admission_wanted():
        body = checked_line(body, [admission_check(v80_sale("covered-w", term))])
    body["notes"] += (f" v3: adds the code B rows of box {BOX[term]} ({gain(term).removeprefix(P)}), whose column (g) "
                      "carries the basis correction and any wash-sale adjustment.")
    return body


def is_cat_yes(node: Any, fact: str) -> bool:
    return cfp.is_cat(node, fact) and (node.get("right") or {}).get("value") == "yes"


def widen3(node: Any) -> Any:
    """The successor edit for every rule that reads the v80 in-class answer.

    In an ``any`` list, ``all(code B answer yes, code B in-class yes)`` goes
    right before the first arm that is the v80 guarded arm or the v80
    in-class test. Elsewhere a bare v80 in-class test becomes
    ``any(that guarded arm, the test)``. A v80 return answers the code B
    question no, so the new arm is false without reading the new in-class
    answer, and the v80 arm decides as before. A code B filer answers yes and
    never needs the v80 in-class answer, which is false on that return.
    """
    if isinstance(node, list):
        return [widen3(item) for item in node]
    if not isinstance(node, dict):
        return node
    if node == G2:
        return copy.deepcopy(node)
    if is_cat_yes(node, IC2):
        return {"op": "any", "args": [copy.deepcopy(G3), copy.deepcopy(node)]}
    if node.get("op") == "any":
        args: list[Any] = []
        inserted = False
        for item in node["args"]:
            if not inserted and (item == G2 or is_cat_yes(item, IC2)):
                args.append(copy.deepcopy(G3))
                inserted = True
                args.append(copy.deepcopy(item))
            elif item == G2 or is_cat_yes(item, IC2):
                args.append(copy.deepcopy(item))
            else:
                args.append(widen3(item))
        return {**{k: widen3(v) for k, v in node.items() if k != "args"}, "args": args}
    return {k: widen3(v) for k, v in node.items()}


IC2_READERS = [
    *(f"rule.f1099b-noncovered-{t}-{k}-subtotal.v2.json" for t in TERMS for k in KINDS),
    *(f"rule.f8949-no1099b-{t}-{k}-subtotal.json" for t in TERMS for k in KINDS),
    "rule.schedule-d-line2.v2.json", "rule.schedule-d-line9.v2.json",
    "rule.schedule-d-line3.json", "rule.schedule-d-line10.json",
    "rule.schedule-d-line1a-gain.v5.json", "rule.schedule-d-line8a-gain.v6.json",
    "rule.selected-preferential-base.v8.json",
]


def bump(version: str) -> str:
    return f"v{int(version[1:]) + 1}"


def file_for(name: str, version: str) -> str:
    stem = name.removesuffix(".json")
    stem = stem.rsplit(".v", 1)[0] if stem.rsplit(".v", 1)[-1].isdigit() else stem
    return f"{stem}.{version}.json"


def ic2_successor(name: str) -> dict[str, Any]:
    body = read(name)
    new = widen3(body)
    assert new != body, name
    new["version"] = bump(body["version"])
    new["notes"] = body.get("notes", "") + (f" {new['version']}: the form8949-code-b-in-class answer admits the "
                                             "return as the v80 answer does, read only when the code B answer is yes.")
    return new


def attachment_f8949() -> dict[str, Any]:
    body = read("attachment.f8949.v4.json")
    body["version"] = "v5"
    body["title"] = ("Form 8949 attachment v5: the v4 parts, plus box A and box D rows with code B (column (e) the "
                     "basis shown on Form 1099-B, column (g) the basis correction and any wash-sale adjustment).")
    parts = list(body["itemizations"])
    for part in body["itemizations"]:
        pid = part["part_id"]
        if not (pid.startswith("box-a-") or pid.startswith("box-d-")):
            continue
        term = "st" if pid.startswith("box-a-") else "lt"
        kind = pid.split("-")[-1]
        clone = swap(copy.deepcopy(part), P + f"f1099b.covered-w-{term}-{kind}", fam(term, kind))
        clone = swap(clone, P + f"f1099b.covered-w-{term}-txn.{kind}", member_fact(term, kind))
        clone = swap(clone, P + f"f1099b.covered-w-{term}-{kind}-subtotal", subtotal(term, kind))
        clone = swap(clone, "v2", "v1")
        clone["part_id"] = f"box-{BOX[term].lower()}-code-b-{kind}"
        label = {"proceeds": "proceeds", "basis": "basis shown on Form 1099-B",
                 "adjustment": "basis correction plus any wash-sale adjustment"}[kind]
        col = {"proceeds": "d", "basis": "e", "adjustment": "g"}[kind]
        clone["label"] = f"Part {PART[term]} box {BOX[term]} column ({col}), code B: {WORD[term]} {label}"
        assert "covered-w" not in json.dumps(clone), clone
        parts.append(clone)
    body["itemizations"] = parts
    subs = list(body["requirement"]["subtotals"])
    for term in TERMS:
        subs += [subtotal(term, "proceeds"), subtotal(term, "basis"), gain(term)]
        if "attachments_read_count" in REPAIRS:
            subs.append(count_symbol(term))
    subs += attachment_reads() + f8949_reads()
    body["requirement"]["subtotals"] = subs
    return body


def attachment_schedule_d() -> dict[str, Any]:
    body = read("attachment.schedule-d.v8.json")
    body["version"] = "v9"
    body["title"] = ("Schedule D attachment v9: the v8 requirement, plus the box A and D code B proceeds and basis "
                     "subtotals and their column (h), so a code B sale requires it.")
    subs = list(body["requirement"]["subtotals"])
    for term in TERMS:
        subs += [subtotal(term, "proceeds"), subtotal(term, "basis"), gain(term)]
        if "attachments_read_count" in REPAIRS:
            subs.append(count_symbol(term))
    subs += attachment_reads() + schedule_d_reads()
    body["requirement"]["subtotals"] = subs
    return body


def form_field(term: str) -> dict[str, Any]:
    body = read(f"schedule-d.line-{LINE[term]}.form-field.v2.json")
    body["version"] = "v3"
    w, box, n = WORD[term], BOX[term], LINE[term]
    d = body["dispositions"]
    d["published_value"]["explain"] = (f"Schedule D line {n}, column (h), is your {w} gain or loss from Form 8949 box "
                                       f"{box}, proceeds minus basis plus adjustments. Column (g) carries any wash-sale "
                                       "adjustment and any code B correction of a wrong reported basis.")
    # Review S1: under a code B "yes" an empty term computes zero, so the sentence covers no sales too.
    d["computed_zero"]["explain"] = (f"Schedule D line {n}, column (h), is zero: no {w} Form 8949 box {box} sales "
                                     "with a wash-sale adjustment or a wrong reported basis are recorded, or their "
                                     "proceeds, basis, and adjustments net to zero.")
    d["closure_backed_zero"]["explain"] = (f"You said you have no {w} Form 8949 box {box} sales with a wash-sale "
                                           "adjustment or a wrong reported basis, so Schedule D line "
                                           f"{n}, column (h), is zero.")
    if "field_words" in REPAIRS:
        # Review S2: a refused sale waits for nothing, so the sentence names the checks and the refusals.
        d["blocked"]["explain"] = (f"Schedule D line {n}, column (h), has no value yet. It is waiting for your Form 8949 "
                                   f"box {box} proceeds, basis, and adjustments, including the column (g) correction of "
                                   "any sale whose reported basis is wrong, and your answers about those sales, or for "
                                   "each sale recorded there to pass its checks (the column (g) of a sale whose "
                                   "reported basis is wrong must equal the basis shown minus the correct basis, plus "
                                   "any wash-sale loss disallowed).")
    else:
        d["blocked"]["explain"] = (f"Schedule D line {n}, column (h), has no value yet. It is waiting for your Form 8949 "
                                   f"box {box} proceeds, basis, and adjustments, including the correct basis of any sale "
                                   "whose reported basis is wrong, and your answers about those sales.")
    if admission_wanted():
        d["blocked"]["explain"] += outside_words(term)
    return body


# ---- Track 1: the inherited v80 fixes (Decision 6) ----------------------------


def other_term(term: str) -> str:
    return "lt" if term == "st" else "st"


# The v80 Form 1099-B sale families, in the order the cross-term check follows.
V80_KINDS = ("covered", "covered-w", "noncovered")
V80_FAMILY_VERSION = {"covered": "v1", "covered-w": "v2", "noncovered": "v1"}
FLAG_PARAMETER = P + "parameter.f1099b-yes-no-flag"
# The other four flags of ADR-0052 Decision 1's eligible-sale predicate (review S5).
ELIGIBILITY_FLAGS = ("ordinary_indicated", "box_1f_market_discount", "qof_indicated", "collectibles_or_special_rate")


def v80_sale(kind: str, term: str) -> str:
    return P + f"f1099b.{kind}-{term}-txn"


def v80_family(kind: str, term: str) -> str:
    return P + f"f1099b.{kind}-{term}"


def counted_other_term(kind: str, term: str) -> list[tuple[str, str]]:
    """The other term's (sale fact, family) this family's sales are checked against."""
    other = other_term(term)
    return [(v80_sale(k, other), v80_family(k, other)) for k in V80_KINDS[:V80_KINDS.index(kind) + 1]]


def not_on_other_term(kind: str, term: str) -> list[dict[str, Any]]:
    """Per sale: no sale of the other term's checked families shares its identity.

    In a per-sale rule a count of another fact type that shares the sale's
    identity-key names counts only the rows on this sale's identity (the
    review S2 check of boxes C and F, and the code B sale's own check).
    """
    return [{"op": "compare", "cmp": "eq", "left": {"op": "count", "name": sale, "source_set": family}, "right": 0}
            for sale, family in counted_other_term(kind, term)]


def admission_fact(sale: str) -> str:
    return sale + ".admission"


def admission_check(sale: str) -> str:
    return sale + ".admission-check"


def admission_inert(sale: str) -> str:
    return sale + ".admission-check-inert-path-unwritten"


ADMITTED_KINDS = ("covered", "covered-w")


def admission_wanted() -> bool:
    return bool({"v80_cross_term_exclusive", "covered_tsa_blocks"} & REPAIRS)


def admission_bundle() -> dict[str, Any]:
    keys = sale_keys()
    domain = {"oneOf": [
        {"const": "admitted", "description": "The sale has no adjustment you make yourself and is recorded only once."},
        {"const": "taxpayer-side-adjustment",
         "description": "The sale is flagged with an adjustment you make yourself, which this return does not compute."},
        {"const": "recorded-twice", "description": "The same transaction is also recorded as a sale of the other term."},
    ]}
    if "covered_flags_block" in REPAIRS:
        domain["oneOf"].append({"const": "flagged-outside-class", "description": (
            "The sale is flagged as ordinary income, market discount, a qualified opportunity fund investment, or a "
            "collectibles or other special-rate gain, which this return does not compute.")})
    facts: list[dict[str, Any]] = []
    for kind in ADMITTED_KINDS:
        for term in TERMS:
            sale = v80_sale(kind, term)
            what = f"{WORD[term]} " + ("Form 1099-B sale reported on line " + ("1a" if term == "st" else "8a")
                                       if kind == "covered" else f"code W sale in box {BOX[term]}")
            facts.append(cfp.fact(admission_fact(sale), f"Whether one {what} is admitted to this return.", domain, keys))
            facts.append(cfp.fact(admission_inert(sale), "Never recorded; the second selection path the selection shape "
                                  "requires.", {"type": "boolean"}, [{"name": "tax-year", "kind": "literal", "values": ["2025"]}]))
    return {"schema": "bundle.v2", "id": P + "f1099b.covered-admission.vocabulary", "version": "v1",
            "label": "Whether each covered or code W Form 1099-B sale is admitted to this return", "fact_types": facts}


def flag_parameter() -> dict[str, Any]:
    body = read("parameter.default-zero.json")
    return {"schema": body["schema"], "id": FLAG_PARAMETER, "version": "v1", "scope": copy.deepcopy(body["scope"]),
            "values": {"yes": "1", "no": "0"}}


def admission_rule(kind: str, term: str) -> dict[str, Any]:
    """Per covered or code W sale: refused when any of the five eligibility flags is yes, or when recorded under both terms."""
    sale = v80_sale(kind, term)
    lit = lambda v: {"op": "category_literal", "fact_type": {"id": admission_fact(sale), "version": "v1"}, "value": v}  # noqa: E731
    value: dict[str, Any] = lit("admitted")
    notes = []
    if "v80_cross_term_exclusive" in REPAIRS:
        value = {"op": "choose", "when": {"op": "all", "args": not_on_other_term(kind, term)}, "then": value,
                 "else": lit("recorded-twice")}
        notes.append("A sale whose transaction is also recorded on the other term's "
                     + ", ".join(f.removeprefix(P + "f1099b.") for _s, f in counted_other_term(kind, term))
                     + " family is recorded twice.")
    def flagged(name: str) -> dict[str, Any]:
        flag = {"op": "parameter", "parameter_id": FLAG_PARAMETER, "key": {"op": "ref", "name": sale, "field": name}}
        return {"op": "compare", "cmp": "eq", "left": flag, "right": 1}

    if "covered_flags_block" in REPAIRS:
        value = {"op": "choose", "when": {"op": "any", "args": [flagged(name) for name in ELIGIBILITY_FLAGS]},
                 "then": lit("flagged-outside-class"), "else": value}
        notes.append("A sale flagged " + ", ".join(ELIGIBILITY_FLAGS) + " yes is outside the eligible-sale predicate.")
    if "covered_tsa_blocks" in REPAIRS:
        value = {"op": "choose", "when": flagged("taxpayer_side_adjustment"),
                 "then": lit("taxpayer-side-adjustment"), "else": value}
        notes.append("A sale flagged taxpayer_side_adjustment yes needs an adjustment this return does not compute.")
    return {
        "schema": "rule-artifact.v15", "id": sale.replace(P, P + "rule.") + ".admission", "version": "v1",
        "scope": read("rule.schedule-d-line2.json")["scope"], "role": "computation",
        "subject": {"id": sale, "version": "v1"}, "requires": [sale], "pins": [], "when": True, "value": value,
        "publishes": admission_fact(sale), "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}, "citations": [],
        "notes": " ".join(notes),
    }


def admission_check_rule(kind: str, term: str) -> dict[str, Any]:
    """Return level: 0 when every sale is admitted or none is recorded; else block (cfp.check_rule's shape)."""
    sale, family = v80_sale(kind, term), v80_family(kind, term)
    body = cfp.check_rule(sale, family)
    body = swap(body, cfp.agree_fact(sale), admission_fact(sale))
    body = swap(body, cfp.check_symbol(sale), admission_check(sale))
    body = swap(body, cfp.inert_fact(sale), admission_inert(sale))
    body = swap(body, sale.removeprefix(P) + "-amounts-check-conflict", sale.removeprefix(P) + "-admission-check-conflict")
    body = swap(body, "agree", "admitted")
    body["id"] = sale.replace(P, P + "rule.") + ".admission-check"
    for path in body["selection"]["paths"]:
        if path["id"] == "sales":
            path["activity"]["source_family"]["version"] = V80_FAMILY_VERSION[kind]
    body["notes"] = ("Blocks unless every recorded sale is admitted: no adjustment you make yourself, no flag for "
                     "ordinary income, market discount, a qualified opportunity fund or a special-rate gain, and not "
                     "also recorded as a sale of the other term.")
    assert "amounts" not in json.dumps(body), body["id"]
    return body


def noncovered_agree_successor(term: str) -> dict[str, Any]:
    body = read(f"rule.f1099b.noncovered-{term}-txn.amounts-agree.json")
    body["version"] = "v2"
    body["value"]["when"]["args"] = [*body["value"]["when"]["args"], *not_on_other_term("noncovered", term)]
    body["notes"] += (" v2: a sale whose transaction is also recorded on the other term's covered, code W or "
                      "noncovered family disagrees, so one transaction is never counted twice.")
    return body


def v80_count_symbol(kind: str, term: str) -> str:
    return P + f"f1099b.{kind}-{term}-count"


def v80_count_rule(kind: str, term: str) -> dict[str, Any]:
    body = count_rule(term)
    body["id"] = P + f"rule.f1099b-{kind}-{term}-count"
    body["publishes"] = v80_count_symbol(kind, term)
    body["blocked"] = {"code": "SOURCE_SET_UNCLOSED", "missing": [v80_family(kind, term)]}
    body["value"] = {"op": "count", "name": v80_sale(kind, term), "source_set": v80_family(kind, term)}
    if kind == "covered":
        body["notes"] = (f"The number of {WORD[term]} Form 1099-B sales reported directly on Schedule D line "
                         f"{'1a' if term == 'st' else '8a'}. Schedule D is required when it is above zero, so a sale "
                         "with zero proceeds is still reported.")
        return body
    what = f"code W sales in box {BOX[term]}" if kind == "covered-w" else \
        f"box {'B' if term == 'st' else 'E'} sales whose basis was not reported to the IRS"
    body["notes"] = (f"The number of {WORD[term]} {what}. Both attachments are required when it is above zero, so a "
                     "sale with zero proceeds is still reported.")
    return body


def count_kinds() -> list[str]:
    return [k for k, switch in (("covered-w", "w_zero_proceeds"), ("noncovered", "b_zero_proceeds")) if switch in REPAIRS]


def count_rule_kinds() -> list[str]:
    """Every v80 family that gets a count rule: the attachment counts, and the direct counts of B1."""
    return [*(["covered"] if "direct_zero_proceeds" in REPAIRS else []), *count_kinds()]


def attachment_reads() -> list[str]:
    """The Track 1 symbols both attachments read (each is 0 or a count; a block blocks the attachment)."""
    out = [v80_count_symbol(kind, term) for kind in count_kinds() for term in TERMS]
    return out


def schedule_d_reads() -> list[str]:
    """Schedule D also reads the line 1a and 8a sale counts (B1); a direct sale needs no Form 8949."""
    if "direct_zero_proceeds" not in REPAIRS:
        return []
    return [v80_count_symbol("covered", term) for term in TERMS]


LINE_7A_ACTIVITY = (P + "schedule-d.line-1a-gain", P + "schedule-d.line-8a-gain")


def line7a_successor() -> dict[str, Any]:
    """Form 1040 line 7a v8: a nonzero line 1a or 8a is Schedule D activity (B1).

    v7 tests the covered proceeds subtotals, which are zero for a direct sale
    with zero proceeds, so such a sale's loss on line 1a or 8a never reached
    line 7a.
    """
    body = read("rule.form1040-line7a.v7.json")
    body["version"] = "v8"
    arms = [{"op": "compare", "cmp": "ne", "left": {"op": "ref", "name": name}, "right": 0} for name in LINE_7A_ACTIVITY]
    body["value"]["when"]["args"] = [*body["value"]["when"]["args"], *arms]
    body["requires"] = [*body["requires"], *LINE_7A_ACTIVITY]
    body["blocked"]["missing"] = [*body["blocked"]["missing"], *LINE_7A_ACTIVITY]
    body["notes"] += (" v8: a nonzero line 1a or line 8a is Schedule D activity, so a direct sale with zero proceeds "
                      "reaches line 7a.")
    return body


def f8949_reads() -> list[str]:
    """Form 8949 also reads the line 1a and 8a admission checks, so a refused direct sale blocks it."""
    if not admission_wanted():
        return []
    return [admission_check(v80_sale("covered", term)) for term in TERMS]


LINE_1A_8A = {"st": ("rule.schedule-d-line1a-gain.v5.json", "schedule-d.line-1a.form-field.v2.json"),
              "lt": ("rule.schedule-d-line8a-gain.v6.json", "schedule-d.line-8a.form-field.json")}


def checked_line(body: dict[str, Any], symbols: list[str]) -> dict[str, Any]:
    """A line successor that also requires the admission checks of the sales it sums."""
    body["requires"] = [*body["requires"], *symbols]
    body["notes"] = body.get("notes", "") + (" It also requires the admission check of each sale it sums, so a sale "
                                             "flagged with an adjustment you make yourself, or recorded under both "
                                             "terms, blocks the line.")
    return body


def outside_words(term: str) -> str:
    """The refusals each line 1a, 8a, 1b and 8b blocked sentence names (review S2, S4 and S5)."""
    other = WORD[other_term(term)]
    flags = (" a sale flagged as ordinary income, market discount, a qualified opportunity fund investment, or a "
             "collectibles or other special-rate gain," if "covered_flags_block" in REPAIRS else "")
    return (f" A sale your answers place outside this return,{flags} and a sale also recorded as a {other} sale are "
            "outside what this return computes. So is a sale with an adjustment you make yourself, unless the "
            "adjustment corrects a wrong basis the Form 1099-B reported; record that sale as a sale whose reported "
            "basis is wrong.")



def direct_field(term: str) -> dict[str, Any]:
    body = read(LINE_1A_8A[term][1])
    body["version"] = bump(body["version"])
    n = "1a" if term == "st" else "8a"
    d = body["dispositions"]
    if term == "lt":
        # Review S3: line 8a in line 1a's plain words.
        d["published_value"]["explain"] = ("Schedule D line 8a, column (h), is long-term proceeds minus basis for the "
                                           "sales you report directly on Schedule D.")
        d["computed_zero"]["explain"] = ("Schedule D line 8a, column (h), is zero because your long-term proceeds "
                                         "equal your basis.")
        d["closure_backed_zero"]["explain"] = ("You said you have no long-term sales reported directly on Schedule D, "
                                               "so line 8a, column (h), is zero.")
    d["blocked"]["explain"] = (
        f"Schedule D line {n}, column (h), has no value yet. It is waiting for your {WORD[term]} proceeds and basis, "
        f"or for each sale recorded there to pass its checks." + outside_words(term))
    return body


# ---- the successor set ---------------------------------------------------------


ROLE = {"parameter-declaration.v1": "parameter", "bundle.v2": "fact-type-bundle", "source-family.v2": "source-family",
        "source-closure-mapping.v4": "source-closure-mapping", "citation.v1": "citation",
        "form-field.v3": "form-field", "attachment-rule.v8": "attachment-rule", "input-question.v1": "input-question"}


def artifacts() -> tuple[list[tuple[str, dict[str, Any]]], dict[tuple[str, str], tuple[str, str]]]:
    out: list[tuple[str, dict[str, Any]]] = [
        ("f1099b-code-b-st.bundle.json", bundle("st")),
        ("f1099b-code-b-lt.bundle.json", bundle("lt")),
        ("schedule-d-boundary-form8949-code-b-in-class.bundle.json", boundary_bundle()),
        ("closure-mapping.f1099b-code-b.json", mapping()),
        *questions(),
    ]
    for term in TERMS:
        for kind in (None, *KINDS):
            out.append((f"family.f1099b-code-b-{term}" + (f"-{kind}" if kind else "") + ".json", family(term, kind)))
        for kind in KINDS:
            out.append((f"rule.f1099b-code-b-{term}-{kind}-subtotal.json", subtotal_rule(term, kind)))
        slug = member_fact(term, None).removeprefix(P)
        out.append((f"rule.{slug}.amounts-agree.json", agree_rule(term)))
        out.append((f"rule.{slug}.amounts-check.json", check_rule(term)))
        out.append((f"rule.f1099b-code-b-{term}-gain.json", gain_rule(term)))
        if "attachments_read_count" in REPAIRS:
            out.append((f"rule.f1099b-code-b-{term}-count.json", count_rule(term)))
    for kind in count_rule_kinds():
        for term in TERMS:
            out.append((f"rule.f1099b-{kind}-{term}-count.json", v80_count_rule(kind, term)))
    if admission_wanted():
        out.append(("f1099b-covered-admission.bundle.json", admission_bundle()))
        if "covered_tsa_blocks" in REPAIRS:
            out.append(("parameter.f1099b-yes-no-flag.json", flag_parameter()))
        for kind in ADMITTED_KINDS:
            for term in TERMS:
                slug = v80_sale(kind, term).removeprefix(P)
                out.append((f"rule.{slug}.admission.json", admission_rule(kind, term)))
                out.append((f"rule.{slug}.admission-check.json", admission_check_rule(kind, term)))
    old: dict[tuple[str, str], tuple[str, str]] = {}

    def replaced(prior_name: str, body: dict[str, Any]) -> None:
        prior = read(prior_name)
        old[(body["id"], body["version"])] = (prior["version"], prior["schema"])
        out.append((file_for(prior_name, body["version"]), body))

    for name in IC2_READERS:
        body = ic2_successor(name)
        for term, (rule_name, _field) in LINE_1A_8A.items():
            if name == rule_name and admission_wanted():
                body = checked_line(body, [admission_check(v80_sale("covered", term))])
        replaced(name, body)
    if "v80_cross_term_exclusive" in REPAIRS:
        for term in TERMS:
            replaced(f"rule.f1099b.noncovered-{term}-txn.amounts-agree.json", noncovered_agree_successor(term))
    if admission_wanted():
        for term in TERMS:
            replaced(LINE_1A_8A[term][1], direct_field(term))
    for term in TERMS:
        replaced(f"rule.schedule-d-line{LINE[term]}.v2.json", line_successor(term))
        replaced(f"schedule-d.line-{LINE[term]}.form-field.v2.json", form_field(term))
    replaced("attachment.f8949.v4.json", attachment_f8949())
    replaced("attachment.schedule-d.v8.json", attachment_schedule_d())
    if "direct_zero_proceeds" in REPAIRS:
        replaced("rule.form1040-line7a.v7.json", line7a_successor())
    return out, old


def companion_v81() -> None:
    """Track 1's two loader entries for v81, applied in process."""
    if getattr(loader, "_codeb_patched", False):
        return
    original_decl = loader.domain_package_companion_declarations
    original_refusal = loader.named_covered_flag_refusal_maps

    def declarations() -> dict[tuple[str, str], dict[str, Any]]:
        found = dict(original_decl())
        v80 = found[(PKG, "v80")]
        pairs = dict(v80["presence_pairs"])
        for term in TERMS:
            for kind in KINDS:
                pairs[member_fact(term, kind)] = member_fact(term, None)
        found[(PKG, "v81")] = {"presence_pairs": pairs, "value_domains": dict(v80["value_domains"])}
        return found

    def refusal() -> dict[tuple[str, str], dict[str, str]]:
        found = dict(original_refusal())
        found[(PKG, "v81")] = dict(found[(PKG, "v80")])
        return found

    loader.domain_package_companion_declarations = declarations  # type: ignore[assignment]
    loader.named_covered_flag_refusal_maps = refusal  # type: ignore[assignment]
    loader._codeb_patched = True  # type: ignore[attr-defined]


V81_FILES = ("package.core-calculations.v81.json", "published-packages.v79.json")
V81_RELEASE_FILES = ("demo.release.sli-worksheet-integration.2025.v79.json",)


def published_names() -> list[str]:
    """The member files the published v81 has (every switch on), whatever REPAIRS this build uses."""
    saved = set(REPAIRS)
    try:
        REPAIRS.clear()
        REPAIRS.update(ALL_REPAIRS)
        return [name for name, _ in artifacts()[0]]
    finally:
        REPAIRS.clear()
        REPAIRS.update(saved)


def digest(folder: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.glob("*.json"))}


def build(scratch: Path, *, rules_dir: Path | None = None) -> dict[str, Any]:
    source_content, source_releases = ORIGIN
    content, releases = scratch / "content", scratch / "releases"
    shutil.copytree(source_content, content)
    shutil.copytree(source_releases, releases)
    bodies, old = artifacts()
    # This branch publishes core v81 in place (Track 1, rebuilt by the review
    # repair). The scratch build starts from v80: the published v81 package,
    # registry v79, release v79 and every v81 member body are removed from the
    # copy first. artifacts() reads only their predecessors.
    for name in (*(n for n, _ in bodies), *published_names(), *V81_FILES):
        (content / name).unlink(missing_ok=True)
    for name in V81_RELEASE_FILES:
        (releases / name).unlink(missing_ok=True)
    for missing in ("package.core-calculations.v81.json", "published-packages.v79.json"):
        assert not (content / missing).exists(), missing
    assert not (releases / "demo.release.sli-worksheet-integration.2025.v79.json").exists()
    before = digest(content)
    members, entrypoints = [], []
    pinned = json.loads((content / "package.core-calculations.v80.json").read_text(encoding="utf-8"))
    entry_keys = {(e["id"], e["version"]) for e in pinned["entrypoints"]}
    if rules_dir is not None:
        rules_dir.mkdir(parents=True, exist_ok=True)
    for name, body in bodies:
        if (content / name).exists():
            raise AssertionError(f"{name} already exists")
        text = json.dumps(body, indent=2) + "\n"
        (content / name).write_text(text, encoding="utf-8")
        if rules_dir is not None:
            (rules_dir / name).write_text(text, encoding="utf-8")
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
    changes = {"package_version": "v81", "release_version": "v79", "members": members, "entrypoints": entrypoints,
               "registry_sort": "id_version", "registry_new_key_order": ["checksum", "id", "version"]}
    (scratch / "changes.json").write_text(json.dumps(changes, indent=2) + "\n", encoding="utf-8")
    report = generate_to_directory(
        content / "package.core-calculations.v80.json",
        content / "published-packages.v78.json",
        releases / "demo.release.sli-worksheet-integration.2025.v78.json",
        content, scratch / "changes.json", scratch / "out",
    )
    for name, folder, target in (
        ("package.json", content, "package.core-calculations.v81.json"),
        ("registry.json", content, "published-packages.v79.json"),
        ("release.json", releases, "demo.release.sli-worksheet-integration.2025.v79.json"),
    ):
        shutil.copy(scratch / "out" / name, folder / target)
    after = digest(content)
    companion_v81()
    probe.CONTENT, probe.RELEASE_DIR = content, releases
    return {
        "package": report.get("package"), "release": report.get("release"),
        "members_edited": len(members), "added_members": sum(1 for m in members if m["op"] == "add"),
        "replaced_members": sum(1 for m in members if m["op"] == "replace"),
        "members": [[m["op"], m["new"]["id"].removeprefix(P), m["new"]["version"]] for m in members],
        "inherited_inconsistencies": [list(r) for r in (report.get("inherited_inconsistencies") or ())],
        "existing_files_changed": sorted(n for n in before if after.get(n) != before[n]),
        "files_added": len([n for n in after if n not in before]),
    }


def publish() -> None:
    """Write the v81 member bodies, package v81, registry v79 and release v79 into the repository.

    Core v81 is unmerged, so it is rebuilt in place: the scratch build (from
    v80, with every REPAIRS switch on) is copied over the published files.
    tests/test_code_b_sales_v81_package.py then holds them to the prototype
    byte for byte.
    """
    assert REPAIRS == set(ALL_REPAIRS), sorted(REPAIRS)
    codeb_probe.pin_v80()
    ORIGIN[:] = [probe.CONTENT, probe.RELEASE_DIR]
    content, releases = ORIGIN
    with tempfile.TemporaryDirectory() as tmp:
        scratch = Path(tmp).resolve() / "scratch"
        build(scratch)
        bodies, _old = artifacts()
        names = [n for n, _ in bodies]
        for name in (*names, *V81_FILES):
            shutil.copy(scratch / "content" / name, content / name)
        for name in V81_RELEASE_FILES:
            shutil.copy(scratch / "releases" / name, releases / name)
    print("published", len(names), "member bodies, package v81, registry v79 and release v79")


def pin(version: str) -> None:
    if version == "v81":
        probe.PACKAGE, probe.PACKAGE_VERSION = "package.core-calculations.v81.json", "v81"
        probe.REGISTRY, probe.RELEASE, probe.RELEASE_VERSION = (
            "published-packages.v79.json", "demo.release.sli-worksheet-integration.2025.v79.json", "v79")
    else:
        cfp.pin("v80")


# ---- recording -------------------------------------------------------------------


BUNDLES: dict[str, dict[str, Any]] = {}


def open_codeb(acts: Acts) -> None:
    for term in TERMS:
        cp.proto._adopt(acts, BUNDLES.setdefault(term, bundle(term)))
    cp.proto._adopt(acts, BUNDLES.setdefault("boundary", boundary_bundle()))
    for term in TERMS:
        for kind in (None, *KINDS):
            slug = fam(term, kind).removeprefix(P + "f1099b.")
            probe._add(acts, "horizon-genesis", {
                "family": {"id": fam(term, kind), "version": "v1"},
                "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
                "horizon_id": f"demo.cb.{slug}.h0",
            })


def record(acts: Acts, term: str, kind: str | None, value: object, tag: str, *, long_term_family: str | None = None) -> None:
    family_id = fam(long_term_family or term, kind)
    declared: list[tuple[str, str]] = []
    for key in sale_keys():
        if key["kind"] == "entity":
            entity = f"demo.ns.{tag}.{key['name']}"  # probe.record's entity names, so a tag reused there is the same sale
            if not cp.proto._known_entity(acts, entity):
                probe._introduce(acts, entity, key["entity_kind"])
            declared.append((key["name"], entity))
        else:
            declared.append((key["name"], key["values"][0]))
    head = probe.horizons(acts, family_id)[-1]
    slug = family_id.removeprefix(P + "f1099b.")
    successor_id = f"demo.cb.{tag}.{slug}.h{len(probe.horizons(acts, family_id))}"
    probe._add(acts, "member-transition", {
        "family": {"id": family_id, "version": "v1"},
        "scope": {"tax-year": probe.YEAR, "subject": "demo.primary"},
        "member": {"action": "assert", "finding": _attested(
            f"demo.cb.{tag}.{slug}.member", fact_id_for(member_fact(long_term_family or term, kind), tuple(declared)),
            value)},
        "successor": {"id": successor_id, "predecessor": head},
    })


def code_b(acts: Acts, term: str, proceeds: float, shown: float, corrected: float | None, tag: str, *,
           wash: float = 0.0, rows: tuple[str, ...] = KINDS, g: float | None = None, long_term: str | None = None) -> None:
    """One code B sale: the sale, and its proceeds, basis-shown and column (g) rows."""
    value: dict[str, Any] = {"proceeds": proceeds, "basis": shown, "long_term": long_term or ("yes" if term == "lt" else "no"),
                             "wash_disallowed": wash}
    if corrected is not None:
        value["corrected_basis"] = corrected
    record(acts, term, None, value, tag)
    amounts = {"proceeds": proceeds, "basis": shown,
               "adjustment": g if g is not None else shown - (corrected if corrected is not None else shown) + wash}
    for kind in KINDS:
        if kind in rows:
            record(acts, term, kind, amounts[kind], tag)


def say(acts: Acts, fact_type: str, value: str, tag: str) -> Acts:
    return cfp.say(acts, fact_type, value, tag)


def v81_return(*, q3: str | None = "no", ic3: str | None = None, sales: Callable[[Acts], Any] | None = None,
               **v80: Any) -> Acts:
    """A harness return with the noncovered, no-1099-B and code B families open.

    Sales are recorded first, then every answer, so no group answer is stale.
    """
    def opened(acts: Acts) -> Acts | None:
        open_codeb(acts)
        return sales(acts) if sales is not None else None

    acts = cfp.v80_return(sales=opened, **v80)
    if q3 is not None:
        acts = say(acts, Q3, q3, "q3")
    if ic3 is not None:
        acts = probe.answer(ccr._renumbered(acts), IC3, ic3, "ic3")
    return ccr._renumbered(acts)


def with_q3(acts: Acts, answer: str | None) -> Acts:
    out = copy.deepcopy(acts)
    open_codeb(out)
    if answer is not None:
        say(out, Q3, answer, "q3carry")
    return ccr._renumbered(out)


# ---- cases -------------------------------------------------------------------------


CLS = {"q1": "no", "q2": "no", "q3": "yes", "form8949": "no", "path_b": "no", "ic3": "yes"}


def new_cases() -> dict[str, Callable[[], Acts]]:
    def ret(fn: Callable[[Acts], Any] | None = None, **kw: Any) -> Callable[[], Acts]:
        return lambda: v81_return(sales=fn, **{**CLS, **kw})

    a_high = lambda a: code_b(a, "st", 10000.0, 7000.0, 4000.0, "ahigh")  # noqa: E731
    d_low = lambda a: code_b(a, "lt", 6000.0, 2000.0, 3000.0, "dlow")  # noqa: E731

    def mixed(acts: Acts) -> Acts:
        a_high(acts)
        d_low(acts)
        cfp.cf_sale(acts, "st", 2500.0, 1000.0, "mxc")
        return codeb_probe.direct(ccr._renumbered(acts), "st", 5000.0, 4000.0, "mxa")

    def with_w_row(acts: Acts) -> Acts:
        a_high(acts)
        return codeb_probe.wash(ccr._renumbered(acts), "st", 4000.0, 5000.0, 300.0, "ww")

    def duplicate(acts: Acts) -> Acts:
        a_high(acts)
        sale = probe.txn(proceeds=10000.0, basis=7000.0, long_term="no", reported="yes", covered="yes")
        return probe.record(ccr._renumbered(acts), P + "f1099b.covered-st", sale, "ahigh")

    def b_on_b(acts: Acts) -> None:
        cp.on_be(acts, "st", 3000.0, 1000.0, "bcb")

    def late(answer_after: str | None) -> Callable[[], Acts]:
        def build() -> Acts:
            acts = v81_return(**{**CLS, "q3": "no"})
            a_high(acts)
            if answer_after is not None:
                acts = say(acts, Q3, answer_after, "q3again")
            return ccr._renumbered(acts)
        return build

    return {
        "wage_q3_no": lambda: v81_return(),
        "wage_q3_unanswered": lambda: v81_return(q3=None),
        "a_high": ret(a_high),
        "d_low": ret(d_low),
        "a_gain_to_loss": ret(lambda a: code_b(a, "st", 5000.0, 3000.0, 9000.0, "aloss")),
        "a_bw": ret(lambda a: code_b(a, "st", 4000.0, 4500.0, 6000.0, "abw", wash=1000.0)),
        "d_bw": ret(lambda a: code_b(a, "lt", 7000.0, 7500.0, 9000.0, "dbw", wash=500.0)),
        "mixed_a_d_c_direct": ret(mixed, q2="yes"),
        "a_high_and_w_row": ret(with_w_row),
        # Box B with a wrong basis shown but not reported: the v80 box B route, correct basis in (e).
        "b_code_b_v80_route": lambda: v81_return(sales=b_on_b, q1="yes", q2="no", q3="no", form8949="no",
                                                 path_b="no", old_ic="yes"),
        "b_code_b_ic3": lambda: v81_return(sales=b_on_b, q1="yes", q2="no", q3="no", form8949="no",
                                           path_b="no", old_ic="no", new_ic="no", ic3="yes"),
        "a_proceeds_row_missing": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, 4000.0, "nop", rows=("basis", "adjustment"))),
        "a_basis_row_missing": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, 4000.0, "nob", rows=("proceeds", "adjustment"))),
        "a_adjustment_row_missing": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, 4000.0, "noa", rows=("proceeds", "basis"))),
        "a_corrected_basis_missing": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, None, "nocb")),
        "a_no_correction": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, 7000.0, "same")),
        "a_g_disagrees": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, 4000.0, "gbad", g=2000.0)),
        "a_w_on_gain_after_correction": ret(lambda a: code_b(a, "st", 5000.0, 6000.0, 3000.0, "wgain", wash=500.0)),
        "a_w_exceeds_corrected_loss": ret(lambda a: code_b(a, "st", 4000.0, 4500.0, 5000.0, "wbig", wash=1500.0)),
        "a_holding_mismatch": ret(lambda a: code_b(a, "st", 10000.0, 7000.0, 4000.0, "hold", long_term="yes")),
        "a_same_sale_both_terms": ret(lambda a: [code_b(a, "st", 10000.0, 7000.0, 4000.0, "both"),
                                                code_b(a, "lt", 10000.0, 7000.0, 4000.0, "both")] and None),
        "a_duplicate_on_direct": ret(duplicate),
        "a_ic3_no": ret(a_high, ic3="no"),
        "a_ic3_unanswered": ret(a_high, ic3=None),
        "a_8949_yes": ret(a_high, form8949="yes", path_b=None),
        "a_path_b_unanswered": ret(a_high, path_b=None),
        "a_q3_no_with_member": ret(a_high, q3="no"),
        "q3_yes_nothing_recorded": ret(None),
        "late_member_after_no": late(None),
        "late_member_reanswered_yes": late("yes"),
    }


# Hand values (p0-law-state-design.md). Single, wages 50,000, standard deduction:
# taxable income 34,250 before capital gains, tax 3,875.
ATT_PUB = ("published", "published")
HAND: dict[str, dict[str, Any]] = {
    "wage_q3_no": {"form1040.line-15": 34250, "form1040.line-16": 3875, "form1040.line-7a": 0,
                   "schedule-d.line-1b": 0, "schedule-d.line-8b": 0, "attachments": ("guard_inapplicable", "guard_inapplicable")},
    "a_high": {"schedule-d.line-1b": 6000, "schedule-d.line-7": 6000, "schedule-d.line-16": 6000,
               "form1040.line-7a": 6000, "form1040.line-15": 40250, "form1040.line-16": 4595, "preferential": 0,
               "attachments": ATT_PUB},
    "d_low": {"schedule-d.line-8b": 3000, "schedule-d.line-15": 3000, "schedule-d.line-16": 3000,
              "form1040.line-7a": 3000, "form1040.line-15": 37250, "form1040.line-16": 3875, "preferential": 3000,
              "attachments": ATT_PUB},
    "a_gain_to_loss": {"schedule-d.line-1b": -4000, "schedule-d.line-7": -4000, "schedule-d.line-16": -4000,
                       "schedule-d.line-21": 3000, "form1040.line-7a": -3000, "form1040.line-15": 31250,
                       "form1040.line-16": 3515, "preferential": 0, "attachments": ATT_PUB},
    "a_bw": {"schedule-d.line-1b": -1000, "schedule-d.line-7": -1000, "schedule-d.line-16": -1000,
             "schedule-d.line-21": 1000, "form1040.line-7a": -1000, "form1040.line-15": 33250,
             "form1040.line-16": 3755, "preferential": 0, "attachments": ATT_PUB},
    "d_bw": {"schedule-d.line-8b": -1500, "schedule-d.line-15": -1500, "schedule-d.line-16": -1500,
             "schedule-d.line-21": 1500, "form1040.line-7a": -1500, "form1040.line-15": 32750,
             "form1040.line-16": 3695, "preferential": 0, "attachments": ATT_PUB},
    "mixed_a_d_c_direct": {"schedule-d.line-1a": 1000, "schedule-d.line-1b": 6000, "schedule-d.line-3": 1500,
                           "schedule-d.line-7": 8500, "schedule-d.line-8b": 3000, "schedule-d.line-15": 3000,
                           "schedule-d.line-16": 11500, "form1040.line-7a": 11500, "form1040.line-15": 45750,
                           "form1040.line-16": 4895, "preferential": 3000, "attachments": ATT_PUB},
    "a_high_and_w_row": {"schedule-d.line-1b": 5300, "schedule-d.line-7": 5300, "schedule-d.line-16": 5300,
                         "form1040.line-7a": 5300, "form1040.line-15": 39550, "form1040.line-16": 4511,
                         "preferential": 0, "attachments": ATT_PUB},
    "b_code_b_v80_route": {"schedule-d.line-2": 2000, "schedule-d.line-7": 2000, "schedule-d.line-16": 2000,
                           "form1040.line-7a": 2000, "form1040.line-15": 36250, "form1040.line-16": 4115,
                           "attachments": ATT_PUB},
}
HAND["late_member_reanswered_yes"] = dict(HAND["a_high"])
# Form 1040 lines 15 and 16 blocked; attachments (f8949, schedule-d); and the
# (disposition, code, missing) of the code B row that says why, when one does.
BLOCKED: dict[str, dict[str, Any]] = {
    "wage_q3_unanswered": {"attachments": ("blocked", "blocked"), "questions": [Q3_TEXT]},
    "a_proceeds_row_missing": {"attachments": ("blocked", "blocked"),
                               "row": ("f1099b-code-b-st-gain", ["blocked", "DEPENDENCY_ABSENT", ["f1099b.code-b-st-txn.proceeds"]])},
    "a_basis_row_missing": {"attachments": ("blocked", "blocked"),
                            "row": ("f1099b-code-b-st-gain", ["blocked", "DEPENDENCY_ABSENT", ["f1099b.code-b-st-txn.basis"]])},
    "a_adjustment_row_missing": {"attachments": ("blocked", "blocked"),
                                 "row": ("f1099b-code-b-st-gain", ["blocked", "DEPENDENCY_ABSENT", ["f1099b.code-b-st-txn.adjustment"]])},
    "a_no_correction": {"attachments": ("blocked", "blocked"), "constraint": "CODE_B_WITHOUT_CORRECTION"},
    "a_g_disagrees": {"attachments": ("blocked", "blocked"),
                      "row": ("f1099b.code-b-st-txn.amounts-check", ["blocked", "DEPENDENCY_INVALID", []])},
    "a_w_on_gain_after_correction": {"attachments": ("blocked", "blocked"), "constraint": "CODE_W_ON_GAIN"},
    "a_w_exceeds_corrected_loss": {"attachments": ("blocked", "blocked"), "constraint": "ADJUSTMENT_EXCEEDS_LOSS"},
    "a_holding_mismatch": {"attachments": ("blocked", "blocked"), "constraint": "HOLDING_PERIOD_MISMATCH"},
    "a_same_sale_both_terms": {"attachments": ("blocked", "blocked")},
    "a_duplicate_on_direct": {"attachments": ("blocked", "blocked")},
    # Refused by the code B in-class answer: each code B subtotal blocks on it, so the
    # column (h) row names the three subtotals.
    "a_ic3_no": {"attachments": ("blocked", "blocked"),
                 "row": ("f1099b-code-b-st-gain", ["blocked", "DEPENDENCY_ABSENT", [
                     "f1099b.code-b-st-proceeds-subtotal", "f1099b.code-b-st-basis-subtotal",
                     "f1099b.code-b-st-adjustment-subtotal"]])},
    "a_ic3_unanswered": {"attachments": ("blocked", "blocked"), "questions": [IC3_TEXT]},
    "a_8949_yes": {"attachments": ("blocked", "blocked"),
                   "row": ("f1099b-code-b-st-gain", ["blocked", "DEPENDENCY_ABSENT", []])},
    "a_path_b_unanswered": {"attachments": ("blocked", "blocked")},
    "a_q3_no_with_member": {"attachments": ("blocked", "blocked"), "questions": [Q3_TEXT]},
    "q3_yes_nothing_recorded": {"attachments": ("blocked", "blocked"),
                                "row": ("f1099b-code-b-st-gain", ["blocked", "DEPENDENCY_ABSENT", []])},
    "late_member_after_no": {"attachments": ("blocked", "blocked"), "questions": [Q3_TEXT]},
    # A box B code B filer who says both earlier in-class answers are false: the code B
    # answer is no (nothing was reported to the IRS), so the code B in-class answer is never read.
    "b_code_b_ic3": {"attachments": ("blocked", "blocked"),
                     "row": ("schedule-d-line2", ["blocked", "DEPENDENCY_ABSENT", [
                         "f1099b.noncovered-st-proceeds-subtotal", "f1099b.noncovered-st-basis-subtotal"]])},
}
QUESTION_FOR = {
    "a_proceeds_row_missing": "What are the proceeds shown on your Form 1099-B for each short-term sale you recorded whose reported basis is wrong?",
    "a_basis_row_missing": "What basis does your Form 1099-B show for each short-term sale you recorded whose reported basis is wrong?",
    "a_adjustment_row_missing": ("What is the column (g) adjustment for each short-term sale you recorded whose reported basis "
                                 "is wrong: the basis shown minus the correct basis, plus any wash-sale loss disallowed?"),
}
for _name, _text in QUESTION_FOR.items():
    BLOCKED[_name]["questions"] = [_text]
WATCH_ROWS = ("f1099b-code-b-st-gain", "f1099b-code-b-lt-gain", "f1099b.code-b-st-txn.amounts-check",
              "f1099b.code-b-lt-txn.amounts-check")


def check(name: str, result: dict[str, Any]) -> dict[str, Any]:
    """Compare a v81 run with the hand values. Returns the mismatches (empty is a pass)."""
    if name == "a_corrected_basis_missing":
        ok = result.get("error") == "FindingModelError" and "corrected_basis" in str(result.get("message"))
        return {} if ok else {"error": result.get("error"), "message": result.get("message")}
    if result.get("error"):
        return {"error": result.get("error"), "message": result.get("message")}
    lines = result.get("lines") or {}
    att = result.get("attachments") or {}
    got_att = (att.get("f8949"), att.get("schedule-d"))
    bad: dict[str, Any] = {}
    if not result.get("presentation_valid"):
        bad["presentation_valid"] = result.get("presentation_error")
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
        for key in ("form1040.line-15", "form1040.line-16"):
            if (lines.get(key) or [None])[0] == "blocked":
                bad[key + ".disposition"] = "blocked"
    elif name in BLOCKED:
        want = BLOCKED[name]
        for key in ("form1040.line-15", "form1040.line-16"):
            if (lines.get(key) or [None])[0] != "blocked":
                bad[key] = lines.get(key)
        if got_att != want["attachments"]:
            bad["attachments"] = {"want": want["attachments"], "got": got_att}
        if "row" in want:
            row_name, row_want = want["row"]
            if (result.get("rows") or {}).get(row_name) != row_want:
                bad["row"] = {"want": row_want, "got": (result.get("rows") or {}).get(row_name)}
        for text in want.get("questions", []):
            if text not in (result.get("questions") or []):
                bad["question"] = {"want": text, "got": result.get("questions")}
        if "constraint" in want:
            codes = [c for b in result.get("blocked") or [] if b["artifact"].endswith("member-validation.synthesized")
                     for c in b.get("missing") or []]
            if want["constraint"] not in codes:
                bad["constraint"] = {"want": want["constraint"], "got": codes}
    else:
        bad["unexpected"] = "case has no expectation"
    return bad


# ---- runs ----------------------------------------------------------------------------


codeb_probe.WHY_ROWS = codeb_probe.WHY_ROWS + tuple(P + "rule." + n for n in (*WATCH_ROWS, "schedule-d-line3", "schedule-d-line10"))
STATE: dict[str, Any] = {}


PARTS_KEPT = ("a_high", "mixed_a_d_c_direct")


def summarize_v81(result: dict[str, Any]) -> dict[str, Any]:
    keep = codeb_probe.keep(result)
    if "blocked" in keep:
        keep["blocked"] = keep["blocked"][:6]
    keep.pop("f8949_parts", None)
    return keep


def dump(payload: dict[str, Any]) -> str:
    """One line per case, so the file stays small and diffs stay readable."""
    out = ["{"]
    keys = sorted(payload)
    for i, key in enumerate(keys):
        end = "," if i < len(keys) - 1 else ""
        value = payload[key]
        if isinstance(value, dict) and key in ("v81_cases", "v80_returns_on_v81"):
            out.append(f" {json.dumps(key)}: {{")
            names = sorted(value)
            for j, name in enumerate(names):
                comma = "," if j < len(names) - 1 else ""
                out.append(f"  {json.dumps(name)}: {json.dumps(value[name], sort_keys=True)}{comma}")
            out.append(f" }}{end}")
        else:
            out.append(f" {json.dumps(key)}: {json.dumps(value, sort_keys=True)}{end}")
    out.append("}")
    return probe.scrub("\n".join(out)) + "\n"


def init() -> None:
    """Build the scratch v81 in this process (each worker builds its own)."""
    codeb_probe.pin_v80()
    ORIGIN[:] = [probe.CONTENT, probe.RELEASE_DIR]
    tmp = tempfile.mkdtemp(prefix="codeb-")
    STATE["tmp"] = tmp
    STATE["build"] = build(Path(tmp).resolve() / "scratch")
    import atexit

    atexit.register(shutil.rmtree, tmp, True)


def v80_world() -> dict[str, Callable[[], Acts]]:
    """Every return tests/test_no1099b_sales_v80.py pins on v80, plus the P0 probe's v80 cases."""
    if "world" not in STATE:
        new: dict[str, Callable[[], Acts]] = {**cfp.new_cases(), **track0.track0_cases()}
        world = {f"v80_{n}": b for n, b in new.items()}
        names = sorted(cfp.v79_cases()) + list(("t0_b_loss_8949_yes", "t0_q1_yes_nothing", "t0_8949no_old_ic_yes_q1_no",
                                                 "t0_b_w_scalar_only_on_gain"))
        for n in names:
            world[f"carried_{n}"] = (lambda n=n: cfp.with_q2(track0.v79_case(n), "no"))
        for n, b in codeb_probe.cases().items():
            world[f"probe_{n}"] = b
        STATE["world"] = world
    return STATE["world"]


def run(task: tuple[str, str]) -> tuple[tuple[str, str], dict[str, Any]]:
    kind, name = task
    started = time.monotonic()
    try:
        if kind == "new":
            pin("v81")
            result = codeb_probe.execute(new_cases()[name], f"demo.codeb.v81.{name}")
            out = {"result": summarize_v81(result), "mismatch": check(name, result)}
            if name in PARTS_KEPT and result.get("f8949_parts"):
                out["result"]["f8949_parts"] = result["f8949_parts"]
        else:
            build = v80_world()[name]
            if kind == "v80":
                pin("v80")
                result = codeb_probe.execute(build, f"demo.codeb.c80.{name}")
            else:
                pin("v81")
                answer = "no" if kind == "v81_q3_no" else None
                result = codeb_probe.execute(lambda: with_q3(build(), answer), f"demo.codeb.{kind}.{name}")
            out = summarize_v81(result)
    except Exception as exc:  # noqa: BLE001
        out = {"error": type(exc).__name__, "message": probe.scrub(str(exc))[:600],
               "trace": probe.scrub(traceback.format_exc())[-800:]}
    out["seconds"] = round(time.monotonic() - started, 1)
    return task, out


def form1040(result: dict[str, Any]) -> tuple[Any, Any]:
    lines = result.get("lines") or {}
    return tuple((lines.get(k) or [None, None])[1] for k in ("form1040.line-15", "form1040.line-16"))  # type: ignore[return-value]


def compare(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Every line, attachment and question v80 shows, on v81."""
    diff: dict[str, Any] = {}
    if before.get("error") or after.get("error"):
        if (before.get("error"), before.get("message")) != (after.get("error"), after.get("message")):
            diff["error"] = [before.get("error"), after.get("error")]
        return diff
    for key, value in (before.get("lines") or {}).items():
        if (after.get("lines") or {}).get(key) != value:
            diff[key] = [value, (after.get("lines") or {}).get(key)]
    for key in ("attachments", "questions", "symbols"):
        if before.get(key) != after.get(key):
            diff[key] = [before.get(key), after.get(key)]
    rows_before, rows_after = before.get("rows") or {}, after.get("rows") or {}
    for key, value in rows_before.items():
        if rows_after.get(key) != value:
            diff["row:" + key] = [value, rows_after.get(key)]
    return diff


def main() -> None:
    args = sys.argv[1:]
    if args[:1] == ["publish"]:  # rebuild the published v81 in place (Track 1 and the review repair)
        publish()
        return
    if args[:1] == ["rules"]:  # write the member bodies to a directory outside the repository
        codeb_probe.pin_v80()
        ORIGIN[:] = [probe.CONTENT, probe.RELEASE_DIR]
        target = Path(args[1]).resolve()
        assert REPO not in target.parents, "write the bodies outside the repository"
        with tempfile.TemporaryDirectory() as tmp:
            build(Path(tmp).resolve() / "scratch", rules_dir=target)
        print("wrote", len(list(target.glob("*.json"))), "bodies")
        return
    workers = int(args[0]) if args and args[0].isdigit() else 8
    selected = {a for a in args if not a.isdigit()}
    init()
    tasks = [("new", n) for n in new_cases() if not selected or n in selected or "new" in selected]
    carry_names = sorted(v80_world()) if not selected or "carry" in selected else []
    tasks += [(k, n) for n in carry_names for k in ("v80", "v81_q3_no", "v81_q3_unanswered")]
    results: dict[str, dict[str, Any]] = {}
    with ProcessPoolExecutor(workers, initializer=init) as pool:
        for (kind, name), result in pool.map(run, tasks):
            results.setdefault(kind, {})[name] = result
            shown = result.get("mismatch", None) if kind == "new" else form1040(result)
            print(kind, name, result.get("error") or "", shown if shown else "ok", result.get("seconds"), flush=True)
    payload: dict[str, Any] = {"source_ref": "milestone/f8949-code-b-2025", "scratch": "v81 / registry v79 / release v79 from v80",
                               "build": STATE["build"]}
    payload["v81_cases"] = results.get("new", {})
    carry = {}
    for name in carry_names:
        before, after, untouched = (results[k][name] for k in ("v80", "v81_q3_no", "v81_q3_unanswered"))
        carry[name] = {
            "v80": {"form1040": form1040(before), "attachments": before.get("attachments"), "error": before.get("error")},
            "v81_q3_no_diff": compare(before, after),
            "v81_q3_no_lines_1b_8b": {k: (after.get("lines") or {}).get(k) for k in ("schedule-d.line-1b", "schedule-d.line-8b")},
            "v81_q3_unanswered_form1040": form1040(untouched),
            "v81_q3_unanswered_questions": [q for q in untouched.get("questions") or [] if q == Q3_TEXT],
        }
    if carry:
        payload["v80_returns_on_v81"] = carry
    if selected and OUT.exists():
        merged = json.loads(OUT.read_text(encoding="utf-8"))
        merged.setdefault("v81_cases", {}).update(payload["v81_cases"])
        if carry:
            merged["v80_returns_on_v81"] = carry
        merged["build"] = payload["build"]
        payload = merged
    OUT.write_text(dump(payload), encoding="utf-8")
    print(f"wrote {OUT.name}", flush=True)


if __name__ == "__main__":
    main()
