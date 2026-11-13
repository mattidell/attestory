# Charter: P0 of age and blindness being asked

Role: Builder. Source HEAD on milestone/age-blindness-asked-2025.
Plan: docs/phases/engine-breadth/milestones/age-blindness-asked.md (read it
whole). Precedent: question-wording-evidence/ (p0.md, track0-closure.md,
law.json, prototype.py). Do not read governance.

## Scope

1. **Trace.** The four facts (filer and spouse age 65 or older, filer and
   spouse blind) on core v86 and scratch v87: where each default of false
   comes from, every rule that reads them, every presentation field that
   shows them, and every recording surface or question that could supply
   them today.
2. **Law.** Quote the 2025 Form 1040 instructions for the standard
   deduction chart and worksheet, age 65 (the day-before-the-birthday
   rule), blindness, a spouse who died in 2025, and the senior deduction,
   with line references. Reuse question-wording-evidence/law.json where it
   already quotes them, checking each checksum.
3. **Probes** through `live_coordinate_run`, with synthetic `demo.*`
   findings, for every case in the plan, on v86: what publishes, against a
   hand value.
4. **Design.** The smallest change that asks the four facts and blocks the
   amounts until answered: question citizens, closures or guards, bundle
   and package successors. Prototype it as a scratch core v88 on top of
   question-wording's scratch v87 (load that prototype; do not copy it).
   Rerun every recorded fixture question-wording Track 0 replayed, on v86
   and scratch v88, as recorded, and classify every change. Count the
   returns newly asked, and show that answering as the record implies
   restores every number.

Stop and report if the fix needs an engine, schema, expression-operation,
selection or recording-surface change; give the cause and the smallest
change.

## Deliverables

In docs/phases/engine-breadth/milestones/age-blindness-asked-evidence/:
p0.md (trace, law, probes with hand values, design, rerun
classification, recommendation and the decisions for the foreman), the
scripts and their small JSON outputs. Every case id cited must appear in a
committed output. Fill the plan's "P0 result" section. No production, test
or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit incrementally, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never use --no-verify or a bare git stash. Foreground commands only.
- No push and no spawn. Do not edit packages/.
