# D3 Round-2 Design: Production Package Resolver

## 1. Registry-Anchored Resolution Contract
The production resolver relies exclusively on the repository-resident public publication registry to authenticate packages and members. The local environment `L` may provide a catalog to locate raw bytes, but `L`'s catalog is never trusted as the source of truth for membership or checksums.

## 2. Declared Adoption Carrier
Package selection requires a formal `AdoptionRecord` (an Article-4 carrier) present in `L`.
Schema requirements for the carrier:
- `actor`: System or automation identity performing the adoption.
- `scope`: Production environment or tax year context.
- `provenance`: The mechanism of placement in `L`.
- `package_pin`: Exact `(id, version)` selector.
- `trust_anchor_pin`: Exact checksum matching the public registry release commit.

## 3. Strict Verification Gate and Inertness
1. **Supply & Anchor**: Extract `AdoptionRecord`. Fetch the pinned `trust_anchor_pin` registry from the repository.
2. **Package Checksum**: Compute the package bytes' checksum from `L`. Reject if it does not match the registry's package checksum.
3. **Member Checksums**: For every member in the registry's `package.members` pin, locate the member bytes in `L`. Compute checksum and reject on any mismatch.
4. **Validation Gate**: Run the validator on the pinned members only. A resolved graph is yielded *only* if `validation.ok == True`.
5. **Inertness**: Co-located unpinned files in `L`, missing members, or glob artifacts are strictly ignored and remain inert/unreadable. 

## 4. D3-P2 Discharge Ledger

### ADR-0027 Ledger
- **D1 (Sole Package Authority)**: Discharged. Graph is constructed only from exact `package.members` registry pins.
- **D2 (Role Canon)**: Discharged. Members retain schema-defined roles; unrecognized roles reject.
- **D3 (Embedded Checksums)**: Rejected natively. Schema-byte checksums are rejected as circular.
- **D4 (Typed Closure & Contained Issues)**: Discharged. The validation gate is strictly `ok == True`. Unresolved dependencies or issues reject the graph.
- **D5 (Producer Integrity)**: Discharged. Adoption requires provenance and an immutable trust anchor.
- **D6 (Member Immutability)**: Discharged. Exact member byte checksums are verified against the registry.
- **D7 (Exclusive Projection)**: Discharged. Unpinned/co-located files remain inert.
- **PC1-PC4 (Production Conditions)**: Discharged. Publication registry rules, source isolation, and immutable registry checks are satisfied by this design.

### ADR-0028 Ledger
- **D1-D9 (Composition & Fact Surface)**: Discharged. Required obligations (e.g., missing facts, composition gaps) result in validation issues, causing `ok == False` and immediate rejection.
- **PC1-PC3**: Discharged. Verified registries and mandatory validation are enforced.

### Interlocks
- **D1 (Installed Wall)**: Deferred. Proof of the ADR-0031 runtime capability (no network, `L`-only write) remains a Track 1/3 obligation.
- **D2 (Marshal-Only)**: Deferred. The `RunContext` interlock remains a Track 2 obligation.

## 5. MUST Production Condition (RG-1)
The synthetic current core package reports 8 contained issues (including two mapping fact-surface issues). The strict `ok == True` validation gate prevents this package from loading. **RG-1 (fixing the 8 contained issues)** is a MUST production condition prior to any live production run; no leniency or issue allowlist shall be added to the gate.
