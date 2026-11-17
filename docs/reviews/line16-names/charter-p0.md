# Charter: P0 of line 16 naming all its questions

Role: Builder. Source HEAD on milestone/line16-names-2025.
Plan: docs/phases/engine-breadth/milestones/line16-names.md (read it
whole). Precedent: preferential-base-reason-evidence/ (p0.md,
track0, line16-gate.json and the scripts that built it; Decisions 7-8
and the Track 1 result in its plan), blocked-names-question-evidence/
(probe.py and its ten cases). Do not read governance.

## Scope

1. **Reproduce first.** On published core v94, run the plan's cases as
   synthetic `demo.*` act lists through the real live coordinate run and
   the presentation projection. For each, record lines 16, 20, Schedule
   3 lines 1 and 8, Schedule 8812 worksheet A line 5, and the other
   blocked filer fields: disposition, code, `missing` list, and every
   reason and question sentence the page model gives. Read the page
   model's own sentences; do not filter by punctuation. If line 16 now
   names the same questions as the other blocked fields, stop and
   report.
2. **Trace.** Name the line 16 rule, version and guard branch that
   names the four sale questions, and why lines 20, Schedule 3 lines 1
   and 8 and 8812 line 5 follow it. Cite file:line.
3. **The protected case.** On `exception1_personal_loss_8949`, answer
   each of the eight questions (through the act list, one at a time)
   and say which ones unblock line 16 or move it to a different block.
   Check each of the eight sentences against the 2025 Form 1040,
   Schedule D and Form 8949 instructions in the local sources. Conclude
   whether eight names are true on that case. If they are, recommend
   that it change; if not, find what tells it apart inside line 16.
4. **Design.** The smallest repair. Prefer content: a
   `rule.form1040-line16` successor declaring the names (rule-artifact
   v17), with any dependant successor only if it is needed. Never change
   which answer a path needs or a refusal code. Compare any alternative
   and say what it costs. Prototype as a scratch core successor on
   published v94, loaded from published content, never by editing
   packages/.
5. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v94 and the scratch successor
   in parallel (CPU count minus one workers), keep the part file outside
   the repo so Track 0 reuses it, and classify every change strictly:
   compare every row (including added or removed rows) and fail any
   changed value, disposition or refusal code before giving a change an
   expected label (see box4-no-prompt-evidence/classify.py). Expected:
   only lists in the required-and-no-sale state change, and only their
   line 16 missing names and question sentences. Report wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection or page change
overlaps another foreman's open milestone (blocked-sale-pages).

## Deliverables

In docs/phases/engine-breadth/milestones/line16-names-evidence/: p0.md
(reproduction table, trace, the protected case, design comparison,
prototype results, rerun classification, recommendation, decisions for
the foreman), the scripts and their small JSON outputs. Fill the "P0
result" section in the plan. No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Write your JSON report before your final checks, so a usage limit
  does not lose it; update it when the checks finish.
- Never --no-verify or a bare git stash. Foreground commands only; do not
  leave background jobs running when you finish.
- No push and no spawn. Do not edit packages/.
