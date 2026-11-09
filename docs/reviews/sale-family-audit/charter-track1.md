# Charter: Track 1 of the sale family audit — core v82

Role: Builder. Source HEAD on milestone/sale-family-audit-2025.
Plan: docs/phases/engine-breadth/milestones/sale-family-audit.md. Read
Decisions 1-6 and "Track 0 adversarial closure". The evidence is in
sale-family-audit-evidence/: track0-closure.md, prototype.py with every
`REPAIRS` switch on, track0.py, tables.py and the v81 rerun scripts.
Precedent for the build shape: tests/test_code_b_sales_v81.py and
tests/test_code_b_sales_v81_package.py. Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Decision 2, on the scratch prototype first.** Reword the Exception 1
   questions so each "yes" means what its fact's "yes" means. Add it as a
   `REPAIRS` switch, rerun the Track 0 harness, and confirm every gate row
   and every v81 classification still holds.
2. **Successor citizens.** Bring the successor set into
   packages/content/tax/2025/ as new versioned citizens, generated from
   the prototype and byte-identical to it. Never edit a published citizen.
3. **Core v82, registry v80 and release v80**, made with
   `python3 -m tools.package_successor`. Add the per-core v82 entries in
   packages/tax/loader.py, carrying v81's companion declaration, refusal
   map and code B pairs.
4. **Tests.**
   - A live module running every Track 0 case and every v81 return through
     `live_coordinate_run` and the presentation model, in both answer
     modes. Pin the lines, the attachment dispositions, each blocked line's
     reason sentences, and the (disposition, code, missing) of the rows
     Track 0 watches. Harness builders record each sale's rows on that
     sale's own transaction (Decision 3).
   - The audit itself as a test: tables.py's fact-field and consumer audit
     over core v82, failing if a sale fact field is read by no consumer
     without a recorded reason.
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v80 add-only, and the loader entries.
   - A test pinning each new or reworded input question's words against
     its proposition.
   - v81 and earlier pinned unchanged.

   Load evidence harnesses under unique module names and never assign
   another evidence module's globals at import (the #264 leak: CI runs
   several modules in one process). Prefer running v81 harnesses in a
   subprocess, as P0 did. Keep every test either under the 3.0 s fast-lane
   budget or `@pytest.mark.live` with a measured reason.
5. **Checks.** Run `pytest -m "not live"`, then the full `pytest`, then
   `python3 -m mypy`. Fill the plan's "Track 1 result" section with case
   counts, the changed v81 returns, and any deviation.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files, prose included.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
