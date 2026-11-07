"""A noncovered scalar amount requires the sale it belongs to."""

from __future__ import annotations

from types import SimpleNamespace
from typing import cast

import pytest

from packages.kernel.currency import CurrencyView
from packages.kernel.findings import FindingModelError, FindingState, _enforce_companion_presence
from packages.kernel.schema_registry import SchemaRegistry
from packages.tax.loader import noncovered_scalar_presence_pairs

SALE = "tax.us.2025.f1099b.noncovered-st-txn"
SCALAR = "tax.us.2025.f1099b.noncovered-st-txn.proceeds"
SUFFIX = "broker=demo-broker,statement=demo-1,transaction=demo-1,tax-year=2025"


def _view(*finding_ids: str) -> CurrencyView:
    return CurrencyView(
        current_finding_ids=frozenset(finding_ids),
        displaced_finding_ids=frozenset(),
        current_evidence_ids=frozenset(),
        displaced_evidence_ids=frozenset(),
    )


def _registry() -> SchemaRegistry:
    return cast(
        SchemaRegistry,
        SimpleNamespace(
            companion_presence_pairs=noncovered_scalar_presence_pairs(),
            companion_value_domains={},
        ),
    )


def test_each_scalar_names_its_sale() -> None:
    pairs = noncovered_scalar_presence_pairs()
    assert pairs == {
        "tax.us.2025.f1099b.noncovered-st-txn.proceeds": "tax.us.2025.f1099b.noncovered-st-txn",
        "tax.us.2025.f1099b.noncovered-st-txn.basis": "tax.us.2025.f1099b.noncovered-st-txn",
        "tax.us.2025.f1099b.noncovered-st-txn.adjustment": "tax.us.2025.f1099b.noncovered-st-txn",
        "tax.us.2025.f1099b.noncovered-lt-txn.proceeds": "tax.us.2025.f1099b.noncovered-lt-txn",
        "tax.us.2025.f1099b.noncovered-lt-txn.basis": "tax.us.2025.f1099b.noncovered-lt-txn",
        "tax.us.2025.f1099b.noncovered-lt-txn.adjustment": "tax.us.2025.f1099b.noncovered-lt-txn",
    }


def test_a_scalar_without_its_sale_blocks_with_a_reason() -> None:
    fact_id = f"{SCALAR}|{SUFFIX}"
    state = FindingState(findings={
        "demo.ns.t1.scalar": {"fact_id": fact_id, "value": "100"},
    })
    with pytest.raises(FindingModelError, match="companion presence violated") as raised:
        _enforce_companion_presence(state, _registry(), (fact_id,), _view("demo.ns.t1.scalar"))
    message = str(raised.value)
    assert SCALAR in message
    assert SALE in message


def test_a_scalar_beside_its_sale_is_admitted() -> None:
    scalar_id = f"{SCALAR}|{SUFFIX}"
    sale_id = f"{SALE}|{SUFFIX}"
    state = FindingState(findings={
        "demo.ns.t1.scalar": {"fact_id": scalar_id, "value": "100"},
        "demo.ns.t1.sale": {"fact_id": sale_id, "value": "{}"},
    })
    _enforce_companion_presence(
        state, _registry(), (scalar_id, sale_id), _view("demo.ns.t1.scalar", "demo.ns.t1.sale"),
    )
