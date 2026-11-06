"""``require_paired`` reads keys and blocks when a statement has no withholding row."""

from __future__ import annotations

import pytest

from packages.derivation.evaluator import (
    BLOCK_ABSENT,
    BLOCK_INVALID,
    LINK_COVERAGE_SCOPE_UNBOUND,
    AccessLog,
    Environment,
    EvalBlocked,
    PairedSourceRow,
    evaluate,
)

WITHHOLDING = "demo.tax.withholding"
INCOME = "demo.tax.income"
OTHER = "demo.tax.other-income"


def _row(finding_id: str, **keys: str) -> PairedSourceRow:
    return PairedSourceRow(finding_id=finding_id, keys=tuple(keys.items()))


def _rows(*rows: PairedSourceRow) -> tuple[PairedSourceRow, ...]:
    return rows


def _env(rows: dict[str, tuple[PairedSourceRow, ...]] | None) -> Environment:
    return Environment({}, {}, frozenset(), {}, {}, paired_sources=rows)


def _expr() -> dict[str, object]:
    return {
        "op": "require_paired",
        "key": "statement",
        "withholding": WITHHOLDING,
        "income": [INCOME, OTHER],
    }


def test_a_shared_statement_passes_and_records_the_rows_it_read() -> None:
    access = AccessLog()
    rows = {
        INCOME: _rows(_row("inc-1", statement="s1")),
        OTHER: _rows(_row("oth-1", statement="s1")),
        WITHHOLDING: _rows(_row("wh-1", statement="s1"), _row("wh-only", statement="s2")),
    }
    assert evaluate(_expr(), _env(rows), access) is True
    assert access.require_paired_findings == {"inc-1", "oth-1", "wh-1", "wh-only"}
    assert access.collects == set()
    assert access.operations == set()


def test_a_withholding_row_with_no_income_row_is_not_a_failure() -> None:
    access = AccessLog()
    rows = {WITHHOLDING: _rows(_row("wh-only", statement="s2"))}
    assert evaluate(_expr(), _env(rows), access) is True
    assert access.require_paired_findings == {"wh-only"}


def test_an_income_statement_without_withholding_names_the_withholding_fact() -> None:
    access = AccessLog()
    rows = {
        INCOME: _rows(_row("inc-1", statement="s1"), _row("inc-2", statement="s2")),
        WITHHOLDING: _rows(_row("wh-1", statement="s1")),
    }
    with pytest.raises(EvalBlocked) as raised:
        evaluate(_expr(), _env(rows), access)
    assert raised.value.category == BLOCK_ABSENT
    assert raised.value.missing == [WITHHOLDING]
    assert access.require_paired_findings == {"inc-1", "inc-2", "wh-1"}


def test_a_null_or_missing_key_names_the_finding() -> None:
    access = AccessLog()
    rows = {
        INCOME: _rows(PairedSourceRow("inc-null", None), _row("inc-other", payer="only")),
        WITHHOLDING: _rows(_row("wh-1", statement="s1")),
    }
    with pytest.raises(EvalBlocked) as raised:
        evaluate(_expr(), _env(rows), access)
    assert raised.value.category == BLOCK_INVALID
    assert raised.value.missing == ["inc-null", "inc-other"]
    assert access.require_paired_findings == {"inc-null", "inc-other"}


def test_an_uninstalled_slot_fail_closes() -> None:
    with pytest.raises(EvalBlocked) as raised:
        evaluate(_expr(), _env(None), AccessLog())
    assert raised.value.category == BLOCK_INVALID
    assert raised.value.missing == [LINK_COVERAGE_SCOPE_UNBOUND]


def test_zero_rows_of_every_named_type_pass() -> None:
    assert evaluate(_expr(), _env({}), AccessLog()) is True
