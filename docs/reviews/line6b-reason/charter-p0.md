# Charter: P0 of line 6b naming why it is blocked

Role: Builder. Source HEAD on milestone/line6b-reason-2025.
Plan: docs/phases/engine-breadth/milestones/line6b-reason.md (read it
whole). Precedent: page-alerts-evidence/ (probe.py, census.py and its
wage + SSA cases; on this branch read it from `git show
github/milestone/page-alerts-2025:<path>` because PR #280 is not merged),
blocked-names-question-evidence/p0.md (ADR 0086 design),
box4-amount-asked-evidence/p0.md (a parked finding that did not
reproduce). Do not read governance.

## Scope

1. **Reproduce first.** On published core v91, run the plan's cases as
   synthetic `demo.*` act lists through the real live coordinate run and
   the presentation projection. For each, record line 6b's disposition,
   code, `missing` list, every reason and question sentence the page
   model gives for it, and the root rule and branch that refused. Read
   the page model's own sentences; do not filter by punctuation. Say
   which cases a truthful filer can reach. If no reachable case blocks
   line 6b without a reason, stop and report.
2. **Trace.** For each reasonless block, name the rule, version and
   expression branch that refuses, why its `missing` list is empty, and
   which question (existing citizen or not) would unblock it. Cite
   file:line.
3. **Design.** The smallest repair. Prefer content: a rule-artifact v17
   successor whose `block` expression declares the names, plus any
   input-question citizen the names need. Never change which answer a
   path needs or its refusal code. Compare any alternative and say what
   it costs. Prototype as a scratch core successor on published v91,
   loaded from published content, never by editing packages/; show the
   page model now gives a true reason and question in every reproduced
   case, and check every new sentence against the 2025 Form 1040
   instructions in the local sources.
4. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v91 and the scratch successor
   in parallel (CPU count minus one workers), keep the part file so
   Track 0 reuses the replay, and classify every change. Target: no
   number changed and no computing return newly asked a question. Report
   wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection or page change
overlaps another foreman's open milestone (blocked-sale-pages).

## Deliverables

In docs/phases/engine-breadth/milestones/line6b-reason-evidence/: p0.md
(reproduction table, trace, design comparison, prototype results, rerun
classification, recommendation, decisions for the foreman), the scripts
and their small JSON outputs. Fill the "P0 result" section in the plan.
No production, test or content edits.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- An evidence script that imports a sibling harness by bare name loads it
  by path under a unique name instead (a bare `import probe` picks up
  whichever evidence directory is first on sys.path).
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never --no-verify or a bare git stash. Foreground commands only; do not
  leave background jobs running when you finish.
- No push and no spawn. Do not edit packages/.
