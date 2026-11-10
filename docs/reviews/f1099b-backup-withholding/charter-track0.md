# Charter: Track 0 adversarial closure of Form 1099-B backup withholding

Role: Builder. Source HEAD on milestone/f1099b-backup-withholding-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md
(read it whole, including the P0 result, the foreman check and Decisions
1-4). Evidence: f1099b-backup-withholding-evidence/. Gate:
`PROJECT_PLANNING.md`, "Track 0 Adversarial Closure Gate" (read that
section and its closing paragraphs whole). Precedent:
sale-family-audit-evidence/track0-closure.md and its track0.py. Do not
read governance.

## Scope

Every claim must come from a `live_coordinate_run` output saved in a
committed JSON file and named by case id. Never substitute answers a
return did not record. Never work under packages/content.

0. **Redo the P0 gaps first.** Run on the scratch v83 every P0 probe with
   a box 4 amount (one statement, two statements, short and long term on
   one statement, beside Form 1099-INT and 1099-DIV withholding, a
   statement removed after its amount). Save outputs; compare each with
   the hand values in p0.md.
1. **Decision 2.** Try a content-only line 25b v7 that lets a recorded v82
   "no" close its statement at $0 beside the new amount. Report whether it
   works, as a `REPAIRS` switch.
2. **Authority-lifecycle table** for the box 4 amount, the v82 yes/no
   answer, the eight sale counts and each statement's identity.
3. **Empty/nonempty matrix:** each sale family with box 4 amount 0,
   positive, unrecorded, and with only the v82 answer.
4. **Late-member trace:** a statement with an amount, then a sale on a
   new statement; a statement removed after its amount.
5. **Claim reuse:** the five existing line 25b subtotals unchanged.
6. **Neighbour dependency diff:** all 213 returns in
   tests/fixtures/sale_family_audit_v82/expected.json, run with their
   recorded answers on v82 and on the scratch v83, in a subprocess (never
   import earlier harnesses beside your own). Classify every change.
7. **Integration surface:** every consumer of line 25b (lines 33, 34, 37),
   each blocked line's reason and (disposition, code, missing), and a
   presentation probe of the new question and field.

Then write the closing declaration under the plan's "Track 0 adversarial
closure" heading. A row is PASS only if no counterexample stands beside
it. Repairs are switchable changes in prototype.py. Where a fix cannot
pass without an engine, schema or recording change, mark it FAIL and stop.

## Deliverables

- f1099b-backup-withholding-evidence/track0-closure.md;
- track0.py (unique module name, mutates no other module's globals) and
  its JSON outputs;
- the plan's "Track 0 adversarial closure" section.

No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
- Never use --no-verify or a bare git stash.
- No push and no spawn. Do not edit packages/kernel/.
