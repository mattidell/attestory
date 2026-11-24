# Charter: P0 of a refused head of household status does not set the worksheet ceilings

Role: Builder. Source HEAD on milestone/hoh-no-worksheet-ceilings-2025.
Plan: docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings.md
(read it whole). Precedents: hoh-qualifying-person (plan, evidence and
review HOH-R5), qss-qualifying-person if present, filing-status tests
(core v98), and the full-surface replay in tools/recorded_replay.py
(`full`). Do not read governance.

## Scope

1. **Trace.** On published core v102, synthetic demo.* returns through the
   real live coordinator: head of household with the qualifying-person
   answer yes, no and unanswered; qualifying surviving spouse likewise; a
   single control. Record what Qualified Dividends and Capital Gain Tax
   Worksheet lines 6 and 13 and every line that reads them publish, block
   or show, and the explanation the page gives. Cite rule ids.
2. **How refusal is read today.** Which rules already read the
   head-of-household and surviving-spouse test results (the
   `hoh.tests-met` and QSS facts or their derived symbols), and how. Can
   lines 6 and 13 read the same thing in content?
3. **What should show.** From the 2025 Form 1040 instructions and the
   worksheet, what a filer whose claimed status is refused should see on
   lines 6 and 13: a block with a reason, or another status's ceiling.
   Quote the source; do not invent a fallback status.
4. **Content route.** Scratch successors on v102. Say whether any route
   changes which answer an unrelated path needs.
5. **Replay.** Full-surface replay of the 775 recorded lists, v102 against
   the scratch successor, expected changes declared. Report
   pass/unexpected, unused expectations and any number change.
6. **Size.** Each scratch rule file against `tests/test_content_file_sizes.py`
   (run it on a scratch copy if needed).

## Deliverables

In docs/phases/engine-breadth/milestones/hoh-no-worksheet-ceilings-evidence/:
p0.md (trace, how refusal is read, sources, route, replay, sizes,
decisions for the foreman), scripts a later test will need, small JSON.
Fill a "P0 result" section in the plan. No production, test or content
edits.

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
