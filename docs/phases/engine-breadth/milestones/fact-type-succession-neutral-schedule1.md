<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "fact-type-succession-neutral-schedule1",
  "milestone_state": "track-0",
  "status": "CHARTERED, NOT YET BUILT. Milestone 2 of the owner-approved two-milestone Form 1098-E prerequisite. Milestone 1 (ssa-no-activity-applicability) closed 2026-08-14 (PR #173). This document charters Track 0 only: settle the fact-type succession design on paper (rival prototypes only if the paper rung leaves more than one viable lifecycle shape) before any implementation. Predecessor population verified directly against origin/main at 05ddd777: thirteen tax.us.2025.ss-benefits-scope fact types (v1, bundle.v2, all keyed on a single {tax-year: 2025} literal, contributed, no derivation pins) are the shared Schedule 1 absence declarations. tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit is explicitly NOT part of that population -- Milestone 1 found it a source-existence proposition, a separate fourteenth migration candidate, and this document must disposition it on its own terms, not by analogy to the thirteen. Do not implement Form 1098-E, Schedule 1 line 21, Form 1040 line 10, or AGI lines 11a/11b in this milestone -- those are Part 3, immediately after this milestone closes. Stop for an Advisor/owner decision if the design turns on docs/governance/ontology.md rather than composing its existing mechanisms.",
  "current_role": "Foreman (present the Track 0 charter for owner-launch; no dispatch without literal authorization)",
  "current_prompt": "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Track 0 charter — seven settlement questions",
  "scope": [
    "identify the exact predecessor population and disposition no-rrb-or-foreign-social-benefit separately",
    "determine what a successor changes: identity, applicability, authority, lifecycle, or representation",
    "determine the fate of every predecessor state: unanswered, yes, no, corrected/superseded, upgraded workspace, fresh workspace",
    "identify the declared derivation or individuation edge that displaces predecessor state -- reject filtering or adoption-selection without a declared edge",
    "determine whether a new schema or migration citizen, and an ADR, are required",
    "define the exact integration surface Part 3 will consume"
  ],
  "non_goals": [
    "Form 1098-E of any kind",
    "Schedule 1 line 21, Form 1040 line 10, or AGI lines 11a/11b",
    "any change to no-rrb-or-foreign-social-benefit's own standing (Milestone 1 recorded, did not act)",
    "repository-wide fact migration or general historical-return migration",
    "reading, quoting, staging, or committing any tax-instruction PDF",
    "implementation ahead of paper-rung Track 0 settlement of all seven questions"
  ],
  "deep_reads": {
    "paper": [
      "docs/roles/builder.md",
      "docs/governance/ontology.md#§2 — Claims, facts, findings",
      "docs/governance/ontology.md#§5 — Derivation machinery",
      "docs/governance/ontology.md#§7 — Supersession and lifecycle",
      "docs/adr/0025-expression-language-extensions.md#7. ADR-0024's interim numeric codes migrate by governed successor claim.",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#T0-1 — authority sufficiency. Verdict: 33 → 1",
      "docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md",
      "packages/content/tax/2025/ss-benefits-scope.bundle.json",
      "packages/schemas/kernel/fact-type.v2.schema.json",
      "packages/schemas/kernel/fact-type.v3.schema.json",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Track 0 charter — seven settlement questions",
      "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Required evidence",
      "docs/process/concurrent-work.md",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Objective",
      "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Required evidence",
      "docs/phases/engine-breadth/milestones/fact-type-succession-neutral-schedule1.md#Stop conditions",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone — Fact-type succession with neutral Schedule 1 vocabulary

**Milestone key:** `fact-type-succession-neutral-schedule1`
**Primary branch:** `milestone/fact-type-succession-neutral-schedule1`
**Base:** `origin/main` at `05ddd777` (includes PR #173, the merged SSA
no-activity applicability repair).
**State:** Track 0 chartered, not yet built. Milestone 2 of the two-milestone
Form 1098-E prerequisite. **Does not share a PR with Milestone 1 and did not
wait on Milestone 1's own review cycle beyond Milestone 1 actually merging.**

## Objective

Make the shared Schedule 1 absence declarations safe to evolve before
introducing actual Schedule 1 activity. Today these facts are literal-keyed
2025 facts instantiated by package adoption, with no declared lifecycle
relationship to any successor fact type. Adding Form 1098-E must not:

- leave old absence answers silently standing once a successor exists;
- require users to repeat irrelevant answers; or
- introduce an undeclared third displacement mechanism beside the two edges
  `docs/governance/ontology.md` §7 recognizes (derivation edges,
  individuation edges).

This is **bounded substrate work**. It does not implement Form 1098-E,
Schedule 1 line 21, Form 1040 line 10, or AGI lines 11a/11b. Those are **Part
3**, chartered immediately after this milestone closes.

## The predecessor population — verified against current `main`

Re-derived directly from `packages/content/tax/2025/ss-benefits-scope.bundle.json`
at this base, not copied from the closed PR #172 split record. The bundle
carries **23** `fact-type.v2` members, all `bundle.v2` `v1`, every one keyed
on a single identity key `{kind: literal, name: tax-year, values: ["2025"]}`
with no entity citizen in any key, `nature: determinable`, domain `{yes, no}`
with no default, `supersession.policy: free`, and titled "Social Security
Benefits Worksheet completeness component … for the bounded Social Security
worksheet claim."

**Thirteen of the twenty-three are the shared Schedule 1 absence population**
this milestone governs — declarations about Schedule 1 Part II (adjustments
to income) lines that are genuinely about Schedule 1, not about the SSA
worksheet itself, and are the ones a future Schedule 1 contributor (Form
1098-E's Schedule 1 line 21 among them) must be able to supersede:

| # | Fact type id |
| --- | --- |
| 1 | `no-schedule1-line24z-writein` |
| 2 | `no-sch1-line11-educator` |
| 3 | `no-sch1-line12-business-expenses` |
| 4 | `no-sch1-line13-hsa` |
| 5 | `no-sch1-line14-moving` |
| 6 | `no-sch1-line15-deductible-se` |
| 7 | `no-sch1-line16-se-retirement` |
| 8 | `no-sch1-line17-se-health` |
| 9 | `no-sch1-line18-penalty` |
| 10 | `no-sch1-line19-alimony-paid` |
| 11 | `no-sch1-line20-ira-deduction` |
| 12 | `no-sch1-line23-archer-msa` |
| 13 | `no-sch1-line25-other-adjustments` |

All thirteen are `tax.us.2025.ss-benefits-scope.<id>` `v1`. This table is the
milestone's own predecessor population; it is not inherited by reference from
the split record, though it agrees with that record's inventory.

### `no-rrb-or-foreign-social-benefit` — dispositioned separately, not by analogy

`tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit` is one of the
same 23 members, same shape, same title pattern. Milestone 1's Track 0 (T0-1,
answered 33 → 1) found it **load-bearing** and **retained** it on both routes
of the SSA no-activity contract, because its proposition is source-existence —
whether an RRB-1099, SSA-1042S, or foreign social-benefit statement exists at
all — not worksheet-internal completeness, and the closure claim it sits
beside explicitly disclaims exactly that class. It is recorded there as a
**fourteenth** migration candidate, but its meaning is not the thirteen's
meaning: the thirteen are genuinely worksheet-only absences whose truth is
irrelevant once `line6a = 0` (proved in Milestone 1's T0-1), while this one
answers a question that exists independent of the worksheet or of Schedule 1
at all. Track 0 here must decide its succession fate on its own terms —
whether it belongs to this migration mechanism, a different one, or none —
and must not fold it into the thirteen, or exclude it from consideration,
merely because it shares a bundle and a title pattern with them.

## Inherited Track 0 input (re-verified, not re-authored)

The closed PR #172 split record is **historical input, not authority and not
a plan to merge.** The items below are carried forward because Track 0
re-verified them against this base; where the split record's prose and this
base disagree, this base governs.

- **`fact-type.v3` is allocated, unused by any content citizen at this base,
  and declares no succession field.** No migration schema family exists
  under `packages/schemas/` at this base.
- **The consequence, from `docs/governance/ontology.md` §2 and §7.** The
  thirteen are contributed, literal-keyed facts: they "arrive with the
  territory, instantiated when a body of fact types is adopted," not
  individuated by a keyed-on citizen. They carry no derivation pins (nothing
  is derived to produce them) and no individuation edge reaches them (they
  are keyed on a literal, not a citizen). Under §7's two recognized edges —
  derivation and individuation — **nothing currently reaches them.** That
  undeclared dependency is the whole of this milestone's problem.
- **Mechanism inventory to re-test on paper, not presume:**
  - Declared migration artifact / adopted-succession citizen (§5) — live
    candidate. §5: "where a version change alters identity itself … migration
    may instantiate successor *facts*, not just findings."
  - Adoption-level fact-type replacement, where superseding the *adoption*
    citizen is the individuation root for the facts it instantiated — a
    hypothesis to test, not an accepted design.
  - New neutral facts with the predecessors left dormant — rejected in the
    split record's Track 0 reasoning (leaves obsolete questions current
    indefinitely); re-test that reasoning against this milestone's own
    evidence rather than importing the conclusion unexamined.
  - Same-identifier redeclaration — rejected in the split record's Track 0
    reasoning (broadens the meaning of existing findings); same instruction.
- **Governance reading to re-verify, not presume:** superseding an adoption
  *may* authorize the transition, but adoption currency *may not* become an
  undeclared third displacement channel. The selected design must expose the
  predecessor fact type or its adoption as an explicit individuation root for
  predecessor facts, or map every displacement through one of §7's two
  recognized edges. **Reject any design that merely filters a runtime
  dictionary or relies on current package selection without declaring the
  lifecycle relationship** — this is the owner's explicit rejection rule for
  this milestone, restated here as binding.

## Track 0 charter — seven settlement questions

Track 0 must settle each of these explicitly, in writing, against verified
committed artifacts — no tax-instruction PDF is opened. If settling a
question turns on interpreting `docs/governance/ontology.md` itself rather
than composing its existing mechanisms, **stop for an Advisor/owner
decision**; do not resolve an Ontology-level ambiguity by fiat.

1. **The exact predecessor population.** Confirm or correct the
   thirteen-member table above, individually, against the committed bundle.
2. **`no-rrb-or-foreign-social-benefit`, dispositioned separately.** Decide
   its succession fate on its own terms — not by analogy to the thirteen,
   and not by silently doing nothing merely because Milestone 1 deferred it.
3. **What a successor changes.** For the selected mechanism: does it change
   the predecessor's *identity* (a new fact type), its *applicability* (when
   it is asked), its *authority* (whose findings are current), its
   *lifecycle* (how it is displaced), or merely its *representation*
   (title/wording with no semantic change)? Name which, and why the others
   are not also true.
4. **The fate of every predecessor state.** For each row below, state the
   exact outcome under the selected mechanism:
   - fact instantiated but unanswered (open);
   - current "yes" finding;
   - current "no" finding;
   - corrected or superseded finding;
   - workspace created under the old package and later upgraded to a
     package containing the successor;
   - fresh workspace created directly under the successor package.
5. **The displacing edge.** Name the exact declared derivation or
   individuation edge (§7) through which predecessor state ceases to govern.
   **Reject any design that merely filters a runtime dictionary or relies on
   current package selection without declaring the lifecycle relationship.**
6. **Schema and migration citizenship.** Decide whether a new schema family
   or migration citizen is required. **Presume an ADR is required** if the
   selected design establishes reusable fact-succession semantics — §5 admits
   migration in principle but this milestone would be the first migration
   schema family, artifact shape, adoption semantics, fact-lattice
   transition, and kernel execution contract future work is written against;
   such an ADR narrows and instantiates the Ontology, it does not amend it.
7. **The Part 3 integration surface.** Define exactly what a Form 1098-E
   contribution must do to replace the relevant absence proposition (the
   Schedule 1 line-21/adjustments-side member(s) among the thirteen) without
   disturbing unrelated SSA worksheet behavior — the remaining twelve members,
   the retained fourteenth (`no-rrb-or-foreign-social-benefit`), and the
   shipped Milestone 1 contract must all be unaffected.

### Rival prototypes

If, after the paper rung, **more than one lifecycle shape remains viable**,
charter rival prototypes — one Builder per design, never one Builder
designing both. Do not implement against an unresolved governance
interpretation; a design that turns on the Ontology is a stop condition
(above), not a prototype question.

## Required evidence

- A complete predecessor-to-successor **state matrix** covering every row in
  question 4.
- **Correction, replay, and package-upgrade behavior**, demonstrated, not
  merely asserted.
- **Proof that no old finding remains silently authoritative** once a
  successor exists.
- **Proof that unrelated SSA worksheet results remain unchanged** — the
  Milestone 1 contract, the retained fourteenth declaration, and the twelve
  Schedule-1 members not touched by the Part 3 integration fixture.
- **Proof that a no-Schedule-1 return is not asked additional questions** —
  the whole point of the succession is fewer irrelevant questions, not more.
- **Exact package/version admission and migration checks** — what a package
  must declare to admit the migration, and what rejects a malformed one.
- **Negative tests** that fail if the implementation falls back to package
  filtering or another undeclared lifecycle mechanism.
- An **integration fixture** showing Part 3 can introduce one real Schedule 1
  item (a stand-in for Form 1098-E's Schedule 1 line-21 contribution) without
  reviving the old contradiction the succession exists to prevent.

## ADR posture

Presumed owed if the selected design establishes reusable fact-succession
semantics (question 6). No governance version change is presently indicated.
Stop for advisor consultation if the paper design cannot express displacement
through a derivation or individuation edge, or would require broadening §7's
definition of either edge.

## Stop conditions

- **The Ontology-turn stop.** If settling any of the seven questions turns on
  interpreting `docs/governance/ontology.md` itself — rather than composing
  its existing derivation and individuation edges — stop for an
  Advisor/owner decision. Do not resolve an Ontology-level ambiguity by
  fiat, and do not implement against an unresolved governance
  interpretation.
- **The edge-declaration stop.** If the best available design displaces
  predecessor state without naming a specific derivation or individuation
  edge — i.e., it filters a runtime dictionary or relies on current package
  selection instead — stop. That is the owner's explicit rejection rule
  (question 5), not a style preference.
- **The single-Builder stop.** If more than one lifecycle shape survives the
  paper rung, stop and charter rival prototypes, one Builder per design.
  Do not let one Builder design both alternatives.
- **The scope-creep stop.** If closing this milestone appears to require
  Form 1098-E, Schedule 1 line 21, Form 1040 line 10, or AGI lines 11a/11b,
  or repository-wide/historical-return fact migration, stop — that scope
  belongs to Part 3 or is explicitly out of bounds, not an extension of
  Track 0.

## Exit criteria

The milestone is complete when the successor population and its lifecycle are
**versioned, executable, independently reviewed, and safe for both upgraded
and fresh synthetic workspaces.** Do not broaden into repository-wide fact
migration or general historical-return migration.

## Standing constraints

No seat reads tax-instruction PDFs. Do not widen `audit_collect_authority`
(durable deferral from Milestone 1, deliberately left open). Do not broaden
`presentation_projection._one_row`. This milestone does not touch
`no-rrb-or-foreign-social-benefit`'s Milestone-1 standing except to
disposition its succession fate (question 2); it does not re-litigate whether
it is load-bearing for the SSA no-activity zero.

## Next milestone after this one

The fresh Form 1098-E vertical-slice milestone — Schedule 1 lines 21/26,
Form 1040 line 10, and AGI lines 11a/11b — is chartered only after this
milestone closes, on its own branch and PR.

## Track 0 findings

Paper only. Every claim below is verified against committed artifacts at
`f5e9887e483e06a583decdef307974bda736b257` (the Track 0 start commit on
this branch, whose parent line is `origin/main` at `05ddd777`); no
tax-instruction PDF was opened.
Where a claim is established by reading committed code or schemas, the
read was against those blobs and left nothing in the repository except
this section. The closed PR #172 split record is treated as historical
input to re-test, not as a conclusion.

**Single lifecycle shape survives.** Declared migration artifact;
predecessor fact types are the individuation roots; human findings
migrate by presented successor claim (ADR-0025 decision 7), not by
silent conversion. Rival prototypes are not indicated. The
Ontology-turn stop does not fire: displacement is composed from §5's
migration artifact, §7's named succession shape, §7's individuation
edge as the charter already offered it ("expose the predecessor fact
type … as an explicit individuation root"), and the kernel's existing
root-contributor pattern (correction, withdrawal, entity-supersession).
The residual composition note is under question 5; it does not reopen
a second shape.

### T0-1 — predecessor population. Verdict: the thirteen-member table stands

Re-read `packages/content/tax/2025/ss-benefits-scope.bundle.json` at this
base. The citizen is `bundle.v2` `tax.us.2025.ss-benefits-scope.vocabulary`
`v1` with **23** nested `fact-type.v2` members. Every member is `v1`,
`nature: determinable`, `supersession.policy: free`, domain
`{"type": "string", "enum": ["yes", "no"]}` with no default, and a
single identity key `{kind: literal, name: tax-year, values: ["2025"]}`.
No member has derivation pins, an entity key, `optional_default`, or a
succession field.

The charter's thirteen ids are present, individually, and are the only
members whose titles name a Schedule 1 Part II line:

| # | Fact type id | Bundle order |
| --- | --- | --- |
| 1 | `tax.us.2025.ss-benefits-scope.no-schedule1-line24z-writein` | 9 |
| 2 | `tax.us.2025.ss-benefits-scope.no-sch1-line11-educator` | 10 |
| 3 | `tax.us.2025.ss-benefits-scope.no-sch1-line12-business-expenses` | 11 |
| 4 | `tax.us.2025.ss-benefits-scope.no-sch1-line13-hsa` | 12 |
| 5 | `tax.us.2025.ss-benefits-scope.no-sch1-line14-moving` | 13 |
| 6 | `tax.us.2025.ss-benefits-scope.no-sch1-line15-deductible-se` | 14 |
| 7 | `tax.us.2025.ss-benefits-scope.no-sch1-line16-se-retirement` | 15 |
| 8 | `tax.us.2025.ss-benefits-scope.no-sch1-line17-se-health` | 16 |
| 9 | `tax.us.2025.ss-benefits-scope.no-sch1-line18-penalty` | 17 |
| 10 | `tax.us.2025.ss-benefits-scope.no-sch1-line19-alimony-paid` | 18 |
| 11 | `tax.us.2025.ss-benefits-scope.no-sch1-line20-ira-deduction` | 19 |
| 12 | `tax.us.2025.ss-benefits-scope.no-sch1-line23-archer-msa` | 20 |
| 13 | `tax.us.2025.ss-benefits-scope.no-sch1-line25-other-adjustments` | 21 |

**No Schedule 1 line 21 member exists.** Student-loan interest is not
among the twenty-three. The thirteen are lines 11–20, 23, 24z, and 25.
That absence is a population fact, not a defect in the table: Part 3
will *add* a line-21 citizen to the successor vocabulary, not replace
one of these thirteen (question 7).

The other ten members are not this milestone's predecessor population.
Nine are worksheet-internal non-Schedule-1 exclusions (Form 1040 lines,
Form 2555/4563/8815, adoption benefits, Puerto Rico/Samoa income,
lump-sum election). The tenth is `no-rrb-or-foreign-social-benefit`
(question 2). They share the bundle and the title pattern; they do not
share the Schedule 1 proposition.

Each of the thirteen is titled "Social Security Benefits Worksheet
completeness component … for the bounded worksheet claim" (line 24z:
"that must be figured before the Social Security Benefits Worksheet").
`yes` asserts the named excluded class is absent; `no` asserts it is
present and blocks. Milestone 1 already proved they are worksheet-only
in the strict sense (T0-1, 33 → 1): they sit in
`rule.ss-benefits-worksheet` v2's `conditional_dependency_set`, gated
on `count(box5-net-benefits) > 0`, and are not in the eleven
unconditional `requires`.

### T0-2 — `no-rrb-or-foreign-social-benefit`. Verdict: not this migration

Disposition, on this declaration's own proposition, not by analogy and
not by silence:

- **Proposition** (title, and Milestone 1 T0-1): source-existence —
  whether an RRB-1099, SSA-1042S, or foreign social-benefit statement
  exists at all. It is not a Schedule 1 line, not an adjustments-side
  absence, and not worksheet-internal completeness.
- **Standing** (shipped, not re-litigated): load-bearing for the
  no-activity zero. `rule.ss-benefits-worksheet` v2 carries it in
  unconditional `requires` and in a `categorical_compare == yes` guard
  conjunct on *both* routes. The closure claim disclaims exactly this
  class. Folding it into a Schedule 1 succession would either displace
  a premise of the shipped zero or retarget that premise onto a
  Schedule 1 identity it does not have.
- **This mechanism does not apply.** The surviving shape succeeds
  Schedule 1 absence *identity* (worksheet-scoped question →
  Schedule-1-native question). Source-existence is a different
  question. A future RRB / SSA-1042S / foreign source-family
  milestone, if one is chartered, is the right succession — if any.
- **Fate in this milestone: none.** Retain
  `tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit` `v1`
  under its existing id. Do not retitle, re-key, re-home, or include it
  in the migration's predecessor list. Do not treat "not in the
  thirteen" as permission to ignore it: it was considered, and it is
  excluded *because its proposition is not a Schedule 1 absence*.

### T0-3 — what a successor changes. Verdict: identity and lifecycle

The selected mechanism changes two things. The others are either
already settled elsewhere, follow as consequences, or are rejected.

**Identity — yes, and this is half of the change.** A successor is a
new fact type (new id), not a new version of the predecessor id.
Committed identity is `fact_type_id|key=value`
(`packages/kernel/facts.py` `_fact_id`). Version is not in the fact
id. `apply_bundle_adoption` stores types in a dict keyed on `id` and
overwrites on re-adoption; it never removes an id that the new bundle
omits. Therefore:

- a `v2` of `tax.us.2025.ss-benefits-scope.no-sch1-line11-educator`
  is the same fact as `v1` (`…educator|tax-year=2025`); existing
  findings stay attached to a declaration whose meaning would have
  broadened;
- omitting the thirteen from a successor
  `ss-benefits-scope.vocabulary` bundle leaves them current — they
  remain in `state.fact_types`.

The retrospective's closeout lesson is the same fact, measured: "A
version bump is not fact-type succession." Same-identifier
redeclaration is rejected on this identity rule, not on imported PR
#172 prose. The successor population is thirteen new Schedule-1-native
fact type ids (Track 1 names them), same `{yes, no}` domain and
literal `tax-year: 2025` key, whose proposition is the Schedule 1
line's absence *as a Schedule 1 question*, not as an SSA-worksheet
completeness component.

**Lifecycle — yes, and this is the other half.** Today nothing in
§7's two edges reaches these facts. They are contributed
(literal-keyed; `individuated_by` is empty). Currency's displacement
roots are corrections, member withdrawals, and superseded entity ids
(`packages/kernel/currency.py` `compute_currency`). Declared edges are
only `derivation` (finding pins) and `individuation` (entity ids on
`Fact.individuated_by`). Package adoption is not a lattice act.
Adopting a successor without a declared retirement therefore leaves
predecessor facts and their findings current. The successor *is* the
declared retirement: a migration that supersedes the named predecessor
fact-type citizens, so those types leave current `state.fact_types`
and their findings displace along the individuation edge (question 5).

**Authority — consequence, not a separate change.** Once the
predecessor type is superseded, its findings are not current. That is
lifecycle doing what §7 says currency is: a derived property of the
record. We do not add a third "authority" channel.

**Applicability — not this milestone's change.** Milestone 1 already
moved the thirteen into a `count > 0` `conditional_dependency_set`.
That is when the worksheet *reads* them. It does not displace them as
questions, and it is not a lifecycle edge. Reusing applicability (or
package membership) as the way predecessor state "goes away" is the
question-5 rejection rule.

**Representation — no.** A title-only or wording-only change on the
same id would leave `fact_id` stable and attach old findings to a
broader question. That is the same-identifier rejection again.
Neutral Schedule 1 vocabulary is a new identity, not a rename.

ADR-0025 decision 7 is precedent only for the *finding* half (below).
It migrates human numeric-code findings onto a successor *label claim*
by user assertion. It is not a fact-lattice migration mechanism and is
not reused as one.

### T0-4 — fate of every predecessor state

Under the selected mechanism. "Migration adopted" means the successor
package's declared migration citizen has been taken up (question 6).
"Presented successor claim" is ADR-0025 decision 7 applied to these
attested `{yes, no}` findings: append-only mapping; the user asserts
the presented claim; no silent conversion of a human finding.

| Predecessor state | Outcome |
| --- | --- |
| Fact instantiated, unanswered (open) | Predecessor type leaves current lattice. No finding exists to present. Successor type is instantiated; the successor fact is open. The predecessor question is no longer asked. Whether the successor is asked is the same applicability the worksheet already has: the nonempty route's conditional set, retargeted at the successor ids. A no-Schedule-1 / SSA-empty return is not asked the successor (and is not asked the predecessor). |
| Current `yes` finding (named class absent) | Predecessor finding is displaced the moment the type is superseded — it is not silently current. History keeps it. The migration presents a successor `yes` claim citing that finding and the mapping. The user asserts the successor. Until that assertion, the successor fact is open; the old `yes` is already non-current. |
| Current `no` finding (named class present) | Same displacement. Presented successor `no` claim. A `no` here means that Schedule 1 line's class is present; it is not rewritten into an amount. Part 3's real line-21 item is a *new* type, not a conversion of any of these `no`s. |
| Corrected or superseded finding | Only the last current predecessor finding (if any) is an input to a presented claim. Earlier findings stay in history on the displaced predecessor fact. Replay of derivation does not restore predecessor currency. A later correction on the *successor* is an ordinary same-fact correction and does not revive the predecessor. |
| Workspace created under the old package, later upgraded to a package that contains the successor | Upgrade is a new package adoption whose closed fact surface includes the migration citizen and the thirteen successor types, and does not require the thirteen predecessor types to remain current. Adopting the migration retires the thirteen predecessor types, presents claims for any current predecessor findings, and leaves the other ten `ss-benefits-scope` types (including `no-rrb-or-foreign-social-benefit` v1) untouched. The Milestone 1 empty-route contract is unchanged: same eleven `requires`, same `no-rrb` conjunct, same `choose(count==0 → 0)`. The nonempty route's conditional set is retargeted at the thirteen successor ids (a worksheet-rule successor is in Track 1 scope because otherwise the nonempty route pins retired types and blocks). |
| Fresh workspace created directly under the successor package | Predecessor types never enter the lattice. No predecessor findings exist; the migration has nothing to present. Successor types are adopted. `no-rrb-or-foreign-social-benefit` v1 is still a member of `ss-benefits-scope.vocabulary`. SSA-empty publishes the canonical zero with the same M1 premises. |

**Correction, replay, and package-upgrade — specified here, demonstrated
in Track 1.** Correction after succession is a new finding on the
successor fact. Replay from the act log recomputes the same lattice
and the same currency; it does not resurrect retired types. Upgrade
runs the migration once as an adopted act, not as a runner-resident
filter of the current package dictionary.

### T0-5 — the displacing edge. Verdict: individuation, from the predecessor fact type

**Named edge.** Individuation. The predecessor fact type is the
citizen that individuates its facts. The act that supersedes that
citizen is adoption of the migration artifact. Findings answering
those facts displace along the individuation edge; consumers of those
findings then displace along existing derivation (pin) edges.
Successor facts are instantiated because their types have been
adopted. Successor findings, when they exist, are either asserted
from a presented claim or later derived by ordinary rules; they are
not a second displacement channel.

This is the charter's offered composition — "expose the predecessor
fact type … as an explicit individuation root" — not a new reading of
§7's words. It is also what the lattice already does for *existence*:
`facts_of` projects one fact per current member of `state.fact_types`
(`packages/kernel/facts.py`). Currency does not yet treat a fact type
leaving that map as an individuation root; Track 1 makes that root
explicit, the same way `entity-superseded` is already an explicit
root for entity-keyed facts. Withdrawal remains the precedent that an
act may contribute displacement *roots* without adding a third edge
kind (`currency.py` `_member_withdrawals`).

**Why the other inventory items fail the rejection rule, re-tested.**

- **Runtime dictionary filter / current package selection.** ADR-0028
  defines the package closed fact surface `F(P)` for *admission and
  binding*, not for displacing facts already in the lattice. Package
  adoption (`act-package-adoption.v1`) is not applied by
  `packages/kernel/facts.py` and is not a currency root. Hiding
  predecessor types because the current package no longer lists them
  would leave their findings current. Rejected by question 5's rule.
- **New neutral facts, predecessors left dormant.**
  `apply_bundle_adoption` only adds or overwrites by id. Adopting
  successor types without retiring predecessor types leaves both
  current. Obsolete questions remain current indefinitely. Re-tested
  and rejected on that kernel fact, not on PR #172's conclusion.
- **Same-identifier redeclaration.** Rejected under T0-3 (fact id
  ignores version; findings stay attached).
- **Adoption-level replacement of the existing bundle or package.**
  The thirteen share `ss-benefits-scope.vocabulary` v1 with ten other
  types, including the retained fourteenth. Superseding that bundle
  adoption, or the package adoption that carried it, would displace
  `no-rrb-or-foreign-social-benefit` and the nine non-Schedule-1
  declarations. That violates T0-2 and the shipped Milestone 1
  contract. Adoption *authorizes* the migration (taking it up is the
  recorded act §5 requires). Adoption currency is not itself the
  displacement channel.

**Residual composition note, not a second shape.** §7's individuation
paragraph says a fact is "keyed on" citizens. Identity keys on these
thirteen are a literal, not the fact type. Treating the fact type as
the individuation root uses the type half of committed fact identity
(`fact_type_id|…`) and the charter's own offered root; it does not
add a key kind and does not treat adoption currency as an edge. If a
later seat holds that this broadens "keyed on" rather than
instantiating it, that is the Advisor stop in the ADR posture — raise
it; do not invent a second lifecycle to dodge it.

### T0-6 — schema, migration citizen, and ADR. Verdict: new family, and an ADR

Verified at this base:

- `fact-type.v3` is published (`packages/schemas/kernel/published.json`)
  and unused by any content citizen (`"schema": "fact-type.v3"` occurs
  in no file under `packages/content`). It widens supersession-policy
  vocabulary (ADR-0041). It declares no succession field.
- No migration schema family exists under `packages/schemas/`.
- §5 already names the citizen: a **migration artifact**, sitting
  closer to adoption than to arithmetic, that may instantiate
  successor *facts* and that runs as derivation runs for the finding
  half.

**Do not put succession on `fact-type.v3`.** Succession is not a
property of a fact type's shape; it is a recorded reshaping of the
lattice. Stuffing a successor pointer into the fact-type schema would
make every future type carry unused migration fields and would still
not provide the authorizing act §5 requires.

**Required, first of their kind:**

1. A new published schema family for the migration artifact (Track 1
   picks the unused version filename; the Ontology's name is
   "migration artifact").
2. An authorizing act that takes the migration up (new act schema, or
   a declared use of an existing adoption act that *names* the
   migration citizen — Track 1 chooses; it must be a recorded user
   act, not runner policy).
3. Kernel execution: adopting the migration retires the named
   predecessor type ids from current `state.fact_types`, admits the
   successor types, contributes individuation roots for findings of
   the retired types, and presents successor claims for then-current
   predecessor findings. Ordinary saturation then cascades via
   existing derivation edges.
4. Package admission: a package that claims this succession must pin
   the migration citizen and the successor types; a package that
   still binds the nonempty worksheet to retired predecessor ids is
   malformed; a migration whose predecessor list includes
   `no-rrb-or-foreign-social-benefit`, or any id not in the T0-1
   table, is rejected. Track 1 writes the exact checks and the
   negatives that fail on package-filter fallbacks.

**ADR is required.** The charter's presumption holds. This is the
first migration schema family, the first lattice-reshape execution
contract, the first fact-type-as-individuation-root, and the first
finding-presentation contract for fact-identity succession. Future
work will be written against it. The ADR narrows and instantiates
§5 / §7; it does not amend the Ontology and does not require a
governance version change. Schema-intent ledger: append the propose
event on the standing `milestone-schema-ledger` branch *before* the
first schema file is added (concurrent-work protocol). Track 0 does
not reserve a version number.

ADR-0025 decision 7 is cited in that ADR as the bounded finding-half
precedent (presented successor claim; no silent conversion; new rules
bind successor types, not dual-read predecessors). It is not the
lattice mechanism.

### T0-7 — Part 3 integration surface

Part 3 (Form 1098-E, Schedule 1 line 21, Form 1040 line 10, AGI
11a/11b) is not built here. The surface it must consume, exactly:

1. **The thirteen successors are the Schedule 1 absence vocabulary.**
   After this milestone, a Schedule 1 line-11…20 / 23 / 24z / 25
   absence is the corresponding *successor* fact, not
   `tax.us.2025.ss-benefits-scope.no-sch1-…`. Predecessor ids are
   retired in any workspace that has taken up the migration, and are
   absent from a fresh successor-package workspace.
2. **Line 21 is an addition, not a replacement.** None of the
   thirteen is line 21. `no-sch1-line25-other-adjustments` and
   `no-schedule1-line24z-writein` are not stand-ins for student-loan
   interest. A Form 1098-E contribution introduces a *new*
   Schedule-1-native line-21 citizen in the same successor vocabulary
   and does not migrate, retarget, or assert any of the thirteen
   predecessors.
3. **What 1098-E must not do.** Instantiate or assert a predecessor
   id; revive a retired type; include `no-rrb-or-foreign-social-benefit`
   in any migration or retarget; edit the Milestone 1 empty-route
   contract (`require_closed`, `count`, the `no-rrb` conjunct, the
   `choose` zero, the eleven unconditional `requires`); displace the
   other twelve successors merely because line 21 became present.
4. **What this milestone must already have done** so that (3) is
   possible: retire the thirteen predecessors; retarget the nonempty
   worksheet conditional set at the thirteen successors; leave the
   other ten `ss-benefits-scope` members, including `no-rrb`, on
   their existing ids.
5. **Integration fixture (Track 1, stand-in only).** One synthetic
   Schedule 1 line-21 item. Expected: predecessors remain non-current
   or never-instantiated; `no-rrb` v1 and the M1 empty route
   unchanged; the twelve successors not named by the stand-in
   unchanged; a no-Schedule-1 return is not asked additional
   questions relative to M1. The stand-in is not Form 1098-E, not
   line 26, not Form 1040 line 10, and not AGI 11a/11b.

### Predecessor-to-successor state matrix

Condensed from T0-4; Track 1's suite must execute every row.

| # | Start state | Lattice | Predecessor finding | Successor fact | Asked on no-Sch1 / SSA-empty? |
| --- | --- | --- | --- | --- | --- |
| 1 | Open predecessor, then migration | Predecessor type retired; successor type current | none | open | no |
| 2 | Current predecessor `yes`, then migration | same | displaced; presented `yes` claim | open until assertion; `yes` after | no additional ask beyond the presented claim on *upgrade*; fresh successor-package workspaces have no claim to present |
| 3 | Current predecessor `no`, then migration | same | displaced; presented `no` claim | same pattern | same as row 2 |
| 4 | Corrected predecessor (last current `yes` or `no`) | same | only last current finding is presented; earlier history stays on the retired fact | same pattern | same as row 2 |
| 5 | Old-package workspace upgraded | migration act retires the thirteen; other ten types including `no-rrb` stay | per rows 1–4 | thirteen successors current | M1 empty route unchanged; no extra questions |
| 6 | Fresh successor-package workspace | predecessors never adopted | none | thirteen successors current, open | M1 empty route unchanged; successors not in the empty-route `requires` |

Track 1 also proves: after any of rows 1–6, a finding on a predecessor
id is never in `current_finding_ids`; a mutant that implements the
same visible result by filtering `F(P)` or the current package
dictionary fails a declared-edge negative; replay from the act log
reproduces the row.

### Mechanism inventory — re-test record

| Inventory item (from Inherited Track 0 input) | Re-test | Disposition |
| --- | --- | --- |
| Declared migration artifact / adopted-succession citizen (§5) | Composes §5 + §7 succession + charter's fact-type individuation root; kernel has no such family yet | **Selected** |
| Adoption-level replacement of the existing bundle/package | Shared bundle with `no-rrb` and nine other types; package adoption is not a lattice act | **Rejected** (too coarse, and would be an undeclared channel if used as a filter) |
| New neutral facts, predecessors left dormant | `apply_bundle_adoption` cannot retire omitted ids | **Rejected** |
| Same-identifier redeclaration | `fact_id` ignores version; findings stay attached | **Rejected** |

One shape remains. The single-Builder stop does not fire.

### Stop/continue recommendation

**Continue.** Charter Track 1 against this settlement. Do not open
rival prototypes. Do not implement Form 1098-E or the Form 1040 /
AGI lines. If review holds that fact-type-as-individuation-root
broadens §7 rather than instantiating the charter's offered
composition, stop for Advisor/owner *then* — that disagreement is
the named residual, not a reason to hold Track 0 open.

## Proposed Track 1 charter

Paper settlement above is binding. Track 1 builds exactly this shape
and the evidence the milestone's `## Required evidence` already lists.
It does not reopen T0-1…T0-7.

### Object

1. **ADR** instantiating this settlement: migration artifact as the
   lattice-reshape citizen; predecessor fact type as individuation
   root; presented successor claim for attested findings (ADR-0025
   decision 7 as the finding-half precedent, not as the lattice
   mechanism); package admission and rejection rules; no Ontology
   amendment.
2. **Schema-intent ledger event** on `milestone-schema-ledger` before
   any schema file is added. Then the unused versioned schema
   filename(s) for the migration artifact and, if Track 1 introduces
   one, its authorizing act. `packages.kernel.schema_registry.write_manifest`
   only; never edit a published schema or a published checksum.
3. **Thirteen successor fact types** — new ids, `fact-type.v2` (or
   whatever published fact-type schema the successors actually need;
   do not migrate them onto `fact-type.v3` merely because v3 exists),
   same domain and `tax-year: 2025` literal key, Schedule-1-native
   titles, in a Schedule 1 vocabulary bundle that is *not* a silent
   `ss-benefits-scope.vocabulary` v2. Predecessor ids are not members.
4. **One migration citizen** naming exactly the T0-1 thirteen as
   predecessors and the thirteen successors as targets, with the
   finding-half mapping (predecessor current finding → presented
   successor claim). It must not name `no-rrb-or-foreign-social-benefit`
   or the other nine `ss-benefits-scope` members.
5. **Kernel execution** of that adoption: retire named types from
   current `state.fact_types`; project successor facts; individuation
   roots for findings of retired types; derivation cascade unchanged.
6. **Worksheet retarget** — a successor of `rule.ss-benefits-worksheet`
   whose nonempty `conditional_dependency_set` names the thirteen
   *successors* and still names the other nine non-Schedule-1
   worksheet declarations. Empty-route contract is byte-for-byte the
   Milestone 1 contract except for that retarget: eleven
   `requires` including `no-rrb-or-foreign-social-benefit`,
   `require_closed`, `count`, `categorical_compare` on `no-rrb`,
   `choose(count==0 → 0)`.
7. **Publication chain** — lowest free package / published-packages /
   release / adoption-fixture versions on the ratified line at
   implementation time, additive.
8. **Synthetic fixtures and tests** covering the T0-4 matrix, the
   required-evidence list, the line-21 *stand-in* integration row, and
   negatives that fail if retirement is implemented as an `F(P)` or
   current-package filter. Named goldens enter through
   `live_coordinate_run`.

### Non-goals (unchanged)

Form 1098-E of any kind; Schedule 1 line 21 as a real form (the
stand-in is a fixture, not the form); Form 1040 line 10; AGI 11a/11b;
any change to `no-rrb-or-foreign-social-benefit`'s Milestone 1
standing; repository-wide or historical-return migration; reading a
tax-instruction PDF; widening `audit_collect_authority`; broadening
`presentation_projection._one_row`.

### Stop conditions

The milestone's four stops still bind. Additionally stop if:

- displacement cannot be expressed as the named individuation root
  plus existing derivation cascade, and would require a third edge
  kind or a runner-resident filter;
- the nonempty worksheet cannot retarget without changing the
  published empty-route zero or its `no-rrb` premise;
- review fires the residual Advisor question on "keyed on" and the
  owner has not dispositioned it.

### Exit for Track 1

The required-evidence list is the exit. Independent review of
derivation behaviour *and* of the lattice/currency edge (not only of
the worksheet value) before this milestone is offered to merge.
