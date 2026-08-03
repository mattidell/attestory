# Retrospective — Schedule B Interest Adjustments

## What differed from the plan

- The paper checkpoint held the selected boundary: nominee distributions,
  accrued interest paid to a bond seller, and taxable amortizable bond-premium
  adjustments remained three independent authority and closure classes, while
  the downstream reduction reused the existing `subtract` vocabulary.
- Rebasing onto `origin/main` exposed published-version collisions. The final
  candidate preserved the existing histories and used attachment-rule.v6,
  artifact-package.v12, package v15, published registry v10, release v8, and
  adoption v15. The older package v10/registry v5 route remains the compatibility
  baseline.
- The Track 1A package-admission gap required the owner-authorized bounded
  successor repair before Track 1B could begin. No new evaluator operation or
  Schedule D dependency was introduced.
- The integrated review measured all contract and boundary areas as passing.
  Its only finding was an extra blank line at EOF in the immutable v6 schema,
  which the Foreman classified as a non-blocking formatting defect. The direct
  edit proposed by the review was deferred because it would mutate published
  schema bytes; a formatting-only schema successor was out of scope.
- Rebase curation exposed a package-history collision with the ratified line.
  The candidate was repaired additively: ratified package v14 and published
  registry v9 were restored byte-for-byte, while the Schedule B package v15
  and registry v10 successors remained intact. An independent re-review
  returned READY after the restoration.
- Post-close CI found two missing return annotations in attachment-rule test
  helpers. The type-only repair changed no product behavior, and the focused
  attachment tests and mypy check passed afterward.

## Result

The bounded synthetic class now computes through the existing positive-interest
universe, Form 1040 line 2b, Schedule B Part I, explanation, package/release
resolution, and the canonical production-shaped presentation golden. The
three adjustment classes remain independent of Schedule D, transaction/basis
machinery, and taxpayer-side investment calculations.

The integrated review reported focused contract tests passing, governance lint
conformant, and the envelope scan clean. The known diff-check warning is
retained as the deferred formatting finding rather than repaired by mutating
immutable history.

The final package-history re-review returned **READY** after confirming the
ratified package files were restored byte-for-byte and the Schedule B successor
graph remained additive and resolvable. The post-CI exact-range final review
also returned **READY** after the isolated test-helper type repair. No new
contract, scope, data-safety, publication, or closeout defect was found.

## What it cost

- The implementation used one sequential schema gate, one integrated Builder,
  and one independent integrated Reviewer, with one bounded Track 1A repair
  cycle before the Track 1B build.
- The review record reports 37 focused tests and the applicable static and
  safety checks. Builder-specific tool-call, wall-time, and authored-versus-
  generated volume measurements were not separately recorded, so they are not
  inferred here.
- The branch was rebased onto the current `origin/main` before the final
  successor versions were selected. No personal or real tax data entered the
  branch, fixtures, review, or output.

## Follow-ups

- Keep Schedule D, transaction/basis machinery, other adjustment classes,
  taxpayer-side accrual, tax-exempt premium, frozen-deposit reductions, and
  unrelated income as separate frontier candidates.
- Preserve the selected-version inventory and append-only schema publication
  checks when the next breadth slice is planned.
- Treat the extra EOF blank line as a publication-authoring hygiene lesson for
  future new schemas; do not revise attachment-rule.v6 or create a successor
  solely to change formatting.
- Leave the next frontier row unselected until the owner chooses the next
  bounded class.

## What should change in the next plan

- Keep the one integrated Builder/Reviewer shape when paper and mechanism reuse
  remain settled, with the schema gate sequenced before the content build.
- Make the final curated-candidate review distinct from the implementation
  review, after working records are removed and the closeout state is visible.
- Keep one canonical positive presentation golden and use compact in-memory
  mutations for malformed negative evidence.
- Record builder and reviewer economy measurements at handoff so the next
  retrospective can report them without inference.
