# Charter: P0 of Form 1099-B box 7 read only beside a loss

Role: Builder. Source HEAD on milestone/f1099b-box7-loss-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box7-loss.md (read it
whole). Precedent: the sale-family-audit and f1099b-backup-withholding
milestones (plans, evidence directories, retrospectives). Do not read
governance.

## Scope

1. **Box 7 table.** For core v83, list every rule, question and loader
   entry that reads the box 7 answer, and for each of the eight sale
   families the amounts a per-sale gain/loss test would read.
2. **Law.** Quote the 2025 Form 1099-B box 7 and Form 8949 instructions
   (and any Schedule D text) with line references. If the PDFs are not
   local, fetch them from irs.gov into a temp directory outside the repo
   and record their checksums.
3. **Probes on core v83.** Through `live_coordinate_run`, with synthetic
   `demo.*` findings and honest answers, run every case in the plan's
   "Cases that will shape the design". Compute Schedule D lines 1a-16 and
   Form 1040 lines 7a, 15, 16, 24, 33, 34 and 37 by hand from the
   instructions, and say whether v83 publishes, blocks or refuses.
4. **Design.** The smallest content fix: the loss test, what box 7 "yes"
   refuses and with what true reason, and whether the box 7 question
   changes. Prototype it on a scratch core v84 under
   f1099b-box7-loss-evidence/, loading harnesses under unique module
   names and running earlier milestones' harnesses in a subprocess. Rerun
   every v83 return from tests/fixtures/f1099b_backup_withholding_v83/
   (as recorded, never with substituted answers) and classify each change
   from measured v83-versus-v84 runs.

Stop and report if the fix needs an engine, schema, expression operation
or recording-surface change. Give the cause and the smallest change.

## Deliverables

In docs/phases/engine-breadth/milestones/f1099b-box7-loss-evidence/:
- p0.md: the table, the law, the probes with hand values, the design, the
  v83 rerun classification and a recommendation with the decisions the
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
