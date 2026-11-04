# Repair 1: wording after the fresh-reader review

Role: Builder. Source HEAD on milestone/scope-answer-questions-2025.
Plan: "Decisions (after review)". Findings:
docs/reviews/scope-answer-questions/review-track1.md (R1, W1-W9, notes).

1. Apply decisions 2-5 to the citizens' sentences. The citizens are new on
   this branch: edit them in place, keeping one sentence per group across
   its facts. Owner rule unchanged: "yes" means present.
2. For L2A2, L2A3, FTC12 and DEP1, trace what the reading rule and the form
   say first; commit the trace as
   scope-answer-questions-evidence/repair1-trace.md, then word each to it.
   Check S1A's "lines 24a through 24z" and FTC12's line numbers against the
   2025 form text in the repo's sources; if the sources do not settle it,
   say so in the trace and use the wording the rule supports.
3. Regenerate core v73, registry v71, release v71 from the change set with
   `tools/package_successor.py` (they are unpublished on this branch);
   confirm the registry still only adds against v70.
4. Decision 6: a test asserting each fact's polarity flag against the rule's
   supported value. Fix the shell-expansion damage in p0-questions.md and
   update its section 3 table to the final sentences.
5. Run `python -m mypy`, tests/test_scope_answer_questions.py,
   tests/test_input_questions.py, tests/test_schema_registry.py and the fast
   lane. The FULL suite only if packages/derivation/ changes.

Only successors against main; never edit anything published on main.
Synthetic demo.* only; no absolute paths. Commit with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` every time; never
--no-verify; never bare git stash. Foreground commands only (split long
runs). No push, no spawn. Report the final 40 (or 41) sentences.
