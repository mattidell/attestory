<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Engine Breadth",
  "topic": "ssa-no-activity-applicability",
  "milestone_state": "track-0",
  "status": "Track 0 (paper). Milestone 1 of the owner-approved two-milestone split; Milestone 2 (fact-type-succession-neutral-schedule1) is chartered only after this merges, on its own branch and PR. OBJECTIVE: a return with no applicable Social Security source publishes the legally authorized line-6 zero and proceeds through line 9 without satisfying worksheet-only scope declarations. THE DEFECT: rule.ss-benefits-worksheet.json is the ONLY producer of social-security.line6b corpus-wide and carries 33 requires; rule.form1040-line9.v7 requires line6b unconditionally; so every return in the engine must satisfy 33 Social Security declarations to reach total income. That existing burden is NOT a precedent. Line 6a is already correct on an empty family. THE NO-ACTIVITY AUTHORITY is not a default and not mere emptiness: it is current tax.us.2025.ssa1099.source-closure v1 (the closure claim declared verbatim in family.ssa1099-benefits.json) TAKEN WITH zero current box5-net-benefits members; both must appear in the zero's provenance. SHARPEST OPEN QUESTION (T0-1): the closure claim's own text disclaims RRB-1099, SSA-1042S and foreign systems, and ss-benefits-scope.no-rrb-or-foreign-social-benefit asserts exactly that absence -- a source-existence proposition wearing worksheet-completeness wording. So the honest reduction may be 33->0 or only 33->1; Track 0 must decide and say why, because a zero that silently ignores a disclaimed neighbouring class is a default wearing the clothes of an authority. If that declaration is load-bearing it is a FOURTEENTH migration candidate for Milestone 2, not a thirteenth Schedule 1 absence -- Milestone 1 records it and does not act on it. ENTERING CONTRACT (Track 0 confirms): copy the ratified rule.schedule-a-total-closed-empty shape -- a new closed-empty producer of line6b with requires:[] pins:[] value:0 guarded on all(require_closed, count==0), plus a successor worksheet version gaining the mutually exclusive count>0 conjunct. requires is checked BEFORE evaluation (runner.py:482), so a single rule carrying the 33 could never skip them by guard however written. Expected content-level, no new schema family, NO ADR unless Track 0 finds a new reusable mechanism (itself a stop). AUTHORITY BOUNDARY: no seat reads tax-instruction PDFs; inadequate authority is a stop requiring a bounded authority review. Stop and re-price the split if generic substrate turns out to be required.",
  "current_role": "Foreman (Track 0 closed by owner disposition; Track 1 charter to be filed)",
  "current_prompt": "docs/phases/engine-breadth/milestones/ssa-no-activity-applicability.md#Owner disposition (binding on Track 1)",
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
**Base:** `origin/main` @ `f60e7d1`
**State:** Track 0 complete (paper). No implementation chartered — the
adversarial-closure gate does not close and two stop conditions are reported;
see `## Track 0 stop report`.

Milestone 1 of the two-milestone split recorded in
`fact-type-succession-ssa-applicability.md`. Milestone 2 (fact-type succession
with the thirteen neutral Schedule 1 propositions) is chartered only after this
merges, on its own branch and PR. **This milestone does not share a PR with
Milestone 2 and does not wait on its prototype and ADR cycle.**

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

The entering contract survives in shape. It does not survive unchanged.

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
| 1 | Implement the closed-empty producer and the successor worksheet guard, with fixtures and regressions, under the two binding owner dispositions | **Chartered** |

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

Required whenever Track 0 plans a producer or successor producer of an
externally bound symbol (`PROJECT_PLANNING.md`, "Track 0 Adversarial Closure
Gate", artifact 6). `tax.us.2025.social-security.line6b` is form-field-bound,
so this artifact applies.

Binding enumeration and cardinality are stateable on paper:
`presentation_projection._one_row` admits exactly one disposition row per
form-field-bound symbol; the runner records a row for every rule on every
path (published, conflict-loser, false-guard, blocked, never-eligible). But
the artifact also requires "one synthetic end-to-end model for every
materially distinct disposition path, exercised through the real consumer" —
built evidence, not argued evidence, which this paper-first Track 0 does not
yet have.

**PENDING.** Discharged in Track 1 once the contract is implemented and run
through `live_coordinate_run` for every compatibility-matrix row. Track 0
does not close this artifact on paper; it only establishes that the design
must be checked against it before the implementation charter is trusted.

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
- Integration surface: **PENDING** — see artifact 6 above; requires Track 1's
  built end-to-end models, not yet available on paper.

**Gate status: closed by owner disposition, with no unresolved `FAIL`; one
artifact `PENDING` on built evidence.** The one `FAIL` artifact and the one
known limitation were both put to the owner and both were dispositioned;
neither was downgraded, waived, or reasoned around. The integration-surface
artifact cannot close on paper and is carried into Track 1 as a binding
obligation, not a waiver. The Track 1 charter may be filed. The dispositions
are recorded below and are binding on Track 1.

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
