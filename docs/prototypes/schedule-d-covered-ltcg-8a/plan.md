# Prototype Plan: Covered Long-Term Gains, Schedule D Line 8a

Audience: Agents

Status: **proposed — awaiting owner approval**. Approval and merge activate
Track 0.

Topic: decide (P1) how a covered, long-term, gain-only Form 1099-B
transaction becomes a closed, correctable source family one level below the
existing statement-identity pattern, and (P2) how the nine-part Schedule D
completeness boundary is declared and checked without a thin "Schedule D
complete" assertion. P3 (Schedule D content and the QDCG/line-16 successor
binding) runs as a paper spike inside the same evidence rounds rather than a
full committee loop, per its Gate 1 score.

This plan governs prototype evidence only. Production adoption remains in
milestone Tracks 1–3.

## Binding inputs

- Milestone plan:
  `docs/phases/engine-breadth/milestones/schedule-d-covered-ltcg-8a.md`.
- ADR-0036: the schedule attachment ontology (attachment citizen states,
  `collect_members`, itemization tie-out, presence-semantics completeness),
  already demonstrated on a Schedule D stub.
- ADR-0050: the accepted component-backed `schedule-d-required` conclusion
  (C1-C4) and its line-16 QDCG successor bound to the box-2a line-7a value.
  Immutable history; this topic proposes an additive successor, never an
  in-place edit.
- ADR-0015/0016: statement-instance identity and source-family claim and
  composition, the pattern P1 extends one level deeper.
- Official 2025 Schedule D instructions (line 8a worksheet and eligibility
  conditions) and Form 1099-B instructions (covered, basis-reported-to-IRS,
  long-term indicators).
- Published history is immutable. Prototype examples may propose successor
  shapes but may not edit existing schemas, content, or accepted ADRs.

## Scope

The topic carries two primary propositions and one secondary:

1. what identifies and closes a covered long-term gain-only transaction
   family (P1);
2. how the nine-part absent-source completeness boundary is declared and
   checked (P2); and
3. how Schedule D content and the QDCG/line-16 successor bind to it without
   double-counting or precedence ambiguity against the existing box-2a route
   (P3, paper spike).

The incumbent and rival must answer P1 and P2 against the same paper cases.
They may disagree per proposition; reviewers report sufficiency per
proposition rather than one monolithic verdict.

## Non-goals

- No short-term transactions, capital losses, loss limitation, carryovers,
  Form 8949, noncovered securities, digital assets, taxpayer-side basis or
  gain adjustments, wash sales, collectibles, or QOF computation.
- No production code, schema publication, manifest update, package release,
  golden regeneration, or browser session.
- No edit to ADR-0050 or any other accepted ADR, published schema, or
  historical content citizen.
- No redesign of the attachment ontology, contribution boundary, or
  presentation contract; P3 instantiates ADR-0036 with content, it does not
  reopen it.
- No real facts, values, documents, dispositions, workspace locations, or
  derived private artifacts.

## Gate 0 — Decision inventory

| Id | Proposition | Standing | Gate-1 score and outcome |
| --- | --- | --- | --- |
| P1 | **Transaction source family and identity.** Decide the broker-and-statement identity plus transaction-member identity, correction/supersession behavior at transaction grain, and multi-broker/multi-transaction closure. | Primary | Blast 2 + migration 1 + uncertainty 2 + test cost 1 = **6, prototype eligible** |
| P2 | **Completeness-boundary declaration shape.** Decide whether the nine-part absent-source universe is one synthesized checked conclusion (ADR-0050 C1-C4 style) or a set of independently read closure/absence claims consumed directly by the attachment and line-16 rules. | Primary | 2 + 1 + 2 + 1 = **6, prototype eligible** |
| P3 | **Schedule D content and QDCG/line-16 binding.** Decide the line 8a/15/16 attachment content as an ADR-0036 instantiation and the line-16 successor binding QDCG to the Schedule D result alongside the existing box-2a route. | Secondary | 1 + 1 + 2 + 1 = **5, paper spike plus ADR draft** |

No fourth proposition may enter this topic. A missing generic substrate is
triaged as a separate decision or prerequisite, not absorbed.

## Rival shapes

### P1 — Transaction identity

- **Incumbent — nested member identity.** Extend the existing
  statement-instance pattern: the transaction is a member fact nested under
  the broker-and-statement family, keyed by tax year + broker + logical
  statement entity + logical transaction entity, mirroring how K-1 and
  market-discount members nest under their statement families.
- **Rival — independent transaction family.** Model the broker-and-statement
  identity as a contributed anchor fact and the transaction identity as its
  own closed family keyed to that anchor, so correction and closure operate
  at transaction grain independent of statement-level correction.

### P2 — Completeness boundary

- **Incumbent — synthesized checked conclusion.** Generalize ADR-0050's
  C1-C4 pattern to a single checked `schedule-d-line8a-eligible` (or similar)
  conclusion over nine contributed/derived component predicates, one per
  absent-source claim, with presence-before-value and no default.
- **Rival — direct multi-read completeness.** No synthesizing citizen. The
  attachment and line-16 rules each `require_closed` the composable families
  (eligible long-term family, box-2a family) directly and read a set of
  independently presence-checked contributed absence declarations for the
  non-composable sources (K-1 gains, Forms 2439/4684/4797/6252/6781/8824,
  lines 18/19, 1099-DA/QOF), reusing the Schedule-B Part-III presence-
  semantics idiom ADR-0036 already generalizes instead of a new conclusion
  shape.

### P3 — Schedule D content and QDCG binding (paper spike)

- **Incumbent — line-16 state-partition extension.** A new versioned line-16
  successor extends ADR-0050 decision 7's branch structure with an
  additional Schedule-D-sourced case, enumerating {box-2a QDCG path,
  Schedule-D QDCG path, ordinary} explicitly at line 16.
- **Rival — shared selected-gain symbol.** Push the branch decision upstream
  of line 16: a new "selected preferential-base" publication that either
  route (box-2a direct or Schedule D) produces exactly one of, consumed by a
  single line-16 rule unchanged in shape from the existing QDCG state
  partition's structure, differing only in which producer is currently
  selected.

Both shapes must preserve the current owner-controlled context and may not
infer an absent condition. The rival is not allowed to win by silently
expanding production scope; any extra facts it needs are part of its cost
and must be explicit in the paper instances.

## Gate 1 — Eligibility

P1 and P2 score 6 and are prototype eligible; P3 scores 5 and runs as a
paper spike inside the same rounds — if paper distinguishes or converges the
P3 shapes, no separate committee loop opens for it.

## Gate 2 — Paper instantiation

All identities and values are obviously synthetic (`demo.*` / `demo-*`).
Each Builder supplies concrete instances, not prose placeholders.

### Shared case matrix

1. **Eligible single broker, single transaction.** One synthetic Form 1099-B
   transaction meets every source-class condition. Show source membership,
   closure, Schedule D line 8a/15/16, line 7a, line 9, and QDCG inputs.
2. **Eligible single broker, multiple transactions.** Two transactions from
   one broker statement. Show the subtotal, exact member pins, and line 8a
   including each transaction once, remaining distinct members.
3. **Eligible multiple brokers.** Transactions from two distinct brokers.
   Show the combined family closure and Schedule D line 8a sum.
4. **Transaction correction.** A corrected transaction supersedes the prior
   amount at the same logical transaction identity; a second original
   transaction from the same broker is unaffected and remains distinct.
5. **Completeness component missing, each of the nine.** In turn, each
   named absent-source component (short-term presence, current loss,
   inbound carryover, Form 8949 transaction, K-1 gain, Form 2439/4684/4797/
   6252/6781/8824, lines 18/19 source, 1099-DA/QOF flow) is present or its
   absence declaration is missing. The walk names every currently missing or
   violated component and publishes neither Schedule D nor a fabricated
   line 7a.
6. **Box-2a interaction, present.** Box 2a is closed with a nonzero member
   alongside an eligible long-term transaction family. Show no double-count
   into line 9 and the selected QDCG binding (P3).
7. **Box-2a interaction, closed empty.** Box 2a is closed empty; only the
   Schedule D route contributes. Show the Schedule-D-only QDCG binding.
8. **Family lifecycle.** Closed-empty, open, undeclared, stale-horizon for
   the eligible transaction family. State whether closed-empty produces
   zero, inapplicability, or another disposition and why.
9. **Historical reach-around attack.** A rule attempts to collect a raw
   transaction member directly into line 9 or QDCG instead of the selected
   Schedule D publication, or a package mixes an incomplete completeness
   boundary with a published Schedule D result. The design rejects the graph
   rather than double-counting or trusting an incomplete universe.
10. **Downstream double-count attack.** Line 9 or QDCG receives gain through
    both the box-2a route and the Schedule D route for the same amount, or
    QDCG reads transaction content directly instead of the selected
    publication. The topology makes the duplicate unrepresentable or fails
    closed.
11. **Non-covered / adjustment-code transaction rejected.** A transaction
    with a market-discount, wash-sale, ordinary, or QOF indicator, or with
    proceeds less than basis, is rejected from or excluded by the eligible
    family rather than silently admitted.

### Per-proposition evidence

For each P1, P2, and P3, each Builder provides:

- two positive concrete instances;
- two meaningful negative instances;
- one lifecycle trace;
- a producer → authority → consumer → failure map;
- the exact accepted contracts consumed unchanged (including ADR-0050 and
  ADR-0036);
- proposed successor contract sentences; and
- unresolved questions and production conditions.

Cases 4, 5, 6, 7, 9, 10, and 11 are mandatory negatives or lifecycle
evidence.

**If paper distinguishes the identity and completeness topologies and
converges P3's binding shape, stop at paper.**

## Gate 3 — Evidence ladder

Initially authorized: **rung 1, static schema/content instances only**.

One climb to rung 2 is permitted only if paper cannot answer this question:

> Can the committed schema/package validators mechanically distinguish the
> selected transaction-identity and completeness-boundary representations
> and reject an incomplete-universe or double-counted graph?

Any rung-2 work is a minimal validator/resolver mutation probe on throwaway
fixtures. Rung 3 requires both reviewers to identify the same unresolved
evaluator-semantics question. Rung 4 is not authorized for contract
selection. Prototype code never becomes a production candidate.

## Gate 4 — Fixed caps and session review

- Two Builder iterations total covering P1 and P2 jointly: one incumbent and
  one clean-room rival, each answering both propositions against the shared
  case matrix. P3's paper spike is produced alongside these iterations, not
  as a separate build.
- One owner-directed repair pass maximum after the rival round unless the
  owner explicitly authorizes a second.
- Two default committee Reviewers.
- A third Reviewer only for one named uncertainty outside both default
  measurement charters.
- Three total prototype iterations is the hard owner check-in boundary; a
  no-progress iteration stops immediately.
- Documents have no line cap. Authors stop when the declared cases,
  proposition reports, and evidence rung are complete.

At every Builder or review session boundary, the foreman records evidence
gained, cost still required, and whether a cheaper disposition is available.

## Gate 5 — Finding triage

The foreman classifies every finding before another iteration:

- `decision-blocking`: P1 identity/closure sufficiency; P2 completeness
  honesty or an unrepresentable double-count/reach-around; P3 QDCG binding
  ambiguity between the two routes.
- `production-condition`: implementation or kill-test work after the
  contract is settled.
- `separate-decision`: a generic citizen, validator, expression, or
  authority mechanism not bounded to this slice.
- `deferred-breadth`: short-term transactions, losses, carryovers, Form
  8949, other capital-gain source forms, digital assets, real-data
  operation.
- `non-blocking defect`: a local example or document error that does not
  change a proposition.

Only decision-blocking findings may support an owner-approved repair
amendment. Reviewer recommendations do not enlarge the charter.

## Gate 6 — Minimum converged subset

The topic may close only if evidence supports all of:

1. one transaction identity/closure path where correction preserves logical
   transaction identity and separate broker sales remain distinct;
2. one declared completeness-boundary shape that honestly blocks Schedule D
   and the direct route on any of the nine missing/violated components,
   never assumes absence, and never fabricates Schedule D from a thin
   assertion;
3. one Schedule D attachment content shape (line 8a/15/16) as an ADR-0036
   instantiation with the tie-out invariant applying;
4. one QDCG/line-16 binding that uses the Schedule D result for this class
   without double-counting or reach-around against the existing box-2a
   route; and
5. complete pins and displacement edges for every current authority/source
   input, with ADR-0050 untouched as immutable history.

If P1 and P2 converge but a nonessential portion of P3 does not, partial
ratification is allowed only when the accepted subset still specifies an
implementable honest Schedule D route. Otherwise the owner stops or
recharters the topic.

## Gate 7 — Production-adoption boundary

Prototype branches are disposable evidence. Only the plan, charters,
designs, examinations, reviews, process log, disposition, and any required
evaluation analysis merge with the accepted ADR decision unit.

Production Tracks 1–3 reimplement accepted contract sentences independently.
No prototype code, fixture, helper, schema, or package artifact is copied
into production merely because it worked.

## Gate 8 — Role and capability plan

| Role | Capability | Effort | Measurement or output | Launch shape |
| --- | --- | --- | --- | --- |
| Foreman | High | high | Scope/economy stewardship, conformance, triage, disposition recommendation | Current thread |
| Incumbent Builder | High | high | Nested-identity + synthesized-conclusion shape over the shared cases, plus P3 spike | Owner launch |
| Rival Builder | High | high | Independent-family + direct-multi-read shape over the shared cases, plus P3 spike | Owner launch |
| Contract/adversary Reviewer | High | high | Accepted-contract fidelity, immutability, completeness-honesty and double-count attacks | Independent context |
| Expressiveness Reviewer | Medium–High | medium | Case-by-case recoverability, distinguishability, and cheapest sufficient evidence | Independent context |
| Repair Builder, if directed | Medium–High | medium | Only the owner-approved blocking delta | Resume the selected design context when available |

The foreman records the actual launch mode and any capability adjustment
when each role starts. Iterative Builders are owner-launched. Review
contexts remain isolated from each other until both notes are filed.

## Review measurements

### Contract/adversary Reviewer

Failure means at least one of:

- a design edits ADR-0050, ADR-0036, or any other accepted history instead
  of proposing a successor;
- transaction identity can be lost or merged across distinct broker sales,
  or correction fails to preserve logical transaction identity;
- the completeness boundary can publish Schedule D while any of the nine
  named components is missing, absent-but-unread, or violated;
- box-2a and Schedule D routes can both contribute the same gain to line 9
  or QDCG, or either route can be reached around;
- Schedule D yields a `required-and-complete` disposition without every
  contributing member pinned, or a fabricated attachment appears where the
  boundary is incomplete;
- a required source, closure, declaration, parameter, or citation lacks a
  pin; or
- a proposal requires interpreting governance text rather than consuming an
  accepted contract.

The reviewer reports each attack run against each rival and cites the
concrete paper instance or authorized probe.

### Expressiveness Reviewer

For each rival and each shared case, recover from the artifact alone:

1. the authoritative producer;
2. why Schedule D line 8a applies or does not;
3. the current source set, family closure, and completeness-boundary state;
4. every downstream consumer;
5. what displaces the result; and
6. the exact failure or non-publication state.

Failure means a required answer is missing, inferred only from prose,
differs between equivalent cases without a contract reason, or requires a
more expensive evidence rung merely because the design is underspecified.

Both reviewers return proposition-level sufficiency and dissent. "Looks
good" is not a measurement.

## Round artifacts and traceability

The topic uses:

- `process-log.md`;
- `it1/charter.md`, `it1/design.md`, and `it1/examination.md`;
- `it2/charter.md`, `it2/design.md`, and `it2/examination.md`;
- `reviews/contract-adversary.md`;
- `reviews/expressiveness.md`;
- `disposition.md`; and
- `evaluation-analysis.md` only if the evidence does not converge in one
  clean round, the rival changes the answer's shape, or dissent remains.

Every conclusion cites a paper instance or named exhibit. Prototype code, if
a rung-2 probe is authorized, lives only on the iteration branch and is
preserved by the required exhibit tag.

## Process conformance

The foreman maintains `process-log.md` as events happen against the
repository's incident categories. The foreman checks role separation,
clean-room isolation, case completion, rung compliance, and review
measurements; the foreman does not review artifact quality.

Each owner disposition packet contains:

- evidence status per proposition;
- process incidents since the prior check-in;
- one sampled review for measurement quality;
- unresolved questions and their cheapest next rung; and
- a recommendation to accept, partially accept, repair, recharter, or stop.

## Data safety

All examples use obviously synthetic `demo.*`/`demo-*` actors, statements,
identifiers, values, horizons, and citations. No personal source shape is
copied; real content informs scope only through the existing
non-descriptive repository record. No workspace path, real disposition,
refusal reason, document, prior return, screenshot, browser output, or
generated private artifact enters any topic artifact.
