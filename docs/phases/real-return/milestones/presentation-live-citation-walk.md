<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-live-citation-walk",
  "milestone_state": "planned",
  "retrospective": null,
  "status": "Selected 2026-07-26. The plan establishes one implementation track, one independent review gate with at most one repair and focused recheck, one owner-held quarantined exercise/attestation unit, and one completion-record unit.",
  "scope": [
    "project one successful live_coordinate_run result into the existing ADR-0046 citation-walk surface from authoritative resolved graph, record state, publications, and dispositions",
    "write the self-contained presentation artifact and its browser profile/cache only below LiveWorkspace",
    "preserve the full covered form-field and Schedule B presentation slice without a caller-supplied value or presentation-model authority channel",
    "verify the live integration on synthetic production-shaped runs before the owner-held exercise",
    "exercise the reviewed surface against one real resolved run in quarantine and record only ADR-0031's three-fact non-descriptive attestation",
    "raise the Presentation row from L2 to L3 across the five currently covered domains if the implementation review, real exercise, and records review all pass"
  ],
  "non_goals": [
    "no new tax computation, form field, citation, schedule, or domain coverage",
    "no schema change or new published citizen",
    "no change to ADR-0046's presentation contract or ADR-0031's data boundary",
    "no browser-evaluation runner relaxation for non-synthetic fixtures",
    "no real workspace, locator, value, identifier, disposition detail, screenshot, report, or generated artifact in the repository, remote, review, chat, or retrospective",
    "no presentation-economy comparison or L4 hardening claim"
  ],
  "deep_reads": {
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/real-return/milestones/presentation-live-citation-walk.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "packages/derivation/live.py",
      "packages/derivation/live_workspace.py",
      "packages/derivation/runner.py",
      "tools/presentation_harness/examples/pages/citation-walk.v1.html",
      "tools/presentation_harness/examples/pages/citation-walk-fixtures/baseline.v1.json",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-repair-review.md",
      "AGENTS.md#Data Safety Rules",
      "AGENTS.md#Fixture Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/real-return/milestones/presentation-live-citation-walk.md",
      "docs/adr/0031-real-data-residency-boundary.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/reviews/2026-07-26-presentation-citation-walk-track1-review.md",
      "AGENTS.md#Data Safety Rules"
    ],
    "dispatch": [
      "docs/roles/foreman.md#Dispatch",
      "AGENTS.md#Dispatch authorization"
    ],
    "merge_or_records": [
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/milestone-retrospectives/2026-07-26-presentation-citation-walk.md",
      "docs/milestone-retrospectives/2026-07-25-presentation-evaluation-process-economy.md",
      "docs/milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md",
      "docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md",
      "docs/milestone-retrospectives/2026-07-23-live-run-system-definition-and-trust-domains.md"
    ]
  }
}
-->
# Milestone: Presentation — Live Citation Walk

Status: **Planned.** The owner selected another Presentation milestone on
2026-07-26. The plan becomes the active milestone when its planning PR reaches
`main`.

## Objective

Operate the ADR-0046 citation-walk surface on one real resolved run while
preserving ADR-0031's quarantine boundary, then raise the Presentation row
from L2 to L3 across the five currently covered domains.

## Current state

The previous milestone shipped a renderer whose disposition behavior,
citations, failure containment, redaction, and accessibility were independently
reviewed against ADR-0046. Its browser manifest covers the complete synthetic
disposition matrix and the T1–T3 fault suite.

That renderer is not yet connected to the production live path:

- `live_coordinate_run` writes a quarantined JSON result containing
  `run_id`, `stop_reason`, and `dispositions`, while the in-memory
  `RunResult` also holds the publications needed for citation lineage;
- the renderer consumes a hand-shaped object that combines form fields,
  resolved publications, citation sites, attachment groups, and diagnostics;
- the browser-evaluation runner correctly confines itself to repository-relative
  synthetic fixtures and rejects a non-synthetic fixture; and
- the page and its default browser profile are currently synthetic-test
  surfaces, not a quarantine-contained live invocation.

The L2→L3 gap is therefore a bounded integration gap, not a new presentation
contract or a new tax-content problem.

## Scope

1. Add one authoritative presentation projection to the successful production
   path. It consumes only the resolved production graph, projected record
   state, `RunResult.publications`, and `RunResult.dispositions` already created
   by `live_coordinate_run`.
2. Project every covered `form-field.v3` member and the existing Schedule B
   attachment into the citation-walk model. Publication values and citation
   sites come only from current runner output and its exact pins; blocked and
   inapplicable states never acquire a value.
3. Produce a self-contained HTML presentation below
   `LiveWorkspace.live_output_path`. No caller may supply a presentation model,
   raw value, `RunContext`, fixture adapter, package member, or citation label
   as a second authority channel.
4. Keep browser state derived from the live page inside quarantine: any browser
   profile, cache, log, temporary file, or failure artifact used by the live
   presentation entrypoint is reserved below `LiveWorkspace`.
5. Preserve the existing synthetic browser manifest as the ADR-0046 regression
   floor and add production-shaped synthetic integration cases through the
   authoritative `live_coordinate_run` path.
6. After Track 1 merges, the owner exercises the presentation entrypoint
   against one real resolved run in quarantine. Only the exact three-fact
   non-descriptive attestation permitted by ADR-0031 may cross.
7. Independently review Track 1 and the final completion record. A matrix lift
   occurs only if the implementation review is `READY`, the owner attestation
   is recorded, and the records review is `READY`.

## Non-goals

- No new tax rule, form field, citation content, attachment, income domain, or
  return line.
- No change to `form-field.v3`, `act-derived-publication.v1`, any other
  published schema, or any accepted ADR.
- No new presentation-model citizen or repository copy of a live presentation
  payload.
- No relaxation or reuse of the browser-evaluation runner's synthetic-only
  fixture boundary.
- No redesign of the citation walk. Track 1 may remove synthetic-only copy from
  the live rendering mode and add the integration seam; it must preserve the
  reviewed information architecture and ADR-0046 behavior.
- No real-data automation by a Builder or Reviewer. The owner alone performs
  the quarantined exercise.
- No presentation-economy comparison, savings claim, data-boundary L4 claim, or
  publication-transport hardening.

## Contracts

### Authoritative projection

- A successful `live_coordinate_run` remains the only production authority
  path. The presentation projection is downstream of that result and cannot
  accept caller-authored values or a caller-authored presentation object.
- Form fields are selected from the resolved exclusive package graph and joined
  to current publications/dispositions by their declared symbols and exact
  versioned pins. Ambiguity, missing binding, unknown disposition, missing
  citation, or non-finite numeric content fails visibly for the affected
  section and renders no value.
- Schedule B presentation is projected from the existing attachment
  disposition and current source lineage. It does not infer attachment
  requirement, completeness, or tie-out status independently.
- The projection performs no arithmetic. Diagnostics may restate an already
  published relationship only when all referenced inputs are valid current
  numeric publications; otherwise they remain suppressed, preserving the prior
  F2 repair.

### Live artifact and browser containment

- The live HTML, any intermediate presentation model, browser profile, cache,
  temporary file, log, and failure output are sensitive live-run artifacts and
  remain below `LiveWorkspace`.
- Repository code is read-only during the owner-held exercise. The live
  entrypoint has no publication or remote URL and uses no external resource.
- The output is self-contained. Serialization into HTML must be inert under
  adversarial strings: no `innerHTML`, executable fixture text, closing-script
  breakout, rejected-value echo, or second DOM authority.
- Live presentation output is reserved before write, cannot escape the
  workspace, and is owner-only readable.

### Evidence boundary

The repository may record only:

1. that the owner exercised the live citation walk in quarantine;
2. that dispositions were observed there; and
3. that no artifact crossed the boundary.

It may not record which fields or attachments published or blocked, any value,
identifier, locator, refusal reason, screenshot, browser output, presentation
artifact, or description of the run.

## Fixtures

Committed fixtures remain independently constructed and obviously synthetic.
Track 1 adds production-shaped cases that enter through `live_coordinate_run`
and cover:

- all currently covered Form 1040 fields and the Schedule B attachment;
- `published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, and
  `guard_inapplicable`;
- citation reuse and exact-pin source lineage;
- a blocked line carrying a smuggled value;
- a non-finite or non-numeric numeric disposition;
- an unknown disposition;
- a missing field citation;
- a derived diagnostic with one invalid input;
- adversarial text containing markup and closing-script sequences;
- a missing/ambiguous symbol-to-field join;
- output-name traversal and a browser profile/cache outside the live workspace;
  and
- a resolver refusal, which creates no presentation artifact.

No fixture is transformed from or selected by a real document or run.

## Verification

Track 1 names the focused test module it creates and keeps these existing
regressions green:

```text
python3 -m unittest tests.test_presentation_live_integration
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
python3 -m unittest tests.test_frrs_t4_w2_live_integration
python3 -m unittest tests.test_dsbs_t4_dividend_live_integration
python3 tools/envelope_scan.py --range main..HEAD
git diff --check
```

The authoritative CI `verify` check remains the gate of record for each PR.
The foreman does not run the full suite.

### Owner-held real exercise

The real exercise occurs only after the reviewed Track 1 implementation is on
`main`. The owner supplies the live workspace capability at runtime, executes
the same production coordinator plus presentation entrypoint over the full
currently covered return slice, and views the resulting citation walk using
the quarantine-contained browser profile. All run and browser detail stays in
quarantine.

The repository acceptance record is exactly:

> "I exercised the live citation walk in quarantine; dispositions were
> observed there; no artifact crossed the boundary."

## Data safety

All committed code, fixtures, manifests, tests, reviews, and records are
synthetic or public-origin. No repository process reads the live workspace.
No locator is committed. The owner-held exercise produces no report for review;
the three-fact attestation is the entire repo-side evidence. Track 1 and the
records review both run the range envelope scan.

## Exit criteria

1. A successful authoritative live run creates a self-contained citation-walk
   artifact and all browser state only below `LiveWorkspace`.
2. The presentation covers the full currently covered Form 1040 and Schedule B
   slice from resolved graph content, current publications/dispositions, and
   exact pins, with no caller-authored value or presentation authority.
3. The existing 26-criterion synthetic citation-walk manifest remains green.
4. The production-shaped synthetic integration battery proves the positive
   path and every fixture class above, including resolver refusal and
   quarantine containment.
5. Track 1's independent review returns `READY` against ADR-0031, ADR-0046,
   the prior F1/F2 findings, and the new live-integration boundary.
6. The owner-held real exercise occurs and only the exact three-fact
   attestation is recorded.
7. A final independent records review confirms the attestation boundary,
   Git/CI evidence, and the matrix claim. On `READY`, the Presentation row moves
   L2→L3 across the five covered domains; otherwise the matrix remains L2 and
   the smallest exact residual is recorded.
8. The retrospective, roadmap, phase state, and branch cleanup agree with the
   ratified record.

## Review gates

### Track 1 implementation review

One fresh author-independent Reviewer must:

1. rerun the new focused integration module and the existing citation-walk
   manifest;
2. confirm goldens enter through `live_coordinate_run`, never a `RunContext`,
   fixture adapter, or direct runner shortcut;
3. probe caller-authored presentation authority, script/markup injection,
   missing/ambiguous joins, rejected-value echo, path/profile escape, resolver
   refusal, and creation of any repo-side artifact;
4. recheck prior F1/F2 invariants and ADR-0046 blast containment/accessibility
   where Track 1 changes the renderer; and
5. run `python3 tools/envelope_scan.py --range main..HEAD`.

`READY` requires all five. `NOT READY` returns the smallest exact residual to
the foreman. The plan carries at most one repair and one focused recheck; a
residual after that recheck returns to the owner for disposition.

### Completion-record review

One fresh Reviewer checks only the attestation boundary, merge/CI evidence,
matrix wording, phase-state pointers, retrospective, and data-safety scan. The
Reviewer never accesses the live workspace or asks the owner for descriptive
evidence.

## Tracks

### Track 1 — Authoritative live presentation integration

**Goal:** connect the reviewed citation walk to the production live result and
contain its artifact plus browser state under `LiveWorkspace`.

**Boundary:** code and synthetic tests only; no live workspace, schema, tax
content, new presentation contract, or real exercise.

**Inputs:** `live_coordinate_run`, resolved exclusive graph, projected record
state, `RunResult`, existing renderer/manifest, ADR-0031, and ADR-0046.

**Outputs:** the smallest production presentation projector/entrypoint,
renderer integration changes needed to support an honest live mode, focused
synthetic integration fixtures/tests, and an independent review record.

**Verification:** the commands above plus the Track 1 review gate.

**Migration risk:** additive live output and a possible additive field on
`LiveCoordinatorOutcome`; preserve existing JSON output and callers.

**Data safety:** no live capability or personal material; all new cases are
synthetic and the range scan is mandatory.

### Track 2 — Owner-held real exercise and attestation

**Goal:** exercise Track 1 against one real resolved run and record only the
three permitted facts.

**Boundary:** owner-held quarantine action plus one attestation record; no
Builder/Reviewer access, no descriptive evidence, and no implementation
change.

**Inputs:** reviewed Track 1 on `main`, the owner-held live workspace capability,
and the full currently covered return slice.

**Outputs:** the exact three-fact attestation in this plan, carried by its own
records/attestation PR.

**Verification:** the owner performs the exercise; repo-side checks are limited
to Git status, installed envelope-gate integrity, range scan, and exact
attestation wording.

**Migration risk:** none.

**Data safety:** every generated artifact remains in quarantine.

### Track 3 — Completion record

**Goal:** close the milestone honestly and disposition the Presentation matrix
claim.

**Boundary:** records only; no repair, implementation, new evidence request, or
quarantine access.

**Inputs:** Track 1 `READY` review and green CI, Track 2 attestation, Git merge
record, and this plan's exit criteria.

**Outputs:** retrospective, L2→L3 matrix update or exact decline, roadmap and
phase-state update, completion review, and cleanup.

**Verification:** independent records review, range scan, `git diff --check`,
and CI `verify`.

**Migration risk:** documentation only.

**Data safety:** the three-fact attestation is the only live-run fact.

## Execution economy

| Unit | Role | Effort | Boundary |
| --- | --- | --- | --- |
| Track 1 build | Builder | Medium | Bounded integration against settled contracts and known attacks |
| Track 1 review | Reviewer | High | Novel live-authority/containment boundary plus prior F1/F2 |
| Track 1 repair, if needed | Same Builder | Medium | Findings only |
| Track 1 focused recheck, if needed | Same Reviewer | Medium | Findings plus directly touched invariants |
| Track 2 | Owner | Owner-held | One quarantined exercise and exact attestation |
| Track 3 records | Foreman + fresh Reviewer | Medium | Evidence/wording check only |

Fixed cap: one Track 1 build, one independent review, at most one repair, and
one focused recheck. No prototype round is planned because ADR-0031 and
ADR-0046 already settle the relevant contracts; Track 1 is implementation
against them. Any need for a new schema, presentation contract, or boundary
meaning stops the track rather than widening it.

## Execution record

| # | Unit | Role | Prompt | Outcome |
| --- | --- | --- | --- | --- |
| 0 | Milestone selection and plan | Foreman | Owner direction, 2026-07-26: begin another presentation milestone | Planning PR prepared |
