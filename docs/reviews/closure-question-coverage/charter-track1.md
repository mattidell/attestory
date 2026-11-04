# Track 1: unconfirmed families name their question (core v75)

Role: Builder. Source HEAD on milestone/closure-question-coverage-2025.
Plan: docs/phases/engine-breadth/milestones/closure-question-coverage.md
(P0 result, Decisions). Evidence: closure-question-coverage-evidence/
p0-survey-and-design.md and probe.py. Do not read governance.

1. **Version switch first.** Find how the engine already varies behaviour by
   core package version without a schema change (for example a companion
   declaration in packages/tax/loader.py keyed by package id and version,
   as earlier successors added). Design one switch, on from core v75, that
   both changes below read. If no switch is possible without a schema or
   published-file change, stop and report before editing.
2. **Engine.** With the switch on, an unadmitted constrained family's
   synthesized member validation (`_evaluate_family_validation`, P0 §3)
   records `SOURCE_SET_UNCLOSED` naming the family id, as `require_closed`
   would, instead of `DEPENDENCY_ABSENT`. Admitted families validate as
   today. Switch off: unchanged.
3. **Projection.** With the switch on, a blocked selection line whose
   roots include an unconfirmed family with a closure question names that
   question beside its selection reason (Form 1099-K with one member:
   sch1-10 and sch1-top). Sorted, distinct, as the existing walk does.
   Switch off: unchanged.
4. Core v75, registry v73, release v73 with `tools/package_successor.py`
   (identical members to v74 unless the switch needs a declaration), and
   any loader entry.
5. tests/test_closure_question_coverage.py through `live_coordinate_run`:
   each wash-sale family unconfirmed, with and without members, names its
   question on v75 on every line P0 counted; Form 1099-K with one member
   names both sentences on the two lines; a sample of the other 48 families
   unchanged on v75; every confirmed return identical to v74 in published
   amounts and presentation; the same cases on v74 byte-identical to today.
6. Inner loop, `pytest -m "not live"`, `python3 -m mypy` on touched files,
   then the full suite (substrate change). Do not regenerate an earlier
   core's golden; if one moves, stop and report.
7. Evidence note closure-question-coverage-evidence/track1.md: the switch,
   the changes, counts of lines gaining a question, suite lines.

Synthetic demo.* only; no absolute paths in committed files. Commit
incrementally with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir; if
held, retry every 10 s up to 5 min, never remove another holder's lock);
never --no-verify; never bare git stash. Foreground commands only; no
pgrep or sleep waiters. No push or spawn.
