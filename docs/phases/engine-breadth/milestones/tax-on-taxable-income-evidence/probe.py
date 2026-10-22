"""P0 probe — tax-on-taxable-income (investigation only, no production edit).

Runs synthetic single-filer returns through the real coordinator
(``live_coordinate_run``) against the adopted production package
(core-calculations v49) and records today's Form 1040 line 16 next to a hand
computation from the 2025 primary-source values recorded in
``p0-law-and-inventory.md``. Also demonstrates the short-term-gain
preferential-base defect on a small Schedule D return.

This script writes its JSON output under ``temp/`` only (git-ignored); it is
committed itself as the evidence trail's probe, per the plan's P0 action. Run from
the repository root:

    python3 docs/phases/engine-breadth/milestones/tax-on-taxable-income-evidence/probe.py

All facts are synthetic (``demo.*`` ids). No absolute paths are written to
any committed file.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, cast

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from packages.derivation.live import live_coordinate_run  # noqa: E402
from packages.derivation.live_workspace import WorkspaceCapability  # noqa: E402
from packages.tax.loader import (  # noqa: E402
    load_f1099k_bundle,
    load_f1099k_circumstances_bundle,
)

from tests.test_f1098e_student_loan_interest_agi_track6 import (  # noqa: E402
    SCHED1_LINE_TOKENS,
    SLI_SCOPE_LEGAL_ZERO_TOKENS,
    SLI_SCOPE_UNIVERSAL_TOKENS,
    _load as _load_sli,
)
from tests.test_form1099g_box1_schedule1_line7 import _act, _attested  # noqa: E402
from tests.test_multiple_statement_sale_acceptance import (  # noqa: E402
    PACKAGE_V49_PATH,
    RELEASE_V47_PATH,
    SURFACE_V47,
)
from tests.test_f1099k_personal_item_sale_track1 import USER  # noqa: E402
from tests.test_ssa1099_benefits_line6_track2 import _ssa_acts  # noqa: E402
from tests.source_completeness.fixture_authority import (  # noqa: E402
    append_wash_sale_v2_empty_authority,
)
from tests.test_f1098_mortgage_interest_line12e_track2 import (  # noqa: E402
    _load_fixture_adoption,
)

SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}
OUT_DIR = REPO / "temp" / "tax-on-taxable-income"
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


_SD_TXN_BASE = {
    "covered_security": "yes",
    "basis_reported_to_irs": "yes",
    "box_1f_market_discount": "no",
    "box_1g_wash_sale_adjustment": "no",
    "ordinary_indicated": "no",
    "qof_indicated": "no",
    "taxpayer_side_adjustment": "no",
    "collectibles_or_special_rate": "no",
}

_SD_BOUNDARY_5 = (
    "tax.us.2025.schedule-d-boundary.no-inbound-capital-loss-carryovers",
    "tax.us.2025.schedule-d-boundary.no-form8949-sources",
    "tax.us.2025.schedule-d-boundary.no-other-schedule-d-sources",
    "tax.us.2025.schedule-d-boundary.no-lines-18-19-sources",
    "tax.us.2025.schedule-d-boundary.no-1099da-or-qof",
)


def _splice_schedule_d_transactions(
    acts: list[dict[str, object]],
    *,
    st: list[tuple[float, float]],
    lt: list[tuple[float, float]],
) -> list[dict[str, object]]:
    """Reopen the closed-empty covered-ST/LT families
    ``tests.test_form1099g_box1_schedule1_line7._ug_acts`` leaves in ``acts``
    and insert real transactions before re-closing them, so the real
    ``tax.us.2025.rule.selected-preferential-base`` v4 route runs on an
    actual Schedule D return instead of a closed-empty one."""
    acts = copy.deepcopy(acts)

    closure_prefixes = {
        "tax.us.2025.f1099b.covered-st.source-closure": "demo.probe.sd.st",
        "tax.us.2025.f1099b.covered-st-proceeds.source-closure": "demo.probe.sd.st-p",
        "tax.us.2025.f1099b.covered-st-basis.source-closure": "demo.probe.sd.st-b",
        "tax.us.2025.f1099b.covered-lt.source-closure": "demo.probe.sd.lt",
        "tax.us.2025.f1099b.covered-lt-proceeds.source-closure": "demo.probe.sd.lt-p",
        "tax.us.2025.f1099b.covered-lt-basis.source-closure": "demo.probe.sd.lt-b",
    }
    start_horizons: dict[str, str] = {}
    kept: list[dict[str, object]] = []
    for act in acts:
        payload = cast(dict[str, Any], act.get("payload", {}))
        finding = cast(dict[str, Any], payload.get("finding", {})) if act.get("kind") == "assertion" else {}
        fact_id = str(finding.get("fact_id", ""))
        matched = None
        for closure_type, _ in closure_prefixes.items():
            if fact_id.startswith(closure_type + "|"):
                matched = closure_type
                break
        if matched is not None:
            start_horizons[matched] = fact_id.split("family-horizon=")[1].split(",")[0]
            continue  # drop the closed-empty closure; it is replaced below
        kept.append(act)
    acts = kept

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": "demo.probe.sd.broker", "kind": "tax.us.f1099b-broker", "label": "Synthetic broker"}},
    )
    add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": "demo.probe.sd.stmt", "kind": "tax.us.f1099b-statement", "label": "Synthetic Form 1099-B"}},
    )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.probe.sd.anchor",
                "tax.us.2025.f1099b.statement-anchor|broker=demo.probe.sd.broker,statement=demo.probe.sd.stmt,tax-year=2025",
                {"broker_name": "Synthetic Broker"},
            )
        },
    )

    horizons = {
        "obj_st": start_horizons["tax.us.2025.f1099b.covered-st.source-closure"],
        "p_st": start_horizons["tax.us.2025.f1099b.covered-st-proceeds.source-closure"],
        "b_st": start_horizons["tax.us.2025.f1099b.covered-st-basis.source-closure"],
        "obj_lt": start_horizons["tax.us.2025.f1099b.covered-lt.source-closure"],
        "p_lt": start_horizons["tax.us.2025.f1099b.covered-lt-proceeds.source-closure"],
        "b_lt": start_horizons["tax.us.2025.f1099b.covered-lt-basis.source-closure"],
    }

    def add_txns(prefix: str, family: str, long_term: str, pairs: list[tuple[float, float]], keys: tuple[str, str, str]) -> None:
        for i, (proceeds, basis) in enumerate(pairs):
            txn_id = f"demo.probe.sd.{prefix}-txn-{i}"
            add("entity-introduced", {"entity": {"schema": "entity.v1", "id": txn_id, "kind": "tax.us.f1099b-transaction", "label": f"Synthetic {prefix} sale {i}"}})
            key = f"broker=demo.probe.sd.broker,statement=demo.probe.sd.stmt,transaction={txn_id},tax-year=2025"
            value = {**_SD_TXN_BASE, "proceeds": proceeds, "basis": basis, "long_term": long_term}
            for hkey, fact_suffix, amount in (
                (keys[0], f"{family}-txn", value),
                (keys[1], f"{family}-txn.proceeds", proceeds),
                (keys[2], f"{family}-txn.basis", basis),
            ):
                fam_id = {
                    keys[0]: f"tax.us.2025.f1099b.{family}",
                    keys[1]: f"tax.us.2025.f1099b.{family}-proceeds",
                    keys[2]: f"tax.us.2025.f1099b.{family}-basis",
                }[hkey]
                pred = horizons[hkey]
                succ = f"{pred}.n{i}"
                add(
                    "member-transition",
                    {
                        "family": {"id": fam_id, "version": "v1"},
                        "scope": SCOPE_KEY,
                        "member": {"action": "assert", "finding": _attested(
                            f"demo.probe.sd.finding.{prefix}-{hkey}-{i}",
                            f"tax.us.2025.f1099b.{fact_suffix}|{key}",
                            amount,
                        )},
                        "successor": {"id": succ, "predecessor": pred},
                    },
                )
                horizons[hkey] = succ

    add_txns("st", "covered-st", "no", st, ("obj_st", "p_st", "b_st"))
    add_txns("lt", "covered-lt", "yes", lt, ("obj_lt", "p_lt", "b_lt"))

    for hkey, closure_type in (
        ("obj_st", "tax.us.2025.f1099b.covered-st.source-closure"),
        ("p_st", "tax.us.2025.f1099b.covered-st-proceeds.source-closure"),
        ("b_st", "tax.us.2025.f1099b.covered-st-basis.source-closure"),
        ("obj_lt", "tax.us.2025.f1099b.covered-lt.source-closure"),
        ("p_lt", "tax.us.2025.f1099b.covered-lt-proceeds.source-closure"),
        ("b_lt", "tax.us.2025.f1099b.covered-lt-basis.source-closure"),
    ):
        add(
            "assertion",
            {"finding": _attested(f"demo.probe.sd.closure.{hkey}", f"{closure_type}|family-horizon={horizons[hkey]},tax-year=2025", True)},
        )

    add("bundle-adoption", {"bundle": _load_content("exception1.bundle.json")})
    for alias, value in {"C1": "yes", "C2": "yes", "C3": "yes", "C4": "yes"}.items():
        fact_type = {
            "C1": "tax.us.2025.exception1.only-box2a-capital-gains",
            "C2": "tax.us.2025.exception1.no-capital-losses",
            "C3": "tax.us.2025.exception1.no-qof-deferral",
            "C4": "tax.us.2025.exception1.no-boxes-2b-2c-2d",
        }[alias]
        add("assertion", {"finding": _attested(f"demo.probe.sd.exception1.{alias}", f"{fact_type}|tax-year=2025", value)})
    for name in _SD_BOUNDARY_5:
        add("assertion", {"finding": _attested(f"demo.probe.sd.boundary.{name.split('.')[-1]}", f"{name}|tax-year=2025", "yes")})

    return acts


def _finish_v49(acts: list[dict[str, object]], note: str) -> list[dict[str, object]]:
    pkg_data = json.loads(PACKAGE_V49_PATH.read_text("utf-8"))
    pkg_csum = pkg_data["package_checksum"]
    rel_csum = hashlib.sha256(RELEASE_V47_PATH.read_bytes()).hexdigest()

    built = copy.deepcopy(acts)
    adoption = copy.deepcopy(_load_fixture_adoption())
    adoption["act_id"] = f"demo.probe.adopt.{len(built):03d}"
    adoption["committed_against"] = len(built)
    payload = adoption["payload"]
    assert isinstance(payload, dict)
    payload["package"] = {
        "id": "tax.us.2025.package.core-calculations",
        "version": "v49",
        "checksum": pkg_csum,
    }
    payload["release"] = {
        "id": "demo.release.sli-worksheet-integration.2025",
        "version": "v47",
        "checksum": rel_csum,
    }
    payload["audit"] = {"note": note}
    built.append(adoption)
    for index, row in enumerate(built):
        row["committed_against"] = index
        row["actor"] = USER
    return built


def _run(acts: list[dict[str, object]], run_id: str) -> dict[str, Any]:
    with TemporaryDirectory() as tmp:
        outcome = live_coordinate_run(
            WorkspaceCapability(Path(tmp) / "L"),
            repo_root=REPO,
            authoritative_acts=acts,
            workspace_revision=len(acts),
            run_scope={"jurisdiction": "us", "year": "2025"},
            scope_user=USER,
            request={"schema": "run-request.v1"},
            run_id=run_id,
            governance_pins=[],
            surface=SURFACE_V47,
            output_name="out.json",
        )
        if outcome.refusal is not None:
            return {"refusal": outcome.refusal}
        assert outcome.output_path is not None
        report = cast(dict[str, Any], json.loads(outcome.output_path.read_text("utf-8")))
        by_artifact = {row["artifact_id"]: row for row in report["dispositions"]}
        sections: dict[str, Any] = {}
        if outcome.presentation_path is not None:
            presentation = cast(dict[str, Any], json.loads(outcome.presentation_path.read_text("utf-8")))
            sections = {s["id"]: s for s in presentation.get("sections", [])}
        return {"dispositions": by_artifact, "sections": sections}


def _section_value(result: dict[str, Any], section_id: str) -> Any:
    section = result.get("sections", {}).get(section_id)
    if section is None:
        return {
            "error": f"no {section_id!r} presentation section",
            "refusal": result.get("refusal"),
            "dispositions": {
                k: v.get("disposition") for k, v in result.get("dispositions", {}).items() if v.get("disposition") == "blocked"
            },
        }
    resolved = section.get("resolved", {})
    return resolved.get("value", resolved.get("disposition"))


def _line16(result: dict[str, Any]) -> Any:
    return _section_value(result, "line-16")


def _taxable_income(result: dict[str, Any]) -> Any:
    return _section_value(result, "line-15")


# --- hand computation from the verified 2025 values (p0-law-and-inventory.md) ---

_BRACKETS_SINGLE = [
    (Decimal(0), Decimal("11925"), Decimal("0.10")),
    (Decimal("11925"), Decimal("48475"), Decimal("0.12")),
    (Decimal("48475"), Decimal("103350"), Decimal("0.22")),
    (Decimal("103350"), Decimal("197300"), Decimal("0.24")),
    (Decimal("197300"), Decimal("250525"), Decimal("0.32")),
    (Decimal("250525"), Decimal("626350"), Decimal("0.35")),
    (Decimal("626350"), None, Decimal("0.37")),
]

_PREF_0_SINGLE = Decimal("48350")
_PREF_20_SINGLE = Decimal("533400")


def _ordinary_tax_single(amount: Decimal) -> Decimal:
    total = Decimal(0)
    for lower, upper, rate in _BRACKETS_SINGLE:
        if amount <= lower:
            continue
        top = amount if upper is None else min(amount, upper)
        total += (top - lower) * rate
    return total


def _round_dollar(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal(1), rounding=ROUND_HALF_UP)


# today's (unverified) demo.parameter.tax-brackets.2025 v2 single schedule --
# used only to isolate the short-term preferential-base defect's own effect
# (case 5) from the separate rate-schedule mismatch (cases 1-3).
_BRACKETS_SINGLE_DEMO = [
    (Decimal(0), Decimal("11600"), Decimal("0.10")),
    (Decimal("11600"), Decimal("47150"), Decimal("0.12")),
    (Decimal("47150"), None, Decimal("0.22")),
]


def _ordinary_tax_single_demo(amount: Decimal) -> Decimal:
    total = Decimal(0)
    for lower, upper, rate in _BRACKETS_SINGLE_DEMO:
        if amount <= lower:
            continue
        top = amount if upper is None else min(amount, upper)
        total += (top - lower) * rate
    return total


def _hand_line16_single(*, taxable_income: Decimal, qualified_pref_base: Decimal) -> Decimal:
    """Single-filer line 16 per the 2025 QDCG worksheet, ordinary tax via the
    2025 Tax Computation Worksheet schedule (exact for income >= $100,000;
    for income below $100,000 the real Tax Table rounds each $50 band to its
    midpoint, so this hand figure can differ from today's engine output by at
    most a few dollars in that range — the probe notes this explicitly)."""
    ordinary_base = taxable_income - qualified_pref_base
    if qualified_pref_base <= 0:
        return _round_dollar(_ordinary_tax_single(taxable_income))
    pref_tax = Decimal(0)
    zero_top = min(taxable_income, _PREF_0_SINGLE)
    zero_amount = min(qualified_pref_base, max(zero_top - ordinary_base, Decimal(0)))
    remaining = qualified_pref_base - zero_amount
    twenty_top = max(min(taxable_income, _PREF_20_SINGLE) - ordinary_base - zero_amount, Decimal(0))
    fifteen_amount = min(remaining, twenty_top)
    remaining -= fifteen_amount
    twenty_amount = remaining
    pref_tax = fifteen_amount * Decimal("0.15") + twenty_amount * Decimal("0.20")
    combined = _round_dollar(_ordinary_tax_single(ordinary_base)) + _round_dollar(pref_tax)
    all_ordinary = _round_dollar(_ordinary_tax_single(taxable_income))
    return min(combined, all_ordinary)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {}

    # Case 1: taxable income ~ $50,000 single, wages only.
    acts = _finish_v49(_base_acts(wages=61850.0, filing_status="single"), "P0 probe case 1: ~$50k taxable income, single, wages only")
    r1 = _run(acts, "demo.p0probe.case1")
    results["case1_50k_single_wages_only"] = {
        "line16_engine": _line16(r1),
        "taxable_income": _taxable_income(r1),
    }

    # Case 2: taxable income ~ $150,000 single, wages only (above $100k => Tax
    # Computation Worksheet, not the Tax Table -- exact comparison).
    acts = _finish_v49(_base_acts(wages=161850.0, filing_status="single"), "P0 probe case 2: ~$150k taxable income, single, wages only")
    r2 = _run(acts, "demo.p0probe.case2")
    ti2 = _taxable_income(r2)
    results["case2_150k_single_wages_only"] = {
        "line16_engine": _line16(r2),
        "taxable_income": ti2,
        "hand_ordinary_tax": str(_round_dollar(_ordinary_tax_single(Decimal(str(ti2))))) if ti2 is not None else None,
    }

    # Case 3: taxable income ~ $600,000 single, wages only.
    acts = _finish_v49(_base_acts(wages=611850.0, filing_status="single"), "P0 probe case 3: ~$600k taxable income, single, wages only")
    r3 = _run(acts, "demo.p0probe.case3")
    ti3 = _taxable_income(r3)
    results["case3_600k_single_wages_only"] = {
        "line16_engine": _line16(r3),
        "taxable_income": ti3,
        "hand_ordinary_tax": str(_round_dollar(_ordinary_tax_single(Decimal(str(ti3))))) if ti3 is not None else None,
    }

    # Case 4: modest wages + qualified dividends entirely within the 0% band.
    acts = _finish_v49(
        _base_acts(wages=20000.0, filing_status="single", qualified_dividends=5000.0, ordinary_dividends=5000.0),
        "P0 probe case 4: qualified dividends in the 0% preferential band",
    )
    r4 = _run(acts, "demo.p0probe.case4")
    ti4 = _taxable_income(r4)
    results["case4_0pct_band_qualified_dividends"] = {
        "line16_engine": _line16(r4),
        "taxable_income": ti4,
        "note": (
            "today's engine taxes the qualified-dividend amount at a flat 15%"
            " (demo.parameter.qdcg-preferential-brackets.2025 v2 has no 0% band);"
            " the verified 2025 0% breakpoint for single filers is $48,350, so"
            " this amount should be entirely in the 0% band by hand computation"
        ),
    }
    if ti4 is not None:
        hand4 = _hand_line16_single(taxable_income=Decimal(str(ti4)), qualified_pref_base=Decimal("5000"))
        results["case4_0pct_band_qualified_dividends"]["hand_line16_with_verified_2025_bands"] = str(hand4)

    # Case 5: the short-term-gain preferential-base defect. ST gain $5,000,
    # LT gain $1,000, wages $90,000 single. Schedule D line 15 (LT) = 1,000,
    # line 16 (ST+LT) = 6,000. The 2025 QDCG worksheet line 3 preferential
    # base is "the smaller of line 15 or line 16" (both positive here) =
    # $1,000 -- only the long-term gain. Today's
    # ``rule.selected-preferential-base.v4`` instead publishes
    # ``max(line-16, 0)`` = $6,000, letting the $5,000 short-term gain into
    # the preferential base.
    acts = _finish_v49(
        _splice_schedule_d_transactions(
            _base_acts(wages=90000.0, filing_status="single"),
            st=[(5000.0, 0.0)],
            lt=[(1000.0, 0.0)],
        ),
        "P0 probe case 5: short-term-gain preferential-base defect (ST $5,000 gain, LT $1,000 gain)",
    )
    r5 = _run(acts, "demo.p0probe.case5")
    ti5 = _taxable_income(r5)
    line16_5 = _line16(r5)
    case5: dict[str, Any] = {
        "line16_engine": line16_5,
        "taxable_income": ti5,
        "defect": (
            "rule.selected-preferential-base.v4's value branch publishes"
            " max(schedule-d.line-16, 0) = max(5000+1000, 0) = 6000 as the"
            " preferential base, which includes the $5,000 short-term gain."
            " The 2025 QDCG worksheet line 3 requires the smaller of Schedule"
            " D line 15 (long-term, here 1000) or line 16 (here 6000) = 1000,"
            " with short-term gain excluded entirely."
        ),
    }
    if ti5 is not None:
        ti5_dec = Decimal(str(ti5))
        ordinary_defect = _round_dollar(_ordinary_tax_single_demo(ti5_dec - Decimal("6000")))
        pref_defect = _round_dollar(Decimal("6000") * Decimal("0.15"))
        all_ordinary = _round_dollar(_ordinary_tax_single_demo(ti5_dec))
        defect_total = min(ordinary_defect + pref_defect, all_ordinary)
        ordinary_correct = _round_dollar(_ordinary_tax_single_demo(ti5_dec - Decimal("1000")))
        pref_correct = _round_dollar(Decimal("1000") * Decimal("0.15"))
        correct_total = min(ordinary_correct + pref_correct, all_ordinary)
        case5["hand_check_with_todays_tax_brackets"] = {
            "defect_preferential_base": "6000",
            "defect_combined_tax": str(defect_total),
            "matches_engine": str(defect_total) == str(line16_5),
            "corrected_preferential_base_per_2025_worksheet": "1000",
            "corrected_combined_tax": str(correct_total),
            "delta_from_defect_alone": str(correct_total - defect_total),
            "note": (
                "this hand check reuses today's (unverified) demo rate"
                " brackets on both sides, isolating the short-term-base"
                " defect's own effect ($350 here) from the separate rate-"
                " schedule and preferential-band mismatches in cases 1-4"
            ),
        }
    results["case5_short_term_preferential_base_defect"] = case5

    results["_notes"] = {
        "case1_tax_table_caveat": (
            "Case 1's taxable income is below $100,000, where the 2025"
            " instructions require the Tax Table (banded $50 midpoints), not"
            " the raw marginal schedule. No hand Tax-Table figure is computed"
            " here (that is the Increment B.4 expressibility question, not a"
            " numeric check); today's engine applies the raw marginal bracket"
            " fold at every income level, never the Tax Table."
        ),
    }

    out_path = OUT_DIR / "probe-output.json"
    out_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(json.dumps(results, indent=2, default=str))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
