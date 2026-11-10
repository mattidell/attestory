# Charter: Track 0 adversarial closure of Form 1099-B box 7 beside a loss

Role: Builder. Source HEAD on milestone/f1099b-box7-loss-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box7-loss.md (read it
whole, including the P0 result and Decisions 1-6). Evidence:
f1099b-box7-loss-evidence/. Gate: `PROJECT_PLANNING.md`, "Track 0
Adversarial Closure Gate" (read that section and its closing paragraphs
whole). Precedent: f1099b-backup-withholding-evidence/track0-closure.md
and its track0.py. Do not read governance.

## Scope

Every claim must come from a `live_coordinate_run` output saved in a
committed JSON file and named by case id. Hand values come from the 2025
instructions (law.json), never from what the prototype publishes. Never
substitute answers a return did not record. Never work under
packages/content.

0. **Decision 5.** Switch prototype.py so line 16 v4 keeps the eight
   sale-count requirements, as a `REPAIRS` entry or the decided default,
   and rerun the 298 recorded v83 runs: all must be identical.
1. **Authority-lifecycle table** for the box 7 answer, each per-sale
   verdict, each family check, the sale counts and each statement's
   identity.
2. **Empty/nonempty matrix:** each of the eight sale families with box 7
   no, yes beside a gain, yes beside a loss, yes beside zero, and
   unanswered.
3. **Late-member traces:** a gain statement answered yes, then a loss sale
   added to it; a loss sale on a yes statement removed; a statement's
   answer changed from yes to no; a new statement added unanswered.
4. **Claim reuse:** lines 7 and 15, the sale counts, the covered-flag
   refusal map and Exception 1 compose unchanged; line 16 on a box 7 "no"
   return is identical to v83.
5. **Neighbour dependency diff:** all 298 recorded runs in
   tests/fixtures/f1099b_backup_withholding_v83/expected.json on v83 and
   the scratch v84, in a subprocess. Classify every change.
6. **Integration surface:** every consumer of line 16 (Schedule D lines
   17-22, Form 1040 lines 7a, 15, 16, 24, 33, 34, 37), each blocked line's
   reason and (disposition, code, missing), and a presentation probe of
   the refusal sentence and the box 7 question.

Also try a smaller shape for Decision 6 (fewer than 16 new rules) and
report whether it works; do not adopt it unless every row still passes.

Then write the closing declaration under the plan's "Track 0 adversarial
closure" heading. A row is PASS only if no counterexample stands beside
it. Repairs are switchable changes in prototype.py. Where a fix cannot
pass without an engine, schema or recording change, mark it FAIL and stop.

## Deliverables

- f1099b-box7-loss-evidence/track0-closure.md;
- track0.py (unique module name, mutates no other module's globals) and
  its JSON outputs;
- the plan's "Track 0 adversarial closure" section.

No production, test or content edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never use --no-verify or a bare git stash.
- No push and no spawn. Do not edit packages/kernel/.
