# ADR 0044 — Live-Run System Boundary and Trust Domains

- Status: **accepted** (owner direction 2026-07-23)
- Tier: 3
- Date: 2026-07-23
- Plain-language analysis:
  [0044-live-run-system-boundary-and-trust-domains.md](analyses/0044-live-run-system-boundary-and-trust-domains.md)

## Context — the system is not the developer workflow

The repository is commonly edited, tested, and executed on the owner's
workstation under a developer-friendly account. That is a convenient workflow,
not a sufficient definition of the application's privacy boundary. If source
development, publication credentials, live workspace data, and execution all
share one effective authority, a process holding that authority can reach
everything the owner can reach. Naming directories or wrapping commands does
not create a trust boundary.

ADR-0031 established the enduring privacy obligations: real data stays in an
out-of-repository residency, crossings fail closed, locators do not enter the
repository, synthetic fixtures are independently constructed, and anything
describing a live run inherits its sensitivity. ADR-0032 made contribution a
separate event that writes only into that residency. ADR-0033 made current
owner adoption and byte verification, rather than caller choice or co-location,
the authority chain for production rule-package resolution.

Later guarded-transport work tried to make a publication credential available
only after a local push gate passed. Its clean-room rival demonstrated that a
mode-600 credential store was readable by a same-UID process. The incumbent and
its one repair did not produce an independently reproducible successful
actual-Git scan-before-release path. Those results establish that neither tested
shape supports its claimed confinement. They do not establish a general
impossibility theorem about operating-system users, containers, virtual
machines, or other isolation substrates.

The active milestone plan authorizes this direct system-definition ADR from
those accepted decisions and completed records. It selects no enforcement
substrate and makes no L4 claim.

## Decision — four logical trust domains

A trust domain groups assets and authorities treated as mutually reachable
without another boundary crossing. It is not, by itself, an operating system
user, process, container, virtual machine, directory, or host. The first three
domains below are execution/data domains; Owner Authorization is the human
authority domain and need not be an execution identity. A later implementation
must map the execution/data domains to mechanisms that preserve the authorities
declared here.

| Domain | Assets | Authority |
| --- | --- | --- |
| **Developer/Supply** | Source repository and worktrees, development tools, build state, independently constructed synthetic fixtures, and publication credentials. | May edit, test, package, and offer publication-eligible material. Has no standing authority to read the live workspace, its locator, or any artifact that describes it. |
| **Publication** | The remote repository and immutable release, registry, package, and member bytes made available from it. Everything here is treated as potentially public. | May distribute only material already classified `MAY_CROSS`. It holds no live workspace state and grants no authority merely because bytes are co-located. |
| **Live-Run Data** | The live workspace, evidence, findings, contribution and run records, dispositions, residency locator, and runtime capabilities serving that workspace. | May consult and change authoritative live state only under the owner's recorded grants and acts. It may consume the current owner-adopted, byte-verified package. It has no source-publication credential or publication path. |
| **Owner Authorization** | The owner's deliberate grants and acts: residency selection, contribution, adoption, run initiation, and any explicit elevation across a boundary. | May authorize a particular crossing or operation. This is the source of authority, not a claim that owner-approved elevation is technically impossible. |

The domains are defined by authority, even when an early implementation places
more than one of them on the same physical workstation. Co-location does not
satisfy the boundary. If one UID or process can exercise both domains'
capabilities, the separation is logical but not yet enforced.

## Decision — permitted system-to-system crossings

1. **Developer/Supply → Publication:** only material classified `MAY_CROSS`
   under ADR-0031 may cross. The whole publication envelope remains in scope:
   content, paths, names, modes, links, histories, messages, refs, patches,
   archives, and API or review text. Unknown or unprovable material refuses.
2. **Publication → Live-Run Data:** only the current owner-adopted,
   byte-verified package and the verified release/registry chain required to
   resolve it may cross. Working-tree proximity, a caller-selected path, and
   unpinned co-located bytes confer no authority. This decision introduces no
   separate application-binary distribution contract.
3. **Owner Authorization → Live-Run Data:** the owner deliberately selects the
   residency and authorizes contribution, adoption, and run acts. Possession of
   the workspace or package is not a substitute for those acts.
4. **Live-Run Data → outside quarantine:** no descriptive live artifact
   crosses back. The sole repository-eligible live-run statement remains
   ADR-0031's non-descriptive attestation: the owner performed the run,
   observed dispositions in quarantine, and no artifact crossed.

No direct Developer/Supply → Live-Run Data crossing is part of the intended
system. In particular, a developer checkout is not the authoritative live-run
supply object.

## Decision — threat posture and residuals

The intended privacy posture protects Live-Run Data from an **unprivileged
Developer/Supply authority**, including malicious developer-side code such as a
compromised dependency, once an implementation enforces the separation above.
Such code may possess ordinary development and publication capabilities; it
must still have no route, mount, credential, locator, or inherited capability
with which to read or describe live data.

This ADR does not claim that the current same-UID developer workflow already
provides that protection. Until a later implementation creates and verifies the
authority separation, same-UID code that can exercise the owner's live-data
capabilities is inside the same effective trust domain.

Accidental publication remains an important current threat even before that
hard separation exists. ADR-0031's fail-closed classification, envelope scans,
locator exclusion, sensitivity inheritance, and synthetic-only posture reduce
that risk at L3. They do not become proof against a determined process that can
bypass the mechanism or read the protected data directly.

Explicit residuals are:

- owner-authorized elevation across the domains;
- administrator, root, hypervisor, physical-device, or equivalent control over
  the selected isolation substrate;
- compromise of the Live-Run Data authority itself; and
- an owner-adopted malicious release. Adoption and byte verification establish
  authority and byte identity, not benevolence.

These residuals are named limits, not hidden exclusions.

## Decision — guarded transport

Guarded transport belongs at the Developer/Supply → Publication crossing. Its
purpose is to ensure that material is classified before a publication
credential can make the outgoing envelope reachable outside the quarantine
posture. It is not the privacy wall between Developer/Supply and Live-Run Data.

The current installed hooks provide conditional protection: when Git invokes
them and their bytes verify, they scan and can refuse a seeded marker. The
completed push-envelope audit also demonstrates that `git push --no-verify`
can bypass the pre-push hook and reach its synthetic remote. Credential
confinement therefore remains `unestablished`; the audit is visibility and
voluntary preflight support, not guarded transport.

ADR-0031 remains authoritative for total fail-closed classification, full
envelope coverage, locator exclusion and screening, independent synthetic
provenance, and sensitivity inheritance. This ADR narrows its architectural
framing in two respects:

1. a read-only mount of developer repository code is not the enduring supply
   boundary; the selected crossing is the adopted, byte-verified package; and
2. guarded transport is a Developer/Supply → Publication integrity condition,
   not the mechanism that establishes Live-Run Data privacy.

ADR-0032's contribution boundary and ADR-0033's adoption and resolution chain
are unchanged.

## Consequences — future implementation gate

The data-boundary maturity row remains **L3**. This ADR makes the intended
system and threat posture decidable, but implements no authority separation.

A later milestone must:

1. select an enforcement substrate, such as a separate OS identity, a
   correctly configured container or virtual machine boundary, or another
   mechanism;
2. prototype only the selected substrate's unresolved feasibility and workflow
   questions;
3. show mechanically that Developer/Supply cannot reach the live workspace,
   its locator, or its runtime capabilities, and that Live-Run Data has no
   publication credential or path;
4. repeat the applicable E18.1 route/canary and E18.2 seeded-egress checks;
5. prove that the live run consumes only the current adopted, byte-verified
   package through the declared crossing; and
6. complete the required owner-run verification, recording only the permitted
   non-descriptive attestation.

Only that implementation and verification can support an L4 data-boundary
claim. Completing guarded transport alone may harden publication integrity, but
does not establish the live-data trust boundary.

### Operational consequences

- Security claims attach to explicit system domains and crossings rather than
  to the convenience of running repository source on a developer workstation.
- A later mechanical design has a stable target: preserve the declared
  authorities and prove the forbidden routes absent. Workflow cost is a
  feasibility consideration, not a reason to blur the boundary.
- The current L3 posture remains useful and honest for accidental leakage while
  making no same-UID malicious-process claim.
- Guarded transport remains valuable, but as separate publication hardening.
- Containers, separate OS users, VMs, credential stores, proxies, and hosted
  controls remain implementation candidates rather than decisions hidden
  inside this ADR.

### Alternatives considered

- **Treat the whole developer workstation or UID as the system boundary.**
  Rejected as the enduring privacy posture: it gives every same-authority
  developer process access to live data and turns workflow convenience into a
  security assertion.
- **Treat the existing hooks and voluntary preflight as the data boundary.**
  Rejected: the synthetic audit demonstrates a reachable `--no-verify` path,
  and hooks do not prevent a process from reading data it can already reach.
  Retained as an L3 accidental-leakage control.
- **Select a separate UID, container, VM, keychain, proxy, or hosted service in
  this decision.** Deferred: the system boundary can be stated without choosing
  its mechanical mapping. Each candidate has platform, workflow, and enforcement
  questions that belong to a later bounded implementation milestone.
- **Retry the same local credential-confinement prototype.** Rejected for this
  milestone: its permitted repair was exhausted, and this decision neither
  needs nor claims a repaired same-UID guarded-push topology.

## Links and evidence limits

The cited evidence has these limits:

- The stopped Guarded Transport topic rejects the tested mode-600-store shape
  and leaves the tested descriptor-release shape unestablished. It does not
  decide whether a separate UID, container, VM, keychain, proxy, or hosted
  mechanism is feasible.
- The Push-Envelope Preflight audit proves only its disposable synthetic Git
  observations: hook-byte verification, hooked marker refusal, and reachable
  `--no-verify` bypass. It does not inspect or protect an owner credential,
  remote, or live run.
- ADR-0031/0032/0033 establish the residency, contribution, adoption, and
  verified-resolution contracts. They do not prove the four domains are
  presently mapped to distinct effective authorities.
- No real workspace, credential, remote, live run, or owner attestation was
  consulted for this decision.

The direct records are:

- Milestone plan:
  `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/live-run-trust-domain-definition.md`
- Residency boundary: `docs/adr/0031-real-data-residency-boundary.md`
- Contribution boundary: `docs/adr/0032-contribution-boundary.md`
- Production package resolver:
  `docs/adr/0033-production-package-resolver.md`
- Guarded Transport triage:
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/round-1-triage.md`
- Guarded Transport repair triage:
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/repair1-triage.md`
- Independent Guarded Transport reviews:
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/reviews/round-1-governance.md`,
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/reviews/round-1-adversary.md`,
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/reviews/repair1-governance.md`, and
  `docs/archive/2026-08-02-milestone-artifacts/prototypes/guarded-transport/reviews/repair1-adversary.md`
- Push-envelope milestone:
  `docs/archive/2026-08-02-milestone-artifacts/phases/real-return/milestones/push-envelope-preflight-and-bypass-visibility.md`
- Governance: Constitution Article 18; Ontology §8; Engineering Constraints
  E18.1 and E18.2
