<!-- foreman-context-v1
{
  "version": 1,
  "phase": "Tax Concept Derivation",
  "topic": "nominee-allocation-assertion-recording",
  "milestone_state": "closed",
  "status": "CLOSED 2026-09-08; owner-directed repairs 2026-09-08. Three tracks; Tracks 1 and 2 were each independently reviewed READY, and Track 0 was closed by the Foreman on executed evidence rather than by an independent reviewer. The application records, corrects, retracts from current use, and asserts again the ordinary statement that a stated amount of interest reported on an identified Form 1099-INT is allocated to a named other person, and recovers current and historical retracted assertions — what was said, who said it, and who later ended current support — with attribution from a committed act log alone. Delivered: tax.us.nominee-allocation.amount (bundle.v2/fact-type.v2, keyed payer+statement+tax-year+recipient sharing the committed box-1 identity components, exclusiveMinimum 0, free supersession, no admission invariant over the amount); the tax.us.interest-allocation-recipient entity kind with an application-minted opaque workspace id and the typed name as a non-authoritative label; a persisting producer; a separate bounded retraction operation on act-finding-retracted.v1; and a recovery view that consults compute_currency as the sole definition of current standing. An allocation assertion requires current ordinary-language-entry evidence whose submitted answers correspond to the mapped finding; production does not invent a synthetic flag. The workspace model is SHARED: one current answer per report and recipient, any recorded actor may correct or retract it, actor is opaque provenance and never admission-validated, and no durable text claims the original actor recanted. Hard gate: no user-facing production caller may rely on assert_nominee_allocation until resumable or idempotent recovery of a persisted multi-act prefix is closed. No nominee tax consequence, line-2b change, Schedule B row, information-reporting implementation, migration, or UI. T0-F5 remains deferred behind its hard production gate.",
  "scope": [
    "establish the smallest canonical proposition for one user's ordinary statement that a stated amount from one identified Form 1099-INT report belongs to one named other non-spouse person, without recording a user-supplied tax classification",
    "select and instantiate a concrete identity and association shape that preserves the closed milestone's report-scoped and independently-correctable-per-recipient behavior",
    "use the real workspace act and projection path to record, correct, retract from current use, assert again, and recover attribution for the assertion",
    "provide a bounded ordinary-answer producer or equivalent engine-level entry surface using synthetic cases, while keeping circumstance routing explicit",
    "establish executable positive, negative, lifecycle, cardinality, and compatibility evidence before calling the recording seam complete"
  ],
  "non_goals": [
    "no nominee-distribution tax classification, derived reduction, line-2b producer, Schedule B row, or information-return filing implementation",
    "no repair of T0-F5 in this milestone; the hard gate remains on the later affected integration",
    "no user-facing tax-label question and no durable negative answer when the user says no or supplies no allocation",
    "no general beneficial-ownership or allocation ontology, spouse model, trust/custodian model, contested-ownership process, or UI",
    "no silent reinterpretation, replacement, or migration of the legacy nominee-adjustment fact",
    "no new generic act kind, kernel primitive, or closure semantics unless evidence shows the existing assertion and lifecycle machinery cannot carry a required case and the resulting contract decision is reviewed"
  ],
  "deep_reads": {
    "implementation": [
      "OWNER_MODEL.md#The Product Model",
      "OWNER_MODEL.md#The Domain Model Model",
      "docs/milestone-retrospectives/2026-09-05-nominee-interest-ownership-translation.md#What transferred, and what did not",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#The abstract product question",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Fixed product cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-interest-ownership-translation.md#Track 0 adversarial closure",
      "docs/adr/0009-derived-finding-shape.md",
      "docs/adr/0010-derived-finding-projection-and-currency.md",
      "docs/adr/0067-canonical-acquisition-field-ref-access.md",
      "docs/adr/0068-acquisition-report-identity-association.md",
      "packages/schemas/kernel/act-assertion.v2.schema.json",
      "packages/schemas/kernel/finding.v2.schema.json",
      "packages/kernel/findings.py",
      "packages/tax/obligation_acquisition_mapping.py",
      "packages/tax/report_statement_identity.py",
      "PROJECT_PLANNING.md#Lean Production Loop",
      "PROJECT_PLANNING.md#Track 0 Adversarial Closure Gate",
      "PROJECT_PLANNING.md#Payload Instantiation Gate",
      "AGENTS.md#Data Safety Rules"
    ],
    "review": [
      "OWNER_MODEL.md#The Product Model",
      "docs/milestone-retrospectives/2026-09-05-nominee-interest-ownership-translation.md#Follow-ups",
      "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md#Fixed cases",
      "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md#Contract decisions still to make",
      "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md#Success and stop conditions",
      "docs/phases/tax-concept-derivation/milestones/nominee-allocation-assertion-recording.md#Exit criteria",
      "docs/roles/qualitative-review.md",
      "AGENTS.md#Data Safety Rules"
    ]
  },
  "retrospective": "docs/milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md"
}
-->

# Nominee Allocation Assertion Recording

## Milestone identity

- Phase: Tax Concept Derivation
- Milestone key: `nominee-allocation-assertion-recording`
- Delivered on branch `milestone/nominee-allocation-assertion-recording`,
  merged and deleted at closure; the ratified line carries the result
- State: **CLOSED 2026-09-08**; all three tracks complete. Tracks 1 and 2 were
  each independently reviewed READY; Track 0 was closed by the Foreman on
  executed evidence rather than by an independent reviewer
- Roadmap role: first production stage after the nominee-interest paper contract

## Plain-language purpose

A Form 1099-INT can report interest in the taxpayer's name even though the
taxpayer says that part of the amount belongs to another person. The application
must preserve two different statements:

1. the payer reported the full amount; and
2. a named user said that a stated part of that identified report belongs to a
   named other person.

The second statement is the user's ordinary-life assertion. It is **not** a
user declaration that “nominee interest” exists, is not a Schedule B
classification, and is not by itself a normalized information-reporting
conclusion. Later tax rules may use it as bounded evidence for those purposes.

This milestone makes only that ordinary assertion real: the application can
accept it through an engine-level entry surface, record who asserted it and
when, project it as current workspace state, correct one recipient's allocation
without rewriting another's, and remove an identified assertion from current
use without asserting the opposite.

Removal here is **workspace-support retraction**: a recorded actor ends the
current support of an identified assertion. The original assertion, its actor,
and its time stay in history, and the retraction carries its own actor and time.
It does not establish that the person who first asserted it has recanted.

## Why this is next

The preceding milestone settled the semantic boundary at the paper rung but
deliberately built nothing. Attempting the complete nominee-interest vertical
now would combine at least four independently testable concerns:

- recording the user's ordinary statement;
- deriving and supporting the nominee reduction;
- reconciling the new result with the legacy adjustment path; and
- presenting line 2b, Schedule B, attribution, and reporting guidance.

This milestone takes the first concern alone. It supplies a real input and
lifecycle boundary that the later tax-rule milestone can consume. A failure can
therefore be attributed to the assertion model rather than hidden inside tax
arithmetic or presentation.

## Current state

The repository already has generic assertion acts, immutable findings,
same-fact correction, entity introduction, and an ordinary-answer mapping
precedent for obligation acquisitions. It also has documentary Form 1099-INT
report facts and statement-instance identity.

It does **not** have a selected canonical nominee-allocation fact, a selected
report-association shape for that fact, an ordinary-language nominee-allocation
producer, or a demonstrated retraction lifecycle for this proposition. The
legacy `tax.us.2025.scheduleb.adjustment.nominee.amount` records a preclassified
tax adjustment and lacks the owner, report association, ordinary proposition,
and attribution required here. It cannot be reinterpreted.

## Scope

The milestone will:

- define one canonical proposition — stated without its speaker — for one
  named allocation recipient and one stated amount;
- preserve the identified payer report independently;
- choose a concrete report-association and identity shape that satisfies the
  already-selected product properties;
- record the assertion through the real act log and kernel projection;
- preserve the asserting actor, time, and commitment revision on the act;
- support same-proposition correction and retraction from current use without manufacturing a
  negative ownership fact;
- keep several owners independently correctable;
- provide a bounded engine-level ordinary-answer producer or mapping surface;
- route accrued-interest and erroneous-form answers away rather than capturing
  them as nominee allocations; and
- prove the behavior with synthetic instances and real-boundary tests.

## Non-goals

- No derived nominee reduction or taxpayer share.
- No new producer for `tax.us.2025.interest.scheduleb-nominee-subtotal` or
  `tax.us.2025.interest.taxable-total`.
- No line-2b, Schedule B, attachment, or information-return implementation.
- No T0-F5 repair.
- No reader-facing UI or final explanation projection.
- No durable “no,” “not mine,” or completeness declaration when the question is
  unanswered or answered negatively.
- No general ownership ontology or legal beneficial-ownership determination.
- No silent conversion, retirement, or migration of the legacy nominee amount.
- No assertion that a user statement proves who owns the interest in the world.

## Contract decisions still to make

These are real contract decisions, but the owner need not choose among
implementation-equivalent shapes. The Foreman should resolve them from the
fixed cases and committed machinery, returning only a choice that changes
product behavior or materially expands scope.

1. **Canonical proposition.** The fact's question is defined **without its
   speaker**: *the amount of interest reported on this identified Form 1099-INT
   that is allocated to this named other person.* The finding supplies the
   current answer with `basis: "attested"`; the enclosing assertion act supplies
   who stated it and when; a later tax rule — not this fact — decides the
   nominee-interest consequence. Embedding the asserter in the proposition
   ("the amount the user says belongs to…") is **forbidden**: it collapses the
   separation of proposition from authorship the predecessor milestone
   requires.
2. **Identity and cardinality.** Identity keys are **payer + statement +
   tax-year + recipient**, where payer and statement are derived by the
   committed document-side conventions in
   `packages/tax/report_statement_identity.py`, so the allocation shares the
   box-1 report's own identity components. `tax-year` is a **literal** key,
   matching the committed `f1099int` bundle; a `scalar` key is refused by
   `fact-type.v1`. Correction operates strictly per `fact_id`, so A4's
   record-identity invariant holds provided the **recipient** is a distinct
   component of the id.

3. **Report association — direct shared identity (R-A), bounded.** The
   allocation is keyed on the report's own identity components rather than
   carrying a separate association citizen. Executed: two statements from one
   payer stay distinct; the same statement reference in two tax years cannot
   collide; correcting the box-1 amount does not detach the allocation; and the
   allocation joins the exact current box-1 finding a later rule would consume.

   **This is a direct shared identity, not a derived association.** ADR-0068's
   "derived and re-evaluated" property does **not** apply here and is not
   claimed; its Decision 9 (tax arithmetic stays out) does apply and is kept.

   **R-A is selected for this report-specific production slice only. It does
   not refute or permanently reject R-B.** *R-B remains deferred*, with a named
   trigger: an allocation known independently of a particular report, or one
   that must survive report-identity replacement.

4. **Act and basis.** Whether existing assertion/finding contracts carry the
   user act without a new act kind, and which declared basis accurately records
   the support. The actor must come from the caller; it must not be manufactured
   by a mapper or inferred from the proposition. **P2:** no invariant collision
   at the payload layer. `basis: "attested"` with `nature: "determinable"` is
   the committed precedent for exactly this shape of statement —
   `packages/tax/obligation_acquisition_mapping.py:599-601` records it as
   "what the person stated about their own circumstance, not what a document
   reported," which is the ordinary/tax separation this milestone needs. A
   complete honest instance was written; no new act kind is indicated.
5. **Lifecycle.** How correction and retraction work without changing another
   recipient's current allocation and without writing zero or false as “belongs to
   the taxpayer.” Retraction removes an identified assertion from current use;
   it is never disguised as a correction, and it never claims the original
   author recanted.
   **SETTLED by the rebuild onto ADR-0073.** This milestone now sits on the
   Assertion Standing and Retraction Semantics contract, which supplies the
   mechanism directly: `act-finding-retracted.v1` ends the current support of
   one identified finding, supplies no replacement value, and asserts no
   opposite claim. Its payload is exactly `{"finding_id": ...}`, closed.

   The earlier candidates -- an individuated allocation entity ended by
   `act-entity-superseded.v1`, and an adopted source family using
   `act-member-transition.v3` -- were compared on executed evidence at T0-A and
   are both superseded. Both removed the **fact**, so the proposition ceased to
   exist and its identity had to be abandoned to answer again. Retraction ends
   a **finding** and leaves the fact standing, which is what A11 requires.
6. **Attribution recovery.** Which record-level join recovers actor, time, and
   assertion identity from a current fact. Reader-facing display remains later,
   but the information must survive this milestone.
7. **Packaging boundary.** Which bundle, entity kinds, mappings, and package
   adoption are needed for this recording capability without admitting a tax
   consequence that has not been built.

   **Recipient identity: an application-minted opaque workspace id** (owner
   decision 2026-09-07). No committed natural-person or allocation-recipient
   entity kind exists, and the committed institution convention derives identity
   from trimmed display text, which would not preserve identity across a name
   correction. The recipient id is minted and retained by the invoking boundary
   under a bounded role-specific entity kind; the typed name is a
   non-authoritative display label. The id means only "this recipient record in
   this workspace" — no verified personal or legal identity, no authorization,
   no cross-workspace correspondence, and two recipients may share a display
   name. **Display-name correction is deferred**, because `entity.v1` labels are
   immutable; the reopening trigger is a concrete need to edit a recipient label
   without displacing recipient-linked facts.

   **Simplified by the rebuild onto ADR-0073.** The earlier owner decision
   stands -- retraction and later assertion are required -- and the family route
   that made this expensive is gone. Retraction is a kernel act; it needs no
   `source-family.v2` adoption, so this milestone takes on neither
   `closure_claim` nor `authorizes_subtotal`, and no horizon genesis or
   succession. A recording-only milestone therefore claims no tax-consequence
   authority, which was the objection that disqualified the family route.

   Two constraints inherited from ADR-0073 are now packaging decisions here:

   - the allocation fact type's supersession policy is **`free`**, retained by
     owner decision. ADR-0073 Decision 3 refuses retraction under `locked`
     unconditionally, so `locked` would make A6 impossible;
   - this recording-only milestone introduces **no cross-fact admission
     invariant** that would reject or clamp an allocation against the report
     amount, or prevent retraction once an allocation becomes absent. A8 records
     the assertion faithfully; **later tax-supportability work owns the
     over-allocation consequence.** Decision 8's sixth refusal re-runs the
     declared admission enforcers over the prospective post-retraction state, so
     an invariant declared here would fence this fact's own retraction.

     **This is a scoping decision for this milestone, not a general rule.** It
     is not a claim that retractable facts can never participate in invariants,
     and it must not be restated as one.

Any published schema must be instantiated with a complete hand-written
synthetic payload before publication. Prefer existing generic schemas when they
express the selected proposition honestly; do not create a new generic citizen
merely to make the domain content look symmetrical.

## Fixed cases

All identifiers and values are synthetic.

| Case | Input or transition | Required observation |
| --- | --- | --- |
| A0 — unanswered | Report exists; no allocation response | No allocation assertion or negative fact is written |
| A1 — explicit no | User answers no during the interaction | No negative, denial, or "belongs to the taxpayer" fact is written. Durable workspace state is indistinguishable from A0. Any acknowledgement is transient to the interaction and leaves no durable claim |
| A2 — one owner | User says `$450` of report A belongs to `demo.owner.pat` | One current ordinary allocation statement, attributed to the caller and associated only with report A |
| A3 — several recipients | `$300` allocated to Pat and `$150` to `demo-recipient-kim` on the same report | Two distinguishable current allocations at distinct fact identities; no combined proposition that erases per-recipient identity |
| A4 — correct one recipient | A workspace actor changes the amount allocated to Pat from `$300` to `$250`; the allocation to Kim remains `$150` | The prior allocation to Pat is non-current. The current allocation to Kim is the **same record**, not an equal one: its finding identity and revision are unchanged, it is still supported by **the same original assertion act and actor**, and **no new act is written for Kim's allocation**. Equal values on a re-created record is a FAIL, because it would record an assertion no actor made |
| A5 — same payer, two reports | Report A and report B share a payer; allocation concerns A | The assertion cannot attach to, reduce, or be mistaken for report B |
| A6 — retract from current use | Alex removes from current use the allocation to Pat that Matt previously supplied | The current allocation to Pat disappears. Matt's assertion remains historical; Alex's retraction is separately recorded with its own actor and time; no replacement value and no opposite ownership proposition is created. **Nothing says Matt recanted.** Admission never consults actor identity, so this records provenance, not permission |
| A7 — report amount correction | Report A changes amount without changing statement identity | The allocation remains the same ordinary statement; no supportability or tax result is manufactured here |
| A8 — over-allocation statement | Recorded allocations exceed the report amount | Preserve what was asserted; do not silently clamp or choose an owner. Tax supportability is a later consumer |
| A9 — accrued-interest route | User describes buying a bond between interest dates and reimbursing the seller | Route to the existing accrued-interest path; write no nominee-allocation assertion |
| A10 — erroneous report route | User says the payer's reported amount is wrong | Route to document correction; write no nominee-allocation assertion |
| A11 — assert again after retraction | After A6, a recorded actor asserts `$250` allocated to Pat on the same report again | A current Pat allocation exists again at the **same** `(report, owner)` fact identity, supported by a **new** assertion act attributed to its own caller. Retraction is a lifecycle state, not a terminal one: the `(report, owner)` proposition must not be exhausted, and the retracted assertion must not be revived in place. The retraction and the later assertion are both recoverable, in order, with their actors distinct in the record |

**A6 and A11 are settled on the retraction contract.** They were a material
discriminator, and they discriminated: they eliminated both original candidates.
Executed under `probes/candidate-4-retraction.py`, the allocation statement
records, corrects, retracts, and **re-asserts at the same `(report, owner)` fact
id**, with owners uncoupled and history retained. Revival by re-using a
retracted finding's id remains refused.

The identity and association alternatives that A6/A11 reopened are therefore
closed by the same evidence: the fact is keyed directly on `(report, owner)`,
with no allocation-entity indirection and no source family, because retraction
does not require either.

## Success and stop conditions

The milestone succeeds when the ordinary allocation assertion is a real,
attributed, correctable, retractable workspace record and nothing more has been
built. Succeeding at a smaller honest scope is preferred to satisfying every
criterion by weakening one.

A **stop** is not a failure and not a defect to work around. It is a boundary
reached, recorded at the exact point of contact, and surfaced to the owner as a
consequential decision with the options and their product consequences. The
Foreman does not resolve one by relaxing a criterion, renaming the operation, or
choosing a representation that reads as honest only under a favorable
interpretation.

Stop and surface, rather than proceeding, when:

1. **Retraction cannot be represented honestly.** If removing an identified
   assertion from current use
   requires writing zero, `false`, an opposite ownership claim, or any fact
   asserting that the amount belongs to the taxpayer, stop at that exact
   boundary. Disguising retraction as a correction to zero is the specific
   failure this condition exists to prevent. Deleting or rewriting the
   assertion's history to make the statement disappear is not an honest
   retraction either: it satisfies "removes current support" by destroying the
   authorship the milestone exists to preserve. This may block exit criterion 5,
   which is then reported unmet with the boundary named — never satisfied by
   redefining what retraction means.
2. **The proposition cannot be recorded without a tax classification.** If no
   honest instance of the canonical fact can be written without asserting a
   nominee-interest characterization, Schedule B consequence, or normalized
   information-reporting conclusion, the boundary is a contract decision.
3. **Existing assertion, finding, or lifecycle machinery cannot carry a fixed
   case.** A new generic act kind, kernel primitive, or closure semantic is out
   of scope by default; needing one is a surfaced decision, not an
   implementation detail. Evidence must show the existing machinery fails the
   case, not merely that it is inconvenient.
4. **Honest recording appears to require touching the legacy nominee
   adjustment.** Reinterpretation, conversion, retirement, or migration of
   `tax.us.2025.scheduleb.adjustment.nominee.amount` is forbidden here; pressure
   toward it is a signal the proposition or association shape is wrong.
5. **A payload cannot be instantiated.** Under the Payload Instantiation Gate,
   an instance that cannot be written without lying or without improvising
   reserved doctrine is a planning-time signal requiring its own decision before
   code depends on the contract.

## Planning review cycle

Planning is built and reviewed before a charter is filed:

1. **P1 — proposition and lifecycle outline.** Confirm the plain-language box,
   decision inventory, fixed cases, and stop conditions. Review specifically for
   tax-label leakage, hidden negative claims, coupled owner correction, and
   accidental legacy reinterpretation.
2. **P2 — artifact and build-readiness map.** Read the actual assertion,
   finding, entity, projection, mapping, package, and retraction consumers.
   Record the exact fields relied upon, sibling fields not relied upon, and
   downstream consumers. Produce at least one fully resolved candidate payload
   for every proposed published shape. Review the evidence map and track
   decomposition before Track 0 or implementation begins.

Repairs are folded into the plan section they correct. A review finding is
triaged before another iteration opens. No review round exists merely to polish
prose already supported by the same evidence.

**Open questions carried into Track 0.** Both gates are closed. Three questions
survive them and are Track 0's to settle before any implementation charter:

1. **Track 2's production/coordinator boundary.** Raised by P1, unresolved by
   P2, which found no distinct coordinator module beyond the contribution-batch
   admission boundary the obligation-acquisition precedent already uses. Track 0
   must either bind Track 2 to that boundary or record that no separate one
   exists — in which case Track 2 is a contract decision, not an integration
   task.
2. **A10's routing owner.** No module was located that owns document/erroneous-
   report routing. If none exists, A10 is a boundary the milestone asserts but
   cannot demonstrate, and its scope must be stated honestly rather than assumed.
3. **ADR-0067 and ADR-0068 were not read during P2.** The identity and
   report-association claims in decisions 2 and 3 rest on code reading alone.
   Track 0 must check them against those ADRs directly before selecting a shape.

**Owner decision 2026-09-07 — the selected operation is workspace-support
retraction.** This resolves what was briefly carried as a blocker; it is
recorded here so no later section reopens it.

One recorded actor originally supplied an allocation assertion. A later
recorded actor may end that assertion's current support. The original
assertion, its actor, and its time remain historical; the retraction act, its
actor, and its time are separately recoverable; no replacement value and no
opposite ownership proposition is created.

The operation **does not** establish that the original author personally
recanted or no longer believes the assertion. Durable product language must not
say the original author withdrew their statement unless a future trusted
identity boundary establishes that the asserting and retracting persons are the
same. ADR-0073's limit is preserved exactly: **actor identity is not
admission-validated**, and this milestone does not claim otherwise.

**No trusted original-author identity system is introduced or required here.**
Author-bound personal recantation and permission rules are **deferred**, not
open work. *Reopening trigger:* a concrete product case — collaboration, audit,
delegation, or similar — that requires the product to prove who may remove whose
assertion, or to claim personal recantation. No authentication, role, identity
verification, or authorization machinery is designed in this milestone.

A same-actor synthetic case may be tested. It must not be presented as evidence
that same-author retraction is enforced, because it is not.

## Track structure

The Foreman may refine these boundaries during P1/P2, but may not collapse them
into one unreviewed build.

### Track 0 — contract instantiation

Select the smallest conforming fact, identity, association, lifecycle, and
packaging contract. Demonstrate its complete synthetic payloads and the
authority-lifecycle/late-correction cases before publishing a schema or ADR.

**Lifecycle mechanism selection is settled.** T0-A compared the individuated
entity and source-family routes on executed evidence and disqualified both; the
rebuild onto ADR-0073 supplied `act-finding-retracted.v1`, which satisfies
A2-A6 and A11 at a stable `(report, owner)` fact identity. Track 0's remaining
work is contract selection, payload instantiation, and adversarial closure --
not mechanism comparison. Do not re-run the candidate comparison.

Return to the owner only if the surviving alternatives carry materially
different product meanings, or if one requires a genuinely broader substrate
contract.

Track 0 receives an independent review before implementation.

### Track 1 — allocation producer and record lifecycle

**COMPLETE**, independently reviewed READY.

Implement the allocation fact type as committed content in the product
namespace, and an ordinary-answer producer that admits it through the real
contribution boundary. Exercise the real act-log and projection path for
A0–A11, including independent per-recipient correction, cross-actor correction
and retraction, and assert-again at the same fact identity. Publish no rule, no
derived symbol, and no nominee tax consequence.

### Track 2 — recovery, read integration, and legacy coexistence

**COMPLETE**, independently reviewed READY.

**Track 1 now owns the production acceptance boundary.** Its named helpers
persist assertion, correction, and retraction through `ActLog`, so Track 2 does
**not** build that boundary again.

Track 2 is responsible for what remains:

- **recovery and read integration** — rebuilding workspace state from the
  committed log and exposing the current allocations and their recoverable
  attribution to a real reader path;
- **legacy coexistence** — showing the new allocation neither rewrites nor
  silently converts `tax.us.2025.scheduleb.adjustment.nominee.amount`;
- **any genuinely remaining coordinator work** the Track 1 helpers do not
  already cover, named explicitly rather than assumed.

Track 2 receives an independent review of the complete recording capability. It
publishes no nominee tax consequence.

## Contracts and boundaries

- The payer report remains documentary evidence of what the payer reported.
- An allocation assertion requires a current `ordinary-language-entry`
  evidence citizen whose submitted answers correspond to the answers being
  mapped on the fields that determine the finding. Missing, malformed,
  document-report, and unrelated modes are refused. The evidence retains the
  submitted representation; the finding is the canonical proposition derived
  from it. Production contribution construction does not invent whether the
  underlying interaction was synthetic.
- The user is author of the ordinary assertion only; the application will be
  author of the later tax classification through an adopted rule.
- “No current allocation assertion” is absence of support, not a user denial and
  not a claim that the taxpayer owns the full amount.
- The legacy nominee amount is immutable published history and is not evidence
  for the new ordinary proposition.
- Standing workspace authorization is unaffected; this is not a completeness
  or per-family confirmation mechanism.
- No source-family closure is introduced merely to make a zero computable.
- T0-F5 remains a hard gate on the later Schedule B integration, not on this
  recording-only milestone.

## Verification

The plan review must name exact focused commands after P2 identifies the
selected modules. At minimum, the final build must provide:

- schema-registry and payload validation for every new published artifact;
- for exit criterion 1, a committed positive payload instance of the canonical
  fact from which the ordinary proposition is readable, plus a structural check
  over the published fact shape showing it carries **no** field expressing a
  nominee-interest characterization, Schedule B classification, or reporting
  conclusion — prose stating the distinction does not discharge this;
- positive, negative, correction, retraction, assert-again, multi-owner,
  same-payer/two-report, wrong-route, and legacy-coexistence tests from A0–A11,
  with the A4 and A11 tests asserting record identity and act provenance rather
  than value equality alone;
- at least one real act-log-to-current-projection integration test;
- a provenance assertion joining the current finding to its assertion act's
  actor and time;
- a structural check over the adopted package's rules — reading each rule's
  declared published symbol, not searching document text — proving that no new
  rule publishes `tax.us.2025.interest.scheduleb-nominee-subtotal` or
  `tax.us.2025.interest.taxable-total`;
- `pytest -m "not live"` unless substrate changes require the full suite;
- repository mypy for typed Python changes;
- `git diff --check`, governance lint, and the envelope scan; and
- full CI as the merge gate.

## Data safety

Only synthetic `demo.*` / `demo-*` people, reports, acts, and amounts may enter
committed fixtures. No real tax document, taxpayer fact, private output,
credential, refusal reason, or absolute workstation path may be committed.

## Exit criteria

The milestone is complete only when:

1. the exact ordinary proposition and its distinction from a nominee tax
   classification are recoverable from committed artifacts;
2. one and several-owner assertions enter through the real selected input and
   act boundary;
3. the current workspace projection preserves report association, per-recipient
   identity, and attribution;
4. correcting the allocation to one recipient leaves another recipient's
   current allocation unchanged **as a record** — same finding identity and
   revision, still supported by the same original assertion act and actor, and
   no act written for that other allocation — not merely equal in value;
5. retraction removes an identified assertion from current use without
   asserting the opposite, without creating a replacement value, without
   destroying history, and without exhausting the `(report, owner)` pair — the
   proposition can be asserted again afterwards, and the assertion actor and the
   retraction actor remain separately recoverable;
6. unanswered and explicit-negative interactions leave no durable allocation
   claim;
7. accrued-interest and erroneous-report routes create no nominee assertion;
8. the legacy nominee adjustment remains unchanged and unconverted;
9. no nominee tax consequence, line-2b change, or Schedule B claim has been
   smuggled into the recording layer; and
10. the final curated candidate passes its independent review and CI.

A criterion blocked by a recorded stop condition is reported **unmet, with the
boundary named**. It is never marked satisfied by redefining the operation it
describes, and the milestone does not close as complete while a stop remains
undisposed by the owner.

## Track 0 adversarial closure

**COMPLETE.** Evidence:
`docs/prototypes/nominee-allocation-assertion-recording/track-0-findings.md`
and the executed probes beside it. Artifacts 1–5 PASS; artifact 6 is `N-A`.

### 1. Authority-lifecycle table — PASS

| Fact or claim | Meaning | Authority scope | Depends on | What invalidates it? |
| --- | --- | --- | --- | --- |
| `…nominee-allocation.amount\|payer,statement,tax-year,recipient` | The amount of interest reported on this identified Form 1099-INT that is allocated to this named other person — **the question, without its speaker** | One `(payer, statement, tax-year, recipient)` tuple; **not** the payer alone, **not** the report's total | The committed payer and statement entity identities; the tax year. **Authorship is on the enclosing act, not the fact** | Correction (a later finding for the same fact, by any actor); retraction of the current finding; supersession of an identity entity |
| The current standing of that fact | Whether some finding answering it is presently in force | The workspace | `compute_currency` displacement closure only | Any of the five displacement roots |
| "No current allocation is recorded" | Absence of support | The workspace, at a moment | Nothing — it is a negative observation, not a declaration | A later assertion |

Storage identity is not authority scope, and the third row is the one that
matters: **absence here is an observation, never a closure claim.** The
milestone declares no completeness authority, so it can say no allocation is
recorded and may never say none exists.

### 2. Empty/nonempty authority matrix — PASS

This milestone **declares no source family**, so no family emptiness can affect
it or a neighbor. The matrix is exercised over the fact type's own membership,
which is the analogous authority, and the first row is deliberately
unreachable:

| Family state | Universe / absence authority | Eligibility | Expected feature result | Expected neighboring result |
| --- | --- | --- | --- | --- |
| Closed empty | Complete authority establishes no allocations exist | — | **Unreachable by construction.** No closure claim is declared, so this state cannot arise | Unchanged; no neighbor may read a closure that is not asserted |
| Empty, no closure authority | None declared, by design | Any | No current allocation is recorded. **Not** blocked, and **not** a denial (A0, A1) | Unchanged. The taxpayer's reported amount continues unreduced because nothing reduced it, not because ownership was established |
| Nonempty, eligible | Assertion act admitted | Positive | The allocation is current at its `(report, owner)` identity (A2, A3) | Unchanged — no consequence is published by this milestone |
| Nonempty, ineligible | Assertion refused at admission | Negative | No finding exists; the refusal is the result. **Explicitly chosen:** refuse, never a silent zero | Unchanged |

The second row is the substantive one: an empty workspace and a retracted
allocation are the same state to every reader, and neither may be presented as
a claim about ownership.

### 3. Late-authority counterexample — PASS

`attest → close → compute → add member → reclose → recompute` does not apply
literally, because nothing here is closed or aggregated. The analogous
trace is the lifecycle itself, and it was **executed**:

`assert → correct → retract → assert again`

At each transition: correction displaces the prior finding, which stops being
current and stays in history; retraction ends the current support of the named
finding and publishes no value; the later assertion becomes current **at the
same fact id**. Nothing is left current after the authority it summarised
changed, because **no aggregate or summary claim is published at all** — the
milestone publishes no subtotal, no total, and no derived result. There is
nothing that could survive stale.

### 4. Claim-reuse proof — PASS (corrected)

**An earlier version of this artifact was false and is withdrawn.** It claimed
the payer report fact "is read as the report identity." At that time the probe
read no report fact at all — it minted an unrelated `demo.report-1099int`
entity. The claim was not supported by the evidence cited for it.

**Corrected and executed.** The probe now adopts the committed
`packages/content/tax/2025/f1099int.bundle.json`, performs horizon genesis for
`tax.us.2025.f1099int.b1`, and admits the documentary box-1 report through
`contribute_1099int_report` → `apply_contribution_batch`. The allocation
**shares that report's own identity components** — payer entity, statement
entity, tax year — derived by the committed document-side conventions.

That shared identity is not a reuse of the box-1 *claim*: the allocation asserts
a different proposition (how much of the reported interest is allocated to a
named other person) at a different identity (adding `recipient`), on different
authority (an actor's attested answer, not the payer's documentary report). It
does not restate, redefine, or broaden the box-1 declaration, and correcting
box-1 leaves the allocation attached and current.

The legacy `tax.us.2025.scheduleb.adjustment.nominee.amount` is **not** reused
and is untouched: different proposition, different lifecycle, different declared
authority.

### 5. Neighboring-capability dependency diff — PASS

| Neighbor | Prerequisites before | After | New feature-specific prerequisite? |
| --- | --- | --- | --- |
| Taxable-interest total / line 2b | Reported box-1 findings | Unchanged | **None** |
| Schedule B attachment | Unchanged | Unchanged | **None** |
| Accrued-interest path | Unchanged | Unchanged | **None** |
| Legacy nominee adjustment | Unchanged | Unchanged | **None** |
| Migration path | Reads `compute_currency` | Unchanged | **None** |

Including the state in which this feature has no activity: with no allocation
recorded, every neighbour behaves exactly as before, because this milestone
publishes no symbol any neighbour binds. No blast-radius review is triggered.

### 6. Integration-surface artifact — `N-A`

This milestone plans **no producer and no successor producer of an externally
bound symbol.** It publishes no rule and no derived symbol; a structural check
over the adopted package's rules' declared published symbols is named in
`## Verification` and must confirm this at build time.

### Known limitations affecting correctness

**Hard gate — interrupted multi-act write is not resumable.**
`assert_nominee_allocation` pre-applies semantically, then appends entity,
contribution, and assertion as three `ActLog.append` calls. There is no atomic
multi-act append, no transaction substrate, and no rollback. An interruption
can persist a prefix. Repeating the same call is not idempotent: an existing
recipient entity, or an already-recorded contribution, can make the retry
fail. **No user-facing production caller may rely on this operation until
resumable or idempotent recovery of that prefix is closed.** Semantic
pre-application is not atomicity.

Two items are recorded that are **not** correctness limitations, stated rather
than disposed:

- **A10 cannot be demonstrated as routing.** No module owning
  document-correction or erroneous-report routing exists anywhere in
  `packages/`. A10's requirement is narrowed to the negative this milestone can
  show — that no allocation is recorded for such an answer. Where such an answer
  *should* go is not established here and must not be claimed.
- **The workspace model is shared, not author-indexed.** A product needing
  several users' independent assertions to coexist would require an
  author-indexed proposition with conflict and reconciliation behaviour.
  Deferred, with a concrete collaborative use case as the trigger.

### Closure record

Two artifacts of an earlier version of this section were **wrong and are
corrected above**: the claim-reuse proof asserted a report-fact reuse that had
not happened, and the Payload Instantiation Gate was reported discharged on
instances that used an invented report entity rather than the selected
production shape. Both are re-executed against the committed identity model, and
the instances are regenerated. The gate is discharged now, not then.

Track 0 closes on the conditions set for it: proposition and attribution are
separated; shared-workspace multi-actor semantics are explicit; report identity
is grounded in committed machinery; and A4, A5, A6, A7, and A11 are demonstrated
against that identity.

## Relationship to the following stages

This milestone records the ordinary assertion. It does not finish nominee
interest. Later milestones should proceed in this order:

1. **Tax consequence and supportability:** adopted rule(s) derive the supported
   nominee reduction from the recorded assertions, independently of any
   payment/credit fact, and separately evaluate authority-indexed reporting
   guidance.
2. **Legacy and return integration:** select the coexistence or migration path,
   connect one canonical reduction to line 2b and Schedule B, and execute the
   real consumer surfaces.
3. **Explanation and interaction projection:** expose who supported the ordinary
   assertion, what the rule concluded, what remains unresolved, and which
   authority supports each statement.

T0-F5 must be repaired no later than stage 2, before the affected Schedule B
integration can be accepted as complete. It need not be repaired to record the
ordinary assertion in this milestone.

## Execution record

Closed 2026-09-08. Retrospective:
[`2026-09-08-nominee-allocation-assertion-recording.md`](../../../milestone-retrospectives/2026-09-08-nominee-allocation-assertion-recording.md).

| Unit | Result |
| --- | --- |
| Gate P1 — framing | Closed. 3 blocking findings absorbed: A4/exit-4 tested value equality where record invariance was meant; no case exercised assert-again after retraction (A11 added); exit criterion 1 had no verification anchor |
| Gate P2 — artifacts | Closed. Machinery mapped; the payload instantiates honestly with `basis: "attested"` |
| Rebuild onto ADR-0073 | The milestone was rebased onto the closed Assertion Standing and Retraction Semantics milestone. A11 then succeeded at the same fact identity, and the family/horizon packaging cost disappeared |
| Track 0 — contract | Closed. Entity and source-family candidates disqualified on executed evidence; retraction selected; report identity grounded in `report_statement_identity.py`; six adversarial-closure artifacts, 1–5 PASS and 6 `N-A` |
| Track 1 — producer and lifecycle | Complete, independently reviewed **READY**. Content, producer, retraction operation, and A0–A11 evidence |
| Track 2 — recovery and coexistence | Complete, independently reviewed **READY**. Log-only recovery, attribution, report-join cardinality, legacy coexistence through committed marshalling and rule execution, named-surface neighbour checks; no coordinator work remained |
| Owner-directed repair 2026-09-08 | Four corrections on the curated candidate: distinct document-report vs ordinary-language evidence; retracted allocations recover what was said and who said it; legacy subtotal exercised through projection/marshalling/admission/`run()`; interrupted-write "re-drive" claim withdrawn and recorded as a hard gate |
| Owner-directed repair 2026-09-08 (evidence boundary) | Replaced the negative-only `document-report-entry` refusal with a positive requirement: current ordinary-language-entry evidence whose submitted answers correspond to the mapped finding. Distinct answer events cite distinct evidence citizens. Production contribution construction no longer invents `synthetic: True` |

**Exit criteria.** All ten are met. Criterion 5 is met by retraction, which
removes an identified assertion from current use without a replacement value,
without destroying history, and without exhausting the `(payer, statement,
tax-year, recipient)` identity.

Two evidence-quality limitations are recorded in the retrospective rather than
disposed of here: the committed no-activity test re-reads the same log, and the
structural rule check inspects `rule-artifact.v2` only. Neither affects
delivered behaviour; the owner decided not to widen the second.
