# Prototype Evaluation Analysis — Citation Resolution

Foreman synthesis, 2026-07-15. Advisory to the owner; the owner decides disposition and ratifies any ADR. Track **0.c** of the Core Tax Conditions milestone. Candidate **ADR-0029**, superseding inert ADR-0018.

## Decision under evidence

1. **CIT-P1** — Citation identity and authority model (what a citation is; attachment).
2. **CIT-P2** — Resolver contract and load-time integrity (what “resolved / verifiable” means statically).

## Evidence

Two independently authored designs of both propositions and seven Gate-2 cases:

- Incumbent (`it1/design.md`, `examination-it1.md`) — `3023650`. Citation citizen; multi-cite `citation_refs` on fields and rules; required `display` + runner display canonicalization; package-closure case 5; IRC / IRS_AUTHORITY bag.
- Clean-room rival (`it2/design.md`, `examination-it2.md`) — `6e9a089`. Citation citizen; single form-field pin + rule pin array; no display claim; structural-and-adoption-only resolver (`statically_resolved`); four authority families with locator discrimination; case 5 not external corpus.

Reviewed independently: Governance (`reviews/round-1-governance.md`, CIT-G1–G8; custody this session) and Adversary (`reviews/round-1-adversary.md`, CIT-A1–A9; `93fa092`). Neither read the other.

## Convergence

Under independent authorship both designs converged on:

1. **Citation is a first-class versioned content citizen**, not an unversioned inline blob and not a free-text residual on residual-closed packages.
2. **Attachment is exact `{id, version}` pins** into the package graph.
3. **Package is sole membership authority** (ADR-0027) — no path/`manifest.json` second authority.
4. **Article 9 immutability** for published citation citizens (new version + pin update; no in-place rewrite).
5. **Article 11: no live fetch / no legal applicability** in the resolver (both state; adversary/governance stress depth).

That convergent floor is strong evidence for the P1 skeleton.

## Divergence and resolution

| Topic | Governance | Adversary | Foreman resolution |
|---|---|---|---|
| **it1 overall** | Reject P1+P2 (G4 multi-cite field; G5 display formatter; G6 false verifiability; G7 weak families) | Cond. accept P1; **reject P2** (A2/A3/A7/A9 + A4 incomplete) | **Reject it1 as sole carry-forward.** |
| **it2 overall** | **Accept** P1+P2 | Cond. accept P1+P2 | **Carry it2** as residual production surface, with named production conditions. |
| **Form-field attachment** | Single pin (it2) over multi-array (it1) — ADR-0012 singular presentation location | Non-semantic fence required (A6) | **Single exact citation pin on form-field.v2**; rules may carry a pin **array**. |
| **Display** | Runner templates violate Article 11 (G5) | Display games break it1 (A3/A7) | **No resolver-enforced display canonicalization.** Display/rendering is a separate presentation contract if ever needed. |
| **“Verifiable” depth** | Structural + package membership only (G6) | it2 `statically_resolved` survives; it1 overclaims (A2) | Resolver yields **static structural/adoption resolution only** — never `legal_verified`. Future corpus is a **separate** versioned contract. |
| **Opaque residual** | Both reject on v2 shape | Residual-closed packages must not admit co-equal form-field.v1 opaque strings (A1) | **Residual-closed generation matrix excludes opaque citation strings** as co-equal cites. |
| **Load outcome** | Contained issues both (G8) | it1 “never abort load” vs adoption reject (A9) — decision-blocking | **Any citation defect → package invalid for adoption/execution** while still collecting all issues (ADR-0006 d3). |
| **Locator taxonomy** | Prefer it2 four families + discriminated oneOf (G7) | A8: discrimination must be enforcement-grade | **Carry it2 family split**; production condition: real discriminated schema (not soft properties-only sketch). |
| **Immutability bytes** | Both claim Article 9 | it2 stronger registry-byte path (A4) | **Publication-registry byte checks** for citation citizens (and package instance) as production condition. |

## Supported conclusions

- **C1 — CIT-P1 settled on it2’s citizen + pin + package-member model**, with single form-field pin and multi-pin rules, residual-closed opaque exclusion, role-canon `citation` role, exclusive projection (no co-located activation).
- **C2 — CIT-P2 settled on it2’s structural-and-adoption-only resolver** (`statically_resolved`), adoption reject on citation defects, no runner display formatter, no external legal corpus in this contract.
- **C3 — it1 is not an acceptable sole production surface** for P2 (and governance rejects P1 multi-cite fields).
- **C4 — Inert ADR-0018 is superseded** (path/display assumptions not carried as authority).

## Rejected alternatives

- **it1 runner display canonicalization.** Rejected: Article 11 / adversary display games (G5, A3, A7).
- **Claiming legal or external-corpus verification at load.** Rejected: false confidence (G6, A2).
- **Multi-citation arrays on form-fields.** Rejected: ADR-0012 singular presentation location (G4).
- **Soft-loading packages with citation defects as warnings-only.** Rejected: A9.
- **Path-manifest or co-location membership.** Rejected: ADR-0027 (G2, A5).

## Production conditions (for ADR-0029 / Track 5)

1. Enforcement-grade discriminated family/locator schema (A8 / G7).
2. Publication-registry / package-instance byte immutability for citation citizens (A4).
3. Residual-closed packages: `admitted_schemas` + generation matrix that excludes opaque free-text citation fields as co-equal (A1).
4. Role-canon admits `citation` monotonously (A5); exclusive projection forbids unpinned co-located cites.
5. Rule/field citations are non-semantic for derivation (A6) — no effect on `when` / `value` / dispositions.
6. Issue-code strings deferred (Gate 5).

## Recommendation

1. **Ratify ADR-0029 (proposed)** on C1–C4 with production conditions 1–6 — **it2 primary**, not a pure paste of either exhibit sketch.
2. On acceptance: close Track 0.c; Track 0 contract remediation complete (all five topics); implementation tracks may open under milestone plan sequencing.
3. If the owner disputes single form-field pin (G4) or no-display (G5), name the clause — those are the only sharp governance/adversary agreements against it1.

Advisory only — the owner decides disposition.

---

## Owner disposition (2026-07-15)

**ADR-0029 accepted** (owner ratification). Track 0.c closed.
