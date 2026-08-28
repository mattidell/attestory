# Independent Review — Reported Interest Tax Concept it5

## Review object

- Candidate branch: `milestone/tax-concept-derivation-phase-definition`
- Candidate commit: `bbcc3fc38925f7d57a95c78ddf46300f141e8356`
- Executable exhibit: annotated tag
  `exhibits/reported-interest-tax-concept/it5`, peeled commit
  `35a10e8b87f8fbca7c3123f17d0711a7b589e3cf`
- Ratified comparison line: `origin/main` at
  `9159a13d261f5005523ad58f8893ffffd735f204`
- Pickup posture: clean worktree, 0 behind and 26 ahead of the ratified line;
  branch tip not contained in that line.

The owner requested a fresh independent review and authorized this temporary
review record to be committed. No candidate document, prototype exhibit,
production code, schema, content artifact, ADR, roadmap, or phase pointer was
edited by this review.

## Verdict

**NOT READY, with one bounded successor repair recommended.**

it5 closes the four blocking findings from the it4 review in substance:

- the source report survives TI-A1's tax-treatment refusal;
- C component provenance and E targets validate exact producer rule identity;
- the access grants are now honestly described as in-memory Python objects;
- dependency displacement is recorded as a correctness invariant rather than
  an owner-selectable policy.

Two contradictions remain inside the executed evidence. First, the
coverage-independent source report still carries the accrued-interest tax
coverage declaration and still stores source support in the field the prototype
calls `authority`. Second, task 5 calls its arithmetic reconstruction a
*current* partition even in access modes where task 6 correctly says currentness
is undecidable. These are central layer and evidence-ceiling defects, but they
are small. Neither revives the case for a new production citizen or changes the
milestone's headline conclusion.

## Blocking findings

### B1 — The source report is operationally ungated but its provenance still collapses source support, tax authority, and tax coverage

**Durable claims affected.**

- `docs/prototypes/reported-interest-tax-concept/charter.md:42-46` says the
  source report's support is the identified source fact, not substantive tax
  authority, and that the report does not apply tax-slice coverage.
- `docs/prototypes/reported-interest-tax-concept/examination.md:163-167` and
  `docs/milestones/reported-interest-tax-concept/README.md:59-61` say the
  source report is independent of tax-slice coverage.
- `docs/phase-state.md:8` promotes that separation into the phase summary.

**Executable contradiction.** At it5:

- `prototype/reported_interest/shapes.py:200-207` gives every `Provenance` one
  field named `authority` and defaults every instance to
  `coverage_id=demo.coverage.accrued-interest-at-purchase`, version 1.
- `prototype/reported_interest/shapes.py:213-218` renders everything in the
  first field as `authority:*` and every instance's coverage as
  `coverage:demo.coverage.accrued-interest-at-purchase.v1`.
- `prototype/reported_interest/shapes.py:227-246` offers no independent source
  support channel or way to omit tax coverage.
- `prototype/reported_interest/shapes.py:272-280` passes
  `SOURCE_FACT_SUPPORT` through the `authority` parameter and leaves the tax
  coverage defaults in place.

Independent inspection of both TI-B2 and TI-A1 source-report artifacts showed
`authority=source-fact:identified-statement-fact` and
`coverage=demo.coverage.accrued-interest-at-purchase.v1`. TI-A1 now correctly
retains the $840 report when treatment refuses, so the behavioural gate is
fixed. Its provenance nevertheless says the coverage-independent report is
inside that tax coverage declaration.

**What is wrong.** A source fact supporting what a statement reports is not a
tax authority, and the accrued-interest treatment coverage does not govern
whether that report exists. The new family label is accurate, but putting it
in an `authority` tuple while attaching the tax coverage declaration preserves
the layer collapse under different values. This directly weakens the
milestone's central promise that source report, tax treatment, and executable
coverage are recoverably separate.

**Smallest property-level repair.** In the prototype only, make source support
separate from tax authority and allow tax coverage to be absent. The source
report may use its exact `reads` as its support rather than adding another
shape. Its substantive-tax-authority collection must be empty and its
accrued-interest coverage id/version absent. Treatment artifacts retain both.
Add assertions over the complete source-report provenance on TI-B2 and TI-A1,
not only checks that three forbidden citation strings are absent. Do not design
a production schema.

### B2 — Task 5 claims a current explanation in modes that cannot determine currentness

**Durable and executable claims affected.**

- `docs/prototypes/reported-interest-tax-concept/examination.md:94-103` defines
  task 5 as explaining the basis reduction as a **current** partition and task 6
  as determining fact-version currentness.
- The score table at `examination.md:105-125` says C and B pass task 5 with only
  the carried object and E passes with object-store access, while explicitly
  saying artifact-object-only cannot answer task 6.
- `docs/milestones/reported-interest-tax-concept/README.md:51-57` consequently
  calls E's object-store result a current-partition answer.
- `prototype/reported_interest/rubric.py:342-363` makes task 5 pass when the
  three amounts reconcile; it does not require a currentness service.
- `prototype/reported_interest/rubric.py:365-380` correctly makes task 6 fail
  when no currentness service is granted.

Independent execution reproduced the contradiction:

- C with `artifact-object-only`: task 5 `True`, task 6 “currentness is not
  decidable”;
- E with `object-store-access`: task 5 `True`, task 6 “currentness is not
  decidable”;
- B with `artifact-object-only`: task 5 `True`, task 6 “currentness is not
  decidable.”

**What is wrong.** Those modes can reconstruct a partition recorded by the
source-year execution. They cannot establish that the reconstruction is
current. The test fixture's unamended state is knowledge held by the harness,
not evidence granted to the later-year consumer. Calling task 5 current makes
the access comparison claim more than its own task 6 permits.

**Smallest property-level repair.** Rename task 5 to recovery of the recorded
or historical partition explanation, leaving task 6 as the fact-version
currentness question. Define a *current explanation* as task 5 plus affirmative
task-6 currentness under the stated fixed rule/authority/coverage/reporting
assumptions. Alternatively, require a currentness grant for task 5, but do not
silently change the score meaning. Reconcile the score table, owner question,
README, charter, plan, roadmap, and phase state to the chosen bounded account.
Do not add a fifth packaging or a persistence probe.

## Non-blocking findings

### N1 — One stale “Bytes-only” sentence survived the whole-publication rename

`docs/milestones/reported-interest-tax-concept/synthetic-case-specification.md:283-290`
still says “Bytes-only cannot detect an amendment” and describes E only as
same-item/correct-kind. Replace it with `artifact-object-only` and carry the
producer-exact target account. This is publication inconsistency, not a new
evidence defect.

### N2 — Curation obligations remain outstanding by design

The working review records must be removed during Track 3 curation. The current
it5 tag is local and absent from `origin`; the curated candidate must make the
selected exhibit durably reachable without promoting historical review or
session metadata. This is not a repair to the substantive comparison.

## Verified clean surfaces

- it5 is an annotated successor tag peeling to the stated commit. it1-it4 were
  not rewritten. Prototype code remains absent from the milestone branch.
- Exact it5 rerun:
  `pytest tests/test_reported_interest_prototype.py -n0 -q` — 37 passed, 483
  subtests passed.
- TI-A1 treatment refuses with `SLICE_COVERAGE_UNSUPPORTED`; every packaging
  retains exactly one source-report artifact with amount 840, and the source
  workspace amount remains unchanged.
- E rejects wrong rule, wrong version, self-key mismatch, wrong kind, foreign
  item, missing target, and displaced target. C rejects a mutated component
  producer and stale copied components.
- Task 6 emits `fact_version_current`, not the former overloaded `usable` label.
- The access grants are explicitly in-memory; the durable record no longer
  claims serialization, persistence, or cross-process recovery was executed.
- Focused incumbent rerun:
  `pytest tests/test_schedule_b_interest_adjustments.py tests/tax/test_track2_line2b.py -q`
  — 14 passed, 9 subtests passed.
- The unchanged tax treatment remains consistent with 2025 Publication 550's
  *Bonds Sold Between Interest Dates* account and the 2025 Schedule B reporting
  instruction. The bounded TI-A1 refusal remains consistent with the additional
  conditions shown on 2025 Form 8815.
- `python3 tools/envelope_scan.py --range origin/main..HEAD` passed.
- `python3 tools/governance_lint.py` reported conformant.
- `git diff --check origin/main..HEAD` passed.
- Relative Markdown links in the milestone and prototype directories resolve.

## Publication recommendation

Do not run another broad comparison. Make one bounded it6 repair that separates
source support from tax authority/coverage and makes task 5 historical recovery
rather than unsupported currentness. Then perform one final contradiction scan
and curate. The stable result is already useful: the executable comparison does
not establish a need for a new production citizen, while it does establish the
missing ordinary-transaction facts, item linkage, substantive proposition, and
later-year basis consequence as real product/modeling gaps.
