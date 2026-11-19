# Retrospective: Chrome Cleanup Does Not Hang CI

Milestone key: chrome-cleanup-hang. Plan:
`docs/phases/engine-breadth/milestones/chrome-cleanup-hang.md`.
Closed 2026-11-19. Harness and test-helper change only; no package
version change.

## What happened

One saved-page Chrome test failed `verify` three times across #287 and
#292 by waiting out its 240 s bound. The foreman read the hang as a
Chrome helper process holding the observer's stderr pipe. A Claude
Sonnet builder reproduced it with a synthetic Chrome whose helper
outlives its parent, ignores SIGTERM and writes into the profile. The
fix makes Chrome its own process-group leader, ends the whole group on
dispose, retries the profile removal, and has the observer exit
promptly with its own exit code.

The fresh review (Claude Opus) found that the builder's control could
not be reproduced: without any held pipe, the old observer still hung.
The open handle was the loopback DevTools server. A rejected `dispose()`
jumped past `server.close()`. The foreman repaired that directly, and the
unremovable-profile test now passes even with the `process.exit`
backstop removed. The review also found that the correction owner's
SIGKILL safety net no longer reached a Chrome in its own group. That is
fixed too.

The review itself stalled for four hours. One of its commands never
ran, most likely because it was waiting on a permission prompt that a
background agent cannot answer. Stopping it and resuming it with its
context intact worked.

## What worked

- A synthetic Chrome that reproduces the mechanism made the hang a
  13-second local test rather than a CI flake.
- The reviewer's mutants: one showed that the stderr `destroy()` is
  untested, and another showed which change actually fixes the hang.

## What to change

- A control experiment in evidence needs to be one a reviewer can rerun
  from the committed files. This one was not, and its conclusion was
  wrong.
- A background agent with no output for an hour needs checking, not
  waiting on. Bound every command that can hang.
