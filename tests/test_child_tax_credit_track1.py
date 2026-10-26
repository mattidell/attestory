"""Track 1a: the 2025 child tax credit and Schedule 8812 Part I, Worksheet A and Part II-A on core v55.

Proved through the real coordinator on core-calculations v55. The credit's
family is separate from the earned income family (a second closure mapping on
the EIC family is refused by the engine). Figures for the computed rows come
from ``docs/phases/engine-breadth/milestones/child-tax-credit-evidence/ctc_case_table.py``,
the committed Schedule 8812 arithmetic, applied to the engine's own inputs.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping, cast

import unittest

from packages.derivation.package_validation import validate_package
from packages.derivation.loader import DerivationSchemas
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for

from tests.test_refund_or_amount_owed_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    _act,
    _attested,
    _finish,
    _load,
    _sdd,
)
from tests.test_eic_qualifying_children_track1 import (
    CHILD_KIND as EIC_CHILD_KIND,
    _build_acts as _eic_build_acts,
    _finish_v54,
    _run_surface,
    PACKAGE_V54,
    REGISTRY_V52,
    RELEASE_V52,
    SURFACE_V54,
    passing_child as eic_passing_child,
)

PACKAGE_V55 = CONTENT / "package.core-calculations.v55.json"
REGISTRY_V53 = CONTENT / "published-packages.v53.json"
RELEASE_V53 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v53.json"
SURFACE_V55 = PublicationSurface(RELEASE_DIR, REGISTRY_V53, CONTENT)
ADOPTION_V55 = ROOT / "packages/sample_data/child_tax_credit/adoptions/adopt-core-v55-current.json"
CASE_TABLE = ROOT / "docs/phases/engine-breadth/milestones/child-tax-credit-evidence/ctc_case_table.py"

YEAR = "2025"
EIC_FAMILY = "tax.us.2025.eic.child-roster"
EIC_CLOSURE = "tax.us.2025.eic.child-roster.source-closure"
EIC_AGE = "tax.us.2025.eic.child.age"
EIC_RES = "tax.us.2025.eic.child.residency"
EIC_NOT_QC = "tax.us.2025.eic.not-qualifying-child-of-another"
EIC_SP_SSN = "tax.us.2025.eic.spouse-valid-ssn"
EIC_SEP = "tax.us.2025.eic.separated-spouse"
USER = "demo.user.filer-1"
CHILD_KIND = EIC_CHILD_KIND
FAMILY = "tax.us.2025.ctc.child-roster"
CLOSURE = "tax.us.2025.ctc.child-roster.source-closure"
COUNT = "tax.us.2025.ctc.child-count"
LINE19 = "tax.us.2025.ctc.form1040-line19"
LINE28 = "tax.us.2025.ctc.form1040-line28"
TAX = "tax.us.2025.tax.total-tax"
AFTER = "tax.us.2025.tax.after-nonrefundable-credits"
PAY2831 = "tax.us.2025.payments.lines28-31"
L4 = "tax.us.2025.ctc.sch8812.line-4"
L6 = "tax.us.2025.ctc.sch8812.line-6"
L2D = "tax.us.2025.ctc.sch8812.line-2d"
GATE_B = "tax.us.2025.ctc.sch8812.part-ii-b-gate"
L17 = "tax.us.2025.ctc.sch8812.line-17"
L20 = "tax.us.2025.ctc.sch8812.line-20"
L12 = "tax.us.2025.ctc.sch8812.line-12"

# Shared with the earned income roster (same fact types, unchanged meaning).
REL = "tax.us.2025.eic.child.relationship"
JOINT = "tax.us.2025.eic.child.joint-return"
SSN = "tax.us.2025.eic.child.ssn"
OTHER = "tax.us.2025.eic.child.another-may-claim"
# Credit-only per-child answers.
U17 = "tax.us.2025.ctc.child.under-17"
RES = "tax.us.2025.ctc.child.lived-with-you"
SUP = "tax.us.2025.ctc.child.no-over-half-support"
CIT = "tax.us.2025.ctc.child.citizen-or-resident"
CLAIM = "tax.us.2025.ctc.child.claimed-as-dependent"
CHILD_TYPES = (REL, JOINT, SSN, OTHER, U17, RES, SUP, CIT, CLAIM)

# Filer and return answers.
TP_SSN = "tax.us.2025.eic.taxpayer-valid-ssn"
NRA = "tax.us.2025.eic.not-nonresident-alien"
NOT_DEP = "tax.us.2025.eic.not-claimable-as-dependent"
UNSUP = "tax.us.2025.eic.no-unsupported-situations"
OD = "tax.us.2025.ctc.no-other-dependent"
SPOUSE = "tax.us.2025.ctc.spouse-ssn-or-itin"
PR = "tax.us.2025.ctc.no-puerto-rico-or-4563-exclusion"
L2931 = "tax.us.2025.lines29-31-scope.no-other-refundable-credits"
FILER_ANSWERS = (TP_SSN, NRA, NOT_DEP, UNSUP, OD, PR, L2931)

CASE_LABEL_BY_CHILD = {"demo-child-1": "one", "demo-child-2": "two", "demo-child-3": "three"}


def child_fid(fact_type: str, child: str) -> str:
    return fact_id_for(fact_type, (("child", child), ("tax-year", YEAR)))


def passing_child() -> dict[str, str]:
    return {REL: "yes", JOINT: "yes", SSN: "yes", OTHER: "no", U17: "yes", RES: "yes",
            SUP: "yes", CIT: "yes", CLAIM: "yes"}


def _load_case_table() -> Any:
    spec = importlib.util.spec_from_file_location("ctc_case_table", CASE_TABLE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the case table")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_acts(
    *,
    wages: float,
    filing_status: str = "single",
    children: Mapping[str, Mapping[str, str]] | None = None,
    return_answers: Mapping[str, str | None] | None = None,
    closed_roster: bool = True,
    eic_roster: bool = True,
    eic_spouse_ssn: str | None = "yes",
    interest: float | None = None,
    can_be_claimed: str = "no",
) -> list[dict[str, object]]:
    raw = cast(list[dict[str, object]], _sdd()._senior_acts(
        wages=wages, filing_status=filing_status, can_be_claimed=can_be_claimed))
    if interest is not None:
        raw = _with_taxable_interest(raw, interest)
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-questions.bundle.json")}))
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-child-roster.bundle.json")}))
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("ctc-child-roster.bundle.json")}))
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("ctc-return-questions.bundle.json")}))

    answers: dict[str, str | None] = {fid: "yes" for fid in FILER_ANSWERS}
    if filing_status == "married_filing_jointly":
        # The earned income credit's dependent answer is not asked on a joint return, and
        # the credit's filer gate reads the standard-deduction answer instead.
        answers.pop(NOT_DEP, None)
        answers[SPOUSE] = "yes"
    if return_answers:
        answers.update(return_answers)
    for fid, val in answers.items():
        if val is None:
            continue
        raw.append(_act(len(raw), "assertion", {"finding": _attested(
            f"demo.{fid.split('.')[-1]}", f"{fid}|tax-year={YEAR}", val)}))

    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    kids = dict(children or {})
    for child in kids:
        raw.append(_act(len(raw), "entity-introduced", {"entity": {
            "schema": "entity.v1", "id": child, "kind": CHILD_KIND, "label": f"Synthetic {child}"}}))
    if eic_roster:
        _add_eic_roster(raw, kids, filing_status, spouse_ssn=eic_spouse_ssn)
    raw.append(_act(len(raw), "horizon-genesis", {
        "family": {"id": FAMILY, "version": "v1"}, "scope": scope_key, "horizon_id": "demo.ctc.h0"}))
    horizon = "demo.ctc.h0"
    for idx, (child, c_answers) in enumerate(kids.items()):
        successor = f"demo.ctc.h{idx + 1}"
        if c_answers.get(CLAIM) is not None:
            raw.append(_act(len(raw), "member-transition", {
                "family": {"id": FAMILY, "version": "v1"},
                "scope": scope_key,
                "member": {"action": "assert", "finding": _attested(
                    f"demo.claim.{child}", child_fid(CLAIM, child), c_answers[CLAIM])},
                "successor": {"id": successor, "predecessor": horizon},
            }))
            horizon = successor
        for fid in CHILD_TYPES:
            if fid in (REL, CLAIM) or fid not in c_answers or c_answers[fid] is None:
                continue
            raw.append(_act(len(raw), "assertion", {"finding": _attested(
                f"demo.{fid.split('.')[-1]}.{child}", child_fid(fid, child), c_answers[fid])}))
    if closed_roster:
        raw.append(_act(len(raw), "assertion", {"finding": _attested(
            "demo.ctc.closure", f"{CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)}))
    return raw


def _with_taxable_interest(acts: list[dict[str, object]], amount: float) -> list[dict[str, object]]:
    """Replaces the base's closed-empty 1099-INT box 1 family with one statement of
    ``amount`` (taxable interest, so AGI rises and earned income does not)."""
    kept: list[dict[str, object]] = []
    for act in acts:
        payload = cast(dict[str, Any], act.get("payload", {}))
        if act.get("kind") == "horizon-genesis" and payload.get("family", {}).get("id") == "tax.us.2025.f1099int.b1":
            continue
        if act.get("kind") == "assertion" and str(payload.get("finding", {}).get("fact_id", "")).startswith(
                "tax.us.2025.f1099int.b1.source-closure"):
            continue
        kept.append(act)
    acts = kept

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099int.bundle.json")})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.ctc.payer", "kind": "tax.us.interest-payer", "label": "Synthetic payer"}})
    add("entity-introduced", {"entity": {"schema": "entity.v1", "id": "demo.ctc.statement", "kind": "tax.us.1099int-statement", "label": "Synthetic 1099-INT"}})
    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    add("horizon-genesis", {"family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"}, "scope": scope_key, "horizon_id": "demo.ctc.intb1.h0"})
    add("member-transition", {
        "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"}, "scope": scope_key,
        "member": {"action": "assert", "finding": _attested(
            "demo.ctc.int.box1",
            "tax.us.2025.f1099int.box1-interest|payer=demo.ctc.payer,statement=demo.ctc.statement,tax-year=2025",
            amount)},
        "successor": {"id": "demo.ctc.intb1.h1", "predecessor": "demo.ctc.intb1.h0"}})
    add("assertion", {"finding": _attested(
        "demo.ctc.int.closure", f"tax.us.2025.f1099int.b1.source-closure|family-horizon=demo.ctc.intb1.h1,tax-year={YEAR}", True)})
    return acts


def _add_eic_roster(acts: list[dict[str, object]], kids: Mapping[str, Mapping[str, str]], filing_status: str, *, spouse_ssn: str | None = "yes") -> None:
    """The earned income roster for the same children. Each relationship fact is a member
    of this family only: the kernel allows one membership per fact, so the credit family's
    member is the claimed-as-dependent fact instead."""

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("assertion", {"finding": _attested("demo.eic.not-qc", f"{EIC_NOT_QC}|tax-year={YEAR}", "yes")})
    if filing_status == "married_filing_jointly" and spouse_ssn is not None:
        add("assertion", {"finding": _attested("demo.eic.sp-ssn", f"{EIC_SP_SSN}|tax-year={YEAR}", spouse_ssn)})
    if filing_status in ("married_filing_separately", "head_of_household"):
        add("assertion", {"finding": _attested("demo.eic.sep", f"{EIC_SEP}|tax-year={YEAR}", "yes")})
    scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
    add("horizon-genesis", {"family": {"id": EIC_FAMILY, "version": "v1"}, "scope": scope_key, "horizon_id": "demo.eic.h0"})
    horizon = "demo.eic.h0"
    for idx, child in enumerate(kids):
        successor = f"demo.eic.h{idx + 1}"
        add("member-transition", {
            "family": {"id": EIC_FAMILY, "version": "v1"}, "scope": scope_key,
            "member": {"action": "assert", "finding": _attested(
                f"demo.eic.rel.{child}", child_fid(REL, child), "yes")},
            "successor": {"id": successor, "predecessor": horizon}})
        horizon = successor
        add("assertion", {"finding": _attested(f"demo.eic.age.{child}", child_fid(EIC_AGE, child), "yes")})
        add("assertion", {"finding": _attested(f"demo.eic.res.{child}", child_fid(EIC_RES, child), "yes")})
    add("assertion", {"finding": _attested(
        "demo.eic.closure", f"{EIC_CLOSURE}|family-horizon={horizon},tax-year={YEAR}", True)})


def run_v55(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    finished = _finish(acts, package_path=PACKAGE_V55, package_version="v55",
                       release_path=RELEASE_V53, release_version="v53", note=run_id)
    return _run_surface(finished, SURFACE_V55, run_id)


def value(pubs: dict[str, dict[str, Any]], symbol: str) -> Decimal:
    finding = pubs.get(symbol)
    if finding is None:
        raise AssertionError(f"missing publication {symbol}")
    return Decimal(str(finding["value"]))


def blocked_by(blocked: list[dict[str, Any]], artifact: str) -> dict[str, Any] | None:
    for row in blocked:
        if str(row.get("artifact_id", "")) == artifact:
            return row
    return None


def _expect(row: dict[str, Any] | None) -> dict[str, Any]:
    assert row is not None, "expected a blocked row"
    return row


def kids(n: int, **overrides: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for i in range(1, n + 1):
        out[f"demo-child-{i}"] = passing_child()
    return out


class PackageChain(unittest.TestCase):
    def test_v55_validates_and_is_listed_with_its_release(self) -> None:
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            value_ = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value_, dict) and isinstance(value_.get("id"), str) and isinstance(value_.get("version"), str):
                corpus[(value_["id"], value_["version"])] = value_
        package = json.loads(PACKAGE_V55.read_text(encoding="utf-8"))
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(result.ok, [issue.code for issue in result.issues])
        registry = json.loads(REGISTRY_V53.read_text(encoding="utf-8"))
        packages = [(row["id"], row["version"]) for row in registry["packages"]]
        self.assertEqual(packages, sorted(packages))
        citizens = [(row["id"], row["version"]) for row in registry["citizens"]]
        self.assertEqual(citizens, sorted(citizens))
        listed = next(row for row in registry["packages"]
                      if row["id"] == "tax.us.2025.package.core-calculations" and row["version"] == "v55")
        self.assertEqual(listed["checksum"], package["package_checksum"])
        release = json.loads(RELEASE_V53.read_text(encoding="utf-8"))
        self.assertEqual(release["package_registry_sha256"], hashlib.sha256(REGISTRY_V53.read_bytes()).hexdigest())
        adoption = json.loads(ADOPTION_V55.read_text(encoding="utf-8"))
        self.assertEqual(adoption["payload"]["package"]["checksum"], package["package_checksum"])
        self.assertEqual(adoption["payload"]["release"]["checksum"], hashlib.sha256(RELEASE_V53.read_bytes()).hexdigest())

    def test_earlier_packages_and_registry_are_unchanged(self) -> None:
        registry = json.loads(REGISTRY_V52.read_text(encoding="utf-8"))
        v54 = json.loads(PACKAGE_V54.read_text(encoding="utf-8"))
        listed = next(row for row in registry["packages"]
                      if row["id"] == "tax.us.2025.package.core-calculations" and row["version"] == "v54")
        self.assertEqual(listed["checksum"], v54["package_checksum"])
        release_v52 = json.loads(RELEASE_V52.read_text(encoding="utf-8"))
        self.assertEqual(release_v52["package_registry_sha256"],
                         hashlib.sha256(REGISTRY_V52.read_bytes()).hexdigest())

    def test_rule_files_stay_under_5kb(self) -> None:
        for path in sorted(CONTENT.glob("rule.ctc-*.json")):
            self.assertLessEqual(path.stat().st_size, 5000, path.name)

    def test_static_required_versus_read_passes_on_v55(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "tools/required_versus_read.py"), "static"],
            cwd=str(ROOT), capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


class ComputedRows(unittest.TestCase):
    """Every computed row of the case table, through the real coordinator on v55."""

    def test_each_computed_row_matches_schedule_8812_on_the_engine_inputs(self) -> None:
        table = _load_case_table()
        for case in table.CASES:
            if case.other_dependents or case.no_ssn_children:
                continue
            with self.subTest(case=case.label):
                wages = float(case.agi)
                status = "married_filing_jointly" if case.joint else "single"
                acts = build_acts(wages=wages, filing_status=status, children=kids(case.under17))
                pubs, blocked = run_v55(acts, f"row-{case.label[:3].strip().lower()}")
                tax = int(value(pubs, TAX))
                expected = table.compute(table.Case(case.label, case.joint, int(wages), tax, int(wages), case.under17))
                if str(expected.get("status", "")).startswith("REFUSED"):
                    # Part II-B is computed on v55; with no W-2 box answers it blocks
                    # naming the box 4 fact, and line 28 is not published.
                    self.assertNotIn(LINE28, pubs)
                    total = _expect(blocked_by(blocked, "tax.us.2025.rule.w2-box4-total"))
                    self.assertIn("tax.us.2025.w2-box4", total["missing"])
                    continue
                self.assertEqual(int(value(pubs, LINE19)), expected["total"] - int(expected.get("line28") or 0),
                                 "line 19")
                self.assertEqual(int(value(pubs, LINE28)), int(expected.get("line28") or 0), "line 28")
                self.assertEqual(int(value(pubs, COUNT)), case.under17)


class ChildAndRosterCases(unittest.TestCase):
    def test_child_aged_17_claimed_blocks_as_other_dependent(self) -> None:
        children = kids(1)
        children["demo-child-2"] = {**passing_child(), U17: "no"}
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=children), "aged17")
        self.assertNotIn(COUNT, pubs)
        self.assertIsNotNone(blocked_by(blocked, "tax.us.2025.rule.ctc-child.counts") or
                             blocked_by(blocked, "tax.us.2025.rule.ctc-child-count"))

    def test_child_without_valid_ssn_claimed_blocks(self) -> None:
        children = kids(1)
        children["demo-child-2"] = {**passing_child(), SSN: "no"}
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=children), "no-ssn")
        self.assertNotIn(COUNT, pubs)
        self.assertIsNotNone(blocked_by(blocked, "tax.us.2025.rule.ctc-child.counts"))

    def test_another_person_may_claim_blocks(self) -> None:
        children = kids(1)
        children["demo-child-2"] = {**passing_child(), OTHER: "yes"}
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=children), "other-claim")
        self.assertNotIn(COUNT, pubs)

    def test_unclaimed_child_living_elsewhere_is_not_counted_and_does_not_block(self) -> None:
        children = kids(1)
        children["demo-child-2"] = {**passing_child(), CLAIM: "no", RES: "no"}
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=children), "unclaimed")
        self.assertEqual(int(value(pubs, COUNT)), 1)
        self.assertIsNone(blocked_by(blocked, "tax.us.2025.rule.ctc-child.counts"))

    def test_roster_not_closed_blocks(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=kids(1), closed_roster=False), "open")
        self.assertNotIn(COUNT, pubs)
        self.assertIsNotNone(blocked_by(blocked, "tax.us.2025.rule.ctc-child-count"))

    def test_closed_empty_roster_gives_no_credit(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=30000.0, children={}), "empty")
        self.assertEqual(int(value(pubs, COUNT)), 0)
        self.assertEqual(int(value(pubs, LINE19)), 0)
        self.assertEqual(int(value(pubs, LINE28)), 0)

    def test_each_missing_child_answer_blocks_with_the_fact_named(self) -> None:
        rules = {U17: "under-17", RES: "lived-with-you", SUP: "no-support", CIT: "citizen", CLAIM: "claimed"}
        for fid, short in rules.items():
            with self.subTest(fact=fid):
                children = kids(1)
                children["demo-child-1"] = {k: v for k, v in passing_child().items() if k != fid}
                _, blocked = run_v55(build_acts(wages=30000.0, children=children), f"miss-{short}")
                count_row = blocked_by(blocked, "tax.us.2025.rule.ctc-child.counts")
                count_row = _expect(count_row)
                self.assertIn(f"tax.us.2025.ctc.child.{short}-met", count_row["missing"])


class ReturnCases(unittest.TestCase):
    def test_other_dependent_no_blocks_the_line_6_rule(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=kids(1), return_answers={OD: "no"}), "od-no")
        row = blocked_by(blocked, "tax.us.2025.rule.ctc-sch8812-line-6")
        row = _expect(row)
        self.assertNotIn(LINE19, pubs)

    def test_missing_no_other_dependent_names_it(self) -> None:
        _, blocked = run_v55(build_acts(wages=30000.0, children=kids(1), return_answers={OD: None}), "od-missing")
        row = blocked_by(blocked, "tax.us.2025.rule.ctc-sch8812-line-6")
        row = _expect(row)
        self.assertIn(OD, row["missing"])

    def test_missing_puerto_rico_answer_names_it(self) -> None:
        _, blocked = run_v55(build_acts(wages=30000.0, children=kids(1), return_answers={PR: None}), "pr-missing")
        row = blocked_by(blocked, "tax.us.2025.rule.ctc-sch8812-line-2d")
        row = _expect(row)
        self.assertIn(PR, row["missing"])

    def test_missing_lines_29_31_answer_names_it(self) -> None:
        _, blocked = run_v55(build_acts(wages=30000.0, children=kids(1), return_answers={L2931: None}), "l2931-missing")
        row = blocked_by(blocked, "tax.us.2025.rule.form1040-lines28-31")
        row = _expect(row)
        self.assertIn(L2931, row["missing"])

    def test_joint_return_spouse_answer_required_with_a_child(self) -> None:
        _, blocked = run_v55(build_acts(wages=30000.0, filing_status="married_filing_jointly",
                                        children=kids(1), return_answers={SPOUSE: None}), "spouse-missing")
        row = blocked_by(blocked, "tax.us.2025.rule.ctc-spouse-gate")
        row = _expect(row)
        self.assertIn(SPOUSE, row["missing"])

    def test_single_return_needs_no_spouse_answer(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=kids(1), return_answers={SPOUSE: None}), "single-no-spouse")
        self.assertIsNone(blocked_by(blocked, "tax.us.2025.rule.ctc-spouse-gate"))
        self.assertIn(LINE19, pubs)

    def test_three_children_below_line_20_need_the_w2_box_answers(self) -> None:
        """Track 1b computes Part II-B: without W-2 box 4 and 6 answers the return blocks,
        naming the box 4 fact through the box total rule. Line 28 is not published."""
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=kids(3)), "part-ii-b")
        self.assertNotIn(LINE28, pubs)
        total = _expect(blocked_by(blocked, "tax.us.2025.rule.w2-box4-total"))
        # The box 4 family is not closed in this return, so the block names the family.
        self.assertIn("tax.us.2025.w2-box4", total["missing"])

    def test_three_children_at_or_above_line_17_are_computed(self) -> None:
        pubs, _ = run_v55(build_acts(wages=60000.0, children=kids(3)), "three-high")
        self.assertEqual(int(value(pubs, COUNT)), 3)
        self.assertIsNotNone(pubs.get(LINE28))


class EarlierPackagesUnchanged(unittest.TestCase):
    def test_earned_income_credit_publications_match_v54(self) -> None:
        children = {"demo-child-1": eic_passing_child(), "demo-child-2": eic_passing_child()}
        acts_v54 = _finish_v54(_eic_build_acts(wages=15000.0, filing_status="single", children=children),
                               note="eic-v54")
        pubs_v54, _ = _run_surface(acts_v54, SURFACE_V54, "eic-v54")
        acts_v55 = _finish(_eic_build_acts(wages=15000.0, filing_status="single", children=children),
                           package_path=PACKAGE_V55, package_version="v55",
                           release_path=RELEASE_V53, release_version="v53", note="eic-v55")
        pubs_v55, _ = _run_surface(acts_v55, SURFACE_V55, "eic-v55")
        def eic_only(pubs: dict[str, dict[str, Any]]) -> dict[str, Any]:
            return {k: v["value"] for k, v in pubs.items()
                    if k.startswith("tax.us.2025.eic.") or k.endswith("payments.line27a")}

        eic_v54, eic_v55 = eic_only(pubs_v54), eic_only(pubs_v55)
        self.assertTrue(eic_v54)
        self.assertEqual(eic_v54, eic_v55)


if __name__ == "__main__":
    unittest.main()


NO_LINE19 = "tax.us.2025.direct-ftc-scope.no-line19-ctc-odc"
FILER_GATE = "tax.us.2025.rule.ctc-filer-gate"
SSN_GATE = "tax.us.2025.rule.ctc-filer-ssn-gate"
ONE_CHILD = {"demo-child-1": passing_child()}


TP_SSN_KEY = "tax.us.2025.eic.taxpayer-valid-ssn"
L18A = "tax.us.2025.ctc.sch8812.line-18a"


def kids_two() -> dict[str, dict[str, str]]:
    return {"demo-child-1": passing_child(), "demo-child-2": passing_child()}


class FilerGateSsnAndDependent(unittest.TestCase):
    """Final review: the filer gate reads the return-level standard-deduction answer
    (a joint return asks no EIC dependent answer), and the SSN passes on either spouse."""

    def test_joint_return_without_the_eic_dependent_answer_computes(self) -> None:
        kids = {"demo-child-1": passing_child(), "demo-child-2": passing_child()}
        pubs, blocked = run_v55(build_acts(wages=75000.0, filing_status="married_filing_jointly", children=kids), "joint-no-eic-dep")
        self.assertIsNone(blocked_by(blocked, FILER_GATE))
        self.assertEqual(int(value(pubs, LINE19)), 4400)

    def test_joint_taxpayer_ssn_not_valid_spouse_valid_computes(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=75000.0, filing_status="married_filing_jointly", children=kids_two(),
                                           return_answers={TP_SSN_KEY: "no"}, eic_spouse_ssn="yes"), "joint-tp-no-sp-yes")
        self.assertIsNone(blocked_by(blocked, FILER_GATE))
        self.assertEqual(int(value(pubs, LINE19)), 4400)

    def test_joint_taxpayer_ssn_not_valid_spouse_not_valid_blocks(self) -> None:
        _, blocked = run_v55(build_acts(wages=75000.0, filing_status="married_filing_jointly", children=kids_two(),
                                        return_answers={TP_SSN_KEY: "no"}, eic_spouse_ssn="no"), "joint-both-no")
        row = _expect(blocked_by(blocked, SSN_GATE))
        self.assertEqual(row["code"], "DEPENDENCY_INVALID")

    def test_joint_taxpayer_ssn_not_valid_spouse_answer_missing_names_it(self) -> None:
        _, blocked = run_v55(build_acts(wages=75000.0, filing_status="married_filing_jointly", children=kids_two(),
                                        return_answers={TP_SSN_KEY: "no"}, eic_spouse_ssn=None), "joint-sp-missing")
        row = _expect(blocked_by(blocked, SSN_GATE))
        self.assertIn(EIC_SP_SSN, row["missing"])

    def test_joint_taxpayer_ssn_valid_needs_no_eic_spouse_answer(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=75000.0, filing_status="married_filing_jointly", children=kids_two(),
                                           eic_spouse_ssn=None), "joint-tp-yes-no-sp")
        self.assertIsNone(blocked_by(blocked, FILER_GATE))
        self.assertEqual(int(value(pubs, LINE19)), 4400)

    def test_single_taxpayer_ssn_not_valid_blocks(self) -> None:
        _, blocked = run_v55(build_acts(wages=30000.0, children=ONE_CHILD, return_answers={TP_SSN_KEY: "no"}), "single-tp-no")
        self.assertIsNotNone(blocked_by(blocked, SSN_GATE))

    def test_standard_deduction_dependent_yes_blocks(self) -> None:
        _, blocked = run_v55(build_acts(wages=30000.0, children=ONE_CHILD, can_be_claimed="yes"), "claimable")
        self.assertIsNotNone(blocked_by(blocked, FILER_GATE))


class FamilyWithChildrenDoesNotNeedTheLine19Absence(unittest.TestCase):
    def test_no_line19_absence_is_not_required(self) -> None:
        pubs, blocked = run_v55(build_acts(wages=30000.0, children=ONE_CHILD), "no-line19")
        for row in blocked:
            self.assertNotIn(NO_LINE19, row.get("missing", []), row.get("artifact_id"))
        self.assertIn(LINE19, pubs)
        self.assertIn("tax.us.2025.tax.total-tax", pubs)


class AgiAboveEarnedIncome(unittest.TestCase):
    """Taxable interest raises AGI and not earned income, so a swapped reference fails.
    Single, one child under 17 with a valid SSN, standard deduction $15,750 (i1040gi-2025.txt:232)."""

    def test_earned_10000_agi_15000_takes_15_percent_of_earned(self) -> None:
        """Taxable 0 (15,000 - 15,750), so tax 0 and line 19 is 0. Line 16a = 2,200; line 16b = 1,700;
        line 17 = 1,700. Line 18a = 10,000 (earned); line 19 = 7,500; line 20 = 15% = 1,125.
        Line 28 = min(1,700, 1,125) = 1,125. (AGI 15,000 would give min(1,700, 1,875) = 1,700.)"""
        pubs, _ = run_v55(build_acts(wages=10000.0, children=ONE_CHILD, interest=5000.0), "agi-c")
        self.assertEqual(int(value(pubs, "tax.us.2025.income.agi")), 15000)
        self.assertEqual(int(value(pubs, L18A)), 10000)
        self.assertEqual(int(value(pubs, LINE19)), 0)
        self.assertEqual(int(value(pubs, LINE28)), 1125)

    def test_earned_2000_agi_22000_has_no_additional_credit(self) -> None:
        """Taxable 22,000 - 15,750 = 6,250; Tax Table 628 (i1040gi-2025.txt:4815, single).
        Line 19 = min(2,200, 628) = 628. Earned 2,000 is not above 2,500: line 19 blank, line 20 = 0, line 28 = 0.
        (AGI 22,000 as earned would give 15% of 19,500 = 2,925 and line 28 = 1,700.)"""
        pubs, _ = run_v55(build_acts(wages=2000.0, children=ONE_CHILD, interest=20000.0), "agi-a")
        self.assertEqual(int(value(pubs, "tax.us.2025.income.agi")), 22000)
        self.assertEqual(int(value(pubs, L18A)), 2000)
        self.assertEqual(int(value(pubs, "tax.us.2025.tax.total-tax")), 628)
        self.assertEqual(int(value(pubs, LINE19)), 628)
        self.assertEqual(int(value(pubs, LINE28)), 0)

    def test_earned_2500_agi_22500_has_no_additional_credit(self) -> None:
        """Taxable 22,500 - 15,750 = 6,750; Tax Table 678 (i1040gi-2025.txt:4825, single).
        Line 19 = 678. Earned exactly 2,500 is not more than 2,500: line 28 = 0.
        (AGI 22,500 as earned would give 15% of 20,000 = 3,000 and line 28 = 1,700.)"""
        pubs, _ = run_v55(build_acts(wages=2500.0, children=ONE_CHILD, interest=20000.0), "agi-b")
        self.assertEqual(int(value(pubs, "tax.us.2025.income.agi")), 22500)
        self.assertEqual(int(value(pubs, L18A)), 2500)
        self.assertEqual(int(value(pubs, "tax.us.2025.tax.total-tax")), 678)
        self.assertEqual(int(value(pubs, LINE19)), 678)
        self.assertEqual(int(value(pubs, LINE28)), 0)
