# Prototype Plan: Live-Run Trust Domains

Status: **draft — proposed to owner** (foreman, 2026-07-23). This plan is a
decision gate, not standing authorization to consume a builder or reviewer
seat.

Related milestone: `docs/phases/real-return/milestones/live-run-trust-domain-definition.md`.

## Gate 0 — Decision inventory

| ID | Decision | Tier and pressure | Required evidence |
| --- | --- | --- | --- |
| TD1 | Is the live return run a distinct trust domain from developer/supply, with a narrow adopted-package crossing and no publication authority? | Tier 3; score 8 | Rival designs plus authority and failure analysis. |
| TD2 | Does guarded transport remain part of the live-data boundary, or is it an independent developer-publication hygiene posture? | Tier 3; score 7 | Consequence analysis tied to TD1 and ADR-0031. |
| TD3 | Which substrate enforces a chosen boundary (separate OS user, VM, container, or other)? | Deferred implementation decision | No selection unless evidence shows it is indispensable to decide TD1. |

## Gate 1 — why prototype

The boundary is a product/security posture, not a file-layout choice. Same-UID
processes on a developer host can generally inspect each other's accessible
credentials and storage; therefore a claim of isolation needs an identity or
equivalent authority boundary, not a wrapper alone. The unresolved question is
not whether a Unix UID has documented permissions, but whether the complete
workflow preserves the intended crossings without reintroducing publication,
egress, package substitution, or owner-disabling friction.

## Gate 2 — declared cases

Positive cases:

1. Developer/supply may build and publish synthetic source/package material,
   but cannot read the synthetic live workspace.
2. Live-run may read a synthetic live workspace and consume the named adopted
   package, but cannot use a Git credential or publication route.
3. Owner authorization may intentionally initiate the crossing without
   granting the developer identity ongoing live-workspace authority.

Negative cases:

1. A coupled same-UID developer process has both a reachable live workspace and
   a durable publication credential.
2. A nominally separate live identity retains a writable publication mount,
   developer-readable workspace, or arbitrary egress.
3. A package handoff that does not identify the adopted bytes is substituted
   after developer preparation.

Lifecycle: developer prepares package -> owner adopts/verifies package -> owner
initiates live run -> live domain creates private output -> only the existing
non-descriptive attestation may cross back. The evidence must name the producer
authority, consumer authority, and failure behavior at each arrow.

## Gate 3 — prototype rung

Start at Rung 1 (paper authority/crossing analysis). Escalate only to a
synthetic Rung 3 capability probe if the chosen host's actual permissions or
network behavior is a decision-blocking uncertainty. A container supplies
useful process packaging evidence, but does not alone demonstrate protection
from a host process with equivalent authority. The Rung 3 question is:

> Can the selected host deny an unprivileged developer identity access to a
> synthetic live workspace while denying the live identity Git credentials and
> named egress, yet allowing it to consume an adopted synthetic package?

No real data, credentials, remote, or owner attestation is permitted at any
rung.

## Gate 4 — evidence shape and separation

If builders are launched, commission two independently contexted clean-room
shapes: one analyzes a separate-identity live domain, and one attacks it or
proposes the least-coupled viable alternative. A single repair pass may address
a review finding. Independently contexted reviewers assess governance and
adversarial capability claims against declared checks, not impressions. The
builder never reviews its own work; the foreman does not review prototype
artifacts it authored. Every dispatch requires contemporaneous owner approval
under ADR-0034.

## Gate 5 — triage boundaries

Evidence may conclude: accept TD1; retain the coupled posture with an honest
rescope; or defer for an explicit implementation prototype. Server-side gates,
credential-store mechanisms, schema publication controls, and builder/reviewer
scope controls are out of charter. Do not smuggle them in as a solution.

## Gate 6 — convergence test

The evidence converges only if it names: the domains; allowed crossings; exact
unprivileged-developer claim; administrator/owner residual risk; the outcome
for TD2; and a later implementation gate. The resulting ADR may defer a
substrate, but may not claim same-UID isolation without evidence.

## Gate 7 — artifact handling

Prototype code/configuration lives only on `prototypes/live-run-trust-domains/it<N>`
branches and is preserved as exhibit tags when an iteration closes; it never
merges to `main`. Only records under this topic may merge. A later boundary
implementation is a separately planned milestone.

## Gate 8 — seats and authority

| Seat | Tier | State |
| --- | --- | --- |
| Prototype foreman | High | Owner appointed for planning only. |
| Clean-room builder A | High | Not authorized. |
| Clean-room builder B/rival | High | Not authorized. |
| Governance reviewer | High | Not authorized. |
| Adversarial reviewer | High | Not authorized. |

Every external handoff must echo scope, prototype rung, and stop conditions.

## Data safety and stop conditions

Stop immediately if a proposed experiment would touch a real workspace,
credential, remote, personal output, or location. Replace it with synthetic
material or report the missing authority. Do not infer owner permission for a
real run from this plan.
