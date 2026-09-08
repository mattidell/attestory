# Compatibility matrix — unifying current standing (ADR-0073 Decision 5)

Substrate unit of the Assertion Standing and Retraction Semantics milestone (ADR-0073 Decision 5).
Written and committed before the behaviour change lands (charter deliverable 2).

## What is being unified

Before this unit, two independent projections answered "does this finding /
fact currently stand":

1. **The full projection**, `packages/kernel/currency.py::compute_currency`.
   Walks five displacement-root kinds (correction, member withdrawal,
   migration supersession, entity supersession via `superseded_entity_ids`,
   and finding retraction) plus the declared derivation/individuation
   closure. This is what `apply_finding_retracted`'s own refusal 2 already
   consulted, and what every L11 kernel reader (read models, derivation
   input marshalling) already agreed with.
2. **A narrower rule**, `packages/kernel/findings.py::_current_value_for_fact`
   / `_current_values_for_fact_type`. Mirrored only correction (last-inserted
   finding for a fact id wins), member withdrawal, and retraction. It had
   **no notion of entity supersession or migration supersession at all**.
   Five kernel admission enforcers read through it:
   `_enforce_closed_on_attestation`, `_enforce_subset_invariants`,
   `_enforce_companion_presence`, `_enforce_companion_equalities`, and
   `_enforce_declaration_signal_contradictions`.

Two tax-layer readers carried their own, independent third and fourth
mirrors: `packages/tax/coverage.py::untranslated_source_findings` (its own
inline last-write-wins scan, excluding only `withdrawn_fact_ids`) and
`packages/tax/ssa_benefits.py::validate_projected_source_boundary` (last-
write-wins with **only** a withdrawn-fact-id parameter — no retraction
channel at all).

The repair makes `compute_currency`'s `CurrencyView.current_finding_ids`
the single source every one of these six call sites reads through, computed
once per admission and threaded to whichever enforcers need it. It is
threaded rather than cached deliberately: a cache across admissions would be
a third definition of current standing, which is what this unit exists to
remove.

## Method

For each of the five enforcers, the current-standing question they ask is
scoped to a **pair of fact ids that share every identity-key binding except
the fact-type id** (companion/subset/equality pairs), or, for the
declaration/signal enforcer alone, spans **every fact id of one fact type**
(`_current_values_for_fact_type`). This scoping bounds where entity
supersession or migration supersession could actually change a verdict:

- **Entity supersession** changes an enforcer's verdict only where the
  enforcer reads a fact id whose individuating entity was superseded
  *without* also being blocked from reading the paired/triggering fact id
  for the identical reason. For a same-suffix pair (subset invariants,
  companion presence, companion equalities, and the gate projection in
  `_enforce_closed_on_attestation`), the entity component of the suffix is
  necessarily identical between the two fact ids — `_validate_finding`
  already refuses any assertion against a fact whose entity is not current
  (`facts.facts_of(state.fact_state)` excludes non-current entities from the
  lattice), so a currently-touched fact's entity is always current, and so
  is its paired fact's identical entity component. **No verdict changes for
  the four same-suffix enforcers under committed content.**
  `_current_values_for_fact_type` has no such suffix constraint — it spans
  every fact id of a type — so a superseded-entity's stale finding could
  survive there. See Entry 1.
- **Migration supersession** changes a verdict only where a retired
  predecessor fact type participates in a declared subset, companion-
  presence, companion-equality, or declaration/signal relation with a type
  that is *not* also retired. The one migration artifact adopted in
  committed content, `tax.us.2025.scheduleb-accrued-interest.succession`,
  retires `tax.us.2025.scheduleb.adjustment.accrued-interest.amount`, which
  participates in **no** declared subset, companion-presence, companion-
  equality, or declaration/signal pair (verified against
  `packages/tax/loader.py`'s domain maps and the fact type's own bundle —
  it is a source-family member predicate only). **No verdict changes for
  any of the five enforcers under committed content.** See Entry 2.
- `_enforce_closed_on_attestation`'s `closed-on-attestation` supersession
  policy is used by **no production fact type** — only the demo `GATED`/
  `GATE` vocabulary in `tests/test_assertion_standing_track0.py`. Its
  entity- and migration-supersession exposure is therefore confined to the
  test corpus, not production content. See Entry 3.

## Matrix

| # | Reader | Committed-content reachable? | Verdict changes? | Correct? | Disposition |
|---|--------|------------------------------|-------------------|----------|-------------|
| 1 | `_enforce_declaration_signal_contradictions` via `_current_values_for_fact_type`, entity supersession | Yes (structurally — see below) | Would change from refuse→admit for the affected case, but **no committed test or content scenario exercises it today** | Yes — a displaced (superseded-entity) finding must not raise a live contradiction | Documented, not separately tested beyond the general L8/individuation regression already in the corpus (see "Regressions" below) |
| 2 | Any of the five enforcers, migration supersession | Structurally possible, **not reachable in committed content** (the one adopted migration's predecessor type is not a companion/subset/equality/signal participant) | No | N/A | No repair needed against committed content; the unification closes the gap for any future migration id that *does* declare such a pair |
| 3 | `_enforce_closed_on_attestation`, entity/migration supersession of the gate fact | Test-corpus only (`GATED`/`GATE`); no production fact type declares `closed-on-attestation` | No (gate fact id's own key values are always projected from the being-corrected fact's own keys, which must themselves be current for the assertion to reach this enforcer at all — see Method) | N/A | No repair needed; verified by reasoning plus existing L14 gate tests, which are unaffected |
| 4 | `packages/tax/ssa_benefits.py::validate_projected_source_boundary` | **Yes — this is the fail-open Track 0 measured.** A spouse-recipient SSA statement's married-filing-jointly authority, ended by *retraction* (not member withdrawal), was silently still read as authoritative. | Yes: production verdict changes from **accepts** (fail-open) to **refuses** (correct) for the exact scenario in `tests/test_assertion_standing_track0.py::TestL11MeasuredDisagreements::test_ssa_fail_open_is_closed` | Yes — unambiguously; this is the fail-open closure the milestone names as its headline deliverable | Repaired: signature changed (`withdrawn_fact_ids` parameter replaced by a required `current_finding_ids` parameter), one production call site (`packages/derivation/live.py`) updated |
| 5 | `packages/tax/coverage.py::untranslated_source_findings` | Yes — a retracted source-amount finding kept being reported as an untranslated current finding (`tests/test_assertion_standing_track0.py::TestL11MeasuredDisagreements::test_coverage_untranslated_source_findings_agrees`, formerly `..._disagrees`) | Yes: `[("demo-finding-src", 42)]` → `[]` after retraction | Yes — a retracted answer is not current under any other reader; reporting it as an "untranslated but current" finding was already wrong before entity/migration supersession entered the picture | Repaired: internal implementation switched from a hand-rolled last-write-wins+withdrawn scan to `compute_currency(state).current_finding_ids`; no required signature change (new `currency` parameter is optional) |
| 6 | The four same-suffix enforcers (`_enforce_subset_invariants`, `_enforce_companion_presence`, `_enforce_companion_equalities`), retraction | Already correct before this unit — the narrow rule already tracked `retracted_finding_ids` | No | — | Unchanged in effect; now reads through the unified path for consistency, not because the verdict differed |

## Findings, not silently-updated tests

Entries 1–3 are the "verdict changes and is not obviously more correct, so
it's a finding" category the charter asks for — except none of them
actually surfaces a verdict change against **committed** content or the
existing test corpus today. Entry 1 is a real structural gap this
unification closes (a stale, entity-superseded declaration/signal
witness could previously have wrongly blocked an unrelated, correct
assertion); it is reported here because no committed content exercises the
declared-relation + entity-supersession combination together, so there is
no pre-existing test whose expectation needed to change. If a future
domain content change pairs an entity-keyed signal/declaration fact type
with entity supersession in a way this reasoning did not anticipate, that
combination should be re-verified against this matrix rather than assumed
covered.

## Regressions run at the shared boundary

In addition to the two repaired-verdict tests (Entries 4 and 5), the full
existing corpus for entity succession (`test_L8_entity_retirement_still_
displaces_by_individuation`), migration supersession (`test_refusal_2_
migration_displaced_finding`), evidence withdrawal (`test_L12_*`), family
transitions (`test_L13_*`, `test_L9_*`), ordinary correction (`test_L1`–
`test_L4`), and the closure-gate policy (`test_L14_*`) all pass unchanged
against the unified path (see Test Report below) — they exercise the
narrow rule's existing agreement cases, which the unification preserves
exactly (same suffix-sharing argument as Entry 2/3 above: none of these
scenarios pair a touched fact with an entity- or migration-superseded
companion under committed content).

## Addendum — measured cost of unifying (recorded after the behaviour change)

The narrow rule's own per-lookup cost was already an unindexed O(n) linear
scan of `state.findings` per fact id, called up to twice per declared pair
per enforcer; the four same-suffix enforcers already made admission cost
grow quadratically with act-log length before this unit touched anything.
Unifying adds one `compute_currency` call per admission (shared across all
four enforcers for that one admission, and deliberately not cached across
admissions), which is itself a handful of additional O(n)
passes over `state.findings` plus the individuation lattice walk.

Measured on a synthetic act log shaped like the worst production case
(every admission touches a fact type at the head of a companion-presence,
subset-invariant, companion-equality, *and* declaration/signal pair, so
all four enforcers run on every admission — denser than real content,
where a given admission usually reaches at most one or two of these
relations), single-process, admitting via `apply_act` directly:

| findings | before (narrow rule) | after (unified) | ratio |
|---|---|---|---|
| 300  | 0.41s (1.37ms/admission)  | 0.64s (2.13ms/admission)  | 1.55x |
| 600  | 1.61s (2.68ms/admission)  | 2.56s (4.26ms/admission)  | 1.59x |
| 1200 | 6.49s (5.41ms/admission)  | 10.18s (8.49ms/admission) | 1.57x |
| 2400 | 26.31s (10.96ms/admission)| 40.80s (17.00ms/admission)| 1.55x |

Unifying costs a consistent ~1.55–1.6x constant-factor overhead at every
size measured; it does not change the asymptotic order (both are already
quadratic in act-log length, driven by the narrow rule's own unindexed
scan, which this unit did not change). No cache was added to absorb this:
a cache of current standing is exactly the third definition this unit
exists to remove. The one optimization applied is computing one
`CurrencyView` per admission and threading it to every enforcer that
admission runs (`_admission_view_if_declared`), rather than one fresh view
per enforcer per fact-id lookup, and paying nothing at all when a registry
declares no subset/companion/equality/signal relation at all.

The pre-existing quadratic growth (present before this unit, unrelated to
unifying) is the real scaling risk at higher act-log lengths, and its fix
is a different shape than anything in this unit's scope: an incrementally
maintained index from fact id to its latest finding id (so
`_current_value_for_fact`'s per-lookup scan becomes O(1) instead of O(n)),
carried on `FindingState` itself and updated by `apply_assertion`/
`apply_member_transition` at admission time rather than recomputed by
every reader. That is a wider change to the state representation than this
substrate unit's assigned paths and is named here as a follow-on, not
undertaken.
