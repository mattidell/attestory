# ADR 0052 — Covered Long-Term Gains, Schedule D Line 8a

- Status: **accepted** (owner ratification 2026-08-02, recorded by merging
  PR #137; production authority now that this complete decision unit is on
  `main`)
- Tier: 2 — contract-foundational reach (sets the transaction-identity and
  completeness-boundary template every future capital-transaction slice
  builds on, per the milestone plan's Gate-1 blast-radius scores of 2 for
  both P1 and P2), but not a product-thesis, user-visible-concept, or
  governance-meaning decision; matches ADR-0050's own tier for the same
  reason.
- Date: 2026-08-01

## Context

Engine Breadth's Covered Long-Term Gains, Schedule D Line 8a milestone must
establish a rival-backed scope contract for (P1) how a covered, long-term,
gain-only Form 1099-B transaction becomes a closed, correctable source family
one level below the existing statement-identity pattern; (P2) how the
milestone's nine-part Schedule D completeness boundary is declared and
checked without a thin "Schedule D complete" assertion; and (P3, paper spike)
how Schedule D content and the QDCG/line-16 successor bind to that boundary
without double-counting or precedence ambiguity against the existing
ADR-0050 box-2a route.

Prototype evidence is assembled under
`docs/prototypes/schedule-d-covered-ltcg-8a/`: sealed incumbent `it1`
(nested-member identity, synthesized checked conclusion), clean-room rival
`it2` (independent anchor-keyed family, direct multi-read completeness,
shared `selected-preferential-base` symbol), independent contract/adversary
and expressiveness committee reviews, owner selection of the rival topology
plus explicit adoption of the box-2a-closed completeness successor
(`round-1-triage.md`), one bounded Rung-1 repair cycle resolving the one
recorded dissent, and an independent confirmation review returning `READY`
(`reviews/repair1-confirmation.md`). The composite controlling paper is
`it2/design.md` as amended by `repair1/design.md`. The full clause-to-evidence
routing, the recorded dissent and its resolution, and the two production
conditions carried forward as owed are in
`docs/prototypes/schedule-d-covered-ltcg-8a/evaluation-analysis.md`.

The owner ratified this decision unit by merging PR #137 on 2026-08-02,
following the same pattern ADR-0050 established for the same milestone
family. This ADR carries production authority; the milestone's production
Tracks 1-4 implement the contracts below.

## Decision

1. **Transaction source family and identity.** A 2025 Form 1099-B statement
   anchor is a contributed fact with identity `(tax-year, subject, broker-ref,
   logical-statement-ref)`; evidence, file, upload, and document identifiers
   are forbidden from the identity. An eligible covered-long-term-gain
   transaction is a member of its own return-level source family — distinct
   from the anchor's family — with identity `(tax-year, subject,
   statement-anchor-ref, logical-transaction-ref)`, pinning the current
   anchor finding named by `statement-anchor-ref`. Two logical sales
   furnished by one broker statement have distinct `logical-transaction-ref`
   values and therefore distinct member identities; two statements or
   brokers have distinct anchors. Neither distinction may be collapsed by
   amount, CUSIP, date, account, or evidence identity.

   A correction to proceeds, basis, gain, or another value at the same
   transaction identity supersedes only the prior transaction finding; it
   does not supersede the anchor, a sibling transaction, the family
   declaration, or the closure, and every result pinning the prior finding
   becomes non-current under ADR-0010. Adding or removing a logical
   transaction is a membership transition and advances the family horizon; a
   closure naming the prior horizon becomes stale and cannot authorize a
   subtotal until the new horizon is closed (ADR-0017). Correction of the
   anchor at the same anchor identity displaces anchor-dependent transaction
   publications through their direct anchor pins, but neither rekeys nor
   merges their transaction identities.

   Family closure covers all and only current members satisfying the
   canonical eligible-transaction predicate for the subject and year across
   anchors. The predicate is a contributed/attested source-class assertion —
   tax year 2025, Form 1099-B source, covered security, basis reported to
   the IRS, broker-reported long-term classification, no box-1f market
   discount, no box-1g wash-sale adjustment, Ordinary not indicated, QOF not
   indicated, no taxpayer-side adjustment, no collectibles/special-rate
   treatment, and gain-only classification — never a derivation of gain-only
   from a proceeds-minus-basis comparison (ADR-0011's presence-before-value
   discipline). Closure does not assert that non-eligible transactions are
   absent and cannot authorize any broader Schedule D result without
   Decision 2's independent authorities.

   This proposition reuses ADR-0015 (statement-instance identity and the
   correction/separate-original distinction), ADR-0016 (family claim and
   composition; no silent subtotal broadening), ADR-0010 (direct-edge
   currency and displacement), and ADR-0023 (member-transition boundaries)
   unchanged, and extends the same nested-composition template one level
   deeper than the existing 1099-INT/K-1/market-discount pattern.

2. **Completeness boundary.** There is no synthesizing "Schedule D complete"
   conclusion citizen. Schedule D content, the Schedule D route, and the
   attachment disposition each read nine authorities directly: the eligible
   long-term family closure (Decision 1); the existing Form 1099-DIV box-2a
   family closure; and seven independent contributed categorical absence
   declarations — no short-term transactions, no current capital losses, no
   inbound capital-loss carryovers, no Form 8949 transactions or adjustments,
   no other Schedule D sources (K-1 gains, Forms 2439/4684/4797/6252/6781/
   8824), no lines-18/19 special-rate sources, and no Form 1099-DA or QOF
   flow — each with domain `{yes, no}`, no default, free supersession, and
   presence-before-value semantics, keyed by tax year and subject. Each
   consumer first checks the presence/currentness of all nine authorities
   independently in one pass, naming every missing boundary member before
   any value is read. Missing closure on the eligible-family or box-2a
   authorities is an unclosed-source non-publication; missing any of the
   seven declarations is `blocked(DEPENDENCY_ABSENT)` naming the exact
   missing declarations. Missing never becomes `"yes"`, zero, false, or an
   empty family. With all nine authorities present, any declaration value of
   `"no"` is a known violation of this bounded source class; the Schedule D
   attachment is `required-and-incomplete`, naming every violated member,
   and Schedule D content, the selected preferential-base symbol, line 7a,
   and downstream results do not publish from this route.

   **Adopted completeness successor.** For this bounded class, the box-2a
   family must be **closed** — either closed-empty or closed-nonempty — for
   the completeness boundary to pass; this explicitly supersedes the
   milestone plan's narrower "closed empty" wording, adopted by owner
   disposition (`round-1-triage.md`). Closed-empty box 2a contributes the
   closure-backed amount zero, exactly as under the milestone's original
   wording. When the Schedule D route is the current producer of the
   selected preferential-base symbol (Decision 4), closed-nonempty box 2a
   contributes its current subtotal exactly once, through Schedule D line
   13. A positive box-2a subtotal is not an absence violation; it makes
   ADR-0050's direct route inapplicable because its C1 component cannot be
   `"yes"` while an eligible 1099-B gain is current. This sentence neither
   expands the transaction source class nor edits ADR-0050, and it creates
   no second capital-gain path into Form 1040 line 9 or the QDCG worksheet.

   The Schedule D attachment publishes `required-and-complete` only when all
   nine direct authorities are current, both closures are established, every
   declaration value is `"yes"`, content pins every collected member, and
   all tie-outs hold (ADR-0036 Decision 3, `ITEMIZATION_TIE_OUT_VIOLATION`).
   Supersession of any one declaration or closure displaces every Schedule D
   publication that pinned it; a rerun against a restored current authority
   publishes a new finding and never revives displaced history.

   For the Schedule D successor graph, this completeness boundary supersedes
   ADR-0050 Decision 1 only as the authority used to decide and complete the
   Schedule D route. ADR-0050's four-component checked conclusion, its truth
   table, and its authority over the existing direct box-2a producer remain
   unchanged.

3. **Schedule D content as an ADR-0036 instantiation.** Schedule D line 8a
   has three aggregate fields: column (d) is the sum of contributed proceeds
   of the exact current eligible-family member set; column (e) is the sum of
   their contributed basis; column (h) is the sum of their source-attested
   gains, tied to (d)−(e) for this bounded no-adjustment class — a mismatch
   raises `ITEMIZATION_TIE_OUT_VIOLATION` for the attachment only, never
   rewriting a source fact or blocking a sibling line. Schedule D line 13
   consumes the closed box-2a subtotal once (Decision 2's adopted
   successor). Schedule D line 15 consumes line 8a and line 13 once each,
   with all other Part II inputs closure-backed zero or covered by the
   absence declarations. In this gain-only slice, line 16 equals line 15,
   because the short-term side and losses are absent under the completeness
   boundary. The Schedule D attachment is one ADR-0036 attachment citizen:
   required-and-complete content pins every line/row publication and all
   nine boundary authorities; required-and-incomplete publishes no form
   content and names all missing or violated boundary facts; a closed-empty
   eligible family with no other Schedule D source is not-required, never a
   zero-valued fabricated form.

   This is content only, no new attachment mechanism: it reuses ADR-0036's
   attachment triad, `collect_members`, the itemization tie-out invariant,
   and independent presence semantics unchanged, on the same generic surface
   already demonstrated on Schedule B and a Schedule D stub.

   **Named production condition, not resolved here (CA-05).**
   `attachment-rule.v2`'s `requirement` block is structurally threshold-only
   — `subtotals`, `threshold_parameter`, and
   `comparison: strictly_greater_than` are all required
   (`packages/schemas/tax/attachment-rule.v2.schema.json`; ADR-0036 Decision
   2). Schedule D's required/not-required disposition is categorical, driven
   by the nine-part completeness boundary in Decision 2, not a numeric
   threshold. This ADR does not resolve that representation gap. An
   additive `attachment-rule.v3` (or equivalent) successor, expressing a
   categorical requirement alongside the existing threshold shape, is owed
   before a production Schedule D attachment can be built. It is a
   `separate-decision` prerequisite (evidence: `evaluation-analysis.md` §4),
   not a blocking condition on the contracts this ADR settles.

4. **Shared selected-preferential-base publication and exact pin contract.**
   One versioned symbol, the **selected preferential-base**, has exactly one
   current producer in an adopted graph, and its numeric value remains
   route-neutral — one amount, not a tagged union:

   - **Direct producer.** A successor projection of the closed box-2a
     subtotal and ADR-0050's four-component checked conclusion. When the
     conclusion is current `"no"`, it publishes the selected preferential
     base equal to the box-2a subtotal, pinning that subtotal's family,
     mapping, current horizon, and closure authority, the checked
     conclusion, and the direct components required by the active branch.
     Form 1040 line 7a is downstream of the selected preferential base, so
     this introduces no line-7a-to-symbol cycle.
   - **Schedule D producer.** The current required-and-complete Schedule D
     publication when the eligible family is closed-nonempty and the full
     completeness boundary (Decision 2) passes; the selected preferential
     base equals positive Schedule D line 16 for this bounded gain-only
     slice, pinning line 16, the Schedule D attachment, and the nine direct
     boundary authorities.

   The two producers are mutually exclusive: a current eligible member
   contradicts the direct route's C1 component (`"only capital gains are
   box-2a capital-gain distributions"`), so the Schedule D producer is
   selected whenever eligible 1099-B gains exist, including when box 2a is
   also nonzero. With no eligible member, Schedule D is not required by this
   slice and the direct producer may publish box-2a positive or
   closure-backed zero as ADR-0050 already provides. A package offering both
   producers, neither producer for a route claiming a numeric line 7a, or a
   raw upstream read into line 9 or the QDCG worksheet is invalid and
   publishes no downstream result.

   **Exact pin-signature contract, resolving the one recorded review
   dissent (CA-04).** The two producer signatures on numeric selected
   preferential-base findings are exact and disjoint:

   | Current producer | Exact direct pins on the numeric selected preferential base |
   | --- | --- |
   | Direct | current box-2a subtotal publication; its accepted family, mapping, current horizon, and closure; current C1, C2, C3, C4; and their checked conclusion `"no"` |
   | Schedule D | current Schedule D line 16; current Schedule D attachment `required-and-complete`; and each current direct completeness authority from Decision 2 |

   The producer signature is recoverable from this direct-pin lineage alone,
   so no route tag is added to the symbol's payload — this is only a paper
   pin contract; it does not select the generic schema/rule representation
   that mechanically enforces exactly one producer (Decision 4's remaining
   production condition, below). Form 1040 line 16 always directly pins the
   current taxable-income publication, filing status, rounding authority,
   current numeric qualified-dividends publication, the current numeric
   selected preferential base, the parameters of the selected QDCG or
   ordinary-tax computation, and the exact line-16/QDCG citation (this
   common set). If the selected preferential base has the direct signature,
   line 16 adds exactly the branch-specific ADR-0050 Decision 7
   declaration/conclusion pins (the four-row table in Decision 6, below); it
   adds no direct pin to C1–C4 or to box-2a family/mapping/horizon/
   closure/subtotal authority, which remain transitive through the selected
   preferential base, as ADR-0050 Decision 8 requires. If the selected
   preferential base has the Schedule D signature, line 16's exact direct
   set is the common set alone, with no declaration/conclusion pin added; it
   does not directly pin Schedule D line 16, the attachment, or the nine
   completeness authorities, which likewise remain transitive. No accepted
   Decision 7 pin moves to a new citizen, and the only line-16 change from
   ADR-0050's accepted graph is the identifier substitution
   `selected_line7a -> selected preferential base` plus this explicit
   producer-signature condition. For nonnumeric selected-preferential-base
   outcomes (`blocked`, `guard_inapplicable`, or numeric-with-blocked
   qualified-dividends), line 16's direct dependency is exactly that
   disposition, and it reads no declaration, conclusion, or numeric tax
   parameter before stopping.

   **Named production condition, not resolved here (CA-06).** The
   exactly-one-producer requirement above is a paper contract: it is not yet
   a selected generic schema/rule representation. Whether two mutually
   exclusive rule citizens may name one publication symbol, or a dedicated
   selected-binding citizen is required, remains open. Current package
   validation enforces exactly one reachable adopted producer per symbol
   absent a selecting conflict-semantics rule (ADR-0027 Decision 5), and
   ADR-0038 Decision 2 forecloses dual producers with a dynamic
   `conflict_semantics` selector as a line-16 pattern; neither precedent by
   itself selects the representation for this two-producer, disjoint-pin
   case. This is a `separate-decision` prerequisite (evidence:
   `evaluation-analysis.md` §4), appropriately scored as a narrow Rung-2
   validator/distinguishability question only after this ADR's exact pin
   contract exists — which it now does. It is not resolved by this ADR.

5. **Line 7a, line 7b, and line 9.** Form 1040 line 7a consumes the selected
   preferential base exactly once. Under the direct producer, line 7b's
   affirmative Schedule-D-not-required disposition publishes only from the
   current checked conclusion `"no"`, unchanged from ADR-0050 Decision 5.
   Under the Schedule D producer, line 7b is not affirmatively checked for
   this class. A versioned line-9 successor consumes the selected line-7a
   value exactly once, regardless of which producer supplied it; neither
   line 9 nor the QDCG worksheet may read Schedule D line 8a, line 13, a
   family subtotal, or a raw transaction member directly.

6. **Relationship to ADR-0036 and ADR-0050.** Both remain immutable history;
   nothing in this ADR edits their accepted text, and this ADR is itself an
   accepted, additive successor, never an in-place edit. ADR-0036 is
   instantiated with Schedule D content only (Decision 3) — no change to the
   attachment citizen, `collect_members`, the tie-out invariant, or presence
   semantics. For the versioned successor graph only, the following named
   ADR-0050 clauses are superseded, and no other ADR-0050 text changes:

   | ADR-0050 accepted clause | Successor effect for the versioned graph only |
   | --- | --- |
   | Decision 1, C1–C4 checked conclusion | Preserved unchanged for the direct producer. Superseded only as Schedule-D-route authority by Decision 2's nine direct reads; no second conclusion citizen is created. |
   | Decision 5, line 7a from box-2a subtotal, line 7b from conclusion `"no"` | Direct arithmetic and authority preserved, projected first into the direct producer's selected-preferential-base value; line 7a consumes that symbol, which may instead be produced by the Schedule D route. Line 7b is never affirmatively checked on the Schedule D route. |
   | Decision 6, line 9 consumes selected line 7a exactly once | Shape preserved; the successor selected line-7a publication is sourced from the selected preferential base; raw box-2a and Schedule D inputs remain forbidden. |
   | Decision 7, state partition over selected line 7a | Superseded only by the identifier substitution `selected_line7a -> selected preferential base`; the STOP/QDCG/ordinary states, their branching, and the branch-specific declaration/conclusion pins are otherwise unchanged. |
   | Decision 7, worksheet line 3 binds to line 7a in the direct case | The direct amount and authority are unchanged behind the selected preferential base. The Schedule D producer binds the same worksheet line-3 input position to the Schedule D line-16 value for this bounded slice. |
   | Decision 8, measured direct graph and kill tests | Extended with the selected preferential base's exactly-one-producer pins (Decision 4's exact table), the Schedule D boundary pins (Decision 2), mixed-producer and raw/reach-around rejection; ADR-0050's direct/transitive pin semantics are otherwise unchanged. |
   | Decision 9, relationship to ADR-0035/0038 | Preserved; this ADR is another versioned successor only. |

7. **Pins, citations, presentation, and production kill tests.** Pin has the
   ADR-0010 direct-edge meaning throughout. The measured direct graph per
   producer signature is Decision 4's exact pin table; Decision 6's ledger
   states which existing ADR-0050 pins survive unchanged and which single
   identifier is substituted. Tax-content grounding is the [2025 Schedule D
   instructions](https://www.irs.gov/pub/irs-prior/i1040sd--2025.pdf),
   "Lines 1a and 8a — Transactions Not Reported on Form 8949" (aggregate
   line-8a eligibility and columns (d)/(e)/(h)), and the [2025 Form 1099-B
   instructions](https://www.irs.gov/pub/irs-prior/i1099b--2025.pdf) (the
   covered/noncovered, box 1f, box 1g, Ordinary, QOF, and box-12 indicators
   the eligible-transaction predicate depends on). A live URL is planning
   grounding only; production must pin exact versioned repository citation
   content (ADR-0029) for line 8a, line 13, line 15, line 16, line 7a, line
   7b, and line 9, matching ADR-0050's existing exact citation for line 7b.
   Presentation of the Schedule D attachment, line 7a, and line 16 states
   follows ADR-0046 unchanged: zero-authority projection, honest blocking,
   and no rejected-value leakage.

   The kill-test set is drawn from the eleven shared prototype cases
   (`plan.md`, "Shared case matrix"; full pins in `it2/design.md` §6 and
   `repair1/design.md` §3–4): one eligible single-broker, single-transaction
   return; one eligible single-broker, multi-transaction return; eligible
   multiple-broker aggregation; transaction correction preserving sibling
   identity; each of the nine completeness components individually missing
   or violated, one walk naming the exact set; box-2a present-and-nonzero
   alongside an eligible transaction (both gains preserved exactly once via
   line 13); box-2a closed-empty (Schedule-D-only route); family lifecycle
   (closed-empty, open, undeclared, stale-horizon, correction, restoration);
   historical/raw reach-around rejection; downstream double-count and
   dual-producer rejection in both directions; and non-covered/
   adjustment-code transaction rejection at admission. Forward correction
   (direct route to Schedule D route) and reverse correction (Schedule D
   route to direct route) must each show the intermediate honest
   block/guard state and confirm no displaced finding revives
   (`repair1/design.md` §4.1–4.2).

## Rejected incumbent

The incumbent (`it1/design.md`, `it1/examination.md`) proposed nested
four-key member identity under the broker-and-statement family (mirroring
the existing K-1 and market-discount precedent one level shallower) and a
single synthesized checked conclusion generalizing ADR-0050's C1–C4 pattern
over the nine completeness components. It is not carried forward. Both
committee reviews independently corroborated its rejection
(`round-1-triage.md`, "Review agreement"):

- **CA-01.** The incumbent's committed member predicate omitted distinct
  covered-security, box-1f/1g, Ordinary, QOF, taxpayer-adjustment,
  collectibles, and special-rate exclusions, and derived gain-only from an
  amount comparison rather than a contributed assertion — admitting a
  broader source class than the milestone's Supported Source Class permits.
- **CA-03.** The incumbent's line-16 successor did not read qualified
  dividends on its Schedule-D-sourced branch at all, and its pin sets and
  correction tracing were not fully enumerated.
- **Box-2a data loss (shared case 6).** Both reviews independently
  reconstructed the same defect: the incumbent's line-7a match chose
  Schedule-D precedence over summation and never added the box-2a amount
  anywhere, silently under-reporting real taxable gain whenever both an
  eligible 1099-B gain and a nonzero box-2a amount were current.

The rival's independent anchor-keyed family, direct multi-read completeness,
and shared selected-preferential-base symbol were preferred because they
preserve both gains exactly once in the box-2a-and-Schedule-D interaction
case, name every missing or violated completeness component without a
synthesizing conclusion hop, and — after the CA-04 repair — supply an exact,
falsifiable pin contract per producer signature.

## Production conditions (owed after ratification; never allowlisted)

- Versioned citizens for the statement anchor, eligible-transaction member,
  family declaration, closure mapping, and the seven categorical absence
  declarations, none rewriting published history.
- An additive `attachment-rule.v3` (or equivalent) successor expressing a
  categorical requirement, resolving CA-05 (Decision 3).
- A selected generic schema/rule representation mechanically enforcing
  exactly one current producer of the selected preferential base, resolving
  CA-06 (Decision 4).
- Successor line-7a, line-9, and Form 1040 line-16 rule content with
  raw-source and dual-producer rejection, per Decision 4's exact pin table.
- Exact 2025 Schedule D and Form 1099-B citation citizens pinned to every new
  field and decision path (Decision 7).
- Coordinator-from-facts goldens and lifecycle tables for the full kill-test
  set in Decision 7, entering through `live_coordinate_run`.
- Package validation rejecting: a mixed graph pairing a current Schedule D
  result with a displaced boundary authority; a raw transaction, family
  subtotal, or Schedule D line read reaching line 9 or the QDCG worksheet
  directly; and a non-`{yes, no}` domain on any of the seven absence
  declarations.

## Consequences

- An eligible covered, long-term, gain-only 1099-B transaction can close a
  correctable source family independent of its statement anchor's own
  correction, matching the correction-safety already accepted for 1099-INT,
  K-1, and market-discount members.
- The nine-part completeness boundary is honest under every named
  missing/violated component: it never assumes absence and never fabricates
  Schedule D or the direct route from a thin assertion.
- Box-2a and Schedule D gains combine exactly once when both are current,
  closing the incumbent's data-loss defect, without a new line-16 branch and
  without editing ADR-0050.
- Two named schema/representation gaps (CA-05, CA-06) remain open production
  conditions; neither blocks this ADR's contract-level clauses, and neither
  may be silently absorbed into production without its own decision.
- Historical ADR-0035/0038/0050 packages and content remain loadable history;
  only packages adopting this successor graph obtain the Schedule D route.

## Non-blocking observations retained from the evidence chain

- The one recorded review dissent, CA-04, is resolved by Decision 4's exact
  pin-signature contract and independently confirmed
  (`reviews/repair1-confirmation.md`, overall verdict `READY`). See
  `evaluation-analysis.md` §3 for the full resolution record.
- CA-07 (the incumbent's unselected synthesized-conclusion binding locus) is
  moot: the incumbent is not carried forward.

## Links

- Prototype evidence:
  `docs/prototypes/schedule-d-covered-ltcg-8a/` (`plan.md`,
  `round-1-triage.md`, `it1/`, `it2/`, `repair1/`, `reviews/`,
  `evaluation-analysis.md`)
- Builds on: ADR-0003 (schema immutability), ADR-0010 (currency), ADR-0011
  (closure / no assumed zero, presence-before-value), ADR-0012 (form-field
  atomic dispositions), ADR-0014–0017 (mapping, identity, family, horizon),
  ADR-0020 / ADR-0029 (explanation, citations), ADR-0023 (member
  transitions), ADR-0027 (package manifests, single-producer-per-symbol),
  ADR-0031 / ADR-0032 (data and contribution boundaries), **ADR-0036**
  (attachment ontology), **ADR-0038** (QDCG worksheet, dual-producer
  foreclosure), **ADR-0050** (capital-gain distributions and line 7a, the
  direct route this ADR coexists with and partially supersedes for the
  versioned successor graph only), ADR-0046 (presentation)
- Consumed by: Engine Breadth production Tracks 1–3 for covered long-term
  gains / Schedule D line 8a (only after ratification and merge)
