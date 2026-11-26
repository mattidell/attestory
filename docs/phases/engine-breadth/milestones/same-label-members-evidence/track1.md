# Track 1: One Question per Member, Same Label or Not (2025)

Plan: `docs/phases/engine-breadth/milestones/same-label-members.md`,
Decisions 1-3. Core v107 (registry v105, release v105); no content, no
published file and no schema changed.

## What changed

`packages/derivation/presentation_projection.py`,
`_closure_question_reasons` only. The walk records a member's missing
question as `(fact type, member subject keys)` instead of
`(fact type, recorded label)`, and builds one reason per
`(label, sentence, member)`, sorted by label, then sentence (the member's
keys only break ties and are never shown). Each reason is still
`{"sentence", "memberLabel"}`. No `memberOrdinal` and no page change: telling
same-named members apart is Track 2 under ADR 0090 (proposed).
`tools/sale_page_observation.py` did not need to change: it prefixes each
reason it is given and deduplicates none.

Effect, from `probe-v107-track1.json` (the 23 P0 probe returns, on the built
code, rendered with the repository page):

| Case | Before | After |
| --- | --- | --- |
| two or three members "Demo Sam", each missing the same answer (age, residency, under-17, tie-breaker, odc TIN, relative TIN, joint return) | one "Demo Sam" reason | one "Demo Sam" reason per member (2 or 3) |
| "Sam", "Sam", "Alex", all missing age | Alex + one Sam | Alex + two Sams |
| same-label members missing different answers | already one reason each | unchanged |
| one of several same-label members missing | one reason | unchanged |
| distinct labels; child and parent sharing a label; all answered | as before | unchanged |

Every blocked line still has a sentence, every saved model passes
`validate_presentation_model`, and for each blocked line with a member
reason the page draws exactly as many member reason items as the model has
(`dom.member_item_counts`, each line rendered alone through the
page-plain-words DOM checker), with no section errors and no first-read
leaks. No line has a question group link, before or after (Decision 3).

## Tests

- `tests/test_same_label_members_walk.py` (unit, fast lane, 10 tests): two
  and three same-label members each missing the answer; one of two missing
  (either one); two missing different answers; two each missing two answers
  (four reasons); two of three sharing a label; distinct-label control; a
  same-label member of another kind; one member reached twice is asked once;
  reasons carry only `sentence` and `memberLabel`. Six of them fail on the
  pre-Track-1 projection.
- `tests/test_same_label_members_live.py` (live, 25 tests): 11 same-label
  and 2 distinct-label probe returns through `live_coordinate_run` on
  published v107. On every line with member reasons: one reason per
  left-out answer with the expected labels, the expected number of distinct
  sentences, no ordinal, no question links; the page draws every member
  reason; the child-and-parent case keeps both questions.
- `tests/test_eic_child_answers_walk.py` still passes unchanged.

## Full-surface replay

`replay-track1.json` (`replay.py`, one shared run, 8 pool workers, about 7
minutes). Each list is taken with the built projection (A) and with the
pre-Track-1 projection at `9f6b57c75` (B, swapped in as the "scratch" copy;
the only differing definition is `_closure_question_reasons`), strict, no
expectations.

- **Recorded lists: 775 of 775 identical** (691 success/success, 84
  error/error on both sides), 0 differences.
- **Probe lists:** 14 identical, 9 differ, 323 differences, all page reason
  entries: 111 member reasons (`memberLabel` and `sentence`) present only on
  the built side, and 101 `resolved.reasons@order` where they are added.
  The 9 are exactly the cases where two or three same-label members miss the
  same answer.

No number, disposition, block code, report row, graph node, attachment or
question link changes anywhere.

## Checks

- Full suite on the built code, run in six foreground file shards because
  one run exceeds the 10-minute command bound on this shared machine:
  7,850 passed, 25 skipped, 0 failed.
- `mypy` on `presentation_projection.py` and both new test modules: clean.
