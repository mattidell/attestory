# Retrospective: The Sale Page Observer Reads Question Groups

Milestone key: sale-observer-question-groups. Plan:
`docs/phases/engine-breadth/milestones/sale-observer-question-groups.md`.
Closed 2026-11-23. Tools and tests only.

## What happened

page-plain-words parked an opt-in Chrome fixture failure: the sale page
observer still expected each blocked reason's raw sentence after
blocked-sale-pages made the page show a question-group link and ADR 0087
added a member label prefix. A grok builder made the observer follow the
page's rendering rules, added fast tests for each branch and ran the ten
real-Chrome cases. A grok review checked the page rules independently and
mutated scratch pages; its two notes concern malformed models only.

## What worked

- Running it beside a content milestone: tools and tests only, no shared
  files.

## What to change

- An observer that mirrors page rendering drifts when the page changes. A
  page change that alters reason rendering should run the opt-in fixture
  (`SALE_PAGE_OBSERVATION_BROWSER=1`) before it merges.
