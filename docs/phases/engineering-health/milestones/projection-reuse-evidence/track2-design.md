# Track 2 design — one projection per recording or review operation

Audience: Builder, reviewer.

Boundary: reuse lives inside one call. A function that has already
projected the exact acts it is about to project again passes that state (and,
where needed, its currency) to the helper instead. After a write, the new
state is derived by applying the written acts to the pre-write state the
function already folded, not by re-reading and re-projecting the log, only
where the written acts are exactly the staged ones and the revision matched.
Nothing is kept after the call returns. Public functions keep their
signatures and stay fresh when called on their own; every new state
parameter is named `_state` (leading underscore), optional, defaulting to
`None` (cold: fold fresh), and is passed only from the same call's own
projection. Historical-prefix reads are untouched.

Every site below is reused under one invariant: `ActLog` is append-only
(Article 9), so two reads at the same revision see byte-identical acts. A
function's own `_read_for_save` / `log.read()` already refuses a moved or torn
log before any reuse is attempted; reuse is only ever applied after that
refusal gate has already passed, so a reuse never admits something a fresh
fold would have refused.

## `packages/tax/f1099k_statement_recording.py`

### `_ensure_bundles`

**Reused.** The caller's own projection of `staged`, when the caller already
has one (a new `_state` parameter, optional, defaulting to `None`).

**Why it covers exactly the same acts and registry.** `_ensure_bundles` is
always called immediately after `staged` is built from `before.acts` (no acts
added yet), with the same `registry` the caller holds throughout. When
`_state` is given, it is exactly `project(staged, registry)` at that point,
by construction of every call site below.

**What still runs.** Every check in `_ensure_bundles` (`STATEMENT_BOX1A` /
`covers-only-single-item` fact-type presence) runs exactly as before, read
from the (possibly reused) state. If a bundle is missing, the function still
appends the bundle-adoption act and folds it onto the state with `apply_act`,
and now **returns** the advanced state instead of discarding it — a latent
gap in the circumstances-bundle branch (which built a `bundle-adoption` act
but never advanced its own local `state` with it, because the caller
re-projected afterward and masked the gap) is closed as part of returning a
state callers can trust. The five callers
(`record_f1099k_statement_durably`, `record_f1099k_no_statements_durably`,
`record_f1099k_statement_answers_durably`, `correct_f1099k_statement_answer_durably`,
`close_f1099k_family_durably`) each drop their immediately-following
`state = project(tuple(copy.deepcopy(row) for row in staged), registry)` and
use `_ensure_bundles`'s return value instead — the exact repeat P0 attributed
to this pair.

### `_commit`

**Reused.** The caller's own `state`, which by the time `_commit` is called
has been advanced act-by-act (via `apply_act` / `admission.state` from
`apply_contribution_batch`) through every act in `staged`, including the ones
just committed.

**Why it covers exactly the same acts and registry.** `additions =
staged[len(before.acts):]` is exactly what `log.append_batch` writes.
`staged[:len(before.acts)] == before.acts` by construction (staged starts as
a deep copy of `before.acts` and only ever grows). So the committed log's
acts equal `staged`'s acts, which `state` already folds. `append_batch`
either writes exactly `additions` and returns `expected_revision +
len(additions)`, or raises and writes nothing (a stale revision or a concurrent
writer is refused there, not here). The `revision == len(staged)` check in
`_commit` therefore always holds once the append returns; it is a defensive
assertion, not concurrency protection. The fallback to `log.read()` plus
`project(fresh.acts, registry)` remains for a caller that passes no state.
(Corrected after independent review.)

**What still runs.** `log.append_batch` is unchanged (still the sole write and
revision check). The seven call sites (`record_f1099k_statement_durably`,
`record_f1099k_no_statements_durably`, `record_f1099k_statement_answers_durably`,
`correct_f1099k_statement_answer_durably`, `withdraw_f1099k_statement_answer_durably`,
`retract_f1099k_statement_durably`, `close_f1099k_family_durably`) each pass
their own tracked `state` as `_state`.

### Cross-module reuse: `prepare_f1099k_statement_review` into the `*_durably` writers

**Reused.** The state `prepare_f1099k_statement_review` already folds from
`contents.acts`, carried through `f1099k_statement_review._revalidate` into
the recording call that follows in the same review-save operation.

**Why it covers exactly the same acts and registry.** Every review-wrapper
function (`save_f1099k_statement_review`, `correct_f1099k_statement_review_answer`,
`answer_f1099k_statement_review_question`, `withdraw_f1099k_statement_review_answers`,
`retract_f1099k_statement_review`) calls `_revalidate`, which re-runs
`prepare_f1099k_statement_review`'s own fold and refuses if anything about
the shown review has changed, then calls the matching `*_durably` function
with `expected_revision=current["revision"]`. The `*_durably` function's own
`_read_for_save` reads the log again and raises unless
`before.revision == expected_revision`; by the append-only invariant, passing
that check means `before.acts` is byte-identical to the acts
`_revalidate`/`prepare_f1099k_statement_review` already folded. `_revalidate`
now returns `(review, state)` instead of only `review`; a private
`_prepare_f1099k_statement_review_impl` does the real work and returns both,
and the public `prepare_f1099k_statement_review` keeps its one-return
signature and is unaffected when called on its own (no `_state` to receive,
nothing new to pass anywhere).

**What still runs.** Each `*_durably` function's own refusal checks
(`_read_for_save`, duplicate-evidence, current-finding, currency) run exactly
as before, now reading from the passed-in `_state` when given (through
`_ensure_bundles`'s own reuse above) instead of a fresh fold. The five
writers that a review wrapper calls
(`record_f1099k_statement_answers_durably`, `answer_f1099k_statement_answer_durably`
[a thin forwarder], `correct_f1099k_statement_answer_durably`,
`withdraw_f1099k_statement_answer_durably`, `retract_f1099k_statement_durably`)
gain an optional `_state` parameter, defaulting to `None` (cold, fresh fold —
their behavior when called directly, outside a review, is unchanged).
`record_f1099k_statement_durably`, `record_f1099k_no_statements_durably` and
`close_f1099k_family_durably` have no review counterpart that folds first, so
they keep only the `_ensure_bundles`/`_commit` reuse above.

## `packages/tax/sli_relationship_recording.py` — `_record_borrowing_answer_durably`

**Reused**, entirely inside this one function:

1. `_stage_relationship_v2_adoption`'s own fold is returned (new `_state`
   parameter mirroring `_ensure_bundles`'s fix above: the bundle-adoption
   branch now also advances its local `state` with `apply_act`, which it
   built but never applied to its own return before). The immediately
   following `_current(staged, registry)` call — a second full fold of the
   same `staged` — is replaced with a new `_current_from_state(state)` helper
   that factors `_current`'s non-project tail (`compute_currency`,
   `facts_of`, the current-findings filter) out of the fold, so `_current`
   itself is unchanged for its other three callers (`current_claim_applicability`,
   `_record_submission`, `_stage_answer`) and stays a correct, fresh,
   stand-alone fold when called on its own.
2. `base = project(tuple(copy.deepcopy(row) for row in (*staged, evidence_act)), registry)`
   folds `staged` plus one more act (`evidence_act`) that the function is
   about to append. Since `state` (from step 1) already equals
   `project(staged, registry)`, and `evidence_act`'s `committed_against ==
   len(staged)`, this is replaced with `apply_act(state, evidence_act,
   registry)` — the pure fold's own incremental step, not a second full
   re-fold.
3. The final `project(recovered.acts, registry)` (after `_commit_save`) is
   replaced with `admission.state` (already the fold through `evidence_act`,
   `contribution`, `assertion`), **guarded** by checking that `_commit_save`
   did not grow `staged` further. `_commit_save` calls
   `_stage_enrollment_follows_schooling`, which only stages retractions when a
   save changes a borrowing's *financing* links; a borrowing-answer save never
   asserts or retracts a financing finding, so the enrollment-follow check is
   provably a no-op on this path — but the guard is a live length check
   (`len(staged)` before and after `_commit_save`), not a one-time proof, so a
   future change to that interaction fails safe into the original
   `log.read()` / `project(recovered.acts, registry)` path instead of reusing
   a stale state.

**Why it covers exactly the same acts and registry.** `staged` is one list,
mutated and folded forward act-by-act within this one function call; no other
caller or process touches it. `registry` is the one parameter passed through
start to finish — nothing in this function calls `install_domain_*` or
otherwise swaps the registry mid-call.

**What still runs.** Every existing refusal (`correction_of_finding_id`
mismatch, duplicate evidence/submission identity, duplicate finding id,
`admission.terminal_record["phase"] != "completed"`) reads from the same
state values as before, just without the now-removed duplicate folds.

## `packages/tax/sli_relationship_review.py` — `borrowing_recognition_clues`

**Reused.** `_prepare_borrowing_answer_review_from_contents`'s own
`state = project(contents.acts, registry)`, passed as a new optional
`_state` parameter.

**Why it covers exactly the same acts and registry.** Both the function's
own top-level fold and every `borrowing_recognition_clues` call it triggers —
once per card, for that card's own clues, and (inside
`_require_card_distinguishable_in_workspace`, which already receives `state`)
once per other current same-label borrowing being compared against — read the
same `contents.acts` with the same `registry`, inside this one
`_prepare_borrowing_answer_review_from_contents` call.

**What still runs.** `borrowing_recognition_clues`'s own logic (the
current-finding scan, the lattice lookup, the label resolution) is unchanged;
it just reads from the passed state instead of folding again.
`recognition_clue_labels` (its public wrapper, used standalone — "safe to
call for every current choice before any review is prepared") gains the same
optional `_state`, defaulting to `None`, so its own direct callers are
unaffected. The one `borrowing_recognition_clues` call inside
`_require_card_distinguishable_in_workspace` that compares against *another*
current borrowing also receives the shared `_state` — it is the same acts,
only a different `borrowing_ref` filter — eliminating that repeat too, inside
the same named site.

## `packages/derivation/correction_session.py` — `_entity_label`

**Reused.** A state folded once per caller, inside the one function that
calls `_entity_label` (and, since it is the same loop, `recognition_clue_labels`)
more than once over the same acts.

**Why it covers exactly the same acts and registry.** Both call sites already
hold the exact acts they are folding — `contents.acts` — for their whole
duration:

- `_opened_loan_answers` already computes
  `state = project(tuple(dict(act) for act in contents.acts), registry)` at
  its top, before its per-answer loop that calls `_entity_label` and
  `recognition_clue_labels` once per current loan-cost/enrollment finding.
  That existing `state` is now passed through as `_state` to both.
- `CorrectionRuntime._working_state` has no such fold yet; it only has
  `contents`/`acts`. A `state = project(tuple(dict(act) for act in acts),
  registry)` is added once, in the same place and the same style
  `_entity_label`'s own cold fold already uses, immediately after
  `_scan_displayed_answers` is called (which is not itself touched — it is
  not a named site, and leaving it fresh keeps this change local to the two
  named helpers). The new `state` is then passed to every `_entity_label` and
  `recognition_clue_labels` call in both the `choices` loop and the
  `unavailable` loop that follow.

**What still runs.** `_entity_label`'s own lookup (`state.fact_state.entities.get(ref)`)
is unchanged; `recognition_clue_labels`/`borrowing_recognition_clues` run
unchanged logic over the shared state. `_scan_displayed_answers` and
`_attribute_borrowing_labels` (reached through `_line21_view`) are left
folding fresh — they are not named sites, and widening the change to them
would mean passing state across another function boundary outside this
track's named sites.

## Not touched, and why

- `findings.project` and `ActLog.append` / `append_batch` themselves: Track 1,
  not this track.
- `_scan_displayed_answers`, `_attribute_borrowing_labels`,
  `_borrowing_cards`, `_current` (as a function, for its other three
  callers), `_record_submission`, `_stage_answer`, `_commit_save`'s other
  callers in `sli_relationship_recording.py`
  (`record_submission_durably`, `withdraw_relationship_claim_durably`,
  `answer_relationship_claim_durably`, `correct_relationship_claim_durably`):
  not among this track's named sites, and each would need its own reuse proof
  (a different acts sequence, or a different caller contract). Left fresh.
- Any registry mutation path (`install_domain_*`): none of the touched
  functions call it between an earlier fold and a later reuse; if one ever
  does, the reused state would no longer cover "exactly the same ... registry"
  and must fold fresh instead.

## Regressions planned

1. **Differential equality**, per changed operation, against an independent
   fresh fold of the resulting log: after the operation, `log.read().acts`
   independently re-projected with `project` must equal the operation's own
   returned `state` (and, for f1099k, the returned `finding_ids` /
   `statement_keys` must resolve to the same current findings either way).
   This is the concrete form of "equal the current implementation's" here: a
   wrong reuse is exactly a state that disagrees with a fresh fold of what was
   actually written.
2. **Call-count observation**: wrap `findings.project` for the duration of one
   operation and assert the call count drops (and stays above zero — the
   first, necessarily cold, fold still happens), and that a public helper
   called alone (`prepare_f1099k_statement_review`, `recognition_clue_labels`)
   still folds fresh and returns correctly without any `_state`.
3. **No cross-call leak**: call the same private helper
   (`_ensure_bundles`, `borrowing_recognition_clues`, `_entity_label`) twice in
   a row against two different act sequences / registries with no `_state`,
   and confirm each call's result reflects only its own input, never the
   other call's.

## Measurement

Before: the design-note commit, using the existing P0 harness
(`temp/projection-reuse/measure_p0.py`) unchanged. After: the same harness,
same histories, run again once the build lands, in
`projection-reuse-evidence/track2-measurement.md`.
