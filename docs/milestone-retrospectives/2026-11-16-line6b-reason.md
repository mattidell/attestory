# Retrospective: Line 6b Names Why It Is Blocked (2025)

Milestone key: line6b-reason. Plan:
`docs/phases/engine-breadth/milestones/line6b-reason.md`.
Closed 2026-11-16. Core v93, registry v91, release v91. Content only: ten
input-question citizens. No rule, schema, engine, projection or page
change.

## What happened

The page-alerts review parked a Form 1040 line 6b that blocked with no
reason on a return with a Form SSA-1099 benefit statement. P0
reproduced 34 such blocks on core v91 across 168 synthetic cases. The
expected cause was an expression block with an empty `missing` list
(ADR 0086). It was not: every block already named its missing fact, and
ten of those facts had no adopted question. Ten question citizens repair
all 34.

P0 stopped because a separate filer with no benefits, whose return
already computed, gained the living-apart question on line 6d. The
projection attaches questions only to blocked fields, so line 6d had
been blocked on that fact with no reason all along; the foreman accepted
it as the same defect. Track 0 stopped twice more. First, it tried to
answer each question through the product and found no answer control;
the questions were declared display-only and judged by the published
convention for `no-...` facts. Second, on a separate return with two
open causes, line 6b names only the first; both questions show on the
page, and that was accepted.

Track 1 was rebased onto page-alerts once it merged and built core v93;
a Codex usage limit stopped it mid-replay, and it resumed after the
reset. The fresh review was blocking on one question: the Puerto Rico
and American Samoa question asked about "income from there" while its
fact covers any income of a bona fide resident, so a resident with only
mainland income would have answered it the wrong way. The repair widened
the words and fixed the evidence's source excerpts, which had been
sliced on page breaks.

Dispatch: Codex (gpt-6.1-sol) throughout, one builder thread resumed
across P0, Track 0, Track 1 and the repair (high effort, then medium),
and one fresh reviewer thread at high effort. Builder turns read 17-60M
input tokens each, 97-98% cached.

## What worked

- Reproducing before designing: the trace replaced the expected design
  (a rule-artifact v17 successor) with a smaller one (questions only).
- Reading why a stop fired. Both P0's and Track 0's stops were correct
  readings of the charter and wrong readings of the product; the trace
  in each report was enough to decide without another run.
- The fresh reviewer read the fact titles, not the questions' own
  sentences, and found a meaning error twenty passing checks had missed.

## What to change

- A charter target such as "no computing return newly asked a question"
  must say what a question attaches to. The projection only explains
  blocked fields, so the right target was "no field that shows a value
  gains a question".
- "Answer through the question" in a charter needs a named path. Say
  whether the product has an answer control before chartering a check
  that depends on one.
- Check each question against its fact's title, not only against the
  form passage: the form passage was narrower than the product fact.
- Evidence that quotes sources by line number slices on `\n`, never
  `str.splitlines()`, which also splits form feeds in PDF extracts.

## Follow-ups

Parked in the roadmap: display-only questions (no answer control beyond
W-2 entry); line 6b naming both open causes on a separate return; the
replay pin as selected-value parity.
