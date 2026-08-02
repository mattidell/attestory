# Schedule K-1 Box-5 Interest Breadth — Independent Review Charter

Audience: Reviewer.

Status: **chartered for owner launch.**

## Context Capsule

- **Source ref and resolved launch commit:** branch
  `milestone/k1-interest-breadth` at
  `466780685e82ec1f957985ac5bed0a08c2386224`.
- **Exact implementation object:**
  `2f8154081aac42e00fda43f9ac0a347d7de0ca0a..466780685e82ec1f957985ac5bed0a08c2386224`.
  The lower commit is the final planning clarification and is context, not an
  implementation object.
- **Role:** one author-independent Reviewer, High tier / high effort. Do not
  consult the Builder's thread, handoff self-assessment, or uncommitted
  operational ledger.
- **Scope and evidence ceiling:** measure K1-C1 through K1-C5 and every
  K1-P1–P10 / K1-N1–N13 case against the exact range. The ceiling is
  production-shaped synthetic evidence through `live_coordinate_run` and the
  committed presentation harness. Do not design or implement repairs, add tax
  breadth, use real data, or make an L3 claim.
- **Stop conditions:** stop and report if the exact range or branch tip differs;
  if the worktree is dirty before review; if a published historical schema,
  content citizen, package, registry, release, or adoption was changed or
  removed; if review requires governance interpretation or a neighboring tax
  decision; if real/private material is encountered; or if a failing command
  cannot be attributed to this range without a focused base comparison.
- **Full reads before acting:** this charter; `docs/roles/reviewer.md`;
  `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-31-k1-interest-breadth-builder.md`;
  `docs/phases/engine-breadth/milestones/k1-interest-breadth.md`;
  every file in the exact implementation range; all sources emitted by the
  Orientation Block for action `review`; and the case-bearing tests
  `tests/test_k1_interest_breadth_contracts.py`,
  `tests/test_attachment_rule_v2.py`, and
  `tests/test_k1_interest_breadth_integration.py` in full.

Before reviewing, echo the resolved branch tip, exact range, synthetic evidence
ceiling, independence constraint, and all stop conditions.

## Review posture

This is the single independent integrated review specified by the milestone's
lean production loop. Measure semantic correctness, omitted adversarial cases,
compatibility, and boundary violations. Do not spend the review merely
repeating the Builder's routine green commands. Read assertions for honesty,
construct independent mutations at the real validation/runtime boundaries,
and cite falsifiable evidence.

The milestone plan is the single specification for K1-C1–C5 and the K1-P/N
matrix. A case is discharged only when its test name or docstring carries the
case ID and its assertion observes the required outcome at the appropriate
production boundary. Shared coverage is acceptable only when the stronger test
plainly proves every named case.

## Required measurements

### 1. Exact range, publication history, and safety

Enumerate the exact range and group its files as schema, content, runtime,
package/release, fixtures, tests, tooling, and presentation. Verify that all
38 implementation files belong to the accepted boundary. Compare historical
schema checksums and the v3 publication registry against the lower commit; the
range may only append `attachment-rule.v2`, `artifact-package.v6`, successor
citizens, package v9, registry v4, release v4, and a new adoption/fixtures.

Independently recompute both new schema checksums and prove each manifest added
one unused filename without changing or removing an old entry. Inspect the
range for real/private data, absolute local paths, or generated private
artifacts and run the envelope scan.

Failure means any out-of-scope file, historical byte/checksum rewrite, unsafe
fixture, or unpublished schema consumption.

### 2. K-1 identity, admission, and lifecycle — K1-C1

Recover the Form-1065-only box-5 contract from the bundle, family, closure
mapping, cited subtotal, contribution path, and integration tests. Verify:

- fact identity is tax year + partnership + logical K-1 statement, never an
  evidence/document/upload key;
- corrections preserve statement identity and currency while two original
  statements from one partnership remain distinct;
- the amount is nonnegative and admission failure is atomic;
- family membership, horizon closure, late-member displacement, and rerun use
  the production contribution/coordinator path; and
- no Form 1120-S, Form 1041, other K-1 box, or partnership-basis claim is
  implied by identifiers, labels, or predicates.

Trace K1-P1, P3, P4 and K1-N1–N4. Independently mutate one negative amount and
one evidence-key identity at the real admission/schema boundary. Failure means
identity broadening, bypassed admission, stale closure authority, or a case
whose assertion only restates fixture bytes.

### 3. Five-family composition and line 2b — K1-C2

Prove composition v2 declares exactly the four historical positive-interest
families plus the Form-1065 K-1 box-5 family, once each, with exact subtotal and
closure pins. Confirm the residual non-form predicate was not widened. Verify
line-2b rule v2 binds that composition, reads and requires closure for all five
slots, declares the exact citation, and remains the sole package-selected
producer of the stable line-2b symbol.

Trace K1-P2, P5, K1-N5, and K1-N6 through package validation and live execution.
Independently create one package mutation that substitutes or duplicates a
composition slot and one that removes the K-1 closure/value dependency from
line 2b. Failure means either mutation admits, an unclosed family publishes, or
downstream line 9 consumes a narrow/mixed producer.

### 4. Attachment v2 structure and semantic admission — K1-C3

Read both new schemas and their fully resolved examples. Verify
`artifact-package.v6` preserves the v5 contract while admitting
`attachment-rule.v2` only under the existing attachment-rule role. For
Schedule B v2, prove Part I uses composition authority over composition v2 and
contains a structural bijection: exactly one row set for every declared family,
each with the correct member type and subtotal. Prove Part II retains its
single-family ordinary-dividend authority and that the trigger, Part III,
FinCEN-114 obligation, symbols, and dispositions are unchanged.

Trace K1-N7–N9 at package-validation—not schema-only—boundaries. Independently
exercise an omitted family, a duplicate family, and one wrong member/subtotal
pair. Failure means any malformed graph reaches execution or a schema negative
fails first for an unrelated reason.

### 5. Schedule B execution and containment

Trace K1-P6–P9 and K1-N10–N11. Verify the evaluator checks each family row set
against its own subtotal before checking the combined Part-I total against line
2b; both use `ITEMIZATION_TIE_OUT_VIOLATION`, block only Schedule B, and publish
no fabricated attachment. Confirm row collection consumes current findings and
preserves same-family authority.

Independently exercise one per-family stale-row mismatch and one whole-part
mismatch through the narrow `RunContext` seam authorized by the plan. Confirm
line 2b remains published and valid sibling sections survive. Failure means a
tie-out is absent, ordered incorrectly, pins fabricated output, or escapes the
attachment-only boundary.

### 6. Package, release, compatibility, and mixed graphs — K1-C4/C5

Resolve registry v4, release v4, and the new adoption through the real package
resolver and `live_coordinate_run`. Prove package v9 selects exactly one current
K-1 family, composition v2, line-2b rule v2, line-2b field content v3, Schedule
B v2, and the unchanged downstream graph. Verify all selected input bytes are
checksum-bound.

Trace K1-P10 and K1-N12. Run the historical v8 route and prove its v1 behavior
still resolves. Independently substitute line-2b field content v1 and v2 in
separate successor-graph mutations, plus one old line-2b or Schedule-B rule;
each must refuse before execution. Failure means a mixed graph admits, a
historical route changes, or v9 depends on unselected field content v2.

### 7. Explanation and presentation boundary

Inspect the generated production-shaped presentation fixtures back to their
live-run inputs and generator. Prove the K-1 amount appears only through derived
line 2b and Schedule B, the form-field → rule → resolved-citation chain is
exact, all five current family closures and consumed row findings are in the
appropriate lineage, and no rejected value reaches the model.

Trace K1-N13 through the actual presentation projection and committed browser
harness evidence. Independently inject one rejected or nonnumeric K-1-derived
value and confirm section-contained redaction without blanking valid siblings.
Failure means fixture-only claims, fabricated provenance, missing citation
identity, unsafe value rendering, or page-wide failure.

### 8. Matrix completeness and test honesty

Build a table covering every K1-P1–P10 and K1-N1–N13 ID with test method,
production boundary, and observed assertion. Search the three prescribed
modules directly and report any missing, duplicate-but-weaker, or mislabeled
case. Read generators and tests for private reconstructions, hard-coded
allowlists, assertions that only echo inputs, or direct writes that bypass
contribution, resolution, validation, or live coordination.

Failure means any case is unaccounted, only asserted below its required
boundary, or passed through a test-only route not used by production.

## Focused verification

Run each once unless an earlier attributed failure makes later execution
meaningless:

```text
python3 -m unittest tests.test_k1_interest_breadth_contracts
python3 -m unittest tests.test_attachment_rule_v2
python3 -m unittest tests.test_k1_interest_breadth_integration
python3 -m unittest tests.tax.test_track2_line2b tests.test_dsbs_t2_schedule_b
python3 -m unittest tests.test_frrs_t3_resolver_bootstrap
python3 -m unittest tests.test_presentation_l2_integration
python3 -m unittest tests.test_schema_registry
python3 -m mypy
git diff --check 2f8154081aac42e00fda43f9ac0a347d7de0ca0a..466780685e82ec1f957985ac5bed0a08c2386224
python3 tools/governance_lint.py
python3 tools/envelope_scan.py --range 7066f26e02467a58ca6cb329666782b32bd7dd12..HEAD
```

Run the committed K-1 presentation harness once when local Chrome is available;
otherwise record the unavailable capability and measure K1-N13 through the
projection seam. Do not run full `pytest`; CI is the gate of record. Use a base
comparison only to attribute a specific failure.

## Review record and verdict

Write `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-31-k1-interest-breadth-review.md` and commit it on
the same branch. Report exactly one verdict:

- `READY` — all required measurements pass with cited evidence and the full
  case table is accounted; or
- `NOT READY` — numbered findings F1… identify the violated K1 contract/case,
  precise file/line evidence, and a reproducible measurement.

Record commands and results. Findings may recommend a bounded correction but
must not implement it or expand scope. Do not edit implementation, schemas,
manifests, fixtures, tests, generators, the Builder charter, phase state, or
the milestone plan; do not open or merge a PR. Stop after the review-record
commit and return custody to the Foreman with self-reported turn and tool-call
counts.
