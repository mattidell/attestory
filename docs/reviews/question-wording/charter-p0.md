# Charter: P0 of questions saying what their rules read

Role: Builder. Source HEAD on milestone/question-wording-2025.
Plan: docs/phases/engine-breadth/milestones/question-wording.md (read it
whole). Precedent: the roadmap's parked list and the milestones that
introduced each question (find them from the question citizens' git
history). Do not read governance.

## Scope

1. **Question table.** For each item in the plan, every question citizen in
   scope on core v86: its id, version and full text as the presentation
   shows it; who is asked (the selection that puts it on the page); every
   rule that reads its answer and exactly what that rule reads.
2. **Law.** Quote the 2025 instruction each question rests on, with line
   references: Form 8949 / Schedule D wash-sale (code W) instructions,
   the Form 1040 line 7 Exception 1 conditions, the Form 1040 age-65 and
   blindness rules (including a death in 2025), and the student-loan
   interest dependency rule. If the PDFs are not local, fetch them from
   irs.gov into a temp directory outside the repo and record checksums.
3. **Probes on core v86.** Through `live_coordinate_run`, with synthetic
   `demo.*` findings, run every case in the plan's "Cases that will shape
   the design". For each, say what a truthful filer would answer under the
   current words and under the proposed words, and what the return
   computes either way, against a hand value from the instructions.
4. **Design.** Proposed words for each question. Prototype a scratch core
   v87 (registry v85, release v85) under question-wording-evidence/ that
   changes only question citizens and the bundles and package entries that
   name them. Rerun the recorded returns earlier milestones replay
   (tests/fixtures/*/expected.json that drive live runs; name which) on
   v86 and scratch v87, as recorded, and classify every change from
   measured runs.

Stop and report if an item needs an engine, schema, expression-operation,
selection or recording-surface change; give the cause and leave that item
out of the prototype.

## Deliverables

In docs/phases/engine-breadth/milestones/question-wording-evidence/:
- p0.md: the table, the law, the probes with hand values, the words, the
  rerun classification and a recommendation with the decisions the
  foreman must make. Every case id it cites must appear in a committed
  output file.
- the probe and prototype scripts, and their small JSON outputs.

Load evidence harnesses in tests through `tests/evidence_loader.py` only
if you add a test; P0 adds none. Fill the plan's "P0 result" section. No
production, test or content edits.

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
