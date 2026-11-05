# Track 1: show the knowable questions in round one (core v76)

Role: Builder. Source HEAD on milestone/all-questions-at-once-2025.
Plan: docs/phases/engine-breadth/milestones/all-questions-at-once.md (P0
result, Decisions). Evidence: all-questions-at-once-evidence/
p0-rounds-and-design.md, probe.py and prototype.py. Do not read governance.

1. **Content.** Successor rules so each unconditional family P0 marked
   knowable (the two Form 1099-B parent families, the six wash-sale
   companions, the W-2 wage family, Form 1099-DIV box 7) is a `requires` of
   the consumer that today hides it, through a closure-check rule whose
   `when` is a single `require_closed`. Reuse existing schemas and
   operations. Published files immutable; only new versions.
2. **Evaluator.** Behind a switch on from core-calculations v76 (add it
   beside `unconfirmed_family_names_closure_question` in
   packages/tax/loader.py, same keying): when an `any` arm raises because a
   `count` is blocked, and a compared set in that arm already has a member,
   also record the `ref`s of the later arms as missing on the blocked row.
   Values never change; only which missing inputs a blocked row names.
   Switch off: byte-identical.
3. Core v76, registry v74, release v74 with `tools/package_successor.py`;
   loader companion entry shared with v75.
4. tests/test_all_questions_at_once.py through `live_coordinate_run`,
   reusing P0's round loop: the six starts' round counts on v76 match P0's
   prototype (or explain each difference); the W-2 box 2 and Form 1099-DIV
   box 4 amounts appear in round one where P0 says; a return with no W-2 is
   not asked box 2; each truly conditional question still appears only
   after its answer; complete returns publish v75's amounts and render the
   same presentation face; v75 runs byte-identical to today.
5. Inner loop, `pytest -m "not live"`, `python3 -m mypy` on every touched
   file, then the full suite (substrate). Do not regenerate an earlier
   core's golden; if one moves, stop and report.
6. Evidence note all-questions-at-once-evidence/track1.md: successors,
   switch, round table before and after, suite lines.

Stop if this needs a schema or a new expression operation. Do not edit
packages/kernel/ (a parallel milestone owns it). Synthetic demo.* only; no
absolute paths in committed files. Commit incrementally with explicit paths
under `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
if held, retry every 10 s up to 5 min, never remove another holder's lock);
never --no-verify; never bare git stash. Foreground commands only; no
pgrep or sleep waiters. No push or spawn.
