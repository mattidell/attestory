# Retrospective — Form 1099-DIV Box 7 Direct Foreign Tax Credit (No Form 1116)

## What differed from the plan

- Track 0 settled associated income as same-statement box-1a presence plus
  tax-year completeness (all foreign income and taxes in class on qualified
  Form 1099-DIV payee statements; all passive), without inferring foreign
  income amounts from box 7. Creditability is named component authorities plus
  a derived eligibility conclusion — not a bare `qualified` boolean. Box 8 is a
  required companion: non-empty country/possession or explicit RIC
  `not_applicable`; multi-country supplemental allocation stayed excluded.
- The residual successor records boxes **3 and 5 only**, extending the
  post-box-12 residual v3 shape. Package validation rejects mixed historical
  residual (still containing box 7) with the independent box-7 family.
  Historical residual and package routes remain byte-identical on the ratified
  predecessors.
- Regular tax for the cap remains Form 1040 line 16
  (`tax.us.2025.tax.total-tax`); new symbols carry Schedule 3 line 1, line 8,
  Form 1040 line 20, and tax-after-nonrefundable-credits. The foreign tax
  credit is counted once and never reduces dividend income.
- Threshold ($300 non-MFJ including MFS; $600 MFJ) **blocks** when exceeded; it
  is distinct from `min(box-7 subtotal, regular tax)`. Whole-dollar half-up
  rounding means the first over-threshold live fixtures use 301 / 601 rather
  than fractional cents.
- No new ADR was required. Accepted identity, family, horizon, package,
  citation, dividend, and presentation ADRs plus the plan contracts were
  sufficient.
- The in-branch independent review returned READY with no numbered findings,
  but that verdict was wrong: an owner-commissioned external review the same
  day found five real defects (below), and one findings-only repair cycle —
  the plan's allowed maximum — was required before a fresh independent review
  confirmed READY.
- Final base synchronization rebased onto `origin/main` after Form 8949
  (PR #161), Form 1099-INT box 8 (PR #164), and Form 1099-G (PR #166). Ephemeral
  semantic-ledger check against the ratified tip (core **v20** /
  `published-packages` **v15** / release max **v13** / `quantity-vocabulary`
  through **v9** / `artifact-package` through **v17**) renumbered this
  milestone’s additive successors to core **v21** (`artifact-package.v18`,
  admits `quantity-vocabulary.v10` and `dividend-universe.v4`), published
  **v16**, release **v14**, and adoption **v21**. No historical package,
  schema, registry, release, or adoption rows were rewritten; the 21 new
  member identities do not collide with main tip members.
- Multi-companion admission for box-7 → box-8 + box-1a required live/runner
  flattening of list-valued companion type maps. Schedule 3 form-field `line`
  labels are `Sch3-1` / `Sch3-8` so presentation section ids do not collide
  with Form 1040 line 8 (other income after 1099-G).
- Post-union package hygiene before publication: foreign-tax-paid member pin
  uses `quantity-vocabulary.v10` (matching the citizen), and entrypoints are
  tip-version-only with no stale wrong-version duplicates from intermediate
  union construction.

## Result

The engine has a bounded, production-shaped synthetic path for 2025 individual
returns that report foreign tax paid in Form 1099-DIV box 7, qualify for and
elect the direct foreign tax credit without filing Form 1116, and carry that
credit through Schedule 3 Part I line 1, Schedule 3 line 8, Form 1040 line 20,
and tax after nonrefundable credits. Associated box-1a (and optional box-1b)
dividend income remains on the existing line 3b/3a paths.

The result does not implement Form 1116 limitation arithmetic, foreign-tax
carryovers, Schedule A deduction of foreign tax, foreign taxes from Form
1099-INT or K-1/K-3, multi-country supplemental allocation, currency
conversion, AMT FTC, general Schedule 3 credits, or payments/refund/filing.

## Evidence and review disposition

- Paper boundary and contracts: `docs/phases/engine-breadth/milestones/form1099div-box7-direct-ftc.md`
  (Track 0 record and B7-C1–C10).
- **Correction (2026-08-05):** an owner-commissioned external review found the
  in-branch READY verdict was made in error. What that review had triaged as
  "non-blocking notes" — the MFS LOOKUP_MISS, the shallow presentation
  mutation, the test-only mypy cast — were the real defects, alongside a
  destructive/non-reproducible generator and incomplete B7-C10 lifecycle
  evidence.
- **Repair (2026-08-05):** one findings-only Builder repair cycle fixed all
  five findings: the generator now bases the registry on the real ratified
  predecessor and derives adoption revision/supersedes from the actual prior
  tip (and two further latent drift bugs the fix surfaced were also closed);
  the MFS claim was narrowed rather than backfilled with real bracket data —
  the milestone plan now states plainly that live MFS is not certified,
  pending a future tax-table milestone, and the test suite makes that gap
  visible instead of hiding it behind single-filer substitution; the
  presentation golden was confirmed stale (not a live-surface defect — the
  extra sections were legitimately-published companion entries from
  sibling milestones merged after the golden was captured) and regenerated,
  with both the positive and negative presentation tests now load-bearing
  against the real projector; the lifecycle test observes identity
  distinctness and exact pins across amount, election, and eligibility
  corrections; mypy is clean.
- **Fresh independent re-review (2026-08-05):** author-independent of the
  repair Builder, re-ran every load-bearing claim rather than accept the
  repair's self-report, and returned **READY** with all five findings
  confirmed fixed and nothing out-of-scope riding along. The foreman
  independently spot-checked mypy and the focused suite a third time before
  this closeout.
- The external review, the repair charter, and the repair re-review were
  working instruments of an in-flight correction; their material findings are
  distilled above and their files are removed at this closeout per
  `PROJECT_PLANNING.md`, "Milestone Publication Curation". The durable review
  evidence for the curated candidate is the final independent review at
  `docs/reviews/2026-08-05-form1099div-box7-direct-ftc-final-review.md`.
- Focused live, package, schema-registry, and regression suites passed
  (milestone suite 38; named regressions 287; full suite 1099 passed / 20
  skipped). Governance lint, envelope scan, and `git diff --check` clean on
  the working branch. The final curated PR head still requires the
  repository CI gate.

## What it cost

- One paper-first Track 0, one integrated Builder, one independent Reviewer,
  one external re-review, one findings-only repair Builder, one independent
  repair re-review. No rival prototype, no new ADR.
- Builder wall time was on the order of twenty minutes with a large tool-call
  count for a content-heavy package graph; independent review about seven
  minutes of wall time with focused suite rechecks; the repair cycle and its
  re-review added roughly sixteen minutes and eight minutes of agent wall
  time respectively. Exact agent-session metrics are operational and not
  product authority.

## Follow-ups

- Keep general Form 1116 foreign tax credit and Schedule A foreign-tax
  deduction as separate frontier candidates.
- Preserve append-only package, schema, registry, release, and adoption
  inventory. This closeout already applied the post-#161/#164/#166 additive
  renumber (v21/v16/v14/v21); further concurrent merges before this PR lands
  require another ledger check and union rebuild, never same-version
  different-byte overwrites.
- Optional fixture hygiene: deepen the named P8 wage path and N15 presentation
  mutation; fill MFS tax-bracket parameters when a later tax-table milestone
  owns that surface.
- Leave the next frontier row unselected until the owner chooses.

## Closeout lesson

Authority-heavy credit composition is controllable with paper-first component
declarations and explicit Schedule 3 completeness absences. Keep line-16
regular-tax meaning stable when introducing tax-after-credit symbols. Treat
shared package version numbers as unreserved until merge inventory and ledger
check against the ratified tip, especially when parallel milestones advance
the same successor slot.

A "READY, no findings" verdict is not self-verifying. The in-branch review
triaged a generator that rebuilt from a stale base, a crashing MFS claim, a
non-load-bearing golden, thin lifecycle evidence, and a red mypy gate all as
non-blocking notes; a second, independently-commissioned review treating the
same evidence as findings caught all five. Fixtures a generator can silently
regress need their own reproducibility test, not just a byte-identical
snapshot at authoring time. A test that substitutes an easier case for a
contract's stated claim (single-filer runs standing in for MFS) is a defect
in the test's honesty even when the substitution is commented — the fix is
to make the gap an explicit, visible assertion, not to hide it better.
