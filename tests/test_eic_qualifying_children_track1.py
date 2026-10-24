"""Track 1: 2025 earned income credit with qualifying children.

Proved through the real coordinator on core-calculations v54. Every figure
comes from the printed 2025 EIC Table and parameter.eic-table-2025.v2.json.
"""

from __future__ import annotations

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast, Mapping

import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.loader import DerivationSchemas
from packages.derivation.package_validation import validate_package
from packages.derivation.production_resolver import PublicationSurface
from packages.kernel.facts import fact_id_for
from tests.test_refund_or_amount_owed_track1 import (
    CONTENT,
    RELEASE_DIR,
    ROOT,
    USER,
    _act,
    _attested,
    _finish,
    _load,
    _sdd,
    _value,
)
from tests.test_earned_income_credit_track1 import (
    PACKAGE_V53,
    REGISTRY_V51,
    RELEASE_V51,
    SURFACE_V53,
    _closure,
)

PACKAGE_V54 = CONTENT / "package.core-calculations.v54.json"
REGISTRY_V52 = CONTENT / "published-packages.v52.json"
RELEASE_V52 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v52.json"
SURFACE_V54 = PublicationSurface(RELEASE_DIR, REGISTRY_V52, CONTENT)
ADOPTION_V54 = (
    ROOT
    / "packages/sample_data/earned_income_credit/adoptions/adopt-core-v54-current.json"
)

YEAR = "2025"
CHILD_KIND = "tax.us.eic-child"
FAMILY = "tax.us.2025.eic.child-roster"
CLOSURE = "tax.us.2025.eic.child-roster.source-closure"

LINE27A = "tax.us.2025.payments.line27a"
L1 = "tax.us.2025.eic.worksheet-a.line-1"
L2 = "tax.us.2025.eic.worksheet-a.line-2"
L3 = "tax.us.2025.eic.worksheet-a.line-3"
L5 = "tax.us.2025.eic.worksheet-a.line-5"
L6 = "tax.us.2025.eic.worksheet-a.line-6"
COUNT = "tax.us.2025.eic.qualifying-child-count"
COL_COUNT = "tax.us.2025.eic.column-count"
TABLE_KEY = "tax.us.2025.eic.table-key"
ELIG = "tax.us.2025.eic.eligibility-result"
GATE = "tax.us.2025.eic.gate-result"
EARLY = "tax.us.2025.eic.early-stop"

# Child fact types
REL = "tax.us.2025.eic.child.relationship"
AGE = "tax.us.2025.eic.child.age"
RES = "tax.us.2025.eic.child.residency"
JOINT = "tax.us.2025.eic.child.joint-return"
SSN = "tax.us.2025.eic.child.ssn"
OTHER = "tax.us.2025.eic.child.another-may-claim"

# Filer fact types
TP_SSN = "tax.us.2025.eic.taxpayer-valid-ssn"
SP_SSN = "tax.us.2025.eic.spouse-valid-ssn"
NRA = "tax.us.2025.eic.not-nonresident-alien"
NOT_QC = "tax.us.2025.eic.not-qualifying-child-of-another"
UNSUP = "tax.us.2025.eic.no-unsupported-situations"
SEP = "tax.us.2025.eic.separated-spouse"
L2831 = "tax.us.2025.lines28-31-scope.no-other-refundable-credits"

# Childless filer facts
FILER_AGE = "tax.us.2025.eic.age-25-under-65"
FILER_HOME = "tax.us.2025.eic.main-home-in-us"
FILER_NOT_DEP = "tax.us.2025.eic.not-claimable-as-dependent"


def child_fid(fact_type: str, child: str) -> str:
    return fact_id_for(fact_type, (("child", child), ("tax-year", YEAR)))


def _eic_missing(blocked: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in blocked:
        for name in row.get("missing", []):
            if str(name).startswith("tax.us.2025.eic."):
                names.append(str(name))
    return names


def _eic_blocked(blocked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        row for row in blocked
        if str(row.get("artifact_id", "")).startswith("tax.us.2025.rule.eic")
        or any(str(m).startswith("tax.us.2025.eic") for m in row.get("missing", []))
    ]


def _finish_v54(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    return _finish(
        acts,
        package_path=PACKAGE_V54,
        package_version="v54",
        release_path=RELEASE_V52,
        release_version="v52",
        note=note,
    )


def _run_surface(
    acts: list[dict[str, object]],
    surface: PublicationSurface,
    run_id: str,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=surface,
            output_name="out.json",
        )
        pubs: dict[str, dict[str, Any]] = {}
        for pub in outcome.publications or ():
            pubs[str(pub.finding["symbol"])] = pub.finding
        blocked: list[dict[str, Any]] = []
        if outcome.output_path is not None:
            report = json.loads(outcome.output_path.read_text(encoding="utf-8"))
            for row in report.get("dispositions", []):
                if row.get("disposition") == "blocked":
                    blocked.append(row)
        return pubs, blocked


def _build_acts(
    *,
    wages: float,
    filing_status: str = "single",
    children: dict[str, dict[str, str]] | None = None,
    filer_answers: Mapping[str, str | None] | None = None,
    closed_roster: bool = True,
    omit_bundle: bool = False,
) -> list[dict[str, object]]:
    raw = cast(
        list[dict[str, object]],
        _sdd()._senior_acts(wages=wages, filing_status=filing_status),
    )
    raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-questions.bundle.json")}))
    if not omit_bundle:
        raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-child-roster.bundle.json")}))

    # Default passing answers for filer
    answers: dict[str, str | None] = {
        TP_SSN: "yes",
        NRA: "yes",
        NOT_QC: "yes",
        UNSUP: "yes",
        L2831: "yes",
    }
    if filing_status == "married_filing_jointly":
        answers[SP_SSN] = "yes"
    if filing_status in ("married_filing_separately", "head_of_household"):
        answers[SEP] = "yes"
    if filer_answers:
        answers.update(filer_answers)

    for fid, val in answers.items():
        if val is None:
            continue
        suffix = fid.split(".")[-1]
        raw.append(
            _act(
                len(raw),
                "assertion",
                {"finding": _attested(f"demo.{suffix}", f"{fid}|tax-year={YEAR}", val)},
            )
        )

    # Child roster
    if children is not None:
        for child in children:
            raw.append(
                _act(
                    len(raw),
                    "entity-introduced",
                    {
                        "entity": {
                            "schema": "entity.v1",
                            "id": child,
                            "kind": CHILD_KIND,
                            "label": f"Synthetic child {child}",
                        }
                    },
                )
            )

        scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
        raw.append(
            _act(
                len(raw),
                "horizon-genesis",
                {
                    "family": {"id": FAMILY, "version": "v1"},
                    "scope": scope_key,
                    "horizon_id": "demo.probe.h0",
                },
            )
        )
        horizon = "demo.probe.h0"
        for idx, (child, c_answers) in enumerate(children.items()):
            successor = f"demo.probe.h{idx + 1}"
            raw.append(
                _act(
                    len(raw),
                    "member-transition",
                    {
                        "family": {"id": FAMILY, "version": "v1"},
                        "scope": scope_key,
                        "member": {
                            "action": "assert",
                            "finding": _attested(
                                f"demo.rel.{child}",
                                child_fid(REL, child),
                                c_answers.get(REL, "yes"),
                            ),
                        },
                        "successor": {"id": successor, "predecessor": horizon},
                    },
                )
            )
            horizon = successor

            for fid in (AGE, RES, JOINT, SSN, OTHER):
                if fid in c_answers and c_answers[fid] is not None:
                    suf = fid.split(".")[-1]
                    raw.append(
                        _act(
                            len(raw),
                            "assertion",
                            {"finding": _attested(f"demo.{suf}.{child}", child_fid(fid, child), c_answers[fid])},
                        )
                    )

        if closed_roster:
            raw.append(
                _act(
                    len(raw),
                    "assertion",
                    {
                        "finding": _attested(
                            "demo.closure",
                            f"{CLOSURE}|family-horizon={horizon},tax-year={YEAR}",
                            True,
                        )
                    },
                )
            )
    elif closed_roster:
        # Empty closed roster
        scope_key = {"tax-year": YEAR, "subject": "demo.primary"}
        raw.append(
            _act(
                len(raw),
                "horizon-genesis",
                {
                    "family": {"id": FAMILY, "version": "v1"},
                    "scope": scope_key,
                    "horizon_id": "demo.probe.h0",
                },
            )
        )
        raw.append(
            _act(
                len(raw),
                "assertion",
                {
                    "finding": _attested(
                        "demo.closure",
                        f"{CLOSURE}|family-horizon=demo.probe.h0,tax-year={YEAR}",
                        True,
                    )
                },
            )
        )

    return raw


def passing_child() -> dict[str, str]:
    return {
        REL: "yes",
        AGE: "yes",
        RES: "yes",
        JOINT: "yes",
        SSN: "yes",
        OTHER: "no",
    }


class PackageChain(unittest.TestCase):
    def test_v54_validates_and_adoption_pins_the_release(self) -> None:
        corpus: dict[tuple[str, str], dict[str, Any]] = {}
        for path in CONTENT.glob("*.json"):
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict) and isinstance(value.get("id"), str) and isinstance(value.get("version"), str):
                corpus[(value["id"], value["version"])] = value
        package = json.loads(PACKAGE_V54.read_text(encoding="utf-8"))
        result = validate_package(package, corpus, DerivationSchemas())
        self.assertTrue(result.ok, [issue.code for issue in result.issues])
        registry = json.loads(REGISTRY_V52.read_text(encoding="utf-8"))
        packages = [(row["id"], row["version"]) for row in registry["packages"]]
        self.assertEqual(packages, sorted(packages))
        citizens = [(row["id"], row["version"]) for row in registry["citizens"]]
        self.assertEqual(citizens, sorted(citizens))
        listed = next(
            row for row in registry["packages"]
            if row["id"] == "tax.us.2025.package.core-calculations" and row["version"] == "v54"
        )
        self.assertEqual(listed["checksum"], package["package_checksum"])
        adoption = json.loads(ADOPTION_V54.read_text(encoding="utf-8"))
        self.assertEqual(adoption["payload"]["package"]["checksum"], package["package_checksum"])
        self.assertEqual(
            adoption["payload"]["release"]["checksum"],
            hashlib.sha256(RELEASE_V52.read_bytes()).hexdigest(),
        )

    def test_rule_files_stay_under_5kb(self) -> None:
        names = [
            path.name
            for path in CONTENT.glob("rule.eic-*.json")
        ]
        for name in names:
            size = (CONTENT / name).stat().st_size
            self.assertLessEqual(size, 5000, name)


class QualifyingChildrenCreditTests(unittest.TestCase):
    def test_children_phase_in_plateau_phase_out(self) -> None:
        """Covers 1, 2, 3, and 4 children on phase-in, plateau, and phase-out for single and joint.

        All figures match the printed 2025 EIC Table:
          1 child:
            wages $5,000  (phase-in): single=$1,709, joint=$1,709
            wages $15,000 (plateau):  single=$4,328, joint=$4,328
            wages $35,000 (phase-out): single=$2,462, joint=$3,600
          2 children:
            wages $5,000  (phase-in): single=$2,010, joint=$2,010
            wages $15,000 (plateau):  single=$6,010, joint=$6,010
            wages $35,000 (phase-out): single=$4,693, joint=$6,193
          3 children:
            wages $5,000  (phase-in): single=$2,261, joint=$2,261
            wages $15,000 (plateau):  single=$6,761, joint=$6,761
            wages $35,000 (phase-out): single=$5,587, joint=$7,087
          4 children (capped at 3 column):
            wages $15,000 (plateau):  single=$6,761, joint=$6,761
        """
        cases = [
            # 1 child single
            (1, "single", 5000.0, Decimal("1709"), 1, "other-1"),
            (1, "single", 15000.0, Decimal("4328"), 1, "other-1"),
            (1, "single", 35000.0, Decimal("2462"), 1, "other-1"),
            # 1 child joint
            (1, "married_filing_jointly", 5000.0, Decimal("1709"), 1, "joint-1"),
            (1, "married_filing_jointly", 15000.0, Decimal("4328"), 1, "joint-1"),
            (1, "married_filing_jointly", 35000.0, Decimal("3600"), 1, "joint-1"),
            # 2 children single
            (2, "single", 5000.0, Decimal("2010"), 2, "other-2"),
            (2, "single", 15000.0, Decimal("6010"), 2, "other-2"),
            (2, "single", 35000.0, Decimal("4693"), 2, "other-2"),
            # 2 children joint
            (2, "married_filing_jointly", 5000.0, Decimal("2010"), 2, "joint-2"),
            (2, "married_filing_jointly", 15000.0, Decimal("6010"), 2, "joint-2"),
            (2, "married_filing_jointly", 35000.0, Decimal("6193"), 2, "joint-2"),
            # 3 children single
            (3, "single", 5000.0, Decimal("2261"), 3, "other-3"),
            (3, "single", 15000.0, Decimal("6761"), 3, "other-3"),
            (3, "single", 35000.0, Decimal("5587"), 3, "other-3"),
            # 3 children joint
            (3, "married_filing_jointly", 5000.0, Decimal("2261"), 3, "joint-3"),
            (3, "married_filing_jointly", 15000.0, Decimal("6761"), 3, "joint-3"),
            (3, "married_filing_jointly", 35000.0, Decimal("7087"), 3, "joint-3"),
            # 4 children single (uses 3-child column)
            (4, "single", 15000.0, Decimal("6761"), 3, "other-3"),
            # 4 children joint (uses 3-child column)
            (4, "married_filing_jointly", 15000.0, Decimal("6761"), 3, "joint-3"),
        ]

        for num_kids, status, wages, expected_credit, expected_col, expected_key in cases:
            with self.subTest(num_kids=num_kids, status=status, wages=wages):
                kids = {f"demo-child-{i}": passing_child() for i in range(1, num_kids + 1)}
                acts = _finish_v54(
                    _build_acts(wages=wages, filing_status=status, children=kids),
                    note=f"{num_kids} kids {status} {wages}",
                )
                pubs, blocked = _run_surface(acts, SURFACE_V54, f"case-{num_kids}-{status}-{int(wages)}")
                self.assertEqual(_eic_missing(blocked), [], f"EIC missing on {num_kids} kids {status} {wages}")
                self.assertEqual(_value(pubs, COUNT), num_kids)
                self.assertEqual(_value(pubs, COL_COUNT), expected_col)
                self.assertEqual(pubs[TABLE_KEY]["value"], expected_key)
                self.assertEqual(_value(pubs, LINE27A), expected_credit)

    def test_child_failing_each_test(self) -> None:
        """A child failing relationship, age, residency, or joint return does not count."""
        for failed_test in (REL, AGE, RES, JOINT):
            with self.subTest(failed_test=failed_test):
                child_data = passing_child()
                child_data[failed_test] = "no"
                kids = {"demo-child-1": child_data}
                # Single filer age 30 so eligible for childless credit ($312 at $15,000 from table)
                filer_ans = {FILER_AGE: "yes", FILER_HOME: "yes", FILER_NOT_DEP: "yes"}
                acts = _finish_v54(
                    _build_acts(wages=15000.0, filing_status="single", children=kids, filer_answers=filer_ans),
                    note=f"failed {failed_test}",
                )
                pubs, blocked = _run_surface(acts, SURFACE_V54, f"fail-{failed_test.split('.')[-1]}")
                self.assertEqual(_eic_missing(blocked), [])
                self.assertEqual(_value(pubs, COUNT), 0)
                self.assertEqual(_value(pubs, COL_COUNT), 0)
                # At $15,000, 0-child credit is $312
                self.assertEqual(_value(pubs, LINE27A), Decimal("312"))

    def test_child_failing_other_claimant_blocks(self) -> None:
        """Another person may claim the child: blocks with DEPENDENCY_INVALID."""
        child_data = passing_child()
        child_data[OTHER] = "yes"
        kids = {"demo-child-1": child_data}
        acts = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids),
            note="other claimant blocks",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "other-claimant-blocks")
        self.assertTrue(len(_eic_blocked(blocked)) > 0, "Expected blocked disposition")
        codes = [b.get("code") for b in _eic_blocked(blocked)]
        self.assertIn("DEPENDENCY_INVALID", codes)

    def test_child_without_valid_ssn_not_counted_filer_gets_self_only_credit(self) -> None:
        """Child has no valid SSN: not counted; filer gets self-only credit when eligible."""
        child_data = passing_child()
        child_data[SSN] = "no"
        kids = {"demo-child-1": child_data}
        # Filer is eligible for childless credit at $9,000 wages ($649 from printed table)
        filer_ans = {FILER_AGE: "yes", FILER_HOME: "yes", FILER_NOT_DEP: "yes"}
        acts = _finish_v54(
            _build_acts(wages=9000.0, filing_status="single", children=kids, filer_answers=filer_ans),
            note="child no ssn self-only credit",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "child-no-ssn")
        self.assertEqual(_eic_missing(blocked), [])
        self.assertEqual(_value(pubs, COUNT), 0)
        self.assertEqual(_value(pubs, COL_COUNT), 0)
        self.assertEqual(_value(pubs, LINE27A), Decimal("649"))

    def test_child_answer_missing_blocks_and_names_fact(self) -> None:
        """Missing child answer blocks naming the fact."""
        child_data = passing_child()
        del child_data[AGE]  # Omit age answer
        kids = {"demo-child-1": child_data}
        acts = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids),
            note="missing child answer",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "child-answer-missing")
        self.assertTrue(len(_eic_blocked(blocked)) > 0)
        missing_facts = [f for b in _eic_blocked(blocked) for f in b.get("missing", [])]
        self.assertTrue(any("child.age" in str(f) for f in missing_facts), f"Expected child.age in {missing_facts}")

    def test_roster_not_closed_blocks(self) -> None:
        """Roster not closed blocks naming the closure fact."""
        kids = {"demo-child-1": passing_child()}
        acts = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids, closed_roster=False),
            note="unclosed roster",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "unclosed-roster")
        self.assertTrue(len(_eic_blocked(blocked)) > 0)
        codes = [b.get("code") for b in _eic_blocked(blocked)]
        self.assertIn("DEPENDENCY_ABSENT", codes)

    def test_mfs_and_hoh_with_and_without_separated_spouse(self) -> None:
        """MFS and HOH with qualifying children: separated-spouse answer controls."""
        for status in ("married_filing_separately", "head_of_household"):
            with self.subTest(status=status, variant="with_yes"):
                kids = {"demo-child-1": passing_child()}
                acts = _finish_v54(
                    _build_acts(wages=15000.0, filing_status=status, children=kids, filer_answers={SEP: "yes"}),
                    note=f"{status} sep yes",
                )
                pubs, blocked = _run_surface(acts, SURFACE_V54, f"{status}-sep-yes")
                self.assertEqual(_eic_missing(blocked), [])
                self.assertEqual(_value(pubs, COUNT), 1)
                self.assertEqual(_value(pubs, LINE27A), Decimal("4328"))

            with self.subTest(status=status, variant="with_no"):
                kids = {"demo-child-1": passing_child()}
                acts = _finish_v54(
                    _build_acts(wages=15000.0, filing_status=status, children=kids, filer_answers={SEP: "no"}),
                    note=f"{status} sep no",
                )
                pubs, blocked = _run_surface(acts, SURFACE_V54, f"{status}-sep-no")
                self.assertEqual(_eic_missing(blocked), [])
                self.assertEqual(_value(pubs, LINE27A), Decimal("0"))

            with self.subTest(status=status, variant="missing"):
                kids = {"demo-child-1": passing_child()}
                acts = _finish_v54(
                    _build_acts(wages=15000.0, filing_status=status, children=kids, filer_answers={SEP: None}),
                    note=f"{status} sep missing",
                )
                pubs, blocked = _run_surface(acts, SURFACE_V54, f"{status}-sep-missing")
                self.assertTrue(len(_eic_blocked(blocked)) > 0)
                missing = [f for b in _eic_blocked(blocked) for f in b.get("missing", [])]
                self.assertTrue(any(SEP in f for f in missing))

    def test_above_completed_amount_is_zero(self) -> None:
        """Wages above column completed amount gives $0 credit."""
        kids = {"demo-child-1": passing_child()}
        acts = _finish_v54(
            _build_acts(wages=70000.0, filing_status="single", children=kids),
            note="above completed",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "above-completed")
        self.assertEqual(_eic_missing(blocked), [])
        self.assertEqual(_value(pubs, LINE27A), Decimal("0"))

    def test_v53_childless_case_unchanged_on_v54(self) -> None:
        """Childless case on v54 produces identical result as v53."""
        filer_ans = {FILER_AGE: "yes", FILER_HOME: "yes", FILER_NOT_DEP: "yes"}
        acts = _finish_v54(
            _build_acts(wages=9000.0, filing_status="single", children=None, filer_answers=filer_ans),
            note="childless on v54",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "childless-v54")
        self.assertEqual(_eic_missing(blocked), [])
        self.assertEqual(_value(pubs, COUNT), 0)
        self.assertEqual(_value(pubs, COL_COUNT), 0)
        self.assertEqual(_value(pubs, LINE27A), Decimal("649"))

    def test_v53_run_unchanged(self) -> None:
        """A run on v53 package produces identical result."""
        raw = cast(
            list[dict[str, object]],
            _sdd()._senior_acts(wages=9000.0, filing_status="single"),
        )
        raw.append(_act(len(raw), "bundle-adoption", {"bundle": _load("eic-questions.bundle.json")}))
        for fid in (
            "tax.us.2025.eic.no-qualifying-child",
            TP_SSN, NRA, FILER_AGE, FILER_HOME, NOT_QC, FILER_NOT_DEP, UNSUP, L2831
        ):
            raw.append(
                _act(
                    len(raw),
                    "assertion",
                    {"finding": _attested(f"demo.{fid.split('.')[-1]}", f"{fid}|tax-year=2025", "yes")},
                )
            )
        acts = _finish(
            raw,
            package_path=PACKAGE_V53,
            package_version="v53",
            release_path=RELEASE_V51,
            release_version="v51",
            note="v53 unchanged run",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V53, "v53-run")
        self.assertEqual(_eic_missing(blocked), [])
        self.assertEqual(_value(pubs, LINE27A), Decimal("649"))


class RequiredWhereReadAndExplanationTests(unittest.TestCase):
    def test_runtime_pins_contain_every_required_answer(self) -> None:
        """On a credit path with children, every required answer is in line 27a's runtime pins."""
        kids = {
            "demo-child-1": passing_child(),
            "demo-child-2": passing_child(),
        }
        acts = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids),
            note="runtime pins test",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "runtime-pins")
        self.assertEqual(_eic_missing(blocked), [])
        self.assertEqual(_value(pubs, LINE27A), Decimal("6010"))

        closure = _closure(pubs, LINE27A)

        # Filer-level required answers
        required_filer_answers = [
            "tax.us.2025.eic.answer.taxpayer-valid-ssn",
            "tax.us.2025.eic.answer.not-nonresident-alien",
            "tax.us.2025.eic.answer.not-qualifying-child-of-another",
            "tax.us.2025.eic.answer.no-unsupported-situations",
        ]
        for sym in required_filer_answers:
            self.assertIn(pubs[sym]["id"], closure, f"{sym} must be in line 27a pin closure")

        # Per-child test findings in closure
        for child in ("demo-child-1", "demo-child-2"):
            for test in ("relationship-met", "age-met", "residency-met", "joint-return-met", "ssn-met", "other-claimant-clear", "counts"):
                child_matches = [
                    f for f in pubs.values()
                    if test in str(f.get("symbol", "")) and child in str(f.get("symbol", ""))
                ]
                self.assertTrue(len(child_matches) == 1, f"Missing pub for {test} {child}")
                self.assertIn(
                    child_matches[0]["id"],
                    closure,
                    f"{test} for {child} must be in line 27a pin closure",
                )

    def test_yes_to_no_correction_displaces_line_27a(self) -> None:
        """A yes-to-no correction of one child's answer displaces line 27a."""
        # Run with 2 children: line 27a is $6,010
        kids_2 = {
            "demo-child-1": passing_child(),
            "demo-child-2": passing_child(),
        }
        acts_2 = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids_2),
            note="2 kids",
        )
        pubs_2, _ = _run_surface(acts_2, SURFACE_V54, "displace-2-kids")
        self.assertEqual(_value(pubs_2, LINE27A), Decimal("6010"))

        # Correct child 2 age to "no": qualifying child count drops to 1, line 27a displaces to $4,328
        kids_corrected = {
            "demo-child-1": passing_child(),
            "demo-child-2": dict(passing_child(), **{AGE: "no"}),
        }
        acts_corrected = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids_corrected),
            note="child 2 corrected",
        )
        pubs_corrected, _ = _run_surface(acts_corrected, SURFACE_V54, "displace-corrected")
        self.assertEqual(_value(pubs_corrected, LINE27A), Decimal("4328"))
        self.assertNotEqual(pubs_2[LINE27A]["id"], pubs_corrected[LINE27A]["id"])

    def test_explanation_walk_two_children(self) -> None:
        """Verifies explanation walk from line 27a for a two-child case."""
        kids = {
            "demo-child-1": passing_child(),
            "demo-child-2": passing_child(),
        }
        acts = _finish_v54(
            _build_acts(wages=15000.0, filing_status="single", children=kids),
            note="explanation walk",
        )
        pubs, blocked = _run_surface(acts, SURFACE_V54, "walk-2-kids")
        self.assertEqual(_eic_missing(blocked), [])

        by_id = {finding["id"]: finding for finding in pubs.values()}
        visited: list[str] = []

        def walk(fid: str) -> None:
            f = by_id.get(fid)
            if not f:
                return
            sym = str(f.get("symbol", f.get("fact_id", fid)))
            visited.append(sym)
            for pin in f.get("pins", []):
                if pin.get("role") == "input":
                    walk(pin["id"])

        walk(pubs[LINE27A]["id"])

        # Check key waypoints in explanation walk:
        # Worksheet A line 6, Worksheet A line 2, table-key, column-count, qualifying-child-count,
        # and per-child counts and tests
        self.assertIn("tax.us.2025.payments.line27a", visited)
        self.assertIn("tax.us.2025.eic.eligibility-result", visited)
        self.assertIn("tax.us.2025.eic.gate-result", visited)
        self.assertIn("tax.us.2025.eic.worksheet-a.line-6", visited)
        self.assertIn("tax.us.2025.eic.worksheet-a.line-2", visited)
        self.assertIn("tax.us.2025.eic.table-key", visited)
        self.assertIn("tax.us.2025.eic.column-count", visited)
        self.assertIn("tax.us.2025.eic.qualifying-child-count", visited)


if __name__ == "__main__":
    unittest.main()
