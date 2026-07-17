# D3 Round 1 — Adversary Review

Date: 2026-07-16  
Seat: Adversary reviewer, Medium. Evidence: Rung 2; all cases below use
synthetic `demo.*` content or committed synthetic fixtures. No real data used.

## Verdict

**Decision-blocking: D3-P1 does not yet settle.** The incumbent admits a
self-consistent but unregistered live catalog; the rival has the right
repo-resident trust anchor but leaves the recorded package-adoption carrier
undefined. A synthesis can close both: a declared adoption act (actor, scope,
provenance, exact package pin, and immutable public trust-anchor/release pin)
plus rival R1/R3/R5/R6. **D3-P2 survives conditionally**: retain the incumbent's
decision-level ledger and revise it for the selected synthesis and the observed
RG-1 count below.

## Attacks

### A1 — Catalog substitution (incumbent) — **bypassed; decision-blocking**

Synthetic `demo.package.v1` and `demo.rule.v1` have public-registry checksums
`P` and `M`. In `L`, supply changed bytes `demo.package.v1'` / `demo.rule.v1'`
and a catalog whose checksums are `P'` / `M'`; the adoption pins that catalog and
`P'`. Incumbent steps 2/5/6 then accept: its catalog is the checksum map passed
to `verify_published_package`, and every post-read comparison agrees with the
attacker-selected catalog. The resolved graph can execute the changed synthetic
rule. This violates ADR-0027 D6: resolution must trust registry-verified
content, not an arbitrary corpus's self-description. A catalog may locate
objects, but cannot be the publication trust anchor.

Rival R1/R3 rejects the same supply: only bytes matching the read-only
repo-resident registry survive. This is the required direction.

### A2 — Adoption authority absent (rival) — **bypassed in contract; decision-blocking**

R2 consumes an `AdoptionRecord` in `L` but proposes no declared act schema or
versioned payload. The committed `adoption_pin` is fixture-shaped metadata, not
an Article-4 act carrying actor, scope, provenance, and a package selection.
A caller-shaped synthetic `{package_id: "demo.package", version: "v1"}` is
therefore indistinguishable at the proposed boundary from a current adoption.
This is an undeclared authoritative noun (Articles 4, 9, 10), not a harmless
implementation detail. The missing carrier must be declared before production;
the incumbent's carrier direction is usable only after A1's registry defect is
removed.

### A3 — Same-key impostor / glob race — **rejected; not blocking for rival**

The race is real in the fixture loader: `runners/derive.py` iterates an unsorted
`package_dir.glob("*.json")` and overwrites `corpus[(id, version)]`. Two
synthetic files with `(demo.member, v1)` select different bytes when enumeration
order changes. With registry checks enabled, a selected impostor yields
`MEMBER_CHECKSUM_MISMATCH` and is excluded; the committed fixture runner may
then fail by `KeyError`, so it is fail-closed in effect, not typed.

Rival R3 gathers candidates and admits only the registry-matching distinct
bytes; R6 avoids enumeration for membership. Thus an unpinned or same-key
impostor cannot enter its graph independent of ordering. Incumbent's unique-key
catalog also prevents the race only after its catalog is anchored to the public
registry (A1).

### A4 — Byte mismatch and R5 / RG-1 — **rejected; gate is correct**

Direct synthetic checks found `package.interest-slice` clean: `ok=True`, zero
issues, 19 resolved members. A changed member produced
`MEMBER_CHECKSUM_MISMATCH`; a stale package checksum produced
`PACKAGE_CHECKSUM_MISMATCH`; recomputing only that field produced
`PACKAGE_VERSION_REWRITE`. The strict `ok=True` gate therefore does not
over-fire on a genuinely clean package and must not gain a leniency list.

The current core package instead reports **8**, not 7, contained issues (two
mapping fact-surface issues plus schema/role/reachability issues) while the
fixture runner still publishes. That is a real availability cost, but RG-1's
honest remedy is validator/content repair before a production run; allowing its
reduced graph would reintroduce silent partial execution. Correct the count and
name all repairs as a MUST production condition.

### A5 — D1 interlock — **no bypass shown; deferred installed proof**

Both papers require the ADR-0031 runtime capability: repository read-only,
writes and records only in `L`, no network/publication capability. I found no
paper path copying synthetic live bytes to a repository artifact. The committed
fixture CLI is not a production entrypoint and cannot prove this wall. The
capability, guarded-transport, and egress kill tests remain ADR-0031 Tracks
1/3 obligations; D3 must not claim they are already installed.

## Proposition findings

| Proposition | Finding |
| --- | --- |
| D3-P1 | **Unresolved at Rung 2; blocking.** Adopt rival registry arbitration, pin-directed projection, and all-or-nothing typed refusal, but add a declared current package-adoption act and pin its public trust anchor. Reject an L-self-authenticating catalog. |
| D3-P2 | **Survives conditionally at Rung 2.** The incumbent enumerates ADR-0027/0028 decisions most completely; carry that ledger into the synthesis, explicitly defer installed D1/D2 proof, and update RG-1 from seven to eight observed issues. |

