# Taxable interest translation: a fluid domain model

This is a working map, not a schema. It exists so a reader — the owner, or a
future agent — can understand the shape of the whole translation the
Document and Ordinary-Fact Translation Vertical milestone builds, without
having to reconstruct it from eight ADRs and a test suite. It is not graded
as exhaustive or binding, and it is expected to change as the product grows
past this slice. Where it names a decision, that decision is the one the
accepted ADRs (0067–0072) actually made, not an aspiration.

## The plain-language stratum

**The life circumstance.** A person owns, or has just bought, an
interest-bearing obligation — typically a bond — from someone else. Bonds
pay interest on fixed dates, but ownership can change between those dates.
When a buyer purchases a bond partway through an interest period, the
buyer conventionally reimburses the seller for the interest that accrued
before the sale (the seller earned it, but the payer will report the whole
period's interest to the buyer, who was the owner of record when it was
paid). At tax time this has two consequences: the interest the buyer is
taxed on this year is reduced by the amount paid back to the seller, and
that same amount reduces the buyer's cost basis in the bond (it was a
repayment of accrued interest, not a payment for the bond itself). This
is an ordinary, common transaction — not a tax election, and not something
most people would recognize as "a tax adjustment" without help.

**What the document contributes.** A Form 1099-INT is an attributed report
of what the payer (typically a bank or broker) told the IRS and the
taxpayer: "this much interest was paid on this obligation, for this tax
year." It is evidence, not a canonical fact about the buyer's own
circumstance — it says what the payer reported, not what happened between
the buyer and the seller when the bond changed hands. Box 1 (or the
equivalent for OID, a K-1, or a non-form report) is the amount; an account
or statement reference, when present, is what actually identifies *which*
report this is, separate from the payer's name and the tax year.

**What the person contributes.** The buyer can state, from ordinary
knowledge of their own affairs: who reported the interest (as it appears
on their own paperwork), enough about the specific obligation to tell it
apart from another one from the same payer, when they acquired it, how
much they paid the seller for already-accrued interest, and — when they
have it — the statement or account reference that ties their purchase to
a specific report. None of this requires knowing tax law. It specifically
does not include "the taxable amount" or "the adjustment" — that is what
the product is supposed to derive, not what the person supplies.

**What law, administrative rules, and convention contribute.** Publication
550 and the Schedule B instructions support subtracting accrued interest
paid to the seller from reported interest, and reducing the buyer's basis
by the same amount. The convention of the buyer reimbursing the seller for
accrued interest at settlement is a market practice the tax treatment
assumes but does not itself create — it is why the ordinary fact ("I paid
the seller X") is a fact a buyer can just know, not a tax judgment they
have to make.

**What translation the application performs.** It never accepts a
preclassified "Schedule B adjustment" as ordinary input. Instead it: takes
the person's acquisition circumstance and the payer's report as two
independent, source-attributed facts; establishes, with real evidence
(never a guess), that they concern the same real-world obligation; checks
that the claimed accrued amount is actually supportable against that
report's own amount, both individually and in aggregate with any other
acquisition sharing the same report; and only then lets an adopted tax rule
— not the document adapter, not the ordinary-language interviewer — derive
the current-year interest reduction and the basis reduction as two
independently-pinned, independently-correctable findings.

**What reaches the return.** A current-year interest adjustment that feeds
the same subtotal Schedule B's legacy path always fed (so Form 1040 line
2b sees one correct number, not two colliding ones), and an item-level
basis consequence that is published with full provenance but has no
consumer yet in this slice (no disposition implementation exists this
milestone; see below).

**What the application cannot yet determine or translate.** It cannot
resolve a missing or ambiguous association without asking the person for
more (a statement reference, or an explicit confirmation) — it will not
guess. It has no allocation policy when several acquisitions sharing one
report together over-claim it — it can only detect and exclude, not decide
whose claim is smaller. It does not implement bond premium, market
discount election, nominee allocation, or any later-year disposition
consequence of the basis reduction. And it does not yet resolve the case
where an honest person genuinely doesn't know which year's report their
acquisition will show up on yet (a real case: interest paid to the seller
in December, no statement received until the following spring) — see
"Cross-year handling" below for how the mechanism that would join a
*known* cross-year report is designed, and why no such report is actually
admitted in this milestone.

## The wider frontier, mapped only far enough to place this slice

```
taxpayer
  |
  +-- owns / acquires --> obligation (a specific bond or similar instrument)
  |                          |
  |                          +-- identified by: payer entity + the
  |                          |   person's own reference/description
  |                          |   (ADR-0068's entity-kind vocabulary --
  |                          |   see "account/statement/obligation" below)
  |                          |
  |                          +-- acquisition event: a date, and (maybe)
  |                              an accrued-interest payment to the seller
  |
payer / broker reporting
  |
  +-- Form 1099-INT (or OID/K-1/non-form) --> a report: an attributed,
  |     payer-authored statement of an amount, for a tax year, optionally
  |     naming a specific statement/account
  |
tax authority (IRC, Pub. 550, Schedule B instructions)
  |
  +-- supports: accrued interest paid to seller reduces reported interest
  |   and reduces basis -- does not support the shape of "who guesses which
  |   report an acquisition concerns" (that is an identity question, not a
  |   tax-law question)
  |
classification (adopted tax rules, this milestone's Seams 1/3/5)
  |
  +-- association: acquisition <-> report, evidenced, never guessed
  +-- supportability: claimed amount <= associated report's amount,
  |     individually and in aggregate across shared reports
  +-- consequence: current-year adjustment + basis reduction, each its own
        independently-supersedable published finding
  |
basis consequence
  |
  +-- published with provenance; no later-year disposition consumer yet
      (explicitly out of this milestone's scope unless it becomes load-
      bearing)
  |
return projection
  |
  +-- Form 1040 line 2b: one number, one subtractand path (see the
      legacy-coexistence note below)
  |
explanation / user adoption
  |
  +-- a fresh reader should be able to recover: what the payer reported,
      what the person said, what rule translated it, what the product
      concluded, and what remains unsupported (exit criterion 9) --
      the existing pin-walk (packages/derivation/explanation.py) and the
      presentation projector (packages/derivation/presentation_projection.py)
      are the real, already-wired mechanisms this relies on; this
      milestone did not need to invent a new one
  |
refusal
  |
  +-- ambiguous association, unconfirmed sole-candidate association, and
      over-aggregated claims all refuse (or exclude) with a named,
      traceable disposition -- never a silent guess or a silent partial
      answer
  |
professional handoff
  |
  +-- out of scope: this product does not claim professional tax
      authority, and nothing here decides what a preparer would do with
      an unsupported case; it only refuses to pretend it handled one
```

## The account/statement/obligation distinctions, and the corrected
## obligation-identity model

The acquisition side needs a real, arbitrary-cardinality identity to
associate *with*, and association needs the one discriminator that can
actually distinguish two obligations from the same payer. ADR-0068 closed
this with three distinct identities that this domain model should keep
straight, because they are easy to conflate:

- **Payer.** A real kernel entity (`tax.us.interest-payer`), shared by both
  the report and the acquisition sides. "Same payer" is now a real identity
  join, not a string-equality guess on a name field.
- **Obligation.** A new entity kind (`tax.us.interest-obligation`), scoped
  under the payer and disambiguated by the person's own reference or
  description. This is *the bond itself*, from the acquisition side's point
  of view — not the report, and not the statement. Two obligations from the
  same payer are two different entities even if no report ever
  distinguishes them.
- **Statement/account.** A real entity kind (`tax.us.1099int-statement`),
  the discriminator that lets association narrow *which report* an
  acquisition's attestation is being made against, when the person knows
  it. The report side already had this identity (a 1099-INT is a specific
  statement); the acquisition side gained the ability to name it too
  (`reported_statement_reference`, canonicalized by the same documented
  convention independently implemented on both sides — see
  `packages.tax.obligation_acquisition_mapping` and
  `packages.tax.report_statement_identity` — so they resolve to the
  identical entity without one side calling the other's code).

**A matching statement/account is not, by itself, proof of obligation
identity.** A real Form 1099-INT statement/account can
aggregate interest from *several* obligations into one box-1 number — the
form's own box 1 is "interest paid or credited to the recipient or
account," covering several forms of indebtedness, with no general box-1
CUSIP or per-obligation identifier. Matching payer, statement, and tax year
proves only that an acquisition's interest was reported *through that
account/relationship* — it does not prove *which* obligation within that
account's aggregate a given acquisition concerns.

**Obligation correspondence always requires an explicit, accountable user
attestation.** A statement/account reference,
when the person knows it, narrows *which report* their attestation is being
checked against (useful when a payer has multiple accounts) — it is never
itself evidence of, nor a substitute for, that attestation. Association is
still two-tiered by how the candidate report is *located* (a named
statement narrows to one report; absent a statement reference, the coarse
payer+year join is what is available instead), but the two tiers no longer
differ in whether confirmation is required — **`confirmed_report_match:
true` is mandatory in both cases.** Two or more candidates always refuse
(`ASSOCIATION_AMBIGUOUS`), whichever tier is in play; a single candidate,
narrowed or coarse, absent confirmation always refuses
(`ASSOCIATION_UNCONFIRMED`). The obligation entity itself is never the join
key for association — it is what the acquisition *is*, but association
locates the candidate report by payer+statement (or payer+year, absent a
statement reference), because that is what the report side can actually
offer as a correlating signal; the person's own attestation, not that
signal, is what actually establishes obligation correspondence.

It is a legitimate, expected outcome — not a defect — for two acquisitions
naming two genuinely different obligations to both attest to, and both
associate with, the same report: one broker statement legitimately
aggregating interest from two bonds is a realistic real-world shape. This
model prevents an acquisition being silently joined to a
report on the strength of the payer/statement/year match alone, with no
attestation. Whether the aggregate of everything attested against one
report is actually supportable by that report's own amount is a separate
question ADR-0070's aggregate-supportability check exists to bound, not
something this identity-association seam needs to prevent on its own.

One gap this model does not close: if the same obligation is
entered twice with a mismatched amount (a typo, or two different people
entering the same real bond), nothing here detects it. That is a named
residual risk (ADR-0072, ADR-0068), not a defect this milestone's evidence
resolves.

## T9: a genuinely unsupported neighbor, and an open presentation-wiring question

A T9 fixture must exercise a genuinely unsupported neighbor rather than a
fact type that merely lacks accrued-interest treatment: Form 1099-INT box
8 (tax-exempt interest) and box 10 (market discount) both already have a
real subtotal rule and their own routed
treatment (`rule.f1099int-b8-subtotal.json`, `rule.f1099int-b10-subtotal
.json`); proving either stays out of the accrued-interest machinery is an
isolation control, not proof of unsupported translation. Form 1099-INT box
11 (bond premium) is a genuine instance of this section's own named
non-goal: `f1099int-box11.bundle.json` declares the fact type, and no
source-family, closure mapping, or rule anywhere in the adopted production
package reads it. It is contributed through a real `bundle-adoption` act
(the same mechanism `obligation-acquisition.bundle.json` already uses),
so admission never rejects it as unrecognized input — it is simply never
consumed once admitted.

`packages/tax/coverage.py` gained `untranslated_source_findings`: a
structural read model, in the same module and spirit as the existing
`coverage_report` (ADR-0016 decision 3 — derived only from committed state,
never a second authority), that names any fact type the workspace
recognizes but the adopted package's own content never genuinely consumes.
This correctly distinguishes box 11 (unreferenced) from box 1 (referenced)
without a hand-authored list.

Collecting every exact string appearing anywhere in every
field of every non-bundle package member is not a safe detection strategy:
a metadata-only member (a
citation, a note) whose incidental field happened to contain the box-11
fact-type id would make box 11 disappear from the untranslated result even
though nothing genuinely consumed it. The detector instead traverses
only the exact semantic reference shapes that create a real derivation or
admission edge — verified against every rule-artifact, source-family,
source-closure-mapping, attachment-rule, and checked-conclusion-binding
schema version the adopted package actually uses:

- a `collect`/`count`/`collect_categorical_all_equal` expression node's own
  `name` field (never a plain `ref` node's `name` in an ordinary,
  non-pairing-scoped rule, which names a published symbol or pin id, not a
  fact type — but this milestone's own pairing-scoped consequence rules
  are a real, narrow exception: their `Environment` binds the acquisition
  and report fact-type ids as symbol names, so a pairing-scoped rule's
  declared `ref` node genuinely does name a fact type. This is safe today
  only because the acquisition fact type isn't marked `source_amount:
  true`; the detector does not yet special-case pairing-local `ref`
  binding, see `packages/tax/coverage.py`);
- any key ending in `fact_type` (`fact_type`, `member_fact_type`,
  `conclusion_fact_type`, ...), whose value is the fact-type id directly or
  an `{id, version}` exact-pin object — a source-family's member predicate,
  a closure mapping's member fact type, a rule expression's
  `category_literal`, a checked-conclusion-binding's conclusion/component
  fact types, or an attachment-rule's itemization row / completeness
  answer;
- a rule's own `pins` entry with `role == "input"` — a fact type read
  directly as a single pinned value without a family collect (e.g. a
  field-mapping/cross-form-bridge rule's scope pin), the genuine
  non-family-collect consumer this section names explicit test coverage for.

Free-text or metadata fields (`notes`, `title`, a citation's own identity,
or any other field outside this exact shape list) are never traversed, so
an unrelated member's incidental field can never manufacture a false
consumption claim — proven directly by a committed negative-control test
covering exactly this metadata-only-member scenario
(`tests/test_t9_unsupported_neighbor_live.py`).

`untranslated_source_findings` is now wired into production output: it is
no longer a read model a caller must invoke in isolation. `build_presentation_
model` (`packages/derivation/presentation_projection.py`) calls it with the
same `state` and `resolved_members` it already holds and carries the result
as the presentation model's `unsupportedSourceFindings` list — so the
unsupported boundary (exit criterion 9) is recoverable from the durable
run's own presentation output produced by `live_coordinate_run`, the same
production path the T9 integration test exercises, not only from a direct
call to the coverage helper.

## Cross-year handling: three distinct years, never conflated

Three things are usually the same year, but are not guaranteed to be:

1. **The event year** — when the person actually bought the bond and paid
   the seller for accrued interest.
2. **The reporting year** — the tax year the payer's own 1099-INT covers
   (the year interest was actually paid to the buyer of record).
3. **The tax-consequence year** — the return year on which the current-year
   adjustment and basis reduction should actually land.

The ordinary-language interview never asks the person to state which year
this applies to. The acquisition's ordinary answer set supplies only
`acquisition_date` — a plain fact about when the person bought the bond,
never a tax-reporting-applicability judgment. The acquisition's own
`acquisition-year` identity component is derived directly from that date
(the event year, above), not asked for as a separate question; this keeps
the interview honest to exit criterion 5 (never asking for a tax
classification).

The reporting year (above) is supplied by the run's own scope, not by the
acquisition side at all: `associate()`'s `reporting_year` parameter is
sourced from `run_scope["year"]` (threaded through
`packages.derivation.live.live_coordinate_run` ->
`marshal_live_run_context` -> `RunContext.reporting_year`), and both
association tiers restrict candidate reports to reports whose own
`tax-year` identity component matches that run-scope context (see
`packages.tax.identity_association._reports_in_reporting_year`). The
report's own `tax-year` remains a report-side, independently attributed
identity component — a real fact about what the payer's own document
covers, never conflated with the acquisition's `acquisition-year` or with
the run's reporting-year context.

Because a bond acquired late in one calendar year can have its first
interest payment land on the *following* year's report (the acquisition
event happened in year N, but the report belongs to year N+1),
`acquisition-year` never gates which report an acquisition can associate
with — only the confirmation's recorded target does. Exact report-target
confirmation (`confirmed_report_fact_id`, mandatory whenever
`confirmed_report_match` is true, uniformly at both the statement-narrowed
and coarse tiers — see ADR-0068 Decision 5) is the general mechanism that
would let a December acquisition legitimately associate with a report
belonging to year N+1: a run scoped to year N+1 narrows candidates to N+1
reports, and the acquisition's own confirmation must name that specific
N+1 report's fact id. The same mechanism is what prevents a stale or
cross-year confirmation from silently retargeting: a confirmation recorded
against one report never authorizes association against a different
report or a different reporting year, even when that different report is
the sole candidate under a later run's scope.

**This mechanism is real and general; the admitted vocabulary in this
milestone is not.** Both the acquisition's `acquisition-year` and the
report's own `tax-year` are literal identity keys restricted to
`["2025"]` in the adopted content (`obligation-acquisition.bundle.json`,
`f1099int.bundle.json`) — no 2026 report vocabulary, package member, or
later-year consequence path exists in this branch, so no real run can
actually have a 2026 report to associate against, and no cross-year
association has actually run end to end. Exercising a genuine later-year
report and the tax-consequence-year question it would raise is the
roadmap's "Later-year basis reuse" candidate (see `docs/phase-state.md`'s
"Open and owner-held" section), not something this milestone closes.

## What this model is not

It is not a schema, not a contract, and not exhaustive. It does not
attempt a general securities ledger, a full taxable-interest census, a
disposition engine, or a joint-return subject model — those remain outside
this milestone's bounded slice by deliberate choice (see the milestone
plan's non-goals), not because they are unimportant. It should be revised
freely as later work changes what is actually built.
