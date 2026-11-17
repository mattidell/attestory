# Charter: P0 of a box 4 "no" not being asked for an amount

Role: Builder. Source HEAD on milestone/box4-no-prompt-2025.
Plan: docs/phases/engine-breadth/milestones/box4-no-prompt.md (read it
whole). Precedent: box4-amount-asked-evidence/ (p0.md, probe and cases;
the observation this milestone starts from), line6b-reason-evidence/
(probe harness on core v93), page-alerts-evidence/. Do not read
governance.

## Scope

1. **Reproduce first.** On published core v93, run the plan's cases as
   synthetic `demo.*` act lists through the real live coordinate run and
   the presentation projection. For each, record lines 25b, 25d, 33 and
   37: disposition, value, code, `missing` list, and every reason and
   question sentence the page model gives. Read the page model's own
   sentences; do not filter by punctuation. Say which cases a truthful
   filer can reach. If a box 4 "no" with no amount no longer blocks or
   no longer shows the amount prompt, stop and report.
2. **Trace.** Quote the published yes/no question and the amount
   prompt, and say whether a truthful "no" means nothing was withheld
   on that statement (cite the 2025 Form 1040 and Form 1099-B
   instructions in the local sources). Name the rule, version and branch
   that wait on the amount, and why they do not read the yes/no. Cite
   file:line.
3. **Design.** The smallest repair. Prefer content: rule successors that
   treat a "no" as zero withheld for that statement, keeping the amount
   prompt for "yes" and unanswered. Settle a "no" with a nonzero amount
   (refuse, or prefer one) and say why. Never change a refusal code or
   what any other answer requires. Compare any alternative and say what
   it costs. Prototype as a scratch core successor on published v93,
   loaded from published content, never by editing packages/; show
   lines 25b/25d compute on a "no" and that the page no longer shows the
   amount prompt there; check every new sentence against the local
   sources.
4. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v93 and the scratch successor
   in parallel (CPU count minus one workers), keep the part file so
   Track 0 reuses the replay, and classify every change. Expected: only
   lists that answered "no" without an amount change, and each change
   is lines 25b/25d (and their dependants) computing where they blocked
   on the amount. Report wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection or page change
overlaps another foreman's open milestone (blocked-sale-pages).

## Deliverables

In docs/phases/engine-breadth/milestones/box4-no-prompt-evidence/: p0.md
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
