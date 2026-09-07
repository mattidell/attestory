# Track 0 findings — assertion-standing lifecycle spike

Evidence rung: **executable spike, kernel only.** This is evidence for the
contract, not the substrate implementation. Everything below was executed;
nothing was argued. All identifiers, entities, and values are synthetic
(`demo.*` / `demo-*`); the only production content used is fact-type and
bundle declarations already committed to the repository.

Test file: `tests/test_assertion_standing_track0.py` (64 tests, 68 subtests),
covering checkpoints T0-A, T0-B and T0-C.
Kernel change under test: `packages/kernel/findings.py`,
`packages/kernel/currency.py`, and the new published payload schema
`packages/schemas/kernel/act-finding-retracted.v1.schema.json`.

Two boundaries are used, never a hand-built state:

- **revision layer** — `ActLog.append` against a real workspace directory and
  the published schema registry;
- **admission layer** — `findings.project` / `findings.apply_act`, folding
  each act through the same appliers production uses.

Out-of-kernel readers are called exactly as production calls them. Nothing
under `packages/derivation/`, `packages/tax/`, or `packages/content/` was
modified.

---

## 1. Executed evidence per case

| Case | Test | Boundary invoked |
| --- | --- | --- |
| Payload gate | `TestPayloadContract::test_committed_positive_instance_validates_against_the_published_schema` | `SchemaRegistry.validate` over the published manifest |
| Payload gate | `TestPayloadContract::test_payload_admits_nothing_but_a_finding_id` | `SchemaRegistry.validate` (rejects `fact_id`, `value`, `reason`, `replacement`, `actor`, `{}`, empty id) |
| Payload gate | `TestPayloadContract::test_committed_instance_drives_a_real_fold` | `findings.project`, fed the committed instance verbatim |
| Revision layer | `TestRevisionLayer::test_act_log_commits_a_real_retraction_act` | `ActLog.append` + `ActLog.read` + `findings.project` |
| L6 (revision) | `TestRevisionLayer::test_L6_act_log_refuses_a_stale_committed_against` | `ActLog.append` → `ActLogError` |
| L1 | `TestLifecycle::test_L1_assertion_is_current` | `findings.project` + `compute_currency` |
| L2 | `TestLifecycle::test_L2_correction_replaces_the_answer_and_keeps_the_fact` | `findings.project` + `compute_currency` |
| L3 | `TestLifecycle::test_L3_retraction_leaves_no_current_answer_and_no_opposite_claim` | `findings.project` + `compute_currency` + `_current_value_for_fact` + `_current_values_for_fact_type` |
| L3 | `TestLifecycle::test_L3_by_names_the_retracting_act` | `findings.project` + `compute_currency` |
| L4 | `TestLifecycle::test_L4_reassertion_is_a_new_finding_that_becomes_current` | `findings.project` + `compute_currency` |
| L4 | `TestLifecycle::test_L4_retracted_finding_carries_both_retraction_and_correction` | `compute_currency` reason tuple |
| L4 | `TestLifecycle::test_L4_history_retains_all_three_findings_in_order` | `findings.project` |
| L4 (negative) | `TestLifecycle::test_L4_revival_by_id_reuse_is_refused` | `findings.project` → existing duplicate-id check |
| L5 | `TestLifecycle::test_L5_an_independent_proposition_is_untouched` | `findings.project` + `compute_currency`, subtested at four points |
| L6 (admission) | `TestAdmissionRefusals::test_L6_refusal_2_corrected_away_finding_is_refused_at_admission` | `findings.project` → `FindingModelError` |
| Refusal 1 | `TestAdmissionRefusals::test_refusal_1_unknown_finding` | `findings.project` |
| Refusal 2 | `test_refusal_2_already_retracted_finding`, `test_refusal_2_entity_displaced_finding`, `test_refusal_2_migration_displaced_finding` | `findings.project`; messages name `retraction by`, `individuation by demo-pat`, `supersession by demo.track0.succession` |
| L14 / refusal 3 | `TestAdmissionRefusals::test_L14_refusal_3_locked_policy` (+ `test_L14_locked_correction_is_refused_on_the_same_predicate`) | `findings.project` |
| L14 / refusal 4 | `test_L14_refusal_4_closed_on_attestation_with_the_gate_true` (+ `..._permits_retraction_before_closure`, `..._permits_reassertion_after_retraction`) | `findings.project` |
| L13 / refusal 5 | `TestAdmissionRefusals::test_L13_refusal_5_family_member_fact` (+ `test_L13_member_transition_removal_of_the_same_fact_is_admitted`) | `findings.project` |
| L7 | `TestAuthorityIsAStateGate::test_L7_a_different_envelope_actor_may_retract_under_free`, `test_L7_the_actor_changes_nothing_about_the_outcome` | `findings.project` |
| Edge vocabulary | `TestEdgeVocabularyUnchanged::test_declared_edge_kinds_are_untouched`, `test_retraction_reason_kind_is_a_root_not_an_edge` | `currency.DECLARED_EDGE_KINDS`, `compute_currency` |
| L11 (agreement) | `TestL11ReaderAgreement::test_L11_all_kernel_readers_and_the_read_model_agree` | `compute_currency`, `_current_value_for_fact`, `_current_values_for_fact_type`, `read_models.build_read_model` (`current`, `history_by_fact`, `open_fact_ids`, `facts`) |
| L11 (agreement) | `TestL11ReaderAgreement::test_L11_marshal_run_context_stops_supplying_the_retracted_answer` | `derivation.marshal.marshal_run_context` |
| L11 (agreement) | `TestL11ReaderAgreement::test_L11_reassertion_restores_every_reader_together` | all of the above |
| L11 (disagreement) | `TestL11MeasuredDisagreements::test_coverage_untranslated_source_findings_disagrees` | `packages.tax.coverage.untranslated_source_findings` |
| L11 (disagreement) | `TestL11MeasuredDisagreements::test_ssa_validate_projected_source_boundary_disagrees` | `packages.tax.ssa_benefits.validate_projected_source_boundary`, called as `packages/derivation/live.py` calls it |
| L11 (scope) | `TestL11MeasuredDisagreements::test_measured_scope_of_the_source_amount_exposure` | `tax_registry()` + committed content scan |
| L10 / D4 | `TestL10DerivationDependency::test_L10_derived_finding_is_current_before_the_retraction`, `..._retraction_displaces_the_derived_finding`, `..._reassertion_produces_a_new_derived_id_and_no_revival`, `..._kernel_projection_ignores_derived_publication_acts` | `derivation.projection.workspace_currency` over `derivation.loader.workspace_registry`, with real `derived-publication` acts |
| L12 | `TestL12EvidenceStanding::test_L12_withdrawn_evidence_leaves_the_documentary_finding_current`, `test_L12_a_retraction_changes_no_evidence_currency` | `findings.project`, `compute_currency`, `build_read_model` |
| L8 | `TestL8L9Neighbors::test_L8_entity_retirement_still_displaces_by_individuation` | `findings.project` + `compute_currency` |
| L9 | `TestL8L9Neighbors::test_L9_an_unrelated_member_transition_is_unaffected` | `findings.project` + `compute_currency` + `horizon_state` |
| D6 | `TestD6AuthorizationFold::test_D6_resolved_status_is_identical_before_and_after`, `test_D6_the_fold_does_not_own_the_retraction_kind` | `derivation.authorization.project` / `.resolve` |
| Real content | `TestRealContentF1098Control::test_the_control_is_unfenced_by_all_five_refusals` | `tax_registry()`, `domain_companion_presence_pairs`, `domain_companion_equality_pairs` |
| Real content L1–L4 + L11 | `TestRealContentF1098Control::test_L1_L4_and_L11_on_real_content` | `tax_registry()` + `findings.project` + every L11 reader, subtested at four points |
| Real content | `test_real_content_history_and_composed_reasons_survive`, `test_no_real_content_invariant_reads_the_retracted_answer` | as above |
| Sixth refusal (T0-C) | `TestRetractionRespectsAdmissionInvariants::test_retracting_a_declared_companion_is_now_refused`, `test_the_wedge_is_unreachable`, `test_both_appliers_run_the_same_four_enforcers`, `test_an_admitted_retraction_always_lands_in_the_admissible_set` | `tax_registry()` + `findings.project` |
| Ordered paths (T0-C) | `TestOrderedRetractabilityOnRealContent` (7 tests, 47 subtests) | `tax_registry()` + `findings.project`, fixtures generated from committed content |
| Reachability (T0-C) | `TestNoAssertionReachableStateBecameUnreachable` (3 tests) | `findings.project`, `build_read_model`, source inspection |

### The two measured disagreements (measured, **not** repaired)

Both were predicted by the plan's P2 map. Both are real. They differ in
repair cost, which is the useful part of the measurement.

1. **`packages/tax/coverage.py::untranslated_source_findings`.** After a
   retraction it still reports the retracted answer as a current
   untranslated source finding (`("demo-finding-src", 42)`), while
   `compute_currency` returns an empty current set and
   `_current_value_for_fact` returns the no-value sentinel. It excludes
   `state.withdrawn_fact_ids` but has no notion of retraction. **It
   receives the whole `FindingState`, so the repair needs no signature
   change.**

2. **`packages/tax/ssa_benefits.py::validate_projected_source_boundary`.**
   Production calls it as
   `validate_projected_source_boundary(state.findings.values(), state.withdrawn_fact_ids)`
   (`packages/derivation/live.py:228`). **The signature has no channel for
   retraction at all**, so the repair requires changing the signature or
   the call site.

   **Re-measured after T0-C, because T0-C closed the path T0-B used.** The
   T0-B demonstration retracted SSA box 4 while box 5 stood; the sixth
   refusal now refuses that, so it no longer demonstrates anything, and
   the test asserts the refusal rather than quietly dropping the case. The
   disagreement survives through `tax.us.2025.filing-status`, which
   participates in no declared relation and is retractable directly.

   It also changed character, for the worse. The T0-B shape was
   fail-closed (production refused where agreement would accept). The
   surviving shape is **fail-open**: with an SSA statement whose recipient
   is `spouse`, retracting the married-filing-jointly filing-status answer
   leaves production **accepting** the statement while agreement with the
   projection would **refuse** it. Production reads a withdrawn
   filing-status authority as though it still stood.

**Reachability of disagreement 2, measured exactly.** Refusal 5 fences every
`source_amount` fact type that is also a source-family member predicate.
Of 39 `source_amount` fact types in the committed 2025 content, 32 are
fenced and 7 are not:

```
tax.us.2025.f1099int.box11-bond-premium
tax.us.2025.f1099r.ira-box2a-taxable-amount
tax.us.2025.interest.accrued-interest-migrated.presented-claim
tax.us.2025.interest.current-year-adjustment.pairing-scoped
tax.us.2025.ssa1099.box3-benefits-paid
tax.us.2025.ssa1099.box3-workers-comp
tax.us.2025.ssa1099.box4-repayment
```

SSA box 3 and box 4 are both in that set and both read by
`validate_projected_source_boundary`, so the disagreement is
production-reachable today, not merely theoretical. The set is asserted in
`test_measured_scope_of_the_source_amount_exposure` so that content changes
which widen it fail loudly.

### Agreements worth recording

- `marshal_run_context` needed **no** change: it selects from
  `currency.current_finding_ids`, so it inherited retraction awareness.
- `build_read_model` needed no change for the same reason, and
  `open_fact_ids` returns the retracted fact to the L0 "unanswered" shape —
  the right product meaning.
- D4 needed **no** change under `packages/derivation/` (a charter stop
  condition that did not fire).
- The authorization fold is invariant because ADR-0010 compose-over means it
  does not own the `finding-retracted` kind. The states compare equal.

### A nuance in the L10 wording

The charter asks for "a `retraction` root in its reasons" on the derived
finding. What is actually true, and what the test asserts, is that the
derived finding's own reason tuple is `[("derivation", <pinned finding>)]`
and the `retraction` reason lives on the **kernel** finding
(`[("retraction", <act id>)]`). This is structural, not retraction-specific:
`displacement_closure` always labels a dependent with the *edge* kind, so no
root kind — retraction, correction, withdrawal, or supersession — can ever
appear directly on a derived finding. The two compose:
`derived → F_250 → retraction → act id`. Both halves are asserted.

---

## 2. Adversarial closure artifact 1 — authority-lifecycle table

Covers the two facts the spike exercises plus the retraction act itself.

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `demo.report-owner-attribution\|report=…,owner=…` (synthetic forcing fact) | "What amount from this identified payer report does this user attribute to this named other person?" | One (report entity, owner entity) pair; **not** tax-year-only — the proposition is individuated by two entities, so entity lifecycle governs it, not the year key | The two entities existing and current; the fact type's declared `free` supersession | A later assertion for the same fact (correction); a `finding-retracted` act naming the current finding; supersession of either keyed entity (individuation); migration retirement of the fact type |
| `tax.us.2025.f1098.liable-and-paid\|payer=…,statement=…,tax-year=2025` (real content) | Taxpayer's declaration that they were liable for and paid the interest on this identified 1098 statement | One (payer, statement, tax-year) triple. It is a **taxpayer-authority declaration**, not a source amount, and it is not a family member — so no horizon and no closure claim participates in its lifecycle | The lender and statement entities; policy `free`; nothing else — it participates in no companion, subset, or equality pair (asserted in `test_the_control_is_unfenced_by_all_five_refusals`) | Correction; retraction; supersession of the payer or statement entity; migration retirement of `tax.us.2025.f1098.liable-and-paid` |
| `act-finding-retracted.v1` act (the new claim) | "The current support supplied by this one identified finding ends now." It supplies no value and asserts no opposite proposition | Exactly one finding id. Its scope is **narrower than the fact**: it does not bind future answers to that fact, which is what distinguishes it from member withdrawal | The named finding being current under the full projection at the moment of admission; the target fact's declared supersession policy; the target fact not currently being a family member | Nothing invalidates a recorded retraction — it is an immutable act. Its *effect* is superseded when a later assertion answers the same fact and becomes current; the retracted finding then carries both `retraction` and `correction` reasons |

Storage identity is deliberately not treated as authority scope anywhere
above: the `tax-year=2025` key on the f1098 fact does **not** make its
lifecycle tax-year-only, because the proposition is about an identified
statement whose entity can be superseded independently (evidenced by
`test_refusal_2_entity_displaced_finding` on the structurally identical
two-entity demo fact).

---

## 3. Adversarial closure artifact 2 — empty/nonempty authority matrix (family control only)

Scoped to the family control, per the charter. The family is the synthetic
`demo.w2` family whose member predicate is `demo.w2.box1`. "The feature" is
retraction; "the neighbor" is the family's closure/subtotal consumer.

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty (horizon genesis, no members) | Horizon exists; no member findings | Retraction inapplicable — there is no finding to name | Refusal 1, "cannot retract unknown finding". No fact-level state is created | Unchanged: closure and subtotal consumers see the same empty family they saw before |
| Closed empty, horizon absent | No horizon genesis | Any | Unchanged: retraction never reads or advances a horizon | Unchanged |
| Nonempty, member current | Member asserted via `member-transition`; horizon `demo-h1` | Retraction **inapplicable by design** | **Refusal 5** — `test_L13_refusal_5_family_member_fact`. Routed to `member-transition` removal, which is admitted on the same fact (`test_L13_member_transition_removal_of_the_same_fact_is_admitted`) | Unchanged, and this is the point: no horizon advances silently and no subtotal shrinks without a declared member transition |
| Nonempty, member withdrawn by `member-transition` | Fact in `withdrawn_fact_ids` | Retraction of the withdrawn member's finding | Refusal 2 — the finding is not current (`withdrawal` reason), so it is refused before refusal 5 is reached | Unchanged; the withdrawal already advanced the horizon, which is the declared route |

The explicit choice recorded here, rather than inherited from a convenient
guard: **a family member fact's answer is never retractable by the assertion
lifecycle.** The alternative (permit it) would leave a fact that is still a
member with no current answer — a state no closure or subtotal consumer was
written for. This is refusal 5, and it is the same routing rule as ADR-0023
Decision 1.

---

## 4. Adversarial closure artifact 3 — late-authority counterexample

The gate's canonical trace is `attest → close → compute → add member →
reclose → recompute`. This spike introduces no aggregate declaration, so the
charter's own substituted trace is used: **`assert → derive → retract →
reassert → re-derive`**. Executed in `TestL10DerivationDependency`.

| Transition | What becomes unusable, and why |
| --- | --- |
| `assert` (`demo-finding-attr-250` = 250) | Nothing. The prior answer `demo-finding-attr-450` was already displaced by correction; it stays in history and stays non-current. |
| `derive` (`demo-derived-001` pins the answer as `input`) | Nothing. The derived finding is current; the kernel projection does not see it at all (compose-over, `test_L10_kernel_projection_ignores_derived_publication_acts`). |
| `retract` | **`demo-finding-attr-250` becomes non-current** (root, reason `retraction`, `by` = the retracting act id). **`demo-derived-001` becomes non-current**, cascaded along the declared `derivation` edge. Every kernel and out-of-kernel current-standing reader that consults `compute_currency` stops supplying the value: `_current_value_for_fact`, `_current_values_for_fact_type`, `build_read_model`, `marshal_run_context`. **Two readers do not**, and that is the FAIL recorded in §1: `coverage.untranslated_source_findings` and `ssa_benefits.validate_projected_source_boundary` remain current after the authority they read has changed. Under this gate's rule that is a `FAIL`, not a limitation — the real-world proposition genuinely did change (there is no longer an answer), so the surviving currency is wrong, not merely stale. The Substrate unit owns the repair. |
| `reassert` (`demo-finding-attr-250-reasserted` = 250, a new id) | **`demo-finding-attr-250` gains a second displacement reason** (`correction` by the new finding, alongside `retraction`). Explanation consumers must tolerate composed reasons. **`demo-derived-001` is *not* revived** even though the reasserted value is byte-identical — it stays displaced. Reuse of the retracted finding's id is refused outright (`test_L4_revival_by_id_reuse_is_refused`). |
| `re-derive` (`demo-derived-002` pins the new finding) | A **fresh** derived id becomes current; `demo-derived-001` stays displaced. No historical result is revived. |

Verdict: the trace passes on every kernel and derivation surface, and
**fails on the two out-of-kernel tax readers**, exactly as the plan
predicted. That failure is this checkpoint's deliverable, not a defect
introduced by the spike.

**T0-C amendment to this trace.** The `retract` transition now has a
precondition it did not have in T0-B: the retraction is admitted only if the
resulting state satisfies every declared admission invariant (sixth
refusal). For the synthetic forcing fact used above, which participates in no
relation, the trace is unchanged. For a fact that *is* a companion, the trace
does not start at all — see §6b. The FAIL against the two tax readers stands
either way; only the path that demonstrates it on the SSA family changed, and
that re-measurement is recorded in §1.

---

## 5. Adversarial closure artifact 4 — claim reuse

**N-A.** This track reuses no claim. It publishes a new payload schema
(`act-finding-retracted.v1`) with its own committed positive instance, and
declares no fact type, no source family, no closure claim, and no
aggregate or absence declaration. The one thing it *could* have reused —
member withdrawal, which superficially produces a similar "no current
answer" output — was executed as a control by P2 and disqualified on
evidence, because it is keyed by fact id and monotonic: a withdrawn fact can
never be current again, so it is a different lifecycle, not the same claim
in different clothing. Retraction's root is the **finding**; withdrawal's
root is the **fact**. That distinction is asserted directly in
`test_L13_member_transition_removal_of_the_same_fact_is_admitted`, which
shows the two roots staying separate (`withdrawal` reason recorded,
`retracted_finding_ids` still empty).

---

## 6. Adversarial closure artifact 5 — neighboring-capability dependency diff

Return state in which the new feature has no activity: **no
`finding-retracted` act in the log.** In that state every row below is
byte-identical before and after this change, because
`retracted_finding_ids` is empty and `_finding_retractions` contributes no
roots. This was verified by the full suite (1795 passed, zero failures).

| Neighboring capability | Prerequisites **before** | Prerequisites **after** | New feature-specific prerequisite? |
| --- | --- | --- | --- |
| Source-family closure (ADR-0017) | Horizon genesis; member transitions; closure finding | Unchanged | **None.** Refusal 5 deliberately keeps retraction out of the family lifecycle, so no horizon can advance and no subtotal can shrink through this act. `test_L9_an_unrelated_member_transition_is_unaffected` |
| Entity succession (individuation) | Entity introduced and current; supersession act | Unchanged | **None.** The two roots stay separate and compose without interaction. `test_L8_entity_retirement_still_displaces_by_individuation` |
| Evidentiary standing | Evidence submitted; `evidence-replaced` for withdrawal | Unchanged | **None.** A retraction changes no evidence currency, and evidence withdrawal remains a non-root. `test_L12_a_retraction_changes_no_evidence_currency` |
| Migration supersession (ADR-0025 / 0072) | Migration artifact adoption; retired fact types | Unchanged | **None.** A migration-displaced finding is refused as a retraction target by refusal 2; the migration path itself is untouched. `test_refusal_2_migration_displaced_finding` |
| Standing authorization (ADR-0069) | Grant act; universe digest; subject/year keys | Unchanged | **None.** Compose-over: the fold does not own the kind, and the projected state compares equal. `TestD6AuthorizationFold` |
| Derivation currency (ADR-0010) | Derived-publication acts; dependency pins | Unchanged | **None.** The new root enters through the existing `kernel_currency.displaced_finding_ids` seam; `DECLARED_EDGE_KINDS` is untouched. `TestL10DerivationDependency`, `TestEdgeVocabularyUnchanged` |
| **Kernel admission invariants** (subset, companion presence, companion equality, declaration/signal) | Enforced on every assertion, against the fully-updated successor state | **Enforced identically on a retraction** (T0-C), against the prospective post-retraction state, by re-running the same four enforcer functions | **None.** T0-B recorded a new, unjustified prerequisite here: a retraction could leave a companion unanswered and wedge the statement. T0-C closed it as a sixth refusal, so this row now imposes nothing new on the neighbour — it restores the neighbour's own rule. The blast radius this row triggered is measured in §6b: no relation participant is retractable by any order, which is a real narrowing of the retraction feature and is reported there rather than absorbed here. |

---

## 6b. T0-C — the ordered-path question, answered by execution

Scope: every declared subset, companion-presence and companion-equality
relation on committed 2025 content. Eight relations, **24 distinct fact-type
participants**, exhaustiveness asserted in
`test_every_relation_participant_is_covered`. Fixtures are generated from
the committed content itself — identity keys, value domains and family
membership all read from `tax_registry()` — so a content change reshapes the
fixtures rather than silently invalidating a hand-written one. Every fixture
is proven admissible before any retraction is attempted
(`test_every_fixture_is_admissible_before_any_retraction`), so a "not
retractable" verdict is a property of the contract and not a broken setup.

### Set A — retractable directly

**Empty, among relation participants.** All 24 are fenced.

Outside the relations, ordinary facts remain retractable directly, and the
two `declaration/signal` declaration fact types are the ones this deliverable
touched:

- `tax.us.2025.capital-gain-distributions`
- `tax.us.2025.line2a-scope.no-f1099int-tax-exempt`
- (and, from T0-B, `tax.us.2025.f1098.liable-and-paid`,
  `tax.us.2025.filing-status`, and every other fact type in no relation)

The declaration/signal enforcer is **monotonically permissive** under
retraction: removing a value can only make the declaration absent, never make
it equal to the contradicting literal, so it never blocks a retraction.
Executed in `test_declaration_signal_declarations_are_retractable_directly`.

### Set B — retractable only after retracting a dependent first

**Empty.** No order of retractions reaches any participant.

The argument is prefix-closure: a retraction sequence is admitted only if its
first act is, and every length-1 retraction of every participant is refused
(`test_direct_retractability_of_every_participant`, 24 subtests), so no
longer order can begin. The empirical backstop executes all **42 ordered
pairs** of the richest relation (SSA-1099 box 5 plus six witnesses) and finds
none admitted (`test_no_order_of_retractions_reaches_any_participant`).

The full exhaustion is a committed artifact rather than a claim about
analysis:
`docs/prototypes/assertion-standing-retraction-semantics/probes/t0c-exhaustive-orderings.py`
executes **every ordering of every length** over that relation — 13,699
sequences, including all 5,040 full-length permutations — through the real
admission boundary, and finds **zero admitted**. It reuses the test module's
own fixture builder, so probe and test cannot drift.

The structural reason is that **every companion-presence subordinate and
every subset participant on real 2025 content is a source-family member
predicate**, so refusal 5 blocks retracting the very fact whose absence would
unblock its companion. There is no order because there is no admissible first
move.

### Set C — not retractable by any order of retractions

Nine fact types are fenced by refusal 5 (they are source-family member
predicates; this predates T0-C):

```
tax.us.2025.f1098e.box1-student-loan-interest
tax.us.2025.f1099div.box12-exempt-interest-dividends
tax.us.2025.f1099div.box1a-ordinary
tax.us.2025.f1099div.box1b-qualified
tax.us.2025.f1099div.box7-foreign-tax-paid
tax.us.2025.f1099g.box1-unemployment
tax.us.2025.f1099int.box8-tax-exempt-interest
tax.us.2025.f1099r.ira-box1-taxable-distribution
tax.us.2025.ssa1099.box5-net-benefits
```

**Fifteen fact types are fenced by the new sixth refusal specifically.** This
is the product-meaning result:

```
tax.us.2025.f1098e.box2-checked-authority
tax.us.2025.f1099div.box13-specified-pab-authority
tax.us.2025.f1099div.box8-country-companion
tax.us.2025.f1099g.box4-federal-withholding-authority
tax.us.2025.f1099int.box9-specified-pab-authority
tax.us.2025.f1099r.box2b-not-determined
tax.us.2025.f1099r.distribution-code
tax.us.2025.f1099r.ira-box2a-taxable-amount
tax.us.2025.f1099r.ira-sep-simple-checkbox
tax.us.2025.ssa1099.box3-benefits-paid
tax.us.2025.ssa1099.box4-repayment
tax.us.2025.ssa1099.box6-withholding
tax.us.2025.ssa1099.lump-sum-election
tax.us.2025.ssa1099.recipient
tax.us.2025.ssa1099.statement-kind
```

Stated exactly: **while its subordinate member fact stands, none of these
fifteen answers can be withdrawn, by any order of retractions.** They are
witnesses and companion amounts that the bounded class requires — box 3 and
box 4 of an SSA-1099, the 1099-R distribution code, the box-2 checkbox on a
1098-E — and the kernel's existing contract says a declared companion may not
be left unanswered.

### Two mitigations, both executed, neither of which dissolves the result

1. **Correction remains available for every one of the fifteen.** Only
   withdrawal-to-no-answer is blocked. A user who entered the wrong box-4
   repayment can still correct it, including to zero
   (`test_correction_remains_available_for_every_fenced_participant`).
2. **The declared member-transition route unblocks all of them.** Removing
   the subordinate member through `member-transition` — the same route
   refusal 5 names — makes every companion retractable immediately
   (`test_the_declared_member_transition_route_does_unblock_companions`).
   This is why set C is stated as "not retractable by any order of
   *retractions*" rather than "unreachable".

### The judgement call, flagged rather than made

The charter's stop condition asks whether set C contains a fact whose answer
a user would plainly expect to be able to withdraw. **This spike does not
decide that, and the contract unit should.** The honest reading of the
evidence, stated so it can be disagreed with:

- For the pure witnesses — `statement-kind`, `lump-sum-election`,
  `distribution-code`, `ira-sep-simple-checkbox`, `box2b-not-determined`,
  `box2-checked-authority` — withdrawal-with-the-statement-still-standing
  has no obvious user meaning. Correcting them is the natural operation and
  it remains available.
- For the **amounts** — `ssa1099.box3-benefits-paid`,
  `ssa1099.box4-repayment`, `ssa1099.box6-withholding`,
  `f1099r.ira-box2a-taxable-amount`, `f1099div.box8-country-companion` — a
  user might well say "I should never have entered box 4 at all." Today that
  user must either correct it to zero, which asserts a different proposition
  ("the repayment was zero") rather than withdrawing a claim, or remove the
  whole statement from the family. **That is a real product gap and it is
  named here rather than argued away.**

The contract was not widened to shrink set C, and no exception was
introduced. Consistency with the accepted contract cuts both ways, and this
is the direction in which it cuts against the feature.

---

## 7. Adversarial closure artifact 6 — integration surface

**N-A.** This track publishes no externally bound symbol. It publishes one
act payload schema, which no form field, attachment, package entrypoint, or
presentation join binds; it declares no rule, publishes no symbol, and
produces no derived finding. The spike's only externally visible surface is
the act kind itself, and the act log validates it against its own published
payload schema at read time (exercised in
`TestRevisionLayer::test_act_log_commits_a_real_retraction_act`). No
form-field-bound symbol exists, so no presentation-model probe is owed.

---

## 8. What this spike does **not** establish

Each item is falsifiable and names what would settle it. This is the part
most likely to be over-claimed, so it is deliberately long.

1. **That the admissible-state repair is free.** It is not; it has a
   product cost this spike measured but did not decide. T0-C closed the
   T0-B wedge: `apply_finding_retracted` now re-runs the same four
   enforcers `apply_assertion` runs, over the prospective post-retraction
   state, and refuses on violation (sixth refusal,
   `TestRetractionRespectsAdmissionInvariants`). The wedge is unreachable
   and an admitted retraction now always lands in the same admissible-state
   set an assertion can reach
   (`test_an_admitted_retraction_matches_never_having_answered`).

   **That "no assertion-reachable state became unreachable" claim (T0-C
   deliverable 4) rests on one canonical equivalence case** —
   `test_an_admitted_retraction_matches_never_having_answered`, which shows
   a single answered-then-retracted fact agrees with a never-answered one
   across every current-value reader — **plus a source-level confinement
   check** — `test_the_sixth_refusal_is_confined_to_the_retraction_applier`,
   which inspects `apply_assertion`'s source for the guard's absence. It is
   not a sweep over the admissible-state space. That is proportionate for a
   spike; the point of recording it is that the next person to touch
   `apply_finding_retracted` should know what was, and was not, measured.

   What that costs is §6b: **no participant of any declared subset,
   companion-presence, or companion-equality relation on committed 2025
   content is retractable, by any order of retractions.** Fifteen fact
   types are blocked by the new refusal specifically. That is a real
   narrowing of the feature, it is a product-meaning question rather than a
   bug, and this spike does **not** establish that it is the right answer —
   only that it is the answer consistent with the kernel's existing
   contract. **Falsified by:** the contract unit deciding that some of
   those fifteen answers must be withdrawable, which would require either a
   relation-aware exception or a different treatment of an absent companion.

2. **That the ordered-path Set B conclusion (§6b) is one enumeration and
   seven inferences, not eight enumerations.** Exhaustive enumeration was
   executed for exactly one of the eight declared relations — the richest,
   the SSA-1099 companion-presence relation, 13,699 orderings of every
   length, zero admitted — and the other seven relations rest on the
   prefix-closure argument from the 24 length-1 refusals
   (`test_direct_retractability_of_every_participant`), not on their own
   enumeration. The argument is sound if the prefix-closure premise holds,
   but it is an argument, not a count. **Falsified by:** enumerating the
   remaining seven relations directly, or a single admitted length-1
   retraction of any relation participant, which would break the
   prefix-closure premise outright.

3. **That every current-standing reader agrees.** Two do not, measured in
   §1. Only the kernel readers, `build_read_model`, and
   `marshal_run_context` were proven to agree.

4. **That the entity-displaced and migration-displaced disagreements are
   fixed.** They are not. T0-A made `_current_value_for_fact`
   retraction-aware only; it still returns entity-displaced and
   migration-displaced values, exactly as P2 observations O3 and O5
   recorded. The charter assigned the shared resolution to the Substrate
   unit and this spike did not attempt it.

   **Review input, carried forward as an argument rather than a
   measurement:** the independent review sharpened this into a reason to
   prefer unifying admission on the full `compute_currency` projection over
   patching each current-value reader individually — doing so would also
   remove the reason `_current_value_for_fact` needed a retraction-specific
   patch at all, since it would then read the same projection every other
   agreeing reader already reads. This spike did not test that unification;
   it records the argument so the Substrate unit inherits it along with the
   defect.

5. **That `by` naming the act id is the right long-run choice.** It is
   defensible (a retraction creates no citizen; a fact can be retracted more
   than once, so the fact id does not discriminate) and it is the
   attribution path, but no consumer reads it yet. **Falsified by:** the
   first explanation consumer that must render a retraction reason and finds
   an act id unresolvable without an act-log lookup it cannot perform.

6. **That the two-table applier split is the right substrate shape.**
   `_ACT_SCOPED_APPLIERS` exists solely because a retraction reason must
   name the act. A uniform act-scoped applier signature may be better. This
   spike chose the minimal change and did not evaluate the alternative.

7. **That admission reading the full projection is affordable.**
   `apply_finding_retracted` calls `compute_currency` on every retraction,
   which walks the whole displacement closure. At spike scale this is
   invisible. No projection-cost measurement was taken at realistic log
   length, and the function-local import that avoids the
   `findings` ↔ `currency` cycle is a smell the Substrate unit should
   resolve properly.

8. **That reason-tuple order is meaningful.** It is contributor order
   (corrections, withdrawals, migrations, retractions, closure), not event
   order. Nothing in a `DisplacementReason` carries event time. The charter's
   phrasing ("`retraction` then `correction`") describes the events, not the
   tuple; the tuple is `("correction", "retraction")`. Asserted as-is so a
   later decision to make reason order chronological fails loudly.

9. **That `locked` retraction should be refused.** It is refused, following
   contract question 2's reasoning that `already_answered` reads history and
   would otherwise leave a permanently unanswerable fact. That is a *policy*
   conclusion inherited from the correction path, not something the spike
   proved to be the right product behavior. A `locked` fact whose single
   answer is wrong now has no remedy at all.

10. **That the real-content control generalizes.**
   `tax.us.2025.f1098.liable-and-paid` was chosen precisely because none of
   the five refusals fences it. It is a taxpayer-authority declaration
   participating in no companion, subset, or equality relation. It proves
   the lifecycle works on real content; it proves nothing about the 32
   fenced `source_amount` member fact types, and item 1 shows the
   unfenced-but-related ones are where the damage is.

11. **That any live run was exercised.** No test here drives
    `live_coordinate_run`, the production resolver, a rule evaluation, or a
    presentation projection. `marshal_run_context` was called directly with
    an empty rule list. The spike stops at the marshalling boundary.

12. **That concurrency was addressed.** Only the act log's existing
    `committed_against` check was exercised (L6, revision layer). Two clients
    retracting different findings of the same fact, or a retraction racing a
    correction beyond that single check, were not modelled.

13. **That the schema is right rather than merely sufficient.**
    `{"finding_id"}` admits and refuses correctly for every case tried, but
    no consumer has yet asked it for anything — for instance a reason or
    note field for the user's own explanation of *why* they retracted, which
    the product may well want and which this payload deliberately excludes.
