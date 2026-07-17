# Prototype Plan: Production Package Resolver (D3)

Audience: Agents

Status: **draft — proposed to owner** (principal foreman, 2026-07-16). Track 0,
topic D3 of the First Real Return Slice milestone — the **last** Track-0 decision.
Operates under ADR-0030 per-ADR / per-track merges; owner may amend before builder
launch.

Topic: **How adopted packages resolve beyond the fixture boundary.** ADR-0027
decision 7 (exclusive execution projection) and ADR-0028 (byte-verification,
quantity/composition closure) are settled *inside the fixture boundary* — the
committed loader/validation operate on repo fixtures. D3 decides how the same
guarantees hold when the adopted package and its members live in a **live
workspace** (ADR-0031 residency `L`), not a committed fixture. It is the named
production deferral of ADR-0027.

## Decision summary (tiered)

- **Tier 2 (default + veto, prototype-backed):** D3 production resolver. The
  foreman proposes a default resolution contract; the owner may veto. Rival
  evidence is still required every round (ADR-0013 2026-07-13). Lower stakes than
  D1/D2: a resolution defect is a correctness/availability failure, and the
  *leak* surface is already walled by ADR-0031 (D3 must not bypass it, but does
  not own it).

## Why this topic exists

Foundation proved exclusive projection and byte-verification against committed
fixtures. The milestone's real run reads an adopted package that is **not** a repo
fixture — it lives in `L`. Nothing yet defines resolution at that boundary:
locating the adopted package, verifying member bytes, and projecting the exclusive
resolved member graph when the source is the live workspace. Settling it is what
lets a real run execute on ratified content without weakening ADR-0027 d7 or
ADR-0028.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| D3-P1 | The **production resolution contract**: how adopted package(s) resolve to their **exclusive resolved member graph** (ADR-0027 d7) when package + members reside in the live workspace (ADR-0031 `L`) rather than a committed fixture — locating the adopted package, **byte-verifying** every member and the package instance (ADR-0028), projecting the exclusive graph, and holding co-located unpinned files inert. The production path must be a strict **superset of guarantees** of the fixture path (never a weaker sibling). | Primary |
| D3-P2 | **Discharge/defer ledger** against ADR-0027/0028's named production conditions: which the production resolver **discharges** (member-byte verification as installed, exclusive projection enforced at the production boundary) vs which remain **explicitly deferred** (e.g. ADR-0027 N1/N2 fact-surface joins, embedded schema-byte checksums per ADR-0027's partial rejection). No silent partial discharge. | Dependent |

Out of scope: the D1 residency mechanics (settled, ADR-0031 — consumed), the
contribution event (D2, ADR-0032 — the resolver reads facts, not contributions),
new tax content, OCR/UI, and the N1/N2 fact-surface joins (their own successor
decision).

## Gate 1 — Eligibility

- Future blast radius: **3** — every real run resolves through this boundary; the
  production/fixture parity guarantee is precedent for all later content.
- Migration cost: **1** — additive to the committed loader/validation; the fixture
  path stays as the reference.
- Residual paper uncertainty: **2** — the production-source resolution shape and
  the byte-verification-at-`L` boundary are undesigned; the discharge/defer ledger
  is unspecified.
- Inability to test cheaply: **1** — a scratch out-of-repo workspace holding a
  synthetic adopted package verifies resolution + exclusive projection cheaply.

Total: **7**. Prototype-eligible.

## Gate 2 — Paper evidence

Each builder resolves these synthetic cases (all content synthetic; the
"production" source is a scratch out-of-repo workspace per ADR-0031):

1. **Clean production resolution.** A synthetic adopted package + members in a
   scratch `L` → resolver produces the exclusive resolved member graph; a run
   executes on it and publishes. Show parity with the same package resolved from a
   committed fixture.
2. **Exclusive projection beyond fixtures (ADR-0027 d7).** A co-located
   unpinned/unadopted file in `L` is **not** executable or renderable — the
   resolver excludes it from the resolved graph.
3. **Member byte-verification (ADR-0028).** A member whose bytes do not match its
   pinned checksum → **reject at load** (fail-closed, not fail-open); a
   package-instance checksum mismatch → reject. Probe both.
4. **D1 interlock (must not bypass ADR-0031).** The resolver reads adopted content
   from `L`; it never copies live package content into a tracked or pushable
   artifact, and a resolver path that would is rejected by the ADR-0031 boundary.
   (D3 consumes the wall; it does not re-prove it.)
5. **Negative — silent partial load.** A package missing a ratified member kind →
   reject, never a silent partial resolution (ADR-0027 context).
6. **Discharge/defer ledger (D3-P2, mandatory).** An explicit list mapping each
   ADR-0027/0028 named production condition to discharged-here or
   still-deferred-with-reason — no item unaccounted.

For each design: claim → resolver/validation change → load/projection behavior →
resolved graph and the reject/accept observed. Cases 3 and 6 are mandatory. If
paper makes the contract clear, stop at paper.

## Gate 3 — Evidence depth per question

Authorized level: **Rung 2** — paper resolver/validation diffs plus throwaway
probes against the committed loader/validation and a scratch out-of-repo workspace
holding a synthetic adopted package. Authorized above paper because
byte-verification and exclusive projection at the production boundary must be
*probed* (show a mismatch actually rejected and a co-located file actually
excluded), not asserted. No production resolver code merges — that is milestone
Track 1/3.

## Gate 4 — Cost caps

- Two paper builders: incumbent plus **clean-room rival** (sealed), each producing
  all six cases and both propositions.
- No repair pass pre-authorized.
- Two reviewers (Governance Medium, Adversary Medium), independent contexts.
- Charter ≤ 100 lines; **design ≤ 300 lines**; examination ≤ 120 lines; reviews
  lean but uncapped; **total topic Markdown target ≤ 1,800 lines** (recalibrated
  cap — see the foreman role template).

## Gate 5 — Triage

Foreman classifies every finding. Decision-blocking only: the production
resolution contract preserving exclusive projection + byte-verification as a strict
superset of the fixture path (D3-P1), the fail-closed byte-verification (case 3),
the D1-interlock non-bypass (case 4), and the completeness of the discharge/defer
ledger (D3-P2, case 6). Deferred: the N1/N2 fact-surface joins, embedded
schema-byte checksums, and any implementation bytes.

## Gate 6 — Minimum converged subset

The floor is D3-P1: a production resolution contract that **byte-verifies every
member and the package instance fail-closed** and **projects the exclusive resolved
member graph** from a live-workspace source, provably a superset of the fixture
path's guarantees, plus the D3-P2 ledger accounting for every ADR-0027/0028 named
condition.

## Gate 7 — Production boundary

Only documents merge. Accepted structures become a Tier-2 ADR (**candidate number
0033**). The production resolver, byte-verification at `L`, and exclusive
projection are implemented in the milestone's Track 3 afterward, discharging the
ADR-0027/0028 conditions the D3-P2 ledger names.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | Medium | Scope and conformance steward; owns triage, the running cap total, and the evidence ladder |
| Incumbent builder | High | First design; resolution contract, byte-verification, exclusive projection, discharge ledger |
| Rival builder | High | Clean-room rival, sealed from the incumbent; all six cases, both propositions |
| Governance reviewer | Medium | Conformance to ADR-0027 d7 / ADR-0028 (byte-verification, quantity/composition closure), ADR-0031 interlock, and the fixture/production parity guarantee |
| Adversary reviewer | Medium | Break parity (a production path weaker than the fixture path); slip an unverified or co-located member into the resolved graph; make byte-verification fail open; bypass the ADR-0031 wall via resolution |

Reviewer seats are named here; owner approval of this plan is the standing
authorization for the foreman to dispatch them as sub-agents in independent
contexts (ADR-0013 reviewer-dispatch amendment).

## Review measurements

Governance: the production path preserves ADR-0027 d7 exclusive projection and
ADR-0028 byte-verification as a strict superset of the fixture path; the
discharge/defer ledger accounts for every named condition without silent partial
discharge; the ADR-0031 interlock is consumed, not weakened. Adversary: resolve a
package with a co-located unpinned file and see if it executes; mutate a member's
bytes and see if it loads; find a production/fixture guarantee gap; and attempt to
leak live package content into the repo via resolution.

## Data safety

All package content, members, values, and identifiers in every case, charter, and
review are synthetic; the "production" source is a scratch out-of-repo workspace
per ADR-0031. No real content appears in the topic's Markdown; a real-shaped
fixture states how it was synthesized (ADR-0031 D1-P2 independent-construction).
