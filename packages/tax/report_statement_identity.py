"""Document-side (Form 1099-INT) payer and statement identity derivation.

This module is the **document-side** counterpart to
``packages.tax.obligation_acquisition_mapping``'s ordinary-language-side
identity derivation. It exists so a reader can independently verify that two
genuinely separate code paths converge on the same real-world entity
identity, instead of one side manufacturing agreement by calling the other's
function.

**The shared convention, stated once, followed independently by both
modules.** A real-world payer name and a real-world statement/account
reference (as they would each appear on a person's own Form 1099-INT or
account statement) canonicalize to entity identity the same way on both the
document side (this module) and the ordinary-language side
(``obligation_acquisition_mapping``):

1. The payer entity id is the payer name string, trimmed of leading/trailing
   whitespace, with no other transformation.
2. The statement entity id is composed as
   ``f"{payer_entity_id}::statement::{reference.strip()}"`` — the trimmed
   statement/account reference, scoped under the same trimmed payer entity
   id, joined by the literal separator ``"::statement::"``.

Both modules implement this convention **independently** — this module does
not import or call anything in ``obligation_acquisition_mapping``, and that
module does not import or call anything here. Each module's own docstring
states the shared convention explicitly so a reader can see the two sides
agree because they follow the same documented rule, not because one
literally invokes the other. This is the same reason two different filers'
EINs match when they name the same real-world employer — both follow the
IRS's format for that employer's own assigned number — not because one
filer copied code from the other.

**What this module adds beyond the shared convention.** It also wires a
real, if minimal, "contribute a documentary Form 1099-INT box-1 report"
path: ``contribute_1099int_report`` builds the family-membership successor
act (box-1 reports are family-scoped facts, ADR-0017) and admits it through
``packages.kernel.contribution.apply_contribution_batch`` — the same real
contribution/admission boundary
``obligation_acquisition_mapping.contribute_ordinary_acquisition`` uses on
the acquisition side — rather than a test hand-assembling a member-transition
act with no admission check at all.

**Named limits.** Family-horizon predecessor/successor identification is the
caller's responsibility here, exactly as it already is for every other
box-1 fixture in this repository (see e.g.
``tests/test_package_membership_wiring.py``'s ``_t2_acts``): this module does
not attempt to discover "the current" family horizon from a projected state,
because the wider family-membership machinery
(``packages.kernel.findings``) already owns that concern and inventing a
second resolution path here would duplicate it, not repair anything this
seam's findings named. A caller who does not already know the current
horizon id must resolve it the same way every existing box-1 fixture does.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from packages.kernel.contribution import ContributionBatchResult, apply_contribution_batch
from packages.kernel.findings import FindingState
from packages.kernel.schema_registry import SchemaRegistry

# Production fact-type and entity-kind ids, re-validated against committed
# content (``packages/content/tax/2025/f1099int.bundle.json``) — not assumed.
REPORT_FACT_TYPE = "tax.us.2025.f1099int.box1-interest"
PAYER_ENTITY_KIND = "tax.us.interest-payer"
STATEMENT_ENTITY_KIND = "tax.us.1099int-statement"

# The family a box-1 report finding belongs to (ADR-0017 membership horizons).
FAMILY_ID = "tax.us.2025.f1099int.b1"
FAMILY_VERSION = "v1"


def derive_reported_payer_entity_id(payer_name: str) -> str:
    """The entity id for the payer named on a Form 1099-INT (document side).

    Implements the shared convention documented at module level: the
    trimmed payer name, no other transformation. Written independently of
    ``obligation_acquisition_mapping.derive_payer_entity_id`` — this
    function does not call it, and is not called by it — but both must
    resolve to the identical entity id for the same real-world payer name,
    because both follow the same documented rule.
    """
    return payer_name.strip()


def derive_reported_statement_entity_id(
    *, payer_name: str, statement_reference: str
) -> str:
    """The entity id for a specific box-1 statement/account (document side).

    Implements the shared convention documented at module level: the
    trimmed statement/account reference, scoped under the payer entity id
    by the literal separator ``"::statement::"``. Written independently of
    ``obligation_acquisition_mapping.derive_reported_statement_entity_id`` —
    this function does not call it, and is not called by it — but both must
    resolve to the identical entity id for the same real-world payer and
    reference, because both follow the same documented rule.
    """
    payer_entity_id = derive_reported_payer_entity_id(payer_name)
    normalized_reference = statement_reference.strip()
    return f"{payer_entity_id}::statement::{normalized_reference}"


def derive_1099int_box1_fact_id(
    *, payer_name: str, statement_reference: str, tax_year: int
) -> str:
    """The box-1 fact id one Form 1099-INT report resolves to.

    Composed from this module's own independently-derived payer and
    statement entity ids — never from
    ``obligation_acquisition_mapping``'s acquisition-side helper.
    """
    payer_entity_id = derive_reported_payer_entity_id(payer_name)
    statement_entity_id = derive_reported_statement_entity_id(
        payer_name=payer_name, statement_reference=statement_reference
    )
    return (
        f"{REPORT_FACT_TYPE}|payer={payer_entity_id},"
        f"statement={statement_entity_id},tax-year={tax_year}"
    )


def build_1099int_report_entity_acts(
    *, payer_name: str, statement_reference: str, act_index: int
) -> list[dict[str, Any]]:
    """Two ``entity-introduced`` acts: the payer and the statement.

    Entity introduction is its own act kind, applied before the
    family-membership transition that asserts the box-1 finding — exactly
    as ``obligation_acquisition_mapping.build_ordinary_acquisition_entity_acts``
    does on the acquisition side. A caller reusing an already-introduced
    payer entity (e.g. a second report from the same payer) is responsible
    for filtering the payer act out, the same responsibility that module's
    docstring already names.
    """
    payer_entity_id = derive_reported_payer_entity_id(payer_name)
    statement_entity_id = derive_reported_statement_entity_id(
        payer_name=payer_name, statement_reference=statement_reference
    )
    payer_act = {
        "schema": "act.v1",
        "act_id": f"demo-report-act-{act_index:03d}",
        "kind": "entity-introduced",
        "actor": "user",
        "at": f"2026-01-01T00:00:{act_index % 60:02d}Z",
        "committed_against": act_index,
        "payload": {
            "entity": {
                "schema": "entity.v1",
                "id": payer_entity_id,
                "kind": PAYER_ENTITY_KIND,
                "label": f"Payer named on a reported Form 1099-INT: {payer_name}",
            }
        },
    }
    statement_act = {
        "schema": "act.v1",
        "act_id": f"demo-report-act-{act_index + 1:03d}",
        "kind": "entity-introduced",
        "actor": "user",
        "at": f"2026-01-01T00:00:{(act_index + 1) % 60:02d}Z",
        "committed_against": act_index + 1,
        "payload": {
            "entity": {
                "schema": "entity.v1",
                "id": statement_entity_id,
                "kind": STATEMENT_ENTITY_KIND,
                "label": f"Statement/account named on a reported Form 1099-INT: {statement_reference}",
            }
        },
    }
    return [payer_act, statement_act]


@dataclass(frozen=True)
class ReportStatementContribution:
    """The synthetic acts one Form 1099-INT box-1 report contribution produces."""

    contribution_act: dict[str, Any]
    member_transition_act: dict[str, Any]
    finding: dict[str, Any]


def build_1099int_report_contribution(
    *,
    payer_name: str,
    statement_reference: str,
    tax_year: int,
    amount: float,
    scope: Mapping[str, str],
    family_predecessor_id: str,
    family_successor_id: str,
    act_index: int,
    contribution_id: str,
    evidence_id: str,
    finding_id: str,
    committed_against: int,
    fact_id: str | None = None,
) -> ReportStatementContribution:
    """Build the contribution + member-transition acts for one box-1 report.

    ``basis`` is ``"documentary"`` — this is what a payer's own document
    reported, not what the person attested to about their own affairs (see
    ``packages/sample_data/identity_association/examples/finding.v2.box1-s2.json``
    for the same convention already used by this repository's own committed
    example).
    """
    resolved_fact_id = fact_id or derive_1099int_box1_fact_id(
        payer_name=payer_name,
        statement_reference=statement_reference,
        tax_year=tax_year,
    )
    finding = {
        "schema": "finding.v2",
        "id": finding_id,
        "fact_id": resolved_fact_id,
        "value": amount,
        "basis": "documentary",
        "evidence_ids": [evidence_id],
        "contribution_id": contribution_id,
    }
    contribution_act = {
        "schema": "act.v1",
        "act_id": f"demo-report-act-{act_index:03d}",
        "kind": "contribution",
        "actor": "user",
        "at": f"2026-01-01T00:00:{act_index % 60:02d}Z",
        "committed_against": committed_against,
        "payload": {
            "contribution": {
                "schema": "contribution.v1",
                "id": contribution_id,
                "evidence_id": evidence_id,
                "content": {"mode": "document-report-entry", "synthetic": True},
            }
        },
    }
    member_transition_act = {
        "schema": "act.v1",
        "act_id": f"demo-report-act-{act_index + 1:03d}",
        "kind": "member-transition",
        "actor": "user",
        "at": f"2026-01-01T00:00:{(act_index + 1) % 60:02d}Z",
        "committed_against": committed_against + 1,
        "payload": {
            "family": {"id": FAMILY_ID, "version": FAMILY_VERSION},
            "scope": dict(scope),
            "member": {"action": "assert", "finding": finding},
            "successor": {
                "id": family_successor_id,
                "predecessor": family_predecessor_id,
            },
        },
    }
    return ReportStatementContribution(
        contribution_act=contribution_act,
        member_transition_act=member_transition_act,
        finding=finding,
    )


def contribute_1099int_report(
    state: FindingState,
    *,
    payer_name: str,
    statement_reference: str,
    tax_year: int,
    amount: float,
    scope: Mapping[str, str],
    family_predecessor_id: str,
    family_successor_id: str,
    registry: SchemaRegistry,
    record_id: str,
    act_index: int,
    contribution_id: str,
    evidence_id: str,
    finding_id: str,
    committed_against: int,
    fact_id: str | None = None,
) -> ContributionBatchResult:
    """Contribute one documentary box-1 report through the real admission
    boundary in one step.

    This is this module's load-bearing guarantee, mirroring
    ``obligation_acquisition_mapping.contribute_ordinary_acquisition`` on
    the acquisition side: the finding is not treated as real until
    ``packages.kernel.contribution.apply_contribution_batch`` — the same
    machinery every other manual-entry or documentary fact goes through —
    admits it.
    """
    built = build_1099int_report_contribution(
        payer_name=payer_name,
        statement_reference=statement_reference,
        tax_year=tax_year,
        amount=amount,
        scope=scope,
        family_predecessor_id=family_predecessor_id,
        family_successor_id=family_successor_id,
        act_index=act_index,
        contribution_id=contribution_id,
        evidence_id=evidence_id,
        finding_id=finding_id,
        committed_against=committed_against,
        fact_id=fact_id,
    )
    return apply_contribution_batch(
        state,
        contribution_act=built.contribution_act,
        successor_acts=[built.member_transition_act],
        registry=registry,
        record_id=record_id,
        workspace_revision=committed_against,
    )
