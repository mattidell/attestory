"""Deterministic 1099-INT statement sameness and anti-duplication.

ADR-0015 decision 5: production assertion defines statement sameness,
rejects duplicates, and classifies correction versus new original —
without using evidence identity as a shortcut. A logical statement
instance is one furnished information return; its sameness key is the
payer, tax year, and the payer's own statement reference (the payer's
account/form designation as printed, not any file or upload identity).

The functions are pure and total over their declared errors: an
evidence-flavored reference is rejected loudly, never normalized away.
"""

from __future__ import annotations

from dataclasses import dataclass

# Markers that betray an evidence/document key being smuggled into
# statement identity (ADR-0015 decision 2). Matched on word boundaries
# of the lowercased reference.
_EVIDENCE_MARKERS = ("evidence", "upload", "document", "file", "scan", "pdf")

NEW_ORIGINAL = "new-original"
CORRECTION = "correction"
DUPLICATE = "duplicate"


class StatementIdentityError(Exception):
    """A statement reference tries to key identity on evidence."""


@dataclass(frozen=True)
class StatementKey:
    """The sameness key of one logical furnished return."""

    payer_id: str
    tax_year: str
    payer_ref: str


def statement_key(payer_id: str, tax_year: str, payer_ref: str) -> StatementKey:
    """Build the deterministic sameness key, rejecting evidence keys."""
    if not payer_id or not tax_year or not payer_ref:
        raise StatementIdentityError("statement key parts must be non-empty")
    lowered = payer_ref.lower()
    for marker in _EVIDENCE_MARKERS:
        if marker in lowered:
            raise StatementIdentityError(
                f"statement reference {payer_ref!r} carries the evidence "
                f"marker {marker!r}; evidence cannot key a fact (Article 1, "
                "ADR-0015)"
            )
    return StatementKey(payer_id=payer_id, tax_year=tax_year, payer_ref=payer_ref)


def statement_entity_id(key: StatementKey) -> str:
    """The deterministic entity id for a statement instance."""
    return f"stmt.{key.payer_id}.{key.tax_year}.{key.payer_ref}"


def classify_assertion(
    key: StatementKey,
    recorded: frozenset[StatementKey],
    *,
    corrected: bool,
) -> str:
    """Classify one incoming return against the recorded statement set.

    A corrected copy of a recorded logical return is a CORRECTION: it
    answers the same fact and supersedes the prior finding. An
    uncorrected copy of a recorded return is a DUPLICATE and is
    rejected — asserting it again would double-count the interest. An
    unrecorded key is a NEW_ORIGINAL and individuates a new fact, even
    when the payer (or the payer and account) already has other
    recorded statements.
    """
    if key in recorded:
        return CORRECTION if corrected else DUPLICATE
    if corrected:
        raise StatementIdentityError(
            f"corrected return {key.payer_ref!r} matches no recorded "
            "statement; a correction must correct something"
        )
    return NEW_ORIGINAL
