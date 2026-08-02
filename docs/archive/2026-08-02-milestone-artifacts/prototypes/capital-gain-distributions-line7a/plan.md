# Prototype Plan: Capital-Gain Distributions to Form 1040 Line 7a

Audience: Agents

Status: **approved — the owner merge is the approval record and activates
Track 0**.

Topic: decide the smallest honest contract that turns Form 1099-DIV box 2a
from recorded/non-composable content into the direct Form 1040 line 7a route
when Schedule D is authoritatively not required, then hands the amount to line
9 and the QDCG computation without weakening existing closure or contradiction
guarantees.

This plan governs prototype evidence only. Production adoption remains in
milestone Tracks 1–3.

## Binding inputs

- Milestone plan:
  `docs/phases/engine-breadth/milestones/capital-gain-distributions-line7a.md`.
- ADR-0035: current dividend universe, recorded box 2a, and
  `CAPITAL_GAIN_DISTRIBUTION_RECORDED`.
- ADR-0038: contributed capital-gain-distribution and Schedule-D-required
  declarations, the contradiction interlock, and the deliberate absence of a
  box-2a route to line 16.
- Official 2025 Form 1040 instructions: the direct line-7a exception applies
  when the return's only capital gains are eligible box 2a distributions and
  Schedule D is not required.
- Published history is immutable. Prototype examples may propose successor
  shapes but may not edit existing schemas, content, or accepted ADRs.

## Scope

The topic carries one primary proposition and two tightly dependent
secondaries:

1. what facts authorize the direct route;
2. how box 2a becomes a closed composable family; and
3. how line 7a feeds line 9 and QDCG while Schedule-D-required cases remain
   honestly outside this milestone.

The incumbent and rival must answer all three against the same paper cases.
They may disagree per proposition; reviewers report sufficiency per
proposition rather than one monolithic verdict.

## Non-goals

- No Schedule D, Form 8949, Form 1099-B, capital-loss carryover, transaction
  inventory, QOF implementation, or general capital-gains claim.
- No production code, schema publication, manifest update, package release,
  golden regeneration, or browser session.
- No decision for Form 1099-DIV boxes 2b, 2c, 2d, 2f, 3, 5, 7, or 12 beyond
  what the authority proposition must acknowledge.
- No redesign of the contribution boundary, attachment ontology,
  presentation contract, or correction-authority policy.
- No real facts, values, documents, dispositions, workspace locations, or
  derived private artifacts.

## Gate 0 — Decision inventory

| Id | Proposition | Standing | Gate-1 score and outcome |
| --- | --- | --- | --- |
| P1 | **Direct-route authority and completeness.** Decide whether ADR-0038's contributed `schedule-d-required` conclusion is sufficient authority or whether eligibility must be derived from finer contributed assertions. Define missing, `"yes"`, `"no"`, correction, and supersession behavior. | Primary | Blast 2 + migration 1 + uncertainty 2 + test cost 1 = **6, prototype eligible** |
| P2 | **Box-2a family promotion.** Decide the successor statement/member/family/closure shape and how it coexists with historical recorded/non-composable content and the current signal/interlock. | Secondary | 2 + 2 + 1 + 1 = **6, prototype eligible; paper first** |
| P3 | **Line-7a and QDCG handoff.** Decide the declared binding path into line 7a, line 9, and QDCG for the direct route, preserving honest inapplicability when Schedule D is required. | Secondary | 2 + 1 + 2 + 1 = **6, prototype eligible** |

No fourth proposition may enter this topic. A missing generic substrate is
triaged as a separate decision or prerequisite, not absorbed.

## Rival shapes

The round compares genuinely different authority topologies:

- **Incumbent — conclusion-level authority.** Reuse the existing contributed
  categorical `schedule-d-required` fact as the direct-route authority. Add
  only the successor family and declared bindings necessary to publish line
  7a and feed QDCG.
- **Rival — component-backed eligibility.** Represent the Form 1040 exception's
  component conditions as explicit contributed assertions and derive
  direct-route eligibility from them. Show whether the existing
  `schedule-d-required` declaration remains an input, becomes a checked
  conclusion, or is displaced by a successor contract.

Both shapes must preserve the current owner-controlled context and may not
infer an absent condition. The rival is not allowed to win by silently
expanding production scope; any extra facts it needs are part of its cost and
must be explicit in the paper instances.

For P2/P3, each Builder may choose the smallest topology consistent with its
authority shape, but must state where it differs from the other shape in
identity, closure, pins, supersession, and failure behavior.

## Gate 1 — Eligibility

All three propositions score 6 and are eligible, but eligibility does not
authorize expensive evidence. P1 is the comparison's primary uncertainty.
P2 and P3 advance only as far as needed to prove that each authority shape can
or cannot close into a coherent production contract.

## Gate 2 — Paper instantiation

All identities and values are obviously synthetic (`demo.*` / `demo-*`).
Each Builder supplies concrete instances, not prose placeholders.

### Shared case matrix

1. **Eligible single payer.** One synthetic Form 1099-DIV has box 2a present;
   direct-route authority is complete and negative for Schedule D. Show source
   membership, closure, line 7a, line 7b disposition, line 9, and QDCG inputs.
2. **Eligible multiple payers.** Two box-2a members at one horizon. Show the
   subtotal, exact member pins, and line 7a including each amount once.
3. **Authority missing.** Box 2a is present but the facts needed to authorize
   the direct route are incomplete. The walk names every currently missing
   contributable fact and publishes neither line 7a nor a fabricated Schedule
   D result.
4. **Schedule D required.** Authority resolves to `"yes"`. The direct route is
   honestly inapplicable; no Schedule D artifact exists, and line 16 does not
   reach around the boundary.
5. **Contradiction interlock.** A current `"no capital-gain distributions"`
   declaration conflicts with box 2a in declaration-first, statement-first,
   and same-batch orders. No ordering admits both.
6. **Authority lifecycle.** A complete direct-route state is corrected or
   superseded into Schedule-D-required. Show displacement of line 7a, line 9,
   and line 16 through declared dependency edges. Then show the reverse
   transition without editing history.
7. **Family lifecycle.** Closed-empty, open, undeclared, stale-horizon, member
   correction, and member removal. State whether closed-empty produces zero,
   inapplicability, or another disposition and why.
8. **Historical reach-around attack.** A rule attempts to collect the existing
   recorded/non-composable box content, or a package mixes historical and
   successor representations. The design rejects the graph rather than
   double-counting or trusting both.
9. **Downstream double-count attack.** Line 9 or QDCG receives box 2a through
   two paths, or QDCG reads statement content directly instead of the selected
   subtotal/publication. The topology makes the duplicate or reach-around
   unrepresentable or fail closed.
10. **Qualified-zero neighbor.** Qualified dividends are zero while box 2a is
    present and the direct route is authorized. Show the selected QDCG/ordinary
    tax path without introducing an unconditional dependency that breaks
    ADR-0038's reduction behavior.

### Per-proposition evidence

For each P1–P3, each Builder provides:

- two positive concrete instances;
- two meaningful negative instances;
- one lifecycle trace;
- a producer → authority → consumer → failure map;
- the exact accepted contracts consumed unchanged;
- proposed successor contract sentences; and
- unresolved questions and production conditions.

Cases 3, 4, 5, 6, 8, and 9 are mandatory negatives or lifecycle evidence.

**If paper distinguishes the authority topologies and closes P2/P3, stop at
paper.**

## Gate 3 — Evidence ladder

Initially authorized: **rung 1, static schema/content instances only**.

One climb to rung 2 is permitted only if paper cannot answer this question:

> Can the committed schema/package validators mechanically distinguish the
> selected successor representation from historical recorded/non-composable
> box-2a content and reject a mixed graph?

Any rung-2 work is a minimal validator/resolver mutation probe on throwaway
fixtures. Rung 3 requires both reviewers to identify the same unresolved
evaluator-semantics question. Rung 4 is not authorized for contract selection.
Prototype code never becomes a production candidate.

## Gate 4 — Fixed caps and session review

- Two Builder iterations total: one incumbent and one clean-room rival.
- Two owner-directed repair passes maximum after the rival round. The owner
  added the second and final pass on 2026-07-28 after Repair 1 confirmation
  returned `NOT READY`.
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

- `decision-blocking`: P1 authority sufficiency; P2 historical/successor
  exclusivity or closure; P3 double-count, reach-around, or lifecycle failure.
- `production-condition`: implementation or kill-test work after the contract
  is settled.
- `separate-decision`: a generic citizen, validator, expression, or authority
  mechanism not bounded to this slice.
- `deferred-breadth`: Schedule D and excluded capital-gain source families.
- `non-blocking defect`: a local example or document error that does not change
  a proposition.

Only decision-blocking findings may support an owner-approved repair amendment.
Reviewer recommendations do not enlarge the charter.

## Gate 6 — Minimum converged subset

The topic may close only if evidence supports all of:

1. one explicit authority path for Schedule-D-not-required, with missing,
   `"yes"`, `"no"`, correction, and supersession semantics;
2. one horizon-closed box-2a source path that cannot mix with or collect the
   historical recorded/non-composable representation;
3. one declared line-7a publication path that enters line 9 exactly once;
4. one QDCG handoff for the direct route, with Schedule-D-required remaining
   honestly outside scope;
5. bidirectional and same-batch contradiction safety; and
6. complete pins and displacement edges for every current authority/source
   input.

If P1 converges but a nonessential portion of P2/P3 does not, partial
ratification is allowed only when the accepted subset still specifies an
implementable honest direct route. Otherwise the owner stops or recharters the
topic.

## Gate 7 — Production-adoption boundary

Prototype branches are disposable evidence. Only the plan, charters, designs,
examinations, reviews, process log, disposition, and any required evaluation
analysis merge with the accepted ADR decision unit.

Production Tracks 1–3 reimplement accepted contract sentences independently.
No prototype code, fixture, helper, schema, or package artifact is copied into
production merely because it worked.

## Gate 8 — Role and capability plan

| Role | Capability | Effort | Measurement or output | Launch shape |
| --- | --- | --- | --- | --- |
| Foreman | High | high | Scope/economy stewardship, conformance, triage, disposition recommendation | Current thread |
| Incumbent Builder | High | high | Conclusion-level authority shape over all ten cases | Owner launch |
| Rival Builder | High | high | Clean-room component-backed shape over the same cases | Owner launch |
| Contract/adversary Reviewer | High | high | Accepted-contract fidelity, immutability, authority and lifecycle attacks | Independent context |
| Expressiveness Reviewer | Medium–High | medium | Case-by-case recoverability, distinguishability, and cheapest sufficient evidence | Independent context |
| Repair Builder, if directed | Medium–High by default; High for final Repair 2 | medium by default; high for final Repair 2 | Only the owner-approved blocking delta | Resume the selected design context when available |

The foreman records the actual launch mode and any capability adjustment when
each role starts. Iterative Builders are owner-launched. Review contexts remain
isolated from each other until both notes are filed.

## Review measurements

### Contract/adversary Reviewer

Failure means at least one of:

- a design edits accepted history instead of proposing a successor;
- direct-route authority can be absent, contradicted, or superseded while an
  output remains current;
- historical and successor box-2a representations can both contribute;
- the existing contradiction can be sequenced around;
- Schedule-D-required yields a direct-route publication or a fabricated
  attachment;
- line 9 or QDCG double-counts or reaches around the selected publication;
- a required source, closure, declaration, parameter, or citation lacks a pin;
  or
- a proposal requires interpreting governance text rather than consuming an
  accepted contract.

The reviewer reports each attack run against each rival and cites the concrete
paper instance or authorized probe.

### Expressiveness Reviewer

For each rival and each shared case, recover from the artifact alone:

1. the authoritative producer;
2. why the direct route applies or does not;
3. the current source set and closure;
4. every downstream consumer;
5. what displaces the result; and
6. the exact failure or non-publication state.

Failure means a required answer is missing, inferred only from prose, differs
between equivalent cases without a contract reason, or requires a more
expensive evidence rung merely because the design is underspecified.

Both reviewers return proposition-level sufficiency and dissent. “Looks good”
is not a measurement.

## Round artifacts and traceability

The topic uses:

- `process-log.md`;
- `it1/charter.md`, `it1/design.md`, and `it1/examination.md`;
- `it2/charter.md`, `it2/design.md`, and `it2/examination.md`;
- `reviews/contract-adversary.md`;
- `reviews/expressiveness.md`;
- `disposition.md`; and
- `evaluation-analysis.md` only if the evidence does not converge in one clean
  round, the rival changes the answer's shape, or dissent remains.

Every conclusion cites a paper instance or named exhibit. Prototype code, if a
rung-2 probe is authorized, lives only on the iteration branch and is preserved
by the required exhibit tag.

## Process conformance

The foreman maintains `process-log.md` as events happen against the repository's
incident categories. The foreman checks role separation, clean-room isolation,
case completion, rung compliance, and review measurements; the foreman does not
review artifact quality.

Each owner disposition packet contains:

- evidence status per proposition;
- process incidents since the prior check-in;
- one sampled review for measurement quality;
- unresolved questions and their cheapest next rung; and
- a recommendation to accept, partially accept, repair, recharter, or stop.

## Data safety

All examples use obviously synthetic `demo.*`/`demo-*` actors, statements,
identifiers, values, horizons, and citations. No personal source shape is copied;
real content informs scope only through the existing non-descriptive repository
record. No workspace path, real disposition, refusal reason, document, prior
return, screenshot, browser output, or generated private artifact enters any
topic artifact.
