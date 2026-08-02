# Presentation — Live Session Path Track 2 Review

Status: **NOT READY**
Date: 2026-07-27
Role: Foreman-performed review at owner direction (not author-independent; see
"Independence" below)
Charter: `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/presentation-live-session-path.md`,
Track 2 review gate

## Object

The Track 2 build at `d166d4b`: `packages/derivation/live_session.py` (new),
`tests/test_presentation_live_session.py` (new), and a five-line addition to
`packages/derivation/live_viewing.py` adding an `initial_url` parameter to
`LiveViewingVehicle.launch`.

## Independence

The owner directed the foreman to review this track directly. The foreman did
not author the build, but is not an independent reviewer seat and did charter
the work. This record states that plainly rather than claiming a fresh-reader
gate it did not have.

## Verification

| Check | Result |
| --- | --- |
| `pytest -n auto` (full suite) | **Pass.** 658 passed, 2447 subtests, 53.7s. |
| Track 2 + vehicle focused modules | **Pass.** 14 passed. |
| `citation-walk.v1.json` manifest | **Pass.** |
| `citation-walk-production-shaped.v1.json` manifest | **Pass.** |
| `tools/envelope_scan.py --range main..HEAD` | **Pass**, rc=0, no output. |
| `git diff --check origin/main...HEAD` | **Pass.** |
| `server.mjs` and both manifests byte-unchanged | **Pass.** The diff touches three files, none of them harness files. |

## Gate measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | The model is served from the workspace and the page from the repository. | **Pass.** `_render_page` confines the page under `repo_root` and the model under `capability.location`, each via `_confined_path` with `strict=True` resolution and a `relative_to` containment check. |
| 2 | Preflight inputs arrive from the caller; nothing reads machine configuration. | **Pass.** `probes: PreflightProbes` is a required keyword parameter of `open_presentation_session`. No subprocess, `tmutil`, `mdutil`, or process-table read appears anywhere in the diff. |
| 3 | Preflight refusal precedes derivation and browser launch. | **Pass**, and tested directly: `test_preflight_refusal_happens_before_derivation_or_browser` asserts the vehicle is never called. |
| 4 | The clipboard partiality guard still holds. | **Pass.** `live_viewing.py`'s disposition logic is untouched; its regression tests pass. |
| 5 | The path is not reachable as an evaluation path. | **Pass in the stated direction, fail in the inverse.** See Finding 2. |
| 6 | Teardown holds on every exit. | **Pass.** Browser-launch failure closes the server before re-raising, and `test_browser_launch_failure_closes_server_and_workspace_session` covers it. `LiveViewingSession.close` raises only `LiveViewingError`, which `LivePresentationSession.close` catches, so the server close is reached on every browser-teardown outcome. |
| 7 | No locator in any surface. | **Partial.** Request logging is suppressed, `__repr__` is redacted, refusals carry stable codes with no paths, and the tests assert the workspace root appears in neither the served body nor the session repr. But see Finding 1: the served body is readable by parties the session does not control. |

## Finding 1 — BLOCKING — the session serves the owner's real return on an unauthenticated loopback socket

`_PresentationServer` binds `("127.0.0.1", 0)` and serves the fully-substituted
page — which now carries the **entire real presentation model inline** — at `/`
with no token, no `Origin` check, and no authentication of any kind.

Any process on the machine can retrieve the owner's complete Form 1040 citation
walk for the lifetime of the viewing session by scanning loopback ports. An
ephemeral port is not a secret: the full range is scannable on loopback in well
under a second.

This is not a variant of an already-named residual. ADR-0047's Class C is
*egress* — the browser reaching out. This is **ingress**: the session opens a
listening socket carrying live data, and nothing in ADR-0047's four-class
classification covers it. The classification is described in the ADR as
**total**, so an unclassified boundary-relevant channel is a gap in the decision
record and not merely a hardening opportunity.

Loopback binding also does not restrict the reader to the same UID. Every local
account can reach `127.0.0.1`, so the exposure is broader than the same-UID
residual ADR-0044 and ADR-0047 already accept.

Cheap and adequate mitigation: serve at an unguessable path derived from
`secrets.token_urlsafe`, keep `/` a 404, and pass that URL as `initial_url`. The
capability to read then requires guessing a 256-bit path rather than a 16-bit
port. Whatever is chosen, the channel needs classifying in ADR-0047 rather than
leaving the total classification incomplete.

## Finding 2 — BLOCKING — the served page tells the owner their real data is synthetic

The session serves
`tools/presentation_harness/examples/pages/citation-walk.v1.html` verbatim apart
from the `__FIXTURE_JSON__` substitution. That file asserts its own provenance in
three places:

- its HTML comment: "Synthetic demo-* data only; loaded via the browser-
  evaluation runner's `__FIXTURE_JSON__` substitution, **never a real workspace**,
  browser, credential, or remote URL";
- its `<title>`: "Citation Walk — Track 1 (synthetic demo-* data only)";
- its visible page header: "Track 1 renderer · synthetic `demo-*` data only".

During the real session those statements are false, and the middle two are
false **on the screen the owner is looking at while forming the attestation**.
A surface that mislabels real data as synthetic is an honesty defect under
ADR-0046 regardless of whether any value is wrong, and this milestone exists
precisely to make the owner's eventual attestation honest.

It is also the inverse of the coupling gate measurement 5 was written to
prevent. The evaluation path cannot reach the session, which is what the gate
asked. But the session now depends on the evaluation fixture tree: a page edited
for evaluation reasons silently becomes the real human surface. The declaration
in that file's own comment — "never a real workspace" — is now false as a
statement about the repository, which means a committed data-safety declaration
has been invalidated by a change that did not touch the file.

Note for whoever repairs this: **do not fix it by string-substituting the
labels.** Targeted replacement of specific wording no-ops silently when the
wording changes, which restores the false labels without any failure — the same
fail-open drift class the Track 1 amendment named as its sharpest residual. The
honest shapes are a product-owned renderer distinct from the evaluation fixture,
or a fail-closed refusal to serve any page carrying a synthetic-provenance
marker.

## Non-blocking observations

1. `test_browser_launch_failure_closes_server_and_workspace_session` asserts the
   workspace session directory is gone but never asserts the HTTP port stopped
   listening, so the half of the behaviour its name promises is untested.
2. `open_presentation_session` wraps `live_coordinate_run` in a bare
   `except Exception` that discards the original error via `from None`. The
   locator hygiene motive is right, but every genuine defect in the coordinator
   collapses into one opaque code with no diagnostic path. A follow-up may want
   a reason code that distinguishes a refusal from a fault.
3. The `initial_url` addition to `LiveViewingVehicle.launch` is correct — it
   routes through the existing `_validate_navigation_url`, so a non-loopback
   URL refuses before any process spawns — but it is a vehicle change inside a
   track whose stated boundary was wiring plus serving. It is small, in the
   spirit of the track, and better than the alternatives; recorded for accuracy,
   not objected to.

## Verdict

**NOT READY.** Two blocking findings, both in the same class: the build wires
the parts together correctly, and the correctness of the wiring is well tested,
but it does not carry the boundary discipline across the join. Finding 1 opens
an unclassified channel; Finding 2 propagates a false provenance claim onto the
human surface.

Neither is a defect in what Track 2 set out to build. Both are consequences of
serving a real model through an evaluation-shaped page over an open socket —
which is the shape the plan asked for and did not think through. The repair
belongs with the owner's disposition, not with a silent fix, because the honest
resolution of Finding 2 changes what Track 2's deliverable is.

## Data safety

No real workspace, residency locator, machine configuration, credential, remote,
live run, or owner attestation was consulted. All tests ran against synthetic
`demo-*` fixtures and temporary directories.
