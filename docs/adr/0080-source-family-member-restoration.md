# ADR 0080 — Source-Family Member Restoration

- Status: **accepted** (2026-10-25; owner-approved restoration goal, with Foreman mechanism disposition after independent Sol review and repair recheck)
- Tier: 2 — source-family membership and current-standing contract
- Date: 2026-10-25

## Context

A member removed from a source family can be entered again. The current kernel
admits a fresh member assertion for the same fact ID through a valid successor
transition, but `withdrawn_fact_ids` remains monotonic. Currency consequently
roots every finding for that fact ID, including the newly admitted assertion.
The report cannot become current again. The mortgage statement restoration
witness reproduces this through the real `ActLog` admission path.

ADR-0073 describes member withdrawal as permanent for a fact ID in its Context
and Alternatives Considered. This decision changes that specific restriction;
it does not amend ADR-0073's bytes. The owner approved the bounded goal that a
fresh re-entry may become usable while earlier findings and their dependent
calculations remain ended. The mechanism below implements that bounded change.
Publication reconciliation, final candidate review and CI remain separate
delivery gates.

## Decision

1. Treat `withdrawn_fact_ids` as the current membership-absence projection,
   rather than a permanent tombstone. A valid fresh assertion clears that
   marker only when its transition predecessor descends from the recorded
   removal successor through validated horizon predecessors, including a
   legitimate family-version handover. This binds restoration to the chain
   that removed the member, not merely to a globally equal fact ID.
2. Keep historical end-of-support in the existing displacement projection.
   `_finding_corrections` already displaces earlier findings for a fact when a
   fresh finding is admitted; the old finding therefore remains ended after
   re-entry without a second stored history set. If the member is removed
   again, the active absence marker roots the then-current finding through the
   existing withdrawal root. A finding ended by another independent root
   (retraction, entity or migration supersession) remains ended under that
   root; restoration does not override it or bypass evidence or policy gates.
   A valid reclassification may restore a previously removed target fact and
   withdraw its currently active source fact in the same transition; both
   membership effects apply to the same successor horizon atomically.
3. A later removal ends the fresh current finding as well, and the sequence may
   repeat. Earlier findings remain displaced through correction, withdrawal,
   horizon-individuation and derivation-cascade rules. No old finding,
   closure, or derived publication is restored by re-entry.
4. Existing restrictions remain: same-member correction uses ordinary
   assertion; removal advances the family horizon; a fresh closure and rerun
   are required; supersession policy, evidence, entity and migration gates,
   retraction, and family-version retirement/containment continue to apply.
5. Previously admitted cross-chain re-adds remain readable during replay, but
   their fresh findings remain non-current and the removal marker remains
   active. A later correctly chained re-add may restore membership. New
   cross-chain restoration writes are refused atomically by both single-act
   and batch ActLog admission. For historical same-chain remove/re-add logs,
   the fresh assertion becomes current under this contract; the earlier
   finding remains ended, and publications pinned to predecessor findings or
   horizons remain displaced. This is not migration of saved artifacts or a
   claim about production persistence.

## Mechanism

Use the existing `withdrawn_fact_ids` set as the current membership-absence
projection, and retain the removal successor horizon ID as the minimum
authority needed to bind a future restoration to the correct lineage. The
existing correction root permanently displaces prior findings; the active
withdrawal root displaces findings while the member is absent. No separate
finding history/root set, act vocabulary, schema, edge kind, current flag on a
finding, or broad authority model is added. Full replay and incremental fold
must produce equal membership, currency and horizon state. New writes use the
already-built prospective projection to validate the lineage before append.

## Consequences

- Member removal remains an end to the then-current assertion, not a permanent
  ban on later assertions of the same fact identity.
- Append-only finding history and derivation/individuation edges remain intact.
- Historical same-chain ignored re-adds become current after adoption;
  historical unrelated-chain re-adds stay non-current. In either case old
  support and closure-backed results do not revive.

## Outside this decision

- Publication-number synchronization if this unmerged candidate collides with
  a newly ratified ADR.
- Any general undo, production persistence, migration, or UI behavior.

## Links

- Superseded restriction: ADR-0073, Context and Alternatives Considered.
- Preserved contracts: ADR-0010 (derivation currency), ADR-0017 (horizon and
  closure freshness), ADR-0023 (member assertion/transition boundary),
  ADR-0041 (supersession policy), ADR-0079 (family handover and containment).
- Implementation witness: `tests/test_member_restoration.py`.
- Consumer and scope: [mortgage milestone](../phases/tax-circumstance-breadth/milestones/mortgage-statement-borrowing.md).
