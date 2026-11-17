# Charter: fresh-reader review of line 16 naming the failing Exception 1 criteria

Role: Reviewer. Source HEAD on milestone/line16-names-2025, diffed
against `github/main`. Plan:
docs/phases/engine-breadth/milestones/line16-names.md (read it whole:
Decision 1 is replaced by Decisions 6-11; the Track 1 result included).
You have not seen the build, so judge from the committed content, tests
and evidence, not from summaries. Do not read governance. Also apply
docs/roles/qualitative-review.md.

## Questions

1. **The names are the reason.** Read `rule.form1040-line16` v9 and
   `rule.selected-preferential-base` v12 against v8 and v11, the four
   Exception 1 question citizens, and the 2025 Form 1040 line 7a
   Exception 1 and Schedule D instructions in the local sources. In the
   state "Schedule D required, no sale recorded, no Form 8949 sources
   yes", does each rule name exactly the criteria whose current answer
   fails Exception 1, for every one of the fifteen non-empty failing
   subsets? Is each criterion's pass/fail test the right polarity for
   its fact? Is every other branch of both rules byte-for-byte v8's and
   v11's?
2. **What the filer reads.** Run the real coordinator on published core
   v95 with synthetic `demo.*` act lists and read the saved page model;
   draw at least two pages in Chrome as tests/test_page_alerts_v92.py
   does. With one and with several failing criteria: is every sentence
   on line 16, its four dependants and the preferential-base fields
   true, and enough for the filer to see why Schedule D is required and
   what to do? Is the "record your sale" route visible anywhere when the
   failing answers are right? Say so if not, and whether that is this
   milestone's to fix.
3. **Decisions 2 and 3.** The personal-loss case keeps its four names;
   an unanswered Form 8949 boundary asks that question. Are both still
   true on v95, and is Decision 2's reasoning sound?
4. **Nothing else changed.** Core v95 equal to v94 except the two
   replaced members; registry v93 and release v93 add-only; loader change
   limited to v95; the diff over packages/kernel, packages/derivation,
   packages/schemas and packages/presentation empty. The two
   tools/required_versus_read_allowlist.json entries for v9: true and
   their reasons current? Sample ten recorded lists across sets and diff
   v94 and v95 yourself with `tools/recorded_replay.py` in parallel. Can
   the strict classification hide a changed value, disposition or code?
5. **Tests.** In tests/test_line16_names_v95.py and its package test:
   name any test that would pass if the content were wrong, any case
   named for a state its act list does not have, any check that
   classifies sentences by punctuation, and live runs that test nothing a
   sibling does not. Are expected names derived independently of the
   rule under test? Evidence loaded only through tests/evidence_loader.py,
   with bare-name sibling imports bound by path first?
6. **Data safety.** `python3 tools/envelope_scan.py --range
   github/main..HEAD`. No absolute or temp-directory path in committed
   files or the review.

Run `pytest` only to confirm a specific failing claim. Run every command
in the foreground; never end your turn while a command is running.

## Deliverable

docs/reviews/line16-names/review.md, committed (explicit path, under
`$(git rev-parse --git-dir)/collaboration-commit.lock`, mkdir … rmdir;
retry every 10 s up to 5 min if held). Each finding: file:line,
reproduction, severity (blocking, should-fix or note), fix. The draft
PR's `verify` gate is expected to refuse a draft; do not report that.
End with a verdict: ready, or the blocking list. No other edits. No
push, no spawn.
