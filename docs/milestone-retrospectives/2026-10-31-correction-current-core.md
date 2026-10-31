# Retrospective — A Correction Recalculates on the Current Core (2025)

## Result

- **Corrections work again on current cores.** The correction session
  pinned registry v40. A workspace that adopted any core after v42 was
  refused (`REGISTRY_CHECKSUM_MISMATCH`), and the filer saw only "not
  calculated". The session now resolves its surface from the workspace's
  adoption; on v66 a correction calculates at opening and at save and
  matches a fresh run.
- **Nothing else moved.** A v42 workspace behaves exactly as before; the
  refusals and the saved-file shape are unchanged.

## What the evidence changed

- **A parked line hid a broken feature.** "Still resolves an older registry"
  read like staleness. The trace showed refusal: since core v43 the session
  has worked only for v42 workspaces. Tests stayed green because every
  correction fixture adopts v42.
- **Resolve from the record, not a name.** The fix finds the registry by the
  hash the release attests, using the coordinator's own adoption selection.
  The 1099-K recorder's filename guess went with it.

## Process

- One Sonnet 5.5 builder for P0, Track 1 and a repair; one reviewer, resumed
  once after a usage-limit stop with its work intact.

## Follow-ups

- The W-2 entry loop fixes its own registry.
- Tell the filer why a correction did not calculate (a protocol change).
- A complete current-core return with student loan interest, to drive line
  21 on the session.
