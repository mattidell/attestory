# Charter: P0 of Form 1099-B backup withholding

Role: Builder. Source HEAD on milestone/f1099b-backup-withholding-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md
(read it whole). Precedent: the sale-family-audit milestone (plan,
evidence directory, retrospective) and the statement-withholding-pairing
milestone (line 25b per-statement pairing, ADR 0083). Do not read
governance.

## Scope

1. **Withholding table.** For core v82, list every source line 25b reads
   (subtotal, statement object, per-statement answer, pairing rule) and
   the Form 1099-B box 4 question and the rules that read it. Say whether
   any Form 1099-B record carries a box 4 amount today.
2. **Law.** Quote the 2025 Form 1040 line 25b and Form 1099-B box 4
   instructions with line references. If the PDFs are not local, fetch
   them from irs.gov into a temp directory outside the repo and record
   their checksums.
3. **Probes on core v82.** Through `live_coordinate_run`, with synthetic
   `demo.*` findings and honest answers, run every case in the plan's
   "Cases that will shape the design". Compute lines 25b, 33, 34 and 37
   by hand and say whether v82 publishes, blocks or refuses.
4. **Design.** The smallest content fix: where the box 4 amount is
   recorded, how line 25b pairs it per statement, what the box 4
   question becomes, and the true reason each blocked line gives.
   Prototype it on a scratch core v83 under
   f1099b-backup-withholding-evidence/, loading harnesses under unique
   module names and running earlier milestones' harnesses in a
   subprocess, never importing them beside your own. Rerun every v82
   return from tests/fixtures/sale_family_audit_v82/ and classify each
   change.

Stop and report if the fix needs an engine, schema, expression operation
or recording-surface change. Give the cause and the smallest change.

## Deliverables

In docs/phases/engine-breadth/milestones/f1099b-backup-withholding-evidence/:
- p0.md: the table, the law, the probes with hand values, the design, the
  v82 rerun classification and a recommendation with the decisions the
  foreman must make;
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
