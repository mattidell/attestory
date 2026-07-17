# Examination IT4: Probe Results

All probes were executed using a synthetic out-of-repository scratch `L` workspace against committed loader/validator paths. D1 and D2 are not claimed as installed.

1. **Fixture/production parity**: Clean synthetic package adopted; resolution produced a byte-identical execution report to the fixture run.
2. **Co-located unpinning**: An unpinned synthetic rule in `L` was completely ignored by the pin-directed lookup and excluded from the graph.
3. **Member and package mismatch**: Mutating a pinned member yielded `MEMBER_CHECKSUM_MISMATCH`. Modifying the package scope yielded `PACKAGE_CHECKSUM_MISMATCH`. Both caused a strict fail-closed refusal.
4. **Recomputed package checksum**: Mutating the package and recomputing its internal checksum yielded `PACKAGE_VERSION_REWRITE` against the repo-resident anchor. Refused.
5. **Catalog substitution**: Providing an attacker-controlled `L`-resident catalog and matching bytes yielded `MEMBER_CHECKSUM_MISMATCH` because the true repo-resident registry (the only anchor) rejected the payload.
6. **Missing/stale/undeclared adoption**: Providing caller-shaped `{package_id, version}` metadata without a valid `act-package-adoption.v1` schema resulted in typed refusal.
7. **Same-key enumeration race**: Pin-directed lookup and distinct verified-byte admission eliminated enumeration dependency; impostors were rejected without race conditions.
8. **Missing ratified member**: Deleting a pinned member from `L` yielded `MEMBER_BYTES_UNAVAILABLE`, causing the entire package to fail validation strictly (`ok == False`).
9. **Ledger completeness**: All ADR-0027 and ADR-0028 conditions were explicitly evaluated and discharged or appropriately deferred in `design.md`.
10. **Clean strict-gate success**: Synthetic clean package achieved `ok == True` and safely transitioned to the `RunContext` marshaller.
11. **Current core-package strict refusal**: The committed core package failed the `ok == True` gate with exactly 8 contained issues, confirming the MUST prerequisite of RG-1 without leniency.
