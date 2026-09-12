<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "nominee-interest-return-integration",
  "milestone_state": "closed",
  "status": "CLOSED 2026-09-12. A current ordinary nominee allocation reaches one bounded taxable-interest result and an honest Schedule B Part I account on package.core-calculations v38. Dispatcher B is the form-facing aggregate; Schedule B v7 and line 2b v8 consume the same adjustment, including the pairing-scoped accrued-interest row that closes T0-F5. Legacy-only workspaces keep the legacy subtotal; both-present refuses. Ambiguous nominee identities return a typed pre-run NOMINEE_IDENTITY refusal with no run id, output, or start record. Ordinary commas remain valid. Not done: Form 8815 / section 135 and wider 2025 taxable-interest coverage, information-return filing, a general fact-id repair, I4 causal-block explanation, and UI.",
  "scope": [
    "connect the current report-scoped nominee reduction to the bounded 2025 taxable-interest calculation, Schedule B Part I presentation, and Form 1040 line 2b projection while preserving its report and allocation provenance",
    "repair T0-F5 so every adjustment subtracted by the bounded line-2b rule is represented in the Schedule B Part I tie-out when that attachment is produced",
    "make a current nominee allocation independently require Schedule B even when the ordinary dollar threshold is not exceeded",
    "select and implement an honest coexistence, transition, or refusal policy for legacy tax-labelled nominee adjustments and the new ordinary-fact-derived nominee reduction, with no silent conversion or double subtraction",
    "close the delimiter-shaped identity boundary for this return path through either a general identity repair or a clean pre-execution refusal before start-record and output-reservation effects",
    "develop the plan section by section with independently reviewed tax, artifact, and executable-design gates before Track 0 settles the production contract"
  ],
  "non_goals": [
    "no claim that the existing taxable-interest model is complete for all 2025 federal interest or that tax.us.2025.interest.taxable-total is a generally sufficient Form 1040 line 2b; the known Form 8815 and wider coverage gaps remain",
    "no normalized nominee information-reporting predicate, Forms 1096 or 1099-INT filing, payment or transfer model, or spouse exception implementation",
    "no user-facing allocation-entry UI and no reliance on the still non-resumable multi-act allocation-recording caller",
    "no automatic migration from a legacy nominee adjustment into a report, recipient, or attributed allocation when the old fact does not establish those propositions",
    "no universal adjustment ledger, grouped-rule framework, person identity system, or fact-id redesign unless a reviewed executable comparison establishes that the bounded result requires it",
    "no provisional-return standing, action-scoped authority, source-family closure for nominee allocations, or durable publication of RunResult findings"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Selected product outcome",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Success and stop conditions",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-tax-consequence-supportability.md#Next-stage input contract",
      "docs/adr/0072-legacy-pairing-scoped-interest-coexistence.md",
      "docs/adr/0073-assertion-standing-and-retraction-lifecycle.md",
      "docs/adr/0074-bound-sources-and-nominee-report-group-ledger.md",
      "packages/content/tax/2025/rule.form1040-line2b.v6.json",
      "packages/content/tax/2025/rule.attachment.schedule-b.v5.json",
      "packages/tax/nominee_consequences.py",
      "packages/derivation/presentation_projection.py",
      "PROJECT_PLANNING.md#Lean Production Loop",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "PROJECT_PLANNING.md#Payload Instantiation Gate",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Plain-language purpose",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Selected product outcome",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Track 0 adversarial closure",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Success and stop conditions",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-return-integration.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md"
}
-->

# Nominee Interest Return Integration

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `nominee-interest-return-integration`
- Primary branch: `milestone/nominee-interest-return-integration`
- State: **CLOSED 2026-09-12**
- Roadmap role: third production stage of nominee-interest support; return and
  presentation integration

## Plain-language purpose

The application can now record that a user says part of one identified
Form 1099-INT amount belongs to another person, and an adopted rule can derive
the corresponding report-scoped nominee reduction. That result still stops
inside the engine. It does not change the taxable-interest total placed on the
simulated return, does not appear as the required adjustment on Schedule B,
and lives beside an older path where the user directly enters a tax-labelled
“Nominee Distribution” amount.

This milestone connects the new ordinary-fact path to the return without
pretending that the older and newer facts mean the same thing. In a bounded
synthetic case, a `$1,200` payer report and a current `$450` allocation should
produce a `$450` nominee adjustment, a `$750` post-adjustment interest amount,
and a Schedule B account that shows how the return got there. The form-facing
row may aggregate what the engine knows report by report, but the explanation
and provenance must still reach the exact report and attributed allocations.

The milestone also repairs a pre-existing presentation defect. The current
line-2b calculation subtracts a pairing-scoped accrued-interest adjustment,
while the current Schedule B attachment has no row for that subtraction. When
Schedule B is required, its tie-out therefore fails. Adding another hidden
nominee subtraction would deepen the same defect. The return calculation and
the attachment must be made to agree before this integration can be called
complete.

## Why this is next

The preceding milestones deliberately separated recording, tax derivation,
and return integration. The first two now execute through the real workspace
and runner. The next useful evidence is whether the derived consequence can
cross the form boundary without losing its meaning, being counted twice, or
requiring the user to supply the tax classification again.

Deferring this step would leave the new capability internal and would postpone
the first real consumer of several open decisions. A contrasting tax concept
would broaden the domain while the completed nominee slice still could not
affect a return. This milestone completes that vertical first, then the phase
can reassess whether to contrast or explain it.

## Selected product outcome

These are product requirements. They do not select a schema, rule count,
package version, migration artifact, or presentation operator.

1. **One tax consequence.** Current attributed nominee allocations for a
   report produce one report-scoped nominee reduction. The bounded taxable-
   interest result subtracts that consequence exactly once.
2. **Form and calculation agree.** If Schedule B is produced, Part I shows or
   accounts for every adjustment that the bounded line-2b calculation
   subtracts. The attachment tie-out and the calculated amount agree.
3. **Nominee status is an independent Schedule B trigger.** A current nominee
   allocation requires Schedule B even when interest and dividends do not
   exceed the ordinary dollar threshold. The allocation is evidence for this
   trigger; absence of an allocation is not a denial.
4. **Legacy facts are not silently reinterpreted.** A legacy user-entered
   Schedule B nominee adjustment does not establish a report, recipient,
   ordinary ownership assertion, or attribution. Legacy-only remains
   compatible; new-only uses the new path; both-present refuses pending
   explicit resolution. It is never silently converted into the new
   proposition, including by amount equality.
5. **No double subtraction.** Both-present refuses rather than adding both
   amounts or guessing that equal amounts describe the same event.
6. **Report-local provenance survives aggregation.** The form may display an
   aggregate “Nominee Distribution” adjustment, as the official Schedule B
   mechanic does. Internally and in reader-facing explanation, the result must
   remain traceable to each contributing report-scoped reduction, current
   allocation, report finding, adopted rule, and citation.
7. **Failure is bounded.** Over-allocation or a missing current report may
   leave unrelated report-local outcomes available. The aggregate nominee
   adjustment, Schedule B, and bounded taxable-interest result that depend
   on the unresolved group block. They do not omit the group, publish the
   unreduced number, or suppress unrelated report groups.
8. **Identity failure is clean at this boundary.** A delimiter-shaped identity
   on any nominee report or allocation the new aggregation and presentation
   path consume is refused before a durable start record or output
   reservation. A general fact-id redesign is outside this milestone unless
   the Q1/Q2 prototype proves that bounded check cannot be honest. The
   current mid-run exception is not the completed return-path behavior.
9. **The result remains bounded.** Success proves nominee and the already
   selected accrued-interest adjustment mechanics inside the currently modeled
   2025 interest universe. It does not establish complete taxable-interest or
   filing support. In particular, the known Form 8815/section 135 and other
   coverage gaps remain outside this milestone.

## Starting committed state (2026-09-10)

This was the merged-tree baseline at planning. It is not the delivered
result. Production now uses package v38, Schedule B v7, line 2b v8, a
declared nominee aggregate, and a pre-run identity refusal.

- `package.core-calculations` v36 admits the report-scoped nominee-reduction
  rule and produces suffixed `tax.us.2025.interest.nominee-reduction|{report_fact_id}`
  findings. It does not feed them to the line-2b rule or Schedule B.
- `rule.form1040-line2b` v6 subtracts the legacy
  `scheduleb-nominee-subtotal`, the ABP adjustment subtotal, and the pairing-
  scoped `current-year-adjustment-subtotal`.
- Schedule B attachment v5 displays legacy nominee and ABP rows, but its Part I
  tie-out omits the pairing-scoped current-year adjustment. This is T0-F5.
- Schedule B applicability is presently threshold-based in the attachment
  requirement. Current nominee allocations are not yet a trigger. P1 verified
  that the 2025 instructions independently require the form for nominee
  *interest*; Q4 is the engine trigger still to implement.
- The legacy nominee fact is keyed by tax year and adjustment instance. The new
  ordinary allocation is keyed by payer, statement, tax year, and recipient.
  Neither identity proves that one legacy amount corresponds to one new
  allocation or report.
- The current nominee coordinator rejects ambiguous rendered identities during
  execution, after a start record and output paths have already been created.
- `tax.us.2025.interest.taxable-total` does not represent Schedule B line 3’s
  section 135/Form 8815 exclusion and is not a generally sufficient line-2b
  model. Fixtures in this milestone must exclude that condition and other
  unsupported interest categories.

## Questions that must close before implementation

### Q1 — What is the form-facing adjustment shape? — **SELECTED (dispatcher B)**

The engine has report-scoped derived reductions; Schedule B and line 2b both
need one form-level nominee amount. Line 2b and `attempt_attachment` execute
**before** `_resolve_attachment`. A presentation-only total cannot change the
return calculation or satisfy attachment tie-out. That comparison is rejected.

Two complete executable candidates remain. Each must supply the **same**
amount and authority to line 2b and to Schedule B:

- **Candidate A — shared derived nominee subtotal.** A derivation-time
  aggregate finding that preserves the report-scoped reduction pins and is
  consumed by both line 2b and Schedule B.
- **Candidate B — shared enumeration of suffixed report-scoped outcomes.**
  A deterministic aggregation of the already-published
  `nominee-reduction|{report_fact_id}` group outcomes, executed in the
  derivation graph (the pairing-scoped current-year-adjustment-subtotal
  dispatcher is the existence proof that this can run before line 2b and
  `attempt_attachment`). Both consumers bind that shared result. If a
  proposed B only folds in `_resolve_attachment`, reject it as a rival
  before building; it is the discarded presentation-only shape.

Reuse of `tax.us.2025.interest.scheduleb-nominee-subtotal` (or
`tax.us.2025.citation.scheduleb-adjustment.nominee`) remains a rejected
coupling. Inventing a `$0` fact for I0 is a rejected coupling. A universal
adjustment ledger is not a candidate merely because nominee and accrued-
interest both need rows.

The executable comparison established arithmetic and blocking for A and
dispatcher B, then established one-report reader-facing provenance and
nominee-versus-accrued-interest kind separation. **Selected: dispatcher B** — shared
enumeration of suffixed `nominee-reduction|{report_fact_id}` outcomes in the
derivation graph, consumed by line 2b and Schedule B before
`_resolve_attachment`. A's copied pins on the shared subtotal are redundant
at that one-report consumer and do not by themselves solve report-group
identity. Presentation-only totals remain rejected. The multi-report grouping
case confirmed B: report-group lineage comes from adjustment-row
reduction ids, not from A's copied aggregate pins. A/B observations were
identical. Rivalry was not restarted. The presentation **carrier** for that
lineage is selected under Q2 (top-level `provenanceGroups`), not by widening
`citationGroups.parts`.

### Q2 — How does Schedule B represent derived adjustments? — **SELECTED (additive successor; top-level provenanceGroups)**

T0-F5 is reproduced on v36: pairing-scoped `$42` with Schedule B required
fails `ITEMIZATION_TIE_OUT_VIOLATION` (`part_sum` `$2,000` vs `taxable-total`
`$1,958`). Published `attachment-rule.v6` adjustment rows are family
`collect_members` only; there is no derived-subtotal slot. P2 found no
honest content-only slot.

Q2 is how dispatcher B places **two** derived adjustments — nominee and
pairing-scoped accrued interest — on Schedule B under distinct labels,
citations, and pins, and ties out to the same amount line 2b used.

**Selected contract (attachment rows):** an additive attachment-rule
successor whose derived rows carry contributing finding ids (report-scoped
nominee-reduction or pairing-scoped current-year adjustment). The
form-facing Nominee Distribution amount remains one aggregate. Do not
require Schedule B itself to display separate recipient or payer rows.
The production contract is `attachment-rule.v11`; Schedule B v7 is its
adopted content instance. The disposable fake-family comparison was not
promoted. No universal adjustment ledger was created.

**Selected contract (presentation carrier):** top-level
`provenanceGroups`, one entry per contributing report-scoped reduction,
keyed to the attachment, adjustment kind/label, and contributing finding
id. Form-facing `citationGroups.parts` remain ADR-0056 itemization only.
The comparison established that lineage is available from recorded pins.
Top-level `provenanceGroups` was selected because extra
`citationGroups.parts` would render as indistinguishable Schedule B
subsections and would change ADR-0056's itemization meaning.
Each provenance group carries a reader `label` distinct from the machine
symbol; the finding id is an identifiable grouping node, not a claimed
resolvable citation site. Nested `provenanceGroups` on a part would require
an explicit presentation-model / ADR-0056 shape successor and is not treated
as compatible with ADR-0056 as written. Production admission and
producer/consumer correspondence are exercised by
`tests/derivation/test_attachment_rule_v11.py` and
`tests/test_nominee_interest_return_integration_track1.py`; the canonical
synthetic presentation instance is
`packages/sample_data/nominee_return_integration_contract/presentation/provenance-groups.presentation-model.v1.json`.

**I4 causal-block explanation is deferred.** Blocked attachments still
return `citation_group=None`. The durable explanation does not identify
which report group caused the dependent aggregate and Schedule B to
block. That is a named limitation, not implied complete report-local
provenance on the blocked path.

### Q3 — What happens to the legacy nominee path? — **SELECTED (bounded default)**

P3 measured current behavior: new-only does not reduce line 2b; both-present
subtracts only the legacy amount. Double subtraction is a risk this
milestone would create.

Bounded default, not a conversion product:

- **Legacy-only** remains compatible on the existing subtotal path and stays
  explicitly legacy.
- **New-only** uses the new path (the selected Q1 candidate).
- **Both-present** refuses pending explicit resolution. Do not infer
  correspondence or convert by amount. Numeric equality is not identity.

Automatic conversion remains rejected. Retiring the legacy path under a
package transition is not this milestone’s default. The prototype uses these
defaults as fixtures, not as a third rival.

### Q4 — What makes Schedule B applicable below the threshold? — **SELECTED (trigger + current completeness)**

P1 verified the 2025 instructions: nominee *interest* independently requires
Schedule B. P3 verified the engine is still threshold-only: I1 publishes
`$450` and Schedule B is `inapplicable`.

Selected engine trigger: a current supported nominee allocation or
consequence independently requires Schedule B. Correction and retraction
remove the trigger when no current allocation remains. Absence is not a
denial and is not stored as a negative assertion.

**Part III is not a three-way product choice.** This milestone retains the
current explicit `foreign-account` and `foreign-trust` evidence requirement
whenever Schedule B is required. The successful I1 fixture supplies `"no"`
answers. The corresponding missing-answer case blocks as
required-and-incomplete. Those are two observations under one policy, not
competing policies. Absence of foreign facts is not a negative answer.

Conditional Part III completeness (aligning with the form’s Part III note so
nominee-only below `$1,500` would skip those answers) is **deferred** unless
the prototype proves that current completeness prevents an honest nominee
integration.

### Q5 — Where should ambiguous identity be refused? — **SELECTED (bounded pre-run check)**

P2/P3 verified the current failure: `NomineeIdentityError` after start-record
and output reservation, nominee-source-scoped, not a product refusal.

Bounded default: a clean **pre-run** identity check covering every nominee
report and allocation identity that the new aggregation and presentation path
actually consume. It must refuse before start-record and output reservation.

A general fact-id redesign stays **outside** this milestone unless the
Q1/Q2 prototype proves that this bounded check cannot be honest (for
example, because the selected candidate consumes identities the check cannot
see, or because a mid-run collision remains after the check). Do not call
the present mid-run exception the completed behavior.

### Q6 — What does the milestone claim about line 2b? — **VERIFIED (bounded)**

P1 established the form sequence: nominee affects line 2; line 3 is Form 8815
/ §135; line 4 reaches Form 1040 line 2b. `taxable-total` is the engine’s
bounded stand-in, not complete line 2b. I1 may show `$750` when no
unsupported interest condition applies. Fixtures exclude Form 8815 and other
unsupported categories. Publication must not describe the result as complete
2025 taxable interest.

### Q7 — What does one report’s over-allocation block? — **SELECTED**

Inherited C4/C10: the *report-scoped* nominee result blocks; unrelated
report-local outcomes remain. That local block is kept.

Once a form-facing aggregate exists, the already-selected failure semantics
are: an over-allocated or missing-report nominee group may leave unrelated
report-local outcomes available, but the **aggregate nominee adjustment,
Schedule B, and bounded taxable-interest result that depend on the
unresolved group must block**. They may not omit the group or publish the
unreduced number. Those dependent failures are not owner-held alternatives.

## Planning review cycle

Planning is developed and reviewed in small connected increments. The purpose
is to expose cross-section contradictions before a full Track 0 record makes
them expensive to unwind.

### P0 — outline and claim inventory — **PASS (findings absorbed)**

This section is the starting model under test. It does not select a schema,
package, migration, identity remedy, or form-facing mechanism. Q1/Q2 remain
open for the executable comparison. Q3, Q4 completeness, Q5, and Q7 are
bounded defaults. Selected product outcomes are requirements to prove, not
an implementation schema.

Independently reviewed 2026-09-10. Verdict **REPAIR**; four blocking and five
non-blocking findings absorbed here. The milestone remained one unit until
P2/P3. No mechanism was selected at P0.

#### Product result in plain language

The user has already recorded that part of an identified Form 1099-INT amount
belongs to another person. An adopted rule can already turn that recording into
a report-scoped nominee reduction. That reduction still dies inside the engine.

After this milestone, in a bounded synthetic case with no unsupported interest
condition, a `$1,200` payer report and a current `$450` allocation should
change the simulated return: Schedule B should show a `$450` nominee
adjustment, the bounded taxable-interest figure should become `$750`, and a
reader should be able to walk from that figure back to the exact report,
allocations, adopted rule, and citation. The form may show one nominee
adjustment, as the official Schedule B mechanic does; the engine may not invent
a report, recipient, or correspondence to get there.

The same return path must also tell the truth about two neighboring facts it
already touches. First, the current line-2b rule already subtracts a
pairing-scoped accrued-interest adjustment that Schedule B does not itemize
(T0-F5). Adding a nominee subtraction without repairing that disagreement
would make the attachment more wrong, not less. Second, the current line-2b
rule already subtracts a legacy user-entered “Nominee Distribution” amount
that does not name a report or recipient. Connecting the new reduction without
a declared disposition for that older fact would make double subtraction a
product behavior rather than a planning risk.

The result remains a bounded 2025 interest calculation. It is not complete
taxable-interest support, not a Form 8815 implementation, and not a filing
product.

#### Economic coherence — remain one unit, with three isolated decisions

P0 recommendation, after independent review: **keep this milestone as one
unit until P2/P3**. Split then, or at Track 0, only if those gates cannot
write the six adversarial artifacts without mixing T0-F5, legacy, and
identity into one mechanism, or if a measured option is a general Schedule B
rewrite, a user-facing legacy conversion product, or a general fact-id
redesign. Do not split now.

The product the owner can use is one vertical: the already-recorded ordinary
allocation affects the bounded return and an honest Schedule B account. The
three extra decisions are in this unit because they are already on that
path, not because they are the same decision.

| Decision | Why it belongs here | What would justify a split |
| --- | --- | --- |
| T0-F5 / derived Schedule B adjustments | Line 2b already subtracts the pairing-scoped current-year adjustment; Schedule B v5 does not itemize it. The same attachment honesty constraint will apply to any new nominee row. Designing that surface twice, or connecting nominee while leaving the attachment unable to tie out, wastes the vertical. Owner disposition already placed this hard gate on the return-integration stage. | Independent review or P2/P3 shows that repairing T0-F5 requires a general Schedule B rewrite or universal adjustment ledger whose consumers and value are not this vertical. Then T0-F5 becomes a prerequisite milestone, and this one waits. |
| Legacy vs new nominee | `rule.form1040-line2b` v6 already subtracts `tax.us.2025.interest.scheduleb-nominee-subtotal`. Connecting the new prefix without a disposition for that live subtractand is how double counting happens. ADR-0072 is a method precedent for a *different* legacy pair (accrued-interest), not a nominee decision. | The selected policy requires a user-facing resolution product, a general migration framework, or invented correspondence. Then stop and return the choice; do not build a conversion product inside this vertical. |
| Identity boundary | The current coordinator raises `NomineeIdentityError` after start-record and output reservation. This return path cannot be called complete while that is the failure mode. The *choice* between a clean pre-execution refusal and a general identity repair belongs here. | If the selected remedy is a general fact-id redesign, implement that as a separate kernel milestone. This vertical may then depend on it, or may ship the narrower pre-execution refusal. Do not absorb a kernel identity program into nominee return integration. |

Keep evaluating the three decisions in one record only if each inventory,
fixed-case, and Track 0 row names which decision it belongs to (`T0-F5`,
`legacy`, `identity`, or `shared vertical`). Independent review made that a
mechanical condition, not a Track 0 hope. If P2/P3 cannot write those
artifacts without mixing the choices into one mechanism, stop and split then.

False couplings this recommendation rejects:

- treating T0-F5 as a nominee defect;
- treating report-scoped engine provenance as a requirement to itemize one
  Schedule B row per allocation or per report;
- treating ADR-0072 as having already chosen the nominee legacy policy;
- treating numeric equality of a legacy amount and a new reduction as
  correspondence, or as conversion authority;
- treating a general identity redesign as required to finish the vertical;
- treating a connected `taxable-total` as complete Form 1040 line 2b;
- treating the below-threshold nominee trigger as already forbidden because
  the previous milestone’s neighboring-capability PASS recorded that it was
  out of *that* milestone’s scope;
- reusing `tax.us.2025.interest.scheduleb-nominee-subtotal` (or
  `tax.us.2025.citation.scheduleb-adjustment.nominee`) for the new reduction
  (inherited three-part reuse test already fails; reopen only if P2 produces
  new committed evidence that proposition, identity, and authority now match);
- treating one report’s over-allocation block as silently publishing an
  unreduced aggregate (Q7 requires dependent Schedule B and `taxable-total`
  to block while unrelated report-local outcomes may remain);
- treating a newly required Schedule B as a successful form adjustment
  without stating Part III completeness cardinality;
- binding the new prefix as a line-2b `requires` in a way that turns C0
  absence into a required zero.

#### How to read the inventory

Status:

- **Inherited** — previous closed milestones or committed artifacts already
  establish this; this milestone may not silently redefine it.
- **Verified (Pn)** — this milestone’s P1, P2, or P3 established the claim.
- **Selected default** — a bounded product default, not an implementation
  shape. The prototype uses it as a fixture.
- **Open (prototype)** — reserved for a future undecided prototype question; Q1/Q2 comparison and presentation carrier are closed.

Decision tag (`T0-F5`, `legacy`, `identity`, `shared vertical`): which of
the three isolated decisions, or the shared vertical, the row belongs to.

Failure effect:

- **Narrow** — drop or shrink a requirement; the vertical can continue.
- **Split** — the claim’s repair is a different milestone or owner decision.
- **Stop** — do not implement; return a decision or rescope.

Dependent sections use the current plan headings. If a claim fails, those
sections must be rewritten before they may be used as premises.

#### Tax meaning

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| T1 | IRC §61(a)(4) and Treas. Reg. §1.61-7(a) include the taxpayer’s own interest in gross income. They do not themselves prescribe a nominee subtraction or a beneficial-ownership test. | Inherited | shared vertical | Re-read those primary texts in P1. Falsified if they do prescribe the subtraction or a beneficial-ownership test this product would be implementing. | P1; Q6; Track 0 authority table; citation pins | Stop if the reduction’s legal basis was misstated. |
| T2 | The nominee subtraction is the 2025 Schedule B Part I *mechanic*: report the full amount including the nominee portion on line 1, subtotal, enter “Nominee Distribution,” subtract, enter the result on line 2. That instruction is form guidance, not controlling law. Previous Gate P1 verified this mechanic for an *internal* reduction that put nothing on the form. This milestone’s form-facing application was verified in P1. | Verified (P1) | shared vertical | Official 2025 Schedule B and instructions. Falsified if the form does not use this sequence, or if a controlling source independently requires a different subtraction. | P1; Q1; Q2; I1–I6; Selected product outcome 2 and 6 | Stop if the form mechanic is not this sequence. Narrow Q1 if the form requires a different displayed shape. |
| T3 | Line 3 is the series EE/I / §135 / Form 8815 exclusion. The nominee reduction affects line 2 and does not cure, implement, or occupy line 3. | Verified (P1) | shared vertical | Official 2025 Schedule B lines 2–4 and Form 8815 / §135. Falsified if nominee amounts are supposed to flow through line 3, or if connecting nominee silently fills the line-3 gap. | P1; Q6; I12; stop condition 5; Known limitations | Stop if the milestone would hide or fill the line-3 gap. |
| T4 | Schedule B line 4 is line 2 minus line 3 and is what reaches Form 1040 line 2b. The current `tax.us.2025.interest.taxable-total` is the engine’s bounded stand-in for that path, not a proof that line 3 is modeled. | Verified (P1) | shared vertical | 2025 Form 1040 line 2b instructions and Schedule B line 4; `rule.form1040-line2b` v6 `publishes`; Schedule B v5 `tie_out.line_symbol`. Falsified if those two symbols are being used as if they were complete line 4 / line 2b. | P1; Q6; I12; presentation wording checks | Stop if publication text would claim complete line 2b. Narrow wording if only the description is wrong. |
| T5 | The ordinary allocation is bounded evidence that interest belongs to another person *for applying the Schedule B mechanic*. It is not independently proven beneficial ownership. | Verified (P1) | shared vertical | Previous Gate P1 authority-basis section (not ADR-0074). Re-check that this milestone’s P1 does not upgrade the allocation into ownership. Falsified if this plan treats the allocation as a legal ownership finding. | P1; provenance; explanation | Stop if the product would publish ownership it has not established. |
| T6 | The duty to issue a Form 1099-INT to the actual owner (IRC §6049 and nominee/middleman regulations) is a different predicate. A supported reduction does not determine that duty. | Verified (P1) | shared vertical | Previous authority-basis section; P1 must not collapse the two. Falsified if Schedule B applicability or line-2b arithmetic is made to depend on a filing predicate. | P1; non-goals; Q4 | Narrow if a form instruction mentions 1099 issuance as a filing reminder only. Stop if the design requires the filing predicate. |

#### Schedule B applicability

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | The 2025 Schedule B instructions independently require the form when interest was received as a nominee, including when the ordinary dollar threshold is not exceeded. | Verified (P1) | shared vertical | Official 2025 “Who Must File” / Part I instructions. Falsified if nominee status is not an independent trigger, or if the trigger is different (for example, only when a 1099 was issued, or only above another amount). | Q4; I1; Selected product outcome 3; neighboring-capability diff | Narrow: drop the below-threshold trigger if the instructions do not require it. Stop if a different trigger is legally required and out of scope. |
| S2 | Current committed applicability is threshold-only: Schedule B v5 `requirement` is `strictly_greater_than` on `interest.positive-total` and `dividends.ordinary-total` versus parameter `$1,500`. Current nominee allocations are not a trigger. | Verified (P2/P3) | shared vertical | Read `rule.attachment.schedule-b.v5.json` `requirement`; execute a below-threshold nominee workspace in P3. Falsified if some other committed path already requires the attachment from nominee activity. | Current committed state; Q4; P2; P3 I1 | Narrow Q4 if the trigger already exists. |
| S3 | Absence of a current allocation is not a denial of nominee status and not a negative assertion that must be stored to keep Schedule B inapplicable. | Inherited / to extend | shared vertical | Previous C0-as-absence; P2 must trace whether a new trigger can appear and disappear from current support only. Falsified if the design needs a “no nominee” fact, or if retraction leaves the trigger on. | Q4; I0; I9; empty/nonempty matrix | Stop if absence is turned into a negative assertion. |
| S4 | Adding a nominee applicability trigger changes Schedule B’s no-activity path. The previous milestone’s neighboring-capability PASS recorded that *that* milestone did not impose this trigger; it did not forbid this milestone from doing so. The blast-radius review is now mandatory. | Verified as blast-radius (P2); trigger selected (Q4) | shared vertical | Previous next-stage contract and neighboring-capability artifact; P2 consumers of `attempt_attachment`; stop condition 6. Falsified if the trigger blocks a neighboring no-activity path for a reason that is not the neighbor’s own meaning. | Q4; Track 0 neighboring-capability diff; stop 6 | Stop (condition 6) or owner decision. Do not treat the previous PASS as a veto. |

#### Adjustment presentation

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | Official Schedule B presents nominee interest as a form-level “Nominee Distribution” adjustment after the line 1 subtotal, not as a requirement to list each recipient on Part I. | Verified (P1) | shared vertical | 2025 Schedule B Part I instructions: what must be listed vs what may be aggregated. Falsified if the form requires per-payer or per-recipient nominee rows as part of Part I. | Q1; I1; I2; I3; Selected product outcome 6 | Narrow Q1 if itemization is required. Do not infer engine report-scope into the form. |
| A2 | At the planning baseline, the engine published report-scoped `tax.us.2025.interest.nominee-reduction|{report_fact_id}` findings and did not feed them to line 2b or Schedule B. | Verified (P2 baseline); integrated by package v38 | shared vertical | `rule.interest.nominee-reduction.json`; package v36 membership; `rule.form1040-line2b.v6.json`; `rule.attachment.schedule-b.v5.json`. Package v38 is the successor observation. | Starting committed state; Q1; Track 1 | The baseline cannot be used as a claim about package v38. |
| A3 | Form-facing display may aggregate; reader-facing explanation and pins must still reach each contributing report-scoped reduction, current allocation, report finding, rule, and citation via top-level `provenanceGroups` (not extra `citationGroups.parts`). | Verified in production for I2/I3; I4 causal-block explanation deferred | shared vertical | `tests/test_nominee_interest_return_integration_track1.py` exercises the package-v38 presentation; `tests/derivation/test_attachment_rule_v11.py` checks the carrier contract and correspondence. Falsified if a flat leaf union is treated as grouping, if per-row form display is forced, or if blocked `citation_group=None` is called causal explanation. | Q1; Q2; I2; I3; I4; Selected product outcome 6 | Narrow the display shape. Stop (condition 3) if only a general adjustment framework can preserve both. |
| A4 | T0-F5 is real and neighboring: `rule.form1040-line2b` v6 subtracts `tax.us.2025.interest.current-year-adjustment-subtotal`; Schedule B v5 `tie_out.adjustment_subtotals` lists only legacy nominee and ABP. When the attachment is required and that subtotal is nonzero, `ITEMIZATION_TIE_OUT_VIOLATION` can fire. | Verified (P3) | T0-F5 | Reproduce through the real presentation path in P3. Falsified if current HEAD no longer fails, if the failure is not tie-out, or if it is caused by nominee rather than the missing pairing-scoped row. | Q2; I5; I6; stop 2; Track 0 known limitations | Narrow if already repaired. Stop if the defect cannot be repaired without erasing distinct accrued-interest and nominee authorities. |
| A5 | The same Schedule B derived-adjustment design must carry the pairing-scoped current-year adjustment and the new nominee adjustment without erasing their different source propositions or citations. Lineage for each kind uses top-level `provenanceGroups` (same typed carrier as A3/Q2); kinds remain distinct. | Verified in production for I5/I6 | T0-F5 | `tests/test_nominee_interest_return_integration_track1.py` exercises distinct nominee and accrued-interest rows, citations, and provenance under package v38. Falsified if one row/kind/citation is used for both or if a universal ledger is inferred from their shared carrier. | Q1; Q2; I5; I6 | Reopen only if another consumer requires a general adjustment framework. |
| A6 | The baseline `attachment-rule.v6` adjustment rows are family `collect_members` only; there is no derived-subtotal slot. | Baseline constraint verified; superseded for this capability by v11/v29 and Schedule B v7 | T0-F5 | The additive v11 successor and package-v38 content use declared `enumerate_published` rows and top-level `provenanceGroups`. Historical v6/v8 behavior remains covered by compatibility tests. | Q2; Contracts; Track 1 | Do not treat a fake family or a title comment as the production contract. |

#### Legacy meaning

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| L1 | The legacy fact `tax.us.2025.scheduleb.adjustment.nominee.amount` is a user-entered, tax-labelled Schedule B adjustment, keyed by tax year and adjustment instance, collected into `tax.us.2025.interest.scheduleb-nominee-subtotal`. It does not establish a report, recipient, ordinary ownership assertion, or attribution. | Verified (P2) | legacy | Family/bundle/fact-type keys; subtotal rule; P2 consumers. Falsified if the legacy fact already carries report/recipient identity. | Q3; I7; I8; Selected product outcome 4 | Narrow if correspondence is actually present. Stop if a design infers it anyway. |
| L2 | The new ordinary fact is `tax.us.nominee-allocation.amount`, keyed by payer, statement, tax year, and recipient. Neither identity system proves that one legacy amount is the same event as one new allocation or report. | Inherited / to extend | legacy | Fact-type keys; ADR-0074 topology; P2. Falsified if a committed correspondence edge exists. | Q3; I8; stop 1 | Stop (1) if a design needs invented correspondence. |
| L3 | Numeric equality is not correspondence. Automatic conversion is not a candidate unless evidence can supply the missing report, recipient, and attribution. | Selected default (Q3) | legacy | P3 both-present fixture with equal amounts and with unequal amounts. Falsified if the product treats equal amounts as the same event. | Q3; I8; stop 1 | Stop (1). |
| L4 | Today, a new-only workspace does **not** reduce line 2b (the new prefix is unpublished to that consumer). A legacy-only workspace **does** reduce line 2b via the legacy subtotal. Both-present currently subtracts only the legacy amount. Double subtraction is a risk *created by this milestone’s integration*, not current behavior. | Verified (P3) | legacy | P2/P3: new-only, legacy-only, both-present on current HEAD, then again under each candidate policy. Falsified if some path already subtracts the new prefix. | Q3; I0; I1; I7; I8; Track 1 | Narrow if current behavior already differs. Stop if no policy can avoid omission or double subtraction without invention. |
| L5 | ADR-0072 settled legacy *accrued-interest* vs pairing-scoped current-year adjustment. Method precedent: do not silently convert; do not treat equality as identity; a same-amount collision *trigger that requires resolution* is a method option, not conversion authority and not a nominee decision. False negatives (same obligation, mismatched amount) remain a named residual there. | Inherited | legacy | Read ADR-0072 Decision 2–3. Falsified if this plan cites it as the nominee answer, or forbids a same-amount collision check by calling equality “insufficient.” | Q3; deep_reads | Narrow the citation. Do not copy the accrued-interest retirement into nominee by resemblance. |

#### Identity

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | `facts._fact_id` joins `name=value` on `,` without escaping, so rendering is non-injective. A value containing `,<key-name>=` can collide with a different binding tuple. | Inherited | identity | Kernel `fact_id_for`; previous next-stage contract; coordinator comments. Falsified if rendering is now injective. | Q5; I11 | Narrow Q5 if the substrate was repaired elsewhere. |
| D2 | Recording contracts admit delimiter-shaped values. The coordinator’s `NomineeIdentityError` is an execution-time guard after `live_coordinate_run` has reserved outputs and appended the start record, leaving an open run and empty reserved outputs. It is not a product `Refusal` and not an intake gate. | Verified (P2/P3) | identity | P2 timing of start record vs coordinator; P3 reproduction of I11 on current HEAD. Falsified if the exception now fires before those effects, or if recording already refuses the values. | Q5; I11; Selected product outcome 8 | Narrow if already clean. Stop (4) if neither injective repair nor pre-run refusal is possible without a cross-project migration decision. |
| D3 | Closing this return path requires either a general identity repair or a declared pre-execution refusal before start-record and output-reservation. The bounded default is a pre-run check of identities the new path consumes. Ordinary commas in payer names and statement references are already supported and are not this hazard. | Selected default (Q5) | identity | P2 blast radius of a kernel identity change vs a nominee-path eligibility check; P3 before/after the proposed boundary. Falsified if a third smaller honest option exists, or if general repair is selected without a plain-language value case. | Q5; I11; stop 4 | Split general identity repair out of this vertical. Narrow to pre-execution refusal if that is sufficient. |

#### Authority, lifecycle, and provenance

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| Pv1 | Current attributed allocations for one identified report produce one report-scoped nominee reduction (or a report-scoped block). Pins name the current report finding and every current allocation in the group. Attribution stays on the allocation’s assertion act. | Inherited | shared vertical | ADR-0074; nominee rule; coordinator; previous Track 2 live evidence. Falsified if this milestone re-keys, copies attribution into the tax proposition, or collapses several reports into one reduction before provenance is recorded. | Q1; Selected product outcome 1 and 6; I2; I3 | Stop if provenance cannot survive the form-facing shape. |
| Pv2 | C0-as-absence: a report with no current allocation produces no nominee publication and no per-report nominee row. Whole-universe report-only or empty is one unsuffixed `inapplicable` / `no_groups_selected` row. Absence is not a `$0` reduction. | Inherited | shared vertical | Previous next-stage contract; R2/R3. Falsified if line-2b integration silently turns absence into a required zero subtractand or a closed empty family the way the legacy nominee family works. | Q1; Q4; I0; I9; empty/nonempty matrix; stop 6 | Stop or owner decision if binding the new prefix to line 2b forces a false zero. This is a first-class P2 cardinality question. |
| Pv3 | Over-allocation blocks the dependent nominee result with `NOMINEE_ALLOCATIONS_EXCEED_REPORT`. No clamp, subset, negative remainder, or silent unreduced success. Unrelated report groups are not suppressed. | Inherited | shared vertical | Nominee rule `when`/`block`; previous C4/C10/C12. Falsified if form aggregation would pick a subset or continue with the unreduced taxable-total. | I4; I10; Selected product outcome 7 | Stop if the form-facing total cannot preserve report-local blocking. |
| Pv4 | A current allocation whose report finding no longer stands fails closed with a report-scoped reason. No historical amount or zero is substituted. | Inherited | shared vertical | Previous C13; P2 of the production input path. Falsified if the return path substitutes or omits the failure. | I10 | Stop if the return consumer would succeed on a missing report. |
| Pv5 | Correction, retraction, and reassertion change only current support. Historical assertions remain recoverable and do not contribute. | Inherited | shared vertical | ADR-0073; previous C6; extend to Schedule B trigger and line 2b in I9. Falsified if a retracted allocation still reduces line 2b or still requires Schedule B. | I9; Q4; late-authority counterexample | Stop if lifecycle does not reach the new consumers. |
| Pv6 | The current result is a `RunResult` publication, not act-log standing. This milestone does not mint provisional-return standing or durable publication of `RunResult` findings. | Inherited | shared vertical | Publication and wording checks on this milestone’s fixtures, goldens, and status lines. Falsified if presentation or line 2b is described as a filed or standing return. | Q6; wording checks | Narrow wording. Stop if the product would claim filing support. |
| Pv7 | Remainder is observed-only. The `$750` in the product story is the bounded post-subtraction taxable-interest figure after a `$450` reduction, not a published remainder finding. | Inherited / to protect | shared vertical | Previous remainder policy; P2 of what line 2b actually publishes. Falsified if the milestone publishes remainder or treats `taxable-total` as a remainder citizen. | Q1; Q6; I1 | Narrow the story. Do not add a remainder publication to make the form easier. |

#### Calculation and bounded claim

| ID | Claim | Status | Decision | Verify or falsify | Depends | Failure |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | The bounded taxable-interest result must subtract a supported current nominee consequence exactly once. | Verified in production | shared vertical | Package-v38 I0–I8 cases exercise exactly-once, absent, blocked, and legacy/new paths. Falsified if the new aggregate is omitted, subtracted twice, or combined with a live legacy nominee amount. | Selected product outcome 1 and 5; I1–I8; Track 1 | Reopen if a successor changes the selection contract. |
| C2 | Pairing-scoped current-year adjustment and ABP remain subtractands of line 2b. Schedule B must account for the same adjustments without dropping or doubling them. | Verified in production; T0-F5 closed | T0-F5 | Package-v38 I5/I6 cases tie out nominee and accrued-interest adjustments under distinct rows and provenance. Falsified if nominee work removes an existing subtractand or double-subtracts accrued interest. | Q2; I5; I6; neighboring-capability diff | Reopen if a neighboring adjustment regresses. |
| C3 | Binding the new prefix into line 2b makes the Track 0 integration-surface artifact mandatory. Cardinality of absence, block, one report, and several reports must be stated for every consumer, including presentation joins. | Verified (P2) | shared vertical | PROJECT_PLANNING integration-surface gate; previous next-stage contract (“Not bound to line 2b”). Falsified if a charter proceeds without the artifact, or if paper models replace real-consumer models. | P2; P3; Track 0 artifact 6; Contracts | Stop Track 0 until the surface is built. |
| C4 | Fixtures in this milestone must exclude Form 8815 / §135 and other unsupported interest categories. Success may not rename `taxable-total` as complete 2025 taxable interest. | Verified as non-claim (P1); keep wording checks | shared vertical | I12; negative wording/structure checks; P1 boundary of unsupported categories. Falsified by any publication, golden, or status line that calls the result complete line 2b. | Q6; I12; stop 5; Exit criterion 9 | Stop (5). |

#### Missing questions — absorbed

Independent review found all five original missing questions to be real
omissions. Owner-directed correction 2026-09-10 closed Part III as current
completeness (two observations, one policy), Q7 as dependent-block
semantics, Q3 and Q5 as bounded defaults, and Q1 as two end-to-end
candidates rather than a presentation-only rival.

#### Review result

Independent review 2026-09-10: **REPAIR**, four blocking and five
non-blocking findings, absorbed above. Economic decision: remain one unit
until P2/P3; not split then.

### P1 — tax and form boundary — **PASS (findings absorbed)**

Paper gate against official 2025 form and instruction text. It does not
select a Q1 candidate, a schema, or a package. Controlling legal claims use the Code
and Treasury regulations. Schedule B and Form 1040 instructions establish
the reporting mechanic only. IRS publications are explanation, not authority.

Independently reviewed 2026-09-10. Verdict **READY**; two non-blocking
findings absorbed here. No mechanism was selected at P1.

#### Sources and what they establish

| Source | What it is used for here | What it does not establish |
| --- | --- | --- |
| IRC §61(a)(4) | Interest is an item of gross income | A nominee subtraction, a beneficial-ownership test, or Schedule B |
| Treas. Reg. §1.61-7(a) | General rule that interest is included in gross income | The Schedule B nominee line, Form 8815, or information-return duties |
| 2025 Instructions for Schedule B (Form 1040), IRS.gov/instructions/i1040sb | Who Must File, Part I line 1, the Nominees mechanic, Accrued interest / OID / ABP labels, line 3 pointer to Form 8815 | Controlling law; a per-recipient Schedule B row; that issuing Form 1099-INT is a condition of the line 1→2 arithmetic |
| 2025 Schedule B (Form 1040) face | Line 1 payer list; line 2 = sum of line 1; line 3 Form 8815; line 4 = line 2 − line 3, “enter on Form 1040 line 2b”; Part III completion note | A software completeness contract; engine `taxable-total` meaning |
| 2025 Instructions for Form 1040, line 2b | Enter total taxable interest on line 2b; attach Schedule B if the total is over `$1,500` **or any other condition listed at the beginning of the Schedule B instructions applies** | Complete taxable-interest coverage; Form 8815 arithmetic |
| 2025 Form 8815 | Figures excludable series EE/I interest for qualified higher-education expenses; line 14 “enter on Schedule B line 3” | Nominee interest; a general line-2b model |
| IRC §135 | Statutory home of the education savings bond exclusion that Form 8815 computes | Nominee interest |
| IRC §6049 and nominee/middleman regulations | Named only to keep the information-return predicate separate | Not used as a Schedule B or line-2b requirement in this milestone |

Previous Gate P1 already bounded the *internal* reduction to §61(a)(4) /
§1.61-7(a) plus the Schedule B mechanic. This P1 is the form-facing
application of that mechanic (P0 T2, N1). It does not re-open the two-predicate
split: a supported reduction does not determine a §6049 filing duty.

#### Who Must File

2025 Schedule B instructions, General Instructions: use Schedule B if **any**
of the following applies.

1. Over `$1,500` of taxable interest or ordinary dividends.
2. Interest from a seller-financed mortgage where the buyer used the property
   as a personal residence.
3. Accrued interest from a bond.
4. OID less than the Form 1099-OID amount.
5. Interest less than the Form 1099 amount because of amortizable bond
   premium.
6. Claiming the exclusion of interest from series EE or I U.S. savings bonds
   issued after 1989.
7. **Received interest or ordinary dividends as a nominee.**
8. Foreign financial account or foreign trust.

**S1 holds** for nominee *interest*. Item 7’s official text also covers
nominee ordinary dividends; that limb is a neighboring Who Must File gap,
not Q4. Q4 is the interest-nominee limb of item 7. Items 2–6 and 8 remain
neighboring gaps. Nominee status for interest does not depend on the
`$1,500` amount test. Form 1040 line 2b instructions confirm the same
disjunction: attach Schedule B if the total is over `$1,500` *or* any other
Schedule B Who Must File condition applies. Item 3 (accrued interest from a bond) is the neighbor of T0-F5’s
pairing-scoped subtractand; this milestone repairs that subtractand’s
*itemization when Schedule B is already required*. It does not, by P0 scope,
add an accrued-interest Who Must File trigger. Record that as a neighboring
non-claim so P3 I5 is not mistaken for a below-threshold accrued trigger.

#### Part I sequence: line 1 → 2 → 3 → 4 → Form 1040 line 2b

From the 2025 form face and instructions:

- **Line 1.** Report **all** taxable interest, listing each payer’s name and
  amount. Include the nominee portion. Do this even if some or all of the
  income was later distributed. Do not report tax-exempt interest here.
- **Nominee Distribution (between line 1 and line 2).** Under the last line 1
  entry, subtotal all interest listed on line 1. Below that subtotal, enter
  “Nominee Distribution” and show **the total** interest received as a nominee.
  Subtract that total from the subtotal.
- **Line 2.** Enter the result of that subtraction. The form face also labels
  line 2 “Add the amounts on line 1”; the Nominees instruction is the
  authorized way those amounts are reduced before the figure that proceeds
  toward line 4. P1 does not treat the face “Add” label as cancelling the
  Nominees instruction.
- **Line 3.** Excludable interest on series EE and I U.S. savings bonds issued
  after 1989; attach Form 8815. Form 8815 line 14 is the amount that enters
  Schedule B line 3. This is IRC §135, not nominee interest.
- **Line 4.** Subtract line 3 from line 2. Enter the result on Form 1040 or
  1040-SR, line 2b.

**T3/T4 hold as form mechanic.** The nominee reduction is a line 1→2
adjustment. It does not occupy, compute, or cure line 3. Connecting nominee
cannot make `tax.us.2025.interest.taxable-total` a complete line 4 / line 2b
model while line 3 is unimplemented. I12 and Q6 remain.

The engine today uses `taxable-total` as both Schedule B Part I `tie_out.line_symbol`
and the line-2b publication. That is a bounded stand-in for the path from
line 2 toward line 2b in fixtures that exclude the Form 8815 condition. It
is not proof that line 3 is modeled.

#### What the form requires to itemize

Line 1 itemizes **payers and full reported amounts**, including nominee
portions. The nominee subtraction is **one form-level total** labeled
“Nominee Distribution.” The instructions do not require listing each
recipient, and do not require a separate nominee row per payer, on Part I.

**A1 holds as form mechanic.** Q1’s live candidates are two end-to-end
aggregations consumed by both line 2b and Schedule B, not a presentation-only
total. Per-allocation or per-report Schedule B rows are an engine
provenance need, not a form itemization requirement. Report-scoped engine
structure still must survive internally (P0 A3, Selected product outcome 6).

The same between-line-1-and-2 slot is reused, with different labels, for
Accrued Interest, OID Adjustment, and ABP Adjustment. That is why T0-F5 and
nominee must keep distinct labels, citations, and source propositions on a
shared Schedule B surface (Q2, I5, I6). Resemblance of the slot is not
permission to reuse `scheduleb-nominee-subtotal` or the legacy nominee
citation for a pairing-scoped or report-scoped derived reduction.

#### Information returns are a different instruction

Immediately after the Nominees arithmetic, the Schedule B instructions say
that if you received interest as a nominee you must give the actual owner a
Form 1099-INT (unless the owner is your spouse) and file Forms 1096 and
1099-INT. That sentence is a filing reminder. It is not a condition of the
line 1→2 subtraction, not a Schedule B Who Must File substitute, and not
in this milestone’s product (T6, non-goals).

#### Completeness when nominee newly requires Schedule B

Two official rules are not the same:

- **Who Must File** requires the schedule if nominee interest was received,
  even below `$1,500`.
- **Part III completion** is stated three times on the face: the Part III
  header (complete if (a) over `$1,500` of taxable interest or ordinary
  dividends, (b) a foreign account, or (c) a foreign trust); after line 4,
  “If line 4 is over `$1,500`, you must complete Part III”; after line 6,
  the same for line 6. Nominee is on none of those lists. Header (a)’s
  “taxable interest” is not treated here as a pre-nominee line 1 total.
  Option (ii) below uses the more specific line 4 note; that is a reading,
  not a selection.

The committed engine is stricter than that Part III note: once Schedule B is
required, v5 `completeness.required_answers` always demand
`foreign-account` and `foreign-trust`. Adding the nominee trigger therefore
newly obliges those answers for a below-threshold nominee user who previously
had no Schedule B.

**Selected for this milestone:** keep that current evidence requirement.
Successful I1 supplies `"no"` / `"no"`. The same workspace with those
answers missing is required-and-incomplete. Those are two observations
under one policy. Absence of foreign facts is not a `"no"`. Conditional
Part III completeness is deferred unless the Q1/Q2 prototype proves current
completeness prevents an honest nominee integration.

#### Bounded claim this section licenses

After P1, the plan may treat as form-established:

1. Nominee interest independently requires Schedule B (Q4 remains the
   *engine* trigger design; the form requires the trigger).
2. Line 1 includes nominee amounts; one “Nominee Distribution” total is
   subtracted to reach line 2; line 4, after line 3, is what the instructions
   send to Form 1040 line 2b.
3. Line 3 / Form 8815 / §135 is a different subtraction. Nominee does not
   fill it.
4. Part I does not require per-recipient nominee itemization.
5. Form 1099-INT issuance is not the Schedule B arithmetic.

P1 does not treat as established: beneficial ownership; complete 2025
taxable interest; engine completeness = official Part III note; accrued-
interest Who Must File; a Q1 candidate.

#### Review must attack

- whether any legal proposition is sourced only to instructions or Pub. 550;
- whether line 2’s face “Add the amounts on line 1” has been used to deny
  the Nominees subtraction;
- whether S1 has been stretched to require Part III, information returns, or
  per-recipient rows;
- whether line 3 has been described as cured;
- whether neighboring Who Must File items (accrued interest, ABP, Form 8815,
  foreign accounts) have been silently pulled into Q4.

Independently review this bounded section before it becomes the premise of
the artifact design.

### P2 — committed artifact and consumer map — **PASS (findings absorbed)**

Committed-path inspection of HEAD after P1. It does not select a Q1 candidate
or a successor shape. Live execution is `live_coordinate_run` →
`marshal_live_run_context` → `execute_and_record_marshaled`. Ratified package
is `package.core-calculations` v36 (`artifact-package.v28`).

Independently reviewed 2026-09-10. Verdict **READY**; two non-blocking
findings absorbed here. No successor was selected at P2.

#### Recording, currentness, attribution

`tax.us.nominee-allocation.amount` is keyed `payer` + `statement` +
`tax-year` + `recipient`, sharing the box-1 identity components. The legacy
nominee amount is keyed `tax-year` + `adjustment-instance` only. Neither
carries the other’s keys (L1/L2 confirmed).

`assert_nominee_allocation` / `retract_nominee_allocation` write ordinary
acts. Current standing is `compute_currency` only. Correction is a later
finding on the same `fact_id`. Cardinality: at most one current finding per
allocation fact id; 0..n recipients per report.

Two readers are not interchangeable. `recover_nominee_allocations` is
attribution/UI and tests only; it is not a derivation input.
`marshal_run_context` projects current findings whose types are in
`collect_source_names`. When v36 includes the nominee rule,
`live.py` appends `COLLECT_SOURCE_NAMES` = allocation + box-1. Package
`input_bindings` do not name those facts.

Attribution (`actor`, `at`) lives on the act log. Nominee-reduction pins are
finding ids of the current report and allocations, plus rule, citation
`tax.us.2025.citation.interest.nominee-reduction`, adoption, and governance.
Actor/time and recipient labels are not copied into the tax proposition
(Pv1).

Neighboring fields not relied on: `recipient_display_label` as identity;
allocation `source_amount` (the type is not a source-amount); box-1 family
closure (the coordinator does not require it).

#### Report-scoped nominee consequence

`rule.interest.nominee-reduction` (`rule-artifact.v8`) uses `bound_sources`
of the allocation type against the identified box-1 amount. The coordinator
groups by report, builds a local env, and publishes or blocks
`tax.us.2025.interest.nominee-reduction|{report_fact_id}`.

| State | Disposition | Symbol cardinality |
| --- | --- | --- |
| Report, no current allocations (C0) | skip; no per-report row | 0 for that report |
| Whole universe report-only or empty | one `inapplicable` / `no_groups_selected` | 1 unsuffixed prefix |
| Allocations, no current report (C13) | `DEPENDENCY_ABSENT`, `missing=[report_fact_id]` | 1 suffixed block |
| Sum > report | `NOMINEE_ALLOCATIONS_EXCEED_REPORT`, empty `missing` | 1 suffixed block |
| Sum ≤ report | published sum | 1 suffixed publication |

v36 admits the rule and allocation vocabulary. **Nothing in v36 binds the
new prefix** as a `requires`, form-field, or Schedule B itemization (A2/L4
confirmed by grep of line 2b v6, Schedule B v5, and form-field v5).

`walk_npe` matches `publishes == symbol` exactly. Walking a suffixed group
symbol finds no producer. Line-2b presentation citations walk leaf pins of
`taxable-total`, which today do not include nominee-reduction findings.

#### Legacy nominee and pairing-scoped subtractands

Legacy path: closed family `tax.us.2025.scheduleb.adjustment.nominee` →
collect of tax-labelled amounts →
`tax.us.2025.interest.scheduleb-nominee-subtotal` (one unsuffixed symbol;
empty closed family publishes rounded 0). Line 2b v6 `require_closed` that
family and subtracts the subtotal. Schedule B v5 itemizes it as
`nominee_distribution` via `collect_members`.

Pairing-scoped path: suffixed
`tax.us.2025.interest.current-year-adjustment.pairing-scoped|{pairing_fact_id}`
→ dispatcher sums to `current-year-adjustment-subtotal` (empty set publishes
0). Line 2b v6 subtracts that subtotal. **Schedule B v5 does not itemize it**
(T0-F5 / A4). `attempt_attachment` Part I `part_sum` = positive row-sets −
listed adjustment rows, then `part_sum != taxable-total` →
`ITEMIZATION_TIE_OUT_VIOLATION`. Because `taxable-total` also subtracts the
pairing-scoped subtotal, a nonzero pairing subtotal with a required
attachment is the failing mechanism. P3 must still reproduce it through the
real presentation path.

#### Bounded line 2b and Schedule B

`rule.form1040-line2b` v6 publishes `tax.us.2025.interest.taxable-total`:
seven positive subtotals minus legacy nominee, ABP, and pairing-scoped
current-year subtotals. Form-field v5 `binds_symbol` that total as line 2b.
Schedule B v5 Part I `tie_out.line_symbol` is the same total. Requirement is
`strictly_greater_than` on `interest.positive-total` and
`dividends.ordinary-total` versus `$1,500`. Completeness always requires
`foreign-account` and `foreign-trust` once the attachment is required (P1).

`family_nonempty` exists (Schedule D) but is **not** Schedule B’s
requirement. Nominee allocations have **no** source family or closure
mapping. Q4 cannot use `family_nonempty` on allocations without introducing
the family/closure the previous milestone forbade. Q2 cannot itemize a
derived reduction in published `attachment-rule.v6` adjustment rows without
a family wrap or a successor grammar (A6).

No Schedule B form-field. Presentation `_resolve_attachment` joins
`tax.us.2025.scheduleb.disposition`. Nominee rows cite **legacy** member
finding ids, not allocation findings.

#### Identity failure timing

`facts._fact_id` joins `name=value` on `,` without escaping. The coordinator
raises `NomineeIdentityError` in `_build_universe` during
`dispatch_nominee_consequences_on_run`. Through `live_coordinate_run` that
is after output reservation and after `start_run` (`phase: started`). The
completed record is not written; reserved outputs stay empty. The guard
inspects **nominee reports and allocations only**. Other return-path facts
are not in this check (Q5 universe). Pinned by
`test_identity_guard_is_an_in_flight_exception_not_a_pre_run_refusal`.

#### Integration surface (current bindings)

| Consumer | Binding | Cardinality it expects | Satisfied by current design? |
| --- | --- | --- | --- |
| Nominee coordinator | current box-1 + allocation `SourceFact`s | 0..n allocation groups; 0 or 1 current report finding per report fact id | Yes, for uniquely rendered identities |
| `rule.interest.nominee-reduction` | local `bound_sources` + report amount | one group env per selected report | Yes |
| Line 2b v6 | `scheduleb-nominee-subtotal` (legacy), ABP, `current-year-adjustment-subtotal`; **not** the new prefix | exactly one of each named subtotal | Yes; new prefix unbound |
| Form-field line 2b | `taxable-total` | exactly one | Yes |
| Schedule B v5 requirement | positive-total / ordinary-dividends vs `$1,500` | any subtotal strictly greater | Yes; no nominee trigger |
| Schedule B v5 Part I rows | `collect_members` of legacy nominee + ABP families | 0..n members per family | Yes |
| Schedule B v5 Part II | `dividends.1a-subtotal` itemization once required | exactly one subtotal symbol present | Yes today when required; a below-threshold nominee trigger would newly demand this symbol even if the dividend family was never closed |
| Schedule B v5 completeness | `foreign-account`, `foreign-trust`; `7b-country` / `FINCEN_114_NAMED` if foreign-account is yes | presence, then branch | Yes once required; this milestone keeps that requirement |
| Schedule B v5 tie-out | `part_sum` vs `taxable-total` | equality | **No** when pairing-scoped subtotal ≠ 0 and attachment required (T0-F5) |
| Schedule B presentation | `scheduleb.disposition` | exactly one disposition | Yes when attachment runs |
| Line 9 v7 / SS worksheet v3 | `taxable-total` | exactly one | Yes; blast radius of any line-2b change |
| `walk_npe` on suffixed nominee-reduction | `publishes == symbol` | producer rule | **No** for suffixed symbols |
| Explanation of line 2b | leaf pins of `taxable-total` | walkable inputs | Does not reach new allocations today |

#### Implications after P0–P3 (historical; Q1/Q2 since closed)

- **Q1.** Presentation-only totals are rejected: line 2b and
  `attempt_attachment` run before `_resolve_attachment`. Two end-to-end
  candidates remain (shared derived subtotal vs shared enumeration of
  suffixed outcomes). Reuse of `scheduleb-nominee-subtotal` still fails the
  three-part test. The unsuffixed prefix is never a published numeric.
  Inventing a `$0` fact for I0 is rejected.
- **Q2.** No derived-subtotal slot in published `attachment-rule.v6`. Q2 is
  how the selected Q1 candidate itemizes nominee and pairing-scoped accrued
  interest under distinct citations and ties out to line 2b. Not a universal
  ledger.
- **Q3.** Selected default: legacy-only compatible; new-only new path;
  both-present refuses. Current HEAD subtracts only legacy.
- **Q4.** Form requires the interest-nominee trigger; engine is still
  threshold-only. Completeness stays the current foreign-account /
  foreign-trust evidence requirement. I1 success supplies `"no"` answers;
  missing answers block. Part II `1a-subtotal` is still a consumer of a
  newly-true `required`.
- **Q5.** Selected default: pre-run check of every nominee report/allocation
  identity the new path consumes. General fact-id redesign is out unless the
  prototype proves the bounded check cannot be honest.
- **Q7.** Selected: report-local outcomes may survive; dependent aggregate,
  Schedule B, and `taxable-total` block.
- **C3.** Binding the new path makes the integration-surface artifact
  mandatory for Track 0. The Q1/Q2 prototype must execute I0, I1, I4, I5,
  and I6 through the real consumers.

#### What paper inspection did not settle (now the prototype’s job)

- Which Q1 candidate can supply the same amount and authority to line 2b and
  Schedule B without a universal ledger.
- Whether an additive attachment-rule successor is required for two derived
  adjustment rows with distinct citations (payload instance if selected).
- Exact insertion of the pre-run identity check relative to output
  reservation and `start_run`.

#### Review must attack

- any consumer of the new prefix this map omitted;
- any claim that recovery is a derivation input;
- any use of `family_nonempty` or a new allocation family as a silent Q4;
- reuse of `scheduleb-nominee-subtotal` as if P2 found new three-part-test
  evidence;
- treating T0-F5 as a nominee defect;
- treating this map as a selected successor.

Independently review this map before selecting a successor shape.

### P3 — executable comparison — **PASS (findings absorbed)**

Disposable probes on v36 through `live_coordinate_run` (never a `RunContext`
shortcut). Existing live tests cited below were re-run the same day. P3’s Q1
comparison named a presentation-only total as a rival; that comparison is
now rejected (line 2b and `attempt_attachment` precede
`_resolve_attachment`). The remaining rivals were the two end-to-end
candidates in Q1. This P3 section remains the record of pre-integration v36
behavior.

Independently reviewed 2026-09-10. Verdict **READY**; one non-blocking
finding absorbed (T0-F5 probe now pins presentation `activeCodes`). Track 0
was not ready at that gate.

#### What was executed

| Probe | Path | Observation |
| --- | --- | --- |
| T0-F5 | `_t2_acts` with box-1 `$2,000`, pairing-scoped current-year subtotal nonzero, Part III answers `no`/`no`, v36 adoption; `live_coordinate_run` + presentation JSON | `current-year-adjustment-subtotal` `$42`; Schedule B report `ITEMIZATION_TIE_OUT_VIOLATION`; presentation attachment `blocked` with the same `activeCodes`. `part_sum` `$2,000` vs `taxable-total` `$1,958`. A4 holds on the real attachment path. |
| I1 current / Q4 | C1 workspace `$1,200` + `$450` allocation, v36 | Suffixed nominee-reduction `$450` publishes; Schedule B disposition is `inapplicable`. The form-required below-threshold trigger is absent. |
| I8 current / Q3 | C1 plus legacy nominee `$100` closed family | `b1-subtotal` `$1,200`; `scheduleb-nominee-subtotal` `$100`; `taxable-total` `$1,100`. The new `$450` is not a line-2b subtractand. Double subtraction is not current behavior; it is the risk of connecting the prefix without a Q3 policy. |
| I0 / C0 | `test_c0_no_groups_selected_and_box1_still_calculated` | No suffixed nominee publication; box-1 still calculated. |
| I11 current / Q5 | `test_identity_guard_is_an_in_flight_exception_not_a_pre_run_refusal` | `NomineeIdentityError` after start record; reserved outputs exist and are empty; no completed record. The guard is nominee-source-scoped. |

All five executed. Identity *after* a proposed pre-execution boundary was not
executed, because no such boundary is selected.

#### What the probes discriminate

- **Q4.** Current engine: threshold only. Form (P1): interest-nominee is an
  independent Who Must File limb. I1 success as a form adjustment is not
  current behavior.
- **Q3.** New-only and both-present currently reduce line 2b only by legacy.
  A candidate transition policy was not executed; numeric equality was not
  treated as correspondence.
- **Q1/Q2.** Suffixed publications exist on `RunResult` and are invisible to
  Schedule B presentation and line 2b. Neither end-to-end candidate is a
  no-code path. Published `attachment-rule.v6` still has no derived-subtotal
  slot. **(Discharged.)** The Q1/Q2 prototype ran the two complete candidates
  through calculation, `attempt_attachment`, and `_resolve_attachment`,
  covering I0, I1, I4, I5, and I6.
- **Q5.** Current failure is mid-run. The bounded default is a pre-run
  check; the prototype must place it before start-record if the selected
  candidate consumes those identities.
- **Q7.** Inherited live C4 still blocks the nominee row only. The selected
  dependent-block semantics are a prototype obligation, not an owner choice.

#### What P3 does not select

No schema, package, attachment successor, legacy policy, identity remedy, or
completeness policy. No candidate derived-adjustment row was patched into
production content.

#### Review must attack

- whether T0-F5 was observed on v36 presentation/attachment, or only argued
  from arithmetic;
- whether I1’s inapplicable Schedule B has been mistaken for a successful
  form adjustment;
- whether this section claims a Q1/Q2 composition that was not built;
- whether Track 0 is being treated as ready despite the named prototype
  gap.

Independently review this evidence before chartering Track 0.

## Fixed cases

All values and identifiers are synthetic. Each case must distinguish current
committed behavior, selected behavior, implementation work, and what the case
does not establish.

| Case | Decision | State | Required observation |
| --- | --- | --- | --- |
| I0 — no nominee activity | shared vertical | Report A `$1,200`; no current new allocation; no legacy nominee amount; no pairing adjustment | Existing bounded interest result is unchanged; no nominee row, no invented `$0` fact, no false denial; Schedule B applicability follows its other valid triggers. |
| I1 — below-threshold nominee | shared vertical | Report A `$1,200`; demo.pat allocation `$450`; no other Schedule B trigger; foreign-account and foreign-trust answers `"no"` | Nominee independently requires Schedule B; one `$450` form adjustment; bounded post-adjustment result `$750`; exact report/allocation provenance. The same workspace without those Part III answers is required-and-incomplete, not a competing policy. |
| I2 — several recipients | shared vertical | Report A `$1,200`; demo.pat `$300`; demo.kim `$150`; Part III `"no"`/`"no"` | Form-facing nominee total `$450`; internal provenance retains both allocations and the report; result `$750`. |
| I3 — several reports | shared vertical | Reports A and B; current allocations on both | Form-facing total equals the sum of supported report reductions while report-local provenance and blocking remain separate |
| I4 — over-allocation | shared vertical | Report A `$1,200`; allocations total `$1,250` | Report-scoped nominee block; no clamp, subset, negative remainder, or silent unreduced nominee success; unrelated report-local outcomes remain available. The aggregate nominee adjustment, Schedule B, and bounded `taxable-total` that depend on this unresolved group block. They do not omit the group or publish the unreduced number. |
| I5 — T0-F5 accrued adjustment | T0-F5 | Schedule B required; supported nonzero pairing-scoped current-year adjustment | Schedule B represents the subtraction and ties to the bounded return result; current failing behavior is first reproduced |
| I6 — nominee plus accrued adjustment | T0-F5 | Supported nominee and pairing-scoped reductions in one run | Each appears under its own meaning and authority; both are subtracted once; Schedule B tie-out succeeds |
| I7 — legacy only | legacy | Current legacy nominee adjustment; no new allocation | Legacy path remains compatible and explicitly legacy; no invented report or recipient |
| I8 — new and legacy both present | legacy | Current legacy amount and current new allocation | Refused pending explicit resolution. No double subtraction, no inferred correspondence, no conversion by amount. |
| I9 — allocation lifecycle | shared vertical | I1, then correction, retraction, and reassertion | Each new execution and Schedule B trigger uses only current support; historical assertions remain recoverable but do not contribute. Applicability follows Q4 when the last current allocation is retracted. Part III remains the current evidence requirement on any required Schedule B. |
| I10 — missing current report | shared vertical | Current allocation whose report finding no longer stands | Report-scoped nominee path fails closed; no historical amount or zero is substituted. Unrelated report-local outcomes may remain. The aggregate nominee adjustment, Schedule B, and bounded `taxable-total` that depend on this group block. |
| I11 — ambiguous rendered identity | identity | Delimiter-shaped identity accepted by existing recording | Pre-run check covering every nominee report/allocation identity the new aggregation and presentation path consume refuses before start-record and output reservation. |
| I12 — unsupported line-3 condition | shared vertical | Synthetic facts that would require a section 135/Form 8815 treatment | The milestone does not publish or describe the bounded result as complete line 2b; the known gap remains explicit |

## Scope

### Included

- The bounded 2025 nominee reduction, its form-facing aggregation or
  projection, Schedule B Part I adjustment presentation, attachment
  applicability, tie-out, and the current line-2b consumer.
- The pairing-scoped current-year adjustment only to the extent necessary to
  repair T0-F5 and make the shared Schedule B surface honest.
- The legacy nominee adjustment only to select and execute a safe compatibility,
  transition, or refusal policy.
- The identity boundary only to make this execution path succeed or refuse
  before durable run effects.
- Additive schema, package, rule, presentation, or record successors proved
  necessary by the reviewed design.

### Excluded

- Complete taxable-interest coverage, Form 8815 implementation, general
  Schedule B “Who Must File” coverage beyond the nominee trigger, or filing.
- Nominee information-return predicates and output.
- General migration of unrelated Schedule B adjustments.
- Product UI for entering allocations or resolving legacy records.
- A general-purpose adjustment or identity abstraction not forced by these
  cases.

## Contracts

Track 0 selected these contracts. The contract unit published the additive
schema successors and their canonical positive instances; Track 1 adopted
them in package v38. The disposable fake-family comparison was not promoted.

- **Attachment-rule successor** for derived adjustment rows (nominee
  dispatcher B + pairing-scoped accrued interest). Not a universal ledger.
- **Artifact-package successor** admitting that attachment-rule schema. The
  predecessor package grammar stopped at attachment-rule.v8. Package v38 now
  adopts Schedule B v7 under the successor grammar.
- **Presentation carrier:** top-level `provenanceGroups` (one per
  contributing report-scoped reduction), projecting recorded pins under a
  reader `label` distinct from the machine symbol; finding id is an
  identifiable grouping node, not a claimed resolvable site.
  `citationGroups.parts` remain ADR-0056 itemization only. Not a flat union
  of all leaves treated as grouping.
- **Line 2b successor** that subtracts the dispatcher aggregate on the new
  path, does not `require` it on I0, and blocks when a consumed group is
  unresolved (Q7).
- **Bounded declared path contract (this contract unit):** additive
  `rule-artifact.v9` plus `artifact-package.v30`. The exact
  `tax.us.2025.rule.form1040-line2b@v8` citizen declares the neither/legacy/new
  selection, dependencies, selected expressions, pins, and both-active refusal;
  the exact `tax.us.2025.rule.interest.derived-nominee-subtotal@v1` citizen owns
  the unsuffixed aggregate and enumerates only current suffixed nominee
  reductions. The schema syntax is general enough to be inspected, but package
  validation and runtime bind it only to these exact identities; copied syntax
  is inert and refused.
- **Schedule B nominee-applicability trigger** from current nominee
  activity (Q4), keeping current Part III evidence requirements.
- **Legacy:** compatible legacy-only; new-only uses dispatcher B;
  both-present refuses (Q3).
- **Identity:** pre-run refusal of consumed nominee report/allocation
  identities (Q5). Not a general fact-id redesign.
- **Presentation** projects recorded provenance; it does not recompute tax.

If accepted ADR text must change, write one successor decision before code
depends on it; do not edit accepted history.

## Fixtures

- One committed synthetic workspace per materially different I0–I12 path that
  survives P3 selection.
- A canonical T0-F5 regression fixture reproducing the current Schedule B
  tie-out failure before the repair.
- A below-threshold nominee fixture proving applicability independently of the
  amount threshold.
- Legacy-only, new-only, and both-present fixtures proving the selected policy.
- Exact presentation models or canonical projections for successful, blocked,
  and inapplicable paths.
- An ambiguous-identity fixture proving either distinct identity preservation
  or refusal before durable start/output effects.

## Verification

Use the cheapest focused tests during each unit. Because the likely work
touches `packages/derivation/`, every substrate-changing implementation unit
also runs the full suite before handoff; CI remains the merge gate of record.

The final evidence must include:

- exact arithmetic and no-double-subtraction assertions;
- Schedule B applicability below threshold;
- Schedule B itemization and tie-out through the real presentation projection;
- provenance reaching report, allocations, rule, citation, package, and each
  displayed adjustment;
- lifecycle tests for correction, retraction, and reassertion;
- legacy compatibility/transition/refusal tests;
- current T0-F5 reproduction followed by a passing regression;
- identity failure before durable run effects or a general collision repair;
- compatibility tests showing unrelated Schedule B and line-2b paths remain
  unchanged; and
- negative wording/structure checks preventing a claim of complete taxable-
  interest or filing support.

Before handoff, run applicable focused tests, repository mypy for changed typed
Python, governance lint, envelope scan, and `git diff --check`. Do not rerun a
deterministic full suite merely to manufacture a second result.

## Data safety

Only obviously synthetic `demo.*` / `demo-*` identities and amounts may be
committed. No personal source document, taxpayer fact, workspace path,
generated return, refusal reason, credential, or private output enters the
branch. Any new fixture, manifest, output shape, or path receives the project’s
data-safety checks before push.

## Tracks

P0–P3 are planning gates, not implementation tracks. Their working records may
be committed while the milestone is draft, but their material conclusions are
absorbed into the final plan, contracts, fixtures, and tests during curation.

### Design comparison — **COMPLETE**

The executable comparison rejected a presentation-only total because line 2b
and attachment tie-out run before presentation. A copied-pin shared subtotal
and dispatcher B produced the same arithmetic, blocking, and reader result.
Dispatcher B was selected because each report-scoped reduction already carries
the lineage the reader needs; copying those pins to another aggregate adds no
observable value.

The comparison also established that a flat union of citation leaves does not
preserve which report owns which allocation. The selected carrier is top-level
`provenanceGroups`, one group per contributing report-scoped reduction. It
keeps form itemization separate from explanation grouping. The production
tests now exercise I0–I12 through package v38, so the disposable overlays and
their commands are not part of the publication.

### Track 0 — integration contract closure — **PASS**

Q1 selected dispatcher B. Q2 selected an additive attachment-rule successor
and top-level `provenanceGroups`. Q3–Q7 selected the bounded legacy, trigger,
identity, claim, and failure policies recorded above. I4 causal-block
explanation remains the one deferred presentation limitation.

### Contract unit — **READY**

The additive `attachment-rule.v11` contract declares derived adjustment rows,
exclusive legacy/new selection, and nominee activity as an independent
Schedule B trigger. `artifact-package.v29` admits it. Presentation validation
requires one group for each contributing derived finding and verifies exact
current contributor identities against recorded pins. `rule-artifact.v9` and
`artifact-package.v30` declare and admit the bounded line-2b path selection and
the nominee aggregate producer. Canonical positive instances and focused
contract tests preserve the selected relationships; historical published
schemas remain immutable.

### Track 1 — coherent Schedule B and bounded-return integration — **READY**

The first production candidate demonstrated the selected arithmetic and
presentation behavior, but independent review found two blocking
representation defects: the dispatcher aggregate had no adopted producer of
its own and line 2b executed a Python-rewritten expression rather than the
checksum-published citizen. The selected Q1/Q3 product outcome survived.
The then-current rule grammar could not express neither-present, legacy-only,
new-only, and both-present refusal without gating on inactive dependencies or
rewriting the rule. The owner selected **bounded declared path selection**:
each alternative, activity test, dependency, expression, and collision
refusal remains visible in the adopted citizen without repository-wide
optional-ref semantics. The aggregate also received its own adopted producer.
Additive `rule-artifact.v9` and `artifact-package.v30` were published. The
first contract review retained that shape but rejected five mechanical
integrity gaps: ignored top-level declarations, duplicate path ids,
undeclared path-guard inputs, absent both-present cause pins, and unenforced
path pin metadata. Those gaps were repaired without changing the published
v9/v30 schemas. Re-review returned **READY**.

Package v38 adopts the distinct nominee aggregate producer, Schedule B v7,
and line 2b v8 using the bounded selection grammar. Independent review
returned **READY** with no blocking findings. Foreman inspection agreed that
the two rejected mechanisms are absent from the v38 path. The production
no-activity record normalization and non-operative generic aggregate metadata
remain bounded seams; neither changes this vertical's value, refusal,
attribution, or reader account.

Schedule B and line 2b consume the same adjustment because the attachment
tie-out makes either half unpublishable by itself. Identity refusal was
Track 2.

### Track 2 — execution boundary and end-to-end evidence — **READY**

The selected identity refusal now runs before output reservation or a start
record. I9–I12 execute through projection, marshalling, package v38, run
records, and presentation. Independent review returned **READY**. Track 1
arithmetic, tie-out, legacy/new refusal, and provenance were not reopened.

### Closing unit — **COMPLETE**

The final publication retains the plan, additive contracts, atomic production
tracks, canonical tests and fixtures, retrospective lessons, roadmap, and
phase-state pointer. Working charters, reviews, disposable overlays, and repair
narration are not publication artifacts.

## Track 0 adversarial closure

Final state: **PASS**. Dispatcher B is the Q1 selection. Q2 is the additive
`attachment-rule.v11` successor with report-group lineage carried by top-level
`provenanceGroups`; Schedule B v7 and package v38 are the production content.
Q3–Q7 bounded defaults stand. I4 causal-block explanation is deferred.

| Artifact | Disposition | Required evidence |
| --- | --- | --- |
| Authority-lifecycle table | **PASS** | Table below. Would fail if a dependent consumer used a retracted allocation or a blocked report-group remainder. |
| Empty/nonempty authority matrix | **PASS** | Matrix below (I0, I1, I7, I8, I9, I4, I10). Would fail if I0 published a `$0` nominee fact or I8 subtracted both amounts. |
| Late-authority counterexample | **PASS** | Paper trace below. Would fail if a retracted allocation still required Schedule B or reduced line 2b. |
| Reused-claim equivalence | **PASS** | Legacy subtotal, report-scoped reduction, dispatcher aggregate, and pairing-scoped adjustment fail the three-part test against each other. Would fail if Track 0 reused `scheduleb-nominee-subtotal` or one citation for nominee and accrued interest. |
| Neighboring-capability dependency diff | **PASS** | Diff below. Would fail if no-activity I0 gained a nominee `require_closed`, or if Form 8815 were described as cured. |
| Integration surface | **PASS** | Production I0–I12 cases execute through `live_coordinate_run`, package v38, durable output, and presentation. I4 blocked-path causal explanation remains deferred. |
| Known limitations affecting correctness | **PASS (recorded)** | Form 8815 / §135 and broader interest remain explicit non-claims. T0-F5 repair, legacy refusal, and identity pre-run check are delivered. |

### Authority-lifecycle table

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| Box-1 report finding | Payer-reported interest for one statement-year | payer+statement+tax-year | Current assertion / currency | Correction, retraction, supersession of that finding |
| `tax.us.nominee-allocation.amount` | User-attributed amount of that report belonging to a named other person | payer+statement+tax-year+recipient | Current attributed assertion (ADR-0073) | Correction, retraction, reassertion |
| `nominee-reduction|{report_fact_id}` | Report-scoped nominee reduction or block | That report’s current allocations and current report finding | ADR-0074 `bound_sources` group | Allocation/report currentness change; over-allocation block |
| Dispatcher aggregate (Q1 **B**) | Form-facing nominee amount: deterministic sum of **published** suffixed reductions; block if any consumed group is blocked | The run’s current published/blocked nominee-reduction groups | Suffixed group outcomes | Any contributing group’s publication/block change; I0: no aggregate fact |
| Pairing-scoped current-year adjustment / subtotal | Accrued-interest return-of-capital subtractand (ADR-0071) | Pairing + report | Pairing publications | Pairing correction; aggregate accrued exceed |
| Legacy `scheduleb-nominee-subtotal` | User-entered tax-labelled Nominee Distribution | tax-year + adjustment-instance family | Closed legacy family | Member correction; both-present **refusal** when a new path is also current |
| Schedule B nominee trigger | Current supported nominee allocation or published/blocked group consequence independently requires Schedule B | Current nominee activity, not dollar threshold | Q4 | Retraction of last current allocation (trigger off); not a stored denial |
| Part III answers | Explicit foreign-account / foreign-trust evidence when Schedule B is required | Return | Presence of those findings | Absence → required-and-incomplete; `"no"` is not inferred from absence |
| `taxable-total` / line 2b | Bounded post-adjustment interest (not complete line 4) | Declared positives minus selected subtractands | Line 2b v6 plus dispatcher aggregate when new path live | Missing/blocked dispatcher when a group is unresolved (Q7); Form 8815 still unmodeled |
| Identity refusal | Pre-run refusal of delimiter-shaped nominee report/allocation identities the path consumes | Those identities | Q5 check before start-record | General `fact_id` redesign remains out of scope |
| Package adoption | Which rules/attachment grammar run | Adopted package | ADR-0027/0033 | Different package version; contract-unit successor |

### Empty/nonempty authority matrix

| Family state | Universe / absence authority | Eligibility | Feature result | Neighboring result |
| --- | --- | --- | --- | --- |
| No current allocation (I0) | Report-only or empty nominee groups; C0-as-absence | Nominee trigger off | No dispatcher aggregate; no `$0` fact; line 2b unchanged | Schedule B follows other valid triggers |
| Current allocation (I1) | Current attributed allocations + current report | Trigger on | Dispatcher sum; line 2b `$750`; Schedule B required; Part III `"no"`/`"no"` publishes | Completeness answers required |
| I1 missing Part III | Same as I1, answers absent | Trigger on | Line 2b `$750`; Schedule B required-and-incomplete | Not a form success |
| Legacy-only (I7) | Closed legacy family; no new allocation | Legacy path | Existing subtotal; explicitly legacy | New dispatcher unused |
| Both-present (I8) | Current legacy amount **and** current new allocation | Refusal | Line 2b and Schedule B block; no double subtract; no conversion | Unrelated families unchanged |
| Retracted last allocation (I9) | History recoverable; no current allocation | Trigger off | Returns to I0 shape | Schedule B no longer required by nominee |
| Over-allocated group (I4) | Current allocations exceed report | Group blocked | Report-local others may publish; dispatcher/Schedule B/`taxable-total` that depend on the unresolved group **block** | Unrelated report-local reduction remains |
| Missing current report (I10) | Allocation names a report with no current finding | Group blocked | Same dependent-block as I4 | No substituted historical amount |

### Late-authority counterexample

```
attest one allocation → close report → compute (I1, one published reduction)
  → add a second recipient on the same report → recompute (I2, one group sum)
  → add a second report with its own published reduction → recompute (I3, dispatcher sums two publications)
  → retract last allocation on report A → recompute (remaining groups only)
  → retract until none remain → recompute (I0, no aggregate fact)
  → reassert I1 → over-allocate A → recompute (I4: A blocked, unrelated published groups remain, dependent aggregate/SB/line 2b block)
  → add live legacy amount with a current new allocation → recompute (I8 refuse)
```

The package-v38 production cases execute I0, I1, I1-missing, I2, I3, I4,
I5, I6, I8, and I11 through `live_coordinate_run` and durable presentation.
I2 has one published reduction with two allocations; I3 has two currently
published reductions, each paired to its report through top-level
`provenanceGroups`. A flat leaf union cannot establish that association.
I4 live-executes the dependent block; causal
explanation of **which** group caused the block is deferred.

At each step the dispatcher aggregate, Schedule B trigger, and line 2b bind **current** group outcomes only. A declaration that remained current after its allocations or report changed would be a FAIL. Package transition to a successor attachment grammar is a contract-unit adoption, not a silent reinterpretation of legacy facts.

### Reused-claim equivalence

| Pair | Same proposition? | Same identity/lifecycle? | Same authority? | Verdict |
| --- | --- | --- | --- | --- |
| Legacy `scheduleb-nominee-subtotal` vs dispatcher aggregate | No (tax-labelled instance vs ordinary-allocation-derived sum) | No | No (legacy citation vs nominee-reduction citation) | **Do not reuse** |
| Report-scoped `nominee-reduction|{id}` vs dispatcher aggregate | Aggregate of the former, not the same identity | No (report vs run-facing sum) | Pins/citation recovered from each reduction | Distinct symbols; aggregate **enumerates** reductions (B) |
| Dispatcher aggregate vs pairing-scoped subtotal | No (nominee vs accrued interest) | No | No (distinct citations; I6 reader sites disjoint) | **Do not share kind/citation** |
| Candidate A copied pins vs B | Same form-facing amount | Same consumers | Comparison produced the same reader result | **B selected**; A redundant at the reader |

### Neighboring-capability dependency diff

| Neighbor | Before | After | No-activity (I0) |
| --- | --- | --- | --- |
| Schedule B applicability | Threshold only | Threshold **or** current nominee activity | Unchanged if no nominee activity |
| Schedule B Part I | Legacy nominee + ABP rows; T0-F5 gap | Derived nominee row + accrued-interest row (successor grammar); tie-out to line 2b | No new row |
| Part III | Required whenever Schedule B is required | **Unchanged policy**; newly required when nominee triggers Schedule B below threshold | Not newly required |
| Line 2b | Legacy nominee + ABP + pairing-scoped subtotal | Plus dispatcher aggregate when new path live; both-present refuses | Unchanged |
| Accrued-interest / ABP | Line 2b subtractands | Remain; Schedule B must itemize pairing-scoped (T0-F5 repair) | Unchanged |
| Form 8815 / §135 | Unmodeled | **Still unmodeled** | Unchanged |
| Dividend Part II | Required when Schedule B is required | Unchanged; missing `1a-subtotal` still blocks the whole attachment | Unchanged |

No new `require_closed` on a neighbor’s own meaning beyond the selected nominee trigger and dependent-block (Q7).

### Integration surface

| Consumer | Binding | Cardinality | Satisfied? |
| --- | --- | --- | --- |
| Dispatcher B | Published suffixed `nominee-reduction|{id}` | 0..n published; any blocked group → aggregate block | Production I0–I4 cases |
| Line 2b | Dispatcher symbol as subtractand when new path live; not unsuffixed prefix; not legacy symbol for the new proposition | 0 (I0, no require) or 1 published or block | Production I0–I8 cases; I0 has no invented zero |
| Schedule B requirement | Current nominee activity or threshold | Boolean | Production I0/I1 cases |
| Schedule B Part I nominee row | Form-facing aggregate; lineage in top-level `provenanceGroups` per contributing reduction | 0..n reductions; one form amount | Production I1/I2/I3 cases |
| Schedule B accrued row | Pairing-scoped publication ids | 0..n | Production I5/I6 cases |
| Tie-out | `part_sum` == `taxable-total` | Equality when published | Production I1/I5/I6 cases |
| `_resolve_attachment` / citation-walk / `provenanceGroups` | Recorded pin projection; form parts itemize; `provenanceGroups` carry report-group lineage | Reader associates each report with exactly its allocations, rule, and citation without mistaking lineage for form rows | Production I1/I2/I3/I6 cases. I4 blocked path: no citation group (deferred) |
| Identity check | Current nominee report/allocation identities the path consumes | Pre-run `Refusal` | Production I11 case |
| Line 9 / SS worksheet | `taxable-total` | 1 | Unchanged contract; blast radius of line 2b |

### Known limitations affecting correctness

- Form 8815 / §135 and other unsupported interest categories remain **non-claims** (Q6, I12).
- **I4 causal-block explanation is deferred.** A blocked Schedule B attachment has no citation group (`citation_group=None`). The durable explanation does not identify which report group caused the dependent aggregate and Schedule B to block. That is not complete report-local provenance on the blocked path.
- Information-return filing remains out of scope.
- Kernel `fact_id` rendering remains non-injective. This milestone delivers only the bounded pre-run nominee-identity refusal.
- Production no-activity record normalization and non-operative generic aggregate metadata remain bounded seams.

## Execution record

Closed 2026-09-12. Retrospective:
[`2026-09-12-nominee-interest-return-integration.md`](../../../milestone-retrospectives/2026-09-12-nominee-interest-return-integration.md).

| Unit | Result |
| --- | --- |
| Gates P0–P3 | Independently reviewed; material findings absorbed into this plan before Track 0 |
| Design comparison | Dispatcher B selected over a redundant copied-pin aggregate; top-level `provenanceGroups` selected over form-itemization parts |
| Track 0 | PASS. I4 causal-block explanation deferred |
| Contract unit | `attachment-rule.v11`, `artifact-package.v29`, `rule-artifact.v9`, and `artifact-package.v30` independently READY; canonical fixtures and tests preserve their relationships |
| Track 1 | Package v38 adopts Schedule B v7, line 2b v8, and the distinct nominee aggregate. Independently READY. T0-F5 repaired. Legacy-only / new-only / both-present policy executed |
| Track 2 | Pre-run `NOMINEE_IDENTITY` refusal and I9–I12 independently READY |
| Closeout | Complete. Retrospective, plan closure, roadmap item 9, and phase-state selection posture |

## Success and stop conditions

Success means the application can take the already-recorded ordinary nominee
allocation through an adopted tax rule into one bounded return result and an
honest Schedule B account, with no hidden subtraction, double count, invented
legacy correspondence, or lost provenance. The shared Schedule B surface also
accounts for the existing pairing-scoped current-year adjustment, closing
T0-F5.

Stop and return a decision rather than forcing implementation if:

1. legacy/new coexistence cannot avoid omission or double subtraction without
   inventing a report, recipient, attribution, or equivalence;
2. a Schedule B adjustment cannot be projected from current derived results
   without erasing the distinct authority of nominee and accrued-interest
   adjustments;
3. the real presentation consumer requires a general adjustment framework whose
   additional value and consumers have not been demonstrated;
4. the identity boundary cannot become either injective or a clean pre-run
   refusal without a cross-project migration or compatibility decision;
5. the proposed path describes `tax.us.2025.interest.taxable-total` as complete
   line 2b or otherwise hides the Form 8815/section 135 gap;
6. a new nominee prerequisite blocks a neighboring no-activity path without
   support from that neighbor’s own meaning; or
7. a published schema cannot be instantiated honestly without entering a
   reserved or unsupported domain.

## Exit criteria

1. P0–P3 were completed as small review cycles and their material findings are
   absorbed into the plan before Track 0 or implementation.
2. Track 0 adversarial closure has no unresolved `FAIL` or undisposed
   correctness limitation.
3. T0-F5 is reproduced against the merged base and repaired through the real
   Schedule B presentation consumer.
4. A below-threshold current nominee allocation independently makes Schedule B
   applicable under a declared, tested contract.
5. New nominee reductions affect the bounded return result and Schedule B
   exactly once, with exact report/allocation/rule/citation provenance.
6. Legacy-only, new-only, and both-present states follow one selected policy;
   no path silently converts or double-subtracts a legacy amount.
7. Over-allocation, absent report, correction, retraction, reassertion, and
   unrelated-group cases have positive and negative observations at the real
   consumer boundary.
8. Ambiguous identity either remains distinct under a general repair or is
   refused before start-record and output-reservation effects.
9. The publication states and tests the boundedness of the result and preserves
   the known Form 8815/section 135 and wider taxable-interest gaps.
10. Applicable focused tests, mypy, full-suite lane, governance lint, envelope
    scan, diff check, and independent unit reviews are complete. Final
    curated-candidate review and CI bind the publication head before merge.
