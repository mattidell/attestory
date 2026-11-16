# Charter: Track 0 adversarial closure of the line 6c and Schedule 1 alerts

Role: Builder. Source HEAD on milestone/page-alerts-2025.
Plan: docs/phases/engine-breadth/milestones/page-alerts.md (read it
whole, including the P0 result and Decisions 1-5). Evidence:
page-alerts-evidence/ (start with p0.md). Gate: `PROJECT_PLANNING.md`,
"Track 0 Adversarial Closure Gate" (read that section and its closing
paragraphs whole). Precedent: line12d-boxes-evidence/ Track 0 files and
preferential-base-reason-evidence/track0-closure.md. Do not read
governance.

## Scope

Every claim comes from a `live_coordinate_run` output or a drawn saved
page recorded in a committed JSON file and named by case id, on
published v91 and scratch v92. Read the page model's own values and the
drawn DOM; never classify by punctuation. Never work under packages/.

1. **State table for line 6c.** Every state of the election fact (not
   made, made, unanswered) crossed with benefits (none, a statement) and
   filing status (single, joint, separate). For each: what v91 draws,
   what v92 draws, the alert count, and whether the words are true
   against the 2025 Form 1040 line 6c instructions. Any state where v92
   is less true than v91 is a FAIL.
2. **The checked sibling (Decision 3).** Prototype it on scratch. For
   the same states record both sections' words, every question each
   field shows, and the page-level question list. Replay the recorded
   lists on that variant. Say whether any return is newly asked a
   question, whether any field shows a question twice, and whether an
   unanswered election blocks anything it did not block on v91.
   Recommend build or park.
3. **State table for the Schedule 1 top entry.** No Form 1099-K; a
   personal-item loss; an amount included in error, if the published
   content reaches it; a blocked top entry (an unresolved Form 1099-K);
   a return with no Schedule 1 attachment. For each: v91 and v92 words,
   alert count, the citation buttons drawn. A blocked or inapplicable
   field must not gain a citation button that implies a value.
4. **The citation (Decision 4).** Quote the passage of the 2025 Schedule
   1 instructions the new citation points at, from the local sources,
   with its locator. Check every field of the citation citizen against
   it and against how sibling citations (the line 6c and Schedule 1 line
   8 citations) are written. Say if the local sources lack the passage.
5. **The button label (Decision 5).** On one page, list the label of
   every citation button drawn on v91 and v92. Say how a label is
   chosen, why the line 6c and top-entry buttons show a raw id, and what
   content would make them read as the others do.
6. **Claim reuse.** The successors add no read, pin or scheduling
   dependency; every other v91 member composes unchanged; a v91
   workspace opened on v92 needs no new answer; an earlier package
   (v90, v79) still draws what it drew, alerts included.
7. **Neighbour table.** Reuse the P0 replay part file for the P0 scratch
   (keep it outside the repo). If item 2 or 4 changes the successor,
   replay again with `python3 tools/recorded_replay.py` in parallel (CPU
   count minus one), in the foreground, and classify every change.
   Report wall time.
8. **Integration surface.** Over the P0 census, the alert count per
   field on v91 and on the recommended v92: both parked alerts at zero on
   every computing return, no new alert anywhere, and the twelve P0
   pages redrawn in Chrome with zero alerts. Recheck the line12d-boxes
   browser cases.

Do not run the full test suite or mypy. Run every command in the
foreground and do not end your turn while a command is running. Stop and
report if anything needs an engine, schema, projection, page or kernel
change.

## Deliverable

page-alerts-evidence/track0-closure.md and track0.py with its
`track0-*.json` outputs, and a "Track 0 adversarial closure" section in
the plan: each table PASS or FAIL with counts and case ids, the item 2
recommendation, the item 4 passage, and "Known limitations affecting
correctness".

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only. No push, no
  spawn.
