# Charter: Track 1 of line explanations

Role: Builder. Source HEAD on milestone/line-explanations-2025.
Plan: docs/phases/engine-breadth/milestones/line-explanations.md (read it
whole: P0 result and Decisions). P0 evidence:
line-explanations-evidence/p0-inventory-and-draft.md, its probe and
prototype. Do not read governance.

## Scope

1. **Wording.** For each of the 36 fields in Decision 1, write the new
   sentences to Decision 3's standard. Read the rule each field binds (its
   addends, `when`, blocked `missing`) so every sentence is true for every
   return that selects it. Only the texts Decision 2 names change.
2. **Successors.** A new version of each field (same schema as its v77
   version), core v78, registry v76 and release v76 with
   `tools/package_successor.py`, and a `packages/tax/loader.py` entry
   sharing v77's companion declaration. Never edit a published file.
3. **Wording check.** A test that loads v78's pinned fields and fails on
   any explain text a field's rule can select that is one of the 37 v77
   generic sentences, contains "derived finding", "closure", "honest",
   "guard", "route" or "calculation comes to zero", or contains an
   internal id. Put the banned list in the test, not in content.
4. **Cases.** `tests/test_line_explanations.py`, through
   `live_coordinate_run` and the presentation projection on v78: the
   plan's cases (wages-only, an unanswered input, a guard that does not
   apply, a closed-empty family, a return using Schedule D). Each shows
   the new sentence in its section, and every value and disposition is
   equal to v77's on the same findings. v77 and earlier byte-identical.
5. **Evidence.** `line-explanations-evidence/track1.md`: a table of every
   changed text (field, disposition, v77, v78), the cases, and the suite
   lines. Fill the plan's "Track 1 result" section.
6. **Run** mypy on changed files, the fast lane, then the full suite.

## Stop conditions

Stop and report if a sentence cannot be made true for every return that
selects it without a rule, schema, projection or page change, if a
published schema or manifest entry would change, or if an earlier core's
golden or byte output moves. Do not edit `packages/kernel/`.

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only; no pgrep or sleep waiters. No push or
spawn.

## Repair (after review)

Review: line-explanations-evidence/review.md. Fix every required and
recommended finding, in successor files not yet published outside this
branch (the v78 field versions may be edited in place before merge).

- A zero that can come from rounding says so ("add to less than a
  dollar" or "round to zero"), not "add to zero".
- A blocked text a static sentence cannot make exact names the line's
  inputs as a group ("one of the amounts this line adds") rather than a
  list that can be wrong or names filled lines; never an input a filer
  cannot supply (the rounding rule).
- Guards say plainly what the filer said or must say, with no double
  negative: for an absence question, "This line is computed only when you
  have no ... . You have not answered that question, or you said you
  have one." Line 22 names Form 4972 too.
- Line 16 and Schedule 3 line 1 guards: at most two short sentences.
  Name the case in plain words (for Schedule 3 line 1, that the return is
  not one where the credit can be claimed without Form 1116, and that the
  questions on that page say which condition) and never assert a
  condition that may be true.
- The wording test also fails on more than two sentences and on the
  double-negative pattern "not say that you have no". Add a case for each
  required finding through `live_coordinate_run` that shows the new
  sentence.

Update track1.md's text table and the plan's Track 1 result, run the
fast lane and the changed tests, and record a "Review dispositions"
section in the plan: each finding and what was done.
