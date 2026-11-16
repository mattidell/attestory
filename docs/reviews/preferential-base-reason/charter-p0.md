# Charter: P0 of the lines below line 16 naming their question

Role: Builder. Source HEAD on milestone/preferential-base-reason-2025.
Plan: docs/phases/engine-breadth/milestones/preferential-base-reason.md
(read it whole). Precedent: blocked-names-question-evidence/ (p0.md,
probe.py, prototype.py, rerun.py, track0.py), ADR 0086, and
docs/reviews/blocked-names-question/review.md note BNQ-R7. Do not read
governance.

## Scope

1. **Reproduce.** On published core v90, run the four recorded v82 lists
   BNQ-R7 names through the real coordinator and the presentation
   projection. For every blocked page field record artifact, code,
   `missing` names and the questions shown at field level and page level.
   Confirm or correct BNQ-R7's list of reasonless fields.
2. **Trace.** From each reasonless field, walk producers to the point the
   question is lost. Name the rule and the guard that turns
   `capital-gains.selected-preferential-base` (or any other producer)
   inapplicable, and why the projection's walk stops there. Cite
   file:line.
3. **Other shapes.** Search the published v90 rules for the same pattern:
   a producer whose guard turns inapplicable while an answer it depends
   on is open, upstream of a filer-visible field. Probe each candidate
   with a synthetic `demo.*` act list a truthful filer can reach. Report
   which are reachable.
4. **Design.** The smallest repair. Prefer content successors on
   `rule-artifact.v17` (the line 16 pattern); compare with a projection
   change and say what each costs. Prototype the preferred design as
   scratch core v91 on published v90, loaded from published content,
   never by editing packages/. Show every case in the plan unanswered
   (each blocked field names its questions) and answered truthfully (the
   2025-instruction hand values).
5. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v90 and scratch v91, in parallel
   (CPU count minus one workers), answered as their records imply. Keep
   the part file so Track 0 can reuse the replay. Classify every change;
   the target is no number changed and no computing return newly asked a
   question. Report wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection change overlaps
another foreman's open milestone.

## Deliverables

In docs/phases/engine-breadth/milestones/preferential-base-reason-evidence/:
p0.md (reproduction table, trace, other shapes, design comparison, probe
results, rerun classification, recommendation, decisions for the
foreman), the scripts and their small JSON outputs. Fill the "P0 result"
section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
