# D3 Iteration 3 — Examination (Incumbent)

Date: 2026-07-16  
Seat: incumbent builder, High tier  
Evidence: Rung 2 only — committed loader/validator + synthetic scratch-`L`.

## Proposition results

| Proposition | Result |
| --- | --- |
| **D3-P1** production resolution contract | **Settled at Rung 2** for the four blockers: release-byte verification before entry use; current-user adoption currency/supersession; order-independent same-key refusal; exclusive pin-directed graph with hard `validation.ok == True`. |
| **D3-P2** discharge/defer ledger | **Settled at Rung 2**: 25 ADR-0027/0028 slots (D1–D7, PC1–PC4; D1–D9, PC1/PC1b/PC1c/PC2/PC3) each classified as contract settled here, production condition with owning track, deferred with reason, or N/A. Embedded schema-byte checksums = N/A rejected. D1/D2 interlocks = production conditions, not D3 discharges. |

## Probe ledger (synthetic scratch-`L`)

Supply: committed synthetic `tax.us.2025.package.interest-slice@v1` (19 members,
`validation.ok == True`) copied into throwaway `L`, plus co-located unpinned
`demo.evil.unpinned@v1`. Registry authority simulated by the published
`published-packages.json` bytes whose sha256 is the adoption `release.checksum`.
Paper resolve implements §1–§3 of `it5/design.md` over committed
`verify_published_package` / `validate_package` / checksum helpers.

| # | Probe | Observed |
| --- | --- | --- |
| 1 | Clean strict-gate pass | **Accept.** Graph size 19; exclusive keys match package pins only. |
| 2 | Release-byte substitution (mutate registry file; pin unchanged) | **Refuse** `RELEASE_CHECKSUM_MISMATCH` before any entry authentication. |
| 3 | Caller-selected `L` registry with forged entries | **Refuse** `RELEASE_CHECKSUM_MISMATCH` (pin names true release digest). |
| 4 | Forged `L` catalog agreeing with hypothetical impostors | **Ignored**; clean resolve still **Accept** via verified release. |
| 5 | Package bytes mismatch vs adoption pin | **Refuse** `PACKAGE_ADOPTION_CHECKSUM_MISMATCH`. |
| 6 | Package rewrite + recomputed self-checksum; adoption pin updated | **Refuse** `PACKAGE_VERSION_REWRITE` against verified registry. |
| 7 | Member byte mutation | **Refuse** `MEMBER_CHECKSUM_MISMATCH`. |
| 8 | Stale user act superseded by current tip | **Accept** current tip only (`stale_superseded_selects_current`). |
| 9 | Non-user `actor=automation` competing act | **Ignored**; user tip still **Accept**. |
| 10 | Two non-superseding user tips, same scope | **Refuse** `ADOPTION_AMBIGUOUS`. |
| 11 | Scope/revision mismatch (run scope ≠ act scope) | **Refuse** `ADOPTION_NONE_CURRENT`. |
| 12 | Missing release pin on act | **Refuse** `ADOPTION_NONE_CURRENT` (malformed act filtered). |
| 13 | Same-key distinct-byte candidates under `aaa_`/`zzz_` enumeration | **Refuse** `SAME_KEY_CANDIDATE_REFUSAL` (order-independent). |
| 14 | Same-key identical-byte duplicates | **Accept** (single distinct digest equals registry). |
| 15 | Unpinned co-located evil file | **Excluded** from graph (`evil_excluded=True`). |
| 16 | Core package eight-issue hard gate | **Refuse.** `ok=False`, **8** issues: `SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`, 2×`MAPPING_FACT_TYPE_NOT_ADMITTED`, 4×`MEMBER_UNREACHABLE`. |
| 17 | Ledger slot completeness | **25/25** required ADR items present with allowed dispositions only. |

## RG-1 (MUST production prerequisite)

Named explicitly, not as vague "fix the package":

1. **Validator-reachability repair** — the four `MEMBER_UNREACHABLE` issues.
2. **v1-generation content debt** — `SCHEMA_NOT_ADMITTED` / `ROLE_MISMATCH` and
   the two mapping fact-surface admissions.

Both are **MUST** before any live production run. The production gate must not
weaken: `validation.ok == True` remains mandatory; no allowlist.

## Critical distinctions preserved

- Release pin authenticates **registry bytes**, then registry entries authenticate
  package/member bytes. Caller path and `L` catalog cannot choose authority.
- Adoption authority is one current **user** act selected by scope + supersession
  tip — never a runner-supplied package dictionary.
- Same-key admission uses the **set of digests**, not filesystem order.
- "Contained issues" means accumulate and refuse production use — not execute the
  clean subset.
- ADR-0031/0032 are consumed interlocks; this examination makes **no** installed
  wall or marshal-only claim.

## Residuals (not decision-blocking for this paper)

- Schema/install of `publication-release.v1` and `act-package-adoption.v1`
  (Track 3).
- Golden suites PC1/PC2/0028-PC1/PC1b (Tracks 3/4).
- Historical v1 bundle migration (deferred PC2).
- Full D1 topology proof and D2 live-entrypoint kill-test (owning tracks).

No new boundary, no weaker validation rule, and no production implementation
claim was required to complete this iteration.
