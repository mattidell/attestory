# ADR 0015 - 1099-INT Statement-Instance Identity

- Status: proposed
- Tier: 2
- Date: 2026-07-12

## Context

Taxable-interest facts must distinguish multiple information returns from one
payer, preserve correction history, and remain peer to evidence. Payer/account
and logical-statement rivals were exercised on the same synthetic cases.

Evidence: `docs/prototypes/source-completeness/evaluation-analysis.md`, C4.

## Decision

1. A Form 1099-INT taxable-interest fact is keyed by tax year, subject, payer,
   and a logical Form 1099-INT statement-instance citizen.
2. The statement instance represents one logical furnished information return.
   It is peer to evidence; file, upload, scan, document, and evidence ids are
   forbidden from fact identity.
3. Multiple original returns from one payer are distinct statement instances,
   including multiple returns concerning one account.
4. A corrected copy of the same logical return answers the same fact and
   supersedes its prior finding. A separate original return is new individuation.
5. Production assertion must define deterministic statement sameness and
   anti-duplication and classify correction versus void/reissue without using
   evidence identity as a shortcut.

## Not Decided

- source-family claim/coverage semantics (SC-P3);
- legal/documentary correction workflow beyond mechanical fact correction;
- account presentation/provenance fields; or
- production schema ids/bytes.

## Consequences

- Same-payer and same-account multiple returns do not collide.
- Evidence replacement does not rekey facts.
- Statement assertion and deduplication are explicit production contracts.
- Correction/displacement fixtures must preserve statement identity.

## Alternatives Considered

- Payer-only: rejected because multiple returns collide.
- Payer/account: rejected because multiple same-account returns collide and
  account correction can rekey the fact.
- Statement/document file id: rejected because evidence cannot key the fact.

## Links

- Analysis: `docs/prototypes/source-completeness/evaluation-analysis.md`
- Exhibits: `exhibits/source-completeness/it1`, `it2`
- Milestone: `docs/phases/foundation/milestones/source-completeness-and-interest-slice.md`
- Precedents: ADR-0005, ADR-0010, ADR-0011, ADR-0013
