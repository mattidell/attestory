# Charter: P0 of gains and break-even sales reach Schedule D

Role: Builder. Source HEAD on milestone/gain-break-even-2025.
Plan: docs/phases/engine-breadth/milestones/gain-break-even.md (read it
whole). Precedent: cf-loss-limit-evidence/ (cases.py, hand.py,
compare.py; how 90 returns were built, run and compared) and
tests/test_schedule_d_current_year_losses_t1.py. Do not read governance.

## Scope

1. **Census.** For each sale path (covered with basis reported, covered
   code W, noncovered, code B, no Form 1099-B box C and F; short and
   long term), list which existing tests run a gain and which an exact
   break-even (proceeds equal basis) through the live coordinator, with
   file:line. Name the gaps.
2. **Cases.** For every gap, and one already-covered path as a control,
   build synthetic demo.* returns with a gain and a break-even, single
   and married filing jointly, and one mixed return (a gain on one path,
   a loss on another, netting to a gain). Run each through the real live
   coordinator and saved page on published core v96.
3. **Hand values.** Form 8949 part totals, Schedule D lines 1a-7 and
   8a-15, 16, Form 1040 line 7a, and for a net gain the
   qualified-dividends-and-capital-gain worksheet path to line 16 tax,
   from the 2025 instructions in the local sources; cite the lines.
   Check accepted ADRs and rule notes for a bound before calling a
   missing or blocked value a defect.
4. **Compare and trace.** Engine against hand value on every line, plus
   disposition, block and question. Trace any difference to rule and
   file:line, and name the smallest repair, or stop if it needs an
   engine change.
5. **Recommendation.** Tests only, a content repair with its successor
   list, or close with evidence if already covered.

## Deliverables

In docs/phases/engine-breadth/milestones/gain-break-even-evidence/:
p0.md (census, cases, hand values with citations, comparison, trace,
recommendation, decisions for the foreman), scripts and small JSON.
Fill a "P0 result" section in the plan. No production, test or content
edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks; update it when done.
- Never --no-verify or a bare git stash. Foreground commands only; leave
  no background jobs. No push and no spawn. Do not edit packages/ or
  tests/.
