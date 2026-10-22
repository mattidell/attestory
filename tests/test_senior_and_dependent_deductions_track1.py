"""Track 1: the 2025 enhanced deduction for seniors, proved through the real
coordinator on core-calculations v51.

Reuses the tax-on-taxable-income P0 probe's act-log builder (via
``tests.test_tax_on_taxable_income_track1``'s own dynamic loader) for the
base W-2-only return, then layers the senior-deduction fact types this
track adds. Pattern: ``tests/test_tax_on_taxable_income_track1.py``.
"""

from __future__ import annotations

import copy
import hashlib
import json
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

import unittest

from packages.derivation.live import live_coordinate_run
from packages.derivation.live_workspace import WorkspaceCapability
from packages.derivation.production_resolver import PublicationSurface

from tests import test_tax_on_taxable_income_track1 as toti

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "packages" / "content" / "tax" / "2025"
RELEASE_DIR = (
    ROOT
    / "packages"
    / "sample_data"
    / "student_loan_worksheet_integration"
    / "publication_surface"
    / "releases"
)
PACKAGE_V51 = CONTENT / "package.core-calculations.v51.json"
REGISTRY_V49 = CONTENT / "published-packages.v49.json"
RELEASE_V49 = RELEASE_DIR / "demo.release.sli-worksheet-integration.2025.v49.json"
SURFACE_V51 = PublicationSurface(RELEASE_DIR, REGISTRY_V49, CONTENT)

LINE_13B = "tax.us.2025.deductions.schedule-1a"
LINE_14 = "tax.us.2025.deductions.line-14"
LINE_15 = toti.TI
LINE_12E = "tax.us.2025.deductions.line-12e"
LINE_36A = "tax.us.2025.schedule1a.line36a-taxpayer"
LINE_36B = "tax.us.2025.schedule1a.line36b-spouse"
LINE_37 = "tax.us.2025.schedule1a.line37-enhanced-deduction-total"
PARTS_II_IV = "tax.us.2025.schedule1a.no-parts-ii-iv-deductions-declared"
TAXPAYER_SSN = "tax.us.2025.senior-deduction.taxpayer-valid-ssn"
SPOUSE_SSN = "tax.us.2025.senior-deduction.spouse-valid-ssn"
ITEMIZED = "tax.us.2025.deductions.itemized"


def _finish_v51(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    probe = toti._probe()
    pkg = json.loads(PACKAGE_V51.read_text(encoding="utf-8"))
    rel_csum = hashlib.sha256(RELEASE_V49.read_bytes()).hexdigest()
    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(probe._load_fixture_adoption())
    adoption["act_id"] = f"demo.sdd.adopt.{len(built):03d}"
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": "v51",
        "checksum": pkg["package_checksum"],
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v49",
        "checksum": rel_csum,
    }
    payload["audit"] = {"note": note}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = probe.USER
    return built


def _senior_acts(
    *,
    wages: float,
    filing_status: str = "single",
    taxpayer_over_65: bool = False,
    spouse_over_65: bool = False,
    taxpayer_blind: bool = False,
    spouse_blind: bool = False,
    taxpayer_ssn: str | None = None,
    spouse_ssn: str | None = None,
    parts_ii_iv: str | None = "yes",
    itemized: float | None = None,
) -> list[dict[str, object]]:
    probe = toti._probe()
    acts = probe._base_acts(wages=wages, filing_status=filing_status)

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(probe._act(len(acts), kind, payload))

    bundle = json.loads(
        (CONTENT / "senior-and-dependent-deductions.vocabulary.bundle.json").read_text(encoding="utf-8")
    )
    add("bundle-adoption", {"bundle": bundle})

    age_facts = {
        "taxpayer_over_65": ("tax.us.2025.taxpayer-over-65", taxpayer_over_65),
        "taxpayer_blind": ("tax.us.2025.taxpayer-blind", taxpayer_blind),
        "spouse_over_65": ("tax.us.2025.spouse-over-65", spouse_over_65),
        "spouse_blind": ("tax.us.2025.spouse-blind", spouse_blind),
    }
    for name, (fact_type, flag) in age_facts.items():
        if flag:
            add(
                "assertion",
                {"finding": probe._attested(f"demo.sdd.{name}", f"{fact_type}|tax-year=2025", True)},
            )

    if taxpayer_ssn is not None:
        add(
            "assertion",
            {"finding": probe._attested("demo.sdd.taxpayer-ssn", f"{TAXPAYER_SSN}|tax-year=2025", taxpayer_ssn)},
        )
    if spouse_ssn is not None:
        add(
            "assertion",
            {"finding": probe._attested("demo.sdd.spouse-ssn", f"{SPOUSE_SSN}|tax-year=2025", spouse_ssn)},
        )
    if parts_ii_iv is not None:
        add(
            "assertion",
            {"finding": probe._attested("demo.sdd.parts-ii-iv", f"{PARTS_II_IV}|tax-year=2025", parts_ii_iv)},
        )
    if itemized is not None:
        add(
            "assertion",
            {"finding": probe._attested("demo.sdd.itemized", f"{ITEMIZED}|tax-year=2025", itemized)},
        )

    return cast(list[dict[str, object]], acts)


def _run(acts: list[dict[str, object]], run_id: str) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    probe = toti._probe()
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=ROOT,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=probe.USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V51,
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


def _value(pubs: dict[str, dict[str, Any]], blocked: list[dict[str, Any]], symbol: str) -> Decimal:
    finding = pubs.get(symbol)
    if finding is None:
        raise AssertionError(f"missing {symbol}; blocked={blocked}")
    return Decimal(str(finding["value"]))


def _missing_names(blocked: list[dict[str, Any]], artifact_token: str) -> list[str]:
    for row in blocked:
        if artifact_token in str(row.get("artifact_id", "")):
            return cast(list[str], row.get("missing", []))
    return []


class SeniorDeductionTrack1Tests(unittest.TestCase):
    def test_case_1_single_60k(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=60000, taxpayer_over_65=True, taxpayer_ssn="yes"),
            "synthetic case 1: single, 66, AGI $60,000",
        )
        pubs, blocked = _run(acts, "demo.sdd.case1")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(6000))
        self.assertEqual(_value(pubs, blocked, LINE_14), Decimal(15750) + Decimal(2000) + Decimal(6000))
        self.assertEqual(_value(pubs, blocked, LINE_15), Decimal(60000) - (Decimal(17750) + Decimal(6000)))

    def test_case_2_single_95k(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=95000, taxpayer_over_65=True, taxpayer_ssn="yes"),
            "synthetic case 2: single, 66, AGI $95,000",
        )
        pubs, blocked = _run(acts, "demo.sdd.case2")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(4800))

    def test_case_3_single_175k_zero_crossing(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=175000, taxpayer_over_65=True, taxpayer_ssn="yes"),
            "synthetic case 3: single, 66, AGI $175,000 (zero crossing)",
        )
        pubs, blocked = _run(acts, "demo.sdd.case3")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(0))

    def test_case_boundary_exactly_at_threshold(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=75000, taxpayer_over_65=True, taxpayer_ssn="yes"),
            "synthetic boundary: single, 66, AGI exactly $75,000",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.boundary.threshold")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(6000))

    def test_case_joint_both_65_160k(self) -> None:
        acts = _finish_v51(
            _senior_acts(
                wages=160000,
                filing_status="married_filing_jointly",
                taxpayer_over_65=True,
                spouse_over_65=True,
                taxpayer_ssn="yes",
                spouse_ssn="yes",
            ),
            "synthetic case: joint, both 65+, AGI $160,000",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.joint.both")
        self.assertEqual(_value(pubs, blocked, LINE_36A), Decimal(5400))
        self.assertEqual(_value(pubs, blocked, LINE_36B), Decimal(5400))
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(10800))

    def test_case_joint_one_spouse_65(self) -> None:
        acts = _finish_v51(
            _senior_acts(
                wages=160000,
                filing_status="married_filing_jointly",
                taxpayer_over_65=True,
                spouse_over_65=False,
                taxpayer_ssn="yes",
            ),
            "synthetic case: joint, one spouse 65+",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.joint.one")
        self.assertEqual(_value(pubs, blocked, LINE_36A), Decimal(5400))
        self.assertEqual(_value(pubs, blocked, LINE_36B), Decimal(0))
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(5400))

    def test_case_joint_spouse_no_valid_ssn(self) -> None:
        acts = _finish_v51(
            _senior_acts(
                wages=160000,
                filing_status="married_filing_jointly",
                taxpayer_over_65=True,
                spouse_over_65=True,
                taxpayer_ssn="yes",
                spouse_ssn="no",
            ),
            "synthetic case: joint, both 65+, spouse lacks a valid SSN",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.joint.ssn")
        self.assertEqual(_value(pubs, blocked, LINE_36A), Decimal(5400))
        self.assertEqual(_value(pubs, blocked, LINE_36B), Decimal(0))
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(5400))
        self.assertFalse(
            [row for row in blocked if "schedule1a" in str(row.get("artifact_id", "")) or "line13b" in str(row.get("artifact_id", ""))],
            f"unexpected senior-deduction block: {blocked}",
        )

    def test_case_mfs_zero(self) -> None:
        acts = _finish_v51(
            _senior_acts(
                wages=80000,
                filing_status="married_filing_separately",
                taxpayer_over_65=True,
            ),
            "synthetic case: married filing separately, 66",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.mfs")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(0))
        self.assertFalse(
            [row for row in blocked if "schedule1a" in str(row.get("artifact_id", "")) or "line13b" in str(row.get("artifact_id", ""))],
            f"unexpected senior-deduction block: {blocked}",
        )

    def test_case_itemizing_still_applies(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=60000, taxpayer_over_65=True, taxpayer_ssn="yes", itemized=20000),
            "synthetic case: itemizing return with a 66-year-old",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.itemize")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(6000))
        self.assertEqual(_value(pubs, blocked, LINE_12E), Decimal(20000))

    def test_case_no_senior_no_ssn_answer_computes(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=50000),
            "synthetic case: no one 65 or older, no SSN answer",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.nosenior")
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(0))
        self.assertFalse(
            [row for row in blocked if "schedule1a" in str(row.get("artifact_id", "")) or "line13b" in str(row.get("artifact_id", ""))],
            f"unexpected senior-deduction block: {blocked}",
        )

    def test_case_senior_missing_ssn_answer_blocks(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=60000, taxpayer_over_65=True),
            "synthetic case: senior with no SSN answer",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.nossn")
        self.assertNotIn(LINE_13B, pubs)
        missing = _missing_names(blocked, "line-36a") or _missing_names(blocked, "line13b")
        found = any(TAXPAYER_SSN in str(row.get("missing", [])) for row in blocked)
        self.assertTrue(found, f"expected {TAXPAYER_SSN} named in a blocked disposition; blocked={blocked}")

    def test_case_missing_parts_ii_iv_answer_blocks(self) -> None:
        acts = _finish_v51(
            _senior_acts(wages=60000, taxpayer_over_65=True, taxpayer_ssn="yes", parts_ii_iv=None),
            "synthetic case: missing Parts II-IV answer",
        )
        pubs, blocked = _run(acts, "demo.sdd.case.noscope")
        self.assertNotIn(LINE_13B, pubs)
        found = any(PARTS_II_IV in str(row.get("missing", [])) for row in blocked)
        self.assertTrue(found, f"expected {PARTS_II_IV} named in a blocked disposition; blocked={blocked}")

    def test_case_v50_run_unchanged(self) -> None:
        probe = toti._probe()
        acts = toti._finish_v50(probe._base_acts(wages=60000), "synthetic v50 comparison, unaffected by v51 content")
        pubs, blocked = toti._run(acts, "demo.sdd.case.v50")
        self.assertEqual(_value(pubs, blocked, toti.STD), Decimal(15750))
        self.assertEqual(_value(pubs, blocked, LINE_13B), Decimal(0))


if __name__ == "__main__":
    unittest.main()
