# Charter: P0 of box C and F losses are limited and carried

Role: Builder. Source HEAD on milestone/cf-loss-limit-2025.
Plan: docs/phases/engine-breadth/milestones/cf-loss-limit.md (read it
whole). Precedents: tests/test_schedule_d_current_year_losses_t1.py and
..._t2_presentation.py (how Schedule D loss cases are built and run),
the no-1099-B family content (family.f8949-no1099b-st.json and -lt) and
the Schedule D line 21 rule. Do not read governance.

## Scope

1. **Cases.** Synthetic demo.* returns that reach Schedule D line 21
   with a net loss from box C only, box F only, and C plus F, each under
   every filing status the engine accepts (at least single and married
   filing separately), with losses below, at and above the limit
   ($3,000; $1,500 separately). Add the same amounts through box A/D as
   a control. Run each through the real live coordinator and the saved
   page.
2. **Hand values.** For each case compute line 7, 15, 16 and 21, Form
   1040 line 7a, and the 2026 short- and long-term carryover by the
   2025 Schedule D instructions and the Capital Loss Carryover Worksheet
   in the local sources; cite the line of the instructions used.
3. **Compare.** Engine against hand value for every line, plus
   disposition and any question or block. Note where the engine computes
   the carryover at all (and where a filer sees it). If a box C/F case
   differs from its A/D control or the hand value, trace it to the rule
   and file:line and name the smallest repair (content successor, or
   stop if it is an engine change).
4. **Recommendation.** Tests only, or a content repair with the list of
   successors.

Stop and report if a correct value needs an engine, schema, projection
or page change.

## Deliverables

In docs/phases/engine-breadth/milestones/cf-loss-limit-evidence/: p0.md
(cases, hand values with citations, comparison table, trace of any
difference, recommendation, decisions for the foreman), scripts and
small JSON outputs. Fill a "P0 result" section in the plan. No
production, test or content edits.

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
