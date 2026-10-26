"""Generate the credit for other dependents content (core v56, successor only).

Writes, under ``packages/content/tax/2025``: the other-dependent child and relative
vocabularies, their families and closure mappings, the return-level answers, the
per-subject chains and counts, the return gate, the successor Schedule 8812 line 6
rule, and the core v56 package; then the v54 registry (a copy of the v53 registry
with the new citizens and the v56 package appended), release v54, and the v56
adoption fixture. v53, v55 and every earlier package, registry and release are not
touched.

Run from the repository root:

    python3 tools/generate_other_dependents_credit_content.py

The generator is the reproducible source of the successor content. Its output is
committed; a re-run must produce byte-identical files.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from packages.derivation.package_validation import (  # noqa: E402
    citizen_checksum,
    package_instance_checksum,
)

CONTENT = REPO / "packages/content/tax/2025"
RELEASE_DIR = REPO / "packages/sample_data/student_loan_worksheet_integration/publication_surface/releases"
ADOPTION_DIR = REPO / "packages/sample_data/other_dependents_credit/adoptions"

SCOPE = {"tax_year": 2025, "jurisdiction": "US-federal", "family": "individual-income-tax"}
CITE = [{"id": "tax.us.2025.citation.schedule8812.part-i", "version": "v1"}]
YESNO = {"enum": ["yes", "no"]}
TAIL = ("Contributed categorical assertion, domain {yes, no}, no default, "
        "presence-before-value, free supersession.")

# Existing facts reused (see the evidence file, section 2).
REL = "tax.us.2025.eic.child.relationship"
JOINT = "tax.us.2025.eic.child.joint-return"
SSN = "tax.us.2025.eic.child.ssn"
OTHER = "tax.us.2025.eic.child.another-may-claim"
U17 = "tax.us.2025.ctc.child.under-17"
RES = "tax.us.2025.ctc.child.lived-with-you"
SUP = "tax.us.2025.ctc.child.no-over-half-support"
CIT = "tax.us.2025.ctc.child.citizen-or-resident"
CLAIM = "tax.us.2025.ctc.child.claimed-as-dependent"
NRA = "tax.us.2025.eic.not-nonresident-alien"
CAN_CLAIM = "tax.us.2025.standard-deduction.can-be-claimed-as-dependent"
FILING = "filing_status"
CTC_COUNT = "tax.us.2025.ctc.child-count"
LINE6 = "tax.us.2025.ctc.sch8812.line-6"
CHILD_KIND = "tax.us.eic-child"
REL_KIND = "tax.us.odc-dependent"

# New child answers and families.
C_BOX = "tax.us.2025.odc.child.other-dependent-box"
C_TIN = "tax.us.2025.odc.child.tin"
C_CLOSE = "tax.us.2025.odc.child-roster.source-closure"
C_INERT = "tax.us.2025.odc.child.inert-path-unwritten"
C_FAM = "tax.us.2025.odc.child-roster"
C_CNT = "tax.us.2025.odc.child-count"
C_PER = "tax.us.2025.odc.child.counted"
C_OTHER = "tax.us.2025.odc.child.other-tests-met"
C_ID = "tax.us.2025.odc.child.identity-met"

# New relative answers and families.
R_BOX = "tax.us.2025.odc.dependent.other-dependent-box"
R_REL = "tax.us.2025.odc.dependent.relationship"
R_NQC = "tax.us.2025.odc.dependent.not-qualifying-child"
R_GI = "tax.us.2025.odc.dependent.gross-income-under-limit"
R_SUP = "tax.us.2025.odc.dependent.over-half-support"
R_TIN = "tax.us.2025.odc.dependent.tin"
R_CIT = "tax.us.2025.odc.dependent.citizen-or-resident"
R_NM = "tax.us.2025.odc.dependent.not-joint-return"
R_CLOSE = "tax.us.2025.odc.relative-roster.source-closure"
R_INERT = "tax.us.2025.odc.dependent.inert-path-unwritten"
R_FAM = "tax.us.2025.odc.relative-roster"
R_CNT = "tax.us.2025.odc.relative-count"
R_PER = "tax.us.2025.odc.dependent.counted"
R_OK = "tax.us.2025.odc.dependent.tests-a-met"
R_OK_B = "tax.us.2025.odc.dependent.tests-b-met"

# Return-level answers and the gate.
TP = "tax.us.2025.odc.taxpayer-tin"
SP = "tax.us.2025.odc.spouse-tin"
F2555 = "tax.us.2025.odc.no-form-2555"
GATE = "tax.us.2025.odc.return-gate"
# The v55 return answer "no other dependent besides the CTC children" (ctc-return-questions).
# Yes: no other-dependent roster is read and its closures are not required. No: the rosters
# and their closures are required and read.
OD = "tax.us.2025.ctc.no-other-dependent"
C_CONFLICT = "tax.us.2025.odc.child-marked-conflict"
R_CONFLICT = "tax.us.2025.odc.relative-marked-conflict"
SPOUSE_GATE = "tax.us.2025.odc.spouse-gate"

PKG_ID = "tax.us.2025.package.core-calculations"
NEW_BUNDLES = {
    "odc-child-roster.bundle.json": "tax.us.2025.odc-child-roster.vocabulary",
    "odc-relative-roster.bundle.json": "tax.us.2025.odc-relative-roster.vocabulary",
    "odc-return-questions.bundle.json": "tax.us.2025.odc-return-questions.vocabulary",
}


def _write(path: Path, body: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def _ref(name: str) -> dict[str, Any]:
    return {"op": "ref", "name": name}


def _pin(item: str) -> dict[str, str]:
    return {"id": item, "version": "v1"}


def _yes(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": _ref(fact),
            "right": {"op": "category_literal", "fact_type": _pin(fact), "value": "yes"}}


def _no(fact: str) -> dict[str, Any]:
    return {"op": "categorical_compare", "cmp": "eq", "left": _ref(fact),
            "right": {"op": "category_literal", "fact_type": _pin(fact), "value": "no"}}


def _met(fact: str) -> dict[str, Any]:
    return {"op": "choose", "when": _yes(fact), "then": 1, "else": 0}


def _eq(expr: dict[str, Any], n: int) -> dict[str, Any]:
    return {"op": "compare", "cmp": "eq", "left": expr, "right": n}


def _block(code: str) -> dict[str, Any]:
    return {"op": "block", "code": code}


def _rule(rule_id: str, *, requires: list[str], pins: list[str], value: Any, publishes: str,
          notes: str, subject: str | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "schema": "rule-artifact.v14", "id": rule_id, "version": "v1", "scope": dict(SCOPE),
        "role": "computation", "requires": requires,
        "pins": [{"id": p, "origin": "assertion", "role": "input", "version": "v1"} for p in pins],
        "when": True, "value": value, "publishes": publishes,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": CITE, "notes": notes,
    }
    if subject is not None:
        body["subject"] = _pin(subject)
    return body


def _fact(fact_id: str, entity: tuple[str, str] | None, values: dict[str, Any]) -> dict[str, Any]:
    keys: list[dict[str, Any]] = []
    if entity is not None:
        keys.append({"kind": "entity", "name": entity[0], "entity_kind": entity[1]})
    keys.append({"kind": "literal", "name": "tax-year", "values": ["2025"]})
    return {"id": fact_id, "identity_keys": keys, "nature": "determinable", "schema": "fact-type.v2",
            "supersession": {"policy": "free"}, **values, "version": "v1"}


def _yesno(title: str) -> dict[str, Any]:
    return {"title": f"{title} {TAIL}", "value_schema": YESNO}


def _closure(fact_id: str, key: str, entity_kind: str, title: str) -> dict[str, Any]:
    return {"id": fact_id, "identity_keys": [
        {"kind": "entity", "name": key, "entity_kind": entity_kind},
        {"kind": "literal", "name": "tax-year", "values": ["2025"]}],
        "nature": "determinable", "schema": "fact-type.v2", "supersession": {"policy": "free"},
        "title": title, "value_schema": {"type": "boolean"}, "version": "v1"}


def _inert(fact_id: str) -> dict[str, Any]:
    return {"id": fact_id, "identity_keys": [{"kind": "literal", "name": "marker", "values": ["unused"]}],
            "nature": "determinable", "schema": "fact-type.v2", "supersession": {"policy": "free"},
            "title": "Internal marker used only to complete an inert rule path for the other-dependent "
                     "roster selection rule.", "value_schema": {"enum": ["unused"], "type": "string"},
            "version": "v1"}


def child_bundle() -> dict[str, Any]:
    ent = ("child", CHILD_KIND)
    return {"fact_types": [
        _fact(C_BOX, ent, _yesno(
            "You check the Credit for other dependents box in row (7) of the Dependents section "
            "for this child (Schedule 8812 instructions, Credit for Other Dependents, "
            "i1040s8.txt:90-96). Yes means you claim this child for the credit for other "
            "dependents; the child is then a member of the other-dependent roster."),),
        _fact(C_TIN, ent, _yesno(
            "This child has a social security number, individual taxpayer identification number, "
            "or adoption taxpayer identification number issued on or before the due date of your "
            "2025 return, including extensions (Schedule 8812 instructions, Dependent required to "
            "have a TIN, i1040s8.txt:56-60 and 82-84). Asked for each child marked for the credit "
            "for other dependents: the identity rule, which runs per marked child, requires it, and "
            "its value reads it only where the child's SSN is no."),),
        _closure(C_CLOSE, "family-horizon", "kernel.family-horizon",
                 "Closure of the 2025 other-dependent child roster. Contributed boolean assertion, "
                 "free supersession."),
        _inert(C_INERT),
    ], "id": "tax.us.2025.odc-child-roster.vocabulary", "label":
        "2025 other-dependent child roster vocabulary", "schema": "bundle.v2", "version": "v1"}


def relative_bundle() -> dict[str, Any]:
    ent = ("dependent", REL_KIND)
    return {"fact_types": [
        _fact(R_BOX, ent, _yesno(
            "You check the Credit for other dependents box in row (7) of the Dependents section "
            "for this person (Schedule 8812 instructions, i1040s8.txt:90-96). Yes means you claim "
            "this person for the credit for other dependents; the person is then a member of the "
            "other-dependent relative roster."),),
        _fact(R_REL, ent, _yesno(
            "This person is related to you as listed in Form 1040 Step 4 (son, daughter, "
            "stepchild, foster child, sibling, parent, grandparent, aunt, uncle, niece, nephew, "
            "in-law, or a step relative), or lived with you all year as a member of your household "
            "(i1040gi-2025.txt:1054-1076)."),),
        _fact(R_NQC, ent, _yesno(
            "No other taxpayer may claim this person as a qualifying child for 2025 (Form 1040 "
            "Step 4, who wasn't a qualifying child of any taxpayer, i1040gi-2025.txt:1087-1088)."),),
        _fact(R_GI, ent, _yesno(
            "This person's 2025 gross income was less than $5,200 (Form 1040 Step 4, "
            "i1040gi-2025.txt:1097). A permanently and totally disabled person whose gross income "
            "is $5,200 or more is outside the class: answer no."),),
        _fact(R_SUP, ent, _yesno(
            "You provided more than half of this person's 2025 support (Form 1040 Step 4, "
            "i1040gi-2025.txt:1106-1107). A multiple support agreement is outside the class: "
            "answer no."),),
        _fact(R_TIN, ent, _yesno(
            "This person has a social security number, individual taxpayer identification number, "
            "or adoption taxpayer identification number issued on or before the due date of your "
            "2025 return, including extensions (Form 1040 Step 5 question 2, i1040gi-2025.txt:"
            "1110-1113; Schedule 8812 instructions, i1040s8.txt:56-60)."),),
        _fact(R_CIT, ent, _yesno(
            "This person was a U.S. citizen, U.S. national, or U.S. resident alien for 2025 (Form "
            "1040 Step 5 question 3, i1040gi-2025.txt:1123-1124; Schedule 8812 instructions, "
            "i1040s8.txt:76-78). A resident of Canada or Mexico who is not one of these does not "
            "meet this test."),),
        _fact(R_NM, ent, _yesno(
            "This person did not file a joint return for 2025, or filed one only to claim a refund "
            "of withheld income tax or estimated tax paid (Form 1040 instructions, married person, "
            "i1040gi-2025.txt:1253-1257). A relative who files a joint return is outside the class: "
            "answer no. Married filing separately qualifies: answer yes."),),
        _closure(R_CLOSE, "family-horizon", "kernel.family-horizon",
                 "Closure of the 2025 other-dependent relative roster. Contributed boolean "
                 "assertion, free supersession."),
        _inert(R_INERT),
    ], "id": "tax.us.2025.odc-relative-roster.vocabulary", "label":
        "2025 other-dependent relative roster vocabulary", "schema": "bundle.v2", "version": "v1"}


def return_bundle() -> dict[str, Any]:
    fam = [
        _fact(TP, None, _yesno(
            "You, the taxpayer, have a social security number or individual taxpayer identification "
            "number issued on or before the due date of your 2025 return, including extensions "
            "(Schedule 8812 instructions, i1040s8.txt:47-50; Form 1040 Step 5 question 1, "
            "i1040gi-2025.txt:1098-1100). Asked when an other dependent is counted. The spouse has "
            "its own question."),),
        _fact(SP, None, _yesno(
            "On this joint return, your spouse has a social security number or individual "
            "taxpayer identification number issued on or before the due date of your 2025 return, "
            "including extensions (Schedule 8812 instructions, i1040s8.txt:47-50). Asked on a "
            "joint return when any dependent counts."),),
        _fact(F2555, None, _yesno(
            "Your 2025 return claims no income excluded on Form 2555 (Schedule 8812 line 2b, "
            "f1040s8.txt:13). Asked when any dependent counts."),),
    ]
    return {"fact_types": fam, "id": "tax.us.2025.odc-return-questions.vocabulary",
            "label": "2025 other-dependent return questions", "schema": "bundle.v2", "version": "v1"}


def child_family() -> dict[str, Any]:
    return {"authorizes_subtotal": C_CNT,
            "closure_claim": "Every child the filer claims for the credit for other dependents is "
                             "recorded as a roster item.",
            "id": C_FAM, "member_predicate": {"fact_type": C_BOX},
            "schema": "source-family.v1", "scope": dict(SCOPE),
            "title": "2025 other-dependent child roster", "version": "v1"}


def relative_family() -> dict[str, Any]:
    return {"authorizes_subtotal": R_CNT,
            "closure_claim": "Every relative the filer claims for the credit for other dependents "
                             "is recorded as a roster item.",
            "id": R_FAM, "member_predicate": {"fact_type": R_BOX},
            "schema": "source-family.v1", "scope": dict(SCOPE),
            "title": "2025 other-dependent relative roster", "version": "v1"}


def mapping(mapping_id: str, family: str, member: str, close: str, admits: str) -> dict[str, Any]:
    return {"admission": {"condition": "current-literal-true"}, "admits_symbol": admits,
            "closure_fact_type": _pin(close), "closure_horizon_key": "family-horizon",
            "family": _pin(family), "id": mapping_id, "member_fact_type": _pin(member),
            "schema": "source-closure-mapping.v2", "version": "v1"}


def other_tests_rule() -> dict[str, Any]:
    """Per child: the joint-return, lived-with-you, no-support, citizen and tie-breaker tests."""
    value = {"op": "choose", "when": _eq({"op": "add", "args": [
        _met(JOINT), _met(RES), _met(SUP), _met(CIT),
        {"op": "choose", "when": _yes(OTHER), "then": 0, "else": 1}]}, 5), "then": 1, "else": 0}
    return _rule("tax.us.2025.rule.odc-child.other-tests-met",
                 requires=[JOINT, RES, SUP, CIT, OTHER], pins=[], subject=C_BOX,
                 value=value, publishes=C_OTHER,
                 notes="Per child on the other-dependent roster: the five shared credit tests (joint "
                       "return, lived with you, no support, citizen or resident, not claimed by "
                       "another). Counts 1 when all pass.")


def identity_rule() -> dict[str, Any]:
    """Per marked child (a roster row exists only for a child whose box is yes): an SSN valid for
    employment, or else an ITIN or ATIN by the due date. A child whose box is no is not a roster row,
    so this rule never runs for it and it needs nothing."""
    value = {"op": "choose", "when": _yes(SSN), "then": 1, "else": {
        "op": "choose", "when": _yes(C_TIN), "then": 1, "else": 0}}
    return _rule("tax.us.2025.rule.odc-child.identity-met", requires=[SSN, C_TIN], pins=[SSN, C_TIN],
                 subject=C_BOX, value=value, publishes=C_ID,
                 notes="Per marked child: 1 with an SSN valid for employment, or else with an ITIN or ATIN by "
                       "the due date; 0 otherwise. Runs only for marked children.")


def child_rule() -> dict[str, Any]:
    ages_ok = _eq({"op": "add", "args": [_met(U17), _met(SSN)]}, 2)
    value = {"op": "choose", "when": _no(C_BOX), "then": 0, "else": {
        "op": "choose", "when": _yes(CLAIM), "then": _block("DEPENDENCY_INVALID"), "else": {
            "op": "choose", "when": _eq(_ref(C_OTHER), 1), "then": {
                "op": "choose", "when": ages_ok, "then": _block("DEPENDENCY_INVALID"),
                "else": {"op": "choose", "when": _eq(_ref(C_ID), 1), "then": 1,
                         "else": _block("DEPENDENCY_INVALID")}},
            "else": _block("DEPENDENCY_INVALID")}}}
    return _rule(
        "tax.us.2025.rule.odc-child.counts",
        requires=[C_BOX, CLAIM, U17, SSN, C_OTHER, C_ID], pins=[], subject=C_BOX, value=value,
        publishes=C_PER,
        notes="Per child on the other-dependent roster. 0 when the box is no. Blocks when the child "
              "tax credit box is also yes, when another test fails, or when the child passes every "
              "credit test (use the credit box). Otherwise 1 with an SSN valid for employment or, "
              "without one, an ITIN or ATIN by the due date.")


def child_count_rule() -> dict[str, Any]:
    return _count_rule("odc-child-count", C_FAM, C_BOX, C_PER, C_INERT, C_CNT,
                       "Count of other-dependent children over the closed child roster. Zero when "
                       "the roster is closed and empty.")


RELATIVE_TESTS_A = [R_REL, R_NQC, R_GI, R_SUP]
RELATIVE_TESTS_B = [R_TIN, R_CIT, R_NM]


def _relative_tests(rule_id: str, tests: list[str], publishes: str, text: str) -> dict[str, Any]:
    value = {"op": "choose", "when": _eq({"op": "add", "args": [_met(t) for t in tests]}, len(tests)),
             "then": 1, "else": 0}
    return _rule(rule_id, requires=tests, pins=[], subject=tests[0], value=value,
                 publishes=publishes, notes=text)


def relative_tests_rule() -> dict[str, Any]:
    return _relative_tests("tax.us.2025.rule.odc-relative.tests-a-met", RELATIVE_TESTS_A, R_OK,
                           "Per relative: relationship or household, not a qualifying child of any "
                           "taxpayer, gross income under $5,200, and over-half support. 1 when all pass.")


def relative_tests_b_rule() -> dict[str, Any]:
    return _relative_tests("tax.us.2025.rule.odc-relative.tests-b-met", RELATIVE_TESTS_B, R_OK_B,
                           "Per relative: identification number, citizen or resident alien, and not "
                           "married at the end of 2025. 1 when all pass.")


def relative_rule() -> dict[str, Any]:
    value = {"op": "choose", "when": _no(R_BOX), "then": 0, "else": {
        "op": "choose", "when": {"op": "all", "args": [_eq(_ref(R_OK), 1), _eq(_ref(R_OK_B), 1)]},
        "then": 1, "else": _block("DEPENDENCY_INVALID")}}
    return _rule("tax.us.2025.rule.odc-relative.counts", requires=[R_BOX, R_OK, R_OK_B], pins=[],
                 subject=R_BOX, value=value, publishes=R_PER,
                 notes="Per relative on the other-dependent roster. 0 when the box is no; 1 when every "
                       "relative test passes; a failed test blocks as outside the class.")


def relative_count_rule() -> dict[str, Any]:
    return _count_rule("odc-relative-count", R_FAM, R_BOX, R_PER, R_INERT, R_CNT,
                       "Count of other-dependent relatives over the closed relative roster. Zero "
                       "when the roster is closed and empty.")


def _count_rule(name: str, family: str, member: str, per: str, inert: str, publishes: str,
                notes: str) -> dict[str, Any]:
    return {
        "schema": "rule-artifact.v14", "id": f"tax.us.2025.rule.{name}", "version": "v1",
        "scope": dict(SCOPE), "role": "computation", "requires": [], "pins": [], "when": True,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}, "citations": CITE,
        "publishes": publishes, "notes": notes,
        "selection": {
            "mode": "exclusive_presence", "conflict": "refuse",
            "paths": [
                {"id": "members",
                 "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(member)]},
                 "reads_subject_results": [{"symbol": per, "subject": _pin(member)}],
                 "requires": [], "pins": [],
                 "when": {"op": "require_closed", "source_set": family},
                 "value": {"op": "add", "args": [{"op": "collect", "name": per, "source_set": family}]}},
                {"id": "inert",
                 "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(inert)]},
                 "reads_subject_results": [], "requires": [], "pins": [], "when": True,
                 "value": {"op": "block", "code": "DEPENDENCY_ABSENT"}},
            ],
            "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [],
                        "when": True,
                        "value": {"op": "count", "name": member, "source_set": family}},
            "refusal": {"code": "DEPENDENCY_INVALID",
                        "missing": [f"tax.us.2025.{family}.inert-path-conflict"], "pins": []},
        },
    }


def _rosters_read(then: Any) -> Any:
    """The other-dependent counts are read only when the return answer says an other dependent is
    present (OD is no). The guarded reads sit inside a conditional dependency set."""
    return {"op": "choose", "when": _yes(OD), "then": 0, "else": {
        "op": "choose", "when": {"op": "all", "args": [{
            "op": "conditional_dependency_set", "condition": _no(OD),
            "members": [_ref(C_CNT), _ref(R_CNT)]}]},
        "then": then, "else": _block("DEPENDENCY_INVALID")}}


def _any_dependent() -> dict[str, Any]:
    return {"op": "compare", "cmp": "gt", "left": {"op": "add", "args": [_ref(C_CNT), _ref(R_CNT)]},
            "right": 0}


PRESENT = "tax.us.2025.odc.dependent-present"


def presence_rule() -> dict[str, Any]:
    """1 when an other dependent is counted on a closed roster, 0 otherwise. Read only while OD is no."""
    inner = {"op": "choose", "when": _any_dependent(), "then": 1, "else": 0}
    value = {"op": "choose", "when": _yes(OD), "then": 0, "else": {
        "op": "choose", "when": {"op": "all", "args": [{
            "op": "conditional_dependency_set", "condition": _no(OD),
            "members": [_ref(C_CNT), _ref(R_CNT)]}]},
        "then": inner, "else": _block("DEPENDENCY_INVALID")}}
    return _rule("tax.us.2025.rule.odc-dependent-present", requires=[OD], pins=[], value=value,
                 publishes=PRESENT,
                 notes="1 when an other dependent is counted on a closed roster; 0 otherwise. Reads the "
                       "rosters only while the return answer says an other dependent is present.")


def gate_rule() -> dict[str, Any]:
    present = {"op": "all", "args": [{"op": "conditional_dependency_set", "condition": _eq(_ref(PRESENT), 1),
                                      "members": [_ref(TP), _ref(F2555), _ref(NRA), _ref(CAN_CLAIM)]}]}
    ok = {"op": "all", "args": [_yes(TP), _yes(F2555), _yes(NRA), _no(CAN_CLAIM)]}
    value = {"op": "choose", "when": _eq(_ref(PRESENT), 1), "then": {
        "op": "choose", "when": present, "then": {
            "op": "choose", "when": ok, "then": 1, "else": _block("DEPENDENCY_INVALID")},
        "else": 1}, "else": 1}
    return _rule("tax.us.2025.rule.odc-return-gate", requires=[PRESENT], pins=[],
                 value=value, publishes=GATE,
                 notes="Return level. With an other dependent present: taxpayer SSN or ITIN, Form 2555 "
                       "(none), nonresident alien (no), could-be-claimed (no).")


def spouse_gate_rule() -> dict[str, Any]:
    joint = {"op": "categorical_compare", "cmp": "eq", "left": _ref(FILING),
             "right": {"op": "category_literal", "fact_type": _pin("tax.us.2025.filing-status"),
                       "value": "married_filing_jointly"}}
    spouse = {"op": "all", "args": [{"op": "conditional_dependency_set", "condition": _eq(_ref(PRESENT), 1),
                                     "members": [_ref(SP)]}]}
    value = {"op": "choose", "when": _eq(_ref(PRESENT), 1), "then": {
        "op": "choose", "when": joint, "then": {
            "op": "choose", "when": spouse, "then": {
                "op": "choose", "when": _yes(SP), "then": 1, "else": _block("DEPENDENCY_INVALID")},
            "else": 1},
        "else": 1}, "else": 1}
    return _rule("tax.us.2025.rule.odc-spouse-gate", requires=[PRESENT, FILING], pins=[],
                 value=value, publishes=SPOUSE_GATE,
                 notes="Return level. Joint return with an other dependent present: spouse SSN or ITIN.")


def _conflict_rule(rule_id: str, member: str, publishes: str, label: str) -> dict[str, Any]:
    """Blocks when a box is marked for the other-dependent credit while OD says no other dependent.
    It reads no roster and needs no closure, so it adds no requirement to a return with no marked row."""
    marked = {"id": "marked", "activity": {"kind": "source_nonempty", "member_fact_types": [_pin(member)]},
              "reads_subject_results": [], "requires": [OD],
              "pins": [{"id": OD, "origin": "assertion", "role": "input", "version": "v1"}], "when": True,
              "value": {"op": "choose", "when": _yes(OD), "then": _block("DEPENDENCY_INVALID"), "else": 0}}
    inert = {"id": "inert", "activity": {"kind": "source_nonempty",
                                         "member_fact_types": [_pin(INERT_FOR[member])]},
             "reads_subject_results": [], "requires": [], "pins": [], "when": True,
             "value": {"op": "block", "code": "DEPENDENCY_ABSENT"}}
    return {
        "schema": "rule-artifact.v14", "id": rule_id, "version": "v1", "scope": dict(SCOPE),
        "role": "computation", "requires": [], "pins": [], "when": True,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []}, "citations": CITE,
        "publishes": publishes,
        "notes": f"{label}: a row marked for the credit for other dependents while the return answer says "
                 "no other dependent is an error (blocks). Otherwise 0.",
        "selection": {"mode": "exclusive_presence", "conflict": "refuse", "paths": [marked, inert],
                      "default": {"id": "neither", "reads_subject_results": [], "requires": [], "pins": [],
                                  "when": True, "value": 0},
                      "refusal": {"code": "DEPENDENCY_INVALID", "missing": [rule_id + ".inert"], "pins": []}},
    }


INERT_FOR: dict[str, str] = {}


def conflict_rules() -> list[dict[str, Any]]:
    INERT_FOR[C_BOX] = C_INERT
    INERT_FOR[R_BOX] = R_INERT
    return [_conflict_rule("tax.us.2025.rule.odc-child-marked-conflict", C_BOX, C_CONFLICT,
                           "Children"),
            _conflict_rule("tax.us.2025.rule.odc-relative-marked-conflict", R_BOX, R_CONFLICT,
                           "Relatives")]


def line6_rule() -> dict[str, Any]:
    # The return gates feed line 6, so a failing or missing gate answer blocks line 19 (through line 8).
    value = {"op": "choose", "when": {"op": "all", "args": [
                 _eq(_ref(C_CONFLICT), 0), _eq(_ref(R_CONFLICT), 0),
                 _eq(_ref(GATE), 1), _eq(_ref(SPOUSE_GATE), 1)]},
             "then": _rosters_read({"op": "add", "args": [_ref(C_CNT), _ref(R_CNT)]}),
             "else": _block("DEPENDENCY_INVALID")}
    return {
        "schema": "rule-artifact.v14", "id": "tax.us.2025.rule.ctc-sch8812-line-6", "version": "v2",
        "scope": dict(SCOPE), "role": "computation",
        "requires": [OD, C_CONFLICT, R_CONFLICT, GATE, SPOUSE_GATE], "pins": [],
        "when": True, "value": value, "publishes": LINE6,
        "blocked": {"code": "DEPENDENCY_ABSENT", "missing": []},
        "citations": CITE,
        "notes": "Line 6 (v2): the other dependents. Zero when the return answer says no other dependent. "
                 "Otherwise the children marked and the relatives counted on their closed rosters.",
    }


def rule_files() -> dict[str, dict[str, Any]]:
    return {
        "rule.odc-child.other-tests-met.json": other_tests_rule(),
        "rule.odc-child.identity-met.json": identity_rule(),
        "rule.odc-child.counts.json": child_rule(),
        "rule.odc-child-count.json": child_count_rule(),
        "rule.odc-relative.tests-a-met.json": relative_tests_rule(),
        "rule.odc-relative.tests-b-met.json": relative_tests_b_rule(),
        "rule.odc-relative.counts.json": relative_rule(),
        "rule.odc-relative-count.json": relative_count_rule(),
        "rule.odc-child-marked-conflict.json": conflict_rules()[0],
        "rule.odc-relative-marked-conflict.json": conflict_rules()[1],
        "rule.odc-dependent-present.json": presence_rule(),
        "rule.odc-return-gate.json": gate_rule(),
        "rule.odc-spouse-gate.json": spouse_gate_rule(),
        "rule.ctc-sch8812-line-6.v2.json": line6_rule(),
    }


def new_members() -> list[tuple[str, dict[str, Any], str]]:
    out: list[tuple[str, dict[str, Any], str]] = [
        ("odc-child-roster.bundle.json", child_bundle(), "fact-type-bundle"),
        ("odc-relative-roster.bundle.json", relative_bundle(), "fact-type-bundle"),
        ("odc-return-questions.bundle.json", return_bundle(), "fact-type-bundle"),
        ("family.odc-child-roster.json", child_family(), "source-family"),
        ("family.odc-relative-roster.json", relative_family(), "source-family"),
        ("closure-mapping.odc-child-roster.json",
         mapping("tax.us.2025.closure-mapping.odc-child-roster", C_FAM, C_BOX, C_CLOSE, C_CNT),
         "source-closure-mapping"),
        ("closure-mapping.odc-relative-roster.json",
         mapping("tax.us.2025.closure-mapping.odc-relative-roster", R_FAM, R_BOX, R_CLOSE, R_CNT),
         "source-closure-mapping"),
    ]
    for file, body in rule_files().items():
        out.append((file, body, "computation"))
    for file, body in form_field_files().items():
        out.append((file, body, "form-field"))
    return out


def _form_field(field_id: str, symbol: str, line: str, label: str, description: str) -> dict[str, Any]:
    """A presentation row for a Schedule 8812 line the other-dependent credit adds (the form-field
    shape of ``form.sch8812.line-4``; only new rows get one)."""
    return {
        "binds_symbol": symbol,
        "citation": {"id": "tax.us.2025.citation.schedule8812.part-i", "version": "v1"},
        "description": description,
        "dispositions": {
            "blocked": {"codes": ["DEPENDENCY_ABSENT", "DEPENDENCY_INVALID"],
                        "explain": f"Schedule 8812 line {line} is blocked because an input it needs is "
                                   "missing or invalid.", "render": ""},
            "closure_backed_zero": {"explain": f"Schedule 8812 line {line} publishes zero through an honest "
                                               "closed-empty source family.", "render": "0"},
            "computed_zero": {"explain": f"Schedule 8812 line {line} publishes a computed zero.",
                              "render": "0"},
            "guard_inapplicable": {"explain": f"No value is published for Schedule 8812 line {line} because "
                                              "its worksheet guard is not satisfied.", "render": ""},
            "published_value": {"explain": description, "render": "{value}"},
        },
        "form": {"authority": "IRS", "form_id": "Schedule 8812", "jurisdiction": "US-federal",
                 "tax_year": 2025},
        "id": field_id, "label": label, "line": f"8812-{line}", "schema": "form-field.v3", "version": "v1",
    }


def form_field_files() -> dict[str, dict[str, Any]]:
    return {
        "form.sch8812.line-6.form-field.json": _form_field(
            "tax.us.2025.form.sch8812.line-6", "tax.us.2025.ctc.sch8812.line-6", "6",
            "Other dependents",
            "Schedule 8812 line 6: other dependents, including children who fail a credit test, "
            "counted on the closed rosters."),
        "form.sch8812.line-7.form-field.json": _form_field(
            "tax.us.2025.form.sch8812.line-7", "tax.us.2025.ctc.sch8812.line-7", "7",
            "Credit for other dependents amount",
            "Schedule 8812 line 7: line 6 multiplied by $500."),
    }


def build_package(v55: dict[str, Any], members: list[tuple[str, dict[str, Any], str]]) -> dict[str, Any]:
    old_line6 = "tax.us.2025.rule.ctc-sch8812-line-6"
    kept = [m for m in v55["members"] if m["id"] != old_line6]
    for file, body, role in members:
        kept.append({"id": body["id"], "version": body["version"], "schema": body["schema"], "role": role})
    entry = [e for e in v55["entrypoints"] if e["id"] != old_line6]
    for file, body, role in members:
        if role in ("fact-type-bundle", "source-family", "source-closure-mapping"):
            entry.append({"id": body["id"], "version": body["version"]})
    entry.append({"id": "tax.us.2025.rule.odc-child-count", "version": "v1"})
    entry.append({"id": "tax.us.2025.rule.odc-relative-count", "version": "v1"})
    entry.append({"id": "tax.us.2025.rule.odc-return-gate", "version": "v1"})
    entry.append({"id": "tax.us.2025.rule.odc-spouse-gate", "version": "v1"})
    entry.append({"id": "tax.us.2025.rule.odc-child-marked-conflict", "version": "v1"})
    entry.append({"id": "tax.us.2025.rule.odc-relative-marked-conflict", "version": "v1"})
    entry.append({"id": old_line6, "version": "v2"})
    package = {k: v for k, v in v55.items() if k != "package_checksum"}
    package["version"] = "v56"
    package["members"] = kept
    package["entrypoints"] = entry
    package["package_checksum"] = package_instance_checksum(package)
    return package


def main() -> int:
    v55 = json.loads((CONTENT / "package.core-calculations.v55.json").read_text(encoding="utf-8"))
    members = new_members()
    for file, body, _ in members:
        _write(CONTENT / file, body)
    package = build_package(v55, members)
    _write(CONTENT / "package.core-calculations.v56.json", package)

    registry_v53 = json.loads((CONTENT / "published-packages.v53.json").read_text(encoding="utf-8"))
    citizens = list(registry_v53["citizens"])
    known = {(c["id"], c["version"]) for c in citizens}
    for file, body, _ in members:
        if (body["id"], body["version"]) not in known:
            citizens.append({"checksum": citizen_checksum(body), "id": body["id"],
                             "version": body["version"]})
            known.add((body["id"], body["version"]))
    packages = list(registry_v53["packages"])
    packages.append({"checksum": package["package_checksum"], "id": PKG_ID, "version": "v56"})
    registry_v54 = {"citizens": citizens, "packages": packages}
    _write(CONTENT / "published-packages.v54.json", registry_v54)

    registry_bytes = (CONTENT / "published-packages.v54.json").read_bytes()
    release = {"id": "demo.release.sli-worksheet-integration.2025",
               "package_registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
               "schema": "release-registry.v1", "version": "v54"}
    release_path = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v54.json"
    _write(release_path, release)
    release_checksum = hashlib.sha256(release_path.read_bytes()).hexdigest()

    adoption = {
        "act_id": "demo.act.adopt.core.v56", "actor": "demo.user.filer-1",
        "at": "2026-10-25T12:00:00Z", "committed_against": 0, "kind": "package-adoption",
        "payload": {
            "audit": {"note": "synthetic successor adoption of core calculations v56 (credit for other "
                              "dependents, Schedule 8812 lines 6 to 14); non-authoritative"},
            "package": {"checksum": package["package_checksum"], "id": PKG_ID, "version": "v56"},
            "release": {"checksum": release_checksum,
                        "id": "demo.release.sli-worksheet-integration.2025", "version": "v54"},
            "revision": 56, "scope": {"jurisdiction": "us", "year": "2025"}},
        "schema": "act.v1",
    }
    _write(ADOPTION_DIR / "adopt-core-v56-current.json", adoption)
    print(f"package v56 checksum {package['package_checksum']}")
    print(f"registry v54 sha256 {hashlib.sha256(registry_bytes).hexdigest()}")
    print(f"release v54 checksum {release_checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
