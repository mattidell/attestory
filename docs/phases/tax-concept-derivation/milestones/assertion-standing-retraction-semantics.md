<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "assertion-standing-retraction-semantics",
  "milestone_state": "closed",
  "status": "CLOSED 2026-09-07. A recorded actor can end the workspace's current support for one identified answer without supplying a replacement value, and every reader agrees about which answer currently stands. A dedicated act contributes a fifth named displacement root behind six admission refusals; the two declared cascade edges are unchanged. One resolution of current standing replaced two across the five kernel admission enforcers, both read models, the derivation layer, the migration path, and both tax-layer readers, closing a production check that accepted a Social Security statement whose filing-status authority had been withdrawn, and preventing a retracted answer from being presented as a live migration claim without weakening ADR-0072's nonzero block. Entity succession and source-family withdrawal were disqualified on executed evidence. Fifteen fact types remain un-withdrawable because capability limits sit in the admission layer; that relocation is a successor milestone by owner disposition. Ratified by ADR-0073. Nominee Allocation Assertion Recording may resume.",
  "scope": [
    "define in plain language the distinction among a stable proposition, an immutable assertion event, and the assertion's current standing",
    "reproduce and bound the current disagreement between full currency projection and admission-time current-value readers",
    "compare the smallest honest lifecycle mechanisms against assert, correct, retract, reassert, attribution, dependency, and concurrency cases",
    "establish a reviewed assertion-standing contract and implement it in the appropriate substrate when the evidence supports one",
    "prove that read models, admission invariants, derivation consumers, and explanations agree about whether a human-authored finding currently supplies support",
    "unify the two current-standing resolutions into one path and close the fail-open source boundary that the split produced"
  ],
  "non_goals": [
    "no nominee-interest tax classification, reduction, information-return conclusion, line-2b change, or Schedule B repair",
    "no production nominee-allocation intake or domain fact type; a nominee-shaped synthetic fact is only a forcing consumer",
    "no universal lifecycle ontology for evidence, entities, grants, elections, derived publications, or source-family membership",
    "no adoption of entity succession or family horizons merely because they can imitate retraction on current machinery",
    "no silent migration or reinterpretation of existing fact types, source families, authorizations, or accepted ADR history",
    "no new generic act or edge until the product semantics, target identity, authority, currency, and consumer behavior are discriminated",
    "no relocation of capability limits out of the admission layer; deferred by owner disposition 2026-09-06 to a named successor milestone"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/adr/0009-derived-finding-shape.md",
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0041-correction-authority-policy.md",
      "docs/adr/0069-standing-workspace-authorization.md",
      "packages/schemas/kernel/act.v1.schema.json",
      "packages/schemas/kernel/act-assertion.v2.schema.json",
      "packages/schemas/kernel/finding.v2.schema.json",
      "packages/schemas/kernel/act-entity-superseded.v1.schema.json",
      "packages/schemas/kernel/act-member-transition.v3.schema.json",
      "packages/schemas/derivation/act-calculation-authorization-end.v1.schema.json",
      "packages/kernel/facts.py",
      "packages/kernel/findings.py",
      "packages/kernel/currency.py",
      "packages/kernel/read_models.py",
      "packages/derivation/authorization.py",
      "PROJECT_PLANNING.md#Lean Production Loop",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "PROJECT_PLANNING.md#Payload Instantiation Gate",
      "AGENTS.md#Data Safety Rules",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Selected product model",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Contract questions",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Fixed cases",
      "packages/derivation/projection.py",
      "packages/tax/ssa_benefits.py",
      "packages/tax/coverage.py",
      "tests/support.py"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Selected product model",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Success and stop conditions",
      "docs/phases/tax-concept-derivation/milestones/assertion-standing-retraction-semantics.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md"
}
-->

# Assertion Standing and Retraction Semantics

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `assertion-standing-retraction-semantics`
- Primary branch: `milestone/assertion-standing-retraction-semantics`
- State: **CLOSED 2026-09-07**; retrospective [`docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md`](/docs/milestone-retrospectives/2026-09-06-assertion-standing-retraction-semantics.md)
- Roadmap role: substrate prerequisite for resuming nominee-allocation recording

## Plain-language purpose

A user can answer a question, correct the answer, stop standing behind it, and
later answer the same question again. Those are not four values of the fact.
They are changes in whether a particular human-authored answer currently
supports the product.

The engine can currently imitate parts of that lifecycle by retiring an entity
or removing a member from a source family. Neither mechanism was designed to
mean “the user retracts this answer,” and they behave differently when the same
question is answered again. The engine also has more than one internal reader
of “current,” and the readers do not account for all displacement mechanisms in
the same way.

This milestone starts from the product behavior rather than selecting whichever
existing mechanism can be made to pass one scenario. It will decide what an
assertion retraction means, determine the smallest architecture that expresses
that meaning, and make every affected consumer agree about current standing.

## Selected product model

The following distinctions are selected direction for this milestone. The
implementation is not selected.

1. **Stable proposition.** A fact identifies one question the workspace can
   answer. Its identity does not change merely because an answer is retracted
   and later supplied again.
2. **Immutable assertion event.** An assertion records that a named actor gave a
   particular answer at a particular time and revision. History does not mutate.
3. **Current support.** A current finding is an answer that presently supplies
   support: it is the answer read models project, admission invariants consult,
   and derivations pin. Current support is derived from recorded acts; it is not
   a stored truth flag and is not the same thing as objective truth. Whether the
   product may further *rely* on a current answer is a separate question
   answered by standing authorization (ADR-0069) and evidentiary standing; this
   milestone does not fold those into currency.
4. **Correction.** A correction supplies a new answer to the same proposition.
   The earlier answer remains historical and the new answer becomes current.
5. **Retraction.** A retraction ends the current support supplied by an answer.
   It supplies no replacement value and asserts no opposite proposition.
6. **Reassertion.** A later assertion may answer the same stable proposition
   again. It is a new event and finding, not a revival or mutation of the old
   event.
7. **Separate neighboring lifecycles.** Replacing or retiring the entity a fact
   concerns may remove the proposition itself. Changing membership in a bounded
   collection may advance that collection's horizon. Withdrawing evidence
   changes evidentiary standing and, on the committed kernel, is not a
   displacement root: a documentary finding citing withdrawn evidence stays
   current while its evidence reference reads `withdrawn`. None of those
   operations is silently treated as assertion retraction merely because its
   present output looks similar.

For the forcing nominee-shaped case, the stable proposition may be rendered
in plain language as: “What amount from this identified payer report does this
user attribute to this named other person?” The user supplies the
answer. No nominee-interest tax classification is part of the proposition.

## Why this milestone precedes further nominee work

The paused nominee-allocation investigation demonstrated two mechanically
possible simulations:

- retire an allocation-statement entity and create a new entity if the user
  later asserts the same content; or
- remove a `(report, owner)` fact from a source family and advance its membership
  horizon.

The first loses a structural link to the stable proposition on reassertion. The
second imports closure, subtotal-authorization, and horizon contracts and still
cannot make a withdrawn fact id current again. Selecting either solely because
it already exists would let the engine dictate the product model.

The same investigation exposed a substrate-level question. Full currency
projection treats entity supersession as a displacement root, while the private
current-value reader used by several admission invariants consults member
withdrawal but not entity supersession. A finding can therefore be non-current
to one consumer and still supply a value to another. Whether that is an
implementation defect or an unsupported combination must be answered from a
declared lifecycle contract, not assumed from the existing call sites.

## Committed behavior at milestone start (the baseline this milestone changed)

This section records the engine as it stood when the milestone opened. It is
the baseline the planning gates verified, not a description of the shipped
result; where the milestone changed one of these behaviors, ADR-0073 and the
closure section below state what it changed to.

Planning gate P2 must re-read and reproduce each claim before it becomes a
prototype premise:

- `act-assertion.v2` carries one immutable finding and has no ending operation.
- same-fact correction is last-current-finding selection under the fact type's
  supersession policy;
- `act-entity-superseded.v1` with no replacement retires an entity, and currency
  displaces findings individuated on it;
- `act-member-transition.v3` removes a family member while advancing a family
  horizon, and its withdrawn-fact set is monotonic;
- a source-family declaration necessarily carries a closure claim and subtotal
  authorization;
- the standing-calculation-authorization family uses a dedicated end act in an
  out-of-kernel fold, which is precedent for separation but not proof that the
  shape transfers to findings;
- `currency.compute_currency` and the admission-time current-value helpers do
  not presently use one common resolution path: `_current_value_for_fact`
  consults `withdrawn_fact_ids` but neither superseded entities nor
  migration-retired fact types (both are roots in `compute_currency`);
- the correction gate (`already_answered`) is a predicate over finding
  *history*, not currency: a fact with any recorded finding is "answered" for
  supersession-policy purposes even if no finding is current;
- evidence withdrawal (`act-evidence-replaced.v1` with no replacement) changes
  `EvidenceLifecycle.status` and is reported by `evidentiary_standing`; it is
  not a currency root and displaces no finding;
- a finding carries no actor; the actor and time of an assertion live only on
  the `act.v1` envelope, and no committed read model maps a finding id back to
  its act; and
- derived dependency displacement, read-model projection, and explanation must
  each be checked independently rather than inferred from one currency result.

For every load-bearing artifact claim, record the artifact and fields read,
relevant sibling fields not relied upon, and every downstream consumer on which
the conclusion depends.

## Scope

The milestone will:

- refine the selected product model into an exact lifecycle contract;
- inventory current assertion, correction, entity, evidence, family,
  authorization-ending, currency, and dependency behavior only as needed to
  establish the boundary;
- compare at least two materially different candidate mechanisms when both
  remain plausible after planning review;
- establish the target rule for retraction, including stale-act behavior, and
  state retraction's admission gate in the same state-gated vocabulary that
  governs correction (ADR-0041);
- establish one authoritative current-standing account for affected consumers;
- implement the selected bounded substrate contract if Track 0 evidence closes
  the decision without an unresolved owner-held product choice;
- exercise it with a synthetic nominee-shaped fact and one existing ordinary
  human-authored fact as a neighboring control; and
- preserve immutable history and recoverable attribution across the lifecycle.

## Non-goals

- No production nominee-allocation fact, mapping, package adoption, or tax rule.
- No information-return determination, line-2b change, Schedule B repair, or
  explanation-interface design.
- No universal unification of evidence withdrawal, entity succession, family
  succession, authorization ending, migration, election, and assertion
  retraction.
- No actor, role, or identity authority concept at admission. ADR-0041 closed
  correction authority to state predicates and rejected actor-scoped
  authority; retraction inherits that rule. The envelope `actor` is recorded
  for attribution and never consulted for admission. A rule that needs to
  know *who* is retracting is stop condition 2, not a design option.
- No new displacement edge kind. A dedicated retraction act may contribute a
  named displacement *root* (the pattern withdrawal and migration already use);
  `DECLARED_EDGE_KINDS` stays `{derivation, individuation}`.
- No reason vocabulary or adjudication workflow unless a fixed case requires it.
- No conversion or migration of existing fact instances.
- No generalized deletion operation. Retraction preserves the record.

## Contract questions

Track 0 must settle or precisely surface:

1. **Target.** Whether a retraction identifies the current finding, its stable
   fact, or both. A stale client must not unknowingly retract a later correction.
   Two staleness layers already differ: the act log refuses any act whose
   `committed_against` is not the workspace revision, and a client that reads
   the latest revision but names an old finding id is not stale at the log.
   The target rule must catch the second case, and it is itself a
   current-standing reader inside admission (question 5). The lead is: the
   payload names one finding id; the fact is derived from it, never supplied
   alongside it; admission refuses unless that finding is current under the
   full projection. Retracting an already-retracted, corrected, entity-displaced,
   or migration-displaced finding is refused on the same rule.
2. **Admission gate.** Retraction is admitted or refused by the target fact
   type's supersession policy exactly as a correction would be (ADR-0041:
   `free`, `locked`, `closed-on-attestation`), never by who is asking. Open
   sub-questions: whether a `locked` fact's single answer may be retracted at
   all, and whether a reassertion after retraction counts as a correction for
   `closed-on-attestation` (the committed `already_answered` predicate says
   yes, because it reads history). P2 answer: retraction obeys the same
   predicate as correction. Under `locked` a retraction is refused, because
   `already_answered` would otherwise leave a permanently unanswerable fact
   (P2-4). Under `closed-on-attestation` a retraction after closure is refused
   and a reassertion after retraction is a correction, gated on the closure
   fact exactly as today. The nominee-shaped fact declares `free`.
3. **Standing projection.** Which acts make an asserted finding current,
   corrected, retracted, or current again, and how those states compose with
   entity and evidence displacement.
4. **Dependency behavior.** What happens to a derived result pinned to an answer
   after retraction and after a later reassertion. Historical results are not
   silently revived.
5. **Admission consistency.** How gate, subset, companion, equality, and
   contradiction enforcement read the same current standing as ordinary read
   models and derivation inputs.
6. **Representation locus.** Whether the selected lifecycle belongs in the
   kernel finding projection or in another reusable fold that can still supply
   authoritative rule inputs without duplicating currentness. P2 answer: the
   kernel projection. `compute_derivation_currency` seeds its closure from
   `kernel_currency.displaced_finding_ids` and nothing else, and the five
   kernel admission enforcers read `FindingState` directly; a fold outside
   `FindingState` cannot reach either without a second currency model
   (P2-1). The lead shape is a `retracted_finding_ids` field on
   `FindingState`, a `_finding_retractions` root contributor parallel to
   `_member_withdrawals` with reason kind `retraction`, and one shared
   current-standing resolution used by admission, the two out-of-kernel
   last-inserted readers, and the read model.
7. **Publication shape.** Whether a new act payload schema or a successor to an
   existing contract is needed. Published schemas remain immutable. P2 answer:
   a new kernel act kind with its own payload schema, instantiated below. An
   assertion successor carrying a retract mode is rejected because the act
   would then mean two things and `_payload_schema_id` selects by nested
   citizen schema, not by mode.
8. **Attribution.** How the original assertion, correction, retraction, and
   reassertion actors and times are recovered without copying them onto every
   fact representation. The committed answer is act-log lookup: finding id to
   the assertion act that carried it; retraction attribution is the retraction
   act's own envelope. Any read-model exposure is derived from that lookup.
   P2 detail: `DisplacementReason.by` names a citizen id, and kernel appliers
   receive only the payload, so a retraction reason cannot name the retracting
   act unless the act id is passed into the applier or recorded in state. That
   is a bounded substrate change the contract must name (P2-6).
9. **Family-member facts.** Whether the current finding of a fact that is
   currently a source-family member may be retracted by the assertion lifecycle
   at all. ADR-0023 routes membership changes through member-transition and
   value corrections through assertion; a retraction leaves the fact a member
   with no current answer, a state no closure or subtotal consumer was written
   for. The lead is refusal at admission (route to member-transition
   withdrawal), parallel to ADR-0023 Decision 1. P2 must read the member
   collection and boundary-validation consumers before this is settled.
11. **Admission invariants under retraction.** Whether ending an answer must
    re-run the admission enforcers that an assertion runs. T0-B found by
    execution that it currently does not: retracting a declared companion
    admits a state that violates the kernel's own companion-presence
    invariant, and the next assertion touching that statement is refused
    until the companion is answered again. A retraction can therefore reach
    a state no assertion could create. The lead is that it must not: the
    enforcers re-run and a violating retraction is refused, which keeps
    retraction inside the same admissible-state set as every other act. T0-C
    settles this by execution, including whether an ordered retraction path
    exists for every real declared relation or whether some facts become
    un-retractable, which is itself a product answer that must be stated
    rather than discovered later.
10. **Reassertion identity.** A reassertion is a new finding with a new id. The
    committed duplicate-id check already refuses reuse of the retracted
    finding's id; the contract states this so revival-by-id-reuse is a tested
    negative, not an assumption. After reassertion the retracted finding
    carries two displacement reasons (retraction, then correction by the new
    finding); explanation consumers must tolerate composed reasons.

## Candidate hypotheses

These are candidates to discriminate, not implementation instructions.

- **H1 — finding-aware retraction in the kernel projection.** A dedicated act
  ends the current support of an identified finding/fact while leaving its
  proposition and history intact. Reassertion supplies a new finding on the same
  fact identity.
- **H2 — separate assertion-standing fold.** A dedicated lifecycle fold
  subscribes to assertions and end acts. It survives only if rules, admission
  enforcement, read models, and explanations can consume one authoritative
  result without creating a second competing currency model. P1 structural
  note: `compute_currency` takes displacement roots only from `FindingState`
  and accepts no caller-supplied roots; kernel admission invariants cannot
  read an out-of-kernel fold without inverting the kernel/derivation
  dependency. H2 therefore survives P1 only in the form "retraction state is
  recorded in `FindingState` and read by one shared resolution path," which is
  H1 under another name. P2 confirms this by reading the derivation-layer
  compose-over projection; if confirmed, Track 0 compares H1 against the two
  controls and no rival prototype is manufactured.
- **Controls — entity succession and family transition.** Exercise both to show
  which behavior belongs to entity identity and collection membership. They may
  be selected only if the product semantics fit without invented closure,
  authority, identity, or migration claims.

If P2 shows that H1 and H2 are not materially different at any affected
consumer, do not manufacture rival prototypes. If they differ, independent
prototype contexts must implement the smallest executable comparison; one
context may not author both shapes.

## Fixed cases

All identifiers and values are synthetic.

| Case | Sequence | Required observation |
| --- | --- | --- |
| L0 — unanswered | Stable fact exists; no assertion | No current answer and no negative claim |
| L1 — assert | User A asserts `450` | One current finding; fact and value from the finding; actor and time from the carrying act's envelope |
| L2 — correct | User A corrects `450` to `250` | Same fact identity; new current finding; old finding historical |
| L3 — retract | User A retracts the current `250` | No current answer; no zero, false, opposite claim, entity retirement, or family succession manufactured |
| L4 — reassert | User A later asserts `250` again | Same stable fact; new finding id current; full ordered history retained; a reassertion reusing the retracted finding's id is refused |
| L5 — independent facts | Pat and Kim have separate propositions; Pat is corrected/retracted | Kim's finding, assertion, and current standing are unchanged |
| L6 — stale retract | Client at the current revision targets the `450` finding after `250` is current | The act refuses at admission, not at the log's revision check; `250` remains current; nothing is silently retracted |
| L7 — different actor | User B attempts to retract User A's answer | Admitted or refused on exactly the predicate that would govern User B correcting the fact (ADR-0041 state gate); envelope actor recorded, never consulted; no identity rule invented |
| L8 — entity succession | The report or owner entity is retired or replaced | The proposition's individuation lifecycle is distinguished from assertion retraction |
| L9 — family transition | An unrelated collection member changes | Assertion standing changes only if the declared contract expressly connects it |
| L10 — derived dependency | A synthetic result pins the current answer; answer is retracted and later reasserted | Old result becomes non-current; later support produces a new result rather than reviving history |
| L11 — invariant consistency | A related fact exercises gate/subset/companion/equality enforcement before and after retraction | Enforcement, read model, and derivation input agree on currentness |
| L12 — evidence standing | Evidence cited by a separate documentary finding is withdrawn | The finding stays current in `compute_currency`; its evidence reference reads `withdrawn` in evidentiary standing; no retraction root appears; retraction of a finding never changes evidence currency |
| L13 — member fact | The current finding of a fact that is currently a source-family member is targeted for retraction | Behavior follows contract question 9; no family horizon advances silently and no subtotal shrinks without a declared member transition |
| L14 — policy gate | The same sequence as L3–L4 on a fact type declaring `locked` and one declaring `closed-on-attestation` | Retraction and reassertion follow the declared supersession policy; `free` is the only policy L1–L4 assume |

## Planning review cycle

No Track 0 charter is filed until both reviewed gates close and their findings
are absorbed into this plan.

1. **P1 — semantic and identity review.** Challenge the selected product model,
   fixed cases, target/authority questions, candidate hypotheses, non-goals, and
   stop conditions. Review for hidden negative claims, entity/fact conflation,
   family/closure leakage, history mutation, and accidental multi-actor policy.
2. **P2 — artifact and consumer map.** Reproduce the current behavior, enumerate
   every current-standing reader and writer reached by the candidates, inspect
   sibling fields and downstream consumers, instantiate complete candidate act
   payloads, and identify the cheapest executable discriminators. Review the map
   before prototypes are chartered.

Each gate is reviewed section by section while the plan is still changing.
Repairs replace the incorrect premise in the plan; later work does not carry a
known-false premise merely because a review record exists.

### Gate P1 — semantic and identity review — **COMPLETE, absorbed 2026-09-05**

Reviewed by the Foreman against the committed kernel at the milestone's plan commit (ADR-0009,
0010, 0023, 0041, 0063, 0069; `facts.py`, `findings.py`, `currency.py`,
`read_models.py`, `act_log.py`; the act and finding schemas). Findings, each
repaired in place above:

- **P1-1 Authority reopened a rejected alternative.** Contract question 2
  asked which *actor* may retract. ADR-0041 rejected actor-scoped authority,
  findings carry no actor, and the envelope `actor` is an untrusted string.
  Repaired: question 2 is now the admission gate in ADR-0041's vocabulary; L7
  and the non-goal are restated; stop condition 2 names the identity tell.
  P2 must inventory the one out-of-kernel reader that compares an act's actor
  to a scope user (`production_resolver.py`) before "never consulted" is
  claimed for consumers.
- **P1-2 Supersession policy was implicit.** L1–L4 silently assumed `free`.
  `already_answered` reads history, so `locked` refuses reassertion after
  retraction and `closed-on-attestation` gates it on closure. Repaired: policy
  sub-questions in question 2; case L14.
- **P1-3 Family/closure leakage through the retracted fact itself.** L9 only
  varied an unrelated member. A retracted member finding leaves a fact that
  admission still counts as a member (`fact_is_member` reads history minus
  withdrawals) while closure and boundary consumers see no current value.
  Repaired: question 9; case L13; the forcing nominee-shaped fact is declared
  non-family.
- **P1-4 Two staleness layers were conflated.** The act log already refuses a
  stale `committed_against`; L6 as written could pass on that check alone.
  Repaired: L6 fixes the client at the current revision; question 1 lists the
  refused non-current targets.
- **P1-5 The admission-reader disagreement is load-bearing, and wider than
  stated.** The retraction target rule is itself an admission-time currency
  read, and `_current_value_for_fact` ignores migration retirement as well as
  entity supersession. Repaired: behavior-to-verify bullets.
- **P1-6 Reassertion identity.** Duplicate finding ids are already refused;
  the contract must make revival-by-id-reuse a tested negative and name the
  composed displacement reasons. Repaired: question 10; L4.
- **P1-7 "May rely upon" overclaimed.** Currency is not authorization
  (ADR-0069) or evidentiary standing. Repaired: product model item 3.
- **P1-8 Evidence composition is already committed.** Evidence withdrawal is
  not a currency root. Repaired: product model item 7; L12 made exact.
- **P1-9 Proposition existence is lattice-derived.** A per-(report, owner)
  fact exists for every current report × owner entity pair, unanswered; an
  entity *replacement* individuates a new fact id, so reassertion after L8
  answers a different proposition. This is evidence for the plan's claim that
  entity succession loses the structural link, and it obliges P2 to fix the
  synthetic fact's identity keys and entity kinds before L5/L8 are executable.
- **P1-10 H2 is structurally constrained.** Recorded under the hypothesis; P2
  confirms against the compose-over projection.
- **P1-11 Non-goal contradicted the honest rule.** "Not all actors may
  retract" implied an identity rule. Repaired: non-goal restated.
- **P1-12 Root, not edge.** Stop condition 4's "new displacement edge" does
  not catch a fifth named root. Repaired: non-goal names the distinction.
- **P1-13 Publication shape lead.** `_payload_schema_id` resolves unknown
  kinds to `act-<kind>.v1`, and kernel projection is gated by
  `KERNEL_ACT_KINDS`. An assertion successor carrying a retract mode would
  make one act kind mean two things; the authorization-end precedent chose a
  dedicated act. Lead only; question 7 stays open for P2 payload
  instantiation.
- **P1-14 Attribution locus.** No read model maps finding id → act. Repaired:
  question 8 names act-log lookup; L1 restated.
- **P1-15 Withdrawn-set monotonicity** is confirmed at
  `_withdraw_member_fact` (set union); P2 reproduces it executably.

No finding changed the selected product model's seven distinctions. No
finding requires an owner decision; the identity tell in P1-1 is now a stop
condition rather than an open choice.

### Gate P2 — artifact and consumer map — **COMPLETE, absorbed 2026-09-05**

Every behavior-to-verify claim was executed against the committed kernel by a
probe over the real projection: fifteen observations, synthetic ids only. Its
conclusions are recorded below and are superseded as a map by the unified
current-standing path the milestone shipped.

**Reproduced behavior** (observation tags are the probe's):

- O1: a per-(report, owner) fact exists for every current report × owner pair
  and is open with no assertion; no negative claim (L0).
- O2: correction is last-inserted-wins in both `compute_currency` and
  `_current_value_for_fact`; they agree (L2).
- O3: retiring the owner entity displaces the finding by `individuation` in
  `compute_currency`, removes the fact from the read-model lattice, and leaves
  Kim untouched, while `_current_value_for_fact` and
  `_current_values_for_fact_type` still return `250`. **Disagree.**
- O4: replacing the entity projects a new fact id for the successor; the old
  fact leaves the lattice. Reassertion after replacement answers a different
  proposition.
- O5: migration retirement displaces by `supersession` in `compute_currency`;
  `_current_value_for_fact` still returns the value. **Disagree.**
- O6a: same-member value correction by plain assertion is admitted and does
  not advance the horizon. O6b: member removal leaves both readers agreeing
  on no current value; `withdrawn_fact_ids` grows. O6c: re-adding the
  withdrawn fact by member-transition is admitted, and the new finding is
  displaced by the `withdrawal` root, because the root is keyed by fact id
  and the set is monotonic. O6d: plain assertion on a withdrawn member fact
  is refused (ADR-0023).
- O7: reusing a recorded finding id is refused. O8: the act log refuses a
  `committed_against` that is not the revision. O8a: the act log refuses a
  `bundle.v3` adoption, because `_payload_schema_id` maps only `bundle.v2`
  to its successor act schema.
- O9: under `locked`, a second answer is refused; `already_answered` reads
  history.
- O10: evidence withdrawal leaves the citing finding current, marks the
  evidence `withdrawn` in the read model, and displaces the evidence only.
- O11: a finding carries no actor; the envelope does; the read-model history
  entry exposes neither actor nor time.

**Current-standing readers and writers.** Writers that change a finding's
standing today: `assertion` (correction), `member-transition` remove and
reclassify, `entity-superseded`, `migration-adoption`. `evidence-replaced`
changes evidence standing only. Readers:

| Reader | Where | Resolves "current" as | Entity supersession | Migration | Withdrawal | Sees a kernel retraction root without change |
| --- | --- | --- | --- | --- | --- | --- |
| `compute_currency` | `kernel/currency.py` | roots + declared-edge closure | yes | yes | yes | yes, by construction |
| `build_read_model` (`current`, `history_by_fact`, `open_fact_ids`), `inspect_workspace` | `kernel/read_models.py`, `kernel/runners/` | `compute_currency` | yes | yes | yes | yes |
| `_current_value_for_fact`, `_current_values_for_fact_type`: closed-on-attestation gate, subset, companion presence, companion equality, declaration-signal contradiction | `kernel/findings.py` | last-inserted minus withdrawn | **no** (O3) | **no** (O5) | yes | **no** |
| `already_answered` (supersession policy) | `kernel/findings.py` | any finding in history | n/a | n/a | n/a | n/a: a retracted fact stays "answered" |
| `fact_is_member` / `is_member` (ADR-0023 routing) | `kernel/findings.py` | history minus withdrawn | n/a | n/a | yes | n/a: a retracted member still routes as member |
| `_present_successor_claims`, `_refuse_unresolved_nonzero_claims` | `kernel/findings.py` | last-inserted minus withdrawn | — | — | yes | **no** |
| `marshal_run_context` inputs and collect sources; `marshal_closure_authority` | `derivation/marshal.py` | `currency.current_finding_ids` | yes | yes | yes | yes |
| `compute_derivation_currency` | `derivation/projection.py` | kernel displaced set as roots | yes | yes | yes | yes |
| entry-loop current W-2 finding | `derivation/entry_loop.py` | `currency.current_finding_ids` | yes | yes | yes | yes |
| `validate_projected_source_boundary` | `tax/ssa_benefits.py` via `derivation/live.py` | last-inserted minus withdrawn | **no** | **no** | yes | **no** |
| untranslated-finding coverage | `tax/coverage.py` | last-inserted minus withdrawn | **no** | **no** | yes | **no** |
| `explain`, `walk_npe` | `derivation/explanation.py` | never reads currency; walks pins | — | — | — | agreement reaches it only through derivation-currency reasons |
| authorization fold | `derivation/authorization.py` | ignores every act kind it does not own (ADR-0069 D2, D6) | subject entity only | — | — | ignores by construction; needs a regression, not a change |
| `production_resolver` | `derivation/production_resolver.py` | compares envelope `actor` for adoption acts only | — | — | — | no finding reader consults actor (closes P1-1) |

**Findings**, each repaired in place above or carried into the Track 0
charter:

- **P2-1 The admission disagreement is one class, seven sites.** A retraction
  root added to `compute_currency` alone would leave five kernel enforcers and
  two out-of-kernel copies of the last-inserted rule reading a retracted
  answer as current, the same class O3 and O5 show for entity and migration
  displacement. The single authoritative current-standing path is therefore a
  requirement of L11, not a refinement. Question 6 names the shape.
- **P2-2 The family control is disqualified on evidence.** The withdrawal
  root is keyed by fact id and monotonic (O6c), so retract-then-reassert on
  one proposition is unavailable to family members on current machinery.
  Question 9 resolves to refusal at admission for a current member fact,
  routing to member-transition; widening the family lifecycle is outside
  this milestone. L13 is executable on real content with
  `tax.us.2025.w2.box1-wages`.
- **P2-3 The entity control is disqualified on evidence.** Retirement
  displaces every fact keyed on the entity, not one answer (O3); replacement
  changes the proposition (O4). Its honest payload names an entity, never a
  finding, so it cannot express "this answer no longer stands" without an
  entity-death claim (stop condition 5 would fire if it were selected).
- **P2-4 History-reading predicates are correct under `free` and force the
  `locked` answer.** `already_answered` and `fact_is_member` read history, so
  a retracted fact stays answered and stays a member. Under `free` that is
  right: reassertion is a correction of a displaced finding. Under `locked`
  it would strand the fact, so retraction is refused there (question 2).
- **P2-5 L14 runs at the projection level only.** No production content
  declares a non-free policy and `bundle.v3` cannot enter the act log (O8a).
  This is an existing surface outside scope; it is recorded, not repaired.
- **P2-6 Reason attribution needs the act id.** Question 8 carries it.
- **P2-7 Explanation agreement has two concrete surfaces.** `explanation.py`
  never reads currency. Exit criterion 7's "explanation" clause is
  discharged at `DerivationCurrencyView.reasons` and
  `read_models.history_by_fact`; the verification section names them.
- **P2-8 The ordinary control is `tax.us.2025.f1098.liable-and-paid`.**
  Determinable, entity-keyed, `free`, human-attested, no family membership.
  The Track 0 charter must read its companion and subset participation
  before L11 is scripted against it.
- **P2-9 H2 is confirmed dead.** Its instantiated payload is identical to
  H1's; it differs only in locus, and `compute_derivation_currency` seeds
  from `kernel_currency.displaced_finding_ids` alone. There is no
  materially different rival to prototype.

**Instantiated candidate payload (H1).** One kernel act kind,
`finding-retracted`, payload schema `act-finding-retracted.v1`:

```json
{
  "schema": "act.v1",
  "act_id": "demo-act-011",
  "kind": "finding-retracted",
  "actor": "demo-user-a",
  "at": "2026-01-01T00:00:11Z",
  "committed_against": 11,
  "payload": { "finding_id": "f-pat-250" }
}
```

The payload names one finding id and nothing else: no fact id (derived from
the finding), no value, no reason, no replacement (a replacement is an
assertion). Admission refuses when the finding is unknown, is not current
under the full projection, answers a fact whose supersession policy would
refuse a correction, answers a fact that is currently a family member, or is
already retracted. The controls' honest payloads for the nominee-shaped case
cannot be written: `entity-superseded` must name an entity, and
`member-transition` requires a family, scope, and horizon successor that a
non-family fact does not have (`HorizonModelError` with no chain).

**Smallest executable discriminators for Track 0** (all at projection level
with `tests/support`; D4 additionally needs the combined kernel and
derivation registry and a `derived-publication` act):

- D1: after retraction, `compute_currency`, `_current_value_for_fact`,
  `validate_projected_source_boundary`, and coverage agree there is no
  current value (L11; fails today's class in P2-1 unless the shared path
  exists).
- D2: retracting the current finding of a family member is refused; a
  member-transition removal of the same fact is admitted (L13).
- D3: reassertion after retraction is current under `free` with a new
  finding id, and the retracted finding carries reasons `retraction` then
  `correction` (L4, question 10); retraction under `locked` is refused (L14).
- D4: a derived finding pinned on the retracted answer is displaced through
  `compute_derivation_currency`; a fresh derivation after reassertion is a
  new derived id (L10).
- D5: a retraction naming a non-current finding at the current revision is
  refused at admission, not at the log (L6); a retraction of an
  entity-displaced or migration-displaced finding is refused on the same
  rule.
- D6: the authorization fold's resolution is byte-identical before and after
  a retraction act (ADR-0069 D6 extended).

## Track structure

The Foreman may refine these boundaries after P1/P2. It may not collapse a
semantic decision and its substrate implementation into one unreviewed unit.

### Track 0 — discriminating lifecycle evidence

P2 left one surviving mechanism (H1) and two evidence-disqualified controls.
Track 0 therefore runs no rival prototypes. It climbs to an executable spike of
H1 on the milestone branch, exercises L0–L14 through the discriminators D1–D6
against real projection and consumer paths, produces the applicable Track 0
adversarial closure artifacts, and receives an independent review. The spike is
evidence, not the substrate: the Substrate unit adopts it, then adds the shared
current-standing path and compatibility regressions. Track 0 selects H1 only if
its product meaning and every reader in the P2 map are established.

### Contract unit — assertion-standing contract

One proposed ADR, number **0073** (the first number not on the ratified line;
owner instruction 2026-09-06). It consolidates the selected lifecycle, target,
admission gate, currency, dependency, and compatibility rules, states the
single current-standing path, and records the inherited restriction with its
real cause and named successor. Do not create within-milestone successor ADRs.
The act payload schema is already committed on this branch as Track 0 evidence
and has not reached the ratified line, so the ADR may still change its shape;
it becomes immutable at merge, not before.

### Substrate unit — lifecycle implementation

Implement the selected act admission and projection behavior, plus a single
authoritative current-standing path for affected readers. Substrate changes
under `packages/kernel/` or `packages/derivation/` require the full test suite.

### Integration unit — two forcing consumers

Exercise the lifecycle through the real act log with:

- a synthetic nominee-shaped, per-report/per-owner human assertion whose fact
  type declares `free` supersession and matches no source-family member
  predicate; and
- one existing human-authored determinable fact selected during P2, chosen so
  that at least one of L13/L14 is exercised against real content.

Prove admission invariants, read models, derivation dependency displacement,
history, and attribution. This unit does not add the production nominee fact or
tax consequence.

## What a retraction establishes

An admitted retraction means that a recorded actor ended the workspace's
current support for one identified finding. It does not establish that the
finding's original author personally withdrew their statement.

Admission never consults actor identity. The gate is the fact type's own
supersession policy (ADR-0041), so any recorded actor may end support for any
finding that policy permits, and the envelope actor is provenance only. The
plan's earlier draft asked for "unauthorized-actor negatives" and for
"unauthorized retractions" to fail; that language predates the P1 repair which
established the state gate, and is reconciled above: unauthorized means
refused by the declared policy, never refused by who is asking.

Whether ending support *should* require the original author is a genuine
product question. It is unanswered here and would require the identity concept
ADR-0041 deliberately declined to build. It is recorded as owner-held, not
resolved by this milestone.

## Owner disposition — 2026-09-06

Track 0 established the lifecycle and, in doing so, found that the rules
blocking withdrawal are not statements about the taxpayer's paperwork. They
are the engine's own capability limits written as admission checks: a
Social Security statement is admissible only if withholding is zero, a 1099-R
only if the distribution code is 7, a 1098-E only if box 2 is unchecked. The
engine refuses to record what the user reports in order to protect what it can
compute, which inverts the Product Model's instruction to preserve reported
facts and to be honest about where it is not deterministic.

The owner's disposition, given after that finding was surfaced:

1. **Capability limits are deferred to a named successor milestone**, not
   accepted as a permanent property of withdrawal. The practical harm inside
   this milestone is narrow: correction and member-transition removal cover
   what a person would actually want to do with a single box of a statement
   they still hold. The real damage — that a taxpayer holding an unsupported
   distribution code cannot record their form at all — predates this work,
   is not worsened by it, and touches content, rules, presentation, and the
   kernel together. It gets its own planning gates.
2. **Unifying current standing stays in this milestone.** It is a defect, not
   a capability limit, and one consequence is live: a production check now
   accepts a Social Security statement whose filing-status authority has been
   withdrawn. Shipping a withdrawal lifecycle whose own readers disagree about
   whether an answer stands would defeat the milestone's second stated aim.

The contract must therefore state the restriction's real cause — limits
sitting in the wrong layer, with a named successor — rather than presenting it
as a property of withdrawal itself.

## Success and stop conditions

Success is a coherent, executed assertion-standing capability, not merely a new
act that changes one set.

Stop and surface when:

1. surviving candidates assign materially different product meanings to
   retraction or reassertion;
2. the target or admission-gate choice would require knowing who is retracting
   or would change what one actor may do to another's recorded statement;
3. a candidate creates a second currentness model rather than unifying affected
   consumers;
4. a candidate requires a new displacement edge or a broader ontology decision;
5. an honest payload cannot be written without entity-death, collection-closure,
   negative-fact, or tax-consequence claims the user did not make; or
6. implementation would change existing fact-type behavior without a named
   compatibility matrix and regression corpus.

A stop produces a decision-ready boundary. It is not bypassed by declaring the
combination unsupported after the product case has demonstrated a need for it.

## Verification

Focused commands (P2): `pytest tests/test_currency.py tests/test_findings.py
tests/test_correction_authority.py tests/test_migration_supersession_root.py
tests/test_schema_registry.py tests/conformance/test_e7_2_no_third_edge.py`
for the kernel surface; `pytest tests/test_frrs_t4_w2_live_integration.py
tests/test_f1098_mortgage_interest_lifecycle.py` for the two real controls;
`pytest -m "not live"` before any handoff; `pytest` plus `python3 -m mypy` and
`python3 tools/governance_lint.py` and `python3 tools/envelope_scan.py --range
main..HEAD` before the PR. Agreement assertions (exit criterion 7) are
measured at `compute_currency`, `_current_value_for_fact`,
`validate_projected_source_boundary`, `coverage`, `marshal_run_context`,
`compute_derivation_currency.reasons`, and `read_models.history_by_fact`.

The final candidate must include:

- schema and payload validation for every new published shape;
- executable L0–L12 positive and negative cases;
- stale-target negatives, and policy-refused negatives under `locked` and
  `closed-on-attestation`. There is deliberately no unauthorized-actor
  negative: admission never consults actor identity, so no such case exists
  to write (see "What a retraction establishes" below);
- agreement assertions across read model, invariant enforcement, derivation
  input, dependency currency, and explanation;
- regression tests for entity succession, evidence withdrawal, source-family
  transitions, authorization ending, ordinary correction, and migration paths
  touched by the implementation;
- structural proof that no nominee tax symbol or externally bound return symbol
  was added or changed;
- repository mypy for typed Python changes;
- the full test suite for substrate changes;
- `git diff --check`, governance lint, envelope scan, and green CI.

## Data safety

Only synthetic `demo.*` / `demo-*` actors, entities, facts, acts, and values may
enter committed fixtures and probes. No real taxpayer data, source document,
workspace location, private result, credential, or personal identifier may be
committed.

## Exit criteria

The milestone is complete only when:

1. proposition identity, assertion-event identity, and current standing are
   distinct in the accepted contract and executable behavior;
2. assert, correct, retract, and reassert operate on one stable proposition
   without a negative or replacement value on retraction;
3. history and actor/time attribution remain recoverable for every lifecycle
   act;
4. stale retractions fail, and retractions the declared supersession policy
   forbids fail, according to that rule and no other;
5. independent propositions and actors are not coupled accidentally;
6. entity succession, evidence withdrawal, family transition, and assertion
   retraction retain distinct meanings and effects;
7. admission enforcement, read models, derivation inputs, dependency currency,
   and explanation agree about current support;
8. derived results depending on a retracted finding cease to be current and are
   not revived by a later assertion;
9. compatibility behavior is executed for every existing lifecycle surface the
   implementation changes;
10. no nominee tax consequence, return integration, or Schedule B repair has
    entered the substrate milestone; and
11. the curated candidate passes independent review and CI.

## Track 0 adversarial closure

Evidence lives in
`docs/prototypes/assertion-standing-retraction-semantics/track-0-findings.md`;
Independent review was performed against the curated candidate.

- Authority-lifecycle table: PASS — the synthetic forcing fact, the real
  control `tax.us.2025.f1098.liable-and-paid`, and the retraction act each
  carry meaning, authority scope, dependencies, and invalidating events.
  Storage identity is not treated as authority scope.
- Empty/nonempty authority matrix: PASS — exercised for the family control
  across four states; refusal 5 keeps retraction out of the family lifecycle,
  so no horizon advances and no subtotal shrinks through this act.
- Late-member lifecycle: **FAIL, and the failure is the deliverable** — the
  substituted trace `assert → derive → retract → reassert → re-derive` passes
  on every kernel and derivation surface and fails on two out-of-kernel tax
  readers, which keep supplying an answer whose authority has been withdrawn.
  `coverage.untranslated_source_findings` needs no signature change;
  `ssa_benefits.validate_projected_source_boundary` has no channel for
  retraction at all and was **fail-open** on a withdrawn filing-status
  authority. Both were measured as unrepaired **at Track 0**, which is what
  this declaration records; both were **subsequently repaired by the
  substrate unit**, which unified them onto the full projection and closed
  the fail-open case with a regression. The `FAIL` above is the Track 0
  measurement, preserved as the evidence sequence, not the shipped state.
- Neighboring capability dependency diff: PASS — six neighbours take on no new
  prerequisite. The seventh, kernel admission invariants, took one in T0-B and
  T0-C removed it by restoring the neighbour's own rule; the resulting
  narrowing is reported rather than absorbed.
- Reused-claim semantic/lifecycle equivalence: PASS — the entity and
  source-family controls were disqualified on executed observations, not
  argument: retirement displaces every fact keyed on the entity and
  replacement changes the proposition, while family withdrawal is keyed by
  fact id and monotonic, so a withdrawn proposition can never be current
  again.
- Integration surface: N-A — the spike publishes no externally bound symbol,
  and the scope forbids one.
- Known limitations affecting correctness: **owner disposition required.** No
  order of retractions reaches any of the twenty-four participants of the
  eight declared relations on committed 2026 content. Fifteen fact types are
  fenced by the sixth refusal specifically; nine of those are companion
  amounts, including Social Security benefits paid, repayment, and
  withholding. A user who should never have entered such an amount cannot
  withdraw it while the statement stands, and must instead correct it to zero,
  which asserts a different proposition. Correction and member-transition
  removal remain available and neither dissolves the result.

Set B's emptiness is exhaustively enumerated for one of the eight relations
(13,699 orderings, zero admitted) and rests on prefix-closure from twenty-four
length-1 refusals for the other seven. The independent review derived the
participants and all three sets from committed content without reading the
tests' constants and matched them exactly.

## Execution record

| Unit | Result |
| --- | --- |
| P1 — semantic and identity review | Closed 2026-09-05; fifteen findings absorbed |
| P2 — artifact and consumer map | Closed 2026-09-05; executable probe, reader map, both controls disqualified |
| Track 0 — discriminating evidence | Closed 2026-09-06; T0-A act and refusals, T0-B reader agreement and measured disagreements, T0-C the sixth refusal and the ordered-path answer; two independent reviews, findings repaired |
| Contract unit | ADR-0073 accepted |
| Substrate unit | One current-standing path; both tax readers unified; fail-open closed; compatibility matrix committed before the behaviour change; cost measured, not cached |
| Integration unit | Lifecycle proven through the real act log against two forcing consumers; replay equals fold; attribution by act-log lookup |
| Migration repair | `_present_successor_claims` selects through the authoritative projection; the nonzero block is stated over the same projection so withdrawal and retraction are one predicate; five regressions, and a mutation check confirming the block is load-bearing |
| Final independent review | Performed against the curated candidate; an earlier review of a pre-closeout commit did not cover the closed candidate and did not reach the migration reader |

Deferred, with cause recorded: relocating capability limits out of the
admission layer (owner disposition 2026-09-06), and the constant-factor cost of
the unified read, whose named follow-on was deliberately not built because a
cache would reintroduce a second definition of current standing.

## Handoff to nominee allocation

Nominee Allocation Assertion Recording resumes only after this milestone
establishes one of the following:

- an accepted, executable lifecycle contract that satisfies L0–L12; or
- an explicit negative result showing that the selected stable-proposition model
  requires a larger owner decision.

The resumed milestone consumes the assertion-standing capability rather than
recreating lifecycle through allocation entities or source-family horizons.
T0-F5 remains a separate gate on the later Schedule B integration and is not
repaired here.
