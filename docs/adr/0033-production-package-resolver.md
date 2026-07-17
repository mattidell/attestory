# ADR 0033 — Production Package Resolver

- Status: **proposed** (awaiting owner ratification)
- Tier: 2
- Date: 2026-07-17
- Plain-language analysis: [why this change is needed](analyses/0033-production-package-resolver.md)

## Context

ADR-0027 settles adopted-package membership, package-instance immutability, and
exclusive execution projection inside the fixture boundary; ADR-0028 completes
the fact/composition membership surface. Neither defines how an adopted package
resolves from live residency `L` (ADR-0031) without trusting co-located bytes or
caller metadata.

The D3 prototype completed three paired Rung-2 build iterations and an
owner-launched confirmation committee. Its final evaluation analysis concludes
that D3-P1 (trusted production resolution) and D3-P2 (an exhaustive
discharge/defer ledger) converge with no remaining decision-blocking finding.
The accepted direction is the sealed rival's independently reviewed release-root
chain; the incumbent independently corroborates all four repaired authority
questions.

## Decision

### 1. A release-rooted, current-user adoption authorizes production resolution

Production resolution begins with exactly one current, scoped user adoption act,
not a caller-provided package id, release id, path, catalog, or fixture-shaped
`adoption_pin`.

- **`release-registry.v1`** is a versioned publication-root citizen. Its
  immutable identity includes the SHA-256 of the exact package registry document
  it attests, and, where citizen registries are split, the SHA-256 of each
  separately attested registry document.
- **`act-package-adoption.v1`** is a declared Article-4 user act. It pins an
  exact package `{id, version, checksum}` and an exact release
  `{id, version, checksum}`, with the user actor, structured scope, revision,
  optional same-scope supersession reference, and non-authoritative audit
  metadata.
- At a fixed workspace revision and declared run scope, the resolver considers
  only well-formed acts by the sole user in that scope. It applies supersession,
  then selects the unique maximum revision. Zero candidates or a tied maximum
  refuses resolution. A non-user act, a stale act, or a runner argument never
  selects authority.

### 2. Verify release bytes before registry entries authenticate supply

Before parsing any registry entry, the resolver loads the adoption-pinned release
from the immutable publication surface, verifies its exact bytes against the
adoption pin, then verifies each registry document against the release's attested
checksum. Only those verified registry bytes may authenticate the adopted package
and its members. A caller-selected working-tree file, `L` catalog, or registry
candidate has no authority.

This closes three distinct substitutions fail-closed: a forged release,
replacement registry bytes under an honest release, and changed package/member
bytes under an honest verified registry. Existing package-instance and citizen
checksum verification remains mandatory; recomputing a package's self-checksum
does not evade the publication registry.

### 3. Resolve one exclusive, verified member graph or refuse

After verified release, registry, and package-instance checks, the resolver walks
only exact package-member pins. For each pinned key it gathers candidate bytes,
computes their canonical checksum, and admits only a body matching the verified
expected digest. Zero matches refuses; byte-identical matching duplicates
collapse; any unresolved ambiguity refuses. Filesystem, glob, and directory order
must not affect admission. Co-located unpinned files never become candidates for
an unpinned key and are not executable or renderable.

The resolver runs the closed-graph validator over this member set and returns no
resolved graph, execution, or rendering unless `validation.ok == True`. This is
a strict superset of the fixture path's guarantees. Contained validation issues
are reported in the refusal; they never authorize a clean subset or allowlist.

### 4. D3-P2 disposition ledger

The following table is the complete disposition surface. `CS` means this ADR
settles the paper production-resolution contract; it does **not** claim Track-3
installation. `PC(Tn)` is a production condition owned by milestone Track *n*;
`DEF` is explicit deferral; `N/A` is not a D3 implementation condition.

| ADR-0027 item | Disposition |
|---|---|
| D1 sole package membership authority | CS |
| D2 role canon | PC(T4) |
| D3 admitted schemas | CS; embedded schema-byte checksums are **N/A / rejected** |
| D4 typed closure and contained issues | CS |
| D5 form-field producer integrity | PC(T4) |
| D6 package-instance and member immutability | CS |
| D7 exclusive execution projection | CS |
| PC1 unpinned-co-located golden | PC(T3/T4) |
| PC2 conflict-semantics golden | PC(T3/T4) |
| PC3 registry-verified package and members | CS |
| PC4 issue-code strings | N/A |

| ADR-0028 item | Disposition |
|---|---|
| D1 versioned fact-type/bundle members | PC(T4) |
| D2 dual fact-surface pin unit | PC(T4) |
| D3 wholesale nested-set equality | PC(T4) |
| D4 exact mapping fact-type edges | PC(T4) |
| D5 declared composition obligation | PC(T4) |
| D6 full composition binding | PC(T4) |
| D7 closed quantity vocabulary | PC(T4) |
| D8 same-quantity force-declare | PC(T4) |
| D9 successor schemas and admitted schemas | PC(T4) |
| PC1 reject-direction goldens | PC(T4) |
| PC1b accept/non-trigger goldens | PC(T4) |
| PC1c confirmation readiness | N/A |
| PC2 historical v1 migration | DEF — migration work outside resolver shape |
| PC3 issue-code strings | N/A |

ADR-0031's residency wall is a PC(T1/T3) consumed by this resolver; ADR-0032's
marshal-only `RunContext` and live-entrypoint kill test are a PC(T2/T3). Neither
is installed or discharged by D3.

### 5. RG-1 is a MUST production prerequisite

Before a live package family can cross the hard `ok == True` gate, it must repair
the committed core package's eight contained issues: four
`MEMBER_UNREACHABLE` validator-reachability defects, plus the v1-generation
content debt represented by `SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`, and two
`MAPPING_FACT_TYPE_NOT_ADMITTED` issues. No leniency or issue allowlist may
substitute for this repair.

## Consequences

- Production resolution has one authority chain: current user adoption → verified
  release → verified registry → verified package/member pins → hard validation →
  exclusive graph.
- Live supply in `L` may provide candidate bytes but cannot define membership,
  publication truth, or adoption authority.
- Track 3 must add the release/adoption schemas, resolver entrypoint, typed
  refusals, and synthetic kill/golden coverage for release substitution,
  adoption currency, same-key handling, missing pins, package/member mismatch,
  and hard-gate behavior.
- A live run remains unavailable for the core package until RG-1, D1, and D2
  owning conditions are discharged.

## Alternatives considered

- **Self-authenticating `L` catalog.** Rejected: changed same-identity bytes can
  agree with attacker-selected catalog checksums.
- **Registry entries without release-byte verification.** Rejected: a replaced
  registry can authenticate forged supply while appearing internally consistent.
- **Caller-selected or automation adoption.** Rejected: Article 4 requires the
  user's recorded, current adoption; caller choice is not authority.
- **Filesystem-order candidate selection or partial graphs.** Rejected: both
  make membership/supply dependent on co-location and admit silent partial use.
- **Leniency for the eight current core-package issues.** Rejected: containment
  records defects; it does not authorize execution of the remaining graph.

## Links

- Evaluation: `docs/prototypes/production-resolver/evaluation-analysis.md`.
- Builds: `it5/design.md` + `examination-it5.md`; sealed rival `it6/design.md` +
  `examination-it6.md`.
- Committee: `reviews/governance-r3.md`, `reviews/adversary-r3.md`.
- Prior blockers: `reviews/governance-r2.md`, `reviews/adversary-r2.md`.
- Contracts: ADR-0027, ADR-0028, ADR-0031, ADR-0032; Constitution Articles 4,
  9, 11, 18; Ontology §§1, 4, 8.
- Milestone: `docs/phases/real-return/milestones/first-real-return-slice.md`.
