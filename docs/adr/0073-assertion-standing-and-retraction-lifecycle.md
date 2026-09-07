# ADR 0073 — Assertion Standing and Retraction Lifecycle

- Status: **accepted** (Track 0 of assertion-standing-retraction-semantics,
  closed 2026-09-06 with two independent reviews and their findings
  repaired; owner disposition 2026-09-06)
- Tier: 2 — first act that ends a finding's current support without
  supplying a replacement value; a fifth named displacement root; a
  correction to which of two existing current-standing resolutions is
  authoritative
- Date: 2026-09-06

## Context

Three things exist today and are routinely conflated: a **stable
proposition** (a fact, individuated by its declared identity keys), an
**immutable assertion event** (a finding — a value someone asserted for a
fact, on the record forever once admitted), and that fact's **current
standing** (whether some finding answering it is presently in force). The
kernel already has mechanisms that change current standing without
touching the underlying record: correction (a later finding for the same
fact wins), member withdrawal (`member-transition` removes a fact from a
family, keyed by fact id, monotonic — a withdrawn fact can never be
current again), entity supersession (individuation), and migration
supersession (ADR-0063). None of them let a person say "this specific
answer no longer stands" without asserting a replacement value or
retiring the whole fact.

Track 0 built and executed a fifth mechanism, retraction, against the real
kernel boundaries (`ActLog.append`, `findings.project`,
`findings.apply_act`), never a hand-built state
(`docs/prototypes/assertion-standing-retraction-semantics/track-0-findings.md`
§1). The kernel change is already committed:
`packages/schemas/kernel/act-finding-retracted.v1.schema.json`, and the
`_finding_retractions` root plus `retracted_finding_ids` /
`retraction_acts` state fields in `packages/kernel/currency.py` and
`packages/kernel/findings.py`. This ADR states the contract that
committed code already embodies, settles the one point Track 0 measured
as unsettled between two competing resolutions, and states the one
restriction Track 0 found and did not itself decide.

An independent review confirmed Track 0's central claim by re-running the
load-bearing tests and probes at the real admission boundary, not by
re-reading the findings prose, and returned READY. Two of its findings are
carried forward rather than
re-derived: that the Set B "no order of retractions succeeds" conclusion
for seven of the eight declared relations rests on a sound but unexecuted
prefix-closure argument, not on brute-force enumeration; and that
deliverable 4's reachability claim rests on one canonical equivalence case
plus a source-confinement check, not a sweep. Both are carried into
Decision 8 below rather than smoothed over.

The owner's 2026-09-06 disposition on the milestone plan
(`docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md`,
"## Owner disposition — 2026-09-06") separated two things Track 0 had
found entangled: the engine's own capability limits, written as admission
checks (an SSA statement admissible only if withholding is zero, a 1099-R
only if the distribution code is 7, a 1098-E only if box 2 is unchecked),
are deferred to a **successor milestone, not yet chartered**, and are not
decided here; unifying the two definitions of current standing, because it
is a defect and not a capability limit, and because one consequence of
leaving it unfixed is already live in production, stays in this milestone
and is decided below.

## Decision

1. **The three distinctions are load-bearing and are restated here as
   contract, not merely as vocabulary.** A stable proposition (the fact)
   is never mutated by retraction. An assertion event (the finding) is
   never deleted, edited, or reinterpreted by retraction — history is
   append-only. Current standing is the one thing retraction changes: it
   ends the current support supplied by one identified finding, supplies
   no replacement value, and asserts no opposite claim. This is the
   schema's own stated contract
   (`act-finding-retracted.v1.schema.json`'s `description`) and is proven,
   not merely declared, by `TestLifecycle::test_L3_retraction_leaves_no_current_answer_and_no_opposite_claim`.

2. **The act names one finding, never a fact.** The payload is exactly
   `{"finding_id": <string>}`, closed
   (`"additionalProperties": false`); no `fact_id`, `value`, `reason`,
   `replacement`, or `actor` is admitted
   (`TestPayloadContract::test_payload_admits_nothing_but_a_finding_id`).
   The fact the retraction affects is derived from the named finding, not
   supplied by the caller. Admission refuses a target that is not current
   under the full displacement-closure projection (`compute_currency`),
   and this covers a corrected-away finding, an already-retracted finding,
   an entity-displaced finding, and a migration-displaced finding alike —
   each refused with a distinctly attributed message
   (`correction by …`, `retraction by …`, `individuation by …`,
   `supersession by …`;
   `TestAdmissionRefusals::test_refusal_2_*`, independently re-run and
   confirmed by the review). A client that reads a stale revision and
   names a superseded finding is refused, never silently redirected to
   whatever is current for that fact now.

3. **The admission gate is the fact type's own supersession policy
   (ADR-0041), exactly as it gates a correction — never an actor check.**
   `free` permits retraction unconditionally, subject to (2) and (4).
   `locked` refuses retraction unconditionally, for the same reason
   ADR-0041 gives for refusing a second correction under `locked`: the
   fact is single-shot, and a fact whose one answer has been ended has no
   remedy — a `locked` fact retracted rather than corrected would become
   permanently unanswerable, which is worse than the second-answer problem
   `locked` exists to prevent. `closed-on-attestation` follows ADR-0041's
   own predicate (gated on the current value of the named closure fact) and
   is unaffected by retraction touching a different fact. No actor, role,
   or identity concept is introduced or consulted; who retracts is envelope
   provenance only, exactly as ADR-0041 already settles for correction
   (`TestAuthorityIsAStateGate::test_L7_*`: a different envelope actor
   changes nothing about the outcome).

   **What an admitted retraction therefore means, precisely.** A recorded
   actor has ended the workspace's current support for one identified
   finding. It does not establish that the finding's original author
   personally withdrew their statement: any recorded actor may end support
   for any finding the state gate permits, and actor identity is
   provenance that admission never consults. Durable text about this
   capability must not claim the original person no longer stands behind
   the answer. Whether ending support should require the original author
   is a real product question, unanswered here, and answering it would
   require the identity concept ADR-0041 deliberately declined to build.

4. **A fifth named displacement root, alongside the four `compute_currency`
   already had** (correction, member withdrawal, migration supersession,
   superseded entity). Like the other three act-contributed roots,
   retraction contributes only *roots* to `displacement_closure`, never a
   new edge kind: `DECLARED_EDGE_KINDS` remains exactly `{derivation,
   individuation}`
   (`TestEdgeVocabularyUnchanged::test_declared_edge_kinds_are_untouched`).
   A structural consequence, not a retraction-specific one, follows
   directly from how `displacement_closure` labels a dependent by the
   *edge* kind it walked, never by the root kind that started the walk: no
   root kind — retraction, correction, withdrawal, or migration
   supersession — can ever appear directly on a derived finding's own
   reason tuple. A derivation-dependent's reason is always
   `[("derivation", <pinned finding id>)]`; the retraction reason lives on
   the kernel finding it names,
   `[("retraction", <retracting act id>)]`. The two compose across the
   edge (`derived → pinned finding → retraction → act id`); both halves are
   independently asserted and neither is lost
   (`TestL10DerivationDependency`, and the nuance recorded in the findings
   file §1).

5. **One current-standing path serves every reader — this milestone's
   second stated aim, and the load-bearing decision.** The full
   `compute_currency` displacement-closure projection is the single
   resolution of current standing. There is no second, independently
   maintained definition: every reader either consults `compute_currency`
   directly or is handed the `CurrencyView` it produced.

   The kernel's `_current_value_for_fact` and `_current_values_for_fact_type`
   read that projection. Both accept an optional view so that one admission
   walks the closure once rather than once per fact-id lookup; omitting it
   computes the full projection, never a narrower fallback. The five kernel
   admission enforcers (`closed-on-attestation`, subset, companion
   presence, companion equality, declaration/signal) are threaded one view
   per admission. `read_models.build_read_model`,
   `derivation.marshal.marshal_run_context`,
   `derivation.projection.workspace_currency`, and the entry loop consult
   the same projection, as they already did.

   Two out-of-kernel readers were unified with it.
   `packages/tax/coverage.py::untranslated_source_findings` selects by
   `current_finding_ids`. `packages/tax/ssa_benefits.py::validate_projected_source_boundary`
   takes `current_finding_ids` as a required parameter in place of the
   withdrawn-fact-id set it previously took, and
   `packages/derivation/live.py` computes currency before the boundary
   check and passes it through. That signature had no channel through which
   retraction, entity supersession, or migration supersession could reach
   it, which is why production accepted a Social Security statement whose
   filing-status authority had been withdrawn. That defect is closed, with
   a regression that fails if the previous signature or body returns.

   Patching each reader's blind spot independently, one root at a time, is
   rejected as the wrong shape: it is what produced the fail-open gap, and
   it leaves in place the reason a narrower rule needed its own
   retraction-specific patch.

   **The migration path reads the same projection.**
   `_present_successor_claims` presents a claim only for a predecessor fact
   whose last recorded finding is current under that projection. It
   previously selected the last recorded finding minus withdrawn fact ids,
   so a retracted answer was still offered to the user as a live claim to
   carry forward.

   Because that filtering removes a retracted finding from the presented
   claims, the guard that protects ADR-0072's safety rule is stated over
   the same projection rather than over withdrawal alone.
   `_refuse_unresolved_nonzero_noncurrent_predecessors` refuses a
   `resolved-required` migration when a predecessor fact **still present in
   the current lattice** has a last recorded finding that is not current and
   a true last value that is nonzero. That range is exact and deliberate: it
   covers a live answer, a member-withdrawn one, and a retracted one, in one
   predicate. It changes no product meaning, because ADR-0072 Decision 4 is
   stated in terms of value rather than mechanism, so retraction simply joins
   withdrawal as a way an answer stops being live. A nonzero predecessor
   blocks whether live, withdrawn, or retracted; a genuinely zero one
   migrates freely in all three cases; and retraction resolves a nonzero
   claim no more than withdrawal does. A corrected fact's last finding is the
   correction and is current, so ordinary correction is undisturbed.

   **Entity succession is outside that range, and correctly so.** Superseding
   the entity a predecessor fact is keyed on removes the fact from the
   lattice, so no claim is presented for it and no block arises, even where
   its historical value was nonzero. That is not a gap in the guard: entity
   succession removes the proposition itself rather than ending an answer to
   it, and treating it as withdrawal or retraction would misdescribe what
   happened to the taxpayer's question. The boundary is exercised
   (`tests/test_migration_retraction_repair.py`).

6. **Dependency behaviour.** A derived result standing on a finding whose
   support is retracted ceases to be current, cascaded along the existing
   `derivation` edge exactly as a correction or migration supersession
   already cascades. It is never revived by a later assertion answering
   the same fact: reasserting the same value (even byte-identical) produces
   a new finding with a new id, and the derived result must be re-derived
   from that new finding — the retracted derivation-dependent stays
   displaced permanently
   (`TestL10DerivationDependency::test_L10_reassertion_produces_a_new_derived_id_and_no_revival`).
   Reuse of a retracted finding's own id is refused outright
   (`test_L4_revival_by_id_reuse_is_refused`).

7. **Attribution is recovered by act-log lookup, never copied onto a fact
   representation.** The displacement reason for a retracted finding is
   `("retraction", <retracting act's id>)`; the act id, not the fact id, is
   what discriminates, because a fact can be retracted, reasserted, and
   retracted again, and the act id is the only thing naming *which*
   retraction ended a given answer. The retracting act's own envelope
   carries actor and time; no actor, reason, or replacement field is added
   to any finding or fact schema by this ADR. The lookup is exercised
   end to end against a committed act log
   (`tests/test_assertion_standing_integration.py`), which walks from a
   finding id to the assertion act that carried it and from a displacement
   reason to the act that ended support. No reader-facing surface renders
   it yet; designing that presentation is not in this contract.

8. **The inherited restriction, stated exactly as measured, with its real
   cause.** On committed 2025 tax content, across the eight declared
   subset, companion-presence, and companion-equality relations (24
   distinct fact-type participants, exhaustiveness independently
   re-derived from `tax_registry()` by the review and matched field for
   field), **no order of retractions reaches any relation participant**:
   Set A (retractable directly) is empty; Set B (retractable only after
   retracting a dependent first) is empty; every participant sits in Set C
   (not retractable by any order of retractions). Of the 24, 9 were already
   fenced pre-existing by member-fact routing (refusal 5, ADR-0023
   Decision 1's routing rule); **fifteen are fenced specifically by the
   new sixth refusal** this track added
   (`_refuse_retraction_violating_admission_invariants`, admitted only if
   the prospective post-retraction state still satisfies every declared
   admission invariant — the same four enforcers `apply_assertion` already
   runs, re-run over the prospective state rather than a new rule).

   **The evidentiary weight behind "no order" is not uniform across the
   eight relations, and this ADR does not restate it as though it were.**
   Exhaustive enumeration — 13,699 orderings of every length, including all
   5,040 full-length permutations, through the real admission boundary,
   zero admitted — was executed for exactly one of the eight relations, the
   richest (SSA-1099 box 5 and its six witnesses). The other seven rest on
   a sound but unenumerated argument: every length-1 retraction of every
   one of their participants is independently refused, and a sequence can
   only succeed if its first act is admitted, so no longer sequence can
   begin (prefix closure). The independent review checked this argument's
   soundness and found no counterexample, and also found that the Track 0
   falsifiable list did not itself name this asymmetry as a falsifiable
   claim — a gap this ADR closes by stating it here rather than by
   widening the enumeration. **One enumeration and seven arguments is what
   was measured; this ADR states it as one enumeration and seven
   arguments, not as eight enumerations or as proof.**

   **The restriction's real cause is that the engine's own capability
   limits live in the admission layer, not that withdrawing an answer is
   inherently unsafe.** The four enforcers the sixth refusal re-runs —
   subset, companion-presence, companion-equality, declaration/signal — are
   witnesses the engine's own computation requires in order to compute at
   all (an SSA benefit computation requires box 3, 4, and 5 reconciled; a
   1099-R computation requires a supported distribution code witness), not
   statements about what the taxpayer is permitted to report. Ending an
   answer that another admitted answer's *computability* depends on would
   leave a state the engine cannot process, so the same admission
   machinery that refuses an inadmissible *assertion* also refuses the
   *retraction* that would produce the equivalent state — correctly, given
   where those limits currently live. This is a property of where the
   engine's capability limits sit today, not a property of retraction, and
   not a permanent property of this feature: the owner's 2026-09-06
   disposition on the milestone plan explicitly defers relocating those
   capability limits out of the admission layer to a **separately
   chartered successor milestone**, named as such and not decided here,
   while directing that this unification contract not wait for it. Two
   mitigations already exist and remain available for every one of the
   fifteen fenced fact types without that relocation: correction (including
   correcting an amount to zero) remains available for all fifteen, and the
   declared member-transition route unblocks every one of them immediately
   by removing the subordinate member fact itself
   (`test_correction_remains_available_for_every_fenced_participant`,
   `test_the_declared_member_transition_route_does_unblock_companions`).
   Whether some of the fifteen — particularly the amount fact types, where
   a user might reasonably want to withdraw a claim rather than correct it
   to zero or remove the whole statement — should be made withdrawable is a
   product question the successor milestone inherits; this ADR does not
   answer it and does not widen Set A or Set B to answer it by fiat.

## Payload Instantiation Gate

Discharged by citation, not re-expansion. The positive payload instance
(`docs/prototypes/assertion-standing-retraction-semantics/act-finding-retracted.v1.example.json`,
`{"finding_id": "demo-finding-attr-250"}`) validates against the published
schema and, independently re-run by the review, folds through the real
`findings.project` boundary
(`TestPayloadContract::test_committed_positive_instance_validates_against_the_published_schema`,
`test_committed_instance_drives_a_real_fold`). The schema is additive:
`packages/schemas/kernel/act-finding-retracted.v1.schema.json` is new, no
existing manifest hash changed, and the manifest gained exactly one
alphabetically-placed entry (review, "Schema/gate").

## Consequences

- The kernel contract in Decisions 1–4, 6, and 7 is already committed code
  (`act-finding-retracted.v1`, `_finding_retractions`,
  `retracted_finding_ids`, `retraction_acts`) and this ADR ratifies it as
  the assertion-standing contract rather than changing it.
- Decision 5 is executed in this milestone. Both tax-layer readers, the
  five kernel admission enforcers, and the migration path consult the one
  projection; the fail-open Social Security gap is closed with a
  regression that fails if the previous signature returns. Unifying costs
  a constant factor of roughly 1.55 to 1.6 on admission for the closure
  walk, with no change to asymptotic order. A cache was deliberately not
  built, because a cache would be a third definition of current standing,
  which is what this decision exists to remove.
- Decision 8's restriction remains in force exactly as stated — fifteen
  fact types are not withdrawable by retraction while their subordinate
  member stands — until a separately chartered successor milestone
  relocates the relevant capability limits or a different disposition is
  made. No content, rule, or kernel change in this ADR narrows or widens
  Set A/B/C.
- No new act kind beyond `act-finding-retracted.v1`, no new edge kind, no
  actor/role concept, and no schema amendment to any accepted ADR's text
  is introduced by this ADR.

## Alternatives considered

- **Patching `_current_value_for_fact`, `coverage.py`, and `ssa_benefits.py`
  independently, one missing root at a time.** Rejected: this is the shape
  that produced the disagreement this milestone repaired (each reader was
  made "retraction aware" or "withdrawal aware" separately and none was
  made fully projection-aware), and it does not remove the reason
  `_current_value_for_fact` needed a retraction-specific patch in the first
  place. Decision 5 instead names the full projection as the one target
  every reader converges on.
- **Treating retraction as reusing member withdrawal.** Disqualified on
  executed evidence, not merely by design preference: withdrawal is keyed
  by fact id and monotonic (a withdrawn fact can never be current again);
  retraction is keyed by finding id and a later assertion answering the
  same fact is admitted normally and becomes current. `test_L13_member_transition_removal_of_the_same_fact_is_admitted`
  demonstrates the two roots staying separate. Findings §5.
- **Widening Set A or Set B to make some or all of the fifteen fenced
  amount fact types directly withdrawable.** Rejected for this ADR:
  Track 0 flagged this as a genuine, un-decided product question (findings
  §6b, "The judgement call, flagged rather than made") and the owner's
  disposition assigns capability-limit relocation to a successor milestone
  rather than deciding it here. Deciding it now would require either a
  relation-aware exception to the sixth refusal or a different treatment of
  an absent companion — both explicitly out of this contract's scope.
- **Presenting the eight-relation restriction as fully enumerated.**
  Rejected: only the richest relation was exhaustively enumerated; the
  other seven rest on a sound argument, not a count. Overstating this would
  misrepresent evidence this contract is required to cite exactly.

## Not decided

- The exact signature or call-site shape that lets
  `validate_projected_source_boundary` and `untranslated_source_findings`
  consult the full `compute_currency` projection. Implementation, assigned
  to a successor (Substrate) unit.
- Whether any of the fifteen sixth-refusal-fenced fact types — particularly
  the amount fact types — should become directly withdrawable, and by what
  mechanism. Assigned to the successor milestone that relocates capability
  limits, per the owner's 2026-09-06 disposition.
- Whether `by` naming the retracting act id is the right long-run
  attribution shape for an explanation consumer; no consumer reads it yet
  (findings §8 item 5).
- Whether the two-table applier split (`_ACT_SCOPED_APPLIERS`) is the right
  long-run substrate shape, and whether `apply_finding_retracted`'s
  `compute_currency` call on every retraction is affordable at realistic
  log length (findings §8 items 6–7). Substrate, not contract.
- Concurrency beyond the act log's existing `committed_against` check:
  two clients retracting different findings of the same fact, or a
  retraction racing a correction, were not modelled (findings §8 item 12).
- Whether the payload should ever carry a user-authored reason or note.
  The current schema deliberately excludes it and no consumer has asked for
  it yet (findings §8 item 13).

## Links

- Milestone:
  `docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md`,
  "## Owner disposition — 2026-09-06".
- Track 0 findings:
  `docs/prototypes/assertion-standing-retraction-semantics/track-0-findings.md`.
- Migration-path repair regressions:
  `tests/test_migration_retraction_repair.py`.
- Substrate compatibility record:
  `docs/prototypes/assertion-standing-retraction-semantics/substrate-unit-compatibility-matrix.md`.
- Committed payload example:
  `docs/prototypes/assertion-standing-retraction-semantics/act-finding-retracted.v1.example.json`.
- Schema: `packages/schemas/kernel/act-finding-retracted.v1.schema.json`.
- Kernel: `packages/kernel/currency.py` (`_finding_retractions`,
  `DECLARED_EDGE_KINDS`, `displacement_closure`, `compute_currency`),
  `packages/kernel/findings.py` (`_current_value_for_fact`,
  `_current_values_for_fact_type`, `retracted_finding_ids`,
  `retraction_acts`, the sixth refusal).
- Out-of-kernel readers named in Decision 5:
  `packages/tax/coverage.py::untranslated_source_findings`,
  `packages/tax/ssa_benefits.py::validate_projected_source_boundary`,
  called from `packages/derivation/live.py`; and the migration path
  (`_present_successor_claims`,
  `_refuse_unresolved_nonzero_noncurrent_predecessors`).
- Precedents: ADR-0041 (supersession-policy vocabulary and state-gated,
  never actor-checked, authority — reused unchanged for the retraction
  gate); ADR-0010 (derivation currency, `DECLARED_EDGE_KINDS`,
  displacement closure); ADR-0017 / ADR-0023 Decision 1 (family-member
  routing rule reused for retraction's Refusal 5); ADR-0063 (fourth named
  supersession root, migration supersession — the precedent for treating a
  new lifecycle event as a displacement root rather than a new edge kind).
