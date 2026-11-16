# Charter: P0 of the box 4 withholding amount being asked

Role: Builder. Source HEAD on milestone/box4-amount-asked-2025.
Plan: docs/phases/engine-breadth/milestones/box4-amount-asked.md (read it
whole). Precedent: preferential-base-reason-evidence/ (p0.md, probe.py,
prototype.py, cases.py, rerun.py), the f1099b-backup-withholding and
f1099b-box4-only plans and evidence, and ADR 0086. Do not read
governance.

## Scope

1. **Reproduce.** On published core v91, run the three cases the plan
   names and the plan's other cases through the real coordinator and the
   presentation projection, as synthetic `demo.*` act lists a truthful
   filer can reach. For every blocked page field record artifact, code,
   `missing` names and the questions shown at field level and page level.
   Say for each case which box 4 answers were recorded, so the silence is
   attributed to the yes/no, the amount, or both.
2. **Trace.** From `form1040.line-25b` and `form1040.line-25d`, walk
   producers to the point the question is lost. Name the rule, the fact
   the walk ends on, and why the projection has no sentence for it.
   Explain the v83 roadmap claim that line 25b blocks "with its
   question": where it holds and where it does not. Cite file:line.
3. **Other shapes.** Search the published v91 content for the same
   pattern: a paired or keyed amount a filer-visible line waits on, with
   no input-question citizen or closure mapping for that fact (Form
   1099-INT, 1099-DIV, W-2G, 1099-K and W-2 withholding amounts
   included). Probe each candidate. Report which are reachable.
4. **Design.** The smallest repair. Prefer content: an input-question
   citizen for the amount fact, or a rule successor on
   `rule-artifact.v17` that declares the names it waits on. Compare with
   a projection change and say what each costs. Prototype the preferred
   design as scratch core v92 on published v91, loaded from published
   content, never by editing packages/. Show every case in the plan
   unanswered (each blocked field asks for the amount) and answered
   truthfully (the 2025-instruction hand values). Say whether the
   question can tell the filer which statement it means and, if not,
   whether the wording is still answerable with two statements.
5. **Rerun.** Replay the recorded lists with
   `python3 tools/recorded_replay.py` on v91 and scratch v92, in parallel
   (CPU count minus one workers), answered as their records imply. Keep
   the part file so Track 0 can reuse the replay. Classify every change;
   the target is no number changed and no computing return newly asked a
   question. Report wall time.

Stop and report if the design needs an engine, schema, projection, page
or kernel change; name the smallest one. A projection or page change
overlaps another foreman's open milestone (blocked-sale-pages).

## Deliverables

In docs/phases/engine-breadth/milestones/box4-amount-asked-evidence/:
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
