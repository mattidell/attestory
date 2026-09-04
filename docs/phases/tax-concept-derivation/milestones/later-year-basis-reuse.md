<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "later-year-basis-reuse",
  "milestone_state": "planned",
  "status": "Planned. Track 0 has not started. The plan charters a later-year basis reuse test: whether a basis consequence established in an earlier tax context can be found, associated with the same investment, corrected, explained, and consumed when adjusted basis actually affects a later calculation. Two experimental dimensions are held separate -- access experiments (AS-1 retrieval, AS-2 re-execution) and representation strategy (aggregate A vs durable components B) -- and are not rival product architectures the owner must pick between. Owner-facing decisions named in advance as four separate items: the cross-scope consumption contract; consumption policy and the distinct historical-retention question; authorship of the broker-versus-derived comparison claim; and whether a collect-target universe guard defect, if found, is repaired.",
  "scope": [
    "model one later disposition of the same synthetic interest-bearing obligation used by the accrued-interest work, and determine what a later calculation must know about adjusted basis",
    "establish, by execution against a production-shaped fixture rather than by code reading, what the committed engine can and cannot do when a run scoped to a later reporting year needs a determination established in an earlier one",
    "identify the smallest honest executable surface that tests cross-year reuse, distinguishing a disposable evidence-only consumer from a source-independent calculation and from production tax-year content, and surface rather than invent any boundary that would require production 2026 content",
    "exercise positive, missing-input, conflicting-report, broker-agreement, correction, stale-history, and no-broker-report cases (S1-S7) against every adjusted-basis representation still viable, at the cheapest evidence rung that can expose a difference",
    "run one narrow, disposable persisted-boundary experiment using committed test machinery (append_publications, workspace_currency, and the real projection/marshalling boundary, against a manual-injection negative control) to distinguish genuine workspace reuse from an in-memory value-passing demonstration",
    "hold two experimental dimensions separate - access strategy (how a later calculation obtains the earlier consequence) and representation strategy (aggregate A vs durable components B) - and, if the committed boundary does not expose the earlier derived publication, run two falsifiable experiments as bounded continuations of the one authorized persisted-boundary experiment on the one temporary act log: AS-1 (C14) retrieving the earlier derived publication, and AS-2 (C15) obtaining the acquisition and report findings from the real kernel projection/marshalling boundary over the authoritative acts and re-executing association, supportability, and consequence production from them under an explicit 2025 rule/package/reporting-year context, with a negative control showing that association under the later reporting year does not silently associate the 2025 report; the association, verdict, and consequence are re-derived, never retrieved or injected (ADR-0068 Decision 7); each reporting identity, currentness, governing version, provenance, historical-vs-newly-derived character, and the exact failure point",
    "decide whether A and B produce any material observable difference - favouring either, or exposing a tradeoff - holding the access strategy, projected source facts and currentness state, scenario, and consumer purpose/output contract constant while permitting only the composition each shape inherently needs, and running under each materially distinct viable access strategy or deferring C12 until the access meaning is selected; defer the representation choice again rather than selecting by taste if no difference appears, and treat an access failure affecting both shapes as an access finding, never evidence of behavioral equivalence",
    "state which of the four earlier composition gaps must close for a production vertical and which remain unrelated"
  ],
  "non_goals": [
    "no 2026 federal content package, 2026 forms, or 2026 return implementation; if production 2026 content would be required to make a claim honest, that boundary is surfaced to the owner, not invented",
    "no Form 8949 or Schedule D production vertical, and no reopening of whether documentary and ordinary facts need a shared source-independent model",
    "no general basis ledger, no production persistence caller, and no new storage; the authorized persisted-boundary experiment is disposable test-local evidence using primitives committed tests already exercise, and changes nothing under packages/",
    "no OID, bond-premium, market-discount, lot-allocation, or non-purchase-origin implementation; these remain the earlier milestone's recorded reopening triggers",
    "no successor ADR correcting another ADR authored within this same milestone",
    "no treatment of the ADR-0071 accrued-interest consequence as the complete basis concept merely because it is the one committed exhibit"
  ],
  "deep_reads": {
    "implementation": [
      "docs/domain-models/investment-basis.md",
      "docs/domain-models/investment-basis-coverage.md#What the application does today",
      "docs/domain-models/investment-basis-coverage.md#Representing adjusted basis",
      "docs/domain-models/investment-basis-coverage.md#Where this leaves the basis concept",
      "docs/milestone-retrospectives/2026-09-02-investment-basis-concept-coverage.md",
      "docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md#Track 0 sections and their abstracts",
      "docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md#Claim and verification architecture",
      "docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md#The smallest honest executable surface",
      "PROJECT_PLANNING.md#Frontier Reduction and Direct-Build Routing",
      "PROJECT_PLANNING.md#Prototype Economic Gates",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "docs/adr/0071-rule-owned-current-year-and-basis-consequences.md",
      "docs/domain-models/taxable-interest-translation.md#Cross-year handling: three distinct years, never conflated",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "docs/domain-models/investment-basis-coverage.md#Representing adjusted basis",
      "docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md#Claim and verification architecture",
      "docs/phases/tax-concept-derivation/milestones/later-year-basis-reuse.md#Exit criteria",
      "PROJECT_PLANNING.md#Frontier Reduction and Direct-Build Routing",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  }
}
-->

# Later-Year Basis Reuse Test

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `later-year-basis-reuse`
- Branch: `milestone/later-year-basis-reuse-test` (the branch name carries a
  `-test` suffix the milestone key does not; the key above is authoritative
  for ledger and phase-state records)
- State: planned. Track 0 has not started.
- Execution posture: iterative construction in four passes, executed evidence
  before architectural conclusion, disposable consumer before production
  content

## Objective

Determine whether a basis consequence established in an earlier tax context
can be **found, associated with the same investment, corrected, explained, and
consumed** when adjusted basis actually affects a later calculation.

The milestone is **not** justified by demonstrating that a value can be passed
between two rules. That is a triviality the existing evaluator already
supports. It is justified only if it establishes:

- what the later calculation needs to know;
- how it knows the determination concerns the same investment;
- which earlier determinations remain current;
- how later documentary basis information is *reconciled* rather than
  substituted for canonical history; and
- what provenance explains the result to a reader.

## Why this milestone, now

The Investment Basis Concept and Coverage Model closed on 2026-09-02 as an
explicit partial result. It deferred the adjusted-basis representation choice
under `PROJECT_PLANNING.md`'s Frontier Reduction and Direct-Build Routing
table, fourth row, and recorded the missing discriminator exactly: **a
consumer that must actually read a composed adjusted basis.**

A later-year disposition is where such a consumer first appears. This
milestone is therefore the first legitimate opportunity to test whether the
deferred representations differ in observable behavior. Testing them here may
discriminate the candidates or may show no material difference. **Neither
outcome is assumed, and neither is required for the milestone to succeed.**

## Current state, preserved accurately

This section restates the prior milestone's result. It is load-bearing and
must not be softened, strengthened, or paraphrased into something stronger.

**Established.** The basis lifecycle and representative coverage (RC1–RC8) are
modeled in `docs/domain-models/investment-basis.md` and
`docs/domain-models/investment-basis-coverage.md`: origin, adjusting events,
allocation, reconciliation, and an as-of projection, with evidence, ordinary
circumstance, tax determination, adjusted basis, calculation consumption, and
presentation kept as six distinct layers.

**Undecided.** Durable components (B) versus a single published aggregate (A)
remains undecided **because the prior milestone had no consumer that behaved
differently.** Real differences survive — per-authority attribution,
displacement granularity, independent supersession — but none was load-bearing
for any named consumer. C (hybrid) was recorded as an implementation option
within B, not a third rival.

**Four concrete composition gaps remain:**

1. No `purchase_price` / `acquisition_costs` vocabulary, so a cost origin's
   inputs cannot be attested against current content.
2. No acquisition-keyed basis-origin producer.
3. No content-declared per-acquisition publication path; the pairing-scoped
   dispatch that exists is intercepted for named rule ids.
4. No declared traversal from the acquisition, through the association, to the
   pairing-scoped consequence — which is keyed by a derived pairing finding
   id, not by the acquisition fact id.

**Neither proved.** None of the four gaps has been proved to require a new
foundational kind. None has been proved solvable by committed machinery. Both
statements must remain true in this milestone's language unless it produces
evidence that changes one.

**Method constraint carried forward.** Runtime behavior must be reproduced
with a production-shaped fixture before it drives an architectural conclusion.
The prior milestone twice reached an architectural conclusion from code
reading that a single fixture run disproved. `tests/test_integration_checkpoint.py`
runs 18 tests in about 2.5 seconds; there is no economic excuse for inferring
where executing is available.

## Pass 1 — Plain-language outline

### The user situation

A person buys an interest-bearing obligation partway through an interest
period. Because the seller earned part of the current period's interest, the
buyer pays that accrued portion to the seller at settlement. When the payer
later pays the full period's interest to the buyer of record, part of what the
buyer receives is not income at all — it is the buyer's own money coming back.
That return of capital reduces what the buyer has invested in the bond.

Years later, the person sells the bond. To report that sale the product must
compute gain or loss, which requires knowing what the bond's basis had become
by then. The earlier reduction is part of that answer.

### The earlier event and the later event

- **Earlier (2025).** `demo-bond-c` is acquired; accrued interest of $150 is
  paid to `demo.seller`; a Form 1099-INT reports the full period's interest;
  the acquisition and report associate; a supportability verdict passes; and
  the committed rule
  `tax.us.2025.rule.basis.item-level-consequence.pairing-scoped` publishes the
  $150 item-level basis consequence. **This milestone supplies and executes
  the $150 case itself.** The committed fixture demonstrates *parameterized*
  publication at `42.0`; it does not already prove this exact execution, so
  the figure is run here rather than assumed.
- **Later.** The same obligation is disposed of. A calculation must produce a
  gain or loss.

### "Later year" names three things, which must not be conflated

`docs/domain-models/taxable-interest-translation.md`, "Cross-year handling:
three distinct years, never conflated," already establishes that the **event
year** (when the person bought the bond), the **reporting year** (what the
payer's document covers, supplied by the run's own scope), and the
**tax-consequence year** (the return year the adjustment lands on) are usually
the same but are not guaranteed to be.

A milestone named "later-year basis reuse" is exactly where those three can be
silently collapsed into one. Track 0 must say, for every claim it makes, *which*
of the three years it means. The disposition introduces a fourth — the
**disposition year** — and whether that is the same as the consuming run's
reporting year is itself a question, not an assumption.

That section also records the mechanism that keeps them honest: a run scoped to
year N+1 narrows candidate reports to N+1 reports, and a confirmation recorded
against one report never authorizes association against a different report or
reporting year. This milestone relies on that behavior and does not reopen it.

### The result the later consumer is trying to produce

Gain or loss on disposition: proceeds minus adjusted basis. Using the prior
milestone's synthetic figures — a $10,000 total purchase price paid to the
seller at settlement, **which already includes the $150 accrued-interest
component**, plus a $40 commission, giving a $10,040 cost origin, reduced by
the $150 consequence to a $9,890 adjusted basis — a $10,200 disposition yields
a **$310 gain**.

**This reading is the one that governs, stated here because the figures are
otherwise ambiguous.** The $150 is counted *into* the cost origin exactly once
and removed from it exactly once — it is never both included in the $10,000 and
added on top of it.

### Why the earlier basis consequence matters

If the later calculation cannot reach the earlier determination it uses
$10,040 and reports a **$160 gain**, understating the gain by exactly the
$150 accrued-interest amount. The number on the return is wrong, and — worse
for this product's thesis — the person cannot see why, because nothing in the
result names the determination that was missed.

The alternative failure is quieter and is the one the product must actually
guard against: the calculation silently uses a broker's reported basis figure,
which may or may not already reflect the same adjustment. Substituting a
documentary figure for canonical history is not reuse; it is abandonment of
the derivation, and it can double-count or omit without any signal.

### What would be wrong or unexplained if reuse failed

- The gain is wrong by a determinable amount.
- No refusal, no coverage statement, and no explanation names the gap.
- A correction to the 2025 acquisition would not reach the later result.
- The product would be unable to distinguish "no adjustment applies" from
  "an adjustment applies and I could not find it."

That last distinction is the product-level point of the whole milestone.

### Bounded scenario

One synthetic obligation, one taxpayer, one earlier acquisition with one
accrued-interest consequence, one later disposition. `demo.*` identities and
synthetic amounts throughout. No second lot, no OID, no premium, no
partial disposition, no joint return.

### Explicit non-goals

As recorded in this plan's metadata: no 2026 package or forms, no Form
8949/Schedule D vertical, no general basis ledger, no invented persistence
machinery, no OID/premium/allocation/non-purchase-origin implementation.

### The smallest owner-facing decisions this work might expose

Named in advance so they are recognized rather than absorbed. They are
separate items; retrieval-versus-re-execution is not a forced choice of
rival product architectures.

- whether a run may consume a determination scoped to a different tax year at
  all, and under what contract (the cross-scope consumption contract);
- what determination a later calculation may consume — the historical
  execution, a newly derived determination, or a policy permitting either —
  and, distinctly, whether historical executions should independently be
  retained and reportable;
- whether a later documentary basis report that disagrees with derived history
  is reconciled, deferred to, or refused — and who authors that claim;
- whether a collect-target universe guard defect, if found, is repaired.

## The smallest honest executable surface

`packages/content/tax/` contains only a `2025/` directory. A scan of every
file under it for `tax.us.<year>.`-shaped tokens returned exactly one
namespace, `tax.us.2025.` — so no committed content references any other
year. (This is a direct observation over the content tree, not a claim about
the whole repository or about test fixtures.) This milestone must not silently
become the implementation of a 2026 package.

Three candidate surfaces, to be **selected by evidence in Track 0 §2–§3, not
by convenience**:

| Surface | What it is | What it can honestly claim | Cost and risk |
| --- | --- | --- | --- |
| **S-a1. Disposable in-memory consumer** | A later-year consumer expressed as test-local rules and findings, supplied directly to the existing `_run()` helper and thrown away | **Only** that the rule vocabulary can express the calculation given the findings. `_run()` is a deliberately assembled fixture entrypoint whose `findings` argument is hand-built, so nothing it shows can establish that a later run *finds* an earlier result | Lowest. Cannot demonstrate reuse at all — only expressiveness |
| **S-a2. Disposable persisted-boundary experiment** | The earlier case executed for real, its publications appended to a temporary act log, currentness computed, and the earlier result offered to the later consumer through the real projection/marshalling boundary | Whether genuine workspace reuse occurs, as distinct from value-passing | Low, and **necessary**: it is the only surface that can tell reuse from injection |
| **S-b. Source-independent adjusted-basis or disposition calculation** | Committed content that computes adjusted basis or a disposition result without claiming to implement a 2026 return | That the product can compose a basis, if and only if such content can be scoped honestly | Medium. Depends on an unresolved scope question — see below |
| **S-c. Production tax-year content** | A 2026 package | That a later-year return path exists | Highest, and out of scope for this milestone |

**S-a1 and S-a2 together are the presumptive surface, and S-a2 is
mandatory.** Both are authorized from the start. S-a1 alone is explicitly
insufficient: a milestone that only passed a value between two rules in one
assembled context would be the triviality this plan's Objective already
disclaims.

**S-b is not inherently owner-held, but Track 0 does not build it.** Track 0
may evaluate whether S-b is viable and prepare its work packet — that is
ordinary work needing no permission. It may **not** author committed S-b
content, because Track 0's own boundary excludes changes under `packages/`. A
**conditional production unit** may be chartered afterwards, once Track 0
leaves no unresolved semantic or contract decision. The stop condition is not
"S-b was reached", nor "`packages/` was entered", but **a consequential scope
or accepted-contract decision** — a new scope convention for basis, say, or a
change to ADR-0068/0070/0071/0072/0010. S-c remains a non-goal.

**The scope question that decides S-b.** Two plan-time code readings bear on
it, and both are flagged for execution rather than treated as settled:

- `packages/derivation/package_validation.py` compares **each member that
  carries a `scope` key** against the package's `("tax_year", "jurisdiction",
  "family")` and reports `SCOPE_MISMATCH` on a difference. Members that
  declare no `scope` are not reached by this check at all, so the constraint
  is narrower than "a package cannot mix years"; what it establishes is a
  constraint on scoped members only.
- The in-package closure check on `requires` appears to bind only symbols
  ending `.member-validation`; a general cross-year symbol reference is not
  obviously blocked by package validation, leaving whether the *runner*
  resolves it a separate, runtime question.

If S-b turns out to require a new scope convention for basis, or a 2026
package to exist, that is a consequential milestone-scope choice: stop and
report it. Track 0 does not resolve it by inventing content, and does not
author committed content to find out.

## Two experimental dimensions, held separate

The milestone varies two things, and conflating them would make both
unmeasurable:

1. **Access strategy** — *how* a later calculation obtains the earlier basis
   consequence.
2. **Representation strategy** — aggregate **A** versus durable components
   **B**.

These are independent. A finding about one is not evidence about the other,
and the single most likely way this milestone could produce a false result is
to let an access failure masquerade as a representation finding.

**Hold the comparison conditions constant when comparing representations.**
A and B are exercised under the same access strategy; the same projected source facts and
currentness state; the same scenario; the same consumer purpose and output
contract; and only the representation-specific composition inherently required
by A or B. A literal shared adapter is *not*
required, and must never be imposed where it would erase the very difference
under test. "Both were unavailable through the real boundary" is an **access
finding**, not evidence that A and B are behaviorally equivalent. A null C12
result is only meaningful when both representations were reachable on equal
terms.

**If AS-1 and AS-2 are both viable and produce materially different access
semantics** — above all the historical-versus-newly-derived distinction — then
**neither may be chosen for C12 by convenience.** Exercise A and B under *each*
materially distinct viable access strategy, or **explicitly defer C12** until
the access meaning has been selected. Only where the two access strategies are
**observationally equivalent for C12** may one stand for both, and that
equivalence must be recorded before it is relied on.

### How a negative C7 routes

If C7 shows the committed boundary does **not** expose the earlier derived
publication, the plan does **not** route to "adopt a production persistence
caller." That would convert a measurement into a product decision without
comparing the alternatives. Instead C7 becomes a branch point:

1. **Test the bounded access alternatives** (AS-1 and AS-2 below).
2. **Run the A/B comparison** under the held-constant conditions above,
   across each materially distinct viable access strategy.
3. **Then** either identify a supported production direction, or close
   explicitly with the smallest genuine contract or product decision named.

### The two access strategies to compare

Both remain **disposable and test-local**. Neither production mechanism is
implemented in this milestone.

| | **AS-1 — retrieve a persisted earlier derived finding** | **AS-2 — re-execute the applicable determination** |
| --- | --- | --- |
| What it does | Expose or retrieve the earlier derived publication that was recorded | Obtain the current canonical findings from the **real kernel projection/marshalling boundary over the same authoritative acts**, then re-derive the determination from them under an explicit earlier rule/package/reporting-year context |
| Same-investment identity | Which facts and identity establish that the retrieved finding concerns this investment | Which facts and identity establish that the re-derived determination concerns this investment |
| Currentness, correction, supersession | How a corrected input reaches the retrieved finding, and whether a displaced finding is detectably stale | How correction and supersession behave when the determination is recomputed |
| Governing version | Which rule/package version governed the original execution, and whether that is recoverable | Which rule/package version governs the re-execution, and whether it may differ from the original |
| Provenance carried | What the later result can say about where its basis figure came from | The same question for a freshly derived figure |
| Historical vs current | Whether the result represents **the historical execution** | Whether it represents **a newly derived current determination** |
| If it cannot be instantiated honestly | Name the exact contract or production gap | Name the exact contract or production gap |

The historical-versus-current row is a substantive distinction between the
two *experiments*, not an implementation detail: retrieval, if it worked,
would report what was determined then; re-execution reports what would be
determined now. Those can differ. They are not rival product architectures
the owner must pick between. What a later calculation may **consume**
(historical execution, newly derived determination, or a policy permitting
either) is distinct from whether historical executions should independently
be **retained and reportable**. The milestone must keep those questions
separate and must not select either policy.

### What each experiment actually does, and its evidence rung

**AS-1 — retrieval. Rung 4, reusing C7's temporary act log.** No second
persistence experiment is manufactured: AS-1 continues from the same
authoritative act log C7 already built. It identifies the derived publication
in that log, establishes its currentness through the derivation
projection/currency machinery (`derived_findings_from_acts` and
`compute_derivation_currency`, as `workspace_currency` composes them),
establishes same-investment identity, and offers the finding to the controlled
consumer. AS-1 **does not pretend the live marshaller already does this** — if
C7 showed the boundary omits derived findings, AS-1's controlled hand-off is
explicitly a test-local adapter standing in for a capability that does not
exist, and must be labelled as such.

**AS-2 — re-execution. Also rung 4, and also a continuation of C7's one
authorized experiment on the same temporary act log.** AS-2 is *not* a
rung-3 experiment over hand-assembled findings. That weaker form would prove
only that the rules recompute when handed values — not that a later workflow
can obtain the canonical facts from authoritative workspace state, which is
the proposition that matters. Its steps:

1. **Obtain the current acquisition and report findings from the real kernel
   projection/marshalling boundary** over the authoritative acts in C7's log.
   These are projected, not assembled.
2. **Re-execute association, supportability, and consequence production** from
   those projected findings, under an **explicit earlier (2025)
   rule/package/reporting-year context**.
3. **Retrieve or inject nothing** that AS-2 is meant to produce. The earlier
   association, the supportability verdict, and the basis consequence are all
   **re-derived**. ADR-0068 Decision 7 states the association "is derived, not
   a stored, independently corrected object," recreated whenever the same
   pairing is evaluated — so retrieving it would be a category error, and
   injecting the earlier consequence would make the experiment circular.
4. **Offer the newly produced consequence to the later disposable consumer
   through an explicitly test-local hand-off**, labelled as standing in for a
   capability that does not exist.
5. **Record** identity, correction/currentness, governing version, provenance,
   historical-versus-newly-derived character, and the exact failure point.

The canonical inputs are therefore the **projected acquisition finding —
including its confirmation fields, notably `confirmed_report_match` and
`confirmed_report_fact_id` — the projected report finding, and any other
current findings the re-execution actually consumes.** They are not "four
canonical source facts," and the association is not among them.

**Reporting-year handling is explicit, because the committed association
filters candidate reports against the run's own `reporting_year`.** AS-2
therefore re-executes the earlier determination under the **2025**
reporting-year and 2025 rule/package context, and its newly produced
consequence is consumed in the **separate later disposition context**. A
**negative control** accompanies it: association attempted directly under the
*later* reporting year must be shown **not** to silently associate the 2025
report. Without that control, a passing AS-2 could not be distinguished from
an accidental cross-year association.

**Rung authorization is stated once, here, so Checkpoint B cannot require what
the ceiling forbids.** AS-1 and AS-2 are **both** bounded continuations of the
**one** authorized persisted-boundary experiment, on the **one** temporary act
log C7 builds. Together they remain a single rung-4 experiment. They introduce
**no** second log, restart, cross-process mechanism, production caller, or
storage design. **No further rung-4 work is authorized**, and any requirement
for one is a **stop and report**, not a silent extension.

**The act log and the record stream are different things, and the distinction
is load-bearing here.** Under ADR-0010 a `derived-publication` act is part of
**authoritative workspace state**: the derived finding it carries is projected
from that act and is legitimate material for a later determination. The
derivation **run/completion record stream** is a different artifact — it
*describes execution* (what ran, what was published, what blocked) and is
**not** a derivation input.

So AS-1 **may** examine the authoritative derived finding projected from its
act, and doing so is not a category error. What AS-1 **must not** do is reach
the earlier value by reading a run or completion record; that would let an
execution account become tax input. If AS-1 finds itself needing the record
stream to locate or interpret the value, that is a finding to report, not a
step to take.

## Claim and verification architecture

Every load-bearing conclusion is inventoried before synthesis. Claim types:
**T** tax meaning, **B** current committed behavior, **D** selected product
direction, **H** hypothetical design.

| # | Proposition | Type | Source / artifact | Exact fields or clauses | Neighbors *not* relied on | Downstream consumers | Sections affected if it changes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Accrued interest received on a bond bought between interest dates is a return of capital reducing the buyer's remaining basis | T | Treas. Reg. § 1.61-7(c); corroborated by IRC § 61(a)(4), Pub. 550 "Bonds Sold Between Interest Dates" | § 1.61-7(c) operative text on interest "in arrears but... accrued at the time of purchase" | § 1.61-7(d), which governs the *seller's* reporting obligation | Track 0 §1, §3 | §1, §3, §5 |
| C2 | Gain or loss on disposition is the amount realized less adjusted basis, where adjusted basis is the § 1012 cost origin adjusted under § 1016, and the earlier reduction changes the result by exactly the accrued amount | T | IRC § 1001(a) (gain/loss = amount realized − adjusted basis); § 1011(a) (adjusted basis = basis determined under § 1012, adjusted under § 1016); § 1012 (cost); § 1016 (adjustments to basis); and for the reduction itself, Treas. Reg. § 1.61-7(c) per C1 | The four provisions' operative sentences only | Character (capital vs ordinary), holding period, wash sales, Form 8949 and Schedule D reporting mechanics — all outside the bounded calculation | Track 0 §1, §3 | §1, §3 |
| C3 | The committed rule republishes **the accrued amount supplied by the ordinary answers**, keyed by the derived pairing finding id — not a fixed figure | B | `tests/test_integration_checkpoint.py::test_t2_accrued_treatment_publishes_both_consequences`; `_answers()`; `packages/tax/pairing_consequences.py`; `runner.absorb_association_result` | The rule's `value` is `ref` to `accrued_interest_paid_to_seller`; the test asserts the string `"42.0"`, sourced from `_answers()`'s `42.0` | The committed test's prefix matching, silent about symbol suffixes | Track 0 §2, §4 | §2, §4, §6 |
| C4 | A run carries exactly one `reporting_year`, sourced from run scope, gating which reports may associate | B | `marshal.py`; `identity_association._reports_in_reporting_year`; `live.py` reading `run_scope["year"]` | The reporting-year filter and its `None` semantics (`None` = no report in scope) | Horizon and closure machinery | Track 0 §2, §4 | §2, §4, §6 |
| C5 | A package member **that carries a `scope` key** receives `SCOPE_MISMATCH` when its `tax_year`, `jurisdiction`, or `family` differs from the package's scope | B | `package_validation.py` member loop: `if "scope" in citizen` then compare `("tax_year","jurisdiction","family")` | Exactly those three keys, and only for members declaring `scope` | Members without a `scope` key, which this check does not reach; role, schema, and citation checks | Track 0 §2, §8; surface selection | §2, §8, surface selection |
| C6 | Package validation **accepts** a rule whose `requires`/`ref` names a symbol no package member produces (the closure check binds only `.member-validation` symbols) — which is *not* evidence that the runtime resolves that symbol | B | `package_validation.py` `requires` handling and `_iter_parameter_and_table_refs`; a `rule-artifact.v7` citizen with `value` of the form `{"op":"ref","name":"<symbol>"}` and a matching `requires` entry | Which required symbols the closure check actually binds | Parameter and table refs, which *are* closed and would error | Track 0 §2, §4 | §2, §4, surface selection |
| C7 | **The real workspace→run boundary exposes a current earlier derived consequence to a later run without manual injection.** | B | To be produced (S-a2): the persisted-boundary experiment | Whether `project()`-derived run state carries derived findings at all, and under what symbol they would resolve | **Production invocation** (whether anything under `packages/` calls this path), **restart guarantees**, and **cross-process durability** — the experiment measures the boundary's behavior within one process against a temporary log and claims nothing about those three | Track 0 §3, §4, §5 | §3–§7 |
| C8a | **The committed correlation structure that exists**: the association records `left_fact_id`/`right_fact_id` in its value and pins both source finding ids, while the consequence's symbol is suffixed by the derived pairing finding id | B | ADR-0068 Decisions 7–8; `identity_association.py`; `pairing_dispatch.py`; `runner.absorb_association_result` | The association's value fields and `pins_for` shape; the consequence's symbol suffix | Whether any *declared expression* can read them — that is C8b | Track 0 §4 | §4, §6, §8 |
| C8b | **A declared expression can traverse that structure** from acquisition identity to the exact consequence | H | To be produced: an authoring attempt plus a bounded corpus search | The expression vocabulary's reach into a derived finding's value payload | Traversals available only to Python, which are not declared-expression evidence | Track 0 §4 | §4, §6, §8 |
| C9 | Durable cross-run retrieval has **no production caller**, though the primitives exist and are exercised in committed tests | B | `runner.append_publications`; callers in `tests/derivation/test_cascade.py` and `tests/derivation/test_act_log_admission.py` | Call sites across `packages/` versus `tests/` | In-run composition, which needs no persistence | Track 0 §5, §6 | §5, §6 |
| C10 | Correcting the earlier acquisition displaces both published consequences | B | `tests/test_pairing_consequences.py::test_shared_pins_displace_both_consequences_via_real_machinery` | One-hop and two-hop displacement | Auto-re-derivation, which ADR-0010 Decision 6 puts out of scope | Track 0 §6 | §6 |
| C11 | No mechanism compares a broker-reported basis against a named product-derived adjustment | B | `rule.schedule-d-line1a-gain.json`; `taxpayer_side_adjustment`'s runtime treatment | That admission selects by `declaration["member_predicate"]["fact_type"]` alone | ADR-0052/0057 decision *text*, which states an intent the code does not implement | Track 0 §6 | §6 |
| C12 | **Holding the access strategy, projected source facts and currentness state, scenario, and consumer purpose/output contract constant, A and B produce a material observable difference in at least one of S1–S7.** Neutral as to direction: a difference may favour A, favour B, or expose a tradeoff | H | To be produced: the same scenarios run against each representation under those held-constant conditions, across **each materially distinct viable access strategy** | Numeric result, disposition, provenance, component addressability, and correction/displacement behavior; only the composition each shape inherently needs | Architectural taste; internal structure invisible to the consumer; **any access difference**, which belongs to C7/AS-1/AS-2 | Track 0 §5, §8, disposition | §5, §8, disposition |
| C13a | Event year, reporting year, tax-consequence year, and disposition year are four conceptually distinct years | D (domain/product distinction; no separately sourced tax proposition is asserted here — the controlling tax authorities are C1 and C2) | `docs/domain-models/taxable-interest-translation.md` "Cross-year handling"; this plan's own addition of the disposition year | The conceptual distinction only | Any claim that a committed field or scope names a tax-consequence year — **no such field or scope is asserted to exist** | Track 0 §1 | §1, §3 |
| C13b | Committed behavior keeps the acquisition's `acquisition-year`, the report's own `tax-year`, and the run-scope reporting year as three separate components, and a confirmation never retargets across reports or reporting years | B | ADR-0068 Decision 5; `confirmed_report_fact_id` handling; `_reports_in_reporting_year` | Those three components and the confirmation's recorded target | Any tax-consequence-year component, which is **not** claimed to exist in committed content | Track 0 §2, §4 | §2, §4, §6 |
| C14 (conditional on C7 negative) | **AS-1 retrieval works**: the earlier derived publication can be identified in C7's authoritative act log, shown current through the derivation projection/currency machinery, tied to the same investment, and delivered to the controlled consumer | H | To be produced (rung 4, continuing C7's temporary act log) | The derived finding projected from its `derived-publication` act; `derived_findings_from_acts`; `compute_derivation_currency`; the identity fields relied on | The run/completion **record stream**, which describes execution and is not a derivation input | Track 0 §4, §5, §6 | §4–§8, disposition |
| C15 (conditional on C7 negative) | **AS-2 re-execution works**: the current acquisition and report findings can be obtained from the real kernel projection/marshalling boundary over the authoritative acts, and association, supportability, and consequence production re-executed from them under an explicit 2025 rule/package/reporting-year context, yielding a determination the later consumer can use | H | To be produced (rung 4, continuing the **same** temporary act log as C7 and AS-1) | The **projected** acquisition finding including its confirmation fields (`confirmed_report_match`, `confirmed_report_fact_id`); the projected report finding; any other current findings the re-execution consumes; the explicit rule/package/reporting-year context; the re-derived association, verdict, and consequence | The association, verdict, and consequence **as stored inputs** — all three are re-derived, never retrieved or injected (ADR-0068 Decision 7); hand-assembled findings, which would prove only recomputation | Track 0 §4, §5, §6 | §4–§8, disposition |

### Verification method and rival predictions

Each claim gets the method its *type* warrants. Executable behavior is
executed or mutated; an absence claim gets a bounded call-site or corpus
search **plus** a negative probe, because a search alone cannot distinguish
"absent" from "searched for badly". Tax-meaning claims are read against
primary text and are not executable at all.

There is **no blanket guarantee that every prior claim is reproduced by
execution.** Several are not executable, and saying otherwise would repeat the
overstatement this plan exists to avoid.

| # | Verification method | Rival predictions, or falsifier |
| --- | --- | --- |
| C1 | Primary-source reading of § 1.61-7(c). Not executable | A reading that excludes the ordinary between-interest-dates buyer |
| C2 | Primary-source reading of IRC §§ 1001(a), 1011(a), 1012, **1016**, and **Treas. Reg. § 1.61-7(c)** — § 1016 supplies the adjustment authority § 1011(a) refers to, and § 1.61-7(c) supplies the particular reduction. Not executable | An authority making the reduction inapplicable at disposition |
| C3 | **Execution**: run the T2 test and inspect published symbol, suffix, and value, confirming the committed fixture demonstrates *parameterized* publication at `42.0`; then execute **this milestone's `$150` scenario** by overriding `_answers()`, so the plan's worked figures are run rather than asserted | The rule publishing something other than the supplied amount, or a different key |
| C4 | **Execution + mutation**: run with `reporting_year` set to the later year and to `None`, observing which reports associate | A report associating outside the run's reporting year |
| C5 | **Mutation**: validate a deliberately mixed-year package and observe `SCOPE_MISMATCH`; and validate a member with **no** `scope` key to confirm the check does not reach it | Either mutation behaving otherwise |
| C6 | **Two-part, and the parts must not be conflated.** (a) *Validator*: submit a `rule-artifact.v7` whose `value` is `{"op":"ref","name":"<unproduced symbol>"}` with a matching `requires`, and observe acceptance. (b) *Runtime*: execute a run containing that rule and record whether the symbol resolves or the rule blocks | Validator rejection falsifies (a). Runtime resolution *or* a specific blocked disposition is the recorded result of (b) — acceptance in (a) predicts nothing about (b) |
| C7 | **Execution, rung 4** — the persisted-boundary experiment below | **Rival A (predicted by plan-time reading):** the boundary *omits* derived findings. `packages/kernel/findings.py` states the kernel projects only its own act kinds and passes over `derived-publication` (ADR-0010 compose-over), and `live.py` builds run state from `project()`, never `derived_findings_from_acts()`. **Rival B:** some path exposes them. A later run resolving the earlier consequence with no manual injection falsifies Rival A |
| C8a | **Execution + direct artifact reading**: run the T2 fixture and inspect the association's value and pins and the consequence's symbol suffix | The recorded fields differing from ADR-0068 Decisions 7–8 |
| C8b | **Construction attempt + bounded corpus search**: attempt to author a declared rule that joins acquisition identity to the consequence; search committed content for any existing declared traversal of an association value | Exhibiting a working declared join falsifies the no-traversal prediction. Failure to author one is *not* proof none exists — it is recorded as "not established as possible," never as "proved impossible" |
| C9 | **Bounded call-site search** across `packages/` and `tests/` **plus a negative probe**: confirm the searched name is the one actually invoked by the committed tests, so the search is shown capable of finding a caller | Any caller under `packages/` |
| C10 | **Execution**: run the named displacement test | Displacement failing to reach a consequence |
| C11 | **Bounded corpus search plus negative probe**: search content and code for any comparison of a broker figure against a named adjustment; probe by confirming the search finds the *uses* of `taxpayer_side_adjustment` that do exist | A committed comparison mechanism |
| C12 | **Execution against both representations** over S1–S7, holding constant the access strategy, the projected source facts and currentness state, the scenario, and the consumer purpose and output contract. Each shape performs **only the representation-specific composition it inherently needs** — a literal common adapter is *not* required, and must not be imposed where it would erase the very difference under test. Where AS-1 and AS-2 are both viable with materially different access semantics, run this **under each**, or defer C12 explicitly; a single strategy may stand for both only after observational equivalence for C12 is recorded. Compare numeric result, disposition, provenance, component addressability, and correction/displacement behavior | **Explicit null result is a legitimate outcome:** no material observable difference in any scenario, *provided both were reachable on equal terms*. "Both were unavailable through the real boundary" is an access finding and does **not** license a null C12. Any material difference falsifies the null, in whichever direction it points |
| C13a | Reading of the domain model. Not executable | — |
| C13b | **Execution**: exercise confirmation retargeting across reporting years | A confirmation authorizing a different report or reporting year |
| C14 | **Execution, rung 4, reusing C7's temporary act log** — no second persistence experiment. Observe, and record separately: (i) same-investment identity — which facts and fields establish it; (ii) currentness under correction and supersession; (iii) which rule/package version governed the original execution and whether it is recoverable; (iv) provenance the retrieved finding carries; (v) that the result is **the historical execution**; (vi) the exact contract or production gap if it cannot be completed honestly | **Rival:** retrieval succeeds and the consumer can use the historical determination. **Falsifier:** the finding cannot be identified, cannot be shown current, cannot be tied to the investment, or can only be delivered by reading a run record. The hand-off adapter must be labelled test-local — AS-1 must not imply the live marshaller already performs it |
| C15 | **Execution, rung 4, on the same act log as C7 and AS-1.** Project the acquisition and report findings through the real boundary; re-execute association, supportability, and consequence production under the explicit 2025 context; hand the new consequence to the later consumer test-locally. **Plus a negative control:** association attempted directly under the *later* reporting year must not silently associate the 2025 report. Observe the same six: identity; correction/currentness; governing rule/package version; provenance; that the result is **a newly derived current determination**; and the exact failure point | **Rival:** the boundary yields the canonical findings and re-execution reproduces a usable determination. **Falsifier:** the acquisition or report findings cannot be obtained from the real projection boundary; or re-execution fails under the explicit context; or it succeeds only when the association, verdict, or consequence is injected rather than re-derived. **A failing negative control** — the 2025 report silently associating under the later reporting year — invalidates the whole AS-2 result, since it would mean the pass came from cross-year leakage |

C7, C8b, and C12 are the milestone's genuinely open questions, joined by C14
and C15 **conditionally** — they open only if C7 is negative, and are
otherwise not reached. C3, C4, C5, C6, C8a, C10, C13b are executable and are
executed in Track 0 §2. C9 and C11 are absence claims verified by bounded
search plus negative probe. C1, C2, C13a are read, not run.

### Fixed scenario matrix

Every representation still viable is exercised against the same scenarios, on
the same fixture, with the same access assumptions.

| # | Scenario | What it tests | Expected observable |
| --- | --- | --- | --- |
| S1 | Positive: earlier consequence available, later disposition | Baseline reuse; the $310 result | A gain reflecting the adjusted basis, with provenance naming the earlier determination |
| S2 | Missing input: earlier consequence not available to the later run | Whether absence is detected or silently wrong | An explicit blocked/unsupported result, never a $160 gain presented as correct |
| S3 | Conflicting report: a later broker-reported basis disagrees with derived history | Reconciliation versus substitution | Track 0 must choose explicitly: reconcile, defer, or refuse — and name who authors the claim |
| S4 | Correction: the earlier acquisition's accrued amount is corrected after the later result exists | Displacement reaching a later consumer | The later result becomes non-current, or the inability to make it so is recorded |
| S5 | Stale history: the earlier determination was superseded by a later rule version | Currentness versus mere availability | The consumer uses the current determination, or the gap is named |
| S6 | Agreement: a broker report agrees with derived history | That agreement is not accidentally treated as conflict | No spurious refusal |
| S7 | **No broker-reported basis is available** — the condition itself, held as a bare fact about the scenario. Track 0 may name a legal occasion for it (a non-covered security, or one predating an issuer's reporting obligation) only if it sources that occasion independently; the scenario does not depend on doing so | Whether the product can state an adjusted basis on its own canonical history, with no documentary figure to lean on | Track 0 must determine what the consumer produces. **Documentary absence must not be treated as evidence that no canonical adjusted basis exists** — the derived history may be complete precisely when the broker is silent |

S7 is deliberately distinct from S2, S3, and S6, and the four must not be
collapsed: S2 is a missing *product-derived* consequence, S3 is a broker
figure that *disagrees*, S6 is one that *agrees*, and S7 is the absence of any
broker figure at all. S7 is the case where the product's own derivation is the
only account available, so it is the strongest test of whether canonical
history is load-bearing or merely decorative.

S2, S5, and S7 are the scenarios most likely to expose a representation
difference, because they are where "which components are addressable" and
"which are current" stop being equivalent.

**Every scenario holds the comparison conditions constant.** Each of S1–S7 is
exercised against A and against B under the same access strategy; the same projected source facts and
currentness state; the same scenario; the same consumer purpose and output
contract; and only the representation-specific composition inherently required
by A or B, so that any difference
observed is attributable to the representation rather than to how the earlier
determination was obtained. If a
scenario cannot be reached under either representation, that is recorded as an
access finding against C7/AS-1/AS-2 and the scenario yields no C12 evidence at
all.

### Verification methods, by evidence rung

Gate 3 rungs: (1) static content examples; (2) resolver/validator mutations;
(3) throwaway evaluator run; (4) persisted end-to-end integration.

- **Rung 3 is the ceiling for rule-expressiveness questions** — whether the
  vocabulary can state the calculation (S-a1).
- **One narrow, disposable rung-4 experiment is authorized**, and only the one
  specified below. It is the *only* authorized rung-4 work.

**The primitives this experiment needs already exist and are exercised by
committed tests.** `runner.append_publications` is called by
`tests/derivation/test_cascade.py` and
`tests/derivation/test_act_log_admission.py`;
`projection.workspace_currency` is called by those and by
`tests/tax/test_track4_correction_cascade.py`. What is absent is a caller
under `packages/` — an absent *production* caller, not an absent capability,
which is exactly what C9 records.

#### The authorized persisted-boundary experiment

Purpose: **distinguish genuine workspace reuse from an in-memory value-passing
demonstration.** Nothing else. Steps:

1. Execute the earlier accrued-interest case through the existing fixture.
2. Append its publications to a **temporary** act log with
   `append_publications`, following the pattern already committed in
   `tests/derivation/test_cascade.py`.
3. Verify the publications' currentness through `workspace_currency`.
4. Attempt to expose the earlier result to the later consumer **through the
   real projection/marshalling boundary** — the path `live.py` actually uses.
5. **Record whether that boundary supplies or omits derived findings.** This
   is the experiment's primary output, and a null or negative result is a
   complete answer, not a failure.
6. Exercise correction/displacement through the same temporary record (S4).
7. Run a **negative control**: the same consumer given a manually injected
   `RunContext`. If the injected control succeeds where the real boundary does
   not, the difference is exactly the measurement — it separates reuse from
   injection.

**What this experiment does not authorize:** a production persistence caller,
new storage, any change under `packages/`, or 2026 content. It is disposable
test-local evidence under Gate 7, thrown away unless a later charter adopts it
deliberately.

**AS-1 and AS-2 are both bounded continuations of this same experiment**, on
the same temporary act log, and need no separate authorization. Together with
C7 they are one rung-4 experiment over one log. Nothing else at rung 4 is
authorized: any requirement for a second log, a restart, a cross-process step,
a production caller, or a storage design is a stop-and-report, not a silent
extension. Checkpoint B therefore never demands work the ceiling forbids.

## Track 0 sections and their abstracts

Track 0 is developed one section at a time. After each, its claims are
reconciled against every earlier section and the claim map above;
contradictions are corrected immediately. A section is not complete because
its local prose is plausible.

### Checkpoint handoffs (required, and enforced)

"Section-level checks" as an aspiration is exactly what fails silently, so the
Track 0 unit **must** structure itself around three checkpoint handoffs.
These are handoffs *within one unit* — they require **no new process document
and no commit-per-checkpoint**. The Builder reports at each, and the foreman
reconciles before the Builder continues.

| Checkpoint | Contents | Hard boundary |
| --- | --- | --- |
| **A** | Semantic outline, the fixed scenarios S1–S7, the falsifiable propositions with rival predictions, and the evidence map | **No representation conclusion may appear.** A checkpoint A that names a preferred representation is rejected and returned |
| **B** | Reproduced current behavior, including the persisted-boundary experiment **and** its manual-injection negative control; and, if C7 is negative, the AS-1 and AS-2 continuations on that same log, with AS-2's later-reporting-year negative control | No synthesis beyond what was executed or searched. **No representation conclusion**, because consumption policy and historical retention are not yet settled |
| **C** | The A/B comparison under the held-constant conditions, lifecycle and provenance synthesis, and the disposition | Must trace every conclusion to checkpoint A's propositions and checkpoint B's evidence. Must state which access strategy or strategies the comparison ran under, and — where more than one was viable — either report both or record the explicit C12 deferral |

**The Builder reconciles each checkpoint against the claim/dependency map
before continuing.** This is the mechanism that moves contradictions earlier;
it is a Track 0 obligation, not a suggestion.

**R2 opens after checkpoint B and before checkpoint C** — after the evidence
exists and before any representation conclusion is drawn. That ordering is the
point: a falsification review of an already-written conclusion measures
nothing.

Evidence labels are mandatory and distinct throughout: **paper**,
**executed**, **committed**, **proposed**. An imagined composition is never
called "supported."

| § | Section | Question it answers | Why that matters to the product |
| --- | --- | --- | --- |
| 1 | Bounded tax and product semantics | What is the taxable event, what must be computed, and under which authority? | Without a bounded tax proposition the later consumer is arbitrary, and the milestone degenerates into passing a number between rules |
| 2 | Current committed behavior, reproduced where executable | What does the engine actually do today about years, scopes, keys, and reuse — and does the real workspace→run boundary supply or omit derived findings? | Every architectural conclusion downstream rests on this. The prior milestone's central cost came from code reading instead; and without the persisted-boundary experiment's control the milestone cannot tell workspace reuse from value injection |
| 3 | Consumer contract and observable success/failure | What exactly does the later calculation need, and what does success or failure look like from outside? | This is the concrete consumer the prior milestone lacked; without a fixed contract nothing can discriminate representations |
| 4 | Identity and access path | How does the later consumer know the determination concerns *this* investment, and how does it reach it — by retrieval (AS-1) or re-execution (AS-2), as experiments, not as rival product architectures? | Same-investment identity is the difference between reuse and coincidence; consumption (historical execution, newly derived, or either) is distinct from whether historical executions are independently retained and reportable |
| 5 | Candidate adjusted-basis representations | Under the held-constant conditions, do A and B produce any material observable difference? | The prior milestone's deferred question; the answer may legitimately be "no", but only if both shapes were reachable on equal terms under each viable access strategy |
| 6 | Correction, supersession, and later-report reconciliation | What happens when an input changes, a determination is superseded, or a report disagrees? | Currentness and reconciliation are where a naive "read the stored number" design fails |
| 7 | Provenance and explanation | What must be preserved so the result can be explained to a reader? | The product thesis is an auditable computation, not just a correct one |
| 8 | Implementation consequences and unresolved owner decisions | What is now buildable, what is blocked, and what requires an owner decision? | Determines whether the milestone continues into a build or closes as a partial result |

## Why the track decomposition follows from the evidence dependencies

The tracks below are derived from the dependency structure of the claim map,
**not** from the eight document sections. Sections §1–§8 are the internal
construction order of one unit of work; they are not tracks, and manufacturing
eight tracks to mirror them would create charter and review overhead with no
evidentiary gain.

The actual dependency structure is:

- C1, C2 (tax meaning) and C3–C6, C9–C11 (reproduced current behavior) are
  **prerequisites of everything else** and are cheap. They belong together in
  one unit, because splitting them would force a second cold agent to re-derive
  the same fixture context.
- C7, C8a, and C8b (reachability and identity) **cannot be settled without**
  the reproduced behavior above; C14 and C15 open only if C7 is negative and
  continue the *same* experiment on the *same* log; and C12 (representation
  discrimination) cannot be settled without C7, C8b, and whichever of C14/C15
  prove viable. All of them are settled by the same executed fixture and log.
  Splitting them would mean rebuilding that fixture per track.
- Contract, production, and integration work all **depend on how C12 and §8
  resolve**, and none of them is known to be needed at planning time.

That yields exactly one unconditional track and three conditional ones.

## Tracks

### Track 0 — semantic, consumer, and discriminating-evidence closure (unconditional)

- **Goal:** produce the eleven Track 0 success conditions below.
- **Boundary:** no production content; no 2026 package; no change under
  `packages/`. Rung 3 for expressiveness, plus the one authorized
  persisted-boundary experiment at rung 4 and nothing further.
- **Inputs:** the two basis domain documents, the prior retrospective, ADRs
  0067–0072, `tests/test_integration_checkpoint.py` and its helpers,
  `tests/test_pairing_consequences.py`.
- **Outputs:** the Track 0 findings document, the executed evidence, and the
  adversarial-closure declaration.
- **Verification:** the commands under Verification below; every executed
  claim reproducible by a named command.
- **Migration risk:** none — no committed artifact shape changes.
- **Capability tier:** High / high (novel synthesis).

### Contract unit (conditional)

Chartered **only if** Track 0 actually selects or changes a durable contract.
If C12 resolves — under the held-constant conditions — that the consumer does not
discriminate A from B, the choice is **deferred again** and no contract unit
is chartered. Deferral is a legitimate result, not a failure to decide.

If instead the AS-1/AS-2 comparison exposes that the consequential decision is
about **consumption policy and historical retention**, or about the
**cross-scope consumption contract**, rather than representation, the
contract unit addresses those questions, and the representation choice stays
deferred. Those dimensions are chartered separately or not at all; they are
never bundled into one unit because they were investigated in one milestone.

### Production unit (conditional)

Chartered **only if** the selected consumer can be implemented without
inventing a 2026 return package and without leaving a semantic decision to the
Builder. If S-b proves blocked, this unit is not chartered and the milestone
closes on S-a evidence with the boundary reported.

### Integration / correction unit (conditional)

Chartered **only where** it verifies a distinct lifecycle claim (S4, S5) rather
than repeating the production test.

## Track 0 success conditions

Track 0 succeeds only if it leaves all of the following:

1. A plain-language account of the earlier acquisition/basis event, the later
   disposition, and the product value of connecting them.
2. One fixed later-consumer task with explicit access assumptions and an
   observable output.
3. A bounded, primary-source-supported tax proposition for that task.
4. Reproduced evidence of what the current engine actually does and cannot do,
   including the persisted-boundary experiment and its manual-injection
   negative control, and an explicit record of whether the real
   projection/marshalling boundary supplies or omits derived findings.
5. The same scenarios exercised against every viable adjusted-basis
   representation under the same access strategy, projected source facts and
   currentness state, scenario, and consumer contract, permitting only the
   composition each shape inherently needs, at the cheapest evidence rung that
   can expose a difference.
6. If C7 is negative, the bounded AS-1 versus AS-2 comparison, answering for
   each strategy: same-investment identity; currentness, correction, and
   supersession; the governing rule/package version; provenance carried;
   whether the result is the historical execution or a newly derived current
   determination; and the exact contract or production gap where the strategy
   cannot be instantiated honestly.
7. Positive, missing-input, conflicting-report, correction, and stale-history
   cases, and the no-broker-report case (S1–S7).
8. A precise account of identity, currentness, provenance, and invalidation.
9. A finding on whether the concrete consumer distinguishes durable components
   from a single aggregate, under the held-constant conditions and across each
   materially distinct viable access strategy. If it does not, defer the
   choice again rather than selecting by taste. An access failure affecting
   both shapes is reported as an access finding and does **not** support a
   no-difference conclusion.
10. An explicit list of which earlier composition gaps must close for a
   production vertical and which remain unrelated.
11. A production work packet containing no unresolved semantic decision — or
    an explicit partial disposition explaining why production should not begin.

Track 0 is **not** successful merely because it produces a long domain account
or a recommendation. Its conclusions must be traceable to executed or directly
examined evidence, and implementation must be charterable without asking a
Builder to finish the product design.

## Review placement

Section-level foreman checks run continuously while the work develops.
Independent review is reserved for two high-leverage points, plus one midpoint
falsification pass.

| Point | When | Purpose | Tier |
| --- | --- | --- | --- |
| **R1 — plan-structure review** | After the semantic outline, scenario matrix, and verification architecture exist, before detailed synthesis | Attack the question set, scenario coverage, evidence methods, and hidden scope couplings. **Not** prose polish | High / high |
| **R2 — midpoint falsification** | **After checkpoint B, before checkpoint C** — evidence exists, no representation conclusion drawn yet | Attempt to falsify the evidence map and the consumer discriminator, including the persisted-boundary experiment's control. **Not** editing finished wording | High / high |
| **R3 — disposition review** | After the integrated Track 0 disposition, before any first production charter | Whether the disposition is traceable to executed evidence and charterable | High / high |

A targeted additional review is appropriate **only for a named unresolved tax,
identity, lifecycle, or runtime claim.** Repeatedly sending the whole packet
through undifferentiated review is prohibited by Gate 4's caps and by this
plan.

## Planning questions the milestone must answer

Restated as completion obligations, each mapped to where it is answered:

| Question | Answered in |
| --- | --- |
| What exact later disposition is being modeled? | §1 |
| What is the smallest honest consumer, given that no 2026 package exists? | §2–§3, surface selection |
| Which earlier facts and determinations must the consumer locate? | §3–§4 |
| What proves they concern the same investment? | §4 (C8a, C8b; and C14/C15 where conditional) |
| Must the consumer read separately attributable components, or does an aggregate behave identically? | §5 (C12) |
| How does a correction to acquisition price, accrued interest, association, or later report affect the result? | §6 (S4, C10) |
| What happens when later broker-reported basis agrees, disagrees, or is unavailable? | §6 (S3, S6, C11) |
| Which results are executable evidence, and which remain conceptual? | Evidence labels throughout; §2 and §5 |
| What must be preserved so the application can explain the result? | §7 |
| Which decisions require a successor contract or owner disposition before production? | §8 |

## Contracts

Expected to exist and be relied upon, not changed by Track 0:

- ADR-0068 acquisition-to-report identity association.
- ADR-0070 supportability.
- ADR-0071 two pairing-scoped consequence rules.
- ADR-0072 legacy/pairing coexistence.
- ADR-0010 derived-finding projection and currency (Decision 5: derived
  findings are displacement targets, never correction roots; Decision 6:
  displacement propagation only, auto-re-derivation out of scope).
- `rule-artifact.v7` and the existing expression evaluator vocabulary.

Any proposal to change one of these is a stop-and-report event, not a Track 0
action.

## Fixtures

- `tests/test_integration_checkpoint.py` — the production-shaped accrued-interest
  fixture and its `_answers()` / `_report()` / `_findings_for()` / `_run()`
  helpers. `_run()` is parameterized by `rules`, `findings`, and
  `reporting_year`, which is what makes a disposable later-year consumer
  expressible without a 2026 package.
- `tests/test_pairing_consequences.py` — displacement evidence (C10).
- `tests/derivation/test_cascade.py` — the committed pattern the
  persisted-boundary experiment follows: a temporary `ActLog`, a real run,
  `append_publications`, then `workspace_currency` over the log's acts,
  including supersession and an unrelated-correction control.
- `tests/derivation/test_act_log_admission.py` — a second committed
  `append_publications` caller, useful for the C9 negative probe.
- `tests/tax/test_track4_correction_cascade.py` — `workspace_currency` applied
  to a tax-domain correction cascade.
- Any new fixture is synthetic, `demo.*`-identified, and disposable by default
  under Gate 7.

## Verification

- `python3 -m pytest tests/test_integration_checkpoint.py tests/test_pairing_consequences.py -q`
- Full suite for any change under `packages/kernel/` or `packages/derivation/`.
- `python3 tools/governance_lint.py`
- `python3 tools/envelope_scan.py --range origin/main..HEAD`
- `git diff --check`
- Every executed claim in Track 0 names the command that reproduces it.
- The PR `verify` workflow is the gate of record once a PR exists.

## Track 0 adversarial closure

PENDING. The six artifacts (authority-lifecycle table, empty/nonempty
authority matrix, late-authority counterexample, claim-reuse proof,
neighboring-capability dependency diff, and integration surface) and the
declaration are produced at Track 0 close, not at plan time.

## Data safety

All examples use obvious `demo.*` or `demo-*` identities and wholly synthetic
amounts and circumstances. No personal document, tax fact, prior return,
private output, refusal reason, credential, or absolute workstation path may
enter the branch, domain model, fixture, test, review, or handoff.

## Stop conditions

Stop and report to the owner when:

- making a claim honest would require production 2026 content — report the
  boundary, do not invent the content;
- adopting a **production** mechanism for either access strategy — a
  persistence caller, new storage, or a production re-execution path — would
  settle a consequential contract question rather than an implementation
  detail. Entering `packages/` is not by itself the trigger; the trigger is
  the consequential decision;
- evidence justifies rung-4 work beyond the one authorized persisted-boundary
  experiment;
- reaching the earlier determination would require changing an accepted
  contract (ADR-0068, 0070, 0071, 0072, or 0010);
- two representations remain viable after the smallest discriminating evidence
  **and** choosing one creates substantial migration or irreversible identity
  cost — defer, per the routing table's fourth row;
- official authority does not support the disposition proposition or exposes a
  materially different fact pattern;
- an honest treatment would require personal or non-synthetic data; or
- the foreman cannot explain in plain language what further work would change.

Do not stop merely because the consumer turns out not to discriminate the
representations. That is a legitimate finding, and deferring again is the
correct response to it.

## Exit criteria

The milestone is complete when:

1. one fixed later-consumer task exists with explicit access assumptions and
   an observable output, supported by a bounded, primary-source-supported tax
   proposition;
2. every claim in the map has been verified **by the method its type
   warrants** — execution or mutation for executable behavior, bounded search
   plus a negative probe for absence claims, primary-source reading for tax
   meaning — with any unverified claim explicitly marked and given a reason;
3. the persisted-boundary experiment has run against its manual-injection
   negative control, and the plan records **whether the real
   projection/marshalling boundary supplies or omits derived findings**. A
   negative result closes this criterion; an unexercised control does not,
   because without it the milestone cannot tell reuse from injection;
4. S1–S7 have been exercised against every viable representation **through
   the same access strategy, projected source facts and currentness state,
   scenario, and consumer contract**, at the cheapest rung that could expose a
   difference, with S7 (no broker report) resolved without
   assuming documentary absence implies no canonical adjusted basis;
5. if C7 was negative, AS-1 and AS-2 have been compared on the six required
   characteristics, and the milestone either identifies a supported production
   direction or closes naming the smallest genuine contract or product
   decision;
6. same-investment identity, currentness, provenance, and invalidation are
   accounted for precisely, including where the account is that no mechanism
   exists;
7. the A-versus-B question is either **settled by an observed consumer
   difference** or **explicitly deferred again** with the missing discriminator
   restated — a silent selection by taste is not an acceptable close, and a
   deferral justified by an access failure rather than by measured equivalence
   is recorded as exactly that;
8. the four earlier composition gaps are each classified as must-close for a
   production vertical or unrelated to it;
9. the milestone closes either with a production work packet containing no
   unresolved semantic decision, or as an explicit partial result naming what
   remains open and its reopening trigger; and
10. the retrospective records a cadence lesson **only if a material
   carry-forward lesson exists.** The four-state cadence went unexercised in
   the prior milestone, so this one may be the first to exercise it — but
   process-history narration is not required, and a retrospective that has
   nothing transferable to say about cadence should say nothing about it.
