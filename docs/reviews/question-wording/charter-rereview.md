# Charter: re-review of the question-wording repair

Role: Reviewer. Source HEAD on milestone/question-wording-2025, diffed
against `github/milestone/selection-keyed-collect-2025`. Read
docs/reviews/question-wording/review.md (your predecessor's findings),
Decision 7 in docs/phases/engine-breadth/milestones/question-wording.md,
and the repair commits after 584aa65a. Do not read governance.

## Questions

1. **F1.** Are the final Exception 1 v3 words and the exception1 bundle
   v2 title true of what `schedule-d-required.conclusion` reads, for
   everyone asked, per the 2025 Form 1040 line 7a and Schedule D
   instructions? Is the personal-item sentence now consistent with the
   Form 1099-K / 1099-S reporting rule? Run at least: no sale, personal
   item sold at a loss with no form; the same loss with a Form 1099-K;
   sales inside an IRA only. Each through the real coordinator on core
   v87 with synthetic `demo.*` findings.
2. **F2, F4, F5.** Is each fixed as Decision 7 says?
3. **Regeneration.** Is registry v85 still add-only against the base,
   every v87 member byte-identical to prototype.py, and the diff over
   packages/schemas, packages/kernel and packages/derivation empty?
4. **Anything new** the repair introduced.
5. **Data safety.** `python3 tools/envelope_scan.py --range
   github/milestone/selection-keyed-collect-2025..HEAD`. No absolute or
   temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim.

## Deliverable

Append a "Re-review" section to docs/reviews/question-wording/review.md,
committed (explicit path, under the collaboration-commit lock; retry with
backoff if held). Each finding: file:line, reproduction, severity
(blocking, should-fix or note), fix. End with a verdict. No other edits.
