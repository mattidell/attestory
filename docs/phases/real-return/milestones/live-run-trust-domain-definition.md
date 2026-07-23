# Milestone: Live-Run System Definition and Trust Domains

Status: **approved — amended 2026-07-23.** This is a records-and-ADR
milestone. It does not authorize a new prototype, feasibility experiment, or
seat dispatch.

## Objective

Record the system boundary already indicated by the project’s existing
evidence. The privacy-critical live-run environment is a distinct trust domain:
it reads real workspace data and consumes an adopted, byte-verified package;
the developer/supply environment prepares and publishes source but has no
standing access to that workspace. The milestone makes this system definition,
its threat posture, and its residual risks explicit in a Tier 3 ADR.

## Why this is records work, not a new prototype

The unanswered question is no longer whether a distinct live-run domain is the
right system definition. ADR-0031's residency posture, ADR-0033's verified
adoption boundary, and the stopped Guarded Transport H1 prototype already
establish the relevant reasoning: a determined same-UID process cannot be
treated as separated from an accessible durable credential, so a developer-host
wrapper is not the privacy boundary around real data.

The existing prototype's failed positive confinement topology is not re-run or
repaired here. Its independently reviewed negative finding is assembled as
cited decision evidence. A later implementation milestone may prototype an
enforcement substrate (for example, a separate OS user) once there is a need to
choose one; that prototype would answer workflow and host-capability questions,
not revisit this system definition.

## Scope

1. Define Developer/Supply, Live-Run Data, Publication, and Owner
   Authorization domains: assets, identities, credentials, storage, network
   authority, allowed crossings, and refusal behavior.
2. State the threat posture precisely. The live-data boundary protects against
   an unprivileged developer/supply identity; it does not claim protection from
   an owner-authorized elevation or administrator/root.
3. Produce a cited decision-evidence analysis from existing records, including
   the Guarded Transport H1 reviews/triage, ADR-0031, ADR-0032, ADR-0033, and
   the current push-envelope audit. The analysis must distinguish evidence for
   the system definition from evidence that would be needed to select a future
   enforcement substrate.
4. Produce a Tier 3 ADR and required plain-language analysis. The ADR must
   clarify that guarded transport is a developer-publication integrity posture,
   not the privacy boundary for the live-run data domain, while retaining
   ADR-0031's residency/classification/provenance controls.

## Explicit non-goals

- No new prototype iteration, synthetic capability probe, container/VM trial,
  separate-UID setup, or feasibility measurement.
- No real workspace, document, credential, remote, live run, or owner
  attestation is used or recorded.
- No credential store, Keychain ACL, server-side gate, push proxy, or transport
  implementation is selected or built.
- No L3-to-L4 maturity claim is made.
- Schema-publication controls and builder/reviewer scope controls are tabled
  by owner direction; this milestone neither designs nor implements them.
- No governance document changes are proposed.

## Decision and evidence surface

The decision is Tier 3: application system definition and trust-domain
posture. It is bounded by ADR-0005, ADR-0013, ADR-0030, ADR-0031, ADR-0032,
ADR-0033, and ADR-0034; Constitution Article 18 and Engineering Constraints
E18.1/E18.2 remain binding.

The new ADR must cite the existing prototype evidence directly: in particular,
`docs/prototypes/guarded-transport/round-1-triage.md` and
`docs/prototypes/guarded-transport/repair1-triage.md`, alongside their
independently contexted reviews. That evidence supports a narrow conclusion:
same-UID local credential confinement is not established. It does **not** prove
that any particular OS, VM, or container configuration is ready to deploy; the
ADR must say so.

## Verification and data safety

Verification is documentary and traceable: every assertion in the ADR's
evidence analysis maps to a source record, the predecessor ADR text, or the
current implementation/audit. Review verifies that no claim of operational
isolation or maturity lift appears without a later implementation milestone and
real-run verification. The ordinary verification floor remains required for
records changes: unit suite, mypy, governance lint, and envelope scan.

All work is records-only. Real data is neither consulted nor named. Owner
attestation belongs only to a later live-run implementation milestone before
any L4 privacy-boundary claim.

## Exit criteria

1. A reader can identify the systems, assets, authorities, and crossings
   without inferring them from a convenient developer workflow.
2. The ADR's evidence analysis cites existing prototype and project records,
   including their limits, without implying a new feasibility result.
3. The accepted ADR unambiguously separates live-data privacy posture from
   developer publication integrity and resolves its relationship to ADR-0031.
4. Completion records state that the data-boundary maturity row remains L3 and
   name the later implementation/real-run gate for any L4 claim.

## Tracks

### Track 0 — Evidence synthesis

Write the cited prototype evaluation/decision analysis from existing artifacts.
No new experiment, configuration, fixture, or prototype branch is created.

### Track 1 — Decision record

Draft the Tier 3 ADR and its required plain-language companion after Track 0
evidence is independently reviewed. It may clarify or supersede only the
relevant framing in ADR-0031; it does not rewrite accepted history in place.

### Track 2 — Completion records

Update phase state, roadmap, handoff, retrospective, and any necessary
maturity-matrix rationale. Do not lift the matrix level.
