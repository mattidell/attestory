# Charter: Track 0 adversarial closure of a selection path collecting a keyed family

Role: Builder. Source HEAD on milestone/selection-keyed-collect-2025.
Plan: docs/phases/engine-breadth/milestones/selection-keyed-collect.md
(read it whole, including the P0 result and Decisions 1-5). Proposed ADR:
docs/adr/0085-selection-collect-by-family.md. Evidence:
selection-keyed-collect-evidence/. Gate: `PROJECT_PLANNING.md`, "Track 0
Adversarial Closure Gate" (read that section and its closing paragraphs
whole). Precedent: f1099b-box4-only-evidence/track0-closure.md and
track0.py. Do not read governance.

## Scope

Every claim must come from a run saved in a committed JSON file and named
by case id. Work against the P0 patch in a temporary copy, as P0 did;
never edit tracked files under packages/.

1. **Authority-lifecycle table** for the box 4 amounts, the subtotal, the
   retired stand-in, and the switch (package id and version).
2. **Empty/nonempty matrix:** the subtotal with no amount, one, two, a
   zero; under the switch on (v86) and off (v85); and a one-path v16 rule
   with and without a default.
3. **Late-member traces:** an amount added, superseded, withdrawn, and a
   second statement added, each after a first publication.
4. **Claim reuse:** line 25b and its consumers, and the explanation walk
   of line 25b and the subtotal: the walk no longer shows 0 under the
   amount id beside a recorded amount, and shows each recorded amount.
5. **Neighbour dependency diff:** every selection rule on v85 (the 32
   with an inert path, line 2b v8, and the rest) validates and runs the
   same with the switch on; every core v2-v85 loads byte-identically with
   the patch applied; the 596 recorded variants are identical on v85 and
   v86 apart from the retired stand-in.
6. **Integration surface:** schema registry (v16 add-only), package
   validation, the runner's wait, presentation of line 25b and the
   subtotal; and an adversarial try: a v16 one-path rule whose path
   collects a family other than its activity family must still list that
   collect in `requires` or be rejected.

Then write the closing declaration under a new "Track 0 adversarial
closure" heading in the plan. A row is PASS only if no counterexample
stands beside it. Where a fix cannot pass without a kernel edit, mark it
FAIL and stop.

## Deliverables

- selection-keyed-collect-evidence/track0-closure.md;
- track0.py (unique module name, mutates no other module's globals) and
  its JSON outputs;
- the plan's "Track 0 adversarial closure" section.

No production, schema, content or test edits.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
  retry every 10 s for up to 5 min if held).
- Never use --no-verify or a bare git stash.
- Run foreground commands only. No push and no spawn. Do not edit
  packages/kernel/.
