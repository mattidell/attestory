# Independent Review — Reported Interest Tax Concept it4

## Review object

- Candidate branch: `milestone/tax-concept-derivation-phase-definition`
- Candidate commit: `9e9c7d8d32db581a60c2c092af245229e46eb41c`
- Executable exhibit: annotated tag
  `exhibits/reported-interest-tax-concept/it4`, peeled commit
  `c374c809e2bf009d134ab85ced3b0eb01a8b4a9b`
- Ratified comparison line: `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`
- Pickup posture: clean worktree, 0 behind and 24 ahead of the ratified line;
  branch tip not contained in that line.

The owner requested a fresh independent review, authorized this temporary
review record to be committed, and will remove review records during curation.
No candidate document, prototype exhibit, production code, schema, content
artifact, or ADR was edited by this review.

## Verdict

**NOT READY.**

it4 closes the three blocking measurements from the it3 review:

- C's copied fields now retain the includible evaluation's provenance and are
  rejected as a current explanation after that evaluation is displaced.
- E now rejects foreign-item, wrong-kind, missing, and displaced targets.
- Task 6 is explicitly bounded to fact-version currentness under fixed rule,
  authority, coverage, and reporting assumptions.

The repaired lifecycle results reran successfully. The remaining defects are
at the layer and identity boundaries. E's “reported-interest” producer still
conditions a statement report on tax-slice coverage and substitutes the blank
IRS form for the particular statement that supplied the value. E also treats a
target's `kind` label as proof that the expected rule produced it; a same-item,
same-kind artifact carrying the wrong rule provenance passes task 5. Finally,
the publication calls an in-memory dataclass grant “artifact bytes” without
executing any serialization boundary, and it presents dependency currentness
as an owner-selectable policy where the current-explanation invariant is
already settled by provenance.

The headline “do not select a production citizen on necessity grounds” remains
prudent. The four-packaging comparison and its owner-decision reduction are not
yet reliable enough to close the milestone.

## Blocking findings

### B1 — E's reported-value artifact is tax-gated and cites a form template as evidence for a particular statement value

**Durable claims affected.**

- `docs/prototypes/reported-interest-tax-concept/examination.md:152-153` says
  E's reported-interest artifact cites Form 1099-INT as “statement support.”
- `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md:81-104`
  says source report, tax classification, tax concept, and form line remain
  separate and all four packagings meet the layer-ownership objective.
- `docs/milestones/reported-interest-tax-concept/accrued-interest-item-model.md:25-49`
  correctly says the particular statement itself supports what it reports and
  that the proposition remains true regardless of the later tax treatment.
- `docs/prototypes/reported-interest-tax-concept/charter.md:75-84` requires the
  statement report to remain unmodified and substantive authority to attach to
  the treatment.

**Executable contradiction.** At it4:

- `prototype/reported_interest/shapes.py:49-55` defines `STATEMENT_SUPPORT` as
  family `irs-form`, citation `Form 1099-INT`.
- `prototype/reported_interest/shapes.py:176-191` makes `reported_guard` read
  `obligation_kind` and `education_expenses` and execute `_coverage`.
- `prototype/reported_interest/shapes.py:277-285` uses that tax-gated guard for
  the reported-value artifact.
- `prototype/reported_interest/rubric.py:170-176` calls every artifact's
  authority “substantive authority,” including this reporting copy.

Independent execution of `evaluate_reported(case_ti_a1())` returned
`Blocked(SLICE_COVERAGE_UNSUPPORTED)`. The synthetic statement still reports
$840; only the tax treatment is outside this slice. The report proposition
therefore disappears from this producer for a reason that cannot affect its
truth.

**What is wrong.** An official blank Form 1099-INT defines the form and its
boxes; it does not establish that one identified synthetic statement reported
a particular amount. The particular statement/source fact is that support.
Tax-treatment coverage cannot determine whether the report exists. The repair
changed the authority label but did not separate source evidence from tax
authority or remove the tax gate.

**Smallest property-level repair.** Make the reported-value evaluation depend
only on the facts needed to identify and read the statement value. It must
succeed on TI-A1 even when the tax treatment refuses coverage. Represent its
support as the source fact or source evidence, not as substantive tax authority
from the generic IRS form. Require substantive authority only on tax-treatment
artifacts. Add an executable assertion that an unsupported treatment leaves the
statement report recoverable and unmodified. Do not design a production schema
to make this distinction.

### B2 — E validates an artifact-kind label but not the producer identity that gives the target its meaning

**Durable claims affected.**

- `docs/milestones/reported-interest-tax-concept/README.md:34-37,50-58` says E
  follows validated targets and uses their dependency currentness.
- `docs/prototypes/reported-interest-tax-concept/examination.md:115-147,160-165`
  says same-item, correct-kind targets make E a successfully executed
  relationship packaging.
- `docs/prototypes/reported-interest-tax-concept/charter.md:42-47` requires
  target validation and says a misdirected relationship must change the
  consumer result.
- Task 6 is expressly evaluated under fixed rule assumptions at
  `docs/prototypes/reported-interest-tax-concept/examination.md:90-99`.

**Executable contradiction.** At it4,
`prototype/reported_interest/rubric.py:346-358` validates only that a lookup
returns an artifact with the carried item and expected `kind`. It does not
validate the target's own key, producing rule id/version, coverage declaration,
or any other producer identity available in its provenance.

Independent mutation copied the valid includible artifact, preserved the same
item, value, and `kind="includible-interest"`, but replaced its provenance with
the basis artifact's `demo.rule.basis-reduction` provenance. E's task 5 still
passed and reported the 1200/900/300 partition.

**What is wrong.** The consumer treats the label `includible-interest` as proof
that the artifact is the output of the includible rule. That is the exact
label-as-definition shortcut the milestone's evidence standard rejects. Item
and kind validation close accidental cross-item lookup; they do not establish
the producing proposition. This also contradicts task 6's fixed-rule premise,
because the followed dependency may not be from that rule at all.

**Smallest property-level repair.** Under the prototype's explicitly fixed-rule
premise, validate each target's exact expected rule id and version as well as
its item, kind, and self-key. Add same-value mutations for wrong producer rule,
wrong rule version, and a dictionary entry whose artifact self-key does not
match the requested key. If the prototype intends to trust an object-store
contract for any of those properties instead, declare and execute that contract
rather than assuming it.

### B3 — “Artifact bytes” and “retained-object store” are not executed access boundaries

**Durable claims affected.**

- `docs/prototypes/reported-interest-tax-concept/examination.md:34-43` and
  `docs/prototypes/reported-interest-tax-concept/charter.md:49-60` define the
  first grant as artifact bytes only and the third as a retained-object store.
- `docs/milestones/reported-interest-tax-concept/README.md:44-59,132-138` and
  `docs/phase-state.md:46-49,85-90` use those grants to frame the remaining
  owner decision.

**Executable boundary.** `prototype/reported_interest/rubric.py:243-255,433-454`
passes live Python `Artifact`, `CurrentnessService`, `ObjectStore`, and
`Workspace` objects directly. No encoding, decoding, persistence, or reloading
occurs. C now embeds `Provenance` dataclass instances inside its payload at
`prototype/reported_interest/shapes.py:423-460`. A direct standard JSON attempt
on every carried artifact fails even before C's nested provenance is reached,
because the amount is a Python `Decimal`.

**What is wrong.** The probe establishes what an in-memory artifact object can
answer when handed other in-memory capabilities. It does not establish an
artifact-bytes-only or durably retained-object boundary. The publication
correctly refuses to infer schema compatibility, but then uses an unexecuted
serialization claim to define the product capabilities the owner must choose.

**Smallest property-level repair.** Choose one bounded honest path:

1. rename the modes to `artifact-object-only` and `object-store access`, state
   explicitly that serialization, persistence, and later-process recovery were
   not executed, and narrow the owner decision accordingly; or
2. add one prototype-only deterministic encode/decode round trip for the
   carried artifact and retained targets, without proposing a production
   schema, and make every later-year task consume only the decoded result.

Do not call an in-memory dataclass “bytes.”

### B4 — The owner is asked to decide whether a stale dependency may count as current

**Durable claims affected.**

- `docs/milestones/reported-interest-tax-concept/README.md:132-138`,
  `docs/prototypes/reported-interest-tax-concept/examination.md:202-215`, and
  `docs/phase-state.md:46-49,85-90` put to the owner whether a copied or
  pointed-to partition is current only while its producing evaluations are
  current.

**What the exhibit actually establishes.** Task 5 is expressly a *current*
partition explanation. it4 demonstrates that displaced copied fields and
displaced pointer targets cannot support that current explanation. That is a
provenance correctness result, not an optional product semantic.

**What is wrong.** The product may choose to recompute the explanation, retain
and label it as historical, or withhold a current explanation. It may also
decide whether the independently current basis amount remains usable for a
specific later-year action. It cannot honestly choose to call a partition
current while the evaluations that produced its components are displaced.
The present wording turns an established invariant into a confusing owner
choice.

**Smallest property-level repair.** Record the dependency-currentness rule as a
settled finding. Restate the remaining owner question as the product consequence
of a split state: what later-year task is required, what capabilities support
it, and what to do when the basis amount remains current but its partition
explanation is historical. Reconcile that wording across every lifecycle
summary.

## Non-blocking findings

### N1 — Task 6's raw output still says `usable=` while disclaiming usability

`prototype/reported_interest/rubric.py:328-337` emits `usable=True/False` and in
the same result says it does not decide general later-year usability. The docs
are now correctly bounded; remove the overloaded `usable` label so the
executable output cannot be quoted more broadly than its premise.

### N2 — C's component-provenance check is presence-oriented rather than producer-exact

`prototype/reported_interest/rubric.py:131-150` requires a `Provenance` object
for both copied fields but verifies the reported-amount read only for the
`reported` component and does not verify the expected producing rule id/version
for either component. The normal publisher supplies the right provenance, so
this did not falsify the rerun. Once B2 adds producer-exact validation, apply
the same property to C and add a mutated-component test.

### N3 — Curation residue remains by owner direction

The it3 review and this it4 review are temporary working-branch records and
must be removed during curation. The prototype charter/examination still carry
exhibit lifecycle metadata. The current `it4` tag is local rather than present
on `origin`; before publication, the curated record must ensure its referenced
executable exhibit is durably reachable without publishing historical session
metadata from the it1 annotation.

## Verified clean surfaces

- it4 is an annotated successor tag peeling to the stated commit. it1-it3 were
  not rewritten. Prototype code remains absent from the milestone branch.
- Exact it4 rerun:
  `pytest tests/test_reported_interest_prototype.py -n0 -q` — 32 passed, 455
  subtests passed.
- The former C stale-copy reproduction now fails task 5 and reports false
  used-dependency currentness after a reported-amount correction.
- The former E foreign-item, wrong-kind, missing-target, and displaced-target
  reproductions now fail.
- The reported-interest artifact no longer carries IRC § 61 / Publication 550
  in its authority tuple. The remaining source-support problem is B1 above.
- Focused incumbent rerun:
  `pytest tests/test_schedule_b_interest_adjustments.py tests/tax/test_track2_line2b.py -q`
  — 14 passed, 9 subtests passed.
- `python3 tools/envelope_scan.py --range origin/main..HEAD` passed.
- `python3 tools/governance_lint.py` reported conformant.
- `git diff --check origin/main..HEAD` passed.
- Relative Markdown links in the milestone and prototype directories resolve.
- The tax analysis, TI-A1 boundary, and incumbent artifact survey were not
  substantively changed by this repair and remain consistent with the official
  sources rechecked for the it3 review:
  [2025 Publication 550](https://www.irs.gov/pub/irs-pdf/p550.pdf),
  [2025 Schedule B instructions](https://www.irs.gov/pub/irs-pdf/i1040sb.pdf),
  [26 USC § 61](https://uscode.house.gov/view.xhtml?req=%28title%3A26%20section%3A61%20edition%3Aprelim%29),
  [26 USC § 135](https://uscode.house.gov/view.xhtml?req=%28title%3A26%20section%3A135%20edition%3Aprelim%29),
  and [2025 Form 8815](https://www.irs.gov/pub/irs-pdf/f8815.pdf).

## Publication recommendation

Do not close or publish the candidate yet. Preserve it4's corrected component
currentness, target item/kind checks, bounded task 6, tax analysis, TI-A1
boundary, and incumbent survey. Repair source support and target producer
identity in one bounded successor exhibit, make the access-mode evidence ceiling
honest, and remove the false owner choice about stale dependencies. No
production citizen, schema, or representation should be selected in that
repair.
