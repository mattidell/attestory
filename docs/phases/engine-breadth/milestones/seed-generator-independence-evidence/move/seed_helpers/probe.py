"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import Any
from typing import cast

REPO = repo_root()

from packages.tax.loader import load_f1099k_bundle
from packages.tax.loader import load_f1099k_circumstances_bundle
from seed_helpers.test_f1098e_student_loan_interest_agi_track6 import SCHED1_LINE_TOKENS
from seed_helpers.test_f1098e_student_loan_interest_agi_track6 import SLI_SCOPE_LEGAL_ZERO_TOKENS
from seed_helpers.test_f1098e_student_loan_interest_agi_track6 import SLI_SCOPE_UNIVERSAL_TOKENS
from seed_helpers.test_f1098e_student_loan_interest_agi_track6 import _load as _load_sli
from seed_helpers.test_form1099g_box1_schedule1_line7 import _act
from seed_helpers.test_form1099g_box1_schedule1_line7 import _attested
from seed_helpers.test_ssa1099_benefits_line6_track2 import _ssa_acts
from seed_helpers.fixture_authority import append_wash_sale_v2_empty_authority
from seed_helpers.test_f1098_mortgage_interest_line12e_track2 import _load_fixture_adoption

SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

CONTENT = REPO / "packages" / "content" / "tax" / "2025"

def _load_content(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))

def _elective(finding_id: str, fact_id: str, value: object) -> dict[str, object]:
    return {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": fact_id,
        "value": value,
        "basis": "elective",
        "evidence_ids": [],
    }

def _base_acts(
    *,
    wages: float,
    filing_status: str = "single",
    qualified_dividends: float | None = None,
    ordinary_dividends: float | None = None,
    capital_gains: float | None = None,
) -> list[dict[str, object]]:
    """A closed, production-shaped single-income-source act log (no Schedule D
    transactions), reusing the SSA-benefits-worksheet corpus builder for its
    wages / filing-status / dividend plumbing (``tests/test_ssa1099_benefits_
    line6_track2.py``), then closing the remaining families
    ``tests.test_f1099k_personal_item_sale_track1._make_base_acts`` closes for
    the current package graph (student-loan-interest scope, Form 1099-K,
    wash-sale v2 empty authority)."""
    acts = _ssa_acts(
        wages=wages,
        benefits=[],
        filing_status=filing_status,
        qualified_dividends=qualified_dividends,
        ordinary_dividends=ordinary_dividends,
        capital_gains=capital_gains,
    )
    acts.pop()  # drop the helper's own (historical) package adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load_sli("f1098e.bundle.json")})
    add("bundle-adoption", {"bundle": _load_sli("sli-scope.bundle.json")})
    add("bundle-adoption", {"bundle": _load_sli("schedule1-adjustments-scope.bundle.json")})
    add(
        "horizon-genesis",
        {
            "family": {"id": "tax.us.2025.f1098e.1", "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.probe.f1098e.h0",
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.f1098e.closure",
                "tax.us.2025.f1098e.1.source-closure|family-horizon=demo.probe.f1098e.h0,tax-year=2025",
                True,
            )
        },
    )
    for token in SLI_SCOPE_UNIVERSAL_TOKENS + SLI_SCOPE_LEGAL_ZERO_TOKENS:
        add(
            "assertion",
            {"finding": _attested(f"demo.probe.sli-scope.{token}", f"tax.us.2025.sli-scope.{token}|tax-year=2025", "yes")},
        )
    for token in SCHED1_LINE_TOKENS:
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.probe.sched1-scope.{token}",
                    f"tax.us.2025.schedule1-adjustments-scope.{token}|tax-year=2025",
                    "yes",
                )
            },
        )

    add("bundle-adoption", {"bundle": load_f1099k_bundle(version="v2")})
    add("bundle-adoption", {"bundle": load_f1099k_circumstances_bundle()})
    add(
        "horizon-genesis",
        {
            "family": {"id": "tax.us.2025.f1099k", "version": "v2"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.probe.f1099k.h0",
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.f1099k.closure",
                "tax.us.2025.f1099k.source-closure|family-horizon=demo.probe.f1099k.h0,tax-year=2025",
                True,
            )
        },
    )
    append_wash_sale_v2_empty_authority(acts)

    # Form 1098 (mortgage interest): Path A -- no mortgage statement on
    # record -- declared via the closed-empty family plus the mandatory
    # scope flag (mirrors tests.test_f1098_mortgage_interest_line12e_track2
    # ``_path_a_acts``).
    add("bundle-adoption", {"bundle": _load_content("f1098.bundle.json")})
    add("bundle-adoption", {"bundle": _load_content("f1098-scope.bundle.json")})
    add(
        "horizon-genesis",
        {
            "family": {"id": "tax.us.2025.f1098", "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.probe.f1098.h0",
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.f1098.closure",
                "tax.us.2025.f1098.source-closure|family-horizon=demo.probe.f1098.h0,tax-year=2025",
                True,
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.f1098.no-mortgage-statement",
                "tax.us.2025.f1098-scope.no-mortgage-statement|tax-year=2025",
                True,
            )
        },
    )

    # Schedule A boundary: no itemizable category declared (so the standard
    # deduction path is taken cleanly).
    add("bundle-adoption", {"bundle": _load_content("schedule-a-boundary.bundle.json")})
    for cat in (
        "no-medical",
        "no-salt",
        "no-other-interest",
        "no-investment-interest",
        "no-charitable",
        "no-casualty-theft",
        "no-gambling-other",
    ):
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.probe.schedule-a-boundary.{cat}",
                    f"tax.us.2025.schedule-a-boundary.{cat}-declared|tax-year=2025",
                    "yes",
                )
            },
        )

    # QBI / Schedule 1-A: neither deduction declared.
    add("bundle-adoption", {"bundle": _load_content("qbi-schedule1a-scope.bundle.json")})
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.qbi-no-deduction-declared",
                "tax.us.2025.qbi.no-qbi-deduction-declared|tax-year=2025",
                "yes",
            )
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.schedule1a-no-additional-deductions-declared",
                "tax.us.2025.schedule1a.no-additional-deductions-declared|tax-year=2025",
                "yes",
            )
        },
    )

    # Form 1099-DIV box 7 (foreign tax paid): closed-empty. (Adopted before
    # the direct-FTC election/scope facts below, since the election fact
    # type itself lives in this bundle.)
    add("bundle-adoption", {"bundle": _load_content("f1099div-box7.bundle.json")})
    add(
        "horizon-genesis",
        {
            "family": {"id": "tax.us.2025.f1099div.7", "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": "demo.probe.div7.h0",
        },
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.div7.closure",
                "tax.us.2025.f1099div.7.source-closure|family-horizon=demo.probe.div7.h0,tax-year=2025",
                True,
            )
        },
    )

    # Direct foreign tax credit (Schedule 3 line 1): no foreign tax at all,
    # so the election is "no" and every scope boundary is vacuously satisfied.
    add("bundle-adoption", {"bundle": _load_content("direct-ftc-scope.bundle.json")})
    for token in (
        "all-foreign-income-passive",
        "all-foreign-income-on-1099div",
        "no-f1099int-foreign-tax",
        "no-k1-k3-foreign-tax",
        "no-other-foreign-tax-source",
        "tax-type-creditable",
        "legal-liability-and-paid",
        "no-refund-rebate-subsidy",
        "no-excluded-income-association",
        "holding-period-16-day-met",
        "no-short-sale-obligation",
        "country-recognized-non-terrorism",
        "no-carryback-carryforward",
        "no-schedule-a-deduction-election",
        "no-form-1116-required",
        "no-sch3-line2",
        "no-sch3-line3",
        "no-sch3-line4",
        "no-sch3-line5",
        "no-sch3-line6",
        "no-line17-schedule2-additional",
        "no-line19-ctc-odc",
        "no-schedule2-regular-tax-add",
        "no-form-4972-on-line16",
    ):
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.probe.direct-ftc-scope.{token}",
                    f"tax.us.2025.direct-ftc-scope.{token}|tax-year=2025",
                    "yes",
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _elective(
                "demo.probe.direct-ftc.election",
                "tax.us.2025.direct-ftc.election|tax-year=2025",
                "no",
            )
        },
    )

    return acts
