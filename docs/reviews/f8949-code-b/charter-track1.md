# Charter: Track 1 of broker basis corrections — core v81

Role: Builder. Source HEAD on milestone/f8949-code-b-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-code-b.md. Read
Decisions 1-8 and "Track 0 adversarial closure". The evidence is in
f8949-code-b-evidence/: track0-closure.md, codeb_prototype.py with every
`REPAIRS` switch on, and codeb_track0.py. Precedent for the build shape:
tests/test_no1099b_sales_v80.py and tests/test_no1099b_sales_v80_package.py.
Do not read governance.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/ or packages/schemas/, or a recording change.

## Build

1. **Decision 6, on the scratch prototype first.** Add the four inherited
   v80 fixes as further `REPAIRS` switches:
   - zero-proceeds code W rows and box B rows require their attachments;
   - cross-term exclusivity between covered and noncovered families, so
     one transaction is never counted twice;
   - a covered sale flagged `taxpayer_side_adjustment` "yes" blocks with
     a true reason.

   Rerun the Track 0 harness. List every v80 return whose result changes.
   Each change must be one of these four patterns; anything else is a
   defect. Every hand value must still hold. If a fix needs more than
   content, park it, note it in the plan and continue.
2. **Successor citizens.** Bring the successor set into
   packages/content/tax/2025/ as new versioned citizens. Never edit a
   published citizen. Generate them from the prototype and keep them
   byte-identical to it.
3. **Core v81, registry v79 and release v79**, made with
   `python3 -m tools.package_successor`. Add the per-core v81 entries in
   packages/tax/loader.py, carrying v80's companion declaration and refusal
   map, plus any code B pairs.
4. **Tests.**
   - A live module running every Track 0 case and every v80 return
     through `live_coordinate_run` and the presentation model. Pin the
     lines, the attachment dispositions, each blocked line's reason
     sentences, and the (disposition, code, missing) of the rows Track 0
     watches.
   - A fast package test: byte identity against the prototype, the exact
     member edits, registry v79 add-only, and the loader entries.
   - A test pinning each new input question's words against its
     proposition.
   - v80 and earlier pinned unchanged.

   Load evidence harnesses under unique module names. Drop exact
   duplicate cases. Keep every test either under the 3.0 s fast-lane
   budget or `@pytest.mark.live` with a reason.
5. **Checks.** Run `pytest -m "not live"`, then the full `pytest`, then
   `python3 -m mypy`. Fill the plan's "Track 1 result" section with case
   counts, the changed v80 returns, and any deviation.

## Rules

- Synthetic demo.* only, and no absolute or temp-directory paths in
  committed files.
- Published citizens and schemas are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only.
- No push and no spawn.
