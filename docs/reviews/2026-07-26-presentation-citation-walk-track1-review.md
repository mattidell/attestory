# Presentation — Citation Walk Track 1 Review Gate

Status: **NOT READY**
Date: 2026-07-26
Role: independent High / medium Reviewer
Charter: `docs/reviews/charter-2026-07-26-presentation-citation-walk-track1-review.md`

## Capsule echo (pre-review)

| Item | Resolved value |
| --- | --- |
| **Source ref** | `track/presentation-citation-walk-track1` resolved and verified at `6ce90e75cc20eaaaf93a8166bb1c9fc5bb8a7528` (PR #77). |
| **Exact object** | The six files added by Track 1 only: `citation-walk.v1.html`; `citation-walk.v1.json`; and `baseline.v1.json`, `t1-inject-on-blocked-line.v1.json`, `t2-non-numeric-published-value.v1.json`, and `t3-unknown-line-status.v1.json` under `tools/presentation_harness/examples/pages/citation-walk-fixtures/`. |
| **Role** | One independent Reviewer, High tier / medium effort. |
| **Scope** | Measure the real renderer against ADR-0046, reproduce the 23 manifest criteria and T1–T3, and confirm the full `form-field.v3` disposition matrix plus the diagnostic cases. |
| **Evidence-rung ceiling** | Presentation content/contract correctness only. The completed harness F1–F6 floor is credited, not re-reviewed; no redesign, new check family, economy comparison, or runner-trust review. |
| **Stop conditions** | None tripped. The object resolved cleanly; findings are repairable in the presentation files without schemas, dependencies, frameworks, build changes, rule-point re-opening, or non-synthetic data. |

The review used only the committed synthetic `demo-*` fixtures. The Builder's
PR description was not used as proof.

## Required measurements

| # | Measurement | Result |
| --- | --- | --- |
| 1 | Independently run `node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json`. | **Pass:** exit 0; 23 pass, 0 fail, 0 error. |
| 2 | Render each declared disposition and show blocked/degraded states without a value. | **Pass for the exercised matrix:** baseline covers `published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, and `guard_inapplicable`; the blocked line shows its missing dependency and remedy rather than a value. Finding F1 prevents accepting the surface overall. |
| 3 | Suppress a diagnostic whose input is blocked. | **Pass:** the blocked-input diagnostic renders the fixed suppression text, not its tie-out value. Finding F2 identifies the corresponding invalid-input gap required by ADR-0046. |
| 4 | Keep rejected or tampered values out of visible text for T1–T3. | **Pass:** T1 remains an honest blocked alert; T2 and T3 become visible generic, redacted section errors. |
| 5 | Preserve distinct, non-colliding identity for a reused citation. | **Pass:** the pin-keyed registry gives the line and Schedule B sites identical labels and a backlink while retaining distinct site IDs. |
| 6 | Keep blocked-state salience section-level. | **Pass:** the block is inline in Line 16; no page-level blocked-lines banner is rendered. |
| 7 | Exclude `innerHTML`, dependencies, framework, and build step. | **Pass:** source inspection found DOM node construction through `createElement`/text nodes only, no dynamic `innerHTML`, external script, dependency, framework, or build step. |
| 8 | Confirm clean diff and reviewed-commit CI. | **Pass:** `git diff --check` on the Track 1 commit is clean; PR #77's `verify` check is green at the reviewed head. |

## Blocking findings

### F1 — Numeric zero lines render without a source citation

The baseline fixture's `computed_zero` Line 2a and `closure_backed_zero` Line
3a each have a `field.citation`, but each has an empty `citationSites` array.
The renderer invokes `renderCitation` only while iterating `citationSites` and
never reads `field.citation`. Both numeric zero values therefore reach the DOM
without a rendered citation.

This violates ADR-0046's zero-authority foreclosure: nothing may render
without a source citation. The smallest repair is to bind a citation to every
numeric field render (including the two zero kinds) and add executable
coverage for those citations.

### F2 — Diagnostic eligibility ignores an invalid numeric input

`healthyDisposition()` accepts a diagnostic input solely because its
disposition is numeric. It does not require the corresponding resolved value
to be a finite number. A diagnostic tied to T2's non-numeric
`published_value` section would therefore render `diag.renderText` even
though that line has failed validation and renders a section error.

This violates ADR-0046's resolved zero-authority rule-point: no derived or
diagnostic value from invalid or blocked input may reach the DOM. The smallest
repair is to require a finite resolved numeric value for diagnostic eligibility
and add the invalid-input diagnostic case to the existing manifest.

## Verdict

**NOT READY.** The runner, T1–T3 reproductions, disposition matrix, citation
reuse, salience, accessibility checks, diff check, and data-boundary scan are
otherwise clean. Either F1 or F2 is sufficient to fail ADR-0046 conformance.
The two focused presentation-layer repairs above are the smallest residual;
they return to the foreman for disposition under the milestone's one-review
cap.

## Repository gate

`python3 tools/envelope_scan.py --range main..HEAD` completed cleanly for this
review-record branch before commit. No renderer, fixture, schema, harness, or
phase-state file is changed by this review.
