# Retrospective: The Saved Page Writes Its Own Words Plainly

Milestone key: page-plain-words. Plan:
`docs/phases/engine-breadth/milestones/page-plain-words.md`.
Closed 2026-11-23. Page and tests only; no package version change.

## What happened

plain-line-texts had parked the words the page writes itself until
blocked-sale-pages, which owned the page, merged. A P0 census found 140
page-owned string kinds, 69 of them engine words or raw ids in the text a
filer reads first, on every rendered recorded list. Track 1 replaced them
and moved ids into collapsed technical details. A fresh review found the
words were not yet all true: `Calculated` is false for a line that repeats
another, and every blocked remedy said information was missing, which is
false for an invalid record or a total that does not match. The repair
chose each sentence from its code; a re-review then found two more
sentences that described the wrong fact, and a test that the fast lane
never ran. The foreman fixed those.

The P0 and Track 1 ran on agy (Gemini 4 Neon). The owner then stopped agy
dispatch: Google's Antigravity FAQ says wrapping `agy -p` inside a
third-party coding agent is not supported on consumer plans. The review,
repair and re-review ran on grok.

## What worked

- Rendering every recorded list and counting first-read leaks gave a
  number (691 lists to 0) instead of a judgement.
- Reviewing for truth, not tone: each review finding was a sentence that
  claimed more than the record proves.

## What to change

- A plain word must be checked against every case that shows it, starting
  from where the code is emitted, before it is drafted. The P0 drafted
  sentences from the code's name.
- Fetch before rebasing a worktree that has not fetched since the merge it
  is meant to follow. A rebase onto a stale ref did nothing, and a builder
  stopped on the stale base.
