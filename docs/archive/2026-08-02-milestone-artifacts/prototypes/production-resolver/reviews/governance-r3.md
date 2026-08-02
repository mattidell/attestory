# D3 Iteration 3 — Governance Review (Round 3)

Date: 2026-07-16. Seat: Governance reviewer, Medium. ADR-0034 owner dispatch.
Evidence: Rung 2 paper/probe only. Subjects: `it5/design.md` + `examination-it5.md`
(incumbent); `it6/design.md` + `examination-it6.md` (rival). Standing blockers from
`reviews/governance-r2.md` and `reviews/adversary-r2.md`. Synthetic examples only.
Confirmation round — no redesign, no new scope.

## Verdict

**D3-P1: conformant and ratifiable at Rung 2.** Both builds independently close
registry-release byte authority, current-user adoption currency, order-independent
same-key refusal, exclusive pin-directed projection, and the strict
`validation.ok == True` gate as a production-path **superset** of the fixture CLI.

**D3-P2: conformant and ratifiable at Rung 2.** Both ledgers enumerate all
required ADR-0027 D1–D7 / PC1–PC4 and ADR-0028 D1–D9 / PC1/PC1b/PC1c/PC2/PC3
slots with only allowed dispositions; neither falsely discharges ADR-0031/0032.

**Basis.** Either build alone is ratifiable. Prefer **synthesis** if selecting one
text: it6 §1.1 two-step release+registry byte gates, plus either adoption rule
(it5 §2.2 tip-set or it6 §1.2 supersession+max-revision), it5/it6 same-key set
rules, shared hard gate and RG-1 MUST. Track-3 installs; paper settles contract.

---

## Measure 1 — Registry/release byte authority (ADR-0027 D6 / PC3)

**Status: closed (both).**

| Build | Design | Contract |
| --- | --- | --- |
| it5 | §1.1–1.2 `publication-release.v1`; adoption pins `release.checksum`; `sha256(registry_bytes)` before entry use; `RELEASE_CHECKSUM_MISMATCH` | D6 immutability; PC3 registry-verified package/members |
| it6 | §1.1 `release-registry.v1`; release digest then `registry_sha256`; `RELEASE_BYTE_MISMATCH` / `REGISTRY_BYTE_MISMATCH` | Same |

Synthetic: adoption pin names digest *R* of honest release/registry; attacker
supplies `L` catalog + registry bytes agreeing with forged package digests *P'*.
Both refuse at release/registry **byte** compare before any entry authenticates
supply (exam it5 probes 2–4; it6 P1–P2). Caller-selected path / `L` catalog is
not authority. Fixture `load_published_*_checksums(path)` remains non-production.

---

## Measure 2 — Current-user adoption currency (Ontology §1/§4; Article 4)

**Status: closed (both).**

| Build | Design | Contract |
| --- | --- | --- |
| it5 | §2.1–2.2 `act-package-adoption.v1`; actor **must be user**; scope filter; supersession tip; `ADOPTION_NONE_CURRENT` / `ADOPTION_AMBIGUOUS` | Article 4 recorded adoption; Ontology §1 sole actor = user; §4 supersession/currency |
| it6 | §1.2 same carrier; non-user ineligible; supersession then unique max `revision`; `NO_CURRENT_USER_ADOPTION` / `AMBIGUOUS_CURRENT_ADOPTION` | Same |

Synthetic: scope *S* holds user act *A* (package safe@v1) superseded by user tip
*B*, plus automation act *C* for evil@v1. Selection yields only *B*; *C* never
enters the tip set; no runner argument chooses among acts (it5 probes 8–12;
it6 P4–P5). Fixture `adoption_pin` is not production authority.

---

## Measure 3 — Order-independent same-key refusal

**Status: closed (both).**

| Build | Design | Rule |
| --- | --- | --- |
| it5 | §3.1 step 5 | Candidate digests form set *D*; `|D|>1` → `SAME_KEY_CANDIDATE_REFUSAL` (no scan-order pick) |
| it6 | §1.3 | Filter to registry `expected`; multi-distinct cannot all match; order must not affect admission |

Synthetic: pin *K* with honest bytes digest *H* and evil co-located digest *E*,
enumerated `aaa_` then `zzz_` and reverse. it5 refuses the key; it6 admits only
*H* if present, never *E*. Neither depends on filesystem order (it5 probe 13;
it6 P6/P7/P10). Unpinned co-located files stay inert (it5 15; it6 P8).

---

## Measure 4 — Exhaustive D3-P2 ledger

**Status: closed (both).** Required 25 slots: 0027 D1–D7+PC1–PC4 (11) and 0028
D1–D9+PC1/PC1b/PC1c/PC2/PC3 (14). Allowed only: contract settled / production
condition (owner track) / deferred (reason) / N/A.

| Build | Ledger | Anti-laundering |
| --- | --- | --- |
| it5 | §4.1–4.2 all 25; exam probe 17 | §4.3 ADR-0031/0032 = production conditions, not D3 discharges; D3 embedded schema-byte checksums = **N/A rejected** (not deferred) |
| it6 | §2.1–2.2 all 25; exam P13 | §2.3 same interlocks + RG-1 PC(MUST); dual CS+N/A on 0027 D3 is compound (admission CS / embedded checksums N/A) — still allowed vocabulary, not "Acknowledged" |

No unclassified entry. it6 is more conservative (many 0028 D* as PC(T4)); it5
marks them CS via the `ok == True` gate binding validation — both acceptable
paper dispositions; neither claims Track-3/4 installed.

---

## Measure 5 — Strict `validation.ok == True` + RG-1 (eight core issues)

**Status: closed (both).**

| Build | Gate | RG-1 accounting |
| --- | --- | --- |
| it5 | §3.1 step 7; §5 | Four `MEMBER_UNREACHABLE` = validator-reachability repair; `SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`, 2×`MAPPING_FACT_TYPE_NOT_ADMITTED` = v1-generation content debt; **MUST**, no allowlist |
| it6 | §1.4–1.5 | Same eight codes and two-part MUST prerequisite |

Synthetic core `tax.us.2025.package.core-calculations@v1`: both exams report
`ok=False`, **exactly 8** issues, refuse graph (it5 16; it6 P12). Clean
interest-slice: `ok=True`, full pin graph (it5 1; it6 P11). Gate is never
weakened to pass the eight; RG-1 remains production MUST, not D3 discharge.

---

## Proposition results

| Proposition | Result |
| --- | --- |
| **D3-P1** | **Pass.** Standing A1/A2 and same-key underspecification closed; exclusive graph + hard gate retained. |
| **D3-P2** | **Pass.** Exhaustive 25-slot ledgers; no false D1/D2 discharge; embedded schema checksums rejected not deferred. |

No decision-blocking gap survives at Rung 2. Residuals (schema install, goldens,
RG-1 content repair, D1 wall / D2 kill-test proof) are production conditions /
track work — not reopened blockers.

**Stop.** One review file; no repo redesign; no coordination with adversary seat.
