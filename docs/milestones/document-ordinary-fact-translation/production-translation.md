# The Production Translation

Track 2 output. What was actually built, where the build departed from the
Track 0 design and why, what it cost, what it deliberately did not do, and how
T1 through T9 are exercised.

The plain-language account lives in
[`docs/domain-models/taxable-interest-translation.md`](../../domain-models/taxable-interest-translation.md).
The design it implements is
[`canonical-slice.md`](canonical-slice.md).

Track 1 did not run. Track 0 left one viable canonical shape, so a
discriminating prototype would have compared it only against shapes already
shown non-viable. That is recorded in `docs/phase-state.md`; nothing in the
build reopened it.

---

## 1. What was built

The canonical slice is one object-valued family plus one scalar family
projected out of it.

| Citizen | Role |
| --- | --- |
| `obligation-acquisition.bundle` | The ordinary-fact vocabulary: the acquisition record and the accrued amount |
| `family.obligation-acquisition` | The canonical family. Object-valued members, one per acquisition |
| `family.obligation-accrued-interest-paid` | The scalar family. `projects_from` the canonical family |
| `closure-mapping.*` (two) | Affirmative-only closure for each |
| `rule.obligation-accrued-interest-subtotal` | Collects the scalar family into `tax.us.2025.interest.obligation-accrued-subtotal` |
| `rule.form1040-line2b` v5 | Adds the seven positive subtotals, subtracts **four** adjustment subtotals |
| `form1040.line-2b.form-field` v6 | The field successor riding v5 |
| `rule.attachment.schedule-b` v5 | Renders the fourth subtraction row |
| `package.core-calculations` v34 | Admits the slice; supersedes line-2b v4, form-field v5, Schedule B v4 |

Two schema successors were minted: `source-family.v3` (adding
`identity_association`, designed in Track 0) and `attachment-rule.v9` (see §3).

The canonical family carries the person's own propositions. The scalar family
carries one number per acquisition, independently asserted, and is the only one
of the two that authorizes a subtotal. That split is not decoration: a rule
cannot read one member of a family, so the amount that line 2b subtracts has to
live in a family whose every member is that amount.

## 2. Departures from the Track 0 design

Four, each with the reason.

**Association is at payer level, not statement level.** The Track 0 payload
carried `concerns_reported_statement`. It was dropped. Statement identity is a
property of the document the payer issued, and asking the person which
*statement* their bond purchase concerns asks them to reason about the
paperwork rather than about the bond. Payer-level association is enough to
discriminate T5 and T8, which is the test the plan set. The consequence is
named, not hidden: two statements from one payer covering different obligations
cannot yet be told apart by association alone. That is future work, and it is
the narrower question, not the one this milestone had to answer.

**The `subject` identity key was kept**, although no other 2025 fact type
carries one. Every existing 2025 fact type is keyed on things a document names.
This one is keyed partly on the person, because the proposition *is* the
person's. Dropping it would have made the identity read as if the acquisition
were an attribute of the payer.

**The three recognition fields were made optional.** The Track 0 payload made
all five fields required. Under that `value_schema`, an unanswered recognition
question is not an unanswered question — it is a payload the kernel refuses to
construct, surfacing as `FindingModelError` rather than as a nameable refusal.
The family's own `field_absent` constraint arms were unreachable. `required` is
now `["acquired_on", "concerns_reported_payer"]`, so a partially answered record
is representable and the product can say which question is open. This is T3's
whole point, and the original shape could not express it.

**Schedule B v5 declares `itemizes_members` only.** It initially also declared
`reads_subtotal` on the canonical family and failed `FAMILY_ACCOUNTING_UNREACHED`:
it reaches that family through `projects_from` widening from the scalar family,
not directly. Line-2b v5 legitimately needs both, because it `requires` the
scalar subtotal by name.

## 3. `attachment-rule.v9` — the cost that exceeded prediction

Track 0 predicted one schema successor. Two were needed.

The fourth Schedule B adjustment row needs a `kind`. The plan of record was to
reuse `accrued_interest` with a distinct label. Reading
`_V3_ADJUSTMENT_BINDINGS` (`packages/derivation/package_validation.py:222`)
showed why that cannot work: `kind` is a **class-authority key**, not a display
hint. It pins both the exact label and the terminal token of the family that
may authorize the row, enforced at `package_validation.py:1888` via
`ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH` and
`ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH`. A row claiming a class it does not
belong to fails admission. That is a property worth keeping, so the vocabulary
had to widen rather than be borrowed against.

Three cheaper routes were tried and rejected on substance:

| Route | Why rejected |
| --- | --- |
| Reuse `accrued_interest` with a new label | The kind pins the label; a second label under one kind is a mismatch by construction |
| Rename the scalar family to the bound token | Creates a duplicate `(kind, label)` pair, which `presentation_projection.py:408` uses to match rows |
| Fold into the existing accrued-interest row via `projects_from` | `projects_from` is a validation-dependency edge, not a derivation mechanism; and one row names exactly one family |

The row is not optional presentation polish. `runner.py:1188` checks
`part_sum != line_value`, so Schedule B is **arithmetically mandatory** for any
line-2b adjustment class. Once line-2b projection is in Track 2's scope — the
plan puts it there explicitly — the fourth row follows, and the schema
successor follows from that.

`attachment-rule.v9` was generated from v8 by byte-level substitution, so shape
inheritance is exact and the diff is provably additive: `$id`, the `schema`
const, the title, and one enum member. Cost: roughly twenty mechanical
touchpoints across six modules. `artifact-package.v26` — minted earlier in this
same uncommitted change and never committed, so re-deriving it is not a
mutation of published history — gained the new token in both closed enums and a
cloned admission conditional.

Per Article 9, both manifests were republished with
`schema_registry.write_manifest`; `git diff --stat` on the two `published.json`
files shows 3 insertions and 0 deletions, no changed lines.

## 4. Generalizations, all strictly stronger

The build replaced two version-pinned checks with version-keyed maps. Both
tighten rather than loosen.

`_ADJUSTMENT_SURFACES` maps a line-2b content version to its exact adjustment
slot set (`v4` the ratified three classes, `v5` those plus the derived one).
The composition route was previously a boolean hard-gated to `"v4"`. A version
absent from the map now declares *no* adjustment surface and fails the
bijection checks, rather than silently widening them.

The Schedule B exact-class-surface check was de-gated from
`pin["version"] == "v4"` and now reads the same map, keyed by the same content
version. The two artifacts are a matched pair enforced structurally, rather
than by trusting that whoever mints a successor remembers to update both. This
was verified safe against the three historical versions: Schedule B v1, v2 and
v3 all carry empty `adjustment_rows`, so `.get(version, ())` yields `[]` and
they pass.

### A latent gap found on the way

Check 10c's subtractive-positive-basis allowance tested
`citizen["schema"] == "attachment-rule.v6"` by equality. Schedule B v4 is a v6
citizen, so no later generation had ever taken the positive-basis route, and
the equality had never been exercised. Schedule B v5 is the first, and it
failed `ATTACHMENT_LINE_AUTHORITY_MISMATCH` for a reason that had nothing to do
with its content. Widened to the set `{v6, v8, v9}` — v8 and v9 inherit v6's
subtractive shape. This was latent, not deliberate.

## 5. What was deliberately not built

**The masking-sibling amount guard**, named in Track 0 §1, remains deferred and
named. Detecting that one acquisition's accrued amount masks a sibling's
requires reading a counterpart member's **value** across families. ADR-0066
decision 2 closes the predicate language against exactly that. Opening it is a
doctrinal decision about the substrate, not an implementation detail of this
slice, and it is not needed for T1–T9. Association reads identity only.

**The later-year basis question.** Deferred by owner direction until the
current-year translation exists. It now exists.

## 6. T1 through T9

`tests/test_obligation_acquisition_translation.py` — 14 tests, 3 subtests, all
passing. Each case drives a real package run, not a unit stub.

| Case | Test class | What it observes |
| --- | --- | --- |
| T1 | `T1NoAcquisitionRecorded` | Closed-empty family derives a closure-backed zero; line 2b stands at the reported total and no row renders |
| T2 | `T2OrdinaryFactsBecomeAnAdjustment` | The purchase reduces line 2b and Schedule B renders it under its own label |
| T3 | `T3MissingAmountIsNamedNotDefaulted` | An absent amount blocks and names the open question; line 2b publishes nothing |
| T4 | `T4NothingToAttachTo` | An unmatched association blocks rather than inventing a report |
| T5 | `T5MoreThanOnePlausibleReport` | Ambiguity blocks rather than choosing |
| T6/T7 | `T6And7CorrectionsDisplaceIndependently` | Each correction moves only its own quantity |
| T8 | `T8SeveralObligationsUnderOnePayer` | Two obligations under one payer both subtract, discriminated by canonical identity |
| T9 | `T9NeighbouringCasesAreRefused` | Each neighbour blocks under its own code, and an unanswered recognition refuses the same way as a "no" |

Two test-construction facts worth recording, because both were initially got
wrong and both are properties of the system rather than of the tests:

**Refusals are read at the synthesized artifact, not run-wide.**
`FAMILY_VALIDATION_BLOCKED` is runner-internal. The report surfaces
`{"artifact_id": "<family>.member-validation.synthesized", "code":
"DEPENDENCY_INVALID", "missing": ["<BLOCK_CODE>"]}`. A run-wide code sweep also
passes for the wrong reason: this base return legitimately blocks dozens of
unrelated artifacts. `_refusal_codes` is scoped to the acquisition family's own
validation artifact.

**Corrections are assertions, not transitions.** Re-asserting a fact already
current in a family must be a plain `assertion` act. `member-transition` is
rejected at `packages/kernel/findings.py:738`, because membership did not
change — only the value did. T6 and T7 emit assertions and do not advance
horizons.

`BASE_BOX1` is `2000.0` because Schedule B's rendering threshold is `$1,500`.
Below it Part I is not rendered at all and the derived class is computed but
invisible, which is not the behavior under test.

Every identity is `demo.*`; every amount is invented.

## 7. Verification

Full suite, required because the change touches `packages/derivation/`.
`pytest` — **1502 passed, 20 skipped, 4135 subtests passed**, zero failures.
`tools/governance_lint.py` — conformant. `envelope_scan --range
origin/main..HEAD` — clean. `git diff --check` — clean.

**The fast lane fails, at HEAD and here equally.** A detached worktree at HEAD
(`6758be16`) was run under `pytest -m "not live"` alongside this tree. Both
produce **six failures, and the two failure sets are byte-identical** — `diff`
of the sorted `FAILED` lines is empty. Every one is `fast-lane budget
exceeded` against the 3.0s cap at `tests/conftest.py:50`; none is a logic
failure, which is why the full suite is green (the budget assertion only arms
under the fast-lane marker selection).

This is pre-existing fast-lane budget decay. It is surfaced to the owner as
such: it is not this milestone's to fix, and it must not be read as a
regression introduced here. One caution for whoever does pick it up — an
earlier measurement of the same baseline reported *five*, not six. The cap is
a wall-clock assertion under `-n auto`, so which tests trip it varies between
runs. Comparing counts is unreliable; compare the sets.

Package validation is green for both generations: `v33 ok: True []` was
re-confirmed after every `package_validation.py` change, so historical packages
are unaffected; `v34 ok: True []`.

## 8. Unresolved

Nothing that meets a stop condition. Two items are named future work:

1. **Statement-level association.** Payer-level is sufficient for T1–T9 and for
   the bounded treatment. Two statements from one payer covering different
   obligations is the case it cannot yet discriminate.
2. **The masking-sibling guard**, which needs a cross-family value read and
   therefore a decision about ADR-0066's closed predicate language.

Neither forces a user to supply a tax classification, and
`test_the_person_supplied_no_tax_classification` asserts that directly: the
recorded payload carries no tax word — no "adjustment", "schedule", "line",
"taxable", or "deduct". The person says what they bought, when, from whom, and
what they paid the seller. The rules do the rest.
