# Round 1 Review — Governance Fidelity

Date: 2026-07-12. Seat: governance-fidelity. Evidence rung: 1 (paper).

Authority used: governance set v0.1; ADR-0011; ADR-0014; ADR-0015; approved plan, iteration charters, round-1.md, and the named it1/it2 exhibits.

## Measurements

### Check 1 — claim → member universe → mapping → calculation → coverage alignment

- **it1 — PASS (paper).** Result: All 5 parts declare and bind to the identical `2025 1099-INT box-1 statement items` family. Meaning is derived from the single joint declaration rather than convention labels. Cite: `it1/design.md` lines 9-25.
- **it2 — PASS (paper).** Result: Invariant `closure claim = member predicate = mapping input set = coverage subject` is explicitly established at the closure domain level (`B1`). Broader calculation layers (`L2B`) must explicitly list their dependent input families rather than assume alignment. Cite: `it2/design.md` lines 8-11, 51-52, 84-111.

### Check 2 — whether closure stays determinable/current-true

- **it1 — PASS (paper).** Result: Affirms narrow claim, producing subtotal zero. On discovery of late statement, the old closure finding is withdrawn/superseded to false/not-current. ADR-0010 currency displacement removes the stale zero from workspace state; rerun computes successor subtotal. Cite: `it1/design.md` lines 67-80; `examination-it1.md` lines 22-23.
- **it2 — PASS (paper).** Result: Asserted `C(B1)` yields `S(B1)=0`. Late discovery supersedes old closure assertion because its completeness proposition is false. The derived zero is displaced and rerun computes successor subtotal. Stale zeros cannot remain current. Cite: `it2/design.md` lines 133-150; `examination-it2.md` line 27.

### Check 3 — whether evidence becomes identity

- **it1 — PASS (paper).** Result: Keyed strictly to logical statement-instance identity per ADR-0015. Document upload, scan, or evidence ids are excluded from member identity. Cite: `it1/design.md` lines 26-28.
- **it2 — PASS (paper).** Result: Treats source instance as peer to evidence. Uploaded statement files are evidence; fact identity represents the logical occurrence, explicitly forbidding file/evidence identifiers. Cite: `it2/design.md` lines 20-23, 37-39.

### Check 4 — whether a narrow family gains undeclared broader tax authority

- **it1 — PASS (paper).** Result: Closed box-1 family authorizes box-1 subtotal zero only. It cannot authorize a Form 1040 line-2b zero. If broader interest is open, line 2b remains blocked. Cite: `it1/design.md` lines 46-49, 53-60 (cases 1, 3, 6).
- **it2 — PASS (paper).** Result: `B1` closure authorizes only `B1` subtotal zero, publishing no line-2b result. Broader line-2b zero requires a closed `TI` universe (or proven coextensive composition); open `TI` blocks line 2b publication. Cite: `it2/design.md` lines 75-80, 110, 120-128 (cases 1, 3, 6).

## Observations (not measurements)

- Both rivals establish a clear semantic partition between narrow document subtotal closures and broader taxable interest concepts.
- The differences lie in modeling detail: `it1` binds all parts to a single, structured 5-part declaration; `it2` models the invariant as a mathematical identity over a named closure domain `B1` while explicitly layering the broader calculation consumer as a separate tax concept.

## Recommendations

- Both designs are fully compliant with ADR-0011/0014/0015 at the paper level. Either design is acceptable for transition to schema specification and next-rung planning.
