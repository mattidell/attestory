# Retrospective: Content Guards Run in the Fast Lane

Milestone key: fast-content-guards. Plan:
`docs/phases/engine-breadth/milestones/fast-content-guards.md`.
Closed 2026-11-23. Tests only.

## What happened

eic-no-ssn-child's first CI verify failed on a rule-file size cap that its
builder's fast-lane run never checked: conftest marks every module that
drives the live coordinator as live, and the size guards sat in five such
modules, each with its own exception list. A grok builder moved them into
one fast module with one table, proved the union of files and caps was
unchanged, and showed an over-cap file now fails the fast lane. It also
fixed a Chrome observer test that failed whenever both color variables
were set. A grok review rebuilt the old guards independently and agreed.
The rebase onto #301 moved its two new exceptions into the table.

## What worked

- Running a tooling milestone beside two content milestones: it touched
  only tests, so it waited on nothing.
- Proving a refactor of guards by reconstructing the old guards and
  comparing sets, not by reading the diff.

## What to change

- A guard that protects content belongs in the fast lane from the start;
  put new content checks in `tests/test_content_file_sizes.py` or a fast
  sibling, not in a module that drives the coordinator.
