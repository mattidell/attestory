# Presentation — Citation Walk Track 1 Charter (Renderer and Fixtures)

Status: **prepared, not launchable.** This record authorizes scope; it does
not authorize a foreman dispatch. Dispatch requires the owner's literal
string `I authorize dispatch` in a live thread, single-use and bound to this
charter (`AGENTS.md#Dispatch authorization`).

## Context Capsule

- **Source ref:** `main` at `62736e517e76390fe833b93555e726a26a165c29` (PR #73
  merge — ADR-0046 ratified, milestone plan owner-approved).
- **Exact object:** a fresh implementation branch off that commit. No prior
  branch is adopted; this is new code against real schemas, not a fork of the
  Presentation Exploratory Milestone's synthetic reference prototypes
  (`docs/prototypes/human-presentation-citation-walk/reference/prototypes/cycle5-{a,b}`),
  which may be read as a settled-criteria checklist only.
- **Role:** one Builder, Medium tier / medium effort
  (`docs/phases/real-return/milestones/presentation-citation-walk.md#Economical execution`).
- **Scope:** build a citation-walk renderer that consumes
  `form-field.v3`/`act-derived-publication.v1` output and satisfies every
  ADR-0046 requirement and foreclosure. Cover the full `dispositions`
  instruction-kind matrix (`published_value`, `computed_zero`,
  `closure_backed_zero`, `blocked`, and any other declared kind) with
  committed synthetic fixtures. Write
  `tools/presentation_harness/examples/manifests/citation-walk.v1.json`
  reproducing the standardized tamper suite (T1 inject-on-blocked-line, T2
  non-numeric published value, T3 unknown line status) against the real
  renderer, plus the derived/diagnostic-value-under-blocked-input case and
  the citation-identity-under-reuse case.
- **Evidence-rung ceiling:** presentation-layer consumer only. No
  derivation/kernel/schema change to `form-field.v3` or
  `act-derived-publication.v1`. No new framework, build step, or external
  dependency — single self-contained module(s), `createElement`/`textContent`
  only, no `innerHTML`. No presentation-economy treatment comparison or
  savings claim. No second schedule attachment or income domain. No
  data-boundary mechanism change.
- **Stop conditions:** stop and route back to the foreman if closing a
  disposition case would require changing `form-field.v3` or
  `act-derived-publication.v1`; if a new dependency, framework, or build step
  seems necessary; if satisfying ADR-0046 seems to require revisiting one of
  its three resolved rule-points (redact policy, derived-value zero-authority,
  blocked-state salience); or if real workspace, credential, remote, or
  personal data would be needed for any fixture.
- **Full reads before acting:** this charter; `docs/roles/builder.md`;
  `docs/adr/0046-presentation-surface-contract.md`; the milestone plan's
  Objective, Current state, Scope, Non-goals, Contracts, Fixtures,
  Verification, Data safety, and Exit criteria
  (`docs/phases/real-return/milestones/presentation-citation-walk.md`);
  `packages/schemas/tax/form-field.v3.schema.json`;
  `packages/schemas/derivation/act-derived-publication.v1.schema.json`;
  `docs/prototypes/human-presentation-citation-walk/analysis/01-feature-citation-walk.md`
  (settled criteria, read as checklist); `AGENTS.md#Fixture Rules`;
  `AGENTS.md#Data Safety Rules`.

Before editing, echo the resolved source commit, object, scope, evidence
ceiling, and stop conditions. Confirm the ADR-0046 requirement/foreclosure
list and the three resolved rule-points before writing any renderer code.

## Verification before handoff

```text
node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/citation-walk.v1.json
git diff --check main..HEAD
```

Exit `0` is required. The Builder does not need to rerun the runner's own
F1–F6 floor (isolation, injection integrity, cleanup, confinement,
validation, redacted failures) — that is already proven and credited to the
completed runner; only the citation-walk content and its manifest are new
evidence here.

## Handoff

On completion, route to Track 2 (Focused independent review) per the
milestone plan's role table. The Reviewer credits the runner's own F1–F6
floor and checks only ADR-0046 conformance and the fault-injection
reproductions this charter required.
