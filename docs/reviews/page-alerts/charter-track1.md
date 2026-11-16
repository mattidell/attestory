# Charter: Track 1 of the line 6c and Schedule 1 alerts — core v92

Role: Builder. Source HEAD on milestone/page-alerts-2025.
Plan: docs/phases/engine-breadth/milestones/page-alerts.md. Read
Decisions 1-9 and "Track 0 adversarial closure". Evidence:
page-alerts-evidence/ (p0.md, track0-closure.md, prototype.py, track0.py
and their JSON). Precedent for the content build and tests:
tests/test_line12d_boxes_v90.py, tests/test_line12d_boxes_v90_package.py
and tests/test_preferential_base_reason_v91_package.py. Do not read
governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/, packages/schemas/ or packages/presentation/, or a
recording change.

## Build

1. **Content.** Six new versioned citizens in packages/content/tax/2025/,
   byte-identical to what Track 0's sibling variant built; never edit a
   published citizen.
   - `rule.form1040-line6c` v2 (publishes `not_checked`) and
     `form1040.line-6c` v2 (renders it).
   - The checked sibling on `social-security.line6c-checked`: its rule
     and its form field, on the line 6d pattern. Each of the two line 6c
     fields explains its inapplicable state in words that are true in
     both states, as the line 12d spouse fields do ("…or the box is the
     other checked/not-checked state"); if the Track 0 build says only
     "Not applicable." through a generic sentence, write the field's own
     sentence and say so as a deviation.
   - `citation.schedule1.top-entry` v1 and
     `schedule1.top-entry.form-field` v2.
2. **Core v92, registry v90, release v90** with
   `python3 -m tools.package_successor`. Add the v92 loader entries in
   packages/tax/loader.py carrying v91's unchanged, and extend any test
   or allowlist that enumerates cores or form fields (the v91 build
   touched tests/test_noncovered_sales_v78_switch.py).
3. **Full replay.** All 775 recorded lists on published v91 and published
   v92 with `python3 tools/recorded_replay.py`, CPU count minus one
   workers, in the foreground, part file outside the repo. Commit the
   classification: the target is 775 identical. Then the alert census on
   published v92: zero alerts on every computing return. Report wall
   times.
4. **Tests.**
   - A live module on published v92 through `live_coordinate_run`, the
     presentation projection and the saved page model, each distinct act
     list once: line 6c election not made, made and unanswered (the
     unanswered case leaves that fact out of its act list; no shared
     helper may answer it); the top entry at 0, at a personal-item loss
     and blocked; for each the field's disposition, render value,
     explain words, citations and the absence of the two alert causes.
     Hand values from the 2025 instructions are held whether or not a
     question remains.
   - One browser test on the precedent of the line 12d page test: a
     saved v92 page drawn in Chrome shows zero safe-render alerts and the
     words "not checked" on line 6c. Mark it as the line 12d one is
     marked.
   - The SSA-1099 guard as the follow-up measured it: closure left on the
     old horizon blocks line 6a and asks the closure question.
   - A fast package test: byte identity with the prototype, exactly the
     six members added or succeeded and the entrypoints moved, registry
     v90 add-only, the loader entries, v91 and earlier unchanged.

   Load evidence only through tests/evidence_loader.py. Keep every test
   under the 3.0 s fast-lane budget or `@pytest.mark.live` with a
   measured reason.
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
