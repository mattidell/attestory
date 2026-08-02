# Review — The Entry Loop (synthetic), Track 1: the W-2 entry loop

- Role: **Reviewer** (`docs/roles/reviewer.md`)
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track1-review.md`
- Builder charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track1.md`
- Branch: `milestone/entry-loop-synthetic`, at `4db2239`
- Under review: `2a00193` — 14 files, 7,174 insertions

## Orientation and review object

`python3 tools/build_orientation_block.py --ref HEAD` resolved reviewer at
`4db223960602629c3043ff687524abe7ef65a5a6`, matching `git rev-parse HEAD`.
After fetching, the derived ratified line is `origin/main-ui`; this branch is
zero commits behind and fourteen ahead. The merged opening-plan PR #109 does
not make the workspace spent.

This review covers the exact Track 1 build. I read the entry usability criteria
only as the build's context and did not conduct its Track 2 scoring procedure.

## Verdict: NOT READY

The synthetic loop, Phase A evidence, contribution admission path, surface
artifact route, and data boundary are substantially sound. One blocking
boundary/honesty finding remains: this independent loopback server has not
closed, or accurately recorded as open, ADR-0048's entry-session condition for
browser spellcheck and preflight. The only implementation measure is a
form-level `spellcheck="false"` attribute. That is not the affirmative
vehicle-level launch flag or policy ADR-0048 requires to close spellcheck's
network path, and it is neither tested nor recorded as a limitation. The new
server does not launch through `live_viewing.py` or otherwise bind its
preflight/confinement/disposal contract.

## Findings

### Blocking

**F1. Track 1 silently leaves ADR-0048's entry-vehicle condition unresolved.**

ADR-0048 says an entry surface must launch with spellcheck's network path
affirmatively closed by a vehicle-level flag or policy; it explicitly says the
existing viewing preflight was not extended to entry sessions. The build adds
an independent `127.0.0.1` server and the Svelte input's `spellcheck="false"`,
but no browser launch policy, preflight binding, or source/recorded limitation.
An HTML control attribute asks the browser not to spellcheck that one input; it
does not close the browser's enabled enhanced-spellcheck network path.

This is not a request to extend the preflight in this repair. The builder
charter forbids that. Close it by recording the precise nonclaim: this
synthetic loop is not an ADR-0048-qualified real-entry vehicle, does not
inherit the viewing preflight, and cannot carry real input until a later vehicle
track affirmatively closes spellcheck and establishes the applicable
entry-session boundary. The current form attribute may remain a useful UI
setting, but must not be presented as that vehicle control.

### Weakening

**F2. The most security-relevant HTTP refusals have no committed regressions.**

The suite tests one malformed W-2 amount, but it has no regression coverage for
wrong content type, oversized body, malformed JSON, JSON type confusion,
template tampering, duplicate submission, or an out-of-order submission. I
manually exercised each against the loopback endpoint and all currently failed
closed with redacted responses and no log advance. That is evidence of current
behavior, not durable coverage for the project's new typed-input boundary.

**F3. The compiled browser client is not exercised against the loopback API.**

The suite builds the adopted artifact and checks output-file markers, while the
endpoint tests use a placeholder HTML file. Source inspection and a reviewer
integration check confirm that the built page and API are served from the same
capability URL, but no committed test executes the compiled client’s relative
`./api/*` requests. This is not usability scoring, which remains Track 2; it is
the remaining technical integration gap most likely to surface when that run
opens the page.

## Measurements

### 1. Phase A dependencies — PASS

All four tests are non-vacuous at their stated boundary.

| Dependency | What the test proves | Mutation attempted | Result |
| --- | --- | --- | --- |
| 1 — W-2 is the only prompt and reaches completion | Initial state is exactly one W-2 Box 1 prompt; entering it leaves no missing facts and yields a computed complete return. | Removed the W-2 prompt from the initial snapshot. | The test's exact initial-prompt assertion failed. |
| 2 — loopback POST uses admitted contribution acts | GET and POST work at the loopback URL; the resulting log tail is contribution, member-transition, assertion with contribution linkage. | Forced `apply_contribution_batch` to refuse. | The POST returned 422 instead of accepting, so the test failed. |
| 3 — sets and completion are observable | Initial snapshot has exactly the nine named lines; entered state is complete with all lines computed. | Omitted Form 1040 line 16 from the visible snapshot. | The exact line-set assertion failed. |
| 4 — fixed mutation pattern | Entry and correction mark all five impact lines changed and all four comparison lines unchanged; values move or hold as applicable. | Forced expected-impact line 16 to `unchanged` after entry. | The changed-set equality assertion failed. |

The fourth test does catch a line that fails to move; it does not merely check
that some line changed.

### 2. No direct fact-writing shortcut — PASS

The browser receives a one-time contribution template. `contribute()` validates
that template, parses only W-2 Box 1, constructs contribution-carrier acts,
and calls the existing `apply_contribution_batch` before appending any act to
the log. It appends only after a completed terminal record, then recomputes
through `live_coordinate_run`. Patching that applicator to refuse prevented the
POST from advancing. I found no second endpoint, `RunContext` shortcut, or
direct fact-store write.

### 3. ADR-0049 route — PASS

`resolve_entry_surface()` calls `resolve_surface_artifact`; it does not recreate
adoption/release/registry verification. The surface resolver in turn reuses
the production resolver's adoption selection and release/registry checks. The
artifact-package core and its schema are byte-identical across the reviewed
commit; the only resolver route used for UI bytes is the separate published
surface artifact.

### 4. Loopback POST boundary — PASS with F2

The server binds only `127.0.0.1`, uses a high-entropy route capability, accepts
only the contribution endpoint, limits bodies to 16,384 bytes, requires JSON,
validates the supplied template and W-2 amount, serializes admission with a
lock, and emits generic locator-free errors. Active probes confirmed:

- malformed JSON and oversized input return 400;
- wrong content type returns 415;
- wrong-type and template-tampered input return 422;
- duplicate and stale/out-of-order events return 422;
- rejected-body input never appeared in the response and none of those
  requests advanced the act log.

The sole acceptance path produced contribution, member-transition, and
assertion acts after the applicator admitted the batch. F2 is the coverage
qualification, not a failure of the observed behavior.

### 5. Data safety — PASS

`python3 tools/envelope_scan.py --range main..HEAD` exited 0 with no output.
The fixture, source, test names, request paths, errors, and diagnostics use
synthetic demo identifiers and contain no residency locator. The generated
manifest contains 941 fingerprinted input entries (source, lockfile, and
vendored dependencies), totals 5,081,010 bytes, and contains no `dist/`
entry; that matches its provenance-only purpose.

### 6. Preflight and spellcheck — FAIL (F1)

No existing preflight was changed, which is correct. But the build neither
notes that it does not bind that preflight nor deals with ADR-0048's expressly
owed vehicle-level spellcheck control. See F1.

### 7. Scope — PASS

The implementation is W-2 Box 1 only, synthetic, and documentation-free of any
per-field explanation schema. Valid correction uses the existing free-fact
supersession path; no refusal UI is added. No tax rule, artifact package,
matrix, or correction authority changes. There is no filing flow or separate
missing-facts screen.

### 8. Test coverage — PASS with F2 and F3

The 316 test lines cover fixture regeneration, all four Phase A dependencies,
admission linkage, correction, one redacted malformed entry, artifact resolve
and build, static criteria markers, and source-level data safety. That is
proportionate for the core synthetic runtime, but the critical rejection matrix
and compiled-client/API interaction remain untested as recorded in F2 and F3.

### 9. Verification — PASS

The `2a00193` commit message records the full sequence from `3a72a6d`, with no
omissions. Reviewer reruns found:

- `pytest -n auto`: 703 tests completed to 100% with no failure report;
- `python3 -m mypy`: no issues in 134 source files;
- governance lint: conformant;
- builder-range envelope scan, reviewer `main..HEAD` envelope scan, and the
  builder-range whitespace check: clean.

`python3 -m unittest tests.test_entry_loop_t1` also passed all 16 Track 1
tests, including the adopted-surface build.

## Remaining uncertainty

The single thing I could not prove is whether a real browser launched for a
future entry session can be kept from using an enabled enhanced-spellcheck
network path. The current loop does not own or test that launch. This is the
same unclosed condition in F1, not a claim that the synthetic fixture sent data
anywhere.

No product code, fixture, criterion, or matrix entry was changed in this
review.
