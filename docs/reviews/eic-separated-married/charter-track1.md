# Charter: Track 1 of the separated-spouse question is asked only of a married filer

Role: Builder. Source HEAD on milestone/eic-separated-married-2025.
Plan: docs/phases/engine-breadth/milestones/eic-separated-married.md (read
it whole; Decisions 1-7 bind; Decision 4 changes the P0b design for a
recorded separated-spouse "no"). Evidence: eic-separated-married-evidence/
p0.md, p0b.md and their scripts. Do not read governance.

## Scope

1. **Design.** From the P0b scratch successor: apply Decision 4 (a recorded
   separated-spouse "no" from a head of household with a qualifying child
   asks the new question; a recorded "yes" passes without it) and Decision
   5 (remove the inert path if validation allows; otherwise quote the
   validation that requires it). Tighten the question wording per Decision
   6, quoting Step 3 question 3 and Publication 596 Rule 3.
2. **Publish.** Core v103, registry v100 -> v101, release v101 from
   published v102. New files only; never edit a published file; loader v103
   entries carry v102's. Schema publication protocol in AGENTS.md for any
   manifest.
3. **Trace and hand credit.** The P0b cases plus: head of household with a
   qualifying child and a recorded separated-spouse "no" then married "no"
   (credit) and married "yes" ($0); married filing separately unchanged.
   Hand credit from the 2025 table for each.
4. **Replay.** Strict full-surface replay of the 775 recorded lists, v102
   against v103, expected changes declared; 0 unexpected; no recorded number
   changes; report newly blocked lists (expected none) and unused
   expectations.
5. **Tests.** Live coordinator tests for every traced case against the hand
   credit and the asked flags; a package test loading v103; mutants (scratch
   only) that fail a test: the new question asked of a married filing
   separately filer, skipped after a separated "no", or required after a
   separated "yes". Run `pytest -m "not live"` (it includes
   `tests/test_content_file_sizes.py` once #303 merges) and the two live
   size tests (`-k 5kb` in tests/test_earned_income_credit_track1.py and
   tests/test_eic_qualifying_children_track1.py), the touched live tests,
   and mypy.

## Deliverables

Content, package, registry, release, loader entries and tests; in
eic-separated-married-evidence/: track1.md (design as built, question
text with sources, files, replay, hand credits, sizes, tests). Fill a
"Track 1 result" section in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Do not edit packages/kernel/ or the engine; content, package, release and
  loader entries only. Stop and report if the route needs more.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
