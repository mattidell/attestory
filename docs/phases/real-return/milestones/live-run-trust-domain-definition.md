<!-- foreman-context-v1
{
  "version": 1,
  "topic": "live-run-trust-domains",
  "status": "planning only; no charter or dispatch authorized",
  "seat": "docs/prototypes/live-run-trust-domains/SEAT.md",
  "scope": [
    "define Developer/Supply, Live-Run Data, Publication, and Owner Authorization domains",
    "compare coupled and separate-live-identity postures with synthetic evidence only",
    "resolve guarded transport's relation to the live-data boundary"
  ],
  "non_goals": [
    "no real workspace, credential, remote, live run, or owner attestation",
    "no enforcement substrate, credential store, push proxy, or transport implementation",
    "no L3-to-L4 maturity claim"
  ],
  "deep_reads": {
    "dispatch": [
      "AGENTS.md#Prototype-process dispatch",
      "docs/adr/0005-prototype-evidence-for-consequential-adrs.md#Decision",
      "docs/adr/0013-prototype-economic-gates.md#Decision",
      "docs/adr/0034-explicit-owner-approval-for-every-dispatch.md#Decision",
      "docs/prototypes/live-run-trust-domains/plan.md#Gate 8 — seats and authority"
    ],
    "adr_draft": [
      "docs/adr/0031-real-data-residency-boundary.md#Decision",
      "docs/adr/0032-contribution-boundary.md#Decision",
      "docs/adr/0033-production-package-resolver.md#Decision",
      "docs/governance/constitution.md#Article 18 — Quarantine",
      "docs/governance/engineering-constraints.md#E18.1 (Quarantine) — Structural walls",
      "docs/governance/engineering-constraints.md#E18.2 (Quarantine) — Egress hygiene"
    ],
    "new_milestone": [
      "PROJECT_PLANNING.md#Required Milestone Plan Contents",
      "docs/milestone-retrospectives/2026-07-22-push-envelope-preflight-and-bypass-visibility.md",
      "docs/milestone-retrospectives/2026-07-22-correction-authority-and-marshaller-simplification.md",
      "docs/milestone-retrospectives/2026-07-21-dividends-and-schedule-b-slice.md",
      "docs/milestone-retrospectives/2026-07-18-first-real-return-slice.md",
      "docs/milestone-retrospectives/2026-07-15-core-tax-conditions-and-presentation-integration.md"
    ],
    "schema_or_fixture": [
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "merge_or_records": [
      "docs/adr/0030-branch-and-merge-strategy.md#Decision",
      "docs/roles/foreman.md#Standing disciplines",
      "PROJECT_PLANNING.md#Milestone Execution Branch Protocol"
    ]
  }
}
-->
# Milestone: Live-Run Trust-Domain Definition

Status: **draft — owner-selected direction, 2026-07-23.** This plan authorizes
planning only. The owner must approve the prototype plan and each later seat
dispatch under ADR-0034.

## Objective

Make the boundary around an actual return run explicit and evidence-backed.
The decision is whether the privacy-critical live-run environment is a distinct
trust domain: it consumes an adopted, byte-verified package and real workspace
data, while the developer/supply environment publishes source but cannot read
that workspace. The milestone produces a Tier 3 decision record; it does not
implement the boundary.

## Current state and decision pressure

ADR-0031 truthfully establishes out-of-repository residency and a local
synthetic push-envelope audit, but its intended guarded-transport hardening
stalled. The production resolver and the owner-held live-run workflow already
show a more useful system shape: source is prepared in a developer/supply
environment, then an adopted package is consumed in a privacy-sensitive run.
The unmade decision is which of these environments are separate systems, what
crosses between them, and whether developer-side Git transport is a data
boundary or a separate publication-integrity posture.

## Scope

1. Define the Developer/Supply, Live-Run Data, Publication, and Owner
   Authorization trust domains: assets, identities, credentials, storage,
   network authority, and permitted crossings.
2. Compare the coupled developer-host posture with a separate live-run OS
   identity that has real-workspace access but no Git credential or publication
   path. Containers or VMs may be evaluated as enforcement substrates; they
   are not assumed to be a security boundary merely because they are scriptable.
3. If the paper analysis leaves a host-capability question open, run a
   synthetic-only capability probe with temporary identities, a dummy workspace,
   a synthetic adopted package, and dummy endpoints.
4. Produce a Tier 3 ADR and its required plain-language analysis after the
   prototype evidence and owner disposition. It must state whether guarded
   transport remains a live-data-boundary concern or becomes an independent
   developer-publication posture.

## Explicit non-goals

- No real workspace, document, credential, remote, live run, or owner
  attestation is used or recorded.
- No credential store, Keychain ACL, server-side gate, push proxy, or transport
  implementation is selected or built.
- No L3-to-L4 maturity claim is made.
- Schema-publication controls and builder/reviewer scope controls are tabled
  by owner direction; this milestone neither designs nor implements them.
- No governance document changes are proposed.

## Decision and contract surface

The primary decision is Tier 3: the application system definition and its
trust-domain posture. A tightly dependent Tier 3 decision determines the
proper status and framing of ADR-0031's guarded transport. The decision is
bounded by ADR-0005, ADR-0013, ADR-0030, ADR-0031, ADR-0032, ADR-0033, and
ADR-0034; Constitution Article 18 and Engineering Constraints E18.1/E18.2
remain binding.

The prospective claim is deliberately narrow: against an unprivileged
developer/supply identity, the live-run domain protects the real workspace and
does not have authority to publish source. It explicitly excludes an owner who
authorizes elevation and an administrator/root adversary. The ADR must name
all residual risk rather than treating an operating-system user as a complete
workstation security model.

## Fixtures and verification

Paper evidence must include a domain/crossing map, positive and negative
capability cases, a lifecycle from package adoption through private output, and
an authority/failure map for each crossing. If a probe is necessary, it must
prove at least:

- developer/supply cannot read the synthetic live workspace;
- the live identity cannot use a Git credential, make a direct publication, or
  reach the deliberately named synthetic egress endpoint;
- the live identity can consume only the intended synthetic adopted package.

The ordinary verification floor remains required for records changes:
unit suite, mypy, governance lint, and envelope scan. Prototype-specific checks
are defined in `docs/prototypes/live-run-trust-domains/plan.md`.

## Data safety

All evidence is synthetic. Real data is neither consulted nor named. Owner
attestation is a later implementation/live-run milestone concern, before any
claim that the privacy boundary is operational at L4.

## Exit criteria

1. The domain and crossing map is traceable to assets and authorities, not a
   diagram of convenient processes.
2. Clean-room rival evidence identifies the cheapest posture sufficient for the
   stated unprivileged-developer threat.
3. The owner can ratify a Tier 3 ADR or stop/defer the topic from the evidence.
4. The ADR unambiguously resolves the relation to guarded transport without
   retaining contradictory same-UID/L4 language.
5. Completion records state that the data-boundary maturity row remains L3
   until a separately planned implementation and real-run verification.

## Tracks

### Track 0 — Prototype evaluation

Run the Gate 0–8 plan at
`docs/prototypes/live-run-trust-domains/plan.md`. No seat is authorized by this
planning record; each builder or reviewer launch needs immediate owner approval.

### Track 1 — Decision record

After accepted prototype evidence and owner disposition, draft the Tier 3 ADR
and required plain-language analysis. It may clarify or supersede the relevant
portion of ADR-0031 only where the new decision actually changes it.

### Track 2 — Completion records

Update phase state, roadmap, handoff, retrospective, and any necessary
maturity-matrix rationale. Do not lift the matrix level.
