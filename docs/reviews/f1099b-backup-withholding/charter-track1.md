# Charter: Track 1 of Form 1099-B backup withholding — core v83

Role: Builder. Source HEAD on milestone/f1099b-backup-withholding-2025.
Plan: docs/phases/engine-breadth/milestones/f1099b-backup-withholding.md.
Read Decisions 1-5 and "Track 0 adversarial closure". The evidence is in
f1099b-backup-withholding-evidence/: track0-closure.md, prototype.py (the
`decided` design; the `bridge_v82_no` repair is NOT taken), track0.py and
its JSON outputs. Precedent for the build shape:
tests/test_sale_family_audit_v82.py and
tests/test_sale_family_audit_v82_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Successor citizens.** Bring the decided v83 set into
   packages/content/tax/2025/ as new versioned citizens, generated from
   prototype.py and byte-identical to it: the box 4 amount fact type and
   its bundle, its input question, its source family, line 25b v7 and its
   form field. Never edit a published citizen. The v82 yes/no box 4
   question and fact leave the v83 core (no rule reads them).
2. **Core v83, registry v81 and release v81**, made with
   `python3 -m tools.package_successor`. Add the per-core v83 entries in
   packages/tax/loader.py, carrying v82's companion declaration (all
   scalar presence pairs) and refusal maps. If the box 4 amount needs a
   presence pair with its statement, add it the way v82 added the
   covered pairs.
3. **Tests.**
   - A live module running every Track 0 case and every one of the 213
     returns through `live_coordinate_run` and the presentation model on
     core v83. Pin lines 25b, 33, 34, 35a and 37, the attachments, each
     blocked line's reason sentences and the watched rows. Also pin, for
     a sample of the 150 changed returns, that answering box 4 as $0
     restores v82's values exactly. Keep it lean: no run that repeats a
     sibling's result.
   - Extend the committed sale-fact audit (sale-family-audit-evidence/
     tables.py) to core v83 so the box 4 amount counts as read and the
     retired yes/no box 4 answer is not required.
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v81 add-only, and the loader entries.
   - A test pinning the new question's words against its proposition.
   - Core v82 and earlier pinned unchanged.

   Load evidence harnesses under unique module names and never assign
   another module's globals. Keep every test under the 3.0 s fast-lane
   budget or `@pytest.mark.live` with a measured reason.
4. **Checks.** Run `pytest -m "not live"`, then the full `pytest` (split
   into shards if one command is too long, and sum the counts), then
   `python3 -m mypy`, and `python3 tools/envelope_scan.py --range
   github/main..HEAD`. Fill the plan's "Track 1 result" section with case
   counts, the changed v82 returns by class, and any deviation.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. No push, no spawn.
