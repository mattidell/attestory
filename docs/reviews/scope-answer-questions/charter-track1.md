# Track 1: questions for the scope answers and filing status

Role: Builder. Source HEAD on milestone/scope-answer-questions-2025.
Plan: docs/phases/engine-breadth/milestones/scope-answer-questions.md
(P0 result, Decisions after P0, Tracks). Table and prototype:
scope-answer-questions-evidence/p0-questions.md and
filing-status-projection.diff. Do not read governance or unrelated
proposals.

1. Trace `direct-ftc-scope.no-schedule2-regular-tax-add` in content and
   apply decision 2. Report what you found.
2. Write the `input-question.v1` citizens: one per fact, carrying its
   group's sentence verbatim from section 3, with EIC1 changed per decision
   1, plus filing status.
3. Apply the filing-status projection change (binding map from
   `resolved.package["input_bindings"]` into the projection); earlier cores
   unchanged.
4. Core v73, registry v71, release v71 with `tools/package_successor.py`;
   the v73 companion entry in `packages/tax/loader.py`.
5. Tests through the real coordinator and projection: one case per group
   (the question attaches under each line it holds), filing status, a group
   question shown once when several of its facts are missing, a mixed line
   with an amount question, and v68-v72 presentation models byte-identical.

Only successors; never edit a published schema, citizen, package or
checksum. `packages/derivation/` is touched: run `python -m mypy`, the new
tests, `tests/test_input_questions.py`, `tests/test_schema_registry.py` and
the FULL suite before handoff. Synthetic demo.* only; no absolute paths.
Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir) every
time; never --no-verify; never bare git stash. Foreground commands only. No
push, no spawn. Stop on any schema or kernel change.
