# Track 1: line 25b waits for each statement's withholding answer

Role: Builder. Source HEAD on milestone/statement-withholding-answer-2025.
Plan: docs/phases/engine-breadth/milestones/statement-withholding-answer.md
(P0 result, Decisions, Tracks). Design and hand values:
statement-withholding-answer-evidence/p0-trace-and-design.md. Do not read
governance or unrelated proposals.

Build, as P0 designed and the foreman decided (`gte`):

1. `tax.us.2025.rule.form1040-line25b` v4 in `rule-artifact.v4`, a successor;
   v3 untouched.
2. Core v71, registry v69, release v69 with `tools/package_successor.py`;
   inspect the generated diff. The v71 entry in
   `domain_package_companion_declarations()` (`packages/tax/loader.py`), with
   a test that pins it.
3. Tests through the real coordinator (`tests/helpers/current_core_returns.py`):
   each of the five families unanswered (blocks `DEPENDENCY_ABSENT` naming
   that family's withholding fact; lines 24 and 25a publish, 25d and 33-37 do
   not); the same with $0 (every published value equal to v70); two Forms
   1099-G, one unanswered; joint, one spouse unanswered; no Form 1099; the
   surplus withholding-only answer (equal to v70); a v70 return adopted onto
   v71 (asked the amount, then the closure again; then v70's numbers); v70
   unchanged for the unanswered case. Keep the module's lane honest (mark it
   live if it drives the coordinator).
4. Report what the explanation and presentation say for the v71 block,
   without changing either.

Only successors; never edit a published schema, rule, package or checksum.
`packages/tax/` is touched: run `python -m mypy`, the new tests, the
package/registry tests and the fast lane; the foreman runs CI. Synthetic
demo.* data only; no absolute paths committed. Commit with explicit paths
under `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
never --no-verify; never bare git stash. No push, no spawn. Stop if anything
needs a kernel, schema, operation or engine change.
