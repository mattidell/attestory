# Charter: repair after the noncovered-sales review

Role: Builder. Source HEAD on milestone/noncovered-sales-2025. Review:
docs/reviews/noncovered-sales/review.md (verdict ready, one should-fix).
Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md. Do not
read governance. Do not edit packages/kernel/.

Core v79, registry v77 and release v77 are unmerged on this branch, so
their new citizens may be corrected in place; regenerate checksums with
`python3 -m tools.package_successor` (or update the registry entry and the
release `package_registry_sha256` exactly as that tool computes them).
Never change a citizen that is on `github/main`.

## Scope

1. **False explain text on Schedule D lines 2 and 9.** `closure_backed_zero`
   says the filer denied sales of that term, but the same disposition is
   selected when the shared answer is yes and that term has no member
   (live long-term gain page shows it on line 2). Rewrite both so the
   sentence is true in both cases, e.g. that no sale of that term whose
   basis was not reported is recorded and the noncovered-sales answer
   confirms the list is complete. Also check each `blocked` explain on
   lines 2 and 9 and the six subtotals' fields: "waiting for the basis of
   a sale" is false when the line blocks because the shared question is
   unanswered, a "yes" went stale, or a covered flag refusal applies. Make
   every blocked sentence true for every code that reaches it (read the
   rule's `when`), in the wording standard of
   docs/phases/engine-breadth/milestones/line-explanations.md.
2. **Schedule D attachment on a pure noncovered return.** The reviewer saw
   the Schedule D attachment `guard_inapplicable` while lines 2, 9 and 16
   publish on a return whose only sales are noncovered. A return with a
   Form 8949 box B or E sale must attach Schedule D. Diagnose
   `attachment.schedule-d.v7` (its applicability and `when`), fix it, and
   assert the attachment disposition in the lt_gain, st_loss and wash
   cases, and that a wage return under one "no" is unchanged.
3. **covered-ltcg in the refusal map.** packages/tax/loader.py names
   `covered-ltcg-txn`, which core v79 does not publish. Drop it from the
   v79 map, and make ADR 0084 and the plan name the four objects this
   package refuses.
4. **Schedule D line 7** is missing from the test digest; add it to every
   case.
5. Run the touched test modules, `pytest -m "not live"`, and
   `python3 -m mypy` as CI runs it. The full suite runs only if a change
   touches packages/derivation/. Add a short "Repair" note under the
   plan's "Track 1 result".

## Rules

Synthetic demo.* only; no absolute paths in committed files. Commit after
each item with explicit paths under
`$(git rev-parse --git-dir)/collaboration-commit.lock` (mkdir … rmdir;
retry every 10 s up to 5 min if held); never --no-verify; never bare git
stash. Foreground commands only. No push or spawn.
