# ADR 0072 — Legacy/Pairing-Scoped Interest Coexistence and Migration

- Status: **accepted**
- Tier: 2 — production coexistence and migration path for the interest
  vertical; not a product-thesis or governance-meaning decision.
- Date: 2026-08-30

## Context

The incumbent Schedule B accrued-interest-subtotal path
(`rule.scheduleb-adjustment.accrued-interest-subtotal` and its fact type)
and the new pairing-scoped mechanism (ADR-0067 through ADR-0071) can both
name a claim against the same real-world obligation. The legacy fact type
carries no payer, report, or acquisition identity — it cannot be
correlated against a pairing-scoped claim by anything but its amount. Left
uncoordinated, the same obligation could be double-counted: once through
the legacy path, once through the new one. This decision defines how the
two coexist during migration, how a same-amount collision is detected and
resolved, and what closes the gap into a single-subtractand successor
rule — without editing, deleting, or reinterpreting the legacy fact type,
which schema immutability forbids.

## Decision

1. **The legacy accrued-interest input surface is retired for new
   obligations; the legacy fact type is never edited, deleted, or
   reinterpreted.** New acquisitions enter through the pairing-scoped
   mechanism. The incumbent fact type and its adopted rule remain valid,
   immutable history, continuing to serve any workspace that already
   depends on them.
2. **A same-amount collision trigger fires when a new pairing is created
   against live legacy content.** Amount equality against a live legacy
   accrued-interest fact in the same workspace is the only correlating
   signal available, because the legacy fact type carries no payer,
   report, or acquisition identity to compare against directly. This
   trigger has named limits: a false positive (two genuinely different
   obligations that happen to share an amount) costs only a resolution
   step; a false negative — the same obligation entered twice, through
   both paths, with a mismatched amount — is not closed by this
   mechanism and remains a named residual risk.
3. **Resolution is a same-identity correction on the legacy fact type's
   own declared `supersession.policy: "free"`, not a new displacement
   edge.** The legacy fact type already declares free same-identity
   correction; a collision resolves by correcting that fact's own value,
   including down to zero, using the mechanism the fact type already
   supports. `DECLARED_EDGE_KINDS` (`{derivation, individuation}`) is
   unchanged — no new edge kind is introduced for this resolution.
4. **A single-subtractand successor rule, `rule.form1040-line2b.v6`,
   reached only via a real migration-adoption act.** `v6` is additive; it
   never replaces `v5` in place. Migration to `v6` for a given workspace
   is authorized by a real, evidenced migration-adoption act, not an
   automatic, silent switch. The migration-resolution rule is:
   - A live or withdrawn legacy predecessor fact whose true (last
     recorded) value is nonzero always blocks migration.
   - A genuinely zero predecessor migrates freely, including on a bare
     withdrawal that names no replacement.
   - The only currently accepted resolution for a nonzero claim is a
     same-identity correction (Decision 3) to a genuinely zero value.
   - Withdrawal never by itself resolves a nonzero claim, regardless of
     any claimed correspondence to a replacement fact: no accepted
     mechanism can check a claimed representation transfer against
     anything, because the legacy fact type carries no obligation,
     payer, or report identity to check it against.
   - `act-member-transition.v3`'s `corresponds_to_fact_id` field is
     recorded (`FindingState.withdrawal_correspondence`) when present on
     a v3-shaped removal act — the field is schema-real and round-trips
     through the act log — but no migration-adoption check reads it for
     authority. It is disclosed provenance only, not a resolution
     mechanism.
   - Whether to build an explicit representation-transfer adjudication
     act — a new, dedicated act kind carrying an accountable "I attest
     this is the same obligation" statement, checked for presence only,
     never for correctness — or to accept that migration never completes
     for a nonzero claim without a genuine zero-correction, is the
     smallest owner decision this ADR identifies and does not make. It
     is disclosed as open and owner-held.
5. **An unmigrated, legacy-only workspace is untouched.** No workspace is
   forced to migrate; a workspace with no pairing-scoped claims and no
   migration-adoption act continues to compute exactly as it does today.
6. **Two genuinely different obligations are never falsely conflated.**
   The collision trigger is silent whenever the legacy and pairing-scoped
   amounts differ — it fires only on exact amount equality, and produces
   no disposition, false or otherwise, when they do not match.

## Production conditions (owed to production implementation; never allowlisted)

- Decide the product surface for resolving a collision-trigger
  disposition: this repository is engine-only, so no UI or intake flow
  exists yet for prompting a same-identity correction.
- The same obligation entered twice with a mismatched amount (Decision 2)
  remains a named residual risk, coordinated with ADR-0068's own named
  residual risk of the same shape.
- The representation-transfer adjudication question (Decision 4) is
  open and owner-held; no migration path exists today for a nonzero
  legacy claim short of a genuine zero-correction.
- Coordinate with ADR-0068's statement-level association gap and
  ADR-0071's later-year basis-consequence-consumer gap: all three name
  adjacent, currently-open production surfaces in the same interest
  vertical.

## Consequences

- A future non-document tax fact facing the same legacy/new-mechanism
  coexistence problem repeats this pattern: retire the input surface for
  new entries, detect collision on the best available correlating
  signal, resolve via the legacy fact type's own declared correction
  policy, and gate the successor rule behind a real migration-adoption
  act rather than a silent automatic switch.
- **Resolved.** The migration artifact, the domain migration-resolution-
  policy map, the migrated `rule.form1040-line2b.v6`, and
  `package.core-calculations.v35` are all built and adopted (not merely
  planned): `packages/content/tax/2025/scheduleb-accrued-interest.succession.json`
  is the real migration artifact naming the successor claim type;
  `packages/tax/loader.py`'s `domain_migration_resolution_policies` /
  `install_domain_migration_resolution_policies` install the resolution
  map every `tax_registry()` and `live_coordinate_run` call already picks
  up; `rule.form1040-line2b.v6.json` is the single-subtractand successor
  rule; and `package.core-calculations.v35.json` admits all four,
  reachable only through the real `scheduleb-accrued-interest.succession`
  migration-adoption sequence (`tests/test_legacy_pairing_coexistence_migration.py`
  exercises the complete sequence end to end through the real production
  coordinator). Representation-transfer adjudication (Decision 4) remains
  the one genuinely unbuilt, owner-held item — see Production conditions
  above.
- The incumbent Schedule B fact type and its adopted rule remain valid,
  immutable history throughout; this decision never edits, migrates, or
  deprecates them in place.
- The collision-detection trigger (Decision 2) is wired into the
  production `associate()` path (`_live_legacy_collision_fact_ids`,
  `_publish_or_refuse_collision` in `packages/tax/identity_association.py`).
  The real `rule.form1040-line2b.v6` rule artifact and its
  migration-adoption act/content citizen (Decision 4) are built and
  adopted, admitted from `package.core-calculations.v35` onward.

## Alternatives Considered

- **Retiring the legacy input surface alone, with no collision
  detection.** Rejected: insufficient on its own — a workspace with
  pre-existing legacy content and a newly-entered pairing-scoped claim
  against the same obligation would double-count with no signal at all.
- **A standing reconciliation mechanism between the legacy and
  pairing-scoped fact types.** Rejected: broader than this milestone's
  need; the two fact types share no identity to reconcile against beyond
  amount, and a general reconciliation mechanism would be disproportionate
  to that one signal.
- **Automatic cross-type displacement**, where a pairing-scoped claim
  directly displaces a matching legacy fact. Rejected: no declared edge
  kind supports cross-fact-type displacement in this codebase, and
  amount equality alone is not sufficient evidence to justify introducing
  one.
- **Treating withdrawal-with-correspondence as sufficient resolution for
  a nonzero legacy claim.** Rejected: `corresponds_to_fact_id` is an
  unchecked, self-asserted field; treating it as authoritative would let
  an unverified claim resolve a real double-counting risk.
- **Leaving both mechanisms live indefinitely, with no migration
  path.** Rejected: leaves every workspace permanently on the legacy
  fact type's structurally-incapable identity, the exact defect
  ADR-0071 exists to replace.
