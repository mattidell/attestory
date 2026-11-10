# Charter: Track 0 adversarial closure of Form 1099-B backup withholding without a sale

Role: Builder. Source HEAD on milestone/f1099b-box4-only-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-box4-only.md (read it
whole, including the P0 result and Decisions 1-7). Evidence:
f1099b-box4-only-evidence/. Gate: `PROJECT_PLANNING.md`, "Track 0
Adversarial Closure Gate" (read that section and its closing paragraphs
whole). Precedent: f1099b-box7-loss-evidence/track0-closure.md and its
track0.py. Do not read governance.

## Scope

Every claim must come from a `live_coordinate_run` output saved in a
committed JSON file and named by case id. Hand values come from the 2025
instructions (law.json), never from what the prototype publishes. Never
substitute answers a return did not record, except where an item below
names the added answer explicitly. Never work under packages/content.

0. **Decision 7.** Change the prototype's two return-level question texts
   (and the line 25b field explanation if it names them) so they exclude a
   statement whose box 4 was entered with its sales. Keep the sentences
   plain and true.
1. **Authority-lifecycle table** for the yes/no, the return-level amount,
   each per-statement amount (with and without a sale) and each
   statement's identity.
2. **Empty/nonempty matrix:** no Form 1099-B, sale statements only, a
   no-sale statement only, both; each with the yes/no unanswered, no, yes
   with amount, and yes with amount unanswered; per-statement amount zero
   and nonzero.
3. **Late-member traces:** a no-sale statement answered yes, then a sale
   added to it and the answer changed to no; a sale removed leaving a
   per-statement amount; the return-level amount corrected; the yes/no
   superseded from yes to no.
4. **Claim reuse:** the six line 25b subtotals, the per-statement box 4
   subtotal and question, and the box 7 checks compose unchanged; line 25b
   on a "no" return equals v84.
5. **Neighbour dependency diff:** all 298 recorded runs in
   tests/fixtures/f1099b_backup_withholding_v83/expected.json on live v84
   and scratch v85, in a subprocess. Then rerun the 91 that newly ask with
   one added answer, the yes/no answered no, and show every v84 number is
   restored. Classify every change.
6. **Integration surface:** every consumer of line 25b (lines 25d, 33, 34,
   37 and anything else that requires it), each blocked line's reason and
   (disposition, code, missing), and a presentation probe of the sentence
   and question the filer sees for the unanswered yes/no and the
   unanswered amount.

Then write the closing declaration under a new "Track 0 adversarial
closure" heading in the plan. A row is PASS only if no counterexample
stands beside it. Repairs are switchable changes in prototype.py. Where a
fix cannot pass without an engine, schema or recording change, mark it
FAIL and stop.

## Deliverables

- f1099b-box4-only-evidence/track0-closure.md;
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
- Run foreground commands only.
- No push and no spawn. Do not edit packages/kernel/.
