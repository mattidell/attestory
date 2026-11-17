# Charter: repair of line 6b review findings

Role: Builder. Source HEAD on milestone/line6b-reason-2025. Plan:
docs/phases/engine-breadth/milestones/line6b-reason.md, Decisions 13-15.
Review: docs/reviews/line6b-reason/review.md. Do not read governance.

## Repairs

1. **L6B-R1.** Reword
   `input-question.ss-benefits-scope-no-puerto-rico-or-samoa-income` so
   it asks about the fact's whole class: any income of a bona fide
   resident of Puerto Rico or American Samoa in 2025, and on a joint
   return the spouse too, following the published sibling convention
   (Decision 8: asked about the thing; "no" means the `no-...` fact
   holds). Read the fact title and the 2025 instruction passage (local
   sources) and say in the plan why the new words are true and match the
   fact. This citizen is new on this branch, so edit its v1 bytes in
   place and rebuild core v93, registry v91 and release v91 with
   `python3 -m tools.package_successor` from published v92; nothing on
   main changes. Update the prototype identity check in the package test
   to name this one difference. Add the reviewer's counterexample (a
   bona fide resident with only mainland income) to the meaning
   evidence and to the live test: under the new words a truthful answer
   records the fact as the rule reads it.
2. **L6B-R2.** Slice source excerpts on physical newlines (not
   `str.splitlines()`), regenerate both question catalogs, and assert in
   the script that each excerpt contains its claimed passage.
3. **L6B-R3.** Describe the replay as selected-pin parity in the plan's
   Track 1 result and track1 evidence, pointing to the neighbour
   comparison for sentences and dispositions.
4. **Re-run what the bytes change touches.** The live and package tests,
   the neighbour comparison (parallel, report wall time), and the
   replay with `python3 tools/recorded_replay.py` (CPU count minus one
   workers; the question words do not reach the pin, so expect 775
   identical). Then `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Fill a
   "Repair result" paragraph under "Review and repair" in the plan.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only: never end your
  turn while a command is running. No push, no spawn. No edits under
  packages/kernel/, packages/derivation/, packages/schemas/ or
  packages/presentation/.
