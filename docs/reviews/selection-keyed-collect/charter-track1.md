# Charter: Track 1 of a selection path collecting a keyed family — core v86

Role: Builder. Source HEAD on milestone/selection-keyed-collect-2025.
Plan: docs/phases/engine-breadth/milestones/selection-keyed-collect.md.
Read Decisions 1-5 and "Track 0 adversarial closure". Proposed ADR:
docs/adr/0085-selection-collect-by-family.md (build to it; do not change
its status). Evidence in selection-keyed-collect-evidence/: engine.patch,
prototype.py, track0-closure.md, track0.py and outputs. Precedent: the
core-v75 and core-v76 switches in packages/tax/loader.py and their tests;
tests/test_f1099b_box4_only_v85.py and its package test. Do not read
governance.

Stop and report if anything needs an edit under packages/kernel/, an edit
to a published schema file, or a recording change.

## Build

1. **Schema.** Publish `rule-artifact.v16` (v15 with selection `paths`
   `minItems` 1) as a new file, append its checksum with
   `packages.kernel.schema_registry.write_manifest`, confirm the manifest
   diff only adds it, and thread v16 through the derivation enumerations
   that list v15. Run `pytest tests/test_schema_registry.py`.
2. **Engine.** Apply engine.patch's change properly: the package switch
   (named as in the ADR) in packages/tax/loader.py, on from
   core-calculations v86, and the validation and runner changes under
   packages/derivation/, each gated on the switch. Earlier cores unchanged.
3. **Content and package.** The box 4 subtotal v2 on rule-artifact.v16
   with one path and the default, byte-identical to prototype.py; core v86
   without `rule.f1099b-b4-amount-symbol`; registry v84 and release v84
   via `python3 -m tools.package_successor`; the v86 loader entries
   carrying v85's companion declaration and refusal maps.
4. **Tests.**
   - Engine unit tests for the switch: on v86 a path's own-family collect
     needs no `requires`; a foreign collect still must be listed; v85 and
     earlier keep the equality; a v16 one-path rule validates, a v15
     one-path rule does not.
   - A live module running the Track 0 cases on published core v86
     (unique act lists only), pinning line 25b, the subtotal, the absence
     of a publication under the amount id, and the explanation walk.
   - The 298 recorded v83 runs on published v86 against
     tests/fixtures/f1099b_backup_withholding_v83/expected.json directly,
     the 91 that v85 asks with the yes/no answered no. Do not copy them
     into a new fixture.
   - A fast package test: byte identity against the prototype, member
     edits, registry v84 add-only, loader entries.
   - Core v85 and earlier pinned unchanged.

   Load evidence harnesses under unique module names and never assign
   another module's globals. Keep every test under the 3.0 s fast-lane
   budget or `@pytest.mark.live` with a measured reason.
5. **Checks.** This is substrate work: run the full `pytest` (split into
   shards if needed, sum the counts), plus `pytest -m "not live"`,
   `python3 -m mypy`, `python3 tools/governance_lint.py` if present, and
   `python3 tools/envelope_scan.py --range github/main..HEAD`. Fill a
   "Track 1 result" section in the plan with counts, the 298-run result,
   fixture size, run count, and any deviation.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Run foreground commands only. No
  push, no spawn.
