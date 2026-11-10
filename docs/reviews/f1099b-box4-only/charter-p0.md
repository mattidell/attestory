# Charter: P0 of Form 1099-B backup withholding without a sale

Role: Builder. Source HEAD on milestone/f1099b-box4-only-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box4-only.md (read it
whole). Precedent: the f1099b-backup-withholding and f1099b-box7-loss
milestones (plans, evidence directories, retrospectives). Do not read
governance.

## Scope

1. **Statement table.** For core v84, list every rule, question, closure,
   recording surface and loader entry that reads Form 1099-B statements,
   their identity, or the box 4 amount. Say how a statement with no sale
   can be recorded today, if at all, and what (if anything) closes the set
   of Form 1099-B statements for a return.
2. **Law.** Quote the 2025 Form 1099-B instructions for box 4 and for
   short sales open at year end, and the Form 1040 line 25b instruction,
   with line references. If the PDFs are not local, fetch them from irs.gov
   into a temp directory outside the repo and record their checksums.
3. **Probes on core v84.** Through `live_coordinate_run`, with synthetic
   `demo.*` findings and honest answers, run every case in the plan's
   "Cases that will shape the design". Compute Form 1040 lines 25a-25d, 33,
   34 and 37 by hand from the instructions, and say whether v84 publishes,
   blocks or refuses, and what sentence and question the presentation
   shows on each blocked row.
4. **Design.** The smallest content fix that never lets line 25b publish
   while no-sale withholding may be unasked: what asks for it (a
   return-level answer, a per-statement question, or an existing closure),
   and with what true reason. Prototype it on a scratch core v85 under
   f1099b-box4-only-evidence/, loading harnesses under unique module names
   and running earlier milestones' harnesses in a subprocess. Rerun every
   recorded v83 return from tests/fixtures/f1099b_backup_withholding_v83/
   on live v84 and scratch v85 (as recorded, never with substituted
   answers) and classify each change from measured runs.

Stop and report if the fix needs an engine, schema, expression operation
or recording-surface change. Give the cause and the smallest change.

## Deliverables

In docs/phases/engine-breadth/milestones/f1099b-box4-only-evidence/:
- p0.md: the table, the law, the probes with hand values, the design, the
  rerun classification and a recommendation with the decisions the
  foreman must make. Every case id it cites must appear in a committed
  output file.
- the probe and prototype scripts, and their small JSON outputs.

Fill the plan's "P0 result" section. No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
- Do not edit packages/kernel/.
