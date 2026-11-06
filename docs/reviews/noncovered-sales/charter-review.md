# Charter: fresh-reader review of noncovered sales

Role: Reviewer. Source HEAD on milestone/noncovered-sales-2025, diff
against `github/main`. Plan: docs/phases/engine-breadth/milestones/noncovered-sales.md
(read it whole). You have not seen the build; keep it that way — judge
from the committed code, content and tests, not from the builder's
summaries. Do not read governance. Do not edit anything except your
review file.

## Questions

1. **Tax correctness, computed by hand.** From the 2025 Form 8949 and
   Schedule D instructions (local sources the citations name), compute
   independently: one noncovered long-term gain; one noncovered short-term
   loss (the $3,000 limit on line 21); a noncovered sale with a code W
   adjustment; one covered and one noncovered sale of each term on the
   same return. Then run each through the real coordinator on core v79
   with synthetic `demo.*` findings and compare every line (Schedule D
   lines 1a, 2, 7, 8a, 9, 15, 16, 21; Form 1040 lines 7a, 15, 16; Form
   8949 boxes B and E). The committed tests assert the scratch digest;
   say whether any expected value there is wrong.
2. **Engine.** Read the grouped-closure admission (marshal.py,
   source_authority.py, runner.py, package_validation.py, both loaders).
   Is the shared answer counted once? Does "no" admit only zero-member
   families, and does a member added after the current answer strip
   exactly that family (Decision 8)? Can any path admit a family it should
   not, or let one answer satisfy a mapping it is not listed in? Does the
   covered-flag refusal (Decision 9) fire on every covered sale object and
   only on v79? Is everything behind the package switch, with core v78 and
   earlier byte-identical?
3. **Schemas.** Are `source-closure-mapping.v4` and `artifact-package.v41`
   new files with add-only manifest entries? Did any published schema or
   citizen change bytes (`git diff github/main --stat` over
   packages/schemas and packages/content)?
4. **ADR 0084.** Is every sentence true of the code? Does it contradict
   or silently revise ADR-0014, ADR-0017, ADR-0079 or ADR-0082 (read their
   full text only where you check it)?
5. **What the filer sees.** For every blocked line in the cases, is the
   page reason non-empty and true? Is every new `explain` sentence true of
   its rule's `when`? Is the shared question asked once?
6. **Gaps.** The scalar-recorded-without-its-sale case is tested only by
   calling the companion enforcer directly. Run it through the live
   coordinator and report what the page shows.
7. **Data safety.** `python3 tools/envelope_scan.py --range github/main..HEAD`;
   no absolute local paths in committed files.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/noncovered-sales/review.md: each finding with file:line, a
reproduction, severity (blocking / should-fix / note), and the fix you
would make. End with a verdict: ready, or the blocking list. Commit it
(explicit path, commit lock `$(git rev-parse --git-dir)/collaboration-commit.lock`,
mkdir … rmdir; never --no-verify; never bare git stash). Foreground
commands only. No push or spawn.
