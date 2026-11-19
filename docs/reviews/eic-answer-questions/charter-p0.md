# Charter: P0 of every earned income credit answer has a question

Role: Builder. Source HEAD on milestone/eic-answer-questions-2025.
Plan: docs/phases/engine-breadth/milestones/eic-answer-questions.md (read
it whole). Precedents: hoh-eic (review.md EIC-R1, where this was found,
and the evidence probe.py), the earned-income-credit and
eic-qualifying-children retrospectives, and the full-surface replay in
tools/recorded_replay.py (`full`). Do not read governance.

## Scope

1. **Census.** For every `rule.eic-answer.*` rule on published core v99:
   the fact it reads, when that answer is required (statuses, child
   count, income), whether an input question for that fact exists, and
   whether the saved page shows a sentence when it is missing. Do the same
   for any other fact a credit rule requires of the filer.
2. **Reproduce.** Synthetic demo.* returns that leave each unasked
   answer missing, run through the real live coordinator and saved page:
   what blocks, and what the page says.
3. **Record.** For each unasked answer, does the record already prove it
   (for example a recorded date of birth for the age test, the dependent
   roster, SSN facts)? A derivation must never make a return newly block
   or change a number where the filer has already answered.
4. **Design.** The smallest honest change: an input question for each
   answer the record cannot prove, written from the 2025 line 27a
   instructions (quote the source lines), and a derivation only where it
   is sound and simple. Never change which answers a path needs.
   Prototype it as a scratch core successor on published v99, loaded
   from published content, never by editing packages/.
5. **Replay.** Full-surface replay of the 775 recorded lists, v99 against
   the scratch successor, with expected changes declared, and probes that
   leave each answer unanswered (no pre-filled answers). Report
   pass/unexpected and unused expectations.

Stop and report if the honest design needs an engine, schema,
projection, page or kernel change, or a new ADR.

## Deliverables

In docs/phases/engine-breadth/milestones/eic-answer-questions-evidence/:
p0.md (census table, reproduction, design with source quotes, prototype
and replay results, recommendation, decisions for the foreman), scripts
and small JSON. Fill a "P0 result" section in the plan. No production,
test or content edits.

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
