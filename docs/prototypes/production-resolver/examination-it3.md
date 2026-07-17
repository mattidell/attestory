# D3 Round-2 Examination: Production Package Resolver

## Probes and Observed Outcomes (Rung-2 Synthetic Evidence)

| Claim | Probe | Outcome |
| :--- | :--- | :--- |
| **Clean parity** | Adopt clean synthetic package with valid registry anchor and passing validation. | **Success**: Resolver yields the graph exactly matching the pinned members. |
| **Unpinned/co-located inertness** | Place `demo.malicious.json` in `L`, omit from registry. | **Success**: Unpinned file is unread, excluded from graph. |
| **Package/member mismatch & rewrite** | Alter member bytes (`demo.rule.v1'`); update package checksum to match the alteration. | **Rejected**: Registry member checksum mismatch triggers `MEMBER_CHECKSUM_MISMATCH`. |
| **Incumbent catalog substitution** | Supply forged catalog in `L` matching the forged bytes. | **Rejected**: Resolver uses the immutable public registry, detecting the mismatch. |
| **Undeclared/stale adoption carrier** | Provide raw `{package_id: "demo", version: "v1"}` without Article-4 act fields. | **Rejected**: `AdoptionRecord` fails schema validation; resolution halts. |
| **Missing ratified member** | Delete one pinned member from `L`. | **Rejected**: Member byte resolution fails, graph construction aborts. |
| **Complete ledger enumeration** | Verify explicit D3-P2 ledger covers all D1-D7/PC1-PC4 and D1-D9/PC1-PC3. | **Success**: Ledger is explicit in `design.md`. |
| **Strict gate (Clean)** | Run strict `ok=True` on a clean, valid package. | **Success**: Does not over-fire; yields the valid graph. |
| **Strict gate (Core with 8 issues)** | Run strict `ok=True` on current core package with 8 known issues. | **Rejected**: Gate strictly enforces `ok=True`. Proves RG-1 is a MUST condition. |

## Unresolved Questions
1. **Adoption Provisioning**: What mechanism physically provisions the `AdoptionRecord` into `L` prior to execution? (Track 1/3 deployment scope).
2. **D1/D2 Proofs**: Full end-to-end proofs of ADR-0031 (kill switches) and ADR-0032 (marshal-only boundary) remain pending their respective tracks.
