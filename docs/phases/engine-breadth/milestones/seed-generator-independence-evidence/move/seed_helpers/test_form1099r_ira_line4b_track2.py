"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from seed_helpers.repo_root import repo_root

import json
from typing import Any
from typing import cast
from packages.tax.loader import TAX_CONTENT_DIR
from seed_helpers.test_form1099g_box1_schedule1_line7 import _act
from seed_helpers.test_form1099g_box1_schedule1_line7 import _attested
from seed_helpers.test_form1099g_box1_schedule1_line7 import _ug_acts

ROOT = repo_root()

CONTENT = TAX_CONTENT_DIR

FIXTURES = ROOT / "packages" / "sample_data" / "form1099r_ira_line4b"

SCOPE_KEY = {"tax-year": "2025", "subject": "demo.primary"}

IRA_BOX1 = "tax.us.2025.f1099r.ira-box1-taxable-distribution"

IRA_BOX2A = "tax.us.2025.f1099r.ira-box2a-taxable-amount"

IRA_CHECKBOX = "tax.us.2025.f1099r.ira-sep-simple-checkbox"

IRA_CODE = "tax.us.2025.f1099r.distribution-code"

IRA_BOX2B = "tax.us.2025.f1099r.box2b-not-determined"

IRA_CLOSURE = "tax.us.2025.f1099r.ira-fully-taxable.source-closure"

IRA_FAMILY = "tax.us.2025.f1099r.ira-fully-taxable"

def _load(name: str) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads((CONTENT / name).read_text("utf-8")))

def _ira_acts(
    amounts: list[float] | None = None,
    *,
    close: bool = True,
    qualified_dividends: bool = False,
    wash_sale_version: str = "v1",
) -> list[dict[str, object]]:
    """Extend a known production-shaped income corpus with IRA statements."""
    acts = _ug_acts(
        box1_values=[],
        close_box1=True,
        box1a=600 if qualified_dividends else None,
        box1b=150 if qualified_dividends else 0,
        wages=90000,
        wash_sale_version=wash_sale_version,
    )
    acts.pop()  # replace the historical v20 adoption with the Track 2 adoption

    def add(kind: str, payload: dict[str, object]) -> None:
        acts.append(_act(len(acts), kind, payload))

    add("bundle-adoption", {"bundle": _load("f1099r-ira.bundle.v2.json")})
    amounts = [1200.0] if amounts is None else amounts
    payer = "demo.ira.payer.alpha"
    add(
        "entity-introduced",
        {"entity": {"schema": "entity.v1", "id": payer, "kind": "tax.us.ira-payer", "label": "Synthetic IRA payer"}},
    )
    horizon = "demo.ira.h0"
    add(
        "horizon-genesis",
        {"family": {"id": IRA_FAMILY, "version": "v2"}, "scope": SCOPE_KEY, "horizon_id": horizon},
    )
    for index, amount in enumerate(amounts):
        statement = f"demo.ira.statement.{index}"
        add(
            "entity-introduced",
            {"entity": {"schema": "entity.v1", "id": statement, "kind": "tax.us.1099r-statement", "label": "Synthetic Form 1099-R"}},
        )
        for fact_type, value, suffix in (
            (IRA_BOX2A, amount, "box2a"),
            (IRA_CHECKBOX, True, "checkbox"),
            (IRA_CODE, "7", "code"),
            (IRA_BOX2B, False, "box2b"),
        ):
            add(
                "assertion",
                {"finding": _attested(f"demo.ira.finding.{suffix}.{index}", f"{fact_type}|payer={payer},statement={statement},tax-year=2025", value)},
            )
        next_horizon = f"demo.ira.h{index + 1}"
        add(
            "member-transition",
            {
                "family": {"id": IRA_FAMILY, "version": "v2"},
                "scope": SCOPE_KEY,
                "member": {
                    "action": "assert",
                    "finding": _attested(f"demo.ira.finding.box1.{index}", f"{IRA_BOX1}|payer={payer},statement={statement},tax-year=2025", amount),
                },
                "successor": {"id": next_horizon, "predecessor": horizon},
            },
        )
        horizon = next_horizon
    if close:
        add(
            "assertion",
            {"finding": _attested("demo.ira.closure", f"{IRA_CLOSURE}|family-horizon={horizon},tax-year=2025", True)},
        )
    adoption = _load_fixture_adoption()
    adoption["committed_against"] = len(acts)
    acts.append(adoption)
    return acts

def _load_fixture_adoption() -> dict[str, object]:
    return cast(dict[str, object], json.loads((FIXTURES / "adoptions" / "adopt-core-v26-current.json").read_text("utf-8")))
