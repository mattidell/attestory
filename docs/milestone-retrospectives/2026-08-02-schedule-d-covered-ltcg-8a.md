# Retrospective — Covered Long-Term Gains, Schedule D Line 8a

## What differed from the plan

- The milestone's contract evidence (P1-P3, ADR-0052/0053/0054) had
  already been established and Track 1 landed before this session; this
  retrospective covers Track 2 onward.
- Track 2's own builder self-identified a fidelity gap mid-charter — the
  `selected-preferential-base` guard's discriminator check risked leaking
  a spurious proceeds-family pin into the direct-producer branch — and
  resolved it before the single atomic commit, exactly per the charter's
  "one complete commit" discipline rather than checkpointing an invalid
  package graph.
- Two genuine architecture gaps surfaced organically, each exactly where
  its charter's own stop conditions anticipated one might: ADR-0036's
  completeness check is presence-only (built for Schedule B, where a
  `"no"` answer is never disqualifying), but Schedule D's seven boundary
  declarations are eligibility gates where a `"no"` is a real violation.
  Track 2's builder flagged it rather than working around it. Separately,
  Track 3's builder found that a blocked or not-required attachment
  rendered no signal at all on the presentation surface — a pre-existing
  gap in ADR-0036's generalized shape that Schedule B's own goldens never
  happened to exercise.
- Both gaps were resolved the same way: a Gate-1-scored paper-spike-plus-
  ADR-draft decision unit (ADR-0055, ADR-0056), owner-ratified with one
  amendment each time (ADR-0055 needed no amendment; ADR-0056's Decision 3
  was amended before ratification to specify that attachment blocked/
  not-required text and the known-code allowlist are renderer-owned
  declared constants, not new tax-content fields), then a separate
  implementation charter. Neither gap blocked forward progress on its own
  track; both were charter-stop findings reported honestly rather than
  improvised past.
- The Track 2/3 independent review (covering Track 2, the ADR-0055
  implementation, Track 3, and the ADR-0056 implementation in one combined
  range) returned `READY` on the first pass — no repair cycle. The
  reviewer's own harness run reported one Chrome-binary environment skip
  unrelated to the change; the Python and Node suites the change owns were
  fully green.
- The branch was subsequently curated into its final five-unit shape
  (Accept ADR-0055; implement Track 2; Accept ADR-0056; implement Track 3;
  close the milestone) before merge, folding the original working
  sequence's paper spikes, decision/implementation charters, temporary
  review record, a mypy-only fix, and an archive-relocation-then-removal
  cleanup into their durable homes. A fresh author-independent review and
  CI run measured the exact curated head before merge, since the original
  review had measured the pre-curation sequence.

## What it cost

- Five durable commits landed the full slice: Accept ADR-0055; the final
  Track 2 Schedule D production route (including the ADR-0055 value-check
  behavior); Accept ADR-0056; the final Track 3 presentation route
  (including the ADR-0056 attachment-visibility behavior); and the
  milestone closeout.
- Two ADRs (0055, 0056) were drafted, reviewed, and ratified within the
  same milestone that surfaced their triggering gaps — both narrow,
  additive, Tier 2, and resolved at the paper-spike rung rather than a
  full prototype round, per Gate 1's own economics (scores of 6 and 5,
  deliberately not escalated since the residual uncertainty in each case
  was "which of two already-known patterns to extend," not an unexplored
  mechanism).
- The final state: Schedule D line 8a/13/15/16, Form 1040 line 7a/9, and
  the Schedule D-bound QDCG line-16 path are synthetic complete, with
  honest completeness-value checking and honest attachment-disposition
  visibility on the presentation surface — not deferred as known gaps.

## Follow-ups

- Keep short-term transactions, capital losses/carryovers, Form 8949,
  noncovered securities, digital assets, other Schedule D sources, and
  QOF flow as separately selectable candidates (deferral ledger entries
  4-9). Reactivate each only through its own selected source and
  completeness boundary.
- ADR-0056's `attachments` presentation-model key and its renderer-owned
  constants pattern is now the template for any future citizen kind that
  is not a simple scalar field. Future attachment-bearing schedules
  inherit visibility for free by adopting the widened model; they do not
  need a new ADR for the same shape.
- ADR-0055's `check: "value"` widening on `attachment-rule.v4` is
  similarly reusable content-only by any future schedule with an
  eligibility-gating declared-absence fact.

## What should change in the next plan

- The "paper-spike-plus-ADR-draft decision unit, then a separate
  implementation charter" pattern worked cleanly twice in one milestone
  and is worth naming explicitly as the default response to a
  builder-flagged, Gate-1-scored architecture gap — faster than a full
  prototype round when the uncertainty is genuinely "which known pattern"
  rather than "what mechanism," and it kept both fixes narrow and
  additive rather than improvised inside an unrelated track's commit.
- Continue chartering the milestone's own required author-independent
  review per production track (or, as here, in one combined pass once all
  tracks in a range are landed) rather than treating foreman-run
  verification (test suites, golden diffs) as a substitute — the two are
  complementary, not interchangeable: the foreman pass catches regressions
  fast between units, the independent review is the actual gate.
- Leave the next frontier row unselected until the owner chooses the next
  bounded class.
- The owner curated this branch's working history into its final five-unit
  shape before merge rather than merging the raw development sequence.
  Consider folding that distillation into the builder/closeout discipline
  itself next time — a paper spike, its decision charter, and its
  implementation charter are working scaffolding for one accepted ADR and
  one implementation commit, not durable history — so the final review
  measures the same candidate that merges, rather than a review of the
  pre-curation sequence followed by a second curation-verification pass.
