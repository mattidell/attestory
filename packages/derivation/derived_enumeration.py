"""Fact-type enumeration for attachment-rule.v11 derived rows.

``enumerate_published`` follows the declared fact-type id. Runtime symbols
must equal that id or use it as ``{fact_type_id}|…``. The producing rule's
``publishes`` field is not the prefix: pairing-scoped current-year adjustment
publishes ``tax.us.2025.interest.current-year-adjustment`` but instantiates
``tax.us.2025.interest.current-year-adjustment.pairing-scoped``.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


def fact_type_matches_symbol(symbol: str, fact_type_id: str) -> bool:
    if not symbol or not fact_type_id:
        return False
    return symbol == fact_type_id or symbol.startswith(fact_type_id + "|")


def enumerate_published_findings(
    publications: Sequence[Any],
    fact_type_id: str,
) -> list[Mapping[str, Any]]:
    """Return published findings whose symbol instantiates ``fact_type_id``."""
    found: list[Mapping[str, Any]] = []
    for pub in publications:
        finding = pub.finding if hasattr(pub, "finding") else pub
        if not isinstance(finding, Mapping):
            continue
        symbol = finding.get("symbol")
        if isinstance(symbol, str) and fact_type_matches_symbol(symbol, fact_type_id):
            found.append(finding)
    return found


def derived_activity_present(
    *,
    publications: Sequence[Any],
    dispositions: Iterable[Mapping[str, Any]],
    fact_type_id: str,
) -> bool:
    """True if any current published or blocked finding instantiates the fact-type.

    Absence is not a negative assertion. A retracted last allocation that
    leaves no current finding removes the activity.
    """
    if enumerate_published_findings(publications, fact_type_id):
        return True
    for row in dispositions:
        if row.get("disposition") != "blocked":
            continue
        symbol = row.get("symbol")
        if isinstance(symbol, str) and fact_type_matches_symbol(symbol, fact_type_id):
            return True
    return False
