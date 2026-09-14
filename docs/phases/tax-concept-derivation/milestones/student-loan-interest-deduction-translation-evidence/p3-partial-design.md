# P3 partial design — eligible-student status

A **decision-ready partial design** for the selected constituent, eligible-student
status under § 221(d)(1)(C) via § 25A(b)(3)(A), on the owner-accepted bounded
path.

**Evidence level and authority.** This is a requirements and design record. It is
**not an accepted contract** and **not evidence that the mechanisms it proposes
work**. Obligations 2a (a declared per-statement path) and 2b (an honest
attachment and explanation surface) are **undischarged**; 2c is discharged. No
production path exists. It implements nothing and publishes no schema.

Four defects in an earlier version of this design are established against the
executing code and are recorded here as settled: the evaluator's `parameter`
operator returns `_as_decimal` on both branches and so cannot return a
categorical catalog value, and no operator constructs a composite lookup key;
`evaluate_pairing_scoped_rule` resolves exactly `left_fact_id` and
`right_fact_id`; pairing dispatch is selected by Python rule-id registration
rather than refused at package admission; and a form field carries one static
`explain` string per disposition.

The demonstrated capability limit, stated exactly: no committed path can
currently use every current Form 1098-E box-1 statement as the iteration subject,
require exactly one usable statement association, resolve this case's
heterogeneous related facts, fail closed on an unassociated statement, and
preserve statement-isolated dependencies. The actual pairing dispatcher iterates
existing pairing records, so an unpaired box-1 statement is never visited and
produces neither a publication nor a blocked row.

## 1. The ordinary facts, and what the rule owns

The user is never asked whether they were an "eligible student," whether a
school is an "eligible educational institution," or what counts as half-time.
Those are determinations the rule owns, from the facts below.

This vertical does not consume
`tax.us.2025.f1098e.no-non-qualified-loan-component`. That compressed `{yes,
no}` is the thing P0 F5 and P1 forbade renaming. Implementing (C) does not
establish the chapeau, (A), (B), the concluding-sentence exclusions, legal
obligation, either § 221(e)(1) operation, or § 221(c). Each of those remains
on its own committed handle, or unresolved. A published line 21 from this
vertical is qualified as to eligible-student status only.

### 1.1 Facts a person supplies

Four enrollment facts and one statement-scoped association claim. Each is a
kernel assertion (ADR-0002 / ADR-0032), `supersession.policy: free`
(ADR-0041), current support resolved by `compute_currency` (ADR-0010,
ADR-0073). None is a tax conclusion.

| Fact | Proposition in ordinary words | Identity keys | Domain |
| --- | --- | --- | --- |
| School | The student whose education this loan paid for was enrolled at this school during the named academic period. | Academic-period identity (the school is a key of the period, not a free-floating school fact). Proposed entity kind `tax.us.educational-institution`, opaque id, never derived from the typed display name (the nominee-recipient minting convention). | An identified institution. Display name is provenance, not identity. |
| Academic period | This is the academic period the borrowed money paid for. | Institution + period designation (term label and academic year of the schooling, **not** tax year 2025). Proposed entity kind `tax.us.academic-period`. Enrollment during 2025 is irrelevant unless 2025 is the period the loan financed (P1 selection). | One institution-specific term. Example shape: Fall 2024 at `demo.institution.riverside`. Two periods are two identities. |
| Program | During that period, the student was a candidate in this program of study. | Filer + academic period. Bounded slice: the student is the filer. A borrower whose student is someone else is refused, not modeled (no person ontology). | Application-resolved program identifier (opaque). A typed display name is a label, not identity. Classification of that identifier is not the user's to make — see 1.2. |
| Course load | During that period, in that program, the student carried this load. | Same as program: filer + academic period. | Nonnegative quantity in the unit the institution uses for that program (credit hours or clock hours). Not a `{yes, no}` half-time answer. |
| Statement-scoped association | This Form 1098-E's box 1 is entirely interest on one loan, and that loan financed exactly the named academic period. | Existing statement identity: `lender` (`tax.us.student-loan-lender`) + `statement` (`tax.us.1098e-statement`) + `tax-year` literal `2025` (ADR-0015 pattern; `f1098e.bundle.json`). | The only admitted current value that proceeds is the single-loan single-period claim, naming the academic-period fact id. Absence of a current association is unknown composition. A mixed or multi-period claim is unconstructible on this vocabulary; see § 2c. |

The association does not mint a loan entity. It does not treat the statement
as the loan. It claims that this statement's aggregation is trivial, at the
identity the statement already has.

Correction, retraction, and reassertion of each of these five are the P2 source-and-entry record
item 4 path already confirmed for a prepared per-statement assertion:
correction is a new `assertion` at the same `fact_id`; retraction is
`finding-retracted` (the contribution batch cannot carry that kind);
reassertion is a new finding; historical findings remain in the log and are
not live tax inputs (ADR-0073).

### 1.2 Facts that come from the institution or public authority

Three determinations the application must support and cannot push onto the
user (P1 selection, the P1 loan-qualification record constituent 4). They have no precedent in this
product, which has so far treated every non-document fact as a user
assertion. They remain a different epistemic class from the user's
enrollment account. The first design stored all three as adopted
*parameters*. That representation is not executable on the current
grammar. This section names what the evaluator can actually evaluate.

Verified against `packages/derivation/evaluator.py`: `op == "parameter"`
returns `_as_decimal(...)` on **both** the keyed and unkeyed branches. A
value such as `eligible` raises `DEPENDENCY_INVALID` (`not a number`).
The keyed branch evaluates one `key` expression; committed usage is a
single `ref` (`filing_status` on MAGI parameters). No operator in the
closed set constructs a composite key. `range_lookup` / `bracket_fold`
return decimals over numeric bands. `categorical_compare` accepts `ref`
and `category_literal` only — not a parameter.

| Determination | What it is | Representation the current grammar can evaluate | Contract gap |
| --- | --- | --- | --- |
| Institution eligibility under (C) | Whether the named school is an institution eligible under HEA § 1094, as incorporated by § 25A(b)(3)(A) → HEA § 484(a)(1). Not the chapeau's § 25A(f)(2) → HEA § 481 test. | A **categorical kernel fact**, domain `{eligible, not-eligible}`, identity = application-resolved institution id + academic period (or the catalog row's effective interval that covers that period). The rule reads it by `ref` and `categorical_compare` against `category_literal`. Typed school name is a label, not identity. | **No categorical-returning parameter.** An adopted-parameter catalog of `{eligible, not-eligible}` cannot be evaluated. Encoding the category as `1`/`0` would hide the determination in a number and is refused. |
| Program classification | Whether the named program is candidacy for a degree, certificate, or other recognized credential. | A **categorical kernel fact**, domain `{recognized-credential, not-recognized}`, identity = application-resolved program id + academic period (or covering interval). Typed program name is a label. Same `ref` / `categorical_compare` path. | Same gap: no categorical-returning parameter, and no lookup keyed on institution id *plus* program id. |
| Institution-certified half-time threshold | The institution's own half-time threshold for that program in that academic period, in the same unit as the user's course load. Compared **directly** with course load (§ 1.2a). Not a full-time workload the rule halves. | A **numeric** adopted parameter, keyed by **one** application-resolved standard id (that id already identifies institution + program + period; the evaluator does not concatenate keys). The rule's `parameter` node uses `key: {op: ref, name: <that id's bound symbol>}`, the same single-`ref` shape as `filing_status`. Catalog miss is `LOOKUP_MISS`. | **No composite-key operator.** A declared lookup keyed on more than one value (institution, program, period as separate expressions) cannot be written. The single opaque standard id is the only executable key shape. |

Who produces the catalog rows is still not the user. In a production
package they would be adopted content of some citizen kind. The only
*evaluable* citizen kinds today are: numeric parameters (half-time), and
current facts that `ref` can read (the two categoricals). Treating the
categoricals as workspace facts in the probe does not make them user
assertions of tax conclusions — the user still does not answer "is this
school eligible." It does mean the first design's "same class as a tax
parameter" claim does not hold for those two rows until a
categorical-returning parameter (or equivalent catalog operator) exists.

A user assertion that "this school is eligible" or "I was half-time" is
still not an input.

`fact-type.v2` declares vocabulary. It does not supply a current
institution-eligibility or program-classification finding. The feasibility probe
injects institution eligibility into a local `Environment` to test
evaluation mechanics. `VALUE_EXPR` does **not** read program
classification; it is a partial mechanics witness, not the full (C)
tree. Injected probe facts are **not** a production catalog. Production
still lacks the authoritative producer or adoption mechanism. Remaining
choice: those determinations become current findings through a defined
evidence/producer path, **or** the rule grammar gains an adopted
categorical catalog/parameter mechanism.

Where a catalog row cannot be established, the route stays unresolved and
never favorable. Missing categorical facts are `DEPENDENCY_ABSENT`.
`LOOKUP_MISS` is reserved for the numeric half-time parameter row.

### 1.2a Half-time quantity (one definition)

The comparison quantity is the **institution-certified half-time
threshold**, compared directly with the user's course load. Load at or
above the threshold supports (C) on this predicate; load below is a
supported negative. The statute's "at least half the normal full-time
workload" is what that certified threshold already is; the rule does not
compute one half of a full-time number. Full-time is not required (the P1 loan-qualification record,
Example 3 of § 1.221-1(e)(4)). Every case and rule description in this
document uses this quantity only.

### 1.3 What the rule owns

From the association, the enrollment facts, and the catalog, an adopted rule
determines:

1. whether composition is known and trivial (one loan, one period), or is
   refused;
2. whether eligible-student status is **supported favorable**, **supported
   negative**, or **unresolved**, for that loan and period;
3. therefore whether this statement's box-1 amount is interest on a qualified
   education loan *as to (C)*, or is not, or cannot be decided.

The user never supplies that tax conclusion. A post-hoc process record is not
an input.

Remaining § 221(d)(1) constituents stay unresolved. A C1 success explain must
not say "complete eligibility authority" — that is the incumbent
`schedule1.line-21` published_value string, and it would pretend the rest of
the definition is complete.

---

## 2. The three open obligations

Each obligation is discharged against committed artifacts and executing code,
not by restating the scope decision.

### 2a. A declared per-statement path — open (repair)

**What is proved, and what is not.** Track 4b proves that a consumer can apply
an aggregate-wide scalar cap while the family's authorized subtotal stays
raw. Confirmed on the committed below-floor golden: attachment
`tieOutText` is `Reported subtotal: 3000` while `line-sch1-21` publishes
`2500` (`packages/sample_data/f1098e_student_loan_interest_track6/presentation/below-floor.presentation-model.v1.json`).
That is not report-specific qualification. G1 and the P2 computation-and-consumers record § 2.4 shape 1 say
so; the executing evaluator confirms why.

`Environment.sources` is `dict[str, list[str]]` — values only
(`packages/derivation/evaluator.py`). `_Run.env()` passes `self.sources`
with no identity (`runner.py`). `collect` and
`collect_categorical_all_equal` both read `env.sources[name]` as a list of
values. One `"yes"` row therefore covers every collected amount (P0 F2 / C6;
the P2 source-and-entry record item 2). Identity is not absent from the run: `SourceFact` carries
`fact_id` and lattice `keys` (`marshal.py`, `runner.py`), and
`self.source_fids` / `self.source_fact_ids` sit beside the value lists.
Ordinary rule evaluation drops that identity. A values-only fold cannot pair
statement A’s box 1 with statement A’s enrollment.

**The P2 computation-and-consumers record § 2.4 shapes, chosen and rejected.**

| Shape | Why it is or is not this path |
| --- | --- |
| 1. Qualify in the consumer, leave the family subtotal raw | The **downstream** half of this path. The worksheet already refs a scalar and applies cap and MAGI (the P2 computation-and-consumers record item 1.3). That consumer can consume an eligible-student-supported scalar the same way it consumes the raw one. Shape 1 does not itself produce per-statement qualification. |
| 2. Second source family of eligible-student-supported amounts | Rejected as the per-statement producer. Those amounts are derived tax results, not reported source members. Putting them in a source family would make a family subtotal carry a different predicate than its members (ADR-0016 Decision 4). |
| 3. Subtractive adjustment family | Rejected as the producer. A user-asserted subtractand would be the tax conclusion. A derived subtractand still needs per-statement evaluation, which this shape does not supply. |
| 4. v9 aggregation of derived per-item findings | The **declared sum** of this path. Precedent: `tax.us.2025.rule.interest.derived-nominee-subtotal` v1 (`rule-artifact.v9`, `aggregation.mode: sum`, `absence: inapplicable`, `blocked: propagate`). `audit_collect_authority` does not constrain it because there is no `collect` / `source_set` (the P2 computation-and-consumers record § 2.4; `_collect_source_sets` walks `op == "collect"` only). |
| 5. Exclusive-presence selection among subtractands | Not needed. This vertical has one eligible-student-supported-subtotal producer, not a legacy/new pair. |
| 6. Refuse mixed composition so no eligible-student-supported subset is published | Discharges C7 (unknown/mixed *on one statement*). Does not discharge C6 (two statements with different circumstances). Kept as the composition refusal, not as the per-statement path. |

**What the committed primitives actually bind.**

The association payload, at statement identity (`lender` + `statement` +
`tax-year`), is an object naming current fact ids:

- `box1_fact_id` — this statement’s box-1 amount
- `academic_period_fact_id` — the period the sole loan financed
- `enrollment_fact_id` — filer + that period (program id, course load,
  application-resolved half-time-standard id)
- `institution_eligibility_fact_id` — categorical catalog row for that
  institution + period
- `program_classification_fact_id` — categorical catalog row for that
  program + period

That is a heterogeneous set. The committed per-item primitives:

| Primitive | What it binds | Gate |
| --- | --- | --- |
| `evaluate_pairing_scoped_rule` | Exactly `left_fact_id` and `right_fact_id` from the pairing payload (`pairing_dispatch.py`). Two facts, indexed by type. The pairing `SourceFact` itself is the driver, not a third resolved peer. | Python rule-id registration (`PAIRING_SCOPED_CONSEQUENCE_RULE_IDS`). **Not** refused at package admission. The first design’s contrary claim is withdrawn. |
| `bound_sources` | One nonempty group of *values* for one named fact type. Not heterogeneous. | Package admission `MEMBER_NO_BINDING_PATH` except nominee-reduction. |
| v9 `aggregation` | Sum of already-published suffixed findings. Does not bind inputs. | Package admission `NOMINEE_AGGREGATE_ID_INVALID` except the nominee aggregate. |
| Ordinary `_Run.env()` / `ref` | One current value per symbol name. Two statements of the same type are ambiguous (marshal disagreement leaves unbound). | n/a |

**The pairing primitive’s left and right, if forced onto this association.**
The only 1:1 pair that is actually two facts of this vertical is **box 1**
(left) and **enrollment** (right), with the association as the pairing
record. That binds the reported amount and the user’s course load /
program id / standard id (by `ref`+`field` on the enrollment object). It
does **not** bind the two categorical catalog facts, the academic-period
fact (except as a field already copied onto enrollment), or a keyed
parameter’s pin identity beyond what `AccessLog.parameters` records.

**Additional facts, without a run-wide ambiguous binding.** Options that
are *not* committed primitives:

1. Copy catalog fields onto the enrollment object — mixes institutional
   authority into a user fact and goes stale when the catalog changes.
2. A Python coordinator that indexes further fact ids from the
   association payload, the way pairing indexes two. That is new
   heterogeneous group-binding, not `evaluate_pairing_scoped_rule`.
3. Run-wide `ref` of the catalog fact types — ambiguous once two
   institutions or two periods are live.

**Missing, duplicate, stale, mismatched.**

| Condition | Honest failure |
| --- | --- |
| No current association for a live box-1 member | Completeness failure. Iteration is driven by **current box-1 family members**, not by association findings. Each box-1 must have exactly one usable association. Association-driven (pairing) dispatch publishes associated statements and **silently omits** the rest — P0 F2 in a new place. The aggregate and line 21 must block or remain unresolved; they must not publish the associated subset. Pairing cannot see an unassociated box-1. |
| Association names a `fact_id` with no current finding | `DEPENDENCY_ABSENT` naming that id (pairing already does this for missing left/right) |
| Two current findings for the named `fact_id` | Currency forbids this; if sources contain two of the same `fact_id`, `_index_by_fact_id` last-wins — a primitive defect to refuse, not rely on |
| Enrollment’s period id ≠ association’s `academic_period_fact_id` | Mismatch; `DEPENDENCY_INVALID` / composition mixed. Pairing does not compare extra fields. |
| Catalog fact’s institution/program/period keys ≠ enrollment’s | Same mismatch; not checked by pairing |

**Pins.** Pairing’s `present_pins` on a real dispatcher call are the
pairing finding, the left finding, and the right finding. Isolation of
two statements’ findings through a production coordinator is **not
proven**. AccessLog symbol names in a hand-built env, and pins authored
onto synthetic derived findings, do not establish finding-level pin
selection.

**Conclusion, after the probe.** No committed primitive binds this
heterogeneous set **or** proves completeness over every current box-1
member. `evaluate_pairing_scoped_rule` with two box-1 `SourceFact`s and
one pairing emitted one publication (`2000`), pinned A, did not pin B,
and recorded zero blocked rows. Box-1-driven completeness is conceptual:
no committed coordinator performs it; the probe computes it by hand. A
**partial** mechanics `value` (eligibility + half-time; no program
classification) evaluates in a hand-built local `Environment`. That is
not the full (C) tree and not a production path. Owner decision:
reusable heterogeneous group-binding with box-1-driven completeness, not
a bespoke exact-rule ADR. Pin isolation is not proven.

The incumbent `collect_categorical_all_equal` of
`no-non-qualified-loan-component` is not on this path. Eligible-student
status is not computed in Python. The tax tree, when an environment
exists, remains `choose` / `categorical_compare` / `compare` /
`parameter` / `block` / `ref`.

**What a local evaluation would publish**, if and only if the binding
path exists: supported negative → `0` for that statement’s box 1;
supported favorable → that box-1 amount; missing support → `block`.
Suffixed `{eligible-student-supported-interest-prefix}|{box1-fact-id}`.
A v9 aggregate of those suffixes remains the declared *sum* shape, still
nominee-locked at admission. The worksheet would consume that sum as line
1; the raw family subtotal stays the attachment tie-out. That consumer
half is unchanged from Track 4b and is not the open obligation.

### 2b. An honest attachment and explanation surface — open (repair)

**Defect 4, not re-litigated.** `schedule1.line-21` has one static
`dispositions.blocked.explain` string, and one static string per other
disposition. The form field cannot dynamically name which statement
failed on which predicate. The renderer shows `activeCodes` filtered
through that static `codes` list; unknown codes become `(unspecified)`
(the P2 computation-and-consumers record item 4.2). Citation sites are the source leaves the projector
actually walks, not an explanation carrier.

**The committed heading problem, still real.** Below-floor golden:
heading `Line 21: Student Loan Interest Deduction`, `tieOutText`
`Reported subtotal: 3000`, line 21 `published_value` `2500`. Relabelling
the attachment part as reported box-1 interest remains the honest
*heading* repair (projector copies `label` → `heading`). It does not
give the field a per-statement explain.

**Narrowed promise — what this surface can show.**

| Reader-visible distinction | How it is shown | What it is not |
| --- | --- | --- |
| Supported favorable vs supported negative vs missing support | Disposition: nonzero `published_value`; numeric `0` (`published_value` or `computed_zero`); `blocked` | The static explain does not say *which* statement or *which* (C) predicate |
| Which findings contributed to a published number | Citation sites to non-closure source leaves actually pinned | Not a structured “statement B failed half-time” sentence |
| Reported box 1 vs line 21 | Relabelled attachment heading vs the form-field label, when the attachment is required | Collapses when the attachment is absent |

**Supported-zero / attachment absent.** Attachment `requirement` keys off
line 21 (and unemployment) strictly greater than zero. A supported
negative that is the only statement, or two statements whose
eligible-student-supported sum is `0`, makes line 21 `0`. The attachment
is then `guard_inapplicable` (“Not required.”). The reader does **not**
see the raw box-1 itemization at all — including the not-eligible-student-supported
statement’s reported amount. Relabel does not help on that path. The
narrowed promise therefore: when line 21 is a supported `0`, the reader
sees the numeric zero and the static computed-zero explain, plus whatever
citation sites the projector kept; they do not see a per-statement
reported inventory. A new explanation carrier would be required to name
the statement and predicate on that path. No carrier is invented here.

**What a reader-facing surface would show (narrowed).** Probe evidence for
these dispositions is presentation projection over synthetic publications
and dispositions, not `live_coordinate_run` or citation-walk. The
attachment-inapplicable observation in the probe used a manually supplied
inapplicable row; the committed requirement (not-required when line 21 is
0) was established in P2.

| Case | Attachment | Line 21 |
| --- | --- | --- |
| C1 favorable, box 1 `2000` | If required: reported-interest heading; members cited | `published_value` `2000`; static published explain (must not say “complete eligibility authority”) |
| Cap `3000` / `2500` | Reported heading; tie-out `3000` | `published_value` `2500`; static explain. Headings differ if relabelled |
| A favorable `2000`, B supported negative `1000` (sum > 0) | Both members under reported heading | `published_value` of A after cap/MAGI. Static explain. Citations may include A’s leaves; they do not *say* “B failed half-time” |
| Only B, supported negative `1000` → line 21 `0` | **Not required.** No itemization | Numeric `0`; static computed-zero explain. B’s reported amount is not on this surface |
| Missing support / unknown composition | Present only if some other requirement subtotal is > 0 | `blocked`; static blocked explain; code visible **only if** on the allowlist (G5 still applies to incumbent `SLI_*` codes) |
| Closed-empty | Not required | F7 numeric zero until Track 0 |

G5 allowlist repair (add every code line 21 still emits) remains owed as
content, not as a per-statement explain. A new explanation carrier is an
owner decision if the product needs the statement and predicate named;
see the feasibility probe.

### 2c. A statement-scoped association that earns its scope — discharged

The P2 source-and-entry record item 6.1 stands: a single-loan single-period association *in
general* needs a distinct loan entity, because the general case must talk
about the loan independently of the statement. The bounded path does not
refute that general finding. It holds here only by relational
identification plus refusal, and only inside the bounds below.

**Why relational identification holds on this slice.**

The association’s proposition is about *this statement’s composition*, not
about a loan object. Identity keys are the statement’s existing
`lender` + `statement` + `tax-year`. The claim, in ordinary words: this
box 1 is entirely interest on one loan, and that loan financed exactly the
named academic period. The loan is identified the way ADR-0068 identifies
a report: by an explicit, accountable claim scoped to the specific
statement named at contribution time, never by treating a join or a
statement id as the loan.

The academic period is first-class vocabulary (§ 1.1). Institutional
evidence attaches to that period and to the enrollment at that period,
not to the statement. The association carries the period by naming its
stable `fact_id` (the identity, not a finding id or version).

Attributable interest is the whole box-1 amount *because* the claim made
composition trivial. That is a consequence of the claim, not an
allocation, and not a use of the statement as a loan proxy (the P2 source-and-entry record
3.1 failure mode: tests treating two statements as “e.g. two loans”).

**Lifecycle — one account.** The association names a stable academic-period
`fact_id`. Correction at that identity is followed automatically: the next
evaluation reads the current finding for that `fact_id`. The association
does **not** pin a particular finding id or version of the period. The
competing stale-target account (association becomes stale when the named
period finding is displaced, and must be recast) is deleted.

The association is a kernel assertion, not a derived pairing: Form 1098-E
omits which loans box 1 aggregates (P0.1), so there is no structural match
to derive from. Absence of the claim is unknown composition. Path as Unit
C item 4 confirmed: correction is a new `assertion` at the same
association `fact_id`; retraction is `finding-retracted`; reassertion is a
new finding.

| Event | Effect on later runs |
| --- | --- |
| Correction of attributes of the named period, at that period `fact_id` | Association unchanged (it still names the same `fact_id`). Current period finding is the correction. Next evaluation follows it. |
| Association corrected to name a *different* period `fact_id` | New association finding at the same statement identity; previous displaced `correction`. Evaluation uses the newly named identity. |
| Correction of course load at the enrollment identity | Association unchanged. Next evaluation sees the new load. At-or-above threshold becoming below is a supported negative, not missing support. |
| Current finding for the named period `fact_id` retracted, none replaces it | Missing support (`DEPENDENCY_ABSENT` on that id), not a stale association that needs recasting. |
| Retraction of the association | Ends current support; no opposite claim (ADR-0073). Composition unknown. Retracting enrollment while the association remains is `DEPENDENCY_ABSENT`, not unknown composition. |
| Reassertion | New finding, new current support. Historical ids stay stored and non-current. |

**Refusal, and where the avoidance stops holding.**

| Composition | Product disposition | Why the statement-scoped claim is honest |
| --- | --- | --- |
| User asserts single-loan single-period, names one period | Proceeds; whole box 1 is attributable to that sole loan | The claim is the proposition; identity is the statement’s |
| No current association | `SLI_COMPOSITION_UNKNOWN`; line 21 blocked | Unknown is the current state of every 1098-E (P0.1, the P2 source-and-entry record 6.3) |
| User cannot name one period (loan financed two terms with different enrollment) | Claim unconstructible; same unknown/mixed refusal | A single named period would pretend the periods are uniform (P1 composition level 2) |
| Two current associations for one statement | Admission cardinality refusal | One statement identity cannot carry two composition claims |
| Student is not the filer | Refused, not modeled | No person ontology; parent-borrower would mis-key enrollment |
| One statement, two loans, different enrollment | Refused, not allocated | Relational identification cannot name “the” loan; this is C7’s general case, deferred to a successor milestone with a loan entity and per-loan amounts (scope decision, “Deferred”) |
| Two statements reporting the same real loan | Each statement has its own association; the design does not know they are the same loan | Stops holding the moment the product must refer to the loan across statements. Not in this milestone |

The avoidance holds only while every live statement on the route is one
the taxpayer can honestly describe as single-loan and single-period, the
student is the filer, and no consumer needs a loan identity distinct from
“the sole loan this statement represents.” The general aggregating case is
refused, not modeled.

---

## 3. The case table

Every case distinguishes **missing support** (no current enrollment, no
catalog row, no association) from a **supported negative** (enrollment and
catalog present; the rule determines that (C) fails). Missing support
blocks or leaves the route unresolved. A supported negative publishes a
per-statement `0` and, when every other live statement has a number, a
eligible-student-supported subtotal that omits that statement’s box 1. Synthetic identities
only (`demo.*`).

Incumbent gates that this slice does not replace — the four remaining
per-statement witnesses, filer-level worksheet-selection, legal-zero,
filing status, Part II absences, MAGI parameters — are held at their
committed passing values in every case below unless a row says otherwise.
Chapeau, (A), and (B) are unresolved; a C1 publication does not establish
them.

### 3.1 Two positives

**P-fav — supported favorable (C1).** One Form 1098-E,
`demo.sli.lender.a` / `demo.sli.stmt.a`, box 1 `2000`. Association:
single-loan single-period, names `demo.period.riverside.fall-2024`.
Enrollment: filer at that period, program id `demo.program.ba-biology`,
course load `12` credit hours. Catalog: institution eligible under HEA
§ 1094; program is a recognized credential; institution-certified
half-time threshold `6` (compared directly with `12`; the rule does not
halve a full-time number). MAGI below the floor.

- Rule owns: (C) holds; eligible-student-supported amount is the whole `2000`.
- Line 21: `published_value` `2000` after cap (cap not binding).
- Missing support vs supported negative: neither. Support is present and
  favorable.
- Maps to **C1**, and the below-floor half of **C8**. Reader account
  **C10** is a required property of a production path, not something this
  probe proved. Presentation evidence here is projection over synthetic
  publications and dispositions. Pin isolation is not proven.

**P-cap — supported favorable, over the cap.** Same ordinary support as
P-fav; box 1 `3000`. Eligible-student-supported subtotal `3000`; worksheet cap publishes
line 21 `2500`. Attachment lists reported `3000` under the reported-
interest heading. Maps to **C1** composed with the committed cap (Track
4b), still **C8** below-floor MAGI. Distinguishes reported interest from
the deduction (§ 2b). Not a (C) negative.

### 3.2 Two meaningful negatives

**N-load — supported unfavorable, below the certified half-time
threshold (C2).** Same statement and association as P-fav. Enrollment
present: course load `3` against certified half-time threshold `6`.
Program recognized; institution eligible.

- Rule owns: (C) fails because the supported load is below the
  institution’s standard. Per-statement publication `0`.
- Line 21: `computed_zero` or `published_value` `0` from an eligible-student-supported
  subtotal of `0`, then cap/MAGI of `0` — a number, not a block. Distinct
  from missing support, which would not publish.
- Maps to **C2**. The product disposition is distinguishable from a
  refusal (Fixed cases C2). Incumbent adverse `"no"` on the compressed
  witness blocked the whole route with `SLI_UNIVERSAL_COMPONENT_VIOLATION`;
  this case does not.

**N-mix — C6, two statements, mixed (C) support.**
`demo.sli.stmt.a` as P-fav (`2000`, supported favorable).
`demo.sli.stmt.b` from `demo.sli.lender.b`, box 1 `1000`, own association
to `demo.period.riverside.spring-2024`, enrollment course load `3` against
certified half-time threshold `6` (supported unfavorable). Ordering of
contribution does not change the result.

- Per-statement: A publishes `2000`; B publishes `0`. Aggregate `2000`.
- Line 21: A’s amount after cap/MAGI. B’s `1000` remains in the reported
  attachment itemization and does not enter worksheet line 1.
- One statement’s favorable answer does not hide the other’s supported
  negative in the **computation** (**C6**), if a box-1-driven coordinator
  exists. The reader-facing field does not name B’s negative (§ 2b).
  If B’s enrollment were absent instead, the aggregate would block and
  A’s `2000` would not become line 21. If B has **no association**,
  association-driven dispatch would publish A and omit B; that must
  block (R-comp).

### 3.3 Required additional cases

**U-catalog — unresolved institution or half-time threshold.** Two
distinct misses, not one:

- Institution-eligibility (or program-classification) categorical fact
  absent: `DEPENDENCY_ABSENT` on that fact type. The probe injects this
  category to test the tree; production has no producer.
- Half-time parameter has no row for the application-resolved standard
  id: `LOOKUP_MISS`. That code is reserved for this numeric parameter.

Neither is a supported negative. Line 21 `blocked`. Maps to **C3**.

**R-comp — unknown or mixed composition refused (C7), including the
two-statement hole.** One statement, box 1 `2000`, no current
association — or two current box-1 statements with a usable association
for A only. Enrollment for some period may exist; it is not attached to
B. Association-driven dispatch would publish A and omit B. Box-1-driven
completeness blocks the aggregate.

- Missing support of the association claim, which this design *defines*
  as unknown composition, not as a supported negative about enrollment.
  Line 21 `blocked` `SLI_COMPOSITION_UNKNOWN`. A user who cannot name one
  period cannot construct the claim (multi-period mix); same block with
  `SLI_COMPOSITION_MIXED` if a mixed value were ever admitted — on this
  vocabulary it is unconstructible. Maps to **C7**’s statement-scoped
  branch, third resolution. Does not invent a loan entity.

### 3.4 Correction / retraction / reassertion trace (C4, C5)

Start from P-fav. Same association identity
`lender=demo.sli.lender.a`, `statement=demo.sli.stmt.a`, `tax-year=2025`
throughout.

1. **Assert** association + enrollment (load `12`). Run: line 21 `2000`
   (C1).
2. **Correct** course load to `3` at the enrollment identity. Run: line
   21 `0` from supported negative (C2 / C4). Prior load `12` finding is
   displaced `correction`; it is not a live input.
3. **Retract** the association. Run: line 21 `blocked`
   `SLI_COMPOSITION_UNKNOWN` (C5, C7). The corrected enrollment remains
   current but does not cover the statement. Retracting enrollment
   *instead*, leaving the association, would be `DEPENDENCY_ABSENT` (C3)
   — missing support, not unknown composition. Those two blocks must
   remain distinguishable on the form-field allowlist (C10 / G5).
4. **Reassert** the association, still naming the same period. Run: line
   21 `0` again from the still-current load `3`. The retracted
   association finding is not revived; the new finding is current (C5).
5. **Correct** load back to `12`. Run: line 21 `2000` (C1 restored).

### 3.5 C6 ordering

N-mix plus the swap of contribution order of A and B. Eligible-student-supported subtotal
and line 21 are identical. A values-only `collect_categorical_all_equal`
fold is not on this path, so the incumbent C6 coverage failure cannot
recur.

### 3.6 Fixed cases this vertical does not reach

| Fixed case | Why this vertical does not reach it |
| --- | --- |
| **C0a** | Closed-empty publishes a numeric line 21 from `count == 0` (P0 F7, G6, the P2 computation-and-consumers record item 6). This vertical does not fire per-statement rules when there are no statements. Track 0 closes the disposition. |
| **C0b** | Documentless-interest input route is excluded. Same disposition as C0a; this milestone states the limitation. |
| **C7 general aggregating case** (honest per-loan allocation, or a loan entity for mixed loans that *are* described) | Refused, not modeled. R-comp is the third resolution only. |
| **C8 inside the phaseout, as a new (C) proof** | MAGI arithmetic is committed (the P2 computation-and-consumers record item 1.3). This vertical composes with it by feeding an eligible-student-supported scalar into the same consumer. It does not re-prove the ratio. A production fixture should still *include* one in-band C1 and one in-band C2 so provenance is distinguishable (C8’s required observation). |
| **C9** | Form 2555 / 4563 / territorial-income still block the standard worksheet (`SLI_UNIVERSAL_COMPONENT_VIOLATION` on those three filer facts, or the incumbent code). This vertical does not implement Publication 970. |
| **C2 via “not in a program”** | N-load uses below half-time. A sibling N-prog (program catalog `not-recognized`, load otherwise sufficient) is the same C2 shape and should ship as a fixture; it is not a separate fixed case. |
| Parent-borrower / non-filer student | Refused (§ 2c). Not a fixed case; named so C1 is not read as covering it. |

**C3** is reached by U-catalog and by retraction-of-enrollment in the
trace. **C4** and **C5** are the trace. **C6** is N-mix. **C10** binds
every row: success, computed-zero, blocked, and (until Track 0) the
unreached closed-empty zero. `unavailable` is not a current presentation
state (the P2 computation-and-consumers record item 4); blocked with a named code is how missing support
is shown.

---

## 4. Producer → authority → consumer → failure map

G5 today: eight gates collapse to one block code, the form field’s
allowlist omits every `SLI_*` code, and the renderer drops unknown codes,
so a reader cannot tell which circumstance caused a refusal (the P2 computation-and-consumers record item
4.2). This vertical is honest only if each failure below has a named
disposition a reader can tell from the others.

### 4.1 Facts this vertical introduces

| Fact | Producer | Authority that owns the determination | Consumers |
| --- | --- | --- | --- |
| School / academic period | Ordinary-language producer, contribution batch `assertion` (the P2 source-and-entry record 4.1 / 5.4). No 1098-E producer exists today (P0 F1, the P2 source-and-entry record 5.1). | User asserts which school and which period the loan paid for. Not a tax classification. | Association (names the period); catalog keys; per-statement rule |
| Program, course load | Same producer, same batch, enrollment identity filer + period | User asserts the ordinary enrollment account | Per-statement rule |
| Statement-scoped association | Same producer. Fact id derived from lender + statement + tax-year, like `derive_nominee_allocation_fact_id`. Evidence mode `ordinary-language-entry` (nominee producer precedent, the P2 source-and-entry record 4.5). | User asserts composition triviality and names the period. The application does not infer composition from the form (the form omits it). | Completeness check: every current box-1 member has exactly one. Not the iteration driver. Pairing dispatch driven by association findings cannot see an unassociated box-1. |
| Institution eligibility | **No production producer.** Probe injects a categorical symbol to test `categorical_compare`. `fact-type.v2` is vocabulary only. | Public / institutional authority, not the user. Not an adopted numeric parameter. | Per-statement rule via `ref` / `categorical_compare` **if** a current finding exists |
| Program classification | Same gap as institution eligibility | Same | Same |
| Institution-certified half-time threshold | Numeric adopted parameter, keyed by one application-resolved standard id. The only catalog row presently representable as a parameter. | Public / institutional authority | Per-statement rule via keyed `parameter`; miss is `LOOKUP_MISS` |
| Box 1, box 2, family closure | Incumbent Form 1098-E contribution and closure. Unchanged. | Lender’s reported figure; completeness claim as P0 F7 states it | Raw subtotal collect; attachment itemization; per-statement rule reads this statement’s box 1 by fact id |
| Per-statement eligible-student-supported amount | Adopted per-statement rule (§ 2a). Dispatch is not the authority. | The adopted rule’s declared `value`, pinning the rule artifact (ADR-0007, ADR-0071) | v9 aggregate (`blocked: propagate`) |
| Eligible-student-supported subtotal | Adopted aggregate producer | Declared `aggregation` (sum of current suffixed publications) | Worksheet successor, as worksheet line 1 |
| Line 21 | Worksheet successor: cap and MAGI on the eligible-student-supported subtotal | Same committed arithmetic (the P2 computation-and-consumers record item 1.3), new line-1 symbol | Line 26 `ref`; form field `schedule1.line-21`; attachment *requirement* (not tie-out) |
| Raw family subtotal | Incumbent `rule.sli-worksheet-line1-subtotal` | Family `authorizes_subtotal` (ADR-0016) | Attachment tie-out only. Not worksheet line 1. |

Retraction of ordinary assertions is a dedicated helper, because
`apply_contribution_batch` refuses `finding-retracted` (the P2 source-and-entry record 4.1, 4.5).
The half-time parameter is not retracted by the user; it changes by
package succession. Categorical catalog rows have no production producer
to retract.

### 4.2 Failure paths

Each row is a product disposition. None is a tax-law zero except the
supported-negative `0` for a statement whose interest is not eligible-student-supported, attributable
interest.

| Failure | Disposition | Named code / kind | Downstream | Can a reader tell it from the others? |
| --- | --- | --- | --- | --- |
| No current association for a live box-1 (R-comp), including A associated and B not | Box-1-driven completeness `block`; aggregate unpublished; must **not** publish A alone | `SLI_COMPOSITION_UNKNOWN` if allowlisted; otherwise renderer `(unspecified)` | Line 26 / line 10 / AGI `DEPENDENCY_ABSENT` naming line 21 (G4). No silent zero. | **Partly.** Disposition is a block. Static explain does not name the unassociated statement. Association-driven dispatch would hide this failure. |
| Mixed / multi-period claim (unconstructible, or refused if somehow present) | Same path | `SLI_COMPOSITION_MIXED` | Same | **Yes**, distinct code from unknown. |
| Enrollment absent (C3) | Per-statement `block` | `DEPENDENCY_ABSENT` missing the enrollment fact type | Same aggregate/line 21 block | **Yes.** `DEPENDENCY_ABSENT` is already on the allowlist. Distinct from composition codes. Trace step 3 (retract enrollment vs retract association) is the test. |
| Missing institution-eligibility or program-classification fact | Per-statement `block` | `DEPENDENCY_ABSENT` on that fact type. Not `LOOKUP_MISS`. | Same aggregate/line 21 block | **Partly.** Same missing-support code as enrollment absence. Production has no producer for these facts. |
| Half-time parameter row absent (U-catalog numeric) | Per-statement `block` | `LOOKUP_MISS` — reserved for this keyed numeric parameter | Same | **Yes, if the code is on the allowlist.** Committed line-21 list omits it (the P2 computation-and-consumers record item 4.2). |
| Institution `not-eligible`, program `not-recognized`, or load below certified half-time threshold (N-load, N-prog) | Per-statement publishes `0`; aggregate sums; line 21 a number (possibly 0) | Not a block. `published_value` or `computed_zero` | Line 26 refs the number. Attachment lists reported box 1 **only if** line 21 > 0; a sole supported-zero hides the itemization (§ 2b) | **Partly.** Disposition (a number vs `blocked`) distinguishes supported negative from missing support. The static explain does not name the statement or predicate. |
| Named period `fact_id` has no current finding | Per-statement `block` | `DEPENDENCY_ABSENT` naming that id | Same aggregate/line 21 block | **Yes**, same missing-support code as enrollment absence; the `missing` list names the period id rather than the enrollment type. Not a stale-target recast (§ 2c). |
| Incumbent MFS | Worksheet `SLI_MFS_INELIGIBLE` | Already emitted; **not** on the committed allowlist (G5) | Line 26 `DEPENDENCY_ABSENT` | **Not today.** Successor allowlist must add it or MFS remains `(unspecified)` beside (C) blocks. This vertical does not change the MFS gate; it does owe the allowlist repair for every code line 21 can still emit, or G5 remains. |
| Incumbent remaining universal witnesses (related-person, employer-plan, employer assistance, QTP) | `SLI_UNIVERSAL_COMPONENT_VIOLATION` | Same G5 drop | Same | **Not today**, and this vertical does not split those four. They remain one code. (C) is no longer among them. |
| Incumbent Part II `"no"` | Worksheet `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE`; line 26 `guard_inapplicable` (the P2 computation-and-consumers record item 3.2) | Same G5 drop on line 21 | Line 26 inapplicable, not blocked | Line 26 inapplicable vs line 21 blocked is already a different field. Line 21 still needs the code on its allowlist. |
| Closed-empty (C0a) | Line 21 literal `0`, `closure_backed_zero` | Not a (C) failure | Line 26 / 10 / AGI compute from that 0 (F7) | Reader currently sees a displayed `0` attributed to complete authority. Track 0. This vertical does not make it worse and does not claim to fix it. |
| Unclosed family | `SOURCE_SET_UNCLOSED` | Already on the allowlist | Line 21 blocked | **Yes** today. |

**G5 after this vertical.** A reader can tell a published number from a
block (supported negative vs missing support) by disposition. They cannot
be told *which* statement or *which* (C) predicate from the static
explain (defect 4). Unknown composition is distinguishable from missing
enrollment only if the codes are on the allowlist and differ. A reader
still cannot tell the remaining four per-statement witnesses apart (one
incumbent code). MFS and Part II stay `(unspecified)` until
`SLI_MFS_INELIGIBLE` and `SLI_SCHEDULE1_PART_II_OUT_OF_SCOPE` are on the
allowlist — content owed because line 21 already emits them.

### 4.3 What does not consume this vertical’s result

- Family `tax.us.2025.f1098e.1` and its collect rule — raw sum only.
- Line 9 / total-income — no feedback into MAGI (the P2 computation-and-consumers record item 3.4).
- The compressed witness `no-non-qualified-loan-component` — not an
  input and not a consumer.
- Closed-empty `count == 0` branch — does not read (C).

---

## 5. Contract assessment

The vertical fits some accepted fact, assertion, retraction, and
presentation *shapes*. It does **not** fit per-item evaluation, catalog
input, or completeness over every current box-1 member. The probe did
**not** establish one additive ADR with no new operator and no new schema
family. That claim is withdrawn. This section does not publish bytes.

### 5.1 What already fits

| Contract | Fit |
| --- | --- |
| ADR-0002 / ADR-0032 | Ordinary facts enter as contribution-batch `assertion`s. Retraction is `finding-retracted` outside the batch (the P2 source-and-entry record 4.1). |
| ADR-0003 | New nouns are new `fact-type.v2` citizens (and `parameter-declaration.v1` members), not a new schema family. Entity kinds remain identity-key strings, as `tax.us.interest-obligation` already is. |
| ADR-0006 / ADR-0071 Decision 3 | Eligible-student arithmetic is the adopted rule’s declared `value`, evaluated by the real evaluator. |
| ADR-0007 / ADR-0009 / ADR-0010 | If a binding path existed, per-statement results would be derived publications with truthful pins; enrollment correction follows identity. Categorical catalog findings have no production producer to displace. |
| ADR-0011 / ADR-0015 | Association is keyed at the existing 1098-E statement identity. Enrollment is keyed filer + academic period. |
| ADR-0016 | `f1098e.1` still authorizes only the raw box-1 subtotal. The eligible-student-supported subtotal is a different symbol. Collect-authority audit stays satisfied (the P2 computation-and-consumers record item 2.1). |
| ADR-0023 / ADR-0041 / ADR-0073 | Association and enrollment are `free` assertions. Retraction ends current support and names no opposite claim. |
| ADR-0024 / ADR-0025 / ADR-0064 | `choose`, `block`, `compare`, keyed numeric `parameter`, `categorical_compare` evaluate the (C) tree **once symbols are bound**. A categorical-returning parameter does **not** exist. |
| ADR-0036 / attachment-rule.v4 | Relabel and unchanged `collect_members` / raw tie-out. No new attachment schema. v6 `adjustment_rows` are not required. |
| ADR-0012 / ADR-0046 | Form-field successor of `form-field.v3`: explain strings and `blocked.codes` allowlist. Relabelled attachment heading is still a zero-authority projection of the part `label`. |
| ADR-0067 | Object-valued association and enrollment can be read by `ref` + `field` in the local env, the same canonical-object path. |
| ADR-0068 | Not used. R4 selected stable period `fact_id` following; the stale-named-period recast account is deleted. This is not an acquisition-report pairing. |
| ADR-0065 | Line 26 still refs line 21. A line-21 block still propagates; a published (C) zero still composes. |

### 5.2 What does not fit without a successor

Ordinary `attempt()` publishes one finding per rule id against
`_Run.env()`, whose `sources` are values without statement identity.
Per-item evaluation exists only as exact-rule intercepts:

- ADR-0071 pairing-scoped consequence dispatch:
  `PAIRING_SCOPED_CONSEQUENCE_RULE_IDS` (two rule ids).
- ADR-0074 `bound_sources` live binding: `BOUND_SOURCE_RULE_IDS`
  (`tax.us.2025.rule.interest.nominee-reduction` only);
  `MEMBER_NO_BINDING_PATH` otherwise.
- v9 `aggregation`: `tax.us.2025.rule.interest.derived-nominee-subtotal`
  v1 only; `NOMINEE_AGGREGATE_ID_INVALID` otherwise.
- v9 `selection`: line 2b v8 only; not used here.

A schema-valid copy of any of those shapes has no binding path. Python
that computed eligible-student status would fail P3. A values-only fold
would fail C6. Therefore the vertical cannot be admitted on committed
contracts alone.

`bound_sources` is additionally the wrong operator: one nonempty group of
values for one fact type. Pairing is the closest primitive and still only
binds two facts **and iterates the wrong subject** (association findings,
not the box-1 family). It is not the matching primitive for this
dependency set (§ 2a, the feasibility probe).

### 5.3 the feasibility probe outcome — owner decision, not a successor ADR yet

The probe at `docs/prototypes/sli-eligible-student/` ran the real
evaluator and `evaluate_pairing_scoped_rule`. Presentation is
`build_presentation_model` over synthetic publications and dispositions —
not `live_coordinate_run`, not a durable file, not citation-walk.
Attachment-inapplicable is a manually supplied row; P2 established the
committed requirement behavior separately. The probe does **not**
authorize a narrow successor ADR. A hand-built local env can evaluate a
**partial** mechanics witness; an ADR blessing that assembly would authorize a
coordinator the committed machinery does not provide, on evidence that does not
show the mechanism works. It would also be the fourth exact-rule exception —
after ADR-0071's two pairing rules and ADR-0074's one bound-sources rule — which
is the pattern the owner declined to extend.

**Smallest owner decision** (three clauses; (1) blocks production):

1. A reusable heterogeneous group-binding mechanism whose iteration
   subject is the **current box-1 family**, with exactly one usable
   association per member, local bindings, fail-closed missing/mismatch,
   and pin isolation — **or** a product cut that fits pairing's two
   facts **and** cannot silently omit an unassociated statement (no
   such cut is honest here).
2. Authoritative institutional determinations as current findings
   through a defined evidence/producer path, **or** an adopted
   categorical catalog/parameter in the rule grammar. Injected probe
   facts are not that path.
3. Live with the narrowed presentation promise (disposition +
   projected citation sites; mixed B-negative invisible in a synthetic
   projection; all-negative attachment inapplicable from a manually
   supplied row — P2 established the requirement separately), **or** a
   new explanation carrier.

A general grouped-rule contract is **not designed here**. If later named,
the reusable abstraction is an identified evaluation context: the subject
that drives iteration (current box-1 members), required related facts,
cardinality and completeness, local bindings, failure behavior, and pin
isolation — not merely "evaluate once per thing." v9 aggregation remains
nominee-locked and is not this decision.

The first design's "one additive ADR reusing pairing dispatch" is
withdrawn. Published schemas are not edited. The compressed witness is
not republished under a new label.

---

## 6. Rival comparison — not earned

A bounded rival comparison is warranted only if two materially different
representations remain plausible **and** a named consumer behaves
differently. Neither pair below meets both tests. Worksheet cap and MAGI
arithmetic are already established by committed tests (the P2 computation-and-consumers record item 1.3);
no rival is run for them.

**Per-statement mechanism.** Pairing-local evaluation and `bound_sources`
are not two plausible representations of this association.
`bound_sources` supplies a variable-length group of values for one fact
type. Pairing binds one left and one right and iterates association
findings. That is too few facts **and** the wrong iteration subject. the feasibility probe
showed association-driven dispatch silently omits an unassociated box-1.
No rival is earned; the bounded pairing-plus-v9 shape is **not** a match.

**Attachment surface.** Relabelling reported box 1 versus a second family
of eligible-student-supported amounts would look different to a reader.
No computational consumer of line 21 discriminates them. Relabel remains
the simpler heading repair when the attachment is required. It does not
discharge 2b. All-negative zero leaves the attachment absent.

The executable probe is `docs/prototypes/sli-eligible-student/`. Outcome:
needs-owner-decision.

---

## Checks run

- Git: branch `milestone/student-loan-interest-deduction-translation`,
  start SHA `81842bc5`; ratified line `origin/main` 0 behind, 54 ahead;
  no merged PR for this branch.
- Below-floor golden: heading `Line 21: Student Loan Interest Deduction`,
  `tieOutText` `Reported subtotal: 3000`, `line-sch1-21`
  `published_value` `2500`; blocked codes list omits every `SLI_*` code.
- `BOUND_SOURCE_RULE_IDS == {tax.us.2025.rule.interest.nominee-reduction}`.
- Pairing-scoped ids are the two ADR-0071 rules.
- `package_validation.py` contains `MEMBER_NO_BINDING_PATH`,
  `NOMINEE_AGGREGATE_ID_INVALID`, `RULE_SELECTION_UNAUTHORIZED`.
- `Environment.sources` is `dict[str, list[str]]`; `_Run.env()` passes
  `self.sources`; `collect_categorical_all_equal` reads that list.
- Attachment part `label` is the projector `heading`; `tieOutText` is
  `Reported subtotal: {value}` (`presentation_projection.py`).
- The P2 computation-and-consumers record § 2.4 six shapes; ADR-0074 Decision 1 and 2; v9 aggregation
  example `rule-artifact.v9.nominee-aggregate.json`.
- P1 the P1 loan-qualification record constituent 4; P2 the P2 source-and-entry record items 3, 4, 6; P2 the P2 computation-and-consumers record items 1–6.
- the feasibility probe evidence repair: `python3 docs/prototypes/sli-eligible-student/probes/feasibility.py`
  (exit 0). `evaluate_pairing_scoped_rule` with two box-1 SourceFacts and
  one pairing emits only A. Box-1 completeness is conceptual.
  `VALUE_EXPR` narrowed (no program classification). Pin isolation
  not-proven. Presentation projection over synthetic rows; attachment
  inapplicable is a manual disposition row (P2 established requirement
  behavior).
