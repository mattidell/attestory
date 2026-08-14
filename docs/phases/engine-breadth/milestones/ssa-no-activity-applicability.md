<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "ssa-no-activity-applicability",
  "milestone_state": "closed",
  "status": "Closed 2026-08-14 (PR #173, merged 2026-08-14 at 05ddd777). SHIPPED CONTRACT: rule.ss-benefits-worksheet v2 (rule-artifact.v4) is the SOLE producer of tax.us.2025.social-security.line6b. 11 unconditional requires = no-rrb-or-foreign-social-benefit, the seven derived numeric inputs, social-security.line6a, filing_status, rounding.convention. Guard = all[require_closed(ssa1099.benefits) BOTH routes; conditional_dependency_set of the 22 worksheet-only declarations gated on count>0; categorical_compare(no-rrb == yes) BOTH routes; any[count==0, all[22 conjuncts, MFS set]]]. Value = choose(count==0 -> 0, else -> the UNCHANGED v1 worksheet expression). Independent review returned APPROVE WITH FINDINGS (both findings closed) and CI (verify) is green on the exact merged head. T0-1 ANSWERED 33 -> 1: no-rrb-or-foreign-social-benefit is load-bearing, retained on both routes, and recorded as a FOURTEENTH migration candidate for Milestone 2, not acted on here. Publication generation: package.core-calculations.v30 / published-packages.v25 / demo.release.2025.v23 / adopt-core-v30-current. ss-benefits-scope stays at its base v1 - no vocabulary successor exists; the withdrawn ss-benefits-scope.bundle.v2 and its package_validation check-10a root cause are fully distilled into the retrospective. Coordination item for Milestone 2 is retracted: its predecessor population is ss-benefits-scope v1, as it always was on the ratified line. Full arc distilled in the retrospective, not carried here.",
  "retrospective": "docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md",
  "current_role": "Foreman (present next-milestone candidates; selection is owner-held)",
  "current_prompt": "docs/phases/engine-breadth/coverage-frontier.md",
  "scope": [
    "identify the exact source-family closure or absence authority establishing that no applicable Social Security benefits exist",
    "produce a canonical line-6b zero carrying that authority and its provenance",
    "ensure the closed-empty branch neither reads nor pins the worksheet-scope declarations",
    "preserve the nonempty worksheet route unchanged except for the mutually exclusive branch guard",
    "prove that unclosed, contradictory, and nonempty SSA states cannot take the zero route",
    "regress Form 1040 line 9 and every existing income route"
  ],
  "non_goals": [
    "neutral Schedule 1 facts and fact-type succession, which are Milestone 2",
    "retiring, deleting, or re-titling any of the 23 predecessor declarations",
    "changing the nonempty worksheet computation beyond the branch guard",
    "Form 1098-E work of any kind",
    "the schedule1-part1-scope and attachment-rule.v5 deferrals",
    "reading, quoting, staging, or committing any tax-instruction PDF"
  ],
  "deep_reads": {
    "paper": [
      "docs/roles/builder.md",
      "docs/governance/ontology.md",
      "docs/adr/0016-source-family-claim-and-composition.md",
      "docs/adr/0017-recorded-family-horizons-for-closure-freshness.md",
      "docs/adr/0038-qdcg-worksheet-and-declared-absence.md",
      "packages/content/tax/2025/family.ssa1099-benefits.json",
      "packages/content/tax/2025/closure-mapping.ssa1099-benefits.json",
      "packages/content/tax/2025/rule.ssa1099-benefits-subtotal.json",
      "packages/content/tax/2025/rule.form1040-line6a.json",
      "packages/content/tax/2025/rule.schedule-a-total-closed-empty.json",
      "packages/content/tax/2025/rule.form1040-line9.v7.json",
      "AGENTS.md#Data Safety Rules"
    ],
    "implementation": [
      "docs/roles/builder.md",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Proposed contract — Track 0 confirms, refines, or replaces",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Compatibility matrix — Track 0 must prove every row",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Verification",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Stop conditions",
      "docs/process/concurrent-work.md",
      "packages/content/tax/2025/rule.schedule-a-total-closed-empty.json",
      "AGENTS.md#Schema Publication Protocol",
      "AGENTS.md#Fixture Rules",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/roles/reviewer.md",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Objective",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Compatibility matrix — Track 0 must prove every row",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Verification",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Exit criteria",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Stop conditions",
      "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Track 0 adversarial closure",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Milestone — SSA no-activity applicability repair

**Milestone key:** `ssa-no-activity-applicability`
**Primary branch:** `milestone/ssa-no-activity-applicability-repair`
**Base:** the current ratified line (`origin/main`), including PR #175's
integration-surface gate.
**State:** **Closed 2026-08-14** (PR #173, merged at `05ddd777`). Track 0
complete (paper) and dispositioned. Track 1's first attempt — the chartered
two-producer contract — **stopped**: it is not implementable at the
presentation boundary, because `tax.us.2025.social-security.line6b` is
form-field-bound, and a form-field-bound symbol admits exactly one
disposition row while a two-producer split always yields two. See `## Track
1 stop report`. Track 1 was then rechartered around a single-producer
contract, built, independently reviewed (APPROVE WITH FINDINGS, both closed),
and shipped as `rule.ss-benefits-worksheet` v2 (`## Track 0 settlement —
final contract`), CI-green on the exact merged head. Retrospective:
`docs/milestone-retrospectives/2026-08-14-ssa-no-activity-applicability.md`.

Milestone 1 of the two-milestone split recorded in
`fact-type-succession-ssa-applicability.md`. Milestone 2 (fact-type succession
with the thirteen neutral Schedule 1 propositions) is now chartered on its own
branch and PR as `fact-type-succession-neutral-schedule1`. **This milestone
did not share a PR with Milestone 2 and did not wait on its prototype and ADR
cycle.**

## Objective

> A return with no applicable Social Security source publishes the legally
> authorized line-6 zero and can proceed through line 9 without satisfying
> worksheet-only scope declarations.

## Current state — verified at this base

| Artifact | Fact |
| --- | --- |
| `family.ssa1099-benefits.json` | `source-family.v1`, `v1`. `member_predicate.fact_type` = `tax.us.2025.ssa1099.box5-net-benefits`; `authorizes_subtotal` = `tax.us.2025.ssa1099.benefits.box5-subtotal` |
| `closure-mapping.ssa1099-benefits.json` | `source-closure-mapping.v2`, `v1`. Closure fact type `tax.us.2025.ssa1099.source-closure` `v1`, horizon key `family-horizon`, admission `current-literal-true` |
| `rule.ssa1099-benefits-subtotal.json` | `when: true`, `requires: [rounding.convention]`. Value is `round(add(collect(box5-net-benefits over the family)))` |
| `rule.form1040-line6a.json` | `when: true`, `requires: [box5-subtotal]`, value is a bare `ref`. Publishes `tax.us.2025.social-security.line6a` |
| `rule.ss-benefits-worksheet.json` | `rule-artifact.v3`, `v1`. **The only producer of `tax.us.2025.social-security.line6b` corpus-wide.** Carries **33** `requires` — the 23 `ss-benefits-scope` declarations plus ten income/convention symbols |
| `rule.form1040-line9.v7.json` | `when: true`, requires `tax.us.2025.social-security.line6b` **unconditionally** |

**The defect.** Line 6a already behaves correctly on an empty family: the
subtotal collects zero members and line 6a is a bare `ref`. Line 6b does not —
its only producer demands all 33 dependencies regardless of whether any Social
Security source exists. Because line 9 requires line 6b unconditionally, **every
return in the engine must satisfy 33 Social Security declarations to reach total
income**, including returns that have never received a benefit.

The existing unconditional burden is **not a precedent** and must not be cited as
one.

## The exact no-activity authority

The absence authority is **not** a default and **not** the emptiness of a
collection. It is a positive taxpayer attestation with recorded provenance,
composed of two things that must both hold:

1. **`tax.us.2025.ssa1099.source-closure` `v1`** — current, keyed on
   `family-horizon`, asserting the closure claim declared verbatim in
   `family.ssa1099-benefits.json`:

   > "Every ordinary Form SSA-1099 statement for tax year 2025 furnished to the
   > return's taxpayer or, on a joint return, the taxpayer's spouse is recorded
   > as a logical statement member with reconciled nonnegative box 3, box 4, and
   > box 5 …"

2. **Zero current members** — `count(tax.us.2025.ssa1099.box5-net-benefits)` over
   `tax.us.2025.ssa1099.benefits` equals `0`.

Taken together these assert: *the taxpayer attests the family is complete, and
it contains nothing.* That is the authority the canonical zero carries, and both
components must appear in its provenance.

### The sharpest open question — T0-1

**The closure claim disclaims the neighbouring classes.** Its own text continues:

> "This claim covers only this bounded ordinary class; it says nothing about
> RRB-1099, SSA-1042S, foreign systems, benefits belonging to another taxpayer,
> the lump-sum election method …"

`tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit` asserts exactly
the absence the closure disclaims: "No RRB-1099, SSA-1042S, or foreign
social-benefit statement is present." Its **proposition** is
source-existence — whether a statement exists at all — even though its **title**
is worded as a worksheet-completeness component.

So the objective's phrase "without satisfying worksheet-only scope declarations"
may be exactly achievable at **33 → 0**, or may be honestly achievable only at
**33 → 1**. Track 0 must decide this on the verified authority packets and say
which, with reasons. **A zero that silently ignores a disclaimed neighbouring
class is not the legally authorized zero — it is a default wearing its clothes.**

If the declaration is load-bearing, it is a **source-existence proposition
mis-scoped as worksheet completeness** — a **fourteenth** migration candidate for
Milestone 2, not a thirteenth Schedule 1 absence. **Milestone 1 records that
finding and does not act on it.**

If resolving this needs authority the packets do not carry, **stop and request a
bounded authority review**. Do not read the source.

## Proposed contract — Track 0 confirms, refines, or replaces

The engine already contains the exact shape this repair needs, on the ratified
line: `rule.schedule-a-total-closed-empty.json`. It is `rule-artifact.v4` with
`requires: []`, `pins: []`, `value: 0`, and a guard of
`all(require_closed(family), count(member) == 0)`. Its own `notes` record why the
two-rule split beats one rule with a value-level `choose`:

> "this rule has no requires at all and is always immediately eligible,
> evaluating `require_closed`/`count` directly from committed facts/closure
> state, never from another rule's published output."

That property is decisive here, and for a second reason the Schedule A case did
not face: `requires` is checked **before** evaluation
(`packages/derivation/runner.py:482`), so a hard `requires` cannot be guarded by
`when`. A single rule carrying the 33 dependencies could never skip them by
guard, however the guard were written.

Entering position, therefore:

1. **A new closed-empty producer of `tax.us.2025.social-security.line6b`** —
   `requires: []`, `pins: []`, value `0`, guarded on the two authority components
   above, `blocked: SOURCE_SET_UNCLOSED`, carrying closure and count provenance
   and its citation.
2. **A successor `rule.ss-benefits-worksheet` version** whose guard gains the
   mutually exclusive `count > 0` conjunct, so the two producers of line 6b can
   never both fire. This is the "successor rule must branch between no-activity
   and worksheet computation" the owner allowed, and is the **only** change to
   the nonempty route.

No neutral Schedule 1 facts. No fact-type succession. No change to the thirteen
predecessor declarations.

## Compatibility matrix — Track 0 must prove every row

`C` = `tax.us.2025.ssa1099.source-closure`; `n` = count of current
`box5-net-benefits` members.

| # | SSA source state | `C` | `n` | line 6a | line 6b | line 9 | Must be true |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | **Closed empty** | `yes` | 0 | `0` | **`0`, canonical zero** | Published | Zero carries closure + count provenance. **None of the 23 declarations is read or pinned.** The route is reachable with every one of them open |
| 2 | **Unclosed, no members** | open/absent | 0 | Blocked | **Blocked** | Blocked | `require_closed` fails. Absence of members is **not** absence authority. No zero is published |
| 3 | **Unclosed, members present** | open/absent | > 0 | Blocked | Blocked | Blocked | Blocks on closure, not on the worksheet declarations. **Amended by owner disposition (Stop 2): this is a deliberate semantic correction of base behaviour, not an incidental consequence.** Line 6b must not publish until the current SSA source family is confirmed complete |
| 4 | **Closed non-empty** | `yes` | > 0 | Subtotal | Worksheet result | Published | **A present SSA source cannot take the zero route.** Every worksheet dependency still required. **Amended by owner disposition (Stop 2): value unchanged from this base; provenance gains the closure triple** — the closure mapping, the family declaration, and the current closure finding |
| 5 | **Contradictory — closure asserts complete, member recorded** | `yes` | > 0 | Subtotal | Worksheet result | Published | Not a contradiction: closure asserts completeness, not emptiness. Row 4 by another name. Track 0 confirms |
| 6 | **Contradictory — closure `no`** | `no` | any | Blocked | **Blocked** | Blocked | An explicit refusal to attest completeness is **not** an authority to publish zero |
| 7 | **Contradictory — member withdrawn after closure** | `yes`, horizon advanced | 0 → | Recompute | **Recompute to `0`** | Republished | Displacement runs through declared edges; the zero is derived afresh, never left standing from the nonempty run |
| 8 | **Late member after closed-empty zero** | re-closed | 0 → 1 | Recompute | Prior zero **displaced**; worksheet route | Recompute | The canonical zero must not survive its premises. This is the late-authority counterexample |
| 9 | **Closed empty, but a disclaimed neighbouring class is present** | `yes` | 0 | `0` | **T0-1 decides** | — | The `no-rrb-or-foreign-social-benefit` question above. Row 9 is the reason T0-1 is a stop condition, not a detail |

## Track 0 findings

Paper only. Every claim below is verified against committed artifacts at this
base; no tax-instruction PDF was opened. Where a claim is established by
executing committed code, the execution was read-only against committed content
and left nothing in the repository.

### T0-1 — authority sufficiency. Verdict: **33 → 1**

**The honest reduction is 33 → 1.** The retained declaration is
`tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit`. The other 22
`ss-benefits-scope` declarations, and the ten income/convention symbols, are
genuinely worksheet-only and must not gate the no-activity zero.

**The test applied.** A matter the closure claim disclaims is load-bearing for
the zero **iff its truth could make the correct value of line 6b nonzero while
the ordinary SSA-1099 family is closed and empty.** Anything that fails that
test is worksheet-internal and cannot be a premise of the zero; anything that
passes it is a premise the zero must carry, whatever its title says.

**Why the 22 fail the test — proved, not asserted.** The committed worksheet
value expression is exactly

```text
round( min( A , bracket_fold(85%-table, line6a) ) )
```

— the `choose`/`compare lte` pair at `rule.ss-benefits-worksheet.json`'s value
root is a `min`, and its right operand is `bracket_fold` over
`demo.parameter.ss-benefits-85-rate.2025` applied to `line6a`. Every non-constant
leaf of `A` is a `bracket_fold` over a single band `lower: "0"`, `upper: null`
with a positive rate, and `_bracket_fold` contributes nothing for
`value <= lower` (`packages/derivation/evaluator.py:294-309`), so `A >= 0`
unconditionally. Therefore `line6a = 0` forces
`min(A, 0.85 x 0) = min(A, 0) = 0`, for every filing status, every MFS living
arrangement, and every value of the seven income inputs and line 2a. Confirmed
by direct evaluation of the committed expression under the committed canon and
parameters across all five filing statuses, both MFS arrangements, and income
vectors of 0 / 100,000 / 1,000,000 in each input slot — 137 cases, all exactly
`0`. The 22 declarations bound `A`; `A` is irrelevant when `line6a = 0`. They
are worksheet-only in the strict sense.

`no-lump-sum-election` is in that 22 despite the closure claim disclaiming "the
lump-sum election method": the election is a method for treating a lump-sum
payment *reported on a statement*, and a closed empty ordinary class contains no
statement for it to operate on. The same reasoning disposes of
"excess-repayment treatment" (unreachable without a member) and "benefits
belonging to another taxpayer" (not this return's line 6 by construction).

**Why `no-rrb-or-foreign-social-benefit` passes the test.** Its proposition is
source-existence — whether an RRB-1099, SSA-1042S, or foreign social-benefit
statement exists at all — and tier-1 railroad retirement benefits are line-6
benefits. If one exists, `line6a = 0` is false as a statement about the return
even though the ordinary family is closed and empty, and the reduction above no
longer reaches zero. The closure claim does not settle this and says so twice:
it disclaims "RRB-1099, SSA-1042S, foreign systems" and, decisively, disclaims
"**Form 1040 line 6a/6b completeness**". Nothing else committed carries the
proposition: the production admission boundary *rejects* an RRB or foreign
statement from being recorded as a family member at all
(`tests/test_ssa1099_benefits_line6_track2.py::test_admission_rejects_out_of_class_statements`),
so an unrecorded RRB statement is indistinguishable from no RRB statement except
through this declaration. There is no RRB fact type, family, or closure anywhere
in the corpus.

**The governance reading agrees.** ADR-0016 decision 5 says closure of a narrow
statement class authorizes only that class's subtotal, "including subtotal zero",
and does **not** authorize the Form 1040 line zero; decision 4 permits a broader
result to consume the subtotal only where the universes are identical or an
explicit composition is established as coextensive. `line6b`'s universe is
broader than `tax.us.2025.ssa1099.benefits` by exactly the RRB/1042S/foreign
class. The retained declaration **is** that coextensivity statement: with it
current and `yes`, the ordinary family's emptiness and line 6's emptiness
coincide. Without it, a closed-empty zero on line 6b is precisely the
narrow-subtotal substitution ADR-0016 forbids — a default wearing the clothes of
an authority.

Two supporting observations, recorded and not acted on:

- `audit_collect_authority` (`packages/derivation/source_authority.py:183-210`),
  which exists to enforce ADR-0016 decisions 2-5, walks only `op == "collect"`
  (`_collect_source_sets`, lines 169-180). A rule that stands on a family through
  `count` or `require_closed` — including the ratified
  `rule.schedule-a-total-closed-empty` and the producer proposed here — is not
  audited at all. The audit under-covers the exact shape this milestone uses.
  **Finding only; no repair proposed in this milestone.**
- `rule.form1040-line6a.json` publishes line 6a as a bare `ref` to the narrow
  family subtotal, with the note "Form 1040 line 6a equals the closed ordinary
  SSA-1099 box-5 family subtotal (W1)". That equation carries the same
  coextensivity gap, and today nothing declares it. **Out of scope** (line 6a is
  a non-goal), recorded so it is not later mistaken for settled.

**Row 9 / Milestone 2 finding.** `no-rrb-or-foreign-social-benefit` is a
**source-existence proposition mis-scoped as worksheet completeness**: its
proposition is about what exists, its title says "Social Security Benefits
Worksheet completeness component", and it sits in the worksheet's `requires`
alongside 22 genuinely worksheet-internal declarations. It is therefore a
**fourteenth** migration candidate for Milestone 2 — not a thirteenth Schedule 1
absence. **Milestone 1 records this and does not act on it**: no retitling, no
succession, no new fact type. Milestone 1 uses the declaration exactly as
committed, at `v1`, under its existing id.

Reading the other 22 for the same disguise: none is a source-existence
proposition. Each names a Form 1040 or Schedule 1 line, form, or exclusion whose
only path to line 6b is through `A`, and `A` is unreachable at `line6a = 0`. The
23 divide 22 / 1, and the 1 is the one the closure claim already told us about.

### T0-2 — the contract: confirmed, with two refinements and one consequence

> ## ⚠ WITHDRAWN — superseded by the corrected settlement
>
> **This settlement selected a two-producer contract. That contract is not
> implementable and the decision is withdrawn.** It is retained unaltered below
> as the record of a decision whose factual premise was later disproved by
> measurement; it is **not** authority for anything.
>
> - **Refuted by:** the presentation measurement in `## Track 1 stop report` —
>   `line6b` is form-field-bound, `presentation_projection._one_row` admits
>   exactly one disposition row for it, and the runner records a row for every
>   rule on every path. No matrix row survives.
> - **False premise:** T0-2's live-scheduler reasoning (see the correction
>   below).
> - **Superseded by:** `## Corrected Track 0 settlement — single producer`.
>
> Owner instruction governing this supersession: *do not preserve a decision
> after its factual premise has been disproved; preserve history by recording
> and superseding the decision, and do not treat precedent as authority against
> measured evidence.*

The entering contract survives in shape. It does not survive unchanged.

> **Correction, entered by the foreman after Track 1 (see the Track 1 stop
> report).** The claim below that `requires` is tested before the guard "in both
> schedulers" is **false for the live marshalled scheduler**, which preflights
> the guard first and treats a provably false guard as an atomic `inapplicable`
> "even when later numeric dependencies are absent" (`runner.py:1126-1145`).
> Verified directly. The **conclusion** stands — a rule still cannot publish
> while skipping its `requires` — but the reasoning as written must not be
> relied on or reused.

**Confirmed — the second producer is necessary, not convenient.** `requires` is
tested before the guard is ever evaluated, in both schedulers:
`packages/derivation/runner.py:516-518` (`missing = [req for req in
rule["requires"] if req not in self.symbols]`, immediately recording `blocked`)
ahead of `runner.py:539` (`guard = evaluate(rule["when"], ...)`), and again at
`runner.py:1149` ahead of `runner.py:1183`; eligibility itself is
`all(req in self.symbols ...)` at `runner.py:481-482`. No guard, however
written, can cause a rule to skip its own `requires`. A single rule carrying the
33 therefore cannot express the no-activity route. Two producers it is.

**Confirmed — every operator already exists.** The guard needs `all`,
`require_closed`, `count`, `compare`, `categorical_compare`, `category_literal`,
`ref`. All seven are in the committed vocabulary
(`packages/derivation/evaluator.py:101-238`). Nothing needs `multiply`,
`divide`, or `min`. **No substrate stop on operators.**

**Refinement 1 — the guard carries the T0-1 conjunct.** The closed-empty
producer's guard is

```text
all[ require_closed(tax.us.2025.ssa1099.benefits),
     count(tax.us.2025.ssa1099.box5-net-benefits over that family) == 0,
     categorical_compare(no-rrb-or-foreign-social-benefit, eq, "yes") ]
```

with `requires: []` and `pins: []`, in that conjunct order. Order is chosen, not
incidental. `all` short-circuits on the first false
(`evaluator.py:173-174`), and a published result's pins come from what the
evaluation actually read (`runner.py:343-359`), so:

- On the **publishing** path order is immaterial — every conjunct must be true,
  hence every conjunct is evaluated, hence closure *and* the declaration are both
  read and both pinned. Both authority components land in provenance.
- On the **blocked/inapplicable** paths order decides the evidence. With
  `require_closed` first, an unclosed family blocks `SOURCE_SET_UNCLOSED` having
  actually consulted closure state, which is what the artifact's declared
  `blocked` block says. With the declaration first, an unclosed family would
  block on an absent declaration and never mention closure.

What the pins actually contain, mechanically: `require_closed` and `count` each
add the family to `AccessLog.closure_reads` (`evaluator.py:200-205` and
`133-141`), and `pins_for` turns each closure read into three pins — the closure
mapping (`package`), the family declaration (`package`), and **the exact current
closure finding** (`input`) — at `runner.py:419-432`. The zero-count component
has no finding to pin by construction; it is carried by the absence of any
member pin (`collects` yields `source_fids.get(name, []) == []`,
`runner.py:360-366`) together with the pinned rule version whose guard demands
`count == 0`. That is the honest record of "closed, and containing nothing", and
it is the same record the ratified Schedule A closed-empty producer makes.

The `input` pin on the closure finding is not decoration: `input` is a
dependency role (`packages/derivation/projection.py:32`) and therefore a
derivation edge (`projection.py:44-56`). It is the entire mechanism by which
rows 7 and 8 work.

**Refinement 2 — the worksheet successor must be `rule-artifact.v4`.** `count`
is admissible only under `rule-artifact.v4`; `rule-artifact.v3` has no `count`
(verified by direct schema inspection of
`packages/schemas/derivation/rule-artifact.v3.schema.json` and `.v4`). `v4` is
`v3`'s grammar plus `count`/`block`, and retains `conditional_dependency_set`,
which the worksheet's MFS living-arrangement node needs. So the successor is a
version *and* schema move: `rule.ss-benefits-worksheet` `v1`
(`rule-artifact.v3`) to a successor under `rule-artifact.v4`. No new schema
family; `v4` is already published and adopted.

**Mutual exclusivity — proved.** The successor's guard gains `count(...) > 0` as
its **first** conjunct. `count == 0` and `count > 0` over the same fact type and
the same family are contradictory for every state, so the two producers can
never both be eligible-and-true. They can both be false (rows 2, 3, 6, 9), and
line 6b is then correctly unpublished. This matters because the runner has **no
guard-exclusivity validation**: a second producer reaching an already-published
symbol is recorded `inapplicable` and the first publisher wins
(`runner.py:520-533`), which would make the pins of a doubly-eligible symbol
depend on traversal order. Exclusivity is a content obligation and Track 1 owes
it a kill test, not an assertion.

**The consequence — and it trips a declared stop condition.** `count` blocks
`SOURCE_SET_UNCLOSED` whenever the family is not closed (`evaluator.py:136-141`),
unconditionally, and adds a closure read whenever it succeeds. `collect`, by
contrast, consults closure **only when the collection is empty**
(`evaluator.py:118-131`). So today a nonempty SSA family publishes line 6a and
line 6b with no closure at all — a committed, named behaviour:
`test_member_present_no_closure_publishes` ("closure only ever gates the empty
case"). Giving the worksheet successor a `count > 0` conjunct therefore changes
the **existing nonempty route** in two ways:

1. **Availability.** An unclosed nonempty family stops publishing line 6b and
   blocks `SOURCE_SET_UNCLOSED`. This is what matrix row 3 demands, and it is
   the opposite of what the base does.
2. **Provenance.** A *closed* nonempty family still publishes the same value,
   but its line-6b finding gains three pins it does not carry at this base —
   closure mapping, family declaration, closure finding.

Neither is avoidable. `count` is the only sound discriminator between empty and
nonempty: a sum-based or `max`-based test would misclassify a legitimate member
whose box 5 is zero (`test_zero_benefits_statement_publishes_zero`,
`test_repayment_equal_to_benefits_publishes_zero`), and there is no operator that
reads membership without reading closure. Leaving the successor's guard untouched
is worse: in a closed-empty return that happens to carry all 33 declarations both
producers would be true, both would compute `0` (by the T0-1 reduction), and
which pins the published zero carried would depend on scheduler order.

The milestone's own stop conditions list "any existing income route's value or
provenance changes". **This is that.** The value never changes; availability and
provenance do. Recorded as a stop for owner disposition, not worked around —
see `## Track 0 stop report`.

### T0-3 — compatibility matrix, proved row by row

`C` = current `tax.us.2025.ssa1099.source-closure` at the family's current
horizon; `n` = count of current `box5-net-benefits` members; `R` =
`no-rrb-or-foreign-social-benefit`. "New" = the closed-empty producer, "WS" =
the worksheet successor.

| # | State | line 6a | line 6b | line 9 | Mechanism |
| --- | --- | --- | --- | --- | --- |
| 1 | `C` yes, `n`=0, `R` `yes` | `0` | **`0`, New** | Published | Subtotal `collect` on an empty closed family returns `[]` → `0`; New's three conjuncts all true, all read, all pinned. WS is `blocked` on its own `requires` when the other 22 are open, and `inapplicable` on `count > 0` when they are present — never a rival. **PASS** |
| 2 | `C` open/absent, `n`=0 | Blocked | **Blocked** | Blocked | `resolve_closure_admissions` leaves the family unadmitted (`source_authority.py:141-156`); `collect` on empty-unclosed raises `SOURCE_SET_UNCLOSED`; New's first conjunct raises the same. Emptiness alone publishes nothing. **PASS** |
| 3 | `C` open/absent, `n`>0 | Published (unchanged) | **Blocked** `SOURCE_SET_UNCLOSED` | Blocked | WS's first conjunct is `count > 0`, which raises before any declaration is read — "blocks on closure, not on the declarations", as the row requires. **PASS on the row as written; this is a change from base** (`test_member_present_no_closure_publishes` asserts today's publish). Line 6a is unchanged and still publishes, because `collect` skips the closure check on a nonempty set. |
| 4 | `C` yes, `n`>0 | Subtotal | Worksheet result | Published | WS: `count > 0` true, 23 categorical conjuncts true, `conditional_dependency_set` unchanged, value expression untouched. **Value PASS. Provenance FAIL as the row is written** — `count` adds the closure triple to the published line-6b pins. See the T0-2 consequence and the stop report. |
| 5 | `C` yes, `n`>0 (closure asserts complete, member recorded) | Subtotal | Worksheet result | Published | Confirmed: this is row 4 under another name and **not** a contradiction. The closure claim asserts *completeness of the recorded set*, never emptiness; `admission: current-literal-true` and a present member are independent facts. **PASS** |
| 6 | `C` `no` | Blocked | **Blocked** | Blocked | A `false` closure finding is a quiet non-admission (`source_authority.py:155-156`: value must be boolean `True`); the family never enters `closed_sets`, so `require_closed` and `count` both raise. An explicit refusal to attest is not an authority to publish zero. **PASS** |
| 7a | Member withdrawn; horizon advanced; **no new attestation** | Blocked | **Blocked** | Blocked | The withdrawal is a membership transition recording a successor horizon (ADR-0017 decision 3). The predecessor horizon is superseded → `superseded_entity_ids` root (`currency.py:151`) → individuation edge to the closure finding keyed on it (`currency.py:127-133`) → closure displaced. No closure at the current horizon → family unadmitted → the now-empty `collect` blocks. The prior nonempty line 6b is displaced independently, through its member-finding pin chain (member → subtotal → 6a → 6b). **PASS** |
| 7b | 7a, then re-attested at the new horizon | `0` | **`0`, New** | Republished | ADR-0017 decision 7: fresh attestation plus explicit rerun. Row 1 mechanics on the successor horizon. **PASS** |
| 8a | Late member after a published closed-empty zero; horizon advanced; **no new attestation** | Published | **Blocked** | Blocked | The prior zero pinned the closure finding as `input` (T0-2), so horizon supersession → closure displaced → derivation edge → **the zero is displaced**. It cannot survive its premises. Line 6a republishes from the present member; line 6b blocks on WS's `count > 0` closure read. **PASS** |
| 8b | 8a, then re-closed at the new horizon | Published | Worksheet result | Published | Row 4 mechanics. **PASS** (subject to row 4's provenance finding) |
| 9 | `C` yes, `n`=0, `R` `no` | `0` | **Unpublished** (`guard_inapplicable`) | Blocked | New's third conjunct is false → `inapplicable` with `guard_result: false`; WS is false on `count > 0`. Line 6b has no producer and line 9 blocks `DEPENDENCY_ABSENT`. **This is the correct answer**: a disclaimed neighbouring class is present and the engine has no route to compute line 6 for it, so it declines rather than publishing a zero it cannot justify. If `R` is *open* rather than `no`, New blocks `DEPENDENCY_ABSENT` naming exactly `R` — one declaration, not 33. **PASS** |

Rows 7 and 8 each split in two because ADR-0017 decision 7 requires a fresh
attestation and an explicit rerun before a successor closure-backed result may
publish; the plan's single-line phrasing ("horizon advanced ... recompute to
`0`") skips that intermediate state. The split is a refinement of the row, not a
failure of the contract, and the intermediate blocked state is already a
committed, tested behaviour for line 6a
(`test_live_late_member_stale_closure_and_reclosure`, step 3).

One presentation consequence worth carrying into Track 1: because the retained
declaration is a non-closure finding in the zero's pin lineage,
`_classify_numeric` (`packages/derivation/presentation_projection.py:148-158`)
sees a source leaf and labels row 1 `computed_zero`, not `closure_backed_zero` —
which is what `test_closed_empty_family_publishes_zero` already asserts. Had
T0-1 landed at 33 → 0, that label would have flipped. `form1040.line-6b.form-field.json`
already declares `closure_backed_zero`, `computed_zero`, `guard_inapplicable`,
and `SOURCE_SET_UNCLOSED`; **no form-field change is needed**.

### T0-4 — impact envelope and regression surface

**Allowed-impact envelope.** Track 1 may touch exactly:

*New content*
- one new `rule-artifact.v4` computation publishing
  `tax.us.2025.social-security.line6b` (the closed-empty producer);
- one successor version of `rule.ss-benefits-worksheet` under
  `rule-artifact.v4`, differing from `v1` in the `count > 0` conjunct and the
  schema line only — value expression, citations, and the 23 categorical
  conjuncts byte-identical;
- one successor `package.core-calculations` version and one successor
  `published-packages` registry version (v29 / v24 are current);
- one adoption fixture under
  `packages/sample_data/ssa1099_benefits_line6/adoptions/` and its publication-
  surface release entry.

*Existing tests at risk — named*
- `tests/test_ssa1099_benefits_line6_track2.py::test_member_present_no_closure_publishes`
  — **breaks by design**; its docstring ("closure only ever gates the empty
  case") becomes false for line 6b. Cannot be repaired without abandoning
  producer exclusivity. Blocked on the stop report.
- `::test_closed_empty_family_publishes_zero` — value and disposition survive
  (see T0-3), but line 6b's producer and pins change; any pin-level assertion
  added here must be rewritten rather than extended.
- `::test_live_late_member_stale_closure_and_reclosure` — steps 1 and 4 gain a
  line-6b assertion path through the new producer; step 3's line-6a expectations
  are unaffected.
- `::test_live_scope_guards_*` (four batches, all 23 tokens) — each sets one
  token to `no` on a **nonempty** family, so WS is `inapplicable` and New is
  `inapplicable` on `count > 0`; expected `guard_inapplicable` should survive,
  but the `no-rrb-or-foreign-social-benefit` subtest now has a second
  inapplicable producer and must be re-verified rather than assumed.
- `::test_worksheet_when_names_every_scope_token`, `::test_worksheet_pin_table_excludes_line9_cycle`
  — must be re-pointed at the successor version; both should pass unchanged in
  substance.
- `::test_package_resolves_v28`, `::test_package_additive_only`,
  `::test_manifest_only_adds`, `::test_package_and_registry_semantic_integrity`
  — extend for the successor package and registry versions.
- `tests/test_f1098_mortgage_interest_line12e_track2.py` — builds its entire base
  corpus on `_ssa_acts(benefits=[], close=True)` and adopts
  `adopt-core-v29-current.json`. It is the clearest witness that the defect is
  engine-wide, and the clearest regression risk from the package bump. Its
  values must not move.
- `tests/tax/test_ssa1099_track1.py` — vocabulary and mapping only; unaffected.

*Unchanged and must stay unchanged*
- `family.ssa1099-benefits.json`, `closure-mapping.ssa1099-benefits.json`,
  `ss-benefits-scope.bundle.json` (all 23 fact types, ids, titles, versions),
  `rule.ssa1099-benefits-subtotal.json`, `rule.form1040-line6a.json`,
  `rule.form1040-line9.v7.json`, `form1040.line-6b.form-field.json`, and every
  evaluator, runner, currency, and projection module. **No kernel or engine code
  changes at all.**

*Fixtures.* Synthetic only, one per matrix row including the 7a/7b and 8a/8b
splits. Row 1 must be built with **22** `ss-benefits-scope` declarations open and
only `no-rrb-or-foreign-social-benefit` present — that fixture, and the fact that
it reaches line 9, is the whole proof of the milestone.

*Version allocation.* None in Track 0. No schema family is created, so nothing
is owed to the schema-intent ledger for a *schema*; the successor package and
registry versions are allocated at the Track 1 charter, after the stop below is
dispositioned.

## Tracks

| Track | Content | State |
| --- | --- | --- |
| 0 | T0-1 authority sufficiency (rows 1, 2, 6, 9); T0-2 contract confirmation and the two-producer split; T0-3 the full compatibility matrix; T0-4 impact envelope and regression surface; adversarial closure | **Complete — both stops dispositioned by the owner; gate closed** |
| 1 | ~~Implement the closed-empty producer and the successor worksheet guard~~ | **Stopped — superseded; see `## Track 1 stop report`** |
| 0′ | Reopened Track 0: withdraw the two-producer settlement, select the single-producer contract, prove it | **Complete — ten obligations measured; see `## Reopened Track 0 prototype evidence`** |
| 1′ | Implement the **single-producer** successor under the corrected settlement | **Chartered — see `## Amended Track 1 charter`** |

## Contracts

Confirmed by Track 0 (T0-2), with two refinements: the closed-empty guard gains
the `no-rrb-or-foreign-social-benefit` conjunct, and the worksheet successor
moves `rule-artifact.v3 → v4` because `count` is not in the v3 grammar. One new
rule artifact and one successor
version of an existing rule artifact, both content-level. **No new schema
family.** Version numbers are allocated only after Track 0 states the
allowed-impact envelope, and any schema family and version is appended to the
schema-intent ledger (`docs/process/concurrent-work.md`) before the edit.

## Fixtures

Synthetic only, one per matrix row. **Amended by T0-1:** row 1 must be
constructed with the **22 worksheet-only `ss-benefits-scope` facts left open**
and only `no-rrb-or-foreign-social-benefit` present, because that is the
property under test: the repair is proved by what the workspace does **not**
need to answer. The original "all 23 open" phrasing predates the 33 → 1 verdict
and would assert a zero with no source-existence authority behind it.

## Verification

1. Every row of the compatibility matrix.
2. Form 1040 line 9 and every existing income route retain their values and
   provenance — W-2, interest, dividend, IRA, capital-gain, unemployment,
   foreign-tax, mortgage.
3. The closed-empty zero's provenance names the closure fact and the member
   count, and pins neither the 23 declarations nor any worksheet symbol.
4. Exactly one producer of `tax.us.2025.social-security.line6b` fires in every
   reachable state.
5. Correction and replay produce the same current state; delete-and-rerun
   reproduces derived results and provenance.
6. Schema registry, data-safety, governance, typing, and CI gates pass.

### Verification results — Track 1

Track 1 stopped before the verification programme could be run to completion.
What was measured, and what was not:

| # | Item | Result |
| --- | --- | --- |
| 1 | Every matrix row | **Not verifiable under the confirmed contract.** The guards behave exactly as T0-3 predicted on every probed row (see the measurement table in the stop report), but **no** row produces a presentation model, because every reachable state yields two `line6b` disposition rows. Rows 1, 2, 3, 4 and 9 measured; rows 5, 6, 7a/7b and 8a/8b not reached |
| 2 | Existing income routes unchanged | **Not measured.** No package version was committed, so no existing route was re-run against a successor package |
| 3 | Closed-empty zero's provenance | **Measured and correct.** The row-1 zero published with 7 pins: the adoption, both citations, the current closure finding (`input`), the closure mapping (`package`), the family declaration (`package`). No `ss-benefits-scope` declaration other than `no-rrb-or-foreign-social-benefit`, no member pin, no worksheet symbol |
| 4 | Exactly one producer fires | **True of publication, false of disposition.** Exactly one producer ever reached `published`. Both producers always recorded a disposition row, which is the defect |
| 5 | Correction and replay | Not reached |
| 6 | Registry, data-safety, governance, typing, CI gates | Ran against the committed tree; results in the stop report. No content, package, registry, release or adoption artifact was committed |

### Verification results — Track 1′ (the published single-producer contract)

Measured against the real published surface: `rule.ss-benefits-worksheet` **v2**
(`rule-artifact.v4`), `package.core-calculations` v30, `published-packages`
v25, release v23, `adopt-core-v30-current`. Permanent suite:
`tests/test_ssa_no_activity_line6b_track1.py` (promoted from the reopened
Track 0 prototype's harness), now **28 tests**: the seventh mutation kill-test
was added when independent review found the numeric-inputs guard existed only
on the prototype's synthetic surface; four more (`TestDependencyCostWitness`)
were added when a targeted re-review found the six-of-seven /
`tax-exempt-interest.line2a-total` relationship existed only as prose, with no
committed regression that would fail if it became false.

| # | Item | Result |
| --- | --- | --- |
| 1 | Every matrix row | **Met.** All nine rows of `## Compatibility matrix` — closed empty (declarations absent and present), unclosed empty, unclosed nonempty, closed nonempty (complete and 4 declarations absent), `R = no` closed empty and closed nonempty, `R` absent closed empty — each yields exactly one `line6b` disposition row and a valid `presentation-model.v1` |
| 2 | Existing income routes unchanged | **Met.** `tests/test_ssa1099_benefits_line6_track2.py` (48 passed, 37 subtests) and `tests/test_f1098_mortgage_interest_line12e_track2.py` (26 passed, 2 subtests) both pass unmodified against the v30 chain; the four `test_live_scope_guards_*` batches and `test_worksheet_when_names_every_scope_token` pass against the untouched v1 rule, which remains reachable through the package versions that admit it |
| 3 | Closed-empty zero's provenance | **Met, unchanged from the prototype's measurement.** The zero pins the closure finding and the retained declaration's finding (`input`), the closure mapping and family declaration (`package`), both citations, and the adoption — no other `ss-benefits-scope` declaration, no worksheet symbol |
| 4 | Exactly one producer fires | **Met.** One rule, `rule.ss-benefits-worksheet` v2, is the package's sole `tax.us.2025.social-security.line6b` producer; no `conflict_semantics` entry names the symbol; every matrix row yields exactly one `line6b` disposition row |
| 5 | Correction and replay | **Met for the lifecycle obligation this milestone owns** (ADR-0017 decision 7, obligation 8): a late member displaces the closed-empty zero, the source family blocks on `SOURCE_SET_UNCLOSED` rather than substituting a stale authority, and fresh closure recomputes — first the complete missing-declarations list, then a real nonzero worksheet value once they are answered. General delete-and-rerun replay was not separately re-measured beyond the existing suite's coverage |
| 6 | Registry, data-safety, governance, typing, CI gates | **Met.** `mypy` success on 191 source files; `governance_lint` conformant; `tools/envelope_scan.py --verify` and `--range <base>..HEAD` clean; full suite green (see below) |

The four-part replacement evidence for the stopped Track 1's never-written
`test_member_present_no_closure_publishes` is in
`TestUnclosedNonemptyReplacesTheSupersededPrototype`: nonempty-unclosed
blocks (`test_part_1_nonempty_unclosed_blocks`); closed-nonempty publishes the
same value with the closure provenance
(`test_part_2_closed_nonempty_publishes_the_same_value_with_closure_provenance`);
a late member invalidates (`test_part_3_a_late_member_invalidates`); fresh
closure republishes (`test_part_4_fresh_closure_republishes`).

All six obligation-10 mutation kill-tests are present and pass:
`test_changing_the_zero_branch_changes_the_published_zero`,
`test_dropping_the_retained_declaration_lets_R_absent_publish_a_zero`,
`test_inverting_the_conditional_condition_activates_members_when_empty`,
`test_mutating_the_family_id_strips_the_zeros_closure_authority`,
`test_mutating_the_member_predicate_changes_the_nonempty_value`,
`test_the_closure_relation_is_carried_by_count_not_by_require_closed`.

No schema-intent ledger entry was made: `rule-artifact.v4`,
`artifact-package.v22`, `bundle.v2` and `release-registry.v1` all already
exist in the corpus, so nothing new was proposed.

## Data safety

Synthetic fixtures only. No personal document, statement, or real return value
enters the repository. **No tax-instruction PDF is opened, quoted, summarized,
staged, or committed** by any seat. No absolute workstation path is committed.

## Non-goals

- Neutral Schedule 1 facts and fact-type succession — **Milestone 2**.
- Retiring, deleting, or re-titling any of the 23 predecessor declarations.
- Changing the nonempty worksheet computation, other than the mutually exclusive
  guard conjunct.
- Form 1098-E work of any kind.
- The `schedule1-part1-scope.bundle.json` and `attachment-rule.v5` deferrals.

## Exit criteria

- Track 0 adversarial closure complete with no unresolved `FAIL`.
- T0-1 answered: the exact authority, and whether the honest reduction is
  33 → 0 or 33 → 1, with reasons.
- Allowed-impact envelope stated before the Track 1 charter.
- Every matrix row and verification item passes.
- No ADR needed, or the discovery that one is needed recorded as a stop.

### Exit-criteria status — Track 1

| Criterion | Status |
| --- | --- |
| Track 0 adversarial closure with no unresolved `FAIL` | **Met** at Track 0 close, by owner disposition |
| T0-1 answered (33 → 1, with reasons) | **Met.** Track 1 found nothing that disturbs it; the retained declaration behaved exactly as T0-1 predicted, gating row 9 `guard_inapplicable` and pinning into the row-1 zero |
| Allowed-impact envelope stated before the Track 1 charter | **Met** |
| Every matrix row and verification item passes | **Not met.** See the Verification results table |
| No ADR needed, **or the discovery that one is needed recorded as a stop** | **Met, by the second limb.** An ADR is needed and the discovery is recorded as a stop rather than resolved by silent adoption |

The milestone does not exit. It returns to the owner with a design question
Track 0 could not have closed on paper, because the obstruction is in the
presentation join and not in the derivation contract.

### Exit-criteria status — Track 1′ (published)

| Criterion | Status |
| --- | --- |
| Track 0 adversarial closure with no unresolved `FAIL` | **Met** at Track 0 close, unchanged |
| T0-1 answered (33 → 1, with reasons) | **Met**, unchanged from Track 1 |
| Allowed-impact envelope stated before the Track 1 charter | **Met** |
| Every matrix row and verification item passes | **Met.** See `### Verification results — Track 1′` above |
| No ADR needed, or the discovery that one is needed recorded as a stop | **Met, by the first limb this time.** The published contract is a content instantiation of `rule-artifact.v4`, `conditional_dependency_set`, `choose`, `count` and `require_closed`, all already ratified; no new reusable engine mechanism was needed |

The milestone's build slice exits on this track. No stop condition was hit:
the single rule expresses every required branch-specific pin and explanation,
the established nonempty worksheet value is unchanged (measured equal to the
ratified route, by value and by disposition, across seven value cases), and
no engine or schema behaviour beyond existing contracts was required.
Independent review of derivation behaviour and presentation projection, per
the owner's instruction, returned **APPROVE WITH FINDINGS**; both findings are
closed. See `## Independent review` below.

## ADR posture

This milestone **should not need an ADR**. It is expected to be a content
instantiation of existing closure, conditional, and canonical-zero contracts,
following a shape already on the ratified line. An ADR becomes necessary only if
Track 0 discovers a **new reusable mechanism** rather than an instantiation —
which is itself a stop condition.

## Stop conditions

Stop and report to the owner if:

- the verified authority packets do not establish the no-activity zero
  (**request a bounded authority review**; do not read the source);
- the honest zero requires a declaration beyond the closure and count — record
  the finding, do not act on it (row 9);
- the repair requires generic substrate, a new schema family, or kernel change
  — **stop and re-price the split**;
- the closed-empty route can be reached without complete closure authority;
- a present SSA source can reach the zero route;
- any existing income route's value or provenance changes;
- Track 0 discovers a new reusable mechanism rather than a content
  instantiation.

## Track 0 adversarial closure

### 1. Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `tax.us.2025.ssa1099.source-closure` `v1` | Every ordinary Form SSA-1099 furnished to taxpayer/spouse for 2025 is recorded as a reconciled member of this family | The family `tax.us.2025.ssa1099.benefits` `v1` **at one recorded horizon** — not the tax year | The family declaration and its member predicate; the horizon current at attestation (`closure_horizon_key: family-horizon`) | Any membership transition — add, remove, or predicate-crossing change — records a successor horizon, superseding the predecessor and displacing this finding through the individuation edge (`currency.py:127-133,151`). Also: correction to `false`, or a duplicate finding at the same horizon (`source_authority.py:146-156`) |
| Zero current `tax.us.2025.ssa1099.box5-net-benefits` members | The recorded ordinary class contains nothing | The same family at the same horizon | Nothing; it is a count over current member findings | Any admitted member. It has no finding of its own and therefore no pin — it is carried by the *absence* of member pins plus the guard of the pinned rule version |
| `tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit` `v1` | **No RRB-1099, SSA-1042S, or foreign social-benefit statement exists for this return** | The **return** — a source-existence proposition over a class the workspace cannot otherwise represent. Its `tax-year=2025` identity key is storage identity, **not** authority scope | Nothing else committed; there is no RRB family, fact type, or closure anywhere | Free supersession (`supersession.policy: free`). A correction to `no` makes the zero inapplicable; withdrawal makes it blocked. Nothing in the engine can contradict it, because an RRB statement cannot be recorded at all (admission rejects it) |
| The other 22 `ss-benefits-scope` declarations `v1` | Worksheet-internal completeness of the `A` term | The return, for worksheet purposes only | The worksheet's input symbols | Irrelevant to the zero: `A` is unreachable at `line6a = 0`. They keep their existing lifecycle on the nonempty route, unchanged |
| `tax.us.2025.ssa1099.benefits.box5-subtotal` (derived) | The family subtotal | The family at its horizon | Member findings, or the closure when empty | Displaced by member correction/withdrawal, or by closure displacement when it stood on closure |

The middle row is the gate's own warning made concrete: the retained declaration
is keyed on the tax year but its proposition is about a statement set that can
change at any time, and its authority scope is the return, not the year. That
mismatch is the Milestone 2 finding, recorded in T0-1 and not acted on here.

**PASS** — every authority the design relies on is listed with a real
invalidation event; none is scoped by storage identity in this table's reading.

### 2. Empty/nonempty authority matrix

| Family state | Universe / absence authority | Eligibility or applicability | Expected feature result (line 6b) | Expected neighboring result (line 9, line 6a) |
| --- | --- | --- | --- | --- |
| Closed empty | Complete: closure current at the current horizon **and** `R` = `yes` | Applicable — New's guard true | Explicit `0`, pinning closure mapping + declaration + closure finding + `R` | Line 9 published; line 6a `0`. **Available with 22 of the 23 declarations open** — this is the milestone's whole claim |
| Closed empty | Required universe incomplete: `R` absent | Blocked | Blocked `DEPENDENCY_ABSENT`, naming exactly `R` | Line 9 blocked along that one dependency only; line 6a still `0`, since 6a does not depend on `R` |
| Closed empty | Required universe contradicted: `R` = `no` | Inapplicable — New's guard false, WS's `count > 0` false | Unpublished, `guard_inapplicable` | Line 9 blocked. Correct: an RRB statement exists and the engine has no route to line 6 for it |
| Closed empty | Closure absent, `false`, or at a stale horizon | Blocked | Blocked `SOURCE_SET_UNCLOSED` | Line 9 blocked; line 6a blocked. Emptiness is never authority |
| Nonempty | Closed and every worksheet declaration `yes` | Applicable — WS | Worksheet result (value unchanged from base) | Line 9 published. **Provenance gains the closure triple** — the row-4 finding |
| Nonempty | Closed, some worksheet declaration `no` | Ineligible — WS guard false, New false on `count` | **Unpublished, `guard_inapplicable`** (chosen explicitly, not inherited) | Line 9 blocked. This is base behaviour, deliberately preserved: an out-of-scope worksheet return must not fall through to a zero |
| Nonempty | Unclosed | Blocked | Blocked `SOURCE_SET_UNCLOSED` | Line 9 blocked. **Change from base**, where it publishes |

**PASS on authority; FAIL on the last row's blast radius** — see artifact 5 and
the stop report. The "nonempty, ineligible" row is decided explicitly:
`guard_inapplicable`, never a zero.

### 3. Late-authority counterexample

`attest → close → compute → add member → reclose → recompute`, traced against
committed machinery. The committed test
`test_live_late_member_stale_closure_and_reclosure` already runs this trace for
line 6a; the line-6b column is what this milestone adds.

| Transition | What becomes unusable, and why |
| --- | --- |
| **attest** — `R` = `yes`, closure `true` at horizon `h0` | Nothing yet. Both are ordinary attested findings |
| **close** | The family enters `closed_sets` only while a single `true` closure finding exists at the *current* horizon (`source_authority.py:141-156`) |
| **compute** | New publishes `line6b = 0`, pinning mapping, declaration, the `h0` closure finding (`input`), and `R`. Line 9 publishes. No member pin exists — that absence is the zero-count evidence |
| **add member** | The member transition atomically records successor horizon `h1` (ADR-0017 decision 3). `h0` is superseded → displacement root (`currency.py:151`) → individuation edge displaces the `h0` closure finding (`currency.py:127-133`) → the **derivation edge from that closure finding displaces the published zero** (`projection.py:44-56`, role `input`). The zero does not survive its premises. Line 9's published total is displaced with it, through its own pin on line 6b. `R` is untouched — its proposition did not change |
| **reclose** | A new closure finding at `h1`. The `h0` finding stays displaced forever; supersession roots accumulate, so removing the member again cannot resurrect the old zero (ADR-0017 decision 6) |
| **recompute** | With the member present, WS computes the worksheet result; New is `inapplicable`. Between *add member* and *reclose* the engine blocks rather than publishing anything — the state the test's step 3 already pins down |

No declaration remains current after the authority it summarizes changes: the
closure is displaced by construction, and `R` is not a summary of the family at
all — it is a proposition about a different, unrepresentable class whose truth is
untouched by a member arriving in this one. **PASS.**

### 4. Claim-reuse proof

The reused claim is the **worksheet's own value**, not a substitute zero.

- **Same real-world proposition.** New publishes the number the worksheet itself
  would publish. Proved, not assumed: the worksheet's value root is
  `round(min(A, 0.85 x line6a))` and `A >= 0` because every leaf is a
  `bracket_fold` over a `lower: "0"` band that contributes nothing below its
  floor, so `line6a = 0` forces `0` — verified across all five filing statuses,
  both MFS arrangements, and income vectors to 1,000,000 in every input slot
  (137 cases, all `0`). New asserts nothing the worksheet does not already say.
- **Same identity and lifecycle.** Same published symbol
  `tax.us.2025.social-security.line6b`, same form field, same displacement
  edges. New's finding is displaced by closure displacement, member arrival, and
  `R` supersession — every event that would invalidate the worksheet's own zero
  in the same state.
- **Same declared authority scope and explanation.** New carries the same line-6b
  citation. Its authority is narrower than the worksheet's, not broader: closure
  + emptiness + `R`, rather than closure + emptiness + 23 declarations. The 22
  it drops are not part of the proposition at `line6a = 0`, which is exactly what
  the reduction proves.

The one place a broadening *was* attempted and rejected is recorded in T0-1:
reusing the narrow family's closure as authority for the broader line-6b universe
without `R` would be a title-and-shape reuse that redefines the source
declaration — the thing this artifact exists to catch. **PASS, at 33 → 1 and
only at 33 → 1.**

### 5. Neighboring-capability dependency diff

| Neighbor | Prerequisites before | Prerequisites after | Verdict |
| --- | --- | --- | --- |
| Form 1040 line 9 / total income, on a **no-activity** return | line 6b, hence all 33 SSA symbols: 23 declarations + 7 income totals + line 2a + line 6a + filing status + rounding | line 6b via New: SSA closure at the current horizon, zero members, and **`no-rrb-or-foreign-social-benefit`** | **PASS.** 32 prerequisites removed, none added. The closure attestation was already required for line 6a's zero at this base; `R` is justified by line 6's own meaning (tier-1 RRB benefits are line-6 benefits), not by convenience |
| Everything downstream of line 9 — AGI, taxable income, line 16, Schedule A, the Form 1098 corpus | Inherit all 33 | Inherit 1 declaration + closure | **PASS.** `tests/test_f1098_mortgage_interest_line12e_track2.py` builds on `_ssa_acts(benefits=[], close=True)` today purely to satisfy this chain |
| Line 6a | Family subtotal; closure only when empty | Unchanged | **PASS.** New does not publish, read, or pin line 6a |
| The **nonempty worksheet route** (existing neighbor) | 33 symbols; **no closure requirement at all** when members are present | 33 symbols **plus SSA family closure**, because `count` cannot read membership without reading closure | **FAIL — blast-radius review owed.** A new feature-specific prerequisite is imposed on an existing neighbor. It is arguable from the neighbor's own meaning (a worksheet over an incomplete benefit set is not the worksheet the instructions describe, and matrix row 3 already demands it), but it is not derivable from it, it changes committed tested behaviour, and the gate forbids downgrading it. Owner disposition required |
| The 23 declarations themselves | Unconditional `requires` of the sole line-6b producer | Unchanged on the nonempty route; 22 unreachable on the no-activity route; none retired, deleted, or retitled | **PASS** |

### 6. Integration-surface artifact

Added retroactively, 2026-08-13. `PROJECT_PLANNING.md`'s Track 0 gate gained a
sixth required artifact (PR #175, merged after this milestone's Track 0 first
closed) generalizing the exact lesson this milestone's own Track 1 learned the
hard way: the chartered two-producer design copied `rule.schedule-a-total-
closed-empty`'s shape, but `tax.us.2025.schedule-a.total` is never
form-field-bound, so the precedent never had to satisfy the one-row
cardinality it silently assumed. That failure is the artifact's origin case;
this section restates the evidence this milestone already committed under
`## Reopened Track 0 prototype evidence` in the artifact's required shape,
rather than re-deriving it.

**Binding table** — `tax.us.2025.social-security.line6b` is form-field-bound:

| Consumer | Binding artifact or join | Cardinality it expects | Satisfied by the design? |
| --- | --- | --- | --- |
| `presentation_projection._one_row` | `tax.us.2025.form1040.line-6b.form-field.json` | exactly one disposition row | **Yes** — one producer only; `test_the_package_declares_exactly_one_producer_of_line6b` |
| `package.core-calculations` entrypoints | `tax.us.2025.rule.ss-benefits-worksheet` | exactly one entrypoint version | **Yes** — package v30 admits exactly one worksheet member and one matching entrypoint |
| `rule.form1040-line9.v7` (`requires`, unconditional) | `tax.us.2025.social-security.line6b` | one published-or-blocked disposition, every path | **Yes** — every compatibility-matrix row yields exactly one worksheet row |

**Cardinality stated explicitly.** `presentation_projection._one_row` admits
exactly one disposition row per form-field-bound symbol; the runner records a
row for **every** rule on **every** path — published, conflict-loser,
false-guard, blocked, and never-eligible. Two producers always yield two rows
in every reachable state; there is no state in which they collapse to one.

**Synthetic end-to-end models, one per materially distinct disposition path.**
The nine rows of `## Compatibility matrix` above, each run through the real
consumer (`live_coordinate_run`) and checked for exactly one worksheet row,
one line-6b row, and a valid `presentation-model.v1` —
`test_every_matrix_row_yields_one_line6b_row_and_a_valid_model`. These are
built models, not argued ones.

**Precedent-sharing check.** The withdrawn two-producer design shared
`rule.schedule-a-total-closed-empty`'s rule shape but not its properties:
`schedule-a.total` is never bound to a form field, so it was never tested
against `_one_row`, and its silence on that property was never permission to
assume the property held for a symbol that *is* form-field-bound.

**Presentation-model probe.** `test_every_matrix_row_yields_one_line6b_row_and_a_valid_model`
builds a real, validated `presentation-model.v1` for every row, satisfying the
requirement that a valid presentation-model probe is part of closure for a
form-field-bound symbol.

**PASS, retroactively** — by evidence already committed under `## Reopened
Track 0 prototype evidence` before this artifact existed, and promoted onto
the published citizen by `tests/test_ssa_no_activity_line6b_track1.py`
(`TestObligation9OneRowAndAValidModel`). No new evidence was required; this
section only restates the existing evidence in the artifact's required shape.

### Declaration

- Authority-lifecycle table: **PASS** — the table above; the retained
  declaration's authority scope is the return, not its `tax-year` key.
- Empty/nonempty authority matrix: **PASS on authority** — all four required
  states plus three, each with an explicitly chosen result; the "nonempty,
  unclosed" row is a change from base and is carried to the stop report.
- Late-member lifecycle: **PASS** — the six-transition trace above, resting on
  `currency.py:127-133,151`, `projection.py:44-56`, and the committed
  `test_live_late_member_stale_closure_and_reclosure`.
- Neighboring capability dependency diff: **FAIL at Track 0 close → RESOLVED by
  owner disposition, not downgraded.** The nonempty worksheet route acquires an
  SSA-closure prerequisite and three provenance pins it does not carry at this
  base. The owner accepted this as a **deliberate semantic correction to the SSA
  worksheet contract**. See "Owner disposition" below for the governing reason,
  which is *not* the `count` limitation.
- Reused-claim semantic/lifecycle equivalence: **PASS** — the worksheet's own
  value under a proved reduction, at 33 → 1. At 33 → 0 this row would be `FAIL`,
  because the zero would then rest on closure of a family narrower than line 6's
  universe, contrary to ADR-0016 decisions 4 and 5.
- Known limitations affecting correctness: **owner disposition recorded as a
  durable enforcement-gap deferral** (see below) — the
  `audit_collect_authority` walker does not cover `count` or `require_closed`
  (T0-1), so the ADR-0016 substitution guard is silent on this shape and on the
  ratified Schedule A precedent; and `rule.form1040-line6a.json` carries the same
  narrow-family-to-Form-1040-line equation with nothing declaring the
  coextensivity. Both recorded, neither repaired here.
- Integration surface: **PASS, retroactively** — artifact 6 above; bindings,
  cardinality, and the nine built end-to-end models. Added 2026-08-13 when
  `PROJECT_PLANNING.md` gained this artifact (PR #175), generalizing this
  milestone's own Track 1 finding; satisfied entirely by evidence already
  committed under `## Reopened Track 0 prototype evidence` before the artifact
  existed — no new evidence was required.

**Gate status: closed by owner disposition, with no unresolved `FAIL`.** The one
`FAIL` artifact and the one known limitation were both put to the owner and both
were dispositioned; neither was downgraded, waived, or reasoned around. The
Track 1 charter may be filed. The dispositions are recorded below and are
binding on Track 1.

## Owner disposition (binding on Track 1)

### Disposition 1 — Stop 2: accept, as a semantic correction

Accepted as a **deliberate semantic correction to the existing SSA worksheet
route**, on this reason:

> For the supported nonempty SSA route, Form 1040 line 6b **must not publish
> until the current SSA source family has been confirmed complete.** Once
> closed, the worksheet value remains unchanged, and its provenance should
> include the closure mapping, the family declaration, and the current closure
> finding.

**The `count` limitation explains why the design takes this shape. It is not the
semantic justification.** Track 1 must not write the implementation constraint
into the record as the reason.

**Scope discipline.** This is an **SSA worksheet contract decision**. It is
**not** a general change to `collect` semantics, and **not** a precedent that
every nonempty family requires closure. Nothing in Track 1 may state or imply
otherwise.

Matrix rows 3 and 4 are amended above. `test_member_present_no_closure_publishes`
is replaced with evidence proving all four of:

1. nonempty but unclosed **blocks** line 6b;
2. closed nonempty **publishes the same value as before**, with the exact
   closure provenance;
3. a late member **invalidates** the prior closure-dependent result;
4. fresh closure **republishes** it.

This disposition does **not** silently resolve the authority-audit finding
below; that finding is retained explicitly.

### Disposition 2 — the `audit_collect_authority` gap: durable deferral

**Do not widen `audit_collect_authority` in this milestone.** Correctly covering
`count` and `require_closed` requires a generic way to represent and validate
explicit coextensive composition. It is not a mechanical extension of the
existing `collect` check, and a naive extension could **incorrectly reject the
ratified Schedule A route**.

Recorded as a **durable enforcement-gap deferral**, not merely an observation in
the Track 0 narrative, scoped to:

- authority-bearing reads through `count` and `require_closed`;
- validation of narrow-family-to-broader-result composition;
- the existing Schedule A precedent;
- the new SSA closed-empty line-6b route.

**Track 1 must nevertheless protect this particular route mechanically**, with
exact structural and behavioural evidence:

- `require_closed` and `count` must reference the **same** SSA family and the
  **current** horizon;
- `count` must inspect the intended **box-5 member type**;
- the retained `no-rrb-or-foreign-social-benefit` declaration must be
  **required and pinned**;
- **mutation of any of those relationships must fail focused tests.**

This disposition accepts a known **generic validator-coverage gap**. It does
**not** declare the gap harmless, does **not** waive ADR-0016, and does **not**
generalize the Schedule A precedent. Revisit it as a separately scoped
validator/composition-contract milestone **after inventorying every current
`count` and `require_closed` authority use.**

## Track 0 stop report

Two stop conditions fired. Both are reported, neither is worked around.

**Stop 1 — "the honest zero requires a declaration beyond the closure and
count" (row 9).** It does:
`tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit`. Recorded in
T0-1 with its reasoning and its Milestone 2 consequence (a **fourteenth**
migration candidate, a source-existence proposition mis-scoped as worksheet
completeness). **Not acted on in this milestone.** The milestone objective —
"without satisfying worksheet-only scope declarations" — is still met exactly,
because the one retained declaration is not worksheet-only; it is the only
committed statement of a source-existence fact.

**Stop 2 — "any existing income route's value or provenance changes."** The
nonempty line-6b route changes in availability (an unclosed nonempty family
blocks instead of publishing, breaking the committed
`test_member_present_no_closure_publishes`) and in provenance (a closed nonempty
family's line-6b finding gains the closure mapping, family declaration, and
closure finding pins). **Values never change.** T0-2 shows the change is forced:
`count` is the only sound empty/nonempty discriminator, it cannot read membership
without reading closure, and without it the two producers are not mutually
exclusive and the published zero's pins become scheduler-order dependent.

The owner's disposition is needed on Stop 2 before Track 1 is chartered. The
options Track 0 can see, without recommending past its authority:

1. **Accept the change.** Amend matrix row 4 to "value unchanged, provenance
   gains the closure triple", amend row 3 to record that it is a deliberate
   correction of base behaviour, and rewrite
   `test_member_present_no_closure_publishes` around the new rule. The nonempty
   worksheet then genuinely stands on the closure it implicitly assumed.
2. **Re-price the split.** Treat the nonempty route's new closure dependence as
   its own decision — it is a claim about what the worksheet means, not about
   how the engine branches — and settle it before or alongside Milestone 2.
3. **Abandon producer exclusivity.** Not viable: the runner has no
   guard-exclusivity validation (`runner.py:520-533`), so a doubly-eligible
   line 6b would publish order-dependent provenance.

No other stop condition fired. In particular: **no generic substrate, no new
schema family, no new evaluator operator, and no kernel change is required** —
every operator the contract needs is committed, and `rule-artifact.v4` already
carries `count`. **No new reusable mechanism was discovered**, so no ADR is owed:
the design is a content instantiation of the ratified
`rule.schedule-a-total-closed-empty` shape. **The committed authority was
sufficient** for every question asked; no bounded authority review is needed and
no PDF was opened.

## Track 1 stop report

Three stop conditions fired. None was worked around. No tax-instruction PDF was
opened, quoted, summarized, staged, or committed.

### The finding, in one sentence

`tax.us.2025.social-security.line6b` is **form-field-bound**, and the
presentation model admits **exactly one disposition row per form-field-bound
symbol** — while a two-producer split produces **two rows in every reachable
state**, because the runner records a disposition for every rule whether it
publishes, is inapplicable, or blocks. The contract Track 0 confirmed therefore
cannot produce a presentation model at all, on any matrix row.

### The mechanism, proved against committed code

1. `packages/derivation/presentation_projection.py:84-89` — `_one_row` raises
   `PresentationModelError` when a symbol's disposition-row count is not
   exactly `1`.
2. `presentation_projection.py:449-451` — it is called for **every** form field,
   keyed on `field["binds_symbol"]`.
   `form1040.line-6b.form-field.json` declares
   `"binds_symbol": "tax.us.2025.social-security.line6b"`.
3. `presentation_projection.py:69-81` — `_dispositions_by_symbol` groups rows by
   the producing rule's `publishes`, so two producers of one symbol always land
   in the same bucket.
4. Every rule always contributes exactly one row, on every path:
   published (`runner.py:1240`), conflict-loser inapplicable
   (`runner.py:522-533` and `1162-1175`), false-guard inapplicable
   (`runner.py:542-550`, `1133-1145`, `1184-1194`), blocked
   (`_record_blocked`, `runner.py:1084-1096`), and — for a rule that never
   became eligible — forced by `finalize_unreached` (`runner.py:1098-1106`).
   **There is no reachable state in which the losing producer is silent.**

### The measurement

The chartered contract was implemented in full and run. Both artifacts are
reproducible byte-for-byte from `tools/generate_ssa_no_activity_content.py`
(committed): a closed-empty producer of `line6b`
(`rule-artifact.v4`, `requires: []`, `pins: []`, `value: 0`, guard
`all[require_closed(ssa1099.benefits), count(box5-net-benefits) == 0,
no-rrb-or-foreign-social-benefit == "yes"]`) and a
`rule.ss-benefits-worksheet` `v2` successor differing from `v1` **only** in the
schema line (`rule-artifact.v3 → v4`) and a leading `count > 0` conjunct, plus
`package.core-calculations` `v30`, `published-packages` `v25`,
`demo.release.2025.v23` and `adopt-core-v30-current.json`.

Run against a live coordinate run on the SSA Track 2 synthetic corpus:

```text
row1 closed-empty, 22 open
PresentationModelError: missing or ambiguous disposition join for symbol
'tax.us.2025.social-security.line6b': 2 row(s)
row1 all 23 present
PresentationModelError: missing or ambiguous disposition join for symbol
'tax.us.2025.social-security.line6b': 2 row(s)
```

The failure is **not** about the 22 open declarations: it is identical with all
23 present.

With `_one_row` relaxed in a throwaway measurement harness — a harness only,
never a proposal — the guards themselves behave exactly as T0-3 predicted:

| Row | closed-empty producer | worksheet `v2` | line 6b presented |
| --- | --- | --- | --- |
| 1 — closed empty, 22 open | `published`, 7 pins | `inapplicable`, `guard_result: false` | `0` |
| 2 — unclosed, empty | `blocked` `SOURCE_SET_UNCLOSED` | `blocked` `DEPENDENCY_ABSENT` (line 6a) | blocked |
| 3 — unclosed, nonempty | `blocked` `SOURCE_SET_UNCLOSED` | `blocked` `SOURCE_SET_UNCLOSED` | blocked |
| 4 — closed nonempty | `inapplicable`, `guard_result: false` | `published`, 52 pins | worksheet result |
| 9 — closed empty, `R` = `no` | `inapplicable`, `guard_result: false` | `inapplicable`, `guard_result: false` | `guard_inapplicable` |

Mutual exclusivity of **publication** holds on every row — no row has two
`published`. Mutual exclusivity of **disposition** does not, and cannot: that is
the defect. Row 1's zero pinned exactly the adoption, both citations, the
current closure finding (`input`), the closure mapping and the family
declaration — and no `ss-benefits-scope` declaration other than
`no-rrb-or-foreign-social-benefit`, no member pin, and no worksheet symbol,
which is what verification item 3 asks for.

### Why Track 0 could not see this on paper

Two reasons, both worth recording so the next paper track checks them.

**The ratified precedent does not carry the property that matters.**
`rule.schedule-a-total-closed-empty` is the shape T0-2 confirmed, and it is
sound — but `tax.us.2025.schedule-a.total` has **no form field**, so `_one_row`
is never called for it. The same pattern was already tried and rejected for a
form-field-bound symbol on the ratified line: the Form 1098 Track 2 generator
records that a second producer for `tax.us.2025.deductions.line-12e` "was tried
and rejected: presentation_projection's `_one_row` join requires exactly one
disposition row per symbol for a form-field-bound symbol, which the
two-disjoint-producer pattern used above for `tax.us.2025.schedule-a.total` —
never form-field-bound — does not have to satisfy"
(`tools/generate_f1098_line12e_t2_content.py`). T0-3 did examine the
presentation layer, but only `_classify_numeric`'s label; it did not examine the
join.

**One T0-2 claim is wrong for the live path, and should be corrected in place.**
T0-2 states that `requires` is tested before the guard "in both schedulers".
That is true of `attempt` (`runner.py:515-539`) but **false of the live
marshalled scheduler**, which preflights the guard first and treats a provably
false guard as an atomic `inapplicable` "even when later numeric dependencies
are absent" (`runner.py:1126-1160`). This does not rescue a single-rule design —
a rule still cannot *publish* while skipping its `requires` — so T0-2's
conclusion that two producers are necessary survives. But the reasoning behind
it should not be relied on as written.

### Stop conditions fired

**Stop 1 — "any matrix row cannot be satisfied by the confirmed contract."**
Fired, in its strongest form: **no** row can be satisfied. Not a row-specific
gap, a whole-contract obstruction.

**Stop 2 — "generic substrate turns out to be required."** Fired. Making the
contract work requires a change to `packages/derivation/presentation_projection.py`
so a form-field-bound symbol with several mutually exclusive producers joins to
one row. The allowed-impact envelope (T0-4) forbids exactly this: "every
evaluator, runner, currency, and projection module … **No kernel or engine code
changes at all.**"

**Stop 3 — "a new reusable mechanism appears."** Fired. Either candidate
resolution is a reusable mechanism needing an ADR, not silent adoption:

- *Multi-producer form-field-bound symbols.* A presentation-layer contract
  saying which of several rows is the field's row, and on what authority the
  others are suppressed. This is a governance question, not a tidy-up: today the
  one-row rule is what guarantees a form line has exactly one explanation, and
  the corpus already has a same-symbol multi-producer allowlist
  (`conflict_semantics`) that the presentation layer does not consult.
- *A single-producer conditional-dependency design.* One rule whose `requires`
  no longer names the 23 declarations, with them moved into a
  `conditional_dependency_set` (ADR-0037) conditioned on `count > 0` and a
  value-level `choose` between `0` and the worksheet expression. It is
  expressible in committed content and `rule-artifact.v4` grammar, and it
  sidesteps the join entirely — but it changes what `requires` means for this
  corpus's canonical-zero pattern, it **changes the worksheet's value
  expression** (which the Track 1 charter forbids), and Track 0 explicitly
  rejected the value-level `choose` shape. **Sketched here for the owner's
  disposition; deliberately not implemented.**

### Stop conditions that did **not** fire

- **Row 1 did not require any of the 22.** The row-1 fixture was built with the
  22 worksheet-only declarations genuinely absent, and the closed-empty producer
  published `0` without reading or pinning any of them. The repair's central
  claim is sound; only its packaging is not.
- **No income route's value changed.** No successor package was committed, and
  on the measured rows the worksheet's own value was unchanged.
- **No new schema family and no new evaluator operator was needed.** Every
  operator the contract uses is committed, and `rule-artifact.v4` already
  carries `count`.
- **The committed authority was sufficient.** No bounded authority review is
  needed.

### What is committed, and what is deliberately not

**Committed:** `tools/generate_ssa_no_activity_content.py` — the chartered
contract implemented in full and deterministically reproducible — and this
report.

**Deliberately not committed:** `rule.ss-benefits-line6b-closed-empty.json`,
`rule.ss-benefits-worksheet.v2.json`, `package.core-calculations.v30.json`,
`published-packages.v25.json`, `demo.release.2025.v23.json` and
`adopt-core-v30-current.json`. Committing them would burn a published package
version, a published registry version and a release version on a package that
cannot produce a presentation model, and would leave a permanently red artifact
set on the branch. `python3 tools/generate_ssa_no_activity_content.py`
regenerates all six byte-for-byte for anyone who wants to re-run the
measurement.

## Track 0 settlement — final contract

The contract Track 1 built and shipped. Stated once, in its final form. The
superseded two-producer settlement and the refuted dependency table are
preserved in `## Track 1 stop report` below, as genuine design history — a
real alternative was chartered, built, and empirically shown unbuildable
against the one-row invariant, and that evidence remains load-bearing for why
this contract has one producer. They are deliberately not restated here,
because a contract a reader has to reconstruct from a sequence of design
attempts is not a contract.

This branch was curated before closeout: an earlier iteration produced this
same content through a chain of documentation-only successor versions
(worksheet `v2` with a miscounted dependency-set comment, corrected as `v3`,
which itself then misdescribed a downstream rule's `requires` and was
corrected again as `v4`), none of which was ever merged or ratified. Since
Article 9 immutability binds published history on the ratified line and not
commits on an open draft branch, that chain was collapsed: the worksheet
ships directly as `v2` — the lowest version free on the ratified line — with
the final, correct notes from the start. No `v3` or `v4` of this citizen
exists on this branch.

**One rule, one producer.** `tax.us.2025.rule.ss-benefits-worksheet` v2 under
`rule-artifact.v4` is the sole producer of
`tax.us.2025.social-security.line6b` corpus-wide. There is no second citizen for
this symbol on any path, because the symbol is form-field-bound and
`presentation_projection._one_row` admits exactly one disposition row.

### `requires` — 11 symbols, unconditional

```json
["tax.us.2025.ss-benefits-scope.no-rrb-or-foreign-social-benefit",
 "tax.us.2025.wages.total-w2-box1",
 "tax.us.2025.interest.taxable-total",
 "tax.us.2025.dividends.ordinary-total",
 "tax.us.2025.ira.distributions.line4b",
 "tax.us.2025.capital-gains.line7a-total",
 "tax.us.2025.income.additional-income",
 "tax.us.2025.tax-exempt-interest.line2a-total",
 "tax.us.2025.social-security.line6a",
 "filing_status",
 "rounding.convention"]
```

Down from **33**. The reduction is 33 → 1 in the scope vocabulary: exactly one
`ss-benefits-scope` declaration remains unconditional.

Three groups, each unconditional for a distinct reason:

* **`no-rrb-or-foreign-social-benefit`** — the source-universe authority. The
  SSA family's closure claim disclaims RRB-1099, SSA-1042S and foreign systems,
  so this is the return's only committed statement that Form 1040 line 6's
  universe and this narrow family coincide. Without it the zero would
  substitute a narrow family's closure for a broader line's authority.
* **The seven derived numeric inputs** — a *sequencing* requirement, not a claim
  the empty route reads them. `requires` is the engine's only sequencing gate;
  conditional-set membership is invisible to eligibility and a blocked rule
  resolves permanently, so conditionalizing them makes the rule eligible before
  its inputs publish. It costs a wageless return almost nothing: each is itself
  an unconditional total rule publishing zero over an empty closed family, and
  six of the seven are already required unconditionally by `rule.form1040-line9`
  to reach total income. The seventh, `tax-exempt-interest.line2a-total`, is
  not — line 2a is informational, not part of total income — so requiring it
  here does pull in `rule.form1040-line2a`'s eight `line2a-scope.*`
  declarations for a return that would otherwise skip them (measured: dropping
  those eight facts from a closed-empty run blocks this rule on
  `DEPENDENCY_ABSENT` naming `tax-exempt-interest.line2a-total`). That cost is
  pre-existing, not introduced by this rule: v1 of this worksheet already
  required `tax-exempt-interest.line2a-total` among its 33 `requires`.
* **`filing_status`** — a contract requirement. ADR-0038 production condition 1,
  enforced by `package_validation` check 10a, forbids a conditional member whose
  fact type the same rule names in a `category_literal` unless that fact type
  declares the `{yes, no}` domain; `tax.us.2025.filing-status` declares five.
  `rounding.convention` and `social-security.line6a` are ordinary v1 carry-overs.

### Guard — `all` of four conjuncts

| # | Conjunct | Active on |
| --- | --- | --- |
| 1 | `require_closed(tax.us.2025.ssa1099.benefits)` | **both routes** |
| 2 | `conditional_dependency_set`, condition `count(box5-net-benefits) > 0`, **22 members** | nonempty only |
| 3 | `categorical_compare(no-rrb-or-foreign-social-benefit == "yes")` | **both routes** |
| 4 | `any[ count == 0, all[22 conjuncts, MFS set] ]` | short-circuits when empty |

Conjunct 1 is unconditional for a **semantic** reason: the worksheet computes
the taxable portion of the benefits actually recorded, so a return whose benefit
set is not yet closed has no line 6b answer to give, empty or otherwise. The
`count` implementation's closure read explains why this shape is available; it
is **not** the justification. This is a decision about what this worksheet
means, scoped to this route — not a change to `collect` semantics, and not a
statement that any other nonempty family requires closure.

### Conditional dependency set — 22 members, and only 22

The 22 `ss-benefits-scope` declarations other than
`no-rrb-or-foreign-social-benefit`. They are worksheet-internal: at line 6a = 0
the worksheet's value reduces to zero for every filing status and every income
vector, so they cannot change the answer and must not gate it. Under ADR-0037
the set both activates them when `count > 0` and reports the complete missing
list in one walk.

The seven numeric inputs are **not** members. That is the single most
load-bearing fact about this contract and the one a future edit is most likely
to get wrong; it is held by
`test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route` on the
published citizen.

### Value branch

```json
{"op": "choose",
 "when": {"op": "compare", "cmp": "eq", "right": 0,
          "left": {"op": "count",
                   "name": "tax.us.2025.ssa1099.box5-net-benefits",
                   "source_set": "tax.us.2025.ssa1099.benefits"}},
 "then": 0,
 "else": "<the v1 worksheet expression, byte-identical>"}
```

`choose` is lazy in the committed evaluator, so the closed-empty route never
reads an income symbol, a parameter, or `round`. On the nonempty route the
expression, pin table, citations and 22 conjuncts are exactly v1's, so the
published worksheet **value is unchanged**; its provenance additionally pins the
closure mapping, the family declaration and the current closure finding.

On the empty route the zero's authority is the closure attestation taken
together with zero current members — never mere emptiness — plus the retained
declaration. The zero-member component has no finding of its own; it is carried
by the absence of any member pin together with the pinned version of this rule,
whose value branch demands `count == 0`.

### ADR posture

**No ADR is owed.** `rule-artifact.v4`, `conditional_dependency_set`, `choose`,
`count` and `require_closed` are all ratified; this is a new content composition
of them, not a new reusable engine mechanism.

## Reopened Track 0 evidence, promoted directly onto the published citizen

The corrected single-producer settlement — the seven derived numeric inputs
stay unconditional — was proven against ten obligations before being built as
the published contract: closed-empty publishes zero with the 22 genuinely
absent; the zero pins exactly closure, family, mapping, adoption, citations,
and the retained declaration; closed-nonempty equals the ratified numeric
result on both routes, neither expression inspected; nonempty pins every
active worksheet dependency and the closure triple; missing nonempty
dependencies produce the complete ADR-0037 list in one walk; unclosed empty
and unclosed nonempty each block honestly; the retained declaration's
negative cannot take the zero branch; late membership displaces and reclosure
recomputes; every matrix row yields exactly one line-6b disposition row and a
valid `presentation-model.v1`; and mutating the family, member predicate,
closure relation, retained declaration, conditional condition, or value
branch each fails a focused test.

There is no separate prototype harness: all ten obligations, the nine
compatibility-matrix rows, and the six mutation kill-tests are the permanent
suite itself, `tests/test_ssa_no_activity_line6b_track1.py`, run against the
real published surface — see `### Verification results — Track 1′` below for
measured numbers. A temporary-surface prototype existed earlier in
development and was removed once its evidence was fully subsumed by the
permanent suite; no ADR depends on it, so it did not meet this project's
durability bar for prototype evidence.

`test_the_closure_relation_is_carried_by_count_not_by_require_closed` records
that the closure relation travels via `count`, not `require_closed` — the
relationship the final contract's guard ordering depends on.

**No ADR is owed.** The proof succeeded on existing `rule-artifact.v4`,
`conditional_dependency_set`, `choose`, `count`, and `require_closed`
semantics; this is a content composition of ratified mechanisms, not a new
reusable engine mechanism.

## Amended Track 1 charter

Supersedes the stopped Track 1. Written against measured evidence, not paper:
the contract is the one proved in `## Reopened Track 0 prototype evidence`, as
corrected there.

### What to build

**One successor rule, the sole producer of
`tax.us.2025.social-security.line6b`**, plus the additive package, registry, and
release successors and the adoption fixture.

| Class | Members |
| --- | --- |
| **Unconditional `requires`** | SSA family closure; `social-security.line6a`; `rounding.convention`; `ss-benefits-scope.no-rrb-or-foreign-social-benefit`; **the seven derived numeric inputs** |
| **`conditional_dependency_set` (ADR-0037), active on `count > 0`** | the **22** worksheet-only `ss-benefits-scope` declarations — and nothing else |

The numeric inputs are unconditional **because it is measured that they must
be**: `requires` alone sequences them, so a conditional numeric input makes the
worksheet fire before its inputs publish. Do not re-litigate this; it is
measured, and `test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route`
keeps it honest.

A declared value-level `choose` selects canonical `0` or the **unchanged**
worksheet expression. The nonempty arithmetic is preserved exactly.

### Binding constraints

- **The presentation join is not to be touched.** Do not broaden
  `presentation_projection._one_row` or relax the one-disposition-row invariant
  by any route.
- **Do not widen `audit_collect_authority`** (standing owner Disposition 2 — the
  enforcement gap is a recorded durable deferral).
- **Do not edit published citizens in place.** Additive successors only.
- The closure relation travels via **`count`**, not `require_closed`. Preserve
  that and keep its kill-test.
- Closure is required on **both** routes for the semantic reason — line 6b must
  not publish until the current SSA source family is confirmed complete. The
  `count` limitation is **not** the justification and must not be written as one.
- Scope discipline: this is an **SSA worksheet contract decision**, not a change
  to `collect` semantics and not a precedent that every nonempty family requires
  closure.

### Carry forward from the prototype

Promote the prototype's coverage into the permanent suite, against the real
published surface rather than a temporary one: all ten obligations, the nine
matrix rows with their one-row/valid-model assertions, and **all six mutation
kill-tests**. Add the four-part replacement evidence for
`test_member_present_no_closure_publishes` that the stopped Track 1 never wrote:
nonempty-unclosed blocks; closed-nonempty publishes the same value with the
closure provenance; a late member invalidates; fresh closure republishes.

### Now permitted

Publishing the package, registry, and release successor versions — the
candidate has produced a valid derivation **and** presentation model across the
matrix, which was the standing condition.

### Verification

Full suite, mypy, governance lint, envelope scan. Then **independent review of
both derivation behaviour and presentation projection**, per the owner's
instruction.

### Stop conditions

Unchanged and narrow: stop only if the single rule cannot express the required
branch-specific pins or explanations, changes the established nonempty worksheet
**value**, or requires engine or schema behaviour beyond existing contracts.

## Independent review

Dispatched as a reviewer seat against the shipped single-producer worksheet
citizen, its publication chain (package, registry, release, adoption), and
the permanent Track 1 suite, with derivation behaviour and presentation
projection reviewed separately as the owner required.

**Verdict: APPROVE WITH FINDINGS.** Derivation behaviour **PASS**, presentation
projection **PASS**, all six owner constraints **PASS**. Measured: 1261 passed,
20 skipped, 3933 subtests (341.18s); `mypy` clean over 191 source files;
governance lint conformant; envelope scan clean. The reviewer independently
recomputed the whole checksum chain — package instance, release bytes, registry
bytes, adoption fixture — rather than assuming it, and read the `MutantSurface`
harness to confirm the kill tests re-seal and re-execute against the real
resolver rather than stubbing it.

Two findings, both low severity, both now closed.

### Finding 1 — the bundle bump's scope was verified nowhere durable

The publish commit message names `ss-benefits-scope.bundle.v2` only inside the
"no new schema family" sentence, and never states what changed. A later reader
had to redo a 23-way JSON diff to confirm the bump is not fact-type succession.
Recorded here so the claim is checkable without repeating that work.

Verified field-by-field across **all 23** `tax.us.2025.ss-benefits-scope.*` fact
types, twice and independently (foreman, then reviewer):

| Field | v1 → v2 |
| --- | --- |
| `version` | `1` → `2` — the only intended change |
| `value_schema` | `{enum: [yes, no], type: string}` → `{enum: [yes, no]}` |
| `identity_keys` | **unchanged** |
| `nature` | **unchanged** |
| `supersession` | **unchanged** |
| `title`, `schema` | **unchanged** |

Because `identity_keys`, `nature` and `supersession` are untouched, this was a
version bump and **not** fact-type succession — the milestone's non-goal held.

**Superseded.** A later architectural review found check 10a's exact-shape
requirement was itself the defect: it mistook one spelling of the {yes, no}
domain for the domain's identity, forcing a needless successor and — because
the worksheet's own `category_literal` pins were never repointed to it —
leaving 24 exact pins across the corpus (this worksheet's 23, plus
`rule.form1040-line6c`) silently validating against a version the package no
longer selected. `package_validation` check 10a now recognizes
`{"type": "string", "enum": ["yes", "no"]}` as equivalent to
`{"enum": ["yes", "no"]}`, and `ss-benefits-scope.bundle` was withdrawn back
to its base `v1` — no successor exists. **Coordination item for Milestone 2
is retracted**: its predecessor population is `ss-benefits-scope` **v1**, as
it always was on the ratified line.

### Finding 2 — the numeric-inputs guard did not reach the shipped citizen

The rule that the seven derived numeric inputs must stay in the unconditional
`requires` was proved on a synthetic surface during earlier development. That
was enough to correct the design, but nothing on the real published artifact
would have caught a later edit repeating the mistake — `TestObligation10Mutations`
had six kill tests and none covered it.

Closed by a **seventh** kill test,
`test_conditionalizing_the_numeric_inputs_breaks_the_nonempty_route`, which
moves the seven out of `requires` and into the `conditional_dependency_set` on
the real citizen through `MutantSurface`. Measured outcome, asserted positively
rather than under an `if refusal is None` guard so it cannot pass vacuously:

* disposition `blocked`, code `DEPENDENCY_ABSENT`, against an unmutated run
  measured in the same test as publishing `10200`;
* `missing` names **only two** of the seven —
  `capital-gains.line7a-total` and `income.additional-income` — because the
  other five had already published by the pass on which the worksheet first
  became eligible.

That partial missing list is the substantive discovery. The defect presents as a
**scheduling race**, not as all seven disappearing at once, so in the field it
would read like an unrelated fixture gap rather than a dependency-declaration
error. `_Run.is_eligible` consults `rule["requires"]` alone —
`conditional_dependency_set` membership is invisible to eligibility sequencing —
and `_record_blocked` resolves the rule permanently, so the worksheet never gets
a second pass.

### Residual gap raised by the reviewer, closed by the foreman

The reviewer could not confirm that `rule-artifact.v3` → `v4` is a strictly
additive grammar extension, having inferred it only indirectly. Verified
directly: a normalised diff of the two schema files removes exactly **two**
lines, `$id` and the `schema` `const`, and adds the `count` and `block` operator
branches. Nothing is removed or narrowed. Both schema files predate this
milestone and are untouched by it (`packages/schemas/` carries no diff
against the ratified line), so the milestone consumes a ratified grammar
rather than extending one.
