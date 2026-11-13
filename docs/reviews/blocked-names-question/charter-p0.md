# Charter: P0 of blocked lines naming their question

Role: Builder. Source HEAD on milestone/blocked-names-question-2025.
Plan: docs/phases/engine-breadth/milestones/blocked-names-question.md (read
it whole). Roadmap: docs/phases/engine-breadth/engine-breadth-roadmap.md,
"Parked work and open questions" (the items the plan lists). Precedent for
evidence shape: docs/phases/engine-breadth/milestones/question-wording-evidence/
(p0.md, probe.py, prototype.py). Do not read governance.

## Scope

1. **Reproduce.** For each of the plan's five cases, build a synthetic
   `demo.*` act list a truthful filer would produce and run it through
   `live_coordinate_run` and the presentation model on published core v87.
   Record: which lines block, each block's disposition, code and missing
   names, the reason sentences shown, and the questions shown (expected
   none). Say plainly if a case is no longer reachable on v87.
2. **Trace.** For each reachable case, find where the question is lost:
   the rule's block (what `missing` names, and why it names no question
   symbol), the admission or closure check, or the presentation projection
   that maps a missing name to a question. Cite file:line.
3. **Design.** The smallest change that makes each block name its
   question. Compare (a) content-only routes (question citizens, closure
   mappings, rule successors within `rule-artifact.v16`) and (b) a
   rule-artifact successor whose block declares the question it waits on.
   Prototype the chosen shape on a scratch core after v87, loaded from
   published content, never by editing packages/. If (b), draft the ADR's
   Decision text in p0.md (not under docs/adr/).
4. **Rerun.** Replay every recorded fixture question-wording Track 0
   replayed (its neighbour set, 775 lists) on v87 and the scratch core,
   as recorded. Run in parallel shards (CPU count minus one) from one
   replay, and report wall time. Classify every change; the target is
   identical numbers and no new question where a return computed before.

Stop and report if the fix needs a kernel change, or changes which answer a
refused path needs (only the naming may change).

## Deliverables

In docs/phases/engine-breadth/milestones/blocked-names-question-evidence/:
p0.md (cases, trace, design comparison, prototype result, rerun
classification, recommendation, the decisions for the foreman), the
scripts and their small JSON outputs. Every case id cited must appear in a
committed output. Fill a "P0 result" section in the plan. No production,
test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never use --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
