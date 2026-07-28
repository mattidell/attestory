# Presentation — Live Session Path Track 3 Dress Rehearsal

Date: 2026-07-27
Role: Foreman-executed at owner direction
Charter: `docs/phases/real-return/milestones/presentation-live-session-path.md`,
Track 3
Commit under rehearsal: `702237a` (Track 2 build `d166d4b` plus its repair)

The point of this track is that the owner's first real session should not also
be the first run of the path. What follows is what actually ran, followed by an
explicit account of what did not — the second list is the more useful one.

## What ran

Executed against synthetic `demo-*` facts in a temporary workspace, through the
real `open_presentation_session` entry point with no test doubles other than the
browser process factory.

### 1. Fail-closed preflight, no probe answers supplied

| Step | Observed |
| --- | --- |
| `PreflightProbes()` (all `UNKNOWN`) | Refused `presentation-preflight-refused`, codes `viewing-residency-backup-indeterminate`, `viewing-residency-index-indeterminate` |
| Vehicle reached? | No. The refusal precedes derivation and browser launch. |

The default state of the system is refusal. Supplying nothing gets nothing.

### 2. Each individually fatal condition

| Condition | Observed |
| --- | --- |
| Residency backed up | Refused, `viewing-residency-backup-present` |
| Residency content-indexed | Refused, `viewing-residency-index-present` |
| Clipboard manager present | Refused, `viewing-clipboard-history-present` |

### 3. Full path with all preconditions clear

| Observation | Value |
| --- | --- |
| Run id | `demo.rehearsal` |
| URL | loopback, 43-character route token |
| Served page | 40,836 bytes |
| Model inlined in body | yes, `presentation-model.v1` |
| `<title>` | `Form 1040 — Citation Walk` |
| Provenance markers in served body | none |
| Workspace root in served body | no |
| Workspace root in session `repr` | no |
| `/`, `/index.html`, `/citation-walk.v1.html` | 404, 404, 404 |
| Model written under the workspace | yes, 38,819 bytes |
| Sections rendered | 9 |
| Socket after `close()` | closed (`URLError`) |
| `.live-view` session directory after close | removed |

Nine sections is the full implemented 1040 slice — lines 1a, 2b, 3a, 3b, 9, 11,
12, 15, 16.

### 4. Provenance refusal

Pointing the page path at the evaluation fixture refused
`presentation-page-declares-provenance`. The fixture cannot be served as the
product surface even by misconfiguration.

### 5. Browser launch failure

An unusable browser refused `viewing-browser-exited-during-launch`, and the
`.live-view` directory was removed. Teardown held on the failure path.

### 6. Product surface equivalence

The product page and the evaluation fixture page were diffed after normalising
the `MODEL`/`FIXTURE` identifier rename. The **only** differences are the three
intended ones: the header comment, the `<title>`, and the visible banner
paragraph. Every line of rendering logic is identical. The product page's script
also passes `node --check`.

This matters because the product page has never been rendered by a browser (see
below); byte-equivalence to a page that has been, modulo three text changes, is
the substitute evidence and is weaker than a render.

## What did not run, and what that leaves uncovered

This is the part a future reader should trust over the section above.

1. **No real browser was ever launched.** Every rehearsal step used a synthetic
   process factory that writes a `DevToolsActivePort` file. Chrome's real
   startup, its profile and cache confinement flags, its handling of the token
   URL, and the actual rendering of the page were **not exercised**. The vehicle
   argument construction was exercised; the browser was not.
2. **The product page has never been rendered.** The evaluation harness renders
   the *fixture* page. The product page is a three-text-change copy that no
   browser has drawn. A rendering defect introduced by the copy would not have
   been caught by anything here — only the diff and the syntax check stand
   behind it.
3. **No real workspace and no real facts.** Synthetic `demo-*` facts only.
   Nothing establishes that the real fact set produces a well-formed model.
4. **Preflight inputs were supplied, not observed.** Per the ADR-0047 amendment,
   observation is owner-held and outside this repository. The rehearsal proves
   the *disposition* logic behaves correctly given an answer; it proves nothing
   about how an answer is obtained, and a wrong answer would pass through
   silently.
5. **Confinement was not exercised at all.** No sandbox profile was applied.
   The session ran unconfined, as it will whenever the owner does not wrap it.
6. **No attestation.** Presentation remains L2.

## What a real session will differ in

The owner supplies the three preflight answers from their own trust domain,
optionally wraps the invocation in their sandbox profile, points the capability
at the real residency, and looks at the result. Everything else is what ran
here. The two differences that carry risk are items 1 and 2 above: the first
real session is still the first time a real browser draws this page.

## Data safety

No real workspace, residency locator, machine configuration, credential,
remote, live run, or owner attestation was consulted. All output went to
temporary directories that were removed. The rehearsal script itself was
scratch and is not committed; every step it performed is reproducible from
`tests/test_presentation_live_session.py`, which covers the same paths.
