# Charter: P0 of a Form 1099-B bartering amount is not lost

Role: Builder. Source HEAD on milestone/f1099b-bartering-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-bartering.md (read it
whole). Precedents: sale-family-audit.md (finding N2 and how other
out-of-class Form 1099-B boxes are refused, e.g. boxes 8 to 11 and the
`no-other-schedule-d-sources` answer), f1099b-box7-loss and
f1099b-backup-withholding (how a box became asked and refused), and
the full-surface replay in tools/recorded_replay.py (`full`). Do not
read governance.

## Scope

1. **Trace today.** On published core v96: can a Form 1099-B with a
   box 13 amount be recorded (recording surface, family, fact types)?
   Which question or answer, if any, asks about bartering or refuses
   it? Build synthetic demo.* returns (box 13 alone, box 13 beside an
   ordinary sale, box 13 of 0) and run them through the real live
   coordinator and saved page. Say exactly what the return shows and
   whether income is silently dropped. Cite file:line.
2. **Sources.** From the 2025 Form 1099-B, Form 1040, Schedule 1 and
   Schedule C instructions in the local sources, state where box 13
   bartering is reported and what the engine would need to compute it.
   Check accepted ADRs and rule notes for a bound on bartering or on
   income outside the supported class.
3. **Design.** The smallest honest change. Prefer a content-only route
   (an input question or answer that refuses a box 13 amount with a
   named reason, as other out-of-class sources do). Never change which
   answer an existing path needs except to refuse a return that is
   silently wrong today. Prototype it as a scratch core successor on
   published v96, loaded from published content, never by editing
   packages/.
4. **Replay.** Full-surface replay of the 775 recorded lists, v96
   against the scratch successor, with the expected changes declared;
   report pass/unexpected and unused expectations, and whether any
   recorded return carries a box 13 amount.

Stop and report if the honest design needs an engine, schema,
projection, page or kernel change, or if a recording surface does not
exist for box 13 at all (then name what records it).

## Deliverables

In docs/phases/engine-breadth/milestones/f1099b-bartering-evidence/:
p0.md (trace, sources with citations, bounds, design, prototype and
replay results, recommendation, decisions for the foreman), scripts and
small JSON. Fill a "P0 result" section in the plan. No production, test
or content edits.

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
