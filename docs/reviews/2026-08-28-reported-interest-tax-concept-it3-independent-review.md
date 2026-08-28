# Independent Review — Reported Interest Tax Concept it3

## Review object

- Candidate branch: `milestone/tax-concept-derivation-phase-definition`
- Candidate commit: `c87fcd744abff83d90107f2b0b74f5784d21f379`
- Executable exhibit: annotated tag
  `exhibits/reported-interest-tax-concept/it3`, peeled commit
  `865486cd0e3a0c44adaf55be4fb658845e380b0a`
- Ratified comparison line: `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`
- Range posture at pickup: 0 behind, 22 ahead; clean worktree; branch not
  contained in the ratified line.

The owner requested a fresh independent review and authorized this temporary
review record to be committed for later removal during curation. No candidate
document, production code, schema, content artifact, or ADR was edited.

## Verdict

**NOT READY.**

The repaired exhibit is materially better than it2: access grants are explicit,
the distributed shapes execute separate rules, pointer mutation is no longer a
completely inert test, TI-A1 is correctly bounded as a coverage probe, and the
tax and incumbent-artifact foundations survive review.

The central comparison is still not decision-ready. Shape C copies values from
the includible evaluation into a basis artifact whose provenance records only
the basis evaluation. Shape E follows pointers, but neither validates the
identity and kind of their targets nor carries target currentness into the
consumer's usability decision. Both defects become observable after a reported-
amount correction; E also accepts same-valued targets belonging to another
item. The published matrix therefore does not establish that C, E, and B
satisfy the same later-year requirements under the stated grants.

The cautious headline — that this evidence does not establish a new production
citizen kind as necessary and therefore does not justify selecting one —
survives. The stronger reduction of the remaining owner decision to “which
later-year capabilities are granted” does not. Provenance granularity, edge
validation, and dependency currentness remain unresolved parts of the
comparison, not downstream implementation detail.

## Blocking findings

### B1 — Shape C's copied fields have no provenance from the evaluation that produced them

**Durable claims affected.**

- `docs/milestones/reported-interest-tax-concept/README.md:31-32,45-47`
  says C carries copied `reported` and `includible` amounts and answers the
  partition-explanation task from the carried artifact.
- `docs/prototypes/reported-interest-tax-concept/examination.md:22-25,110-116`
  says each distributed rule has its own access log and C recovers the
  partition from its carried artifact.
- `docs/prototypes/reported-interest-tax-concept/examination.md:141-148` and
  `docs/phase-state.md:8,39-49` use that result to reduce the owner question to
  retained capabilities.
- `docs/prototypes/reported-interest-tax-concept/charter.md:76` requires each
  artifact's provenance to match the expression that ran and account for the
  facts that expression read.

**Executable contradiction.**

At the it3 tag:

- `prototype/reported_interest/shapes.py:403-433` obtains `reported` and
  `includible` from the includible evaluation, copies them into the basis
  artifact, and assigns only `basis.provenance` to that artifact.
- `prototype/reported_interest/shapes.py:145-165` deliberately makes the basis
  rule omit the reported amount and payer.
- `prototype/reported_interest/shapes.py:206-208` determines displacement only
  from the versions in that one provenance object.
- `prototype/reported_interest/rubric.py:130-144` cannot detect the packaging
  error: it compares `provenance.reads` with a set that already contains those
  same reads. It never traces the origin of each payload field.

Independent reproduction on TI-B2 produced a C basis artifact with payload
`{amount: 300, reported: 1200, includible: 900}` whose provenance omitted the
box-1 amount and payer. After correcting the reported amount from 1200 to 1000,
the currentness consumer reported:

```text
displaced=False
task 5=True: of 1200 reported, 900 was includible and 300 was accrued interest
task 6=True: usable=True (current)
```

Under the same correction, B reported `displaced=True` and `usable=False`.
A's full-workspace task 5 failed because it combined current `reported=1000`
with stale `includible=900`; E's outcome is covered separately below.

**What is wrong.** C is not an honestly provenanced embedded composite. Its
basis amount may remain valid after a report correction, but the same artifact's
copied report and includible values do not. Whole-artifact currentness declares
all three fields current because it sees only the basis rule's dependencies.
The test therefore erases the lifecycle difference the comparison is meant to
measure.

**Smallest property-level repair.** Preserve the distinction between basis
currentness and the currentness of the copied partition, whether by explicit
field/component provenance, a declared composite dependency, or another
bounded prototype mechanism. Then run every source and circumstance correction
through the later-year consumer, not only through per-artifact `Store.serve`,
and require a stale copied field to be rejected or explicitly identified as a
historical snapshot. Do not select a production schema while repairing the
evidence.

### B2 — Shape E's pointers are key lookups, not validated item relationships, and target displacement does not propagate

**Durable claims affected.**

- `docs/milestones/reported-interest-tax-concept/README.md:33-35,45-47` calls E
  a relationship edge whose partition is recoverable through an object store.
- `docs/prototypes/reported-interest-tax-concept/examination.md:122-137` says a
  “true edge-only packaging” passed task 5 and that pointer mutations make the
  task fail.
- `docs/milestones/reported-interest-tax-concept/synthetic-case-specification.md:288-292`
  relies on E as a differentiated retained-capability alternative.
- `docs/prototypes/reported-interest-tax-concept/charter.md:75,82-84` requires
  the declared relation to be verified against the statement item and the
  relationship fields to be exercised adversarially.

**Executable contradiction.**

At the it3 tag:

- `prototype/reported_interest/shapes.py:437-482` writes `sibling` and
  `reported_key` strings into the carried basis artifact.
- `prototype/reported_interest/rubric.py:314-326` performs an untyped
  `ObjectStore.get` and reads `payload["amount"]`. It does not check the target
  artifact's `item`, `kind`, rule, or provenance.
- `prototype/reported_interest/rubric.py:255-304` checks currentness only for
  the carried basis artifact. It never checks whether either pointer target is
  displaced.
- `tests/test_reported_interest_prototype.py:339-391` exercises missing keys,
  an empty store, and one same-item misdirection whose arithmetic happens not
  to balance. It does not exercise a wrong-item target with compatible values
  or a displaced target.

Independent mutation copied the valid 1200 reported and 900 includible
artifacts under new keys, changed both target artifacts' `item` to
`demo.obligation-other`, and pointed E's basis artifact at them. Task 5 still
passed:

```text
of 1200 reported, 900 was includible and 300 was accrued interest
```

After correcting the real item's reported amount to 1000, E's referenced
reported and includible artifacts were displaced, but the carried basis
artifact still reported `displaced=False`, task 5 used the stale 1200/900
targets, and task 6 reported `usable=True`.

**What is wrong.** The prototype proves that two strings can retrieve two
numerically compatible objects. It does not prove an item relationship or a
current dependency edge. Arithmetic catches the one tested misdirection by
accident; it does not validate identity. Target displacement is invisible to
the claimed edge consumer.

**Smallest property-level repair.** Make the prototype consumer validate the
target item and expected artifact kind, reject missing or foreign targets, and
include the currentness of every followed target in the relevant recovery and
usability result. Add adversarial cases for same-valued foreign-item targets,
wrong-kind targets, and source corrections that displace a target without
changing the basis amount. Preserve it3 as historical evidence; if executable
evidence changes, publish a successor exhibit rather than rewriting it3.

### B3 — Task 6 and the owner decision overstate what the currentness service can decide

**Durable claims affected.**

- `docs/prototypes/reported-interest-tax-concept/examination.md:90-108` defines
  task 6 as deciding whether the later year can use the artifact and reports
  currentness as sufficient to answer it.
- `docs/prototypes/reported-interest-tax-concept/examination.md:187-198`,
  `docs/milestones/reported-interest-tax-concept/README.md:125-136`, and
  `docs/phase-state.md:46-49,85-92` present the retained-capability selection as
  the remaining owner decision.
- The same documents acknowledge that rule, authority, coverage-declaration,
  and reporting-artifact succession were not executed.

**Executable boundary.** `prototype/reported_interest/shapes.py:197-215`
records rule, authority, and coverage identifiers, but
`prototype/reported_interest/shapes.py:299-310` gives `CurrentnessService` only
fact versions. `prototype/reported_interest/rubric.py:293-304` declares
usability decidable solely from those fact versions.

**What is wrong.** The executable service can answer only whether the carried
artifact's recorded fact versions remain current. It cannot decide general
later-year usability when rule, authority, coverage, reporting contract, edge
target, or artifact succession may have changed. The publication states those
dimensions are open while its task matrix simultaneously counts task 6 as
passed. That makes the owner question look smaller than the evidence supports.

**Smallest property-level repair.** Rename and bound task 6 to fact-version
currentness under fixed rule, authority, coverage, reporting, and target-
artifact assumptions, or execute a bounded currentness contract that includes
the additional dimensions. Reconcile the owner-decision wording across the
README, examination, case specification, plan, roadmap, and phase state. The
repair need not design production storage or a schema.

## Non-blocking findings

### N1 — Final-curation metadata and one stale exhibit pointer remain

- `docs/prototypes/reported-interest-tax-concept/examination.md:3-7` records
  exhibit commit hashes and branch-cleanup state. The plan's exit criterion 7
  at `docs/phases/tax-concept-derivation/milestones/reported-interest-tax-concept-vertical-slice.md:444-455`
  says final documents contain no commit or review/process metadata.
- `docs/phase-state.md:121-123` calls the executed prototype record current but
  points readers to `it1`; every other current lifecycle pointer names `it3`.
- This review file is temporary working-branch material under the owner's
  direction and must be removed during final curation.

These are publication-curation defects, not reasons to alter the prototype's
substantive result.

### N2 — The reported-interest artifact receives tax-treatment authority rather than statement support

For E, `prototype/reported_interest/shapes.py:263-265,448-470` creates a
`reported-interest` artifact by copying the reported amount, but the shared
`_run` helper at lines 224-237 attaches the same IRC § 61 / Publication 550
authority stack used for the tax treatment. The statement is the support for
what the statement reports; those tax authorities do not establish that source
fact. The ordinary fact name remains in `reads`, so the source is not wholly
lost, but the artifact-level authority account blurs a layer the milestone says
must remain separate. Bound or repair that attribution if E remains in a
successor comparison.

## Verified clean surfaces

- The it3 tag is an annotated tag peeling to the stated commit. it1 and it2 were
  not rewritten, and prototype code is absent from the milestone branch.
- Exact rerun in the it3 tree:
  `pytest tests/test_reported_interest_prototype.py -n0 -q` — 26 passed, 431
  subtests passed.
- The same tests under repository-default parallel settings also passed: 26
  tests and 431 subtests.
- Focused incumbent rerun on the candidate branch:
  `pytest tests/test_schedule_b_interest_adjustments.py tests/tax/test_track2_line2b.py -q`
  — 14 passed, 9 subtests passed.
- `python3 tools/envelope_scan.py --range origin/main..HEAD` passed.
- `python3 tools/governance_lint.py` reported conformant.
- `git diff --check origin/main..HEAD` passed.
- Relative Markdown links in the milestone and prototype directories resolve.
- No absolute local path, personal tax datum, credential, or session URL was
  found in the milestone or prototype publication.
- TI-A1 is now honestly bounded. The official 2025 Form 8815 and 26 USC § 135
  require facts absent from that fixture, so it is a coverage probe rather than
  proof of a positive exclusion. The incumbent's selected line-2b v4 consumes
  box-3 subtotal and has no Form 8815 / § 135 dependency.
- The accrued-interest treatment remains supportable: IRC § 61(a)(4) supplies
  the gross-income default; the official 2025 Publication 550 and 2025 Schedule
  B instructions supply the between-interest-dates purchaser treatment and
  reporting operation. Sources checked:
  [2025 Publication 550](https://www.irs.gov/pub/irs-pdf/p550.pdf),
  [2025 Schedule B instructions](https://www.irs.gov/pub/irs-pdf/i1040sb.pdf),
  [26 USC § 61](https://uscode.house.gov/view.xhtml?req=%28title%3A26%20section%3A61%20edition%3Aprelim%29),
  [26 USC § 135](https://uscode.house.gov/view.xhtml?req=%28title%3A26%20section%3A135%20edition%3Aprelim%29),
  and [2025 Form 8815](https://www.irs.gov/pub/irs-pdf/f8815.pdf).

## Publication recommendation

Do not close or publish this candidate yet. Preserve the tax analysis, the
incumbent survey, TI-A1's repaired boundary, explicit access grants, and the
separate evaluator runs. Repair the lifecycle and identity tests for C and E,
bound task 6 to the service actually executed, and then reconcile every durable
summary from the resulting evidence. No production representation should be
selected as part of that repair.
