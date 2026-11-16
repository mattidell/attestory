# Charter: fresh-reader review of the lines below line 16

Role: Reviewer. Source HEAD on milestone/preferential-base-reason-2025,
diffed against `github/main`. Plan:
docs/phases/engine-breadth/milestones/preferential-base-reason.md (read it
whole, Decisions 1-9 and the Track 1 result included). Contract: ADR 0086
(accepted). You have not seen the build, so judge from the committed
content, tests and evidence, not from summaries. Do not read governance.

## Questions

1. **The successor changes one state.** Diff
   `rule.selected-preferential-base` v11 against v10. Is the only
   behavioural change that "Schedule D required, no sale or Schedule D
   amount recorded" blocks `DEPENDENCY_ABSENT` with eight names where v10
   was inapplicable? Construct states to break that: activity of each
   kind, each Schedule D conclusion (no, required, open), boundary answers
   open and answered. Any other difference in disposition, value, read or
   pin is a finding.
2. **Every name is true and answerable.** For each of the eight names on
   the four recorded returns: does it resolve to a question a filer can
   answer, and is the sentence true of that return? Is any of them a
   question the filer has already answered in a way that makes asking it
   again misleading? Is a question shown twice on one field?
3. **The dead end is closed.** Run the real coordinator on core v91 with
   synthetic `demo.*` findings. A return with no sale to enter: does
   changing Exception 1 to "yes" unblock every line and reach the
   2025-instruction hand value? A return with an unentered sale: does
   entering it reach the hand value? Is any filer-visible field on these
   returns still blocked with no question? Does a "blocked" preferential
   base where it was "inapplicable" change any downstream line that used
   to publish (a line that read the inapplicable symbol as absent and
   computed)?
4. **Line 16 parked.** The Track 1 gate found a line 16 successor would
   change one of the ten blocked-names-question cases
   (`exception1_personal_loss_8949`), so line 16 still names four
   questions while the 23 fields name eight. Is that inconsistency
   harmful on the page (a filer told different things on adjacent lines),
   or acceptable to park? Was the gate's reading right?
5. **Numbers untouched.** Check track1-replay.json's classes against the
   classifier: can the four "numbers_changed" lists hide a changed line
   value, and can "identical" hide a changed question? Sample ten lists,
   including all four changed ones, and diff v90 and v91 yourself with
   `tools/recorded_replay.py` in parallel.
6. **Immutability.** Registry v89 and release v89 add-only over v88; core
   v91 equal to v90 with exactly one member replaced; the new citizen
   byte-identical to prototype.py's build; the loader change limited to
   v91; the diff over packages/kernel, packages/derivation,
   packages/schemas and packages/presentation empty.
7. **Tests.** In tests/test_preferential_base_reason_v91.py: name any
   test that would pass if the rule were wrong, any case named for a
   state its act list does not have (an "unanswered" case a helper
   answers), and live runs that test nothing a sibling does not. Evidence
   loaded only through tests/evidence_loader.py?
8. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in the review.

Run `pytest` only to confirm a specific failing claim. Run every command
in the foreground; never end your turn while a command is running.

## Deliverable

docs/reviews/preferential-base-reason/review.md, committed (explicit
path, under the collaboration-commit lock; retry with backoff if held).
Each finding: file:line, reproduction, severity (blocking, should-fix or
note), fix. End with a verdict: ready, or the blocking list. No other
edits.
