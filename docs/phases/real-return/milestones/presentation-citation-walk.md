<!-- foreman-context-v1
{
  "version": 1,
  "topic": "presentation-citation-walk",
  "milestone_state": "planned",
  "retrospective": null,
  "status": "Owner-approved 2026-07-25 on ADR-0046 (ratified same day). Ready for a charter; no dispatch has occurred.",
  "scope": [
    "render the real citation walk against actual derivation output (form-field.v3 + act-derived-publication.v1), not a synthetic fixture",
    "satisfy ADR-0046's Presentation Surface Contract end to end",
    "verify with the completed browser evaluation runner as the review harness",
    "raise the Presentation aspect of the maturity matrix from L3-with-shim toward a real human surface",
    "one focused independent review against ADR-0046 plus the runner's F1-F6 floor"
  ],
  "non_goals": [
    "no new tax computation, form-field, or citation content",
    "no schema change to form-field.v3 or act-derived-publication.v1",
    "no presentation-economy treatment comparison or savings claim",
    "no second schedule attachment or income domain",
    "no data-boundary mechanism change",
    "no real workspace, credential, remote, or personal output"
  ],
  "deep_reads": {
    "implementation": [
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/prototypes/human-presentation-citation-walk/analysis/01-feature-citation-walk.md",
      "docs/prototypes/human-presentation-citation-walk/reference/prototypes/cycle5-a",
      "packages/schemas/tax/form-field.v3.schema.json",
      "packages/schemas/derivation/act-derived-publication.v1.schema.json",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/adr/0046-presentation-surface-contract.md",
      "docs/prototypes/human-presentation-citation-walk/analysis/01-feature-citation-walk.md"
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
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules",
      "docs/governance/constitution.md#Article 18 — Quarantine"
    ],
    "new_milestone": [
      "docs/phases/real-return/maturity-matrix.md",
      "docs/milestone-retrospectives/2026-07-24-presentation-exploratory-milestone.md",
      "docs/milestone-retrospectives/2026-07-25-browser-evaluation-runner-completion.md"
    ]
  }
}
-->
# Milestone: Presentation — Citation Walk on Real Derivation Output

Status: **owner-approved plan; ready for a charter.** No dispatch has
occurred — dispatch still requires the owner's literal string
`I authorize dispatch` per `AGENTS.md`.

## Objective

Build the real, human-facing citation walk — the page a filer actually reads
— against actual derivation output, satisfying ADR-0046's Presentation
Surface Contract, and raise the Presentation aspect of the maturity matrix
from its current L3-with-shim ("form-field disposition content, not a human
surface") to a genuine human surface with L3 evidential grounding (Ontology
§8).

## Current state

`form-field.v3` already carries everything a renderer needs and says so in
its own description: "rendering remains a future consumer concern (ADR-0012
amendment; ADR-0029)." Each resolved field carries a `citation` pin and a
`dispositions` object (`published_value` / `computed_zero` /
`closure_backed_zero` / `blocked` / …). `act-derived-publication.v1` is the
companion derived-finding shape (ADR-0009). Nothing in the derivation or
kernel layer needs to change; this milestone is the first "future consumer."

The Presentation Exploratory Milestone (2026-07-24) built and adversarially
tested a synthetic stand-in for this exact page across five cycles and left
worked reference implementations. ADR-0046 (2026-07-25) ratifies the
invariant set that exploration converged on, resolving all three open
rule-points. The Browser Evaluation Runner Completion milestone (2026-07-25,
PR #71) finished the general browser-evaluation tool — `node
tools/presentation_harness/run.mjs --manifest <path>` — as trustworthy
tooling capable of driving and verifying exactly this kind of surface. All
three prerequisites this milestone depends on are complete and merged to
`main`.

## Scope

1. Build a renderer that consumes `form-field.v3` + `act-derived-publication.v1`
   output from an existing resolved run and produces the citation walk:
   line → subtotal → per-source disposition → citation pin → source fact.
2. Satisfy every ADR-0046 requirement and foreclosure, including the three
   resolved rule-points (derived/diagnostic values are zero-authority;
   blanket redact on rejected values; section-level blocked-state salience).
3. Cover the full range of `dispositions` states the schema defines
   (`published_value`, `computed_zero`, `closure_backed_zero`, `blocked`, and
   any other declared instruction kind), not only the happy path.
4. Reuse the exploratory milestone's settled, mechanized criteria (six
   citation-walk criteria, class 1–4 in
   `docs/prototypes/human-presentation-citation-walk/analysis/01-feature-citation-walk.md`)
   as a starting checklist rather than re-deriving them.
5. Write a browser-evaluation-runner manifest exercising this real surface
   with the standardized tamper/fault cases (T1 inject-on-blocked-line, T2
   non-numeric published value, T3 unknown line status) plus the
   dispositions-coverage cases from item 3.
6. One focused independent review against ADR-0046 and the runner's F1–F6
   floor (network confinement, storage isolation, injection integrity,
   cleanup, deterministic output — all already proven by the runner itself;
   the review's job is the *content* satisfying the contract, not
   re-proving the harness).

## Non-goals

- No change to `form-field.v3`, `act-derived-publication.v1`, or any
  derivation/kernel content — this is a presentation-layer consumer only.
- No presentation-economy treatment comparison, cost claim, or savings claim
  — Track 0's contracts remain available but are not this milestone's
  subject.
- No second schedule attachment, income domain, or new tax computation.
- No data-boundary mechanism change; this surface renders already-resolved,
  already-published dispositions and adds no new crossing.
- No real workspace, owner browser, credential, remote URL, or personal
  output — synthetic resolved-run fixtures only, per Data Safety.
- No re-litigation of ADR-0046's three resolved rule-points within this
  milestone; a future ADR may revisit them with real-filer evidence this
  milestone's review is not chartered to gather.

## Contracts

### Renderer

- Consumes exactly the citizens ADR-0046 already assumes: `form-field.v3`
  records with a `citation` pin and a `dispositions` object, plus
  `act-derived-publication.v1` for derived/composite lines.
- Single frozen source object per render; one render-path-per-citation
  function, called from every citation site for that field (Requirement 1).
- No `innerHTML`; construct nodes only.
- Self-contained: no framework, no build step, no new dependency — the
  exploratory milestone's ten independent builder runs converged on this
  unprompted, and it keeps the surface auditable by the same tooling that
  already exists (the browser evaluation runner needs nothing new to drive
  it).

### Verification surface

- A committed manifest at
  `tools/presentation_harness/examples/manifests/citation-walk.v1.json`,
  matching the completed runner's existing `examples/manifests/` convention
  (`smoke.v1.json`, `invalid-cases.v1.json`), drives the real citation walk
  through the runner.
- Fault-injection and tamper cases from the exploratory milestone's tamper
  suite (T1–T3) are reproduced against the real renderer, not the synthetic
  one.

## Fixtures

Synthetic resolved-run outputs only — hand-constructed `form-field.v3` /
`act-derived-publication.v1` instances covering: a fully published line, a
`computed_zero` line, a `closure_backed_zero` line, a `blocked` line with its
missing-fact/remedy text, a derived/diagnostic value with one blocked input
(the zero-authority side-channel case ADR-0046 forecloses), and a reused
citation across two lines (identity-under-reuse case). No fixture may
reference real form content beyond what already exists in the repository's
committed sample data (`packages/sample_data/`).

## Verification

```text
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
```

Exit `0` requires every ADR-0046-derived criterion to pass against the real
renderer, across the full dispositions-state matrix in Scope item 3, plus the
inherited F1–F6 floor the runner itself already guarantees (isolation,
injection integrity, cleanup, confinement, validation, redacted failures —
not re-verified here, only relied upon).

## Data safety

Only constructed, committed synthetic `form-field.v3` /
`act-derived-publication.v1` fixtures. No real workspace, owner browser,
credential, remote URL, or quarantined data. The renderer itself adds no new
data-boundary crossing — it consumes only already-resolved, already-published
dispositions that exist purely as repository-committed fixtures for this
milestone.

## Exit criteria

1. The renderer satisfies every ADR-0046 requirement and foreclosure,
   verified by execution (fault injection), not documentation claims.
2. All `dispositions` instruction kinds the schema declares are covered by at
   least one rendered and one blocked/degraded fixture case.
3. The three ADR-0046 resolved rule-points are demonstrably enforced:
   derived values disappear when their inputs are invalid; rejected values
   never appear in visible text; blocked-state signals stay section-level.
4. The standardized tamper suite (T1–T3) fails closed against the real
   renderer.
5. The browser-evaluation-runner manifest passes with exit `0`.
6. One focused independent review confirms 1–5 and finds no ADR-0046
   violation.
7. The retrospective records the maturity-matrix Presentation cell claim with
   its Ontology §8 evidential basis, or explicitly declines the claim with
   the smallest exact gap if review returns short of readiness.

## Tracks

### Track 1 — Real citation-walk renderer and fixtures

**Goal:** build the renderer against real derivation-output schemas and cover
the full dispositions-state matrix.

**Boundary:** presentation-layer consumer only; no derivation/kernel/schema
change; no new dependency or framework.

**Inputs:** ADR-0046; `form-field.v3`/`act-derived-publication.v1` schemas;
exploratory milestone's settled criteria and reference implementations
(as a starting pattern, not committed content — the real renderer is new
code against real schemas, not a fork of the synthetic prototype).

**Outputs:** renderer module(s), committed synthetic fixtures across the
dispositions-state matrix, a citation-walk manifest for the browser
evaluation runner.

**Verification:** runner manifest passes; each Scope item 3/6 case has an
executable check, not a doc claim.

**Migration risk:** none — additive presentation-layer consumer.

**Data safety:** synthetic committed fixtures only.

### Track 2 — Focused independent review

**Goal:** verify the renderer against ADR-0046 and confirm no violation
survives adversarial execution.

**Boundary:** content/contract correctness only; relies on the runner's own
F1–F6 floor rather than re-proving harness trustworthiness.

**Inputs:** Track 1 diff, ADR-0046, the runner manifest and its result.

**Outputs:** one review record with a `READY`/`NOT READY` verdict and, if
`NOT READY`, the smallest exact residual.

**Verification:** independent reproduction of the fault-injection/tamper
suite; inspection against every ADR-0046 clause.

**Migration risk:** none — review only.

**Data safety:** synthetic fixtures only; no real data ever enters review
scope.

## Economical execution

Role allocation, per the same craft rules the last two milestones used:

| Unit | Role | Tier / effort | Boundary |
| --- | --- | --- | --- |
| Track 1 | Builder | Medium / medium | New renderer against real schemas; reuse settled criteria as checklist, not code fork |
| Track 2 | Reviewer | High / medium | ADR-0046 conformance and fault-injection reproduction; credits the runner's own F1–F6 evidence rather than re-deriving it |

Fixed cap: one Track 1 implementation and one Track 2 review. A remaining
`NOT READY` residual returns to the owner for disposition rather than an
automatic second cycle, consistent with the last two milestones' discipline.

## Owner approval

The owner selected this milestone (2026-07-25), approved ADR-0046's evidence
bar and its three resolved rule-points, and confirmed this plan's scope,
tracks, and exit criteria plus the manifest path above. This plan and ADR-0046
are ready for a charter; no dispatch has occurred, and dispatch still requires
the owner's literal string `I authorize dispatch` per `AGENTS.md`.
