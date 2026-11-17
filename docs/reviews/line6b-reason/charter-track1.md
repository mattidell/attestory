# Charter: Track 1 of line 6b naming why it is blocked — core v93

Role: Builder. Source HEAD on milestone/line6b-reason-2025, rebased onto
main after page-alerts (core v92, registry v90, release v90) merged.
Plan: docs/phases/engine-breadth/milestones/line6b-reason.md. Read
Decisions 1-12 and "Track 0 adversarial closure". Evidence:
line6b-reason-evidence/ (p0.md, track0-closure.md, prototype.py,
track0.py and their JSON). Precedent for the content build and tests:
tests/test_page_alerts_v92.py, tests/test_page_alerts_v92_package.py and
tests/test_preferential_base_reason_v91_package.py. Do not read
governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/, packages/schemas/ or packages/presentation/, or a
recording change.

## Build

1. **Content.** Ten new `input-question.v1` citizens in
   packages/content/tax/2025/, byte-identical to the P0 prototype's
   (`prototype-build.json` lists them); never edit a published citizen.
2. **Core v93, registry v91, release v91** with
   `python3 -m tools.package_successor` on published v92, adopting the
   ten as members and entrypoints exactly as the prototype did on v91.
   Add the v93 loader entries in packages/tax/loader.py carrying v92's
   unchanged, and extend any test or allowlist that enumerates cores
   (the v92 build touched tests/test_noncovered_sales_v78_switch.py).
   Say in the plan if the v92 base changed anything the prototype
   assumed.
3. **Full replay.** All 775 recorded lists on published v92 and
   published v93 with `python3 tools/recorded_replay.py`, CPU count minus
   one workers, in the foreground, part file outside the repo. Commit the
   classification: the target is 775 identical. Then rerun Track 0's
   neighbour comparison (track0.py, parallel) on v92 vs v93: zero value,
   disposition or required-answer changes; every added question on a
   field already blocked on its fact. Report wall times.
4. **Tests.**
   - A live module on published v93 through `live_coordinate_run`, the
     presentation projection and the saved page model, each distinct act
     list once: each of the ten facts left out alone (line 6b blocked,
     shows exactly that question, no generic blocked text); one scope
     pair (both questions on line 6b); one separate-filing scope + living
     apart pair (line 6b asks the scope question, line 6d asks living
     apart, both on the page); benefits with every fact answered (line 6b
     publishes the hand value from the 2025 worksheet, no question); a
     separate filer with no benefits and living apart unanswered (refund
     unchanged, line 6d asks the question). Facts are set by the
     published convention (Decision 8); a left-out fact is absent from
     the act list, never removed by a shared helper.
   - One browser test on the page-alerts precedent: a saved v93 page in
     Chrome draws line 6b's question and shows zero safe-render alerts.
     Mark it as that one is marked.
   - A fast package test: byte identity with the prototype, exactly the
     ten members and entrypoints added, registry v91 add-only, the loader
     entries, v92 and earlier unchanged.

   Load evidence only through tests/evidence_loader.py. A harness that
   imports a sibling by bare name must have that sibling loaded by path
   under that name first (see `_line12d_names` in
   tests/test_page_alerts_v92.py); run each new module once with an
   unrelated evidence directory first on PYTHONPATH to prove it. Keep
   every test under the 3.0 s fast-lane budget or `@pytest.mark.live`
   with a measured reason.
5. **Checks.** `pytest` on the new modules and every test file touched,
   `pytest -m "not live"`, `python3 -m mypy`,
   `python3 tools/envelope_scan.py --range github/main..HEAD`. CI
   `verify` is the gate for the full suite. Fill a "Track 1 result"
   section in the plan, with deviations.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only: never end your
  turn while a command is running. No push, no spawn.
