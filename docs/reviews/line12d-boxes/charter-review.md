# Charter: fresh-reader review of line 12d's boxes

Role: Reviewer. Source HEAD on milestone/line12d-boxes-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/line12d-boxes.md (read it whole,
Decisions 1-6 and the Track 0 disposition included). You have not seen the
build, so judge from the committed content, page, tests and evidence, not
from summaries. Do not read governance.

## Questions

1. **Each box is true.** For every filing status, with the taxpayer and
   the spouse each 65-or-older or not, blind or not, and unanswered, run
   the real coordinator on core v90 with synthetic `demo.*` findings. Does
   each of the four boxes show checked or not checked exactly as the 2025
   Form 1040 instructions for line 12d say (born before January 2, 1961;
   spouse boxes on a joint return, or on a separate return only when the
   spouse had no income, is not filing and cannot be claimed as a
   dependent)? Does any box show an answer the filer never gave? In
   particular: an unanswered taxpayer age or blindness must not be drawn
   as "not checked" on the page. The Track 1 report says a shared test
   helper states an unstated age or blindness as false; decide whether
   that hides this case, and test the unanswered case without the helper.
2. **Hidden spouse boxes.** For single, head of household, qualifying
   surviving spouse, and separate with the condition no or unanswered: is
   each spouse box not applicable, with words a filer would read as true?
   After joint is changed to separate, does a stale spouse answer draw a
   box?
3. **Numbers untouched.** Line 12e and every other line: is any value on
   v90 different from v89 on any of the 775 recorded lists? Check
   rerun-output.json's classes against rerun.py's classifier: can
   "numbers identical, new fields only" hide a changed number, a changed
   reason or a changed question? Sample ten lists and diff them yourself.
   The report also says the v83 check ignores rows that only grow a
   dependency-name list; confirm that exclusion cannot hide a number.
4. **The page.** Is the change to `citation-walk.v1.html` exactly
   Decision 1 (draws `not_checked` as "not checked"; any other render
   still throws), identical in the package copy and the harness copy? Does
   any existing page or baseline change? Can page data reach the lookup
   with a key such as `__proto__` or `constructor` and draw something?
5. **Immutability.** Are registry v88 and release v88 add-only over their
   predecessors, core v90 equal to v89 plus the 17 members, every new
   citizen byte-identical to prototype.py's build, and the loader change
   limited to v90? Is the diff over packages/kernel and over every
   published schema empty?
6. **CI cost and isolation.** tests/test_line12d_boxes_v90.py makes live
   runs: name runs that test nothing a sibling does not, and any test
   that would pass if the rule under test were wrong. Evidence loaded only
   through tests/evidence_loader.py?
7. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim. Any recorded-return
replay you run must use `tools/recorded_replay.py` with parallel workers.

## Deliverable

docs/reviews/line12d-boxes/review.md, committed (explicit path, under the
collaboration-commit lock; retry with backoff if held). Each finding:
file:line, reproduction, severity (blocking, should-fix or note), fix. End
with a verdict: ready, or the blocking list. No other edits.
