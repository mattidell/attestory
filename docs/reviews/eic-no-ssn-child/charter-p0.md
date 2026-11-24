# Charter: P0 of a child without a valid SSN routes the earned income credit correctly

Role: Builder. Source HEAD on milestone/eic-no-ssn-child-2025.
Plan: docs/phases/engine-breadth/milestones/eic-no-ssn-child.md (read it
whole). Precedents: the hoh-eic plan and evidence (Decision 5 parked this),
eic-qualifying-children and eic-answer-questions evidence, ADR 0081
(per-subject conditional dependencies), and the full-surface replay in
tools/recorded_replay.py (`full`). Do not read governance.

## Scope

1. **Sources.** Fetch the 2025 Form 1040 instructions (line 27a) and
   Publication 596 into the ignored temp/ directory. Quote, with page and
   line, every rule about a qualifying child who does not have a valid SSN:
   the separated-spouse rule (Step 4), whether such a child makes the
   filer "a filer with a qualifying child", and whether the filer may then
   claim the credit for a filer without a qualifying child. Read each rule
   section whole, including exceptions after the first sentence.
2. **Trace.** On published core v101, synthetic demo.* returns through the
   real live coordinator: married filer as head of household and as
   married filing separately; one child with a valid SSN, one without,
   and both; separated (written agreement or apart the last six months) or
   not; the child lived with the filer more or less than half the year.
   Record what each computes (credit, class, which questions are asked,
   what blocks), and what the sources say it should. Cite rule ids.
3. **Content route.** Try, as scratch successors on v101 loaded from
   published content: which rules, facts or input questions would route
   it. Say whether any route changes which answer an unrelated path needs.
   If content cannot, name the smallest engine change (file:line) and
   whether it needs an ADR; do not build it; stop and report.
4. **Replay.** For a content route, full-surface replay of the 775
   recorded lists, v101 against the scratch successor, with expected
   changes declared. Report pass/unexpected and unused expectations.
5. **Hand values.** For each traced case the sources decide, the expected
   credit by hand from the 2025 EIC table.

## Deliverables

In docs/phases/engine-breadth/milestones/eic-no-ssn-child-evidence/:
p0.md (sources quoted, trace table, routes tried, recommendation,
decisions for the foreman), the scripts a later test will need, and small
JSON. Fill a "P0 result" section in the plan. No production, test or
content edits.

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
