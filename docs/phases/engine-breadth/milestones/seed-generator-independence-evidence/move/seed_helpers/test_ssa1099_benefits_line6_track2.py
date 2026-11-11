"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import Any
from typing import cast
from packages.tax.loader import TAX_CONTENT_DIR
from seed_helpers.test_form1099r_ira_line4b_track2 import _ira_acts
from seed_helpers.test_form1099g_box1_schedule1_line7 import _act
from seed_helpers.test_form1099g_box1_schedule1_line7 import _attested

ROOT = repo_root()

CONTENT = TAX_CONTENT_DIR

FIXTURES = ROOT / "packages" / "sample_data" / "ssa1099_benefits_line6"

SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

FAMILY = "tax.us.2025.ssa1099.benefits"

BOX3 = "tax.us.2025.ssa1099.box3-benefits-paid"

BOX4 = "tax.us.2025.ssa1099.box4-repayment"

BOX5 = "tax.us.2025.ssa1099.box5-net-benefits"

BOX6 = "tax.us.2025.ssa1099.box6-withholding"

RECIPIENT = "tax.us.2025.ssa1099.recipient"

KIND = "tax.us.2025.ssa1099.statement-kind"

LUMP = "tax.us.2025.ssa1099.lump-sum-election"

CLOSURE = "tax.us.2025.ssa1099.source-closure"

MFS = "tax.us.2025.mfs-lived-apart-all-year"

SCOPE_TOKENS = (
    "no-unsupported-line1-entries",
    "no-pension-annuity-line5b",
    "no-traditional-ira-deduction",
    "no-form-2555",
    "no-form-4563",
    "no-form-8815",
    "no-excluded-adoption-benefits",
    "no-puerto-rico-or-samoa-income",
    "no-schedule1-line24z-writein",
    "no-sch1-line11-educator",
    "no-sch1-line12-business-expenses",
    "no-sch1-line13-hsa",
    "no-sch1-line14-moving",
    "no-sch1-line15-deductible-se",
    "no-sch1-line16-se-retirement",
    "no-sch1-line17-se-health",
    "no-sch1-line18-penalty",
    "no-sch1-line19-alimony-paid",
    "no-sch1-line20-ira-deduction",
    "no-sch1-line23-archer-msa",
    "no-sch1-line25-other-adjustments",
    "no-lump-sum-election",
    "no-rrb-or-foreign-social-benefit",
)

def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))

def _scope_id(token: str) -> str:
    return f"tax.us.2025.ss-benefits-scope.{token}"

def _ssa_acts(
    *,
    benefits: list[tuple[float, float, float]] | None = None,
    close: bool = True,
    wages: float = 15000,
    interest: float | None = None,
    ordinary_dividends: float | None = None,
    qualified_dividends: float | None = None,
    capital_gains: float | None = None,
    unemployment: float | None = None,
    filing_status: str = "single",
    mfs_lived_apart: str | None = None,
    tax_exempt: float | None = None,
    ira_amounts: list[float] | None = None,
    scope: dict[str, str] | None = None,
    recipient: str = "taxpayer",
    statement_overrides: list[dict[str, object]] | None = None,
    wash_sale_version: str = "v1",
) -> list[dict[str, object]]:
    """Production-shaped acts with controlled ordinary-income components + SSA."""
    import seed_helpers.test_form1099r_ira_line4b_track2 as ira_mod

    original_ug = cast(Any, getattr(ira_mod, "_ug_acts"))

    def _ug_with_components(**kwargs: Any) -> list[dict[str, object]]:
        kwargs["wages"] = wages
        # Unemployment → Schedule 1 / Form 1040 line 8 via 1099-G box 1.
        if unemployment is not None and unemployment > 0:
            kwargs["box1_values"] = [unemployment]
            kwargs["close_box1"] = True
        else:
            kwargs["box1_values"] = []
            kwargs["close_box1"] = True
        # Ordinary / qualified dividends and capital-gain distributions.
        if ordinary_dividends is not None:
            kwargs["box1a"] = ordinary_dividends
        if qualified_dividends is not None:
            kwargs["box1b"] = qualified_dividends
        if capital_gains is not None:
            kwargs["box2a"] = capital_gains
        return cast(list[dict[str, object]], original_ug(**kwargs))

    setattr(ira_mod, "_ug_acts", _ug_with_components)
    try:
        acts = _ira_acts(
            amounts=[] if ira_amounts is None else ira_amounts,
            close=True,
            qualified_dividends=False,
            wash_sale_version=wash_sale_version,
        )
    finally:
        setattr(ira_mod, "_ug_acts", original_ug)
    acts.pop()  # drop historical package adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    # Ensure wages / filing status from base corpus; override wages via W-2 if needed
    # is already set by upstream helpers. Adopt SSA vocabulary + scope + successor packages.
    add("bundle-adoption", {"bundle": _load("ssa1099.bundle.v2.json")})
    add("bundle-adoption", {"bundle": _load("ss-benefits-scope.bundle.json")})
    # Line 2a residual scopes + closed-empty box-12 so tax-exempt line 2a
    # publishes zero for the worksheet W4 pin without Path B INT box-8.
    if not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.line2a-scope.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load("line2a-scope.bundle.json")})
    line2a_scope_tokens = (
        "no-f1099int-tax-exempt",
        "no-f1099oid-tax-exempt",
        "no-unreported-tax-exempt",
        "no-premium-adjustment",
        "no-child-income-election",
        "no-amt-form-6251",
        "no-credit-using-tax-exempt",
        "no-deduction-using-tax-exempt",
    )
    for token in line2a_scope_tokens:
        fid = f"tax.us.2025.line2a-scope.{token}"
        # skip if already asserted by upstream corpus
        already = any(
            str(cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("finding", {})).get("fact_id", "")).startswith(fid + "|")
            for act in acts
        )
        if not already:
            add(
                "assertion",
                {"finding": _attested(f"demo.ssa.line2a.{token}", f"{fid}|tax-year=2025", "yes")},
            )
    div12_family = "tax.us.2025.f1099div.12"
    if not any(
        act.get("kind") == "bundle-adoption"
        and cast(dict[str, Any], cast(dict[str, Any], act.get("payload", {})).get("bundle", {})).get("id")
        == "tax.us.2025.f1099div.box12.vocabulary"
        for act in acts
    ):
        add("bundle-adoption", {"bundle": _load("f1099div-box12.bundle.v2.json")})

    scope_vals = {token: "yes" for token in SCOPE_TOKENS}
    if scope:
        scope_vals.update(scope)
    for token, value in scope_vals.items():
        add(
            "assertion",
            {
                "finding": _attested(
                    f"demo.ssa.scope.{token}",
                    f"{_scope_id(token)}|tax-year=2025",
                    value,
                )
            },
        )

    if mfs_lived_apart is not None:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.mfs-lived-apart",
                    f"{MFS}|tax-year=2025",
                    mfs_lived_apart,
                )
            },
        )

    # Override corpus filing status when a non-default status is requested.
    if filing_status != "single":
        replaced = False
        for act in acts:
            finding = cast(
                dict[str, Any],
                cast(dict[str, Any], act.get("payload", {})).get("finding", {}),
            )
            fact_id = str(finding.get("fact_id", ""))
            if fact_id.startswith("tax.us.2025.filing-status|"):
                finding["value"] = filing_status
                replaced = True
                break
        if not replaced:
            add(
                "assertion",
                {
                    "finding": _attested(
                        "demo.ssa.filing-status",
                        "tax.us.2025.filing-status|tax-year=2025",
                        filing_status,
                    )
                },
            )

    # Taxable interest (Form 1099-INT box 1): advance the CGD closed-empty
    # int-b1 horizon so line 2b includes the amount exactly once.
    if interest is not None and interest > 0:
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.ssa.int.payer",
                    "kind": "tax.us.interest-payer",
                    "label": "Synthetic interest payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": "demo.ssa.int.stmt",
                    "kind": "tax.us.1099int-statement",
                    "label": "Synthetic Form 1099-INT",
                }
            },
        )
        add(
            "member-transition",
            {
                "family": {"id": "tax.us.2025.f1099int.b1", "version": "v1"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(
                        "demo.ssa.finding.int-b1",
                        "tax.us.2025.f1099int.box1-interest|"
                        "payer=demo.ssa.int.payer,statement=demo.ssa.int.stmt,tax-year=2025",
                        interest,
                    ),
                },
                "successor": {
                    "id": "demo.ssa.int-b1.h1",
                    "predecessor": "demo.cgd.t2.int-b1.h0",
                },
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.closure.int-b1",
                    "tax.us.2025.f1099int.b1.source-closure|"
                    "family-horizon=demo.ssa.int-b1.h1,tax-year=2025",
                    True,
                )
            },
        )

    benefits = [(12000.0, 0.0, 12000.0)] if benefits is None else benefits
    horizon = "demo.ssa.h0"
    add(
        "horizon-genesis",
        {"family": {"id": FAMILY, "version": "v1"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, (b3, b4, b5) in enumerate(benefits):
        statement = f"demo.ssa.statement.{index}"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.ssa1099-statement",
                    "label": "Synthetic Form SSA-1099",
                }
            },
        )
        # box5 is the collected member: assert companions first so presence
        # admission sees a complete same-statement witness set.
        ov = {}
        if statement_overrides and index < len(statement_overrides):
            ov = statement_overrides[index]
        kind_val = cast(str, ov.get("kind", "ssa-1099"))
        lump_val = cast(bool, ov.get("lump_sum_election", False))
        recip_val = cast(str, ov.get("recipient", recipient))
        box6_val = cast(float | None, ov.get("box6", 0))
        members: tuple[tuple[str, object, str], ...] = (
            (BOX3, b3, "box3"),
            (BOX4, b4, "box4"),
            (BOX6, box6_val, "box6"),
            (RECIPIENT, recip_val, "recipient"),
            (KIND, kind_val, "kind"),
            (LUMP, lump_val, "lump"),
            (BOX5, b5, "box5"),
        )
        for member_fact_type, member_value, member_suffix in members:
            add(
                "assertion",
                {
                    "finding": _attested(
                        f"demo.ssa.finding.{member_suffix}.{index}",
                        f"{member_fact_type}|statement={statement},tax-year=2025",
                        member_value,
                    )
                },
            )

    if close:
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.closure",
                    f"{CLOSURE}|family-horizon={horizon},tax-year=2025",
                    True,
                )
            },
        )

    # Line-2a residual scopes still required by line2a v3 (except removed SS residual)
    # Already present via IRA/UG helpers for many paths; tax-exempt optional Path A/B.

    # Line 2a / box-12: present tax-exempt dividends or closed-empty zero.
    div12_family = "tax.us.2025.f1099div.12"
    horizon = "demo.ssa.div12.h0"
    add(
        "horizon-genesis",
        {
            "family": {"id": div12_family, "version": "v1"},
            "scope": SCOPE_KEY,
            "horizon_id": horizon,
        },
    )
    if tax_exempt is not None and tax_exempt > 0:
        payer = "demo.ssa.div12.payer"
        statement = "demo.ssa.div12.statement.0"
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": payer,
                    "kind": "tax.us.dividend-payer",
                    "label": "Synthetic dividend payer",
                }
            },
        )
        add(
            "entity-introduced",
            {
                "entity": {
                    "schema": "entity.v1",
                    "id": statement,
                    "kind": "tax.us.1099div-statement",
                    "label": "Synthetic Form 1099-DIV",
                }
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.div12.box13",
                    "tax.us.2025.f1099div.box13-specified-pab-authority|"
                    f"payer={payer},statement={statement},tax-year=2025",
                    None,
                )
            },
        )
        add(
            "assertion",
            {
                "finding": _attested(
                    "demo.ssa.div12.box12",
                    "tax.us.2025.f1099div.box12-exempt-interest-dividends|"
                    f"payer={payer},statement={statement},tax-year=2025",
                    tax_exempt,
                )
            },
        )
    add(
        "assertion",
        {
            "finding": _attested(
                "demo.ssa.div12.closure",
                f"tax.us.2025.f1099div.12.source-closure|family-horizon={horizon},tax-year=2025",
                True,
            )
        },
    )


    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _load_fixture_adoption() -> dict[str, object]:
    return cast(
        dict[str, object],
        json.loads((FIXTURES / "adoptions" / "adopt-core-v28-current.json").read_text("utf-8")),
    )
