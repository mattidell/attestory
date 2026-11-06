# Charter: P0 of statement withholding pairing

Role: Builder. Source HEAD on milestone/statement-withholding-pairing-2025.
Plan: docs/phases/engine-breadth/milestones/statement-withholding-pairing.md
(read it whole). Do not read governance.

## Scope

On core v76 (`package.core-calculations.v76.json`, registry
`published-packages.v74.json`, release
`demo.release.sli-worksheet-integration.2025.v74.json`), through
`live_coordinate_run` only:

1. **Reproduce.** For each of Form 1099-INT, 1099-DIV, 1099-R (IRA), 1099-G
   and SSA-1099, build the plan's cases with synthetic `demo.*` findings:
   two statements, one answered and one not, where the count still passes
   (a second withholding member on the answered statement, or a statement
   with withholding and no income amount); the cross-form case; a statement
   recorded only through another box. For each, record what line 25b
   publishes or blocks, and the hand-computed right answer. If admission,
   identity or the statement key already refuses a case, say so and show
   the refusal: an unreachable case is not a defect.
2. **Key.** What ties a withholding member to its statement (statement
   identity, horizon, subject), and whether two members for one statement
   and box can coexist at all.
3. **Operations.** Read `shared_key_count` and `link_coverage` in
   `packages/derivation/evaluator.py` and their existing uses. Can either,
   or any existing operation, express "every statement with an income
   amount has its own withholding answer"? Give the expression if so.
4. **Design.** Prototype the smallest successor set in a scratch copy under
   the evidence directory (never under packages/content), run the cases on
   it, and count what changes for answered returns, fixtures and goldens.
5. **Line 25a.** Does W-2 box 2 have the same gap?

Stop and report if the fix needs an engine, schema or operation change; give
the cause and the smallest change.

## Deliverables

docs/phases/engine-breadth/milestones/statement-withholding-pairing-evidence/:
p0-reproduce-and-design.md (cases table, key, operations, design, line 25a,
and a one-paragraph recommendation), the probe script and its JSON output,
the prototype and its output. Fill the plan's "P0 result" section (a short
summary that links the evidence). No production, test or content edits.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn. Do not edit packages/kernel/.
