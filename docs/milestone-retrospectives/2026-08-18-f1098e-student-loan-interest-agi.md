# Retrospective — 2025 Form 1098-E Student-Loan Interest through Schedule 1 Lines 21/26 and AGI

## What differed from the plan

- The plan's own exit criteria named "independent review READY on the
  curated branch range" as a closing condition. That review was not
  performed before this closeout was first drafted: every track was built
  by a dispatched Sonnet builder and reviewed personally by the foreman
  (diffs read by hand, arithmetic and citations verified, tests run
  directly), but no separate reviewing party or owner-advisor pass had
  covered the branch as a whole. The gap was recorded rather than silently
  treated as satisfied — and an independent review was performed after
  this closeout was drafted, against the curated object at `64c540ce`. It
  returned `CHANGES REQUESTED` on two defects, both introduced by the
  curation itself, both fixed at `29971813`, gate re-verified green. See
  "Independent review findings" below.
- Track 6 (`aa190909` in the pre-rebase history) surfaced a real
  order-dependence defect in `marshal.py`'s unkeyed-symbol binding: two
  statements disagreeing on a per-statement universal eligibility witness
  could publish a deduction or block the whole route depending only on
  which finding's id sorted first. The foreman stopped rather than
  disposition it alone. The owner independently re-verified the finding,
  corrected two of the foreman's own claims about it, and issued a precise,
  itemized repair charter (content fix via a new `collect_categorical_all_equal`
  op, a substrate guard in both `marshal.py` binding loops, explicit
  no-new-ADR direction) executed as Track 6b under standing authority.
- Track 7 needed one repair round (of two authorized) to add the
  Consequences/Alternatives-considered/Links sections the ADR-0063 template
  requires; the repair was verified byte-identical against the original
  Context/Decision content before being accepted.
- The branch was cut from `origin/main` at `85b6a0f1` and built through all
  eight tracks before the concurrent `declarative-validation-substrate-f8949`
  milestone (PR #174) merged. Bringing the branch current required a
  rebase-and-rebuild, not a mechanical rebase: the package this milestone
  built (`package.core-calculations` v32) collided ADD/ADD with the exact
  same version number the concurrent milestone had independently claimed
  and shipped, with different content. Schema versions themselves were not
  in collision (rule-artifact.v6/artifact-package.v25/derivation-record.v7
  vs. the other milestone's rule-artifact.v5/artifact-package.v24/
  source-family.v2) — the ledger worked. The package instance did collide
  and was resolved by rebuilding on top of the concurrent milestone's
  ratified package as v33/v28/v26, not by renumbering schemas.
- `artifact-package.v25` had been authored as v23's own additive successor
  (correct against the state of `main` when Track 6 built it), which meant
  it silently dropped the concurrent milestone's own v24 admissions
  (`attachment-rule.v8`, `source-family.v2`, `rule-artifact.v5`) once
  rebased onto real `main`. Regenerated as v24's true additive successor.
- The rebase-and-rebuild's own version-allowlist audit found and fixed 8
  stale sites across `live.py`/`marshal.py`/`package_validation.py`/
  `runner.py` — including one, `runner.py`'s disposition `record_codes`
  closed set, that is not a pre-existing "site missed by this milestone" at
  all: it is a new mechanism the concurrent milestone introduced, and this
  milestone's three SLI block codes had never been registered in it because
  it did not exist when Track 6 was originally built. A schema-valid,
  correctly-produced block code was silently downgraded to generic
  `DEPENDENCY_INVALID` before ever reaching the derivation record.
- After the branch was rebuilt and pushed once as a merge-based rebase, the
  owner asked for a true rebase instead, then for genuine per-commit
  bisectability on top of that — the branch was rebuilt twice more. The
  first rebuild used a tree-hash-matching construction (each curated
  commit's files sourced from a known-good final tree); the second replayed
  every original commit individually onto `origin/main` and resolved each
  conflict where it actually occurred. The second pass caught three defects
  the first had papered over: a stale package-registry checksum for
  `rule.sli-worksheet.json` (Track 6b edits the citizen in place without
  bumping its version, so the registry's checksum needs regenerating at
  that exact commit or the resolver refuses it with
  `MEMBER_ABSENT_OR_MISMATCH`); Track 8 goldens built against a package
  version that no longer existed once replayed onto the rebuilt base; and a
  git rename-detection collision that briefly staged the deletion of
  `origin/main`'s own real, unrelated `artifact-package.v24.schema.json`
  (caught via `git status` before committing, not after).

## What it cost

- Eight tracks, each foreman-reviewed individually: diffs read by hand,
  arithmetic and citations independently verified, tests run directly by
  the foreman rather than trusted from a builder's report.
- Two same-milestone repairs under standing authority: Track 4b (an
  itemization-cap ordering bug — filers with over $2,500 in interest got a
  false Schedule 1 attachment block) and Track 6b (the marshal.py
  order-dependence defect, owner-dispositioned).
- One additional repair round for Track 7 (of two authorized under the
  owner's explicit cap for that dispatch).
- Two incidental substrate-bug fixes found during ordinary review, unrelated
  to Form 1098-E content: `tools/build_orientation_block.py`'s
  `current_prompt` anchor being silently ignored past `max_bytes`, and a
  duplicate-heading defect in this plan's own document causing the
  orientation tool's first-match-wins section resolution to return the
  wrong content for every T0-N deep-read anchor.
- One rebase-and-rebuild onto the concurrent `declarative-validation-substrate-f8949`
  milestone, performed three times at increasing rigor (merge-based, then a
  true linear rebase, then a genuinely bisectable one) at the owner's
  explicit direction each time.
- Final package is the additive union core **v33** / published **v28** /
  release **v26** / adopt **v33**, over the merged `declarative-validation-substrate-f8949`
  base (core v32/published v27/release v25).
- Zero new production ADRs beyond the two this milestone's own Track 7
  drafted (ADR-0064 expression-language extension, ADR-0065 Schedule 1 Part
  II completeness and line-26 composition), both accepted.

## Independent review findings

An independent review of PR #178 at the curated object `64c540ce` (base
`origin/main` `e49c8c04`, fully absorbed; prior reviewed object `bf142585`,
the pre-curation rebase-and-rebuild tip) returned `CHANGES REQUESTED` on two
defects, both introduced by the bisectable-rebase curation itself and
present in neither `bf142585` nor this retrospective/deferral ledger's
first draft:

- **`runner.py`'s `run_and_record` function had its own separate `use_v2`
  computation, missing `rule-artifact.v6`, while `_Run.__init__`'s
  equivalent computation had it.** This is the exact two-site divergence
  the original rebase-and-rebuild had closed; the curation reopened it at
  one of the two sites. Latent and test-invisible only because f1098e's
  real package also trips `_uses_attachment_machinery`, forcing both paths
  to `True` regardless. Fixed at `29971813` to match `_Run.__init__` exactly.
- **Three code comments describing `rule-artifact.v6`'s capability had been
  silently narrowed to "multiply/divide only"** during the same curation
  pass (`marshal.py` and `package_validation.py`, two sites), dropping
  `collect_categorical_all_equal` — contradicted by the accepted ADR-0064,
  this milestone's own deferral ledger, and the shipped
  `rule.sli-worksheet.json` content that uses the op at five sites. Fixed
  in the same commit.

Both defects are instances of the P1 capability-allowlist problem named
below, and the `runner.py` one is the first instance in this corpus's
history where the mechanism was re-broken after being fixed, rather than
missed on first build — a sharper argument for building the consolidation
than any of the prior three instances alone.

Gate re-verified green after the fix: 1488 passed, 20 skipped, `mypy`
clean, `governance_lint` conformant, `envelope_scan` clean.

## Follow-ups

- **P1 — carried forward, now confirmed a fifth time, and for the first
  time re-broken after being fixed rather than missed on first build.** The
  hand-maintained rule-artifact/attachment-rule capability allowlist
  problem named in `milestones/rule-artifact-capability-table-consolidation.md`
  recurred twice more in this milestone alone: 8 sites across `live.py`,
  `marshal.py`, `package_validation.py`, and `runner.py` needed independent
  fixes during the rebase to admit `rule-artifact.v6`, plus one
  new-mechanism site (`runner.py`'s `record_codes` closed set); then the
  curation pass that followed re-broke one of those same sites, caught only
  by independent review, not by the suite. Still scoped, not built.
  Trigger: owner selects it as its own milestone.
- **Curation that rewrites history should be provably tree-identical
  outside process/documentation paths, or it needs its own review.** The
  bisectable-rebase curation was not purely a reorganization: it carried
  engine edits to `marshal.py`/`package_validation.py`/`runner.py` that
  were not in the object the earlier review covered, and the result was a
  net regression neither the retrospective nor the deferral ledger
  recorded until this review caught it. A future history-rewrite pass over
  an already-reviewed object should diff engine paths against the prior
  reviewed tip and either show zero diff or flag the diff for its own
  review, rather than relying on the full suite to catch it (it didn't).
- **`no-rrb-or-foreign-social-benefit` succession** — the fourteenth
  migration candidate named by the SSA no-activity and fact-type-succession
  prerequisites — remains deferred; this milestone did not touch it.
- Schedule 1 Part II lines 11/12/13/14/15/16/17/18/19/20/23/25 (educator
  expenses, business expenses, HSA, moving, deductible SE tax, SE
  retirement, SE health insurance, penalty on early withdrawal, alimony
  paid, IRA deduction, Archer MSA, other adjustments) have no producer.
  Any return that genuinely has one of those adjustments correctly blocks
  with `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` rather than silently
  underweighting MAGI; building any of those producers is out of scope
  here and remains a distinct candidate.

## What should change in the next plan

- **A rebase across a concurrent milestone's own version claims needs a
  version-allowlist audit as a standing step, not an incident response.**
  This is the fourth milestone in a row to independently rediscover the
  same hand-maintained-allowlist defect class from a different angle. The
  scoped consolidation plan exists; it has not yet been selected.
- **When two milestones both build a new package version from the same
  base, resolving the ADD/ADD collision by rebuilding on top of whichever
  side merged first is right, but the losing side's own schema
  successor (here, `artifact-package.v25`) must be re-derived from the
  winning side's actual content, not renamed in place.** A rename-only fix
  silently drops whatever the winning side itself contributed.
- **Tree-hash equality to a known-good target is necessary but not
  sufficient evidence that a reconstructed commit sequence is bisectable.**
  It proves the final state is right; it says nothing about any
  intermediate commit. The three defects the second rebuild pass caught
  (stale registry checksum, stale goldens, a rename-detection near-miss)
  were all invisible to the first pass's tree-hash check specifically
  because they lived in intermediate commits the check never inspected.
  Spot-running the full suite at several intermediate commits — not just
  the tip — is what actually caught them.
