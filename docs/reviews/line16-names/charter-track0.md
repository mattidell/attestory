# Charter: Track 0 adversarial closure of line 16 naming all its questions

Role: Builder. Source HEAD on milestone/line16-names-2025.
Plan: docs/phases/engine-breadth/milestones/line16-names.md, read whole,
especially Decisions 1-5. P0 evidence: line16-names-evidence/ (p0.md,
prototype.py, boundary.py, classify.py, law.json and outputs). Seat
reading: docs/roles/qualitative-review.md. Do not read governance.

Work on P0's narrow scratch successor (v95 on published v94). Do not edit
packages/ or tests/.

## Scope

1. **Each name is a way forward.** On each of the four recorded target
   returns and the three required-Schedule-D neighbours: answer each of
   the eight named questions through the act list, one at a time, both
   ways, and record line 16's result. Every name line 16 shows must have
   at least one truthful answer that unblocks line 16 or moves it to a
   different block. FAIL a name that never does; say whether it should
   go.
2. **The boundary states.** `no-form8949-sources` yes, no and unanswered,
   each with Exception 1 fully answered, partly answered and unanswered,
   on single, joint and separate returns. Quote every reason and question
   sentence on lines 16, 20, Schedule 3 lines 1 and 8, Schedule 8812
   worksheet A line 5 and the other blocked fields (the page model's own
   sentences, no punctuation filter). FAIL an untrue sentence or a field
   with no sentence a filer can act on (Decision 3).
3. **Late answers and corrections.** Answer `no-form8949-sources` yes,
   then change it to no; withdraw it; record a sale after the eight names
   show. The names follow the current answers; no stale finding stays.
4. **Neighbours.** No Schedule D; Schedule D not required; a recorded
   sale (short and long term); the ten blocked-names-question cases. Every
   page field's value, disposition and sentence, v94 vs successor;
   classify every difference. FAIL a computing return that changes or
   gains a question, or any change to the ten cases.
5. **Drawn page.** Save the citation-walk page for one target return and
   one unanswered-boundary return and open each in headless Chrome as
   tests/test_page_alerts_v92.py does; confirm the questions draw and no
   safe-render alert appears.
6. **Replay reuse.** Reuse P0's part file; replay again only if content
   bytes change, then with `python3 tools/recorded_replay.py` in
   parallel (CPU count minus one workers), strict classification, and
   report wall time.

Write a PASS/FAIL table per item. If a FAIL needs more than a change to
which names line 16 declares (a projection, page, schema or engine
change), stop and report.

## Deliverables

In line16-names-evidence/: track0.py, track0-*.json, track0-closure.md
(tables, FAILs with proposed fixes, recommendation). Add a "Track 0
adversarial closure" section to the plan after Decisions. No production,
test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Load sibling harnesses by path under a unique name, never a bare
  `import probe`.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, and update it when
  they finish.
- Never --no-verify or a bare git stash. Foreground commands only; no
  background jobs left running.
- No push and no spawn. Do not edit packages/ or tests/.
