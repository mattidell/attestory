"""Credit for other dependents on core v56, through the real coordinator.

Every computed row of ``docs/phases/engine-breadth/milestones/other-dependents-credit-evidence/
odc_case_table.py`` runs on the engine (the wages are the AGI, the engine's tax is the
input to Credit Limit Worksheet A). The other-dependent children, relatives and return
answers are added to the child tax credit harness of v55 (the same child roster and
filer answers), so the credit's inputs are the ones the engine already reads.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any, Mapping, cast

from packages.derivation.package_validation import validate_package
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for

from tests.test_child_tax_credit_track1 import (
    CHILD_TYPES,
    CLAIM,
    OD,
    RES,
    SSN,
    U17,
    build_acts as ctc_build_acts,
    child_fid,
    passing_child as ctc_passing_child,
    run_v55,
    value,
    blocked_by,
)
from tests.test_refund_or_amount_owed_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    _act,
    _attested,
    _close_empty,
    _close_other_box4_families,
    _finish,
    _load,
)
from tests.test_refund_or_amount_owed_track2 import _add_bottom_line_answers, _add_box2_only
from tests.test_eic_qualifying_children_track1 import _run_surface

PACKAGE_V56 = CONTENT / "package.core-calculations.v56.json"
REGISTRY_V54 = CONTENT / "published-packages.v54.json"
REGISTRY_V53 = CONTENT / "published-packages.v53.json"
RELEASE_V54 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v54.json"
SURFACE_V56 = PublicationSurface(RELEASE_DIR, REGISTRY_V54, CONTENT)
ADOPTION_V56 = ROOT / "packages/sample_data/other_dependents_credit/adoptions/adopt-core-v56-current.json"
CASE_TABLE = ROOT / "docs/phases/engine-breadth/milestones/other-dependents-credit-evidence/odc_case_table.py"

YEAR = "2025"
USER = "demo.user.filer-1"
JOINT_STATUS = "married_filing_jointly"

# New answers (tools/generate_other_dependents_credit_content.py).
C_BOX = "tax.us.2025.odc.child.other-dependent-box"
C_TIN = "tax.us.2025.odc.child.tin"
C_CLOSE = "tax.us.2025.odc.child-roster.source-closure"
C_CNT = "tax.us.2025.odc.child-count"
R_BOX = "tax.us.2025.odc.dependent.other-dependent-box"
R_REL = "tax.us.2025.odc.dependent.relationship"
R_NQC = "tax.us.2025.odc.dependent.not-qualifying-child"
R_GI = "tax.us.2025.odc.dependent.gross-income-under-limit"
R_SUP = "tax.us.2025.odc.dependent.over-half-support"
R_TIN = "tax.us.2025.odc.dependent.tin"
R_CIT = "tax.us.2025.odc.dependent.citizen-or-resident"
R_NM = "tax.us.2025.odc.dependent.not-joint-return"
C_CONFLICT = "tax.us.2025.odc.child-marked-conflict"
R_CONFLICT = "tax.us.2025.odc.relative-marked-conflict"
R_TESTS_A = (R_REL, R_NQC, R_GI, R_SUP)
R_TESTS_B = (R_TIN, R_CIT, R_NM)
R_CLOSE = "tax.us.2025.odc.relative-roster.source-closure"
R_CNT = "tax.us.2025.odc.relative-count"
REL_KIND = "tax.us.odc-dependent"
TP = "tax.us.2025.odc.taxpayer-tin"
SP = "tax.us.2025.odc.spouse-tin"
F2555 = "tax.us.2025.odc.no-form-2555"
GATE = "tax.us.2025.odc.return-gate"
NRA = "tax.us.2025.eic.not-nonresident-alien"
CAN_CLAIM = "tax.us.2025.standard-deduction.can-be-claimed-as-dependent"
PR = "tax.us.2025.ctc.no-puerto-rico-or-4563-exclusion"
TAX = "tax.us.2025.tax.total-tax"
OD_ANSWER = OD
L7 = "tax.us.2025.ctc.sch8812.line-7"
L8 = "tax.us.2025.ctc.sch8812.line-8"
L6 = "tax.us.2025.ctc.sch8812.line-6"
LINE19 = "tax.us.2025.ctc.form1040-line19"

NEW_ANSWERS_CHILD = (C_BOX, C_TIN)
NEW_ANSWERS_RELATIVE = (R_BOX, R_REL, R_NQC, R_GI, R_SUP, R_TIN, R_CIT, R_NM)
BUNDLES = ("odc-child-roster.bundle.json", "odc-relative-roster.bundle.json",
           "odc-return-questions.bundle.json")


def _load_case_table() -> Any:
    spec = importlib.util.spec_from_file_location("odc_case_table", CASE_TABLE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the case table")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def ctc_child(**over: str) -> dict[str, str]:
    """A child for the child tax credit (box yes, every test yes, TIN answered)."""
    answers = dict(ctc_passing_child())
    answers[C_BOX] = "no"
    answers[C_TIN] = "yes"
    answers.update(over)
    return answers


def odc_child(**over: str) -> dict[str, str]:
    """A child for the credit for other dependents: box yes, aged 17, SSN valid."""
    answers = ctc_child(**{CLAIM: "no", C_BOX: "yes", U17: "no"})
    answers.update(over)
    return answers


def odc_child_itin(**over: str) -> dict[str, str]:
    """A child with an ITIN and no valid SSN: box yes, under 17, SSN no, TIN yes."""
    answers = odc_child(**{U17: "yes", SSN: "no", C_TIN: "yes"})
    answers.update(over)
    return answers


def relative(**over: str) -> dict[str, str]:
    answers = {R_BOX: "yes", R_REL: "yes", R_NQC: "yes", R_GI: "yes", R_SUP: "yes",
               R_TIN: "yes", R_CIT: "yes", R_NM: "yes"}
    answers.update(over)
    return answers


def without(answers: Mapping[str, str], key: str) -> dict[str, str]:
    return {k: v for k, v in answers.items() if k != key}


def _odc_extras(
    raw: list[dict[str, object]],
    children: Mapping[str, Mapping[str, str]],
    relatives: Mapping[str, Mapping[str, str]],
    *,
    child_closed: bool,
    relative_closed: bool,
    return_answers: Mapping[str, str | None],
) -> None:
    def add(kind: str, payload: dict[str, object]) -> None:
        raw.append(_act(len(raw), kind, payload))

    for name in BUNDLES:
        add("bundle-adoption", {"bundle": _load(name)})
    scope = {"tax-year": YEAR, "subject": "demo.primary"}
    head = "demo.odc.child.h0"
    family = {"id": "tax.us.2025.odc.child-roster", "version": "v1"}
    add("horizon-genesis", {"family": family, "scope": scope, "horizon_id": head})
    # A roster row exists only for a child marked yes; a child marked no (or not marked) is not a row.
    marked = [(c, a) for c, a in children.items() if a.get(C_BOX) == "yes"]
    for idx, (child, answers) in enumerate(marked):
        successor = f"demo.odc.child.h{idx + 1}"
        add("member-transition", {"family": family, "scope": scope, "member": {
            "action": "assert", "finding": _attested(
                f"demo.odc.box.{child}", child_fid(C_BOX, child), answers[C_BOX])},
            "successor": {"id": successor, "predecessor": head}})
        head = successor
        if answers.get(C_TIN) is not None:
            add("assertion", {"finding": _attested(
                f"demo.odc.tin.{child}", child_fid(C_TIN, child), answers[C_TIN])})
    if child_closed:
        add("assertion", {"finding": _attested(
            "demo.odc.child.closure", f"{C_CLOSE}|family-horizon={head},tax-year={YEAR}", True)})

    rel_scope = {"tax-year": YEAR, "subject": "demo.primary"}
    rel_head = "demo.odc.rel.h0"
    rel_family = {"id": "tax.us.2025.odc.relative-roster", "version": "v1"}
    for name, answers in relatives.items():
        add("entity-introduced", {"entity": {"schema": "entity.v1", "id": name, "kind": REL_KIND,
                                             "label": "Synthetic other dependent"}})
    add("horizon-genesis", {"family": rel_family, "scope": rel_scope, "horizon_id": rel_head})
    rel_marked = [(n, a) for n, a in relatives.items() if a.get(R_BOX) == "yes"]
    for idx, (name, answers) in enumerate(rel_marked):
        successor = f"demo.odc.rel.h{idx + 1}"
        add("member-transition", {"family": rel_family, "scope": rel_scope, "member": {
            "action": "assert", "finding": _attested(
                f"demo.odc.rel.box.{name}", _rel_fid(R_BOX, name), answers[R_BOX])},
            "successor": {"id": successor, "predecessor": rel_head}})
        rel_head = successor
        for fact in NEW_ANSWERS_RELATIVE:
            if fact == R_BOX or answers.get(fact) is None:
                continue
            add("assertion", {"finding": _attested(
                f"demo.odc.rel.{fact.rsplit('.', 1)[-1]}.{name}", _rel_fid(fact, name), answers[fact])})
    if relative_closed:
        add("assertion", {"finding": _attested(
            "demo.odc.rel.closure", f"{R_CLOSE}|family-horizon={rel_head},tax-year={YEAR}", True)})

    for fact, answer in return_answers.items():
        if answer is None:
            continue
        add("assertion", {"finding": _attested(
            f"demo.odc.ret.{fact.rsplit('.', 1)[-1]}", f"{fact}|tax-year={YEAR}", answer)})


def _complete(acts: list[dict[str, object]]) -> list[dict[str, object]]:
    """Adds the W-2 box 2 family, closes the other box 4 families and the bottom-line answers, as the
    child tax credit presentation does, so the return is complete on v55 and on v56."""
    acts = _add_box2_only(acts, employer="demo.cgd.t2.employer", slip="demo.cgd.t2.w2", amount=0.0)
    _close_empty(acts, family="tax.us.2025.w2-box2", version="v1",
                 closure_fact="tax.us.2025.w2-box2.source-closure", horizon="demo.odc.complete.w2box2")
    _close_other_box4_families(acts, skip={"w2-box2"})
    return _add_bottom_line_answers(acts, estimated=0.0, applied_2026=0.0)


def _rel_fid(fact_type: str, name: str) -> str:
    return fact_id_for(fact_type, (("dependent", name), ("tax-year", YEAR)))


def build(
    *,
    wages: float,
    filing_status: str = "single",
    children: Mapping[str, Mapping[str, str]] | None = None,
    relatives: Mapping[str, Mapping[str, str]] | None = None,
    return_answers: Mapping[str, str | None] | None = None,
    child_closed: bool = True,
    relative_closed: bool = True,
    can_be_claimed: str | None = "no",
    ctc_closed: bool = True,
) -> list[dict[str, object]]:
    kids = dict(children or {})
    ctc_kids = {name: {k: v for k, v in answers.items() if k in CHILD_TYPES}
                for name, answers in kids.items()}
    ret: dict[str, str | None] = {TP: "yes", F2555: "yes"}
    if filing_status == JOINT_STATUS:
        ret[SP] = "yes"
    if children or relatives:
        # An other dependent is present: the return answer says the rosters are read.
        ret[OD] = "no"
    ret.update(return_answers or {})
    odc_side = {k: ret[k] for k in (TP, SP, F2555) if k in ret}
    ctc_side = {k: v for k, v in ret.items() if k not in (TP, SP, F2555)}
    raw = ctc_build_acts(wages=wages, filing_status=filing_status, children=ctc_kids,
                         closed_roster=ctc_closed, can_be_claimed=cast(Any, can_be_claimed),
                         return_answers=ctc_side)
    _odc_extras(raw, kids, relatives or {}, child_closed=child_closed,
                relative_closed=relative_closed, return_answers=odc_side)
    return raw


def run_v56(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    finished = _finish(acts, package_path=PACKAGE_V56, package_version="v56",
                       release_path=RELEASE_V54, release_version="v54", note=run_id)
    return _run_surface(finished, SURFACE_V56, run_id)


def _expect(row: dict[str, Any] | None) -> dict[str, Any]:
    assert row is not None, "expected a blocked row"
    return row


class PackageChain(unittest.TestCase):
    def test_v56_validates_against_the_corpus(self) -> None:
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            body = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(body, dict) and isinstance(body.get("id"), str) and isinstance(body.get("version"), str):
                corpus[(body["id"], body["version"])] = body
        package = json.loads(PACKAGE_V56.read_text(encoding="utf-8"))
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(result.ok, str(getattr(result, "issues", "")))

    def test_v56_is_listed_with_registry_v54_and_release_v54(self) -> None:
        package = json.loads(PACKAGE_V56.read_text(encoding="utf-8"))
        registry = json.loads(REGISTRY_V54.read_text(encoding="utf-8"))
        listed = [row for row in registry["packages"] if row["id"] == package["id"] and row["version"] == "v56"]
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]["checksum"], package["package_checksum"])
        release = json.loads(RELEASE_V54.read_text(encoding="utf-8"))
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(REGISTRY_V54.read_bytes()).hexdigest())
        adoption = json.loads(ADOPTION_V56.read_text(encoding="utf-8"))
        self.assertEqual(adoption["payload"]["package"]["checksum"], package["package_checksum"])
        self.assertEqual(adoption["payload"]["release"]["checksum"], hashlib.sha256(RELEASE_V54.read_bytes()).hexdigest())

    def test_earlier_registry_and_v55_are_unchanged(self) -> None:
        registry = json.loads(REGISTRY_V53.read_text(encoding="utf-8"))
        v55 = json.loads((CONTENT / "package.core-calculations.v55.json").read_text(encoding="utf-8"))
        listed = [row for row in registry["packages"] if row["id"] == v55["id"] and row["version"] == "v55"]
        self.assertEqual(listed[0]["checksum"], v55["package_checksum"])

    def test_rule_files_stay_under_5kb(self) -> None:
        for path in sorted(CONTENT.glob("rule.odc-*.json")):
            self.assertLessEqual(path.stat().st_size, 5000, path.name)

    def test_static_required_versus_read_passes_on_v56(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/required_versus_read.py"), "static"],
            cwd=str(ROOT), capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


class ComputedRows(unittest.TestCase):
    """Every computed row of the other-dependent case table, on v56."""

    def test_each_computed_row_matches_schedule_8812(self) -> None:
        table = _load_case_table()
        for case in table.CASES:
            with self.subTest(case=case.label):
                status = JOINT_STATUS if case.status == "joint" else "single"
                children: dict[str, dict[str, str]] = {}
                relatives: dict[str, dict[str, str]] = {}
                for n in range(case.under17_ssn):
                    children[f"demo-child-{n + 1}"] = ctc_child()
                for n in range(case.odc):
                    if case.label.startswith("K3"):
                        children[f"demo-child-{len(children) + 1}"] = odc_child_itin()
                    elif case.label.startswith("K4"):
                        relatives[f"demo-dependent-{n + 1}"] = relative()
                    else:
                        children[f"demo-child-{len(children) + 1}"] = odc_child()
                acts = build(wages=float(case.agi), filing_status=status, children=children,
                             relatives=relatives)
                pubs, blocked = run_v56(acts, f"row-{case.label[:3].strip().lower()}")
                engine_tax = int(value(pubs, TAX))
                expected = table.compute(table.Case(case.label, case.status, case.agi, engine_tax,
                                                    case.under17_ssn, case.odc))
                self.assertEqual(int(value(pubs, L7)), expected["l7"], "line 7")
                self.assertEqual(int(value(pubs, L8)), expected["l8"], "line 8")
                self.assertEqual(int(value(pubs, LINE19)), expected["l19"], "line 19")
                self.assertEqual(int(value(pubs, L6)), case.odc, "line 6")


STATUSES = ("single", JOINT_STATUS, "married_filing_separately", "head_of_household",
            "qualifying_surviving_spouse")
ONE_ODC = {"demo-child-1": odc_child()}


class ChildAndRelativeCases(unittest.TestCase):
    def test_v55_child_tax_credit_only_return_gets_the_v55_result_on_v56(self) -> None:
        """A child-tax-credit-only return: the v55 answers, complete as the v55 presentation is, plus
        two children marked no for the credit with no TIN answer. Nothing blocks on v55 or v56 (no
        artifact is skipped), and line 19 on v56 equals the v55 value."""
        kids = {
            "demo-child-1": without(ctc_child(), C_TIN),
            "demo-child-2": without(ctc_child(), C_TIN),
        }
        self.assertEqual(kids["demo-child-1"][C_BOX], "no")
        acts55 = _complete(ctc_build_acts(wages=75000.0, children={
            name: {k: v for k, v in answers.items() if k in CHILD_TYPES} for name, answers in kids.items()}))
        pubs55, blocked55 = run_v55(acts55, "v55-set-on-v55")
        acts56 = _complete(build(wages=75000.0, children=kids, return_answers={OD: "yes"}))
        pubs56, blocked56 = run_v56(acts56, "v55-set-on-v56")
        self.assertEqual(blocked55, [])
        self.assertEqual(blocked56, [])
        self.assertEqual(int(value(pubs55, LINE19)), 4400)
        self.assertEqual(int(value(pubs56, LINE19)), 4400)
        self.assertEqual(int(value(pubs56, COUNT_CTC)), int(value(pubs55, COUNT_CTC)))

    def test_married_relative_filing_separately_qualifies(self) -> None:
        pubs, _ = run_v56(build(wages=30000.0, filing_status="married_filing_separately",
                                relatives={"demo-dependent-1": relative()}), "married-separate")
        self.assertEqual(int(value(pubs, R_CNT)), 1)
        self.assertEqual(int(value(pubs, LINE19)), 500)

    def test_child_marked_while_no_other_dependent_is_yes_blocks(self) -> None:
        acts = build(wages=30000.0, children=ONE_ODC, return_answers={OD: "yes"})
        _, blocked = run_v56(acts, "conflict-child")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child-marked-conflict"))

    def test_relative_marked_while_no_other_dependent_is_yes_blocks(self) -> None:
        acts = build(wages=30000.0, relatives={"demo-dependent-1": relative()}, return_answers={OD: "yes"})
        _, blocked = run_v56(acts, "conflict-rel")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-relative-marked-conflict"))

    def test_child_roster_closure_omitted_blocks_the_line_6_path(self) -> None:
        pubs, blocked = run_v56(build(wages=30000.0, children=ONE_ODC, child_closed=False), "no-child-closure")
        row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child-count"))
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertIn("tax.us.2025.odc.child-roster", str(row["missing"]))
        self.assertNotIn(LINE19, pubs)

    def test_relative_roster_closure_omitted_blocks_the_line_6_path(self) -> None:
        pubs, blocked = run_v56(build(wages=30000.0, relatives={"demo-dependent-1": relative()},
                                      relative_closed=False), "no-rel-closure")
        row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-relative-count"))
        self.assertEqual(row["code"], "SOURCE_SET_UNCLOSED")
        self.assertIn("tax.us.2025.odc.relative-roster", str(row["missing"]))
        self.assertNotIn(LINE19, pubs)

    def test_no_other_dependent_yes_reads_no_roster_and_needs_no_closure(self) -> None:
        pubs, _ = run_v56(build(wages=30000.0, children={}, child_closed=False,
                                relative_closed=False, return_answers={OD: "yes"}), "od-yes-no-closure")
        self.assertEqual(int(value(pubs, L6)), 0)
    def test_seventeen_year_old_alone_is_one_other_dependent(self) -> None:
        pubs, blocked = run_v56(build(wages=30000.0, children=ONE_ODC), "aged17-alone")
        self.assertEqual(int(value(pubs, C_CNT)), 1)
        self.assertEqual(int(value(pubs, L7)), 500)
        self.assertEqual(int(value(pubs, LINE19)), 500)

    def test_itin_child_alone_is_one_other_dependent(self) -> None:
        pubs, _ = run_v56(build(wages=30000.0, children={"demo-child-1": odc_child_itin()}), "itin-alone")
        self.assertEqual(int(value(pubs, C_CNT)), 1)
        self.assertEqual(int(value(pubs, LINE19)), 500)

    def test_parent_alone_is_one_other_dependent(self) -> None:
        pubs, _ = run_v56(build(wages=30000.0, relatives={"demo-dependent-1": relative()}), "parent-alone")
        self.assertEqual(int(value(pubs, R_CNT)), 1)
        self.assertEqual(int(value(pubs, LINE19)), 500)

    def test_child_under_17_with_seventeen_year_old_adds_both_credits(self) -> None:
        kids = {"demo-child-1": ctc_child(), "demo-child-2": ONE_ODC["demo-child-1"]}
        pubs, _ = run_v56(build(wages=30000.0, children=kids), "both")
        self.assertEqual(int(value(pubs, COUNT_CTC)), 1)
        self.assertEqual(int(value(pubs, L7)), 500)
        self.assertEqual(int(value(pubs, LINE19)), min(2700, int(value(pubs, TAX))))

    def test_parent_with_child_under_17_adds_both(self) -> None:
        pubs, _ = run_v56(build(wages=30000.0, children={"demo-child-1": ctc_child()},
                                relatives={"demo-dependent-1": relative()}), "parent-and-child")
        self.assertEqual(int(value(pubs, L6)), 1)
        self.assertEqual(int(value(pubs, LINE19)), min(2700, int(value(pubs, TAX))))

    def test_each_failing_test_blocks_the_relative(self) -> None:
        for fact in (R_GI, R_SUP, R_TIN, R_CIT, R_NM, R_NQC, R_REL):
            with self.subTest(fact=fact):
                _, blocked = run_v56(build(wages=30000.0, relatives={"demo-dependent-1": relative(**{fact: "no"})}),
                                     f"rel-{fact.rsplit('.', 1)[-1]}")
                _expect(blocked_by(blocked, "tax.us.2025.rule.odc-relative.counts"))

    def test_child_failing_residency_with_box_blocks(self) -> None:
        children = {"demo-child-1": odc_child(**{RES: "no"})}
        _, blocked = run_v56(build(wages=30000.0, children=children), "res-no")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child.counts"))

    def test_both_boxes_block(self) -> None:
        children = {"demo-child-1": ctc_child(**{C_BOX: "yes", U17: "no"})}
        _, blocked = run_v56(build(wages=30000.0, children=children), "both-boxes")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child.counts"))

    def test_credit_box_on_a_seventeen_year_old_blocks(self) -> None:
        children = {"demo-child-1": ctc_child(**{U17: "no"})}
        _, blocked = run_v56(build(wages=30000.0, children=children), "ctc-box-17")
        _expect(blocked_by(blocked, "tax.us.2025.rule.ctc-child.counts"))

    def test_other_dependent_box_on_a_child_who_passes_every_test_blocks(self) -> None:
        children = {"demo-child-1": odc_child(**{U17: "yes"})}
        _, blocked = run_v56(build(wages=30000.0, children=children), "odc-passes")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child.counts"))

    def test_child_without_ssn_or_tin_blocks(self) -> None:
        children = {"demo-child-1": odc_child_itin(**{C_TIN: "no"})}
        _, blocked = run_v56(build(wages=30000.0, children=children), "no-tin")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child.counts"))

    def test_married_or_disabled_or_multiple_support_relatives_are_outside(self) -> None:
        for label, over in (("married", {R_NM: "no"}), ("disabled-high-income", {R_GI: "no"}),
                            ("multiple-support", {R_SUP: "no"})):
            with self.subTest(label=label):
                _, blocked = run_v56(build(wages=30000.0, relatives={"demo-dependent-1": relative(**over)}),
                                     f"out-{label[:4]}")
                _expect(blocked_by(blocked, "tax.us.2025.rule.odc-relative.counts"))

    def test_nonresident_alien_filer_is_outside(self) -> None:
        pubs, blocked = run_v56(build(wages=30000.0, children=ONE_ODC, return_answers={NRA: "no"}), "nra-no")
        _expect(blocked_by(blocked, "tax.us.2025.rule.odc-return-gate"))
        self.assertNotIn(LINE19, pubs)

    def test_roster_not_closed_blocks(self) -> None:
        pubs, blocked = run_v56(build(wages=30000.0, children=ONE_ODC, child_closed=False), "open")
        self.assertTrue(blocked)
        self.assertNotIn(LINE19, pubs)

    def test_closed_empty_rosters_give_no_other_dependent_credit(self) -> None:
        pubs, _ = run_v56(build(wages=30000.0, children={}), "empty")
        self.assertEqual(int(value(pubs, L6)), 0)
        self.assertEqual(int(value(pubs, LINE19)), 0)


COUNT_CTC = "tax.us.2025.ctc.child-count"


def _outside_class_acts(over: dict[str, str | None], *, status: str = "single",
                        can_be_claimed: str | None = "no") -> list[dict[str, object]]:
    """A 17-year-old marked child and a parent, with one return answer changed."""
    return _complete(build(wages=30000.0, filing_status=status, children={"demo-child-1": odc_child()},
                           relatives={"demo-dependent-1": relative()}, return_answers=over,
                           can_be_claimed=can_be_claimed))


class GatesGovernLineNineteen(unittest.TestCase):
    """The return gates feed line 6, so a failing or missing exclusion answer keeps line 19 unpublished."""

    def test_control_with_every_answer_passing_publishes_line_19(self) -> None:
        pubs, blocked = run_v56(_outside_class_acts({}), "gate-control")
        self.assertEqual(int(value(pubs, LINE19)), 1000)
        self.assertEqual(blocked, [])

    def test_each_failing_answer_leaves_line_19_unpublished(self) -> None:
        cases: list[tuple[str, dict[str, Any]]] = [
            ("taxpayer-tin-no", {"over": {TP: "no"}}),
            ("form-2555-no", {"over": {F2555: "no"}}),
            ("nonresident-alien-no", {"over": {NRA: "no"}}),
            ("could-be-claimed-yes", {"over": {}, "can_be_claimed": "yes"}),
        ]
        for label, case in cases:
            with self.subTest(case=label):
                acts = _outside_class_acts(case.get("over", {}), can_be_claimed=case.get("can_be_claimed", "no"))
                pubs, blocked = run_v56(acts, f"gate-{label}")
                self.assertNotIn(LINE19, pubs)
                self.assertNotIn(L6, pubs)
                self.assertTrue(blocked)

    def test_each_omitted_answer_leaves_line_19_unpublished(self) -> None:
        for fact in (TP, F2555, NRA):
            with self.subTest(fact=fact):
                pubs, _ = run_v56(_outside_class_acts({fact: None}), f"gate-omit-{fact.rsplit('.', 1)[-1][:8]}")
                self.assertNotIn(LINE19, pubs)
        with self.subTest(fact="could-be-claimed"):
            pubs, _ = run_v56(_outside_class_acts({}, can_be_claimed=None), "gate-omit-cbc")
            self.assertNotIn(LINE19, pubs)

    def test_joint_spouse_answer_no_or_omitted_leaves_line_19_unpublished(self) -> None:
        overs: list[dict[str, str | None]] = [{SP: "no"}, {SP: None}]
        for over in overs:
            with self.subTest(over=over):
                pubs, _ = run_v56(_outside_class_acts(over, status=JOINT_STATUS), f"gate-sp-{len(over)}")
                self.assertNotIn(LINE19, pubs)

    def test_child_tax_credit_only_return_is_unaffected_by_the_other_dependent_gates(self) -> None:
        """Taxpayer TIN no is an other-dependent answer; with no other dependent it is not read."""
        kids = {"demo-child-1": ctc_child(), "demo-child-2": ctc_child()}
        pubs, blocked = run_v56(_complete(build(wages=75000.0, children=kids, return_answers={TP: "no"})),
                                "ctc-only-tp-no")
        self.assertEqual(int(value(pubs, LINE19)), 4400)
        self.assertEqual(int(value(pubs, COUNT_CTC)), 2)
        self.assertEqual(blocked, [])



class OmittedAnswers(unittest.TestCase):
    """Each new and reused answer, omitted on every filing status where it can be required."""

    def test_child_identification_omitted_blocks_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                children = {"demo-child-1": without(odc_child(), C_TIN)}
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=children),
                                     f"tin-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child.identity-met"))
                self.assertIn(C_TIN, str(row))

    def test_relative_answers_omitted_name_the_missing_fact_on_every_status(self) -> None:
        for status in STATUSES:
            for fact in R_TESTS_A + R_TESTS_B:
                with self.subTest(status=status, fact=fact):
                    rel = {"demo-dependent-1": without(relative(), fact)}
                    _, blocked = run_v56(build(wages=30000.0, filing_status=status, relatives=rel),
                                         f"rel-{fact.rsplit('.', 1)[-1][:6]}-{status[:4]}")
                    # The relative's own tests are per-subject; the first fact of each group is the
                    # subject, so an omitted subject answer is named by the counting rule (the rule
                    # that reads the group), and any other omitted answer by the group's rule.
                    group = "tests-a-met" if fact in R_TESTS_A else "tests-b-met"
                    subject = R_TESTS_A[0] if fact in R_TESTS_A else R_TESTS_B[0]
                    counts = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-relative.counts"))
                    if fact == subject:
                        self.assertIn(f"tax.us.2025.odc.dependent.{group}", str(counts["missing"]))
                    else:
                        row = _expect(blocked_by(blocked, f"tax.us.2025.rule.odc-relative.{group}"))
                        self.assertIn(fact, str(row["missing"]))

    def test_taxpayer_identification_omitted_blocks_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           return_answers={TP: None}), f"tp-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-return-gate"))
                self.assertIn(TP, row["missing"])

    def test_relative_roster_closure_omitted_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status,
                                           relatives={"demo-dependent-1": relative()}, relative_closed=False),
                                     f"rclose-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-relative-count"))
                self.assertIn("tax.us.2025.odc.relative-roster", str(row["missing"]))

    def test_child_roster_closure_omitted_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           child_closed=False), f"cclose-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-child-count"))
                self.assertIn("tax.us.2025.odc.child-roster", str(row["missing"]))

    def test_spouse_identification_is_required_only_on_a_joint_return(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           return_answers={SP: None}), f"sp-{status[:6]}")
                row = blocked_by(blocked, "tax.us.2025.rule.odc-spouse-gate")
                if status == JOINT_STATUS:
                    assert row is not None
                    self.assertIn(SP, row["missing"])
                else:
                    self.assertIsNone(row)

    def test_form_2555_omitted_blocks_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           return_answers={F2555: None}), f"f2555-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-return-gate"))
                self.assertIn(F2555, row["missing"])

    def test_nonresident_alien_answer_omitted_blocks_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           return_answers={NRA: None}), f"nra-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-return-gate"))
                self.assertIn(NRA, row["missing"])

    def test_could_be_claimed_answer_omitted_blocks_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           can_be_claimed=None), f"cbc-{status[:6]}")
                row = _expect(blocked_by(blocked, "tax.us.2025.rule.odc-return-gate"))
                self.assertIn(CAN_CLAIM, row["missing"])

    def test_puerto_rico_answer_omitted_names_it_on_every_status(self) -> None:
        for status in STATUSES:
            with self.subTest(status=status):
                _, blocked = run_v56(build(wages=30000.0, filing_status=status, children=ONE_ODC,
                                           return_answers={PR: None}), f"pr-{status[:6]}")
                self.assertTrue(any(PR in str(row.get("missing", "")) for row in blocked))


class CreditUnchangedForChildrenOnly(unittest.TestCase):
    def test_child_tax_credit_case_is_unchanged_on_v56(self) -> None:
        kids = {"demo-child-1": ctc_child(), "demo-child-2": ctc_child()}
        pubs56, _ = run_v56(build(wages=75000.0, children=kids), "ctc-only-v56")
        pubs55, _ = run_v55(ctc_build_acts(wages=75000.0, children=kids), "ctc-only-v55")
        self.assertEqual(int(value(pubs56, LINE19)), int(value(pubs55, LINE19)))
        self.assertEqual(int(value(pubs56, LINE19)), 4400)
        self.assertEqual(int(value(pubs56, COUNT_CTC)), 2)
        self.assertEqual(int(value(pubs56, L6)), 0)
