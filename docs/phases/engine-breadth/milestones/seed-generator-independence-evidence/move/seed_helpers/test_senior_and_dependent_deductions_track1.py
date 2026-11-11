"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import cast
import seed_helpers.test_tax_on_taxable_income_track1 as toti

ROOT = repo_root()

CONTENT = ROOT / "packages" / "content" / "tax" / "2025"

PARTS_II_IV = "tax.us.2025.schedule1a.no-parts-ii-iv-deductions-declared"

TAXPAYER_SSN = "tax.us.2025.senior-deduction.taxpayer-valid-ssn"

SPOUSE_SSN = "tax.us.2025.senior-deduction.spouse-valid-ssn"

ITEMIZED = "tax.us.2025.deductions.itemized"

CAN_BE_CLAIMED = "tax.us.2025.standard-deduction.can-be-claimed-as-dependent"

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
    can_be_claimed: str | None = "no",
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
    if can_be_claimed is not None:
        add(
            "assertion",
            {"finding": probe._attested("demo.sdd.can-be-claimed", f"{CAN_BE_CLAIMED}|tax-year=2025", can_be_claimed)},
        )

    return cast(list[dict[str, object]], acts)
