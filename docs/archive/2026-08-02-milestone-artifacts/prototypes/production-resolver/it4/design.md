# D3 it4 — Production Package Resolver (Clean-Room Rival Design R2)

Builder: clean-room rival, High tier.
Date: 2026-07-16.

**Clean-Room Seal Statement:** I have read only the repository entry chain, `SEAT.md`, `charter-it4.md`, `plan.md`, `process-log.md`, Round-1 committee reviews (`governance-r1.md`, `adversary-r1.md`), ADR-0027, ADR-0028, ADR-0031, ADR-0032, and committed loader/validator/runner/publication registry surfaces. I have not read `it3/`, `examination-it3.md`, or any incumbent material. My design is sealed until foreman custody.
**Rung-2 Ceiling & Evidence Boundary:** All examples are synthetic. No real workspace, values, locators, implementation code, or schema changes are used or claimed. The outputs are limited to this `design.md` and `examination-it4.md`.
**Stop Conditions:** Stop and report if the contract needs a new D1/D2 boundary, demands production implementation, relaxes all-or-nothing validation, or exceeds Rung 2.

## 1. D3-P1: Production Resolution Contract

The contract introduces a secure, immutable, and strictly gated production resolver that strictly separates authority from supply location, closing the Round 1 blockers without weakening fixture guarantees.

### 1.1 Declared Versioned Adoption Act
Authority resides entirely in a declared versioned adoption act inside the live workspace `L`. A new schema `act-package-adoption.v1` is defined, carrying:
- `actor`, `scope`, and `provenance`
- `package`: exact `(id, version, checksum)` pin
- `trust_anchor`: exact release/registry pin

A caller-shaped dictionary or undeclared metadata cannot authorize resolution. The resolver accepts only a current, valid adoption act as the entrypoint.

### 1.2 Immutable Publication Authority and Supply Indifference
The public, repo-resident publication registries (`published-packages.json`, `published.json`) are the sole immutable publication authority. 
No self-authenticating `L` catalog, directory scan, or filesystem walk acquires authority.
`L` provides candidate bytes, but the resolver admits **only** bytes whose canonical checksum perfectly matches the repo-resident registry. An `L`-resident catalog or substitution cannot override the registry (closing the A1 blocker).

### 1.3 Pin-Directed Supply and Exclusive Graph
Resolution is strictly pin-directed:
1. Load the adoption act.
2. Verify the package instance bytes against the adoption's package checksum and the repo-resident registry.
3. Iterate exact `package.members`. For each pin, locate candidates in `L`, verify bytes against the repo-resident citizen registry, and admit only the distinct matching bytes.
This approach inherently prevents the same-key impostor/glob race. Duplicate or unpinned impostors are completely ignored as they are never pinned or fail the registry checksum. Only verified exact pins construct the exclusive resolved graph.

### 1.4 Strict Gate: `ok == True`
Before any execution, marshalling, or rendering, the constructed graph is evaluated. The resolver enforces a mandatory `ok == True` gate.
If any validation issue is present (e.g., missing members, schema violations, reachability faults), the resolver yields a typed `ResolutionRejected` ledger containing all issues. No partial graph is ever returned. Leniency is strictly forbidden.

## 2. D3-P2: Discharge/Defer Ledger

The contract explicitly accounts for all ADR-0027 and ADR-0028 decisions.

| ADR Item | D3 Disposition | Reason / Production Evidence Owed |
|---|---|---|
| 0027 D1 (sole package authority) | **Discharged** | Pinned `package.members` dictates the set. No directory walks. |
| 0027 D2 (role canon) | **Discharged** | Admitted citizens evaluated against the closed role canon before graph creation. |
| 0027 D3 (admitted schemas) | **Discharged** | Verified members pass schema admission; embedded schema-byte checksums are explicitly **rejected**. |
| 0027 D4 (typed closure / issues) | **Discharged** | Mandatory `ok == True` strict gate prevents partial execution. Issues are contained in the refusal ledger. |
| 0027 D5 (producer integrity) | **Discharged** | Cross-package owner checks run inside the validation gate. |
| 0027 D6 / PC3 (immutability) | **Discharged** | Package and member bytes are strictly verified against the immutable repo-resident registry. |
| 0027 D7 / PC1 (exclusive projection) | **Discharged** | Co-located unpinned files are structurally excluded by pin-directed lookup. |
| 0027 PC2 (conflict semantics) | **Discharged** | Validation strictly enforces producer selection for conflicts. |
| 0027 PC4 / 0028 PC3 (issue strings) | **Acknowledged** | Issue strings remain an implementation detail. |
| 0028 D1-D4 (fact/adoption equality)| **Discharged** | Nested-set equality of `act-bundle-adoption.v2` enforced at resolution boundary. |
| 0028 D5-D8 (composition/quantity) | **Discharged** | Composition obligations and quantity triggers checked within the strict validation gate. |
| 0028 D9 (successor schemas) | **Discharged** | Checked via `admitted_schemas` validation. |
| 0028 PC1 / PC1b (goldens) | **Deferred** | Implementation golden fixtures deferred to Track 4 (coverage). |
| 0028 PC1c (confirmation) | **N/A** | Already complete. |
| 0028 PC2 (historical v1 migration) | **Deferred** | Explicitly deferred to Track 3/4. |
| RG-1 (core package conditions) | **MUST Production Condition** | The core package must be repaired to `ok == True` before production. Observed count is 8 issues. |
| D1/D2 Interlocks (ADR-0031/0032) | **Deferred** | Interlocks honored via read-only capability and exclusive `RunContext` feed, but installed proof deferred to Tracks 1/3/4. |
