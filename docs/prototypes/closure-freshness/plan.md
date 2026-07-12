# Prototype Plan: Closure Freshness

Audience: Agents

Status: **approved by owner, 2026-07-12.** Tier-3 decision process. Builder and
review seats remain owner-launched unless explicitly delegated.

Problem: a closure-backed empty zero pins a true closure and mapping but no
member finding. A later, previously unknown family member therefore has no
existing ADR-0010 edge to the old zero. Manual closure withdrawal is not an
acceptable correctness mechanism. Any solution must remain record-derived and
respect Article 7's derivation/individuation edge exclusivity and the Ontology's
reserved T1 derived-finding authority boundary.

## Gate 0 — Decision inventory

| Id | Candidate decision | Standing |
|---|---|---|
| CF-P1 | Closure authority is fresh only relative to a declared family-membership horizon; a later relevant member assertion or removal makes prior closure authority stale until re-attestation. | Primary |
| CF-P2 | Closure-backed result currency reaches later member changes through an authorized derivation or individuation structure—never a third standing-affecting edge or an unrecorded trigger. | Tightly dependent secondary |

## Gate 1 — Eligibility

Blast radius 2; migration cost 2; residual paper uncertainty 2; inability to
test cheaply in production 2; total **8**. This shapes every future closure-
backed result and touches reserved governance meaning. Tier 3.

## Gate 2 — Paper evidence first

Each rival resolves:

1. empty family → true closure → zero;
2. later new member assertion without manual closure correction;
3. member correction with unchanged membership;
4. member displacement/removal;
5. re-attestation after the change;
6. rebuild from the act log reaching identical currency;
7. two independent families where one changes and the other remains fresh.

Required per design: ordered act/state table; producer → authority → edge →
currency consumer → failure map; two positives/two negatives; exact explanation
pins; and classification of every standing effect as derivation or
individuation. If a design requires a third edge or reserved derived-authority
meaning, it must say so and fail rather than hide it.

## Gate 3 — Evidence depth per proposition

Start at paper. CF-P1 may settle semantically at paper while CF-P2 advances to a
small throwaway act-log/currency reducer. The only reason to climb is inability
to prove rebuildable late-member invalidation and no-resurrection using the
declared two-edge structure. No production runner or persisted workspace is
authorized in this prototype.

## Gate 4 — Cost

- Two independent paper designs, one clean-room rival.
- One bounded repair at a time under delegated foreman progression.
- Two Medium/medium owner-launched reviewers by default; specialist only if a
  reducer runs.
- No review line caps. Builder artifacts: charter ≤100, examination ≤150;
  topic Markdown target ≤1,200 lines.

## Gate 5 — Triage

Decision-blocking only: late-member zero remains current; rebuild differs from
incremental projection; a third edge appears; derived authority is assumed; one
family invalidates another; removal resurrects old zero. UI, tax content,
coverage presentation, and schema ids are deferred.

## Gate 6 — Minimum convergence

CF-P1 observable freshness and CF-P2 authorized currency path must both
converge before closure-backed zero can ship. Partial ratification may record
semantic outcome, but it does not unblock implementation without the machinery
path.

## Gate 7 — Production boundary

Prototype reducers are evidence only. An accepted Tier-3 ADR may amend or
supersede governance/ADRs as required; governance text itself changes only by
version and explicit owner ratification. Production reimplements after that.

## Gate 8 — Roles

| Role | Tier | Reason |
|---|---|---|
| Foreman | High/high | Tier-3 boundary, edge classification, scope control |
| Incumbent builder | High/high | Novel authority/currency synthesis |
| Rival builder | High/high | Independent two-edge alternative |
| Governance reviewer | Medium/medium | Explicit Article 7/T1 measurement |
| Adversary reviewer | Medium/medium | Late-member, rebuild, isolation, resurrection cases |

Builders and reviewers are owner-launched unless the owner directs otherwise.

## Data safety

All acts, families, findings, and amounts are synthetic and visibly non-real.
