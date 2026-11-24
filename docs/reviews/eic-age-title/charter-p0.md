# Charter: P0 of the age fact's title says what its question asks

Role: Builder. Source HEAD on milestone/eic-age-title-2025.
Plan: docs/phases/engine-breadth/milestones/eic-age-title.md (read it
whole). Precedents: eic-answer-questions (review EAQ-R7), sale-reasons-plain
(P0: successors of pinned citizens unpin saved records), and the
full-surface replay in tools/recorded_replay.py (`full`). Do not read
governance.

## Scope

1. **Where the title shows.** Every place the `eic.age-25-under-65` fact
   type's title reaches a filer or an auditor on core v103 (saved page,
   question groups, explanation graph, reports). Cite file:line and give a
   rendered example on a synthetic demo.* return.
2. **Pins.** How a saved answer pins the fact type and the bundle
   (`eic-questions.bundle.json`), and what a successor would do to a saved
   return that answered on the current version. Test it on a synthetic
   return: answer on v103, then load a scratch successor.
3. **Source.** Quote the 2025 Form 1040 instructions (line 27a, Step 4)
   and Publication 596 on age at death for this test.
4. **Route.** If safe, a scratch successor with the corrected title and a
   full-surface replay of the 775 recorded lists, v103 against it,
   expected changes declared. If not safe, or the title is never shown,
   stop and recommend parking with the reason.

## Deliverables

In docs/phases/engine-breadth/milestones/eic-age-title-evidence/: p0.md
(where it shows, pins, source, route or stop reason, decisions for the
foreman), scripts a later test will need, small JSON. Fill a "P0 result"
section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed. Fetched sources
  stay in ignored temp/.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit with separate simple commands (mkdir lock; git add <paths>;
  git commit -F file; rmdir lock) under
  `$(git rev-parse --git-dir)/collaboration-commit.lock`.
- Bound every command that can hang; never `rm -rf`.
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
