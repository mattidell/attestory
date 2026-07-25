<!-- foreman-context-v1
{
  "version": 1,
  "topic": "live-run-trust-domains",
  "status": "complete; ADR-0044 accepted by owner 2026-07-23; publication PR #61 pending owner merge",
  "scope": [
    "draft the specified Tier 3 system-definition ADR and plain-language companion",
    "state Developer/Supply, Live-Run Data, Publication, and Owner Authorization domains",
    "review the drafted ADR against its specified shape and cited existing records"
  ],
  "non_goals": [
    "no prototype, evidence-synthesis artifact, or committee as a prerequisite",
    "no real workspace, credential, remote, live run, or owner attestation",
    "no enforcement-substrate selection or L3-to-L4 maturity claim"
  ],
  "deep_reads": {
    "adr_draft": [
      "docs/adr/0031-real-data-residency-boundary.md#Decision",
      "docs/adr/0032-contribution-boundary.md#Decision",
      "docs/adr/0033-production-package-resolver.md#Decision",
      "docs/prototypes/guarded-transport/round-1-triage.md",
      "docs/prototypes/guarded-transport/repair1-triage.md",
      "docs/phases/real-return/milestones/push-envelope-preflight-and-bypass-visibility.md",
      "docs/governance/constitution.md#Article 18 — Quarantine",
      "docs/governance/engineering-constraints.md#E18.1 (Quarantine) — Structural walls",
      "docs/governance/engineering-constraints.md#E18.2 (Quarantine) — Egress hygiene"
    ],
    "adr_review": [
      "docs/roles/reviewer.md",
      "docs/roles/foreman.md#Standing disciplines"
    ],
    "merge_or_records": [
      "docs/adr/0030-branch-and-merge-strategy.md#Decision",
      "PROJECT_PLANNING.md#Branch, PR, and Merge Protocol"
    ]
  }
}
-->
# Milestone: Live-Run System Definition and Trust Domains

Status: **complete — ADR-0044 accepted by owner direction 2026-07-23;
publication PR #61 pending owner merge.** The bounded review returned READY with
no blocking finding. The milestone changes no implementation or maturity
claim.

## Objective

Write the bounded Tier 3 ADR that makes the project’s existing system boundary
plain: real data belongs to a Live-Run Data trust domain; Developer/Supply
prepares publishable source but has no standing authority to read that data;
the adopted, byte-verified package is the intended supply crossing. This
milestone defines the system and posture. It does not implement an enforcement
substrate.

## Owner-authorized process deviation

For this milestone only, the owner authorizes a direct ADR-and-companion path
instead of the default new-prototype/evaluation-analysis/committee sequence in
`PROJECT_PLANNING.md`. The decision may rely directly on the accepted boundary
ADRs and completed Guarded Transport and push-envelope records already named
below. This deviation waives no data-safety, evidence-honesty, ADR,
plain-language-analysis, or verification requirement; it authorizes no L4
claim and no implementation work.

This plan is the complete direction for the next foreman: draft the ADR in the
shape below. Do not create an evidence-synthesis artifact, a new prototype
topic, or a feasibility experiment as a prerequisite. A review may be chartered
only after the ADR is drafted, and reviews that ADR against this shape and its
cited records — not as a prototype committee or a new evidence phase.

## Required ADR shape

The new ADR is Tier 3 and links its required non-normative companion near the
top. It has these bounded sections:

1. **Context — system versus developer workflow.** Explain that a developer
   workstation convenience arrangement is not the application’s privacy
   boundary; distinguish logical trust domains from a later mechanical
   enforcement choice.
2. **Decision — four domains.** Define Developer/Supply, Publication,
   Live-Run Data, and Owner Authorization by their assets and authorities.
3. **Decision — permitted crossings.** State: Developer/Supply → Publication
   carries only publication-eligible material; Publication → Live-Run Data
   carries only a current adopted, byte-verified package; Owner Authorization
   supplies deliberate residency/contribution/adoption/run authority; no
   descriptive live artifact crosses back.
4. **Decision — threat posture and residuals.** The claimed posture concerns
   an unprivileged Developer/Supply authority once a later implementation
   enforces the separation. Owner-authorized elevation and administrator/root
   are explicit residuals, not hidden exclusions.
5. **Decision — guarded transport.** Reframe guarded transport as a
   Developer/Supply → Publication integrity control. Preserve ADR-0031’s
   residency, classification, provenance, and sensitivity rules; state that
   hook protection is conditional, `--no-verify` bypass remains reachable, and
   credential confinement is unestablished.
6. **Consequences — future implementation gate.** Select no OS user,
   container, VM, credential store, proxy, or hosted mechanism. The data
   boundary remains L3. A later milestone must select and test one substrate,
   then perform its required real-run verification before any L4 claim.
7. **Links and evidence limits.** Cite ADR-0031/0032/0033, the two Guarded
   Transport triages and their reviews, and Push-Envelope Preflight. State that
   the stopped same-UID work rejects only its tested shapes; it is not a general
   impossibility theorem.

## ADR review shape

After the ADR and companion exist, a chartered reviewer checks only whether the
draft matches the seven required sections, its cited records support the stated
claims and limits, it introduces no unplanned enforcement claim, and its
companion accurately explains the decision. The reviewer does not recreate a
prototype committee, demand a rival design, or require an evidence-synthesis
artifact. Any dispatch for that role follows the owner/foreman process in force
at the time; it is not created by this plan.

## Scope

- Draft the ADR and companion in the required shape.
- Use existing accepted records as citations; accurately preserve their limits.
- Charter the bounded ADR review after drafting.
- Update only the active plan pointers and completion records needed to make
  the ADR’s relationship to guarded transport unambiguous.

## Explicit non-goals

- No new prototype, evaluation analysis, committee, evidence-synthesis record,
  or feasibility measurement.
- No real workspace, document, credential, remote, live run, or owner
  attestation.
- No separate-UID, container, VM, Keychain, server-side gate, push proxy, or
  credential implementation.
- No L3-to-L4 maturity lift.
- Schema-publication controls and builder/reviewer scope controls remain
  tabled.
- No general governance change is implied by this milestone-specific deviation.

## Verification and data safety

Verify that the ADR matches the required shape; every cited record exists and
is not overstated; its companion is linked; and no operational isolation,
maturity lift, or implementation commitment is implied. The ADR review checks
the same bounded claims. Run the ordinary records verification floor: unit
suite, mypy, governance lint, and envelope scan. All work remains
synthetic/non-descriptive; real data is neither consulted nor named.

## Exit criteria

1. The new ADR and companion have the required shape and direct citations.
2. A reader can identify systems, authorities, crossings, and residuals without
   mistaking developer workflow for the privacy boundary.
3. Guarded transport is accurately placed as publication integrity, not
   live-data privacy.
4. The bounded ADR review is complete; it made no prototype-process demand.
5. The L3 row remains unchanged and the later L4 gate is explicit.

## Tracks

### Track 0 — Direct ADR draft

Draft the ADR and plain-language companion in the required shape. No preceding
prototype, evidence-synthesis artifact, or review role is required.

Status: **complete.** ADR-0044 and its plain-language companion follow the
owner-authorized direct path and the seven-section shape above.

### Track 1 — ADR review and records

Charter and complete the bounded ADR review, then record the owner’s ADR
disposition and update milestone completion records. The review remains a
review of the ADR, not a new prototype process.

Status: **complete.** The owner directly took the reviewer seat before
returning to the foreman seat. The review at
`docs/reviews/2026-07-23-live-run-system-trust-domains-adr-review.md` returned
READY with no blocking finding. The owner then accepted ADR-0044 and directed
milestone closure and publication through a PR; merge remains owner-held under
ADR-0030.
