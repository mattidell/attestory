# Charter: P0 of a counted child's missing credit answer is asked

Role: Builder. Source HEAD on milestone/eic-child-answers-2025.
Plan: docs/phases/engine-breadth/milestones/eic-child-answers.md (read it
whole). Precedents: eic-answer-questions-evidence/p0.md (sections 2 and
6, where this was found), ADR 0086 (a block expression may name what it
waits on) and the blocked-names-question milestone, ADR 0081
(per-subject conditional dependencies), the eic-qualifying-children and
child-tax-credit retrospectives, and the full-surface replay in
tools/recorded_replay.py (`full`). Do not read governance.

## Scope

1. **Trace.** On published core v100, for each per-child earned income
   credit answer (relationship, age, residency, joint return, SSN, and
   any other the count reads): synthetic demo.* returns with one and two
   children, each leaving one answer missing for one child, through the
   real live coordinator and saved page. Record what blocks, the root
   tuple (artifact, code, missing) each blocked line waits on, and what
   the page says. Cite file:line in the projection's question walk.
2. **Other rosters.** Do the same for the child tax credit roster and the
   other-dependent rosters: is a missing per-member answer asked?
3. **Content routes.** Can content reach a question? Try, as scratch
   successors on published v100 loaded from published content: declared
   `missing` names (ADR 0086) on the rule that blocks; an input question
   for the per-child fact type; a closure mapping question. Say which the
   projection reaches, whether the shown question can name the child,
   and whether any route changes which answer a path needs.
4. **If content cannot.** Name the smallest projection or schema change,
   where it would go (file:line), and whether it changes a published
   contract (needs an ADR). Do not build it; stop and report.
5. **Replay.** For a content route, full-surface replay of the 775
   recorded lists, v100 against the scratch successor, with expected
   changes declared and probes that leave each answer missing. Report
   pass/unexpected and unused expectations.

## Deliverables

In docs/phases/engine-breadth/milestones/eic-child-answers-evidence/:
p0.md (trace with root tuples, other rosters, routes tried and results,
recommendation, decisions for the foreman), scripts and small JSON. Fill
a "P0 result" section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included. Nothing over 200 KB committed.
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
