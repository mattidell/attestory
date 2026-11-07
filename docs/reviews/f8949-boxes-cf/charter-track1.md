# Charter: Track 1 of sales without a Form 1099-B — core v80

Role: Builder. Source HEAD on milestone/f8949-boxes-cf-2025.
Plan: docs/phases/engine-breadth/milestones/f8949-boxes-cf.md: read
Decisions 1-7 and "Track 0 adversarial closure". Evidence is in
f8949-boxes-cf-evidence/: track0-closure.md, cf_prototype.py with every
`REPAIRS` switch on, cf-prototype-rules/ and track0.py. Do not read
governance.

Stop and report if the build needs anything outside content, tests and
the per-core loader entries. That covers any edit under
packages/kernel/, packages/derivation/ or packages/schemas/, and any
change to recording.

## Build

1. **Successor citizens.** Bring the scratch v80 successor set from
   cf-prototype-rules/ into packages/content/tax/2025/ as new versioned
   citizens. Never edit a published citizen. The set includes:
   - the box C and F families, subtotals and sale entities;
   - the new grouped question and its input question;
   - the new in-class answer, with "entered only once" in its wording;
   - Schedule D lines 2, 3, 9 and 10, with the missing-amount, count,
     amount-agreement and admission checks;
   - lines 7, 15, 16 and 21 where changed;
   - line 7a and the preferential base v8;
   - the Form 8949 and Schedule D attachment successors;
   - form fields with `explain` text in the line-explanations wording
     standard;
   - the four missing-amount questions;
   - citations.
2. **Core v80, registry v78 and release v78**, made with
   `python3 -m tools.package_successor`. Then write the per-core entries
   in packages/tax/loader.py, which P0 patched in-process. Take the
   covered-flag refusal map and companion declarations from v79.
3. **Tests through the real coordinator and the presentation model:**
   - every case in track0-output.json with its hand values, asserting
     each attachment disposition and that no blocked line shows an empty
     reason;
   - the current-core returns under the new "no", unchanged from v79
     except the accepted blocks (Decisions 2 and 5), with the
     current-core expectation for `boundary_no_without_member` updated;
   - v79 and earlier pinned unchanged.

   Keep new slow tests honest: `@pytest.mark.live` with a comment, or
   under the 3.0 s fast-lane budget.
4. **Checks:** run `pytest -m "not live"`, then the full `pytest`, then
   `python3 -m mypy` as CI runs it. Then fill the plan's "Track 1 result"
   with case counts and any deviation from the prototype.

## Rules

- Synthetic demo.* only, and no absolute paths in committed files.
- Published schemas and citizens are immutable: successors only.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir).
  If the lock is held, retry every 10 s for up to 5 min.
- Never use --no-verify or a bare git stash.
- Run foreground commands only, with no pgrep or sleep waiters.
- No push and no spawn.
