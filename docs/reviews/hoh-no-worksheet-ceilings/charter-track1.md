# Charter: Track 1 of a refused head of household status does not set the worksheet ceilings

Role: Builder. Source HEAD on milestone/hoh-no-worksheet-ceilings-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md
(read it whole; Decisions 1-4 bind). Evidence:
hoh-no-worksheet-ceilings-evidence/p0.md and its scripts. Do not read
governance.

## Scope

1. **Publish.** Core v104, registry v102, release v102 from published v103
   with the two P0 successors. New files only; never edit a published file;
   loader v104 entries carry v103's. Schema publication protocol in
   AGENTS.md for any manifest.
2. **Size guard.** Add the two successor files to
   `tests/test_content_file_sizes.py` at the worksheet cap, keeping the
   guard's exact-name-set check.
3. **Trace and replay.** Re-run the P0 cases on v104 (head of household
   and surviving spouse yes, no, unanswered; single, joint, separate
   controls). Strict full-surface replay of the 775 recorded lists, v103
   against v104, expected changes declared; 0 unexpected; no number change.
4. **Tests.** Live tests through the coordinator for each traced case
   (lines 6 and 13 publish the 2025 ceiling for "yes" and the three other
   statuses, and block for "no" and unanswered); a package test that loads
   v104; mutants on scratch copies that fail a test (a refused status
   publishing its ceiling; a fallback to the single ceiling; a control
   status blocking). Fast lane (includes the size guard), the touched live
   tests, mypy.

## Deliverables

Content, package, registry, release, loader entries and tests; in
hoh-no-worksheet-ceilings-evidence/: track1.md (files, trace, replay,
tests). Fill a "Track 1 result" section in the plan. Commit in steps.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- Do not edit packages/kernel/ or the engine. Stop and report if the route
  needs more.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn.
