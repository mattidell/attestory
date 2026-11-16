# Charter: fresh-reader review of the line 6c and Schedule 1 alerts

Role: Reviewer. Source HEAD on milestone/page-alerts-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/page-alerts.md (read it whole,
Decisions 1-9 and the Track 1 result included). You have not seen the
build, so judge from the committed content, tests and evidence, not from
summaries. Do not read governance. Also apply
docs/roles/qualitative-review.md.

## Questions

1. **The words are true.** Run the real coordinator on published core
   v92 with synthetic `demo.*` findings and read the saved page model
   (and draw at least two pages in Chrome as the line 12d page test
   does). For line 6c with the lump-sum election not made, made and
   unanswered, with and without a benefit statement: what does each of
   the two line 6c sections show (value, explain, citation, questions),
   and is every word true against the 2025 Form 1040 line 6c
   instructions in the local sources? Is the form's box a checkbox, so
   that "not checked" is the right word? Would a filer reading two line
   6c sections understand them?
2. **The Schedule 1 top entry.** At 0, at a personal-item loss, blocked,
   and on a return with no Schedule 1: value, explain, citation buttons.
   Does the new citation say what the instructions say
   (`citation.schedule1.top-entry` against the passage Track 0 quotes,
   checked in the local source yourself)? Is "No Form 1099-K statements
   were received for 2025." true on every return where it shows? Does a
   blocked or inapplicable top entry draw a citation that implies a
   value?
3. **No alert, and none hidden.** Is the census's zero real: read
   census.py and say whether it could miss an alert the drawn page
   shows (a different alert class, a field outside the form roots, an
   attachment). Draw one page from each of three different recorded sets
   and count alerts in the DOM.
4. **Nothing else changed.** Diff the two successors against their
   predecessors and the sibling against the line 6d checked/not-checked
   pair. Any change of read, pin, guard, disposition or question other
   than the intended ones is a finding. Does the sibling make an
   unanswered election block anything v91 did not block, or show its
   question twice on one field? Sample ten recorded lists across sets
   and diff v91 and v92 yourself with `tools/recorded_replay.py` in
   parallel; can "identical" in track1-replay.json hide a changed
   sentence or disposition?
5. **The settled Social Security rows.** Track 0 first reported two FAIL
   rows on line 6a and a follow-up called them case artifacts. Check
   that independently: with the SSA-1099 closure left on an old horizon,
   does line 6a block and ask on v92? Is there any act list a truthful
   filer can reach where line 6a publishes without a current closure?
6. **Immutability.** Registry v90 and release v90 add-only over v89;
   core v92 equal to v91 except the six citizens and two entrypoints;
   the loader change limited to v92; the diff over packages/kernel,
   packages/derivation, packages/schemas and packages/presentation
   empty; v91 and earlier pages draw what they drew.
7. **Tests.** In tests/test_page_alerts_v92.py and its package test:
   name any test that would pass if the content were wrong, any case
   named for a state its act list does not have (an "unanswered" case a
   helper answers), any check that classifies sentences by punctuation,
   and live runs that test nothing a sibling does not. Is the browser
   test marked as the line 12d one is? Evidence loaded only through
   tests/evidence_loader.py?
8. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim. Run every command
in the foreground; never end your turn while a command is running.

## Deliverable

docs/reviews/page-alerts/review.md, committed (explicit
path, under the collaboration-commit lock; retry with backoff if held).
Each finding: file:line, reproduction, severity (blocking, should-fix or
note), fix. End with a verdict: ready, or the blocking list. No other
edits.
