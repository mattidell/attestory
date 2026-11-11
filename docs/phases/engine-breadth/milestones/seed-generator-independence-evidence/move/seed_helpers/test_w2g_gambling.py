"""Scratch copy of helpers the v70 entry seed calls. Not a production module."""

from __future__ import annotations

from typing import Any
from typing import Sequence
from seed_helpers.test_form_1099_withholding import _add
from seed_helpers.test_form_1099_withholding import _base
from seed_helpers.test_form_1099_withholding import _close
from seed_helpers.test_form_1099_withholding import _social_security_withholding
from seed_helpers.test_form_1099_withholding import _unemployment_withholding
from seed_helpers.test_refund_or_amount_owed_track1 import _attested
from seed_helpers.test_refund_or_amount_owed_track1 import _load

P = "tax.us.2025."

YEAR = "2025"

SCOPE_KEY = {"tax-year": YEAR, "subject": "demo.primary"}

B1_FAMILY = P + "w2g.b1"

B4_FAMILY = P + "w2g.b4"

BOX1 = P + "w2g.box1-winnings"

BOX4 = P + "w2g.box4-withholding"

B1_CLOSURE = P + "w2g.b1.source-closure"

B4_CLOSURE = P + "w2g.b4.source-closure"

SCOPE_ANSWER = P + "w2g-scope.no-sch1-other-income-except-w2g"

def _v64_return(*, wages: float = 50000.0, w2: float = 4500.0, joint: bool = False) -> list[dict[str, object]]:
    """A complete return as core v64 asks it: no W-2G fact exists, every earlier answer given."""
    acts = _base(wages=wages, w2_withheld=w2, joint=joint)
    _unemployment_withholding(acts, [])
    _social_security_withholding(acts, [])
    return acts

def _w2g(
    acts: list[dict[str, object]],
    statements: Sequence[tuple[float | None, float | None]],
    *,
    b1: str = "closed",
    b4: str = "closed",
    other_income: str | None = "yes",
) -> None:
    """Records Form W-2G statements as (box 1, box 4) pairs and the three v65 answers.

    ``b1`` / ``b4`` is ``"closed"`` (closure attested after the last member), ``"never"`` (no
    closure) or ``"stale"`` (closed after the first statement, then a later statement is
    recorded so the closure is behind the family's horizon). ``None`` for a box records no
    amount on that statement. ``other_income`` is the new Schedule 1 answer (None leaves it
    unanswered).
    """
    _add(acts, "bundle-adoption", {"bundle": _load("w2g.bundle.json")})
    heads = {B1_FAMILY: "demo.w2g.b1.h0", B4_FAMILY: "demo.w2g.b4.h0"}
    for family, head in heads.items():
        _add(acts, "horizon-genesis", {"family": {"id": family, "version": "v1"}, "scope": dict(SCOPE_KEY), "horizon_id": head})
    modes = {B1_FAMILY: b1, B4_FAMILY: b4}
    closures = {B1_FAMILY: B1_CLOSURE, B4_FAMILY: B4_CLOSURE}
    names = {B1_FAMILY: "b1", B4_FAMILY: "b4"}
    for i, (box1, box4) in enumerate(statements):
        keys = (("payer", f"demo.w2g.payer.{i}"), ("statement", f"demo.w2g.stmt.{i}"))
        _introduce(acts, f"demo.w2g.payer.{i}", "tax.us.gambling-payer")
        _introduce(acts, f"demo.w2g.stmt.{i}", "tax.us.w2g-statement")
        for family, fact_type, amount, tag in ((B1_FAMILY, BOX1, box1, "box1"), (B4_FAMILY, BOX4, box4, "box4")):
            if amount is None:
                continue
            heads[family] = _transition(
                acts, (family, "v1"), heads[family], f"demo.w2g.{names[family]}.h{i + 1}",
                f"demo.w2g.{tag}.{i}", fact_type, keys, amount,
            )
        if i == 0 and len(statements) > 1:
            for family in heads:
                if modes[family] == "stale":
                    _close(acts, closures[family], heads[family], f"demo.w2g.closure.{names[family]}.stale")
    for family in heads:
        if modes[family] == "closed":
            _close(acts, closures[family], heads[family], f"demo.w2g.closure.{names[family]}")
    if other_income is not None:
        _add(acts, "assertion", {"finding": _attested("demo.w2g.scope.other-income", f"{SCOPE_ANSWER}|tax-year={YEAR}", other_income)})

def _w2g_return(
    statements: Sequence[tuple[float | None, float | None]],
    *,
    wages: float = 50000.0,
    w2: float = 4500.0,
    joint: bool = False,
    **kwargs: Any,
) -> list[dict[str, object]]:
    acts = _v64_return(wages=wages, w2=w2, joint=joint)
    _w2g(acts, statements, **kwargs)
    return acts
