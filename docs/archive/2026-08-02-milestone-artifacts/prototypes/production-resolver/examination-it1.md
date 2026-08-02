# D3 Iteration 1 — Examination

Date: 2026-07-16  
Evidence: Rung 2 only

## Proposition findings

| Proposition | Finding |
|---|---|
| **D3-P1 — production resolution contract** | **Settled at Rung 2.** Resolve from a current package-adoption act through an adoption-pinned installed-content catalog inside the live capability. Use one source-neutral integrity/validation core; verify the package and every exact member after read; require a clean complete validation; expose only the exclusive immutable resolved graph to the production marshaller and renderer. The production path is a strict guarantee superset of the fixture path because it retains every fixture check and adds current-adoption, catalog-anchor, capability, all-or-nothing, and live-entrypoint constraints. |
| **D3-P2 — discharge/defer ledger** | **Settled at Rung 2.** ADR-0027 package authority, admitted generations, typed closure, producer integrity, package/member immutability, contained issues, and exclusive projection are assigned to D3 production enforcement. ADR-0028 N1/N2 are not reopened or silently deferred: current bundle-set equality and quantity/composition closure gate the production graph. Exact issue strings, the full installed golden suite, and historical v1 bundle migration remain explicitly deferred as the ADRs permit. Embedded schema-byte checksums remain rejected, not deferred. |

## Case accounting

1. **Clean resolution / parity — supports D3-P1.** The committed synthetic
   `interest-slice` package validated from the fixture source and from a copied
   out-of-repository scratch source. Each projection contained the same 19 exact
   member ids. Running the scratch projection published the synthetic B1
   subtotal. This establishes source substitution without graph drift at Rung 2.
2. **Exclusive projection — supports D3-P1 and ADR-0027 D7/PC1.** A valid
   co-located package existed in the scratch corpus but not in the resolved
   projection. The production contract strengthens this by preventing corpus or
   path access after graph construction.
3. **Byte verification (mandatory) — supports D3-P1 and D3-P2.** A pinned member
   mutation yielded `MEMBER_CHECKSUM_MISMATCH`. A package mutation yielded
   `PACKAGE_CHECKSUM_MISMATCH`; replacing only its self-checksum then yielded
   `PACKAGE_VERSION_REWRITE` against the publication registry. The production
   gate returns no graph for any such issue.
4. **D1 interlock — supports D3-P1 within its evidence ceiling.** The synthetic
   scratch workspace resolved outside the repository and no scratch content was
   written into the repository. The design accepts only ADR-0031 runtime
   capability state, writes records only inside `L`, and has no publish/network
   output. Installed topology/capability proof remains ADR-0031 Track 1/3 work;
   D3 does not claim it here.
5. **No silent partial load — supports D3-P1.** Removing one pinned citation
   yielded `MEMBER_ABSENT` and `CITATION_ABSENT`. Although the committed validator
   accumulated an 18-member intermediate, the paper production constructor
   rejects the package and makes that intermediate unreachable by execution or
   rendering.
6. **Ledger (mandatory) — supports D3-P2.** Every ADR-0027/0028 item is mapped in
   `it1/design.md`: discharged by the D3 production contract, already settled,
   explicitly rejected, or deferred with a named reason and later evidence gate.

## Critical distinctions preserved

- `artifact-package.v2` remains the sole membership authority. The installed
  catalog locates and authenticates bytes; it cannot adopt a co-located object.
- “Contained issue” means accumulate and record defects, not execute the clean
  subset of an invalid package.
- The adoption pin anchors catalog/package integrity and names the user’s act;
  no request-supplied path or package-shaped dictionary can substitute for it.
- The resolved graph is transient and rebuildable, not a second authoritative
  store. The adoption act, catalog citizen, package citizens, and run record stay
  in the workspace.
- The D2 invariant is preserved: the graph supplies adopted machinery, while the
  marshal-only production `RunContext` separately consumes projected current
  findings. Contributions and raw input values never enter resolution.

## Residual risk and production proof

Rung 2 cannot prove an installed capability wall, entrypoint unreachability, or
crash-safe record placement. Track 3 must therefore provide: live-source
confinement and no-path-constructor tests; catalog/package/member rewrite tests;
co-location and invalid-subset kill tests at both runner and renderer entrypoints;
package↔bundle swap/omit/extra tests; the ADR-0028 PC1/PC1b matrix; cross-package
producer conflicts; and the ADR-0032 marshal-only reachability kill test.

Neither proposition requires reopening ADR-0031 or ADR-0032. No contract change
proved unrepresentable as a versioned paper diff. Stop at these two static files.
