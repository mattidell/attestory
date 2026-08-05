# Retrospective: Covered Form 1099-B Wash-Sale Adjustments through Form 8949 and Schedule D Lines 1b/8b

- Phase: Engine Breadth
- Closed: 2026-08-05
- Plan: `docs/phases/engine-breadth/milestones/schedule-d-form8949-covered-wash-sale.md`

## Result

A 2025 individual return within the supported covered, basis-reported
capital-transaction class becomes computable when one or more Form 1099-B
transactions are routed to Form 8949 solely because the broker reported a
nondeductible wash-sale loss in box 1g (code W). Short-term transactions route
through Form 8949 Part I, box A, to Schedule D line 1b; long-term through Part
II, box D, to line 8b. Form 8949 columns (a)-(h), code W in column (f), and
row arithmetic `h = d − e + g` are production-shaped and independently
reviewed correct — including per-transaction validation guards for code W on
a gain and an adjustment exceeding the otherwise-deductible loss. Successor
Schedule D lines 1b/7/8b/15/16/21 and Form 1040 line 7a/9 recompute over the
new lines alongside the existing 1a/8a, box-2a, and carryover lines. The
blanket `no-form8949-sources` completeness declaration is not retired; a new
Path A/B gate and a fifth boundary declaration
(`no-other-form8949-adjustments`) admit exactly the supported code-W case.

## Accepted contract decisions

ADR-0061 (transaction authority, family topology, completeness successor) and
ADR-0062 (Form 8949 attachment, arithmetic, Schedule D 1b/8b composition)
were both settled by a paper-first Track 0 before any implementation charter,
mirroring the ADR-0059/ADR-0060 split from the predecessor milestone. All
seven Track 0 decision topics settled on paper against real committed source
and the 2025 Form 8949/Schedule D instructions; no implementation prototype
was warranted.

**ADR-0061 was amended once, pre-merge**, after independent review found a
real defect: both mechanisms Decision 1 originally named for the accompanying
box-1g amount (a `v3` successor of `covered-st-txn`, or the same `v2` identity
plus a field) turned out to be structurally unsafe. `source-family.v1`
membership is keyed by bare fact-type id only, with no value-filtering
capability — sharing the direct family's fact-type id, as both named
mechanisms required, would have made every direct-reporting assertion an
automatic member of both families at once, guaranteeing double-counting for
every transaction and directly contradicting Decision 2's own package-
exclusivity requirement. The amendment names the mechanism actually built (a
wholly separate `covered-w-st-txn`/`covered-w-lt-txn` fact type) and adds the
real enforcement this requires: a package-validation kill-test on identity-key
collision across the direct and wash-sale families. Because the milestone had
not yet merged, the ADR was edited in place by owner direction rather than
filed as a numbered amendment.

## Track 1: three repair rounds, three independent reviews

Track 1's first independent review returned **NOT READY** with four
findings:

1. **CRITICAL** — the validation guards (code W on a gain; adjustment
   exceeding the otherwise-deductible loss) were evaluated against a box's
   *aggregated* subtotal instead of each contributing transaction. This let
   an individually-invalid row net silently against a valid loss in the same
   box and publish a wrong Schedule D number instead of blocking — the
   reviewer demonstrated a concrete reproduction.
2. **HIGH** — the transaction-identity mechanism deviated from ADR-0061
   Decision 1's two named options (this became the ADR amendment above).
3. **HIGH** — the independently-blockable box-1g flag/amount guard was
   unimplemented, and five of the plan's twenty required fixtures were
   missing.
4. **LOW** — the line-1a/8a non-confusion invariant was verified only by an
   ad hoc string test rather than a structural package-validation kill-test.

A first repair round fixed Findings 1 and 4 outright, partially fixed Finding
3, and stopped on Finding 2 per its own charter's stop condition — correctly
escalating rather than improvising a third mechanism. After the ADR
amendment, a continuation repair implemented the identity-key collision
kill-test and the remaining fixtures.

**A second independent review** then found the collision kill-test correct in
isolation but never invoked in production: `resolve_production_package` — the
real hard-gate entrypoint — had no way to receive the asserted fact ids the
check needed, and was the wrong layer regardless, since it validates the
package/citizen graph once, independent of any specific run's facts. A third
repair round wired the check into `packages/derivation/runner.py` alongside
the already-existing per-transaction arithmetic guard, discovering along the
way that the runner's existing fact-id plumbing (`source_fids`) carried only
finding ids, not identity-bearing fact ids — fixed with an additive
`SourceFact.fact_id` field.

**A third independent review returned READY**, confirming the live-path check
genuinely blocks a real reproduction (not just a unit-test-level check), the
`fact_id` plumbing is additive and safe, and all three call sites are covered.

## Track 2: already substantially delivered

Track 2 (presentation, integrated regression) found that Track 1's own
repair rounds had already delivered the presentation and citation-walk
requirements: `packages/derivation/presentation_projection.py` builds its
model generically from whatever form-field/attachment citizens a resolved
package contains, so once Track 1 published its content, Form 8949 row
explanation and the Schedule D line 1b/8b citation walk followed
automatically with zero new production or presentation code. Track 2's
actual contribution was one presentation-model-level test making the
row/column citation walk explicit, plus fresh regression evidence run in the
same session (985 passed, 20 skipped full suite; 141 passed on a targeted
cross-milestone subset). Independent review verified the "already delivered"
claim was genuine — confirming the presentation-projection file was
byte-unmodified and genuinely generic, not a rationalization for skipped
work — and found no findings.

## Cross-milestone incident: a second package/schema version collision

Rebasing onto the separately merged Form 1099-DIV Box 12 milestone (PR #158,
merged first) revealed that both milestones had independently minted the
same next core-package version (`v17`) and registry version (`v12`), and
independently minted colliding schema successors — `quantity-vocabulary.v6`
for two different additive reasons, `artifact-package.v13` likewise. Unlike
the earlier Schedule B incident, this was caught **before** either PR merged,
via the same disposable dry-run semantic-ledger technique used in the
inbound-carryovers milestone, run proactively as an explicit owner
instruction before the real rebase. Resolved as a validated additive union:
`package.core-calculations.v18`, `published-packages.v13`,
`quantity-vocabulary.v7`, `artifact-package.v15` — keeping every already-
merged file (`v17`, `v12`, box-12's own `v6`/`v13`) byte-immutable. Zero
member/citizen id collisions existed; only the container package/registry/
schema version numbers and two content citizens' schema-string references
needed renumbering.

A worktree-registry incident also occurred mid-rebase: the git worktree this
session was operating in was unintentionally torn down and replaced by an
unrelated concurrent session's worktree for a different milestone, orphaning
this session's in-progress rebuild. Caught immediately (every git command in
the directory began failing), reported to the owner rather than silently
worked around, and recreated cleanly on the owner's confirmation — no work
was lost, since the branch's actual commits remained safe in the shared
object store and on `origin` throughout.

## What it cost

Three Track 1 repair rounds and three independent reviews (plus Track 2's own
review) — more review cycles than any prior milestone in this phase, driven
by a genuinely deep defect (the per-transaction vs. aggregate guard bug) and
a genuine substrate constraint (`source-family.v1`'s lack of value-filtered
membership) that neither Track 0 nor the first Builder pass caught. Both were
real, not process overhead: the arithmetic bug would have silently
misreported real returns, and the identity mechanism question was a correct
escalation, not a missed requirement.

## Follow-ups for the next plan

- **`source-family.v1`'s lack of value-filtered membership** is now a named,
  understood constraint (documented in ADR-0061's amended alternatives). A
  future milestone needing per-value family membership, rather than a
  separate-fact-type-plus-collision-check workaround, should consider whether
  a `source-family.v2` schema is warranted — deferred here as disproportionate
  to one bounded slice.
- **Per-transaction guard placement** is now a named pattern
  (`_f8949_row_guard_violations` and its sibling collision check in
  `runner.py`) worth citing directly if a future milestone needs another
  per-row validation guard, rather than rediscovering the aggregate-vs-
  per-transaction distinction from scratch.
