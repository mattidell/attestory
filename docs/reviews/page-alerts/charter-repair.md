# Charter: repair after the review of the page alerts

Role: Builder. Source HEAD on milestone/page-alerts-2025. Read
docs/reviews/page-alerts/review.md (PA-1, PA-2, PA-3) and the plan's
"Review and repair" section. Core v92, registry v90 and release v90 are
not on main, so their files on this branch may be rebuilt; nothing at
v91 or earlier may change.

## Repair

1. **PA-1.** In `schedule1.top-entry.form-field.v2.json`, replace the
   `closure_backed_zero` explain with a sentence the closed empty
   personal-item family establishes: it speaks only of Form 1099-K box
   1a amounts for personal items sold, in the words of the closure
   question (`closure-mapping.f1099k.v3.json`), and is true on a return
   that received a Form 1099-K for something else. Check the field's
   other three explain strings against the same standard and say what
   you found. Field v1 stays as published.
2. **PA-2.** Give `form1040.line-6c` v2 and `form1040.line-6c-checked`
   labels that read as the two states of the one line 6c checkbox, on
   the wording pattern the line 12d and line 6d field pairs use. No page
   edit.
3. **Rebuild** core v92, registry v90 and release v90 from the changed
   citizens with `python3 -m tools.package_successor`; update
   prototype-derived byte checks so the package test locks the committed
   sentences and labels and names each intended difference from the
   prototype.
4. **Tests.** The live test requires the new zero sentence on the wage
   return and on a return whose Form 1099-K is not for a personal item
   if the published content reaches one (say so if it does not). The
   Chrome test also draws the election-made page and the
   personal-item-loss page and asserts zero `section-error` nodes in the
   whole DOM and the words "checked" and the loss sentence.
5. **Checks.** `pytest` on the touched test files, `pytest -m "not
   live"`, `python3 -m mypy`, `python3 tools/envelope_scan.py --range
   github/main..HEAD`. The replay pin does not hold these strings, so no
   replay. Add a "Repair result" paragraph under "Review and repair" in
   the plan.

Stop and report if anything needs an edit under packages/kernel/,
packages/derivation/, packages/schemas/ or packages/presentation/.

## Rules

- Synthetic demo.* only; no absolute or temp-directory paths in committed
  files, prose included.
- Commit after each numbered item, staging explicit paths, under
  `$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir);
  if held, retry every 10 s up to 5 min.
- Never --no-verify or a bare git stash. Foreground only: never end your
  turn while a command is running. No push, no spawn.
