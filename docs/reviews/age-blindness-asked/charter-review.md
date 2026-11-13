# Charter: fresh-reader review of age and blindness asked

Role: Reviewer. Source HEAD on milestone/age-blindness-asked-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/age-blindness-asked.md (read it
whole, including Decisions 1-10, the Track 0 Disposition and the Track 1
result). You have not seen the build, so judge from the committed content,
tests and evidence, not from summaries. Do not read governance.

## Questions

1. **Truth of each sentence, by hand.** From the 2025 Form 1040
   instructions (line 12d, the standard deduction chart and worksheet,
   Schedule 1-A senior deduction) and Publication 501 (public IRS
   sources), say whether each of the five questions and the retitled
   facts is true of what its rule reads, for everyone asked. Try at least:
   single born January 1 and January 2, 1961; joint with one spouse 65;
   a taxpayer who died in 2025 the day before and two days before turning
   65; separate with a spouse who has income and one who has none;
   head of household with a spouse recorded; qualifying surviving spouse;
   a dependent filer who is 65. Run each through the real coordinator on
   core v88 with synthetic `demo.*` findings and compare lines 12e, 13b
   (Schedule 1-A), 15 and 16. Say whether any pinned hand value in
   tests/test_age_blindness_v88.py is wrong.
2. **Who is asked.** Is any question asked where it cannot matter, or
   missed where it can? Does a filing-status change leave a stale answer
   that moves a number?
3. **What the filer sees.** Are the five sentences plain enough to answer
   once? Does any promise more than its rule does?
4. **Immutability.** Is registry v86 add-only, every new citizen
   byte-identical to prototype.py's decided build, and the loader change
   limited to v88 entries? Is the diff over packages/schemas,
   packages/kernel and packages/derivation empty?
5. **CI cost.** The live module replays 775 recorded lists in a process
   pool inside pytest (about 22 minutes on 4 workers) plus 38 cases.
   Earlier milestones replayed 298 in their live module. Is a 775-list
   replay in CI justified, or should the module replay a smaller set and
   leave the 775 to the committed evidence? Name what each choice loses.
   Is a process pool inside a pytest-xdist worker safe?
6. **The 104 v81 lists** that block where their fixture published a
   number: is the explanation (questions added after v81) true, and is
   comparing them against v87 instead of the fixture sound?
7. **Test isolation.** Evidence loaded only through
   tests/evidence_loader.py; no other module's globals assigned.
8. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

docs/reviews/age-blindness-asked/review.md, committed (explicit path,
under the collaboration-commit lock; retry with backoff if held). For each
finding give: file:line; a reproduction; a severity (blocking, should-fix
or note); the fix you would make. End with a verdict: ready, or the
blocking list. Make no other edits.
