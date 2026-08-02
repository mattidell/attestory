# D3 Iteration 3 — Adversary Review (Round 3)

Date: 2026-07-16. Seat: Adversary, Medium. Confirmation round (ADR-0034).
Evidence: Rung-2 paper on `it5`/`it6` + synthetic scratch-`L` attacks; read-only
committed `validate_package` for the eight-issue core. Synthetic only. Governance
reviewer work not read.

## Verdict

**D3-P1 and D3-P2 survive at Rung 2.** No working bypass of the four Iteration-2
blockers on either build. Clean confirmation of: release-root → verified registry
→ package/member pins → `validation.ok == True` → exclusive pin-directed graph,
with current-user adoption and order-independent same-key refusal. ADR-0033 is
supportable from this seat; residuals are not decision-blocking.

## Attacks

### A1 — Forge past release-byte authority — **rejected** (not decision-blocking)

**Synthetic:** `L` holds forged package `P'` / member `M'`; attacker offers a
forged combined package+citizen registry agreeing with them, a caller-selected
`L` registry path, and a rewritten release attesting that registry. Honest
adoption pin names true release/registry digest `H`.

- **it5 — rejected.** §1.2 requires `sha256(registry_bytes) ==
  adoption.release.checksum` before any entry is trusted; forged registry under
  honest pin → `RELEASE_CHECKSUM_MISMATCH`. Caller/`L` catalog is never authority
  (exam 2–4).
- **it6 — rejected.** Verify release digest vs pin, then registry vs
  `registry_sha256` (P1–P2). Evil release fails pin; evil registry under honest
  release → `REGISTRY_BYTE_MISMATCH`; entry rewrite → `PACKAGE_VERSION_REWRITE`
  (P3).

**Residual (non-blocking):** it5’s “release digest **or** registry digest”
equivalence is softer than it6’s two-step chain but yields no forge under an
honest pin. If registries split, it6’s optional `citizen_registry_sha256` should
be required; first surface is one combined document.

### A2 — Break current-user adoption selection — **rejected** (not decision-blocking)

**Synthetic:** scope `S` has user act `A`→`demo.safe@v1`, competing/stale user
act `B`→`demo.changed@v1`, automation act `C`→`demo.evil@v1`. Runner tries to
supply package id / act id.

- **it5 — rejected.** Drop non-user and wrong scope; supersession tip set must be
  size 1 else `ADOPTION_AMBIGUOUS` / `ADOPTION_NONE_CURRENT`. Automation never
  enters tip set (cannot supersede user). Exam 8–12.
- **it6 — rejected.** Same filters; supersession then unique max `revision` (tie
  → ambiguous). Storage shuffles do not change selected `act_id` (P4–P5).
  `recorded_at` is non-authoritative.

Caller cannot select among acts. Ontology sole-user actor honored.

### A3 — Defeat same-key refusal by ordering — **rejected** (not decision-blocking)

**Synthetic:** pin `K` with expected digest `E`; co-locate honest body (`=E`) and
evil body (`≠E`) under `aaa_`/`zzz_` names both orders; evil-only; identical-byte
duplicates.

- **it5 — rejected (stricter).** Distinct digest set `|D|>1` →
  `SAME_KEY_CANDIDATE_REFUSAL` independent of order (exam 13). Identical digests
  collapse; sole digest must equal registry (exam 14).
- **it6 — rejected.** Filter to `checksum == expected` first; evil drops; honest
  admits. Evil-only → `MISSING_PINNED_BYTES`. Reversed pin list → identical graph
  id-set (P6/P7/P10).

No order admits unintended candidate bytes. Unpinned co-located files never enter
pin-key candidate sets.

### A4 — Byte-verification / strict `ok == True` / RG-1 — **rejected** (not decision-blocking)

**Synthetic:**

1. Mutate member under honest registry → both refuse `MEMBER_CHECKSUM_MISMATCH`.
2. Drop one pinned member → both refuse; **no partial graph**.
3. Self-checksum rewrite → `PACKAGE_VERSION_REWRITE` via
   `verify_published_package`.
4. Clean `tax.us.2025.package.interest-slice@v1` → committed measure
   **`ok=True`, 0 issues** — gate does not over-fire (exam 1 / P11).
5. `tax.us.2025.package.core-calculations@v1` → committed measure **`ok=False`,
   exactly eight issues:** `SCHEMA_NOT_ADMITTED`, `ROLE_MISMATCH`,
   2×`MAPPING_FACT_TYPE_NOT_ADMITTED`, 4×`MEMBER_UNREACHABLE`. Both refuse the
   graph and name RG-1 as MUST (reachability + v1-generation debt). No allowlist.

No leniency path. Contained issues still block production use. RG-1 is honest
prerequisite, not gate weakening.

### A5 — Ledger honesty + D1 interlock — **rejected** (not decision-blocking)

**Synthetic:** claim ADR-0031 wall or ADR-0032 marshal-only as D3-discharged;
leave an ADR-0027/0028 slot unclassified; reintroduce embedded schema-byte
checksums as deferred work.

- **it5 — rejected.** §4: all 25 slots with allowed dispositions; D1/D2 =
  production conditions; embedded schema-byte checksums = **N/A rejected**.
  Exam 17: 25/25.
- **it6 — rejected.** §2 item-by-item CS/PC(T)/DEF/N/A; anti-laundering rows for
  ADR-0031/0032 and RG-1 MUST; embedded schema checksums N/A rejected (P13).

**D1 bypass:** neither defines a resolver write/export of live `L` into a
tracked/pushable artifact. No paper ADR-0031 bypass (wall consumed, not
re-proven or claimed discharged).

**Residual (non-blocking):** it5 marks more ADR-0028 D-rows “contract settled
here” (via validation gate); it6 prefers `PC(T4)`. Neither falsely claims
installed Track-3/4 evidence.

## Proposition result

| Proposition | Result |
| --- | --- |
| **D3-P1** | **Survives.** Release-byte authority, current-user adoption, order-independent same-key refusal, fail-closed package/member verification, and hard `ok == True` exclusive projection hold under synthetic attack on both builds. |
| **D3-P2** | **Survives.** Exhaustive item-by-item ledger; no silent partial discharge; D1/D2 not laundered; RG-1 named as MUST production prerequisite. |

## Confirmation close

All five charter attack classes: **rejected**. Zero decision-blocking bypasses
at Rung 2. D3 is **converged** from the adversary seat for Tier-2 ADR-0033,
carrying RG-1 + strict gate + ADR-0031/0032 interlocks as production conditions.
