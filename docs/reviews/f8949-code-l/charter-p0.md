# Charter: P0 of Form 8949 code L for a box 7 loss

Role: Builder. Source HEAD on milestone/f8949-code-l-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-code-l.md (read it
whole). Precedent: the f1099b-box7-loss and f8949-code-b milestones
(plans, evidence directories, retrospectives). Do not read governance.

## Scope

0. **Opening fix.** Measure why
   `tests/test_integration_checkpoint.py::TestT1ThroughT9::test_t1_fully_includible_report_survives_without_adjustment`
   takes about 7 s in the fast lane (CI `quick`; budget 3.0 s in
   tests/conftest.py). If it pays a one-time load another test would
   otherwise pay, make the load cheaper or shared; otherwise mark it
   honestly live with a measured reason. Never raise the budget. Commit
   this alone first.
1. **Law.** Quote the 2025 Form 1099-B box 7 instruction, the Form 8949
   instructions for code L (and any column (g) rule for it), and any
   Schedule D text, with line references. If the PDFs are not local,
   fetch them from irs.gov into a temp directory outside the repo and
   record their checksums. Say plainly whether a box 7 loss is wholly
   disallowed, and whether any part can be allowed and on what facts.
2. **Table.** For core v85, every rule, question and loader entry that
   reads the box 7 answer, verdicts or checks, and every Form 8949 code
   path (B, W, and how other codes are refused).
3. **Probes on core v85.** Through `live_coordinate_run`, with synthetic
   `demo.*` findings and honest answers, run every case in the plan's
   "Cases that will shape the design". Compute Schedule D lines 1a-16 and
   21, Form 8949 rows, and Form 1040 lines 7a, 15, 16, 24, 33, 34 and 37
   by hand from the instructions.
4. **Design.** The smallest content fix: the code L row and adjustment,
   which box 7 losses compute and which stay refused, and with what true
   reason and question. Prototype it on a scratch core v86 under
   f8949-code-l-evidence/, loading harnesses under unique module names and
   running earlier milestones' harnesses in a subprocess. Rerun every
   recorded return in tests/fixtures/f1099b_backup_withholding_v83/
   (as recorded, plus the box 4 yes/no answered no where core v85 asks it)
   on live v85 and scratch v86, and classify each change from measured
   runs.

Stop and report if the fix needs an engine, schema, expression operation
or recording-surface change. Give the cause and the smallest change.

## Deliverables

In docs/phases/engine-breadth/milestones/f8949-code-l-evidence/:
- p0.md: the opening fix, the law, the table, the probes with hand values,
  the design, the rerun classification and a recommendation with the
  decisions the foreman must make. Every case id it cites must appear in
  a committed output file.
- the probe and prototype scripts, and their small JSON outputs.

Fill the plan's "P0 result" section. No production or content edits
beyond item 0.

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
