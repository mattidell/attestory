# Charter: fresh-reader review of line 6b naming why it is blocked

Role: Reviewer. Source HEAD on milestone/line6b-reason-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/line6b-reason.md (read it whole,
Decisions 1-12 and the Track 1 result included). You have not seen the
build, so judge from the committed content, tests and evidence, not from
summaries. Do not read governance. Also apply
docs/roles/qualitative-review.md.

## Questions

1. **The words are true.** For each of the ten new questions, read the
   fact it pins, every rule that reads that fact, and the 2025 Form 1040
   / instruction / worksheet passage in the local sources yourself. Is
   every word true? Under the published convention in Decision 8 (a
   `no-...` fact asked about the thing itself; "no" means the fact
   holds), would a filer's plain yes/no record the meaning they intend?
   Is any question so broad or so narrow that a truthful "no" sets a
   fact the rule reads differently (for example a question that asks
   about one form when the fact covers several)? Compare each with its
   published siblings on the same fact family.
2. **Placement.** Run the real coordinator on published core v93 with
   synthetic `demo.*` act lists and read the saved page model; draw at
   least two pages in Chrome as tests/test_page_alerts_v92.py does. Does
   any field that publishes a value gain a question? Does any field ask
   a question that answering would not unblock? Is any question shown
   twice on one field, or on a field that has nothing to do with it?
   Check line 6d on a separate filer with and without benefits.
3. **Decision 10.** In a separate-filing case missing one scope answer
   and living apart, is what line 6b and line 6d say true and enough for
   the filer to finish? After the scope answer alone, does line 6b then
   ask living apart?
4. **Nothing else changed.** Core v93 equal to v92 except the ten
   members and their entrypoints; registry v91 and release v91 add-only;
   loader change limited to v93; the diff over packages/kernel,
   packages/derivation, packages/schemas and packages/presentation
   empty. Sample ten recorded lists across sets and diff v92 and v93
   yourself with `tools/recorded_replay.py` in parallel; can "identical"
   in track1-replay.json hide a changed sentence or disposition? Do the
   neighbour results support "questions only"?
5. **Tests.** In tests/test_line6b_reason_v93.py and its package test:
   name any test that would pass if the content were wrong, any case
   named for a state its act list does not have (an "unanswered" fact a
   helper sets), any check that classifies sentences by punctuation, and
   live runs that test nothing a sibling does not. Do hand values come
   from the 2025 worksheet? Is the browser test marked as the page-alerts
   one is? Evidence loaded only through tests/evidence_loader.py, with
   bare-name sibling imports bound by path first?
6. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in committed
   files or the review.

Run `pytest` only to confirm a specific failing claim. Run every command
in the foreground; never end your turn while a command is running.

## Deliverable

docs/reviews/line6b-reason/review.md, committed (explicit path, under
`$(git rev-parse --git-dir)/collaboration-commit.lock`, mkdir … rmdir;
retry every 10 s up to 5 min if held). Each finding: file:line,
reproduction, severity (blocking, should-fix or note), fix. End with a
verdict: ready, or the blocking list. No other edits. No push, no spawn.
