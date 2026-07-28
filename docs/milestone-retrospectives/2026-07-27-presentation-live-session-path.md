# Retrospective — Presentation: Live Session Path (2026-07-27)

Closed 2026-07-27. Four tracks, one session, one day. Presentation ends at
**L2**, exactly as planned. The data-boundary row ends at **L3**, now recorded
as a permanent owner-accepted ceiling rather than a pending task.

## What it was for

The owner was away from their desk, so the one thing that would move Presentation
to L3 — a real viewing session and an attestation — was unavailable. The
milestone asked a narrower question instead: *what can be done so that the act,
when it happens, is short and already rehearsed?*

That framing is the milestone's main structural result. It produced a plan whose
success condition was explicitly "no maturity row moves," which is an unusual and
useful shape. A milestone that cannot raise anything cannot be tempted to claim
it did.

## What changed while it ran

**The plan lost a track before it was chartered.** The original four-track shape
included implementing the three preflight probes. The owner cut it: workstation
precondition observation is owner-held for the same reason confinement is. That
turned out to be more than scope reduction. It made the repository's posture
uniform — it authors *none* of its own boundary enforcement — and it removed a
concrete hazard rather than answering one. The natural probe,
`tmutil isexcluded <path>`, would have put the residency locator in `argv`,
readable from the process table by exactly the Developer/Supply domain ADR-0044
says is not separated. Three imperfect mitigations existed; not doing it was
better than all of them.

**The PR cadence changed.** The foreman assumed one PR per completed track and
opened one for Track 1. The owner corrected it to a single PR at milestone close.
The governing rule, "merge unit = review unit," never required per-track PRs —
the milestone is independently reviewable too. Each track kept its own review and
its own record; only the timing of reaching `main` changed. Recorded in
`docs/roles/foreman.md`.

## The two findings, which are one finding

Track 2's build was clean where it aimed. The full suite passed, both evaluation
manifests were untouched and passing, the envelope scan was clean, preflight
refusal provably preceded both derivation and browser launch, and teardown was
covered on the failure path. The review found two blocking defects anyway, and
they are the same defect:

1. The loopback server carried the **entire presentation model inline** with no
   authentication. Loopback binding is not a control — every local account
   reaches `127.0.0.1`, and an ephemeral port is not a secret, the full range
   being scannable in well under a second. ADR-0047's classification is
   described as *total*, and this channel was in none of its four classes,
   because it is ingress and the ADR only ever considered egress.
2. The session served the **evaluation fixture page**, whose title, visible
   header, and own comment declare synthetic `demo-*` data and never a real
   workspace. Those statements would have been false on the screen the owner
   reads *while forming the attestation*.

Neither is a defect in a component. Both live in the **join** — the consequence
of serving a real model through an evaluation-shaped page over an open socket.
Each component was correct about its own job and neither could see the
composition. The plan asked for that shape and did not think it through, so the
finding is as much a planning defect as a build one.

**The generalizable lesson: when a component moves from a synthetic context to a
real one, its self-descriptions move with it and stop being true.** The fixture
page's comment — "never a real workspace" — was an accurate committed data-safety
declaration that a change *in a different file* silently falsified. Nothing
checks that class of claim.

## The repair, and one thing deliberately not done

The obvious fix for finding 2 was string-substituting the three labels at serve
time. That was rejected explicitly: targeted replacement silently no-ops when the
wording changes, restoring the false labels with no failure anywhere. That is
precisely the fail-open drift class the Track 1 amendment had just named as its
sharpest residual — and it would have been introduced in the same milestone that
named it. The chosen shape instead **refuses to serve any page carrying a
synthetic-provenance marker**, so misconfiguration cannot quietly succeed, and
the product surface asserts nothing about provenance in either direction on the
grounds that a page cannot verify what it holds.

The cost is a forked renderer: two near-identical pages that can drift. That was
the owner's call, taken knowingly, because the alternative — one page reading its
provenance from the model — would have edited the frozen evaluation tree.

## What the rehearsal did and did not prove

It ran the fail-closed default, all three individual refusals, the clear path,
teardown, the browser-failure path, and the provenance refusal. Nine sections
rendered; no locator on any surface; 404 on every unguessed route; the socket
closed on exit.

It did **not** launch a real browser, and **the product page has never been
rendered by one**. Only a normalized diff against the fixture page and a
`node --check` stand behind it. The rehearsal record says so in its own words,
and the maturity matrix repeats it, because a rehearsal that overstates itself is
worse than none.

## Process observations

- **Pointer discipline held.** Every charter and its pointer advance went in one
  commit. The recurring drift from the previous milestone did not recur.
- **A new drift class appeared in its place.** The capsule's free-text `status`
  field went stale twice — the Track 1 reviewer caught it in `phase-state.md`,
  and the same staleness was then found in the plan's own capsule. The
  machine-read fields stay honest because tooling pushes on them; the prose has
  no such pressure and rots silently. Now covered by the post-merge PR-state rule
  in `docs/roles/foreman.md`, which forces a re-read of the whole capsule before
  every PR.
- **The foreman reviewed Track 2 itself,** at owner direction, and said so in the
  record rather than claiming an independence it did not have.

## State at close

| Row | Level | Note |
| --- | --- | --- |
| Presentation (all five domains) | **L2** | Unchanged. One owner act from L3. |
| Data boundary | **L3** | Permanent owner-accepted ceiling (ADR-0044 line 164). |
| Everything else | unchanged | No other cell moved. |

Records: ADR-0047 amendments 1 and 2; Track 1 review; Track 2 review; Track 3
rehearsal record; `packages/derivation/live_session.py`;
`packages/presentation/pages/citation-walk.v1.html`.
