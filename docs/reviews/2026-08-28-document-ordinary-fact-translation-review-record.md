<!-- Independent review record. Produced by a Grok CLI reviewer agent under
     docs/reviews/charter-2026-08-28-document-ordinary-fact-translation-review.md,
     against commit 0cac5ce9, without access to the milestone lead's thread.
     Machine-local measurement paths removed; content otherwise as returned. -->

# Independent Review — Document and Ordinary-Fact Translation Vertical

Reviewer seat. Charter: `docs/reviews/charter-2026-08-28-document-ordinary-fact-translation-review.md`.
Object: `origin/main..0cac5ce9` (plan `40ec8f88`, Track 0 `6758be16`, Track 2 `0cac5ce9`).
Charter commit `a0abe24d` rides on top of HEAD; noted, not in the object.
Branch: `milestone/document-ordinary-fact-translation`.
Draft PR #188. Ratified comparison: `origin/main` is 0 behind / 4 ahead of HEAD (4 includes charter). Not spent.

## Orientation

Verified `0cac5ce9c59fdc0b85108b13e9f26af0d89e3b98` exists as the Track 2 commit and is the parent of the charter. SHA match. Proceeding.

Independence: evidence docs in `docs/milestones/document-ordinary-fact-translation/` and `docs/domain-models/taxable-interest-translation.md` are candidate claims, not sources of truth.

No candidate modification. No commit. `docs/phase-state.md` untouched.

## Verdict

**READY** at `0cac5ce9`. One non-blocking evidence finding. No blocking defect.

The box: ordinary purchase facts and payer reports enter; adopted family constraints and `identity_association` make those inputs usable; the box may derive a fourth line-2b / Schedule B adjustment class from those facts; tax classification stays rule-owned; neighboring treatments and later-year basis stay outside; historical v33 and the three incumbent Schedule B classes remain unchanged.

---

## Findings

### F1 — Plan T6 is not an executed production case (evidence, non-blocking)

**Claim.** The plan's T6 required observation is: corrected reported amount, acquisition unchanged, only dependent conclusions change, the ordinary fact is not rewritten. Exit criterion 6 asks the same of document and ordinary-fact corrections. `production-translation.md` §6 claims T6/T7 coverage via `T6And7CorrectionsDisplaceIndependently`.

**Check.** Read `tests/test_obligation_acquisition_translation.py` `T6And7CorrectionsDisplaceIndependently` (lines 459–477) and the plan table in `docs/phases/tax-concept-derivation/milestones/document-ordinary-fact-translation.md` (T6/T7 rows). Traced `_acquisition_acts(..., corrections=...)`: corrections emit `assertion` acts against the acquisition / scalar fact ids, never against a box-1 finding.

**Found.**
- `test_correcting_the_accrued_amount_moves_only_that_amount` is plan **T7** (300 → 250; line 2b = `BASE_BOX1 - 250`).
- `test_correcting_the_purchase_record_leaves_the_amount_standing` changes `acquired_on` only and asserts line 2b still subtracts 300. That does not observe a document correction, and it does not observe a tax conclusion moving.
- No live case corrects the box-1 reported amount and checks that the acquisition member is untouched.

**Consequence.** Document-correction independence for this slice is not established by the package-level battery. Ordinary-fact correction (T7) is established. Box-1 supersession is pre-existing kernel behavior, not new machinery. This is an evidence gap, not an observed wrong displacement.

**Smallest repair.** One additional `_run` that corrects the base box-1 finding, asserts line 2b moves by the document delta, and asserts the acquisition member / scalar amount are unchanged. Do not expand into a second identity scheme.

---

## Required questions

### 1. Necessity of `attachment-rule.v9`

Re-derived from `packages/derivation/package_validation.py` `_V3_ADJUSTMENT_BINDINGS` (lines 222–235) and the 10c loop (1920–1936): `kind` is a dict key mapping to exactly one `(label, family-token)`. `ATTACHMENT_ADJUSTMENT_LABEL_MISMATCH` and `ATTACHMENT_ADJUSTMENT_AUTHORITY_MISMATCH` fire when a row borrows another class. Confirmed against `tests/test_schedule_b_interest_adjustments.py` `test_v15_attachment_mutations_reject_each_class_label_or_authority`, which still mutates Schedule B v4.

`runner.py:1191` (`part_sum != line_value`) makes a fourth Schedule B adjustment row arithmetically mandatory once line 2b subtracts a fourth class. Without the row, Part I cannot publish beside the new line-2b value.

Byte diff of `attachment-rule.v8` (origin/main, unchanged) vs `attachment-rule.v9`: `$id`, `schema` const, title/description, and one enum member `obligation_accrued_interest`. Additive.

Byte diff of `artifact-package.v25` (origin/main, unchanged) vs `v26`: `$id` / const / title / description, `attachment-rule.v9` and `source-family.v3` added to both closed enums, and two cloned admission conditionals. Additive.

The three recorded cheaper routes:

| Route | Holds? |
| --- | --- |
| Reuse `accrued_interest` with a new label | Yes. Bindings pin one label per kind. |
| Rename the scalar family to the bound token `accrued-interest` | Yes. `presentation_projection.py:408` matches adjustment rows on `(kind, label)`. Two rows with the same pair are ambiguous. |
| Fold via `projects_from` into the existing accrued-interest row | Yes as stated: `projects_from` is a validation-widening pin (`package_validation.py` `_constrained_closure`), not a collect. One row names one family. |

Fourth route considered (not recorded): feed both families into the **existing** `scheduleb-accrued-interest-subtotal` symbol so line 2b still subtracts three classes and Schedule B keeps three rows. That avoids v9. It fails the runner's per-row tie-out (`row_sum != subtotal_value` at `runner.py:1165–1168`): the existing row still `collect_members` of the transcribed family, so its row sum cannot equal a combined subtotal unless the new amounts are members of that same family. Same-family membership is the Track 0 reused-claim collapse (different author, identity, vocabulary). Weakening the tie-out is worse than minting v9.

v9 is necessary given a distinct class; a distinct class is necessary given provenance plus itemization tie-out. Not a missed viable cheaper route.

### 2. Whether the generalizations are strictly stronger

`_ADJUSTMENT_SURFACES` maps content version → exact slot set (`v4` three classes, `v5` those plus the derived slot). Composition bijection and the Schedule B class-surface check both read this map via `.get(version, ())`.

Unrecognized-version construction (in-process, no candidate edit):

- `v6` carrying v5's four adjustment requires → bijection **fails**.
- `v6` dropping adjustments → bijection **passes** with empty surface (same as origin/main's non-`v4` path).
- Schedule B `v6` with four rows → class-surface **fails**.
- Schedule B `v6` with zero rows → **passes**.

Compared with origin/main (`pin["version"] == "v4"` hard gate at former lines 1174/1215/1901): a successor that carried adjustment rows was previously **not checked**. It is now checked and fails unless added to the map. Strictly stronger for any successor that subtracts. Empty-surface success for a version absent from the map is not a silent widening of the slot set.

Historical Schedule B v1/v2/v3: inspected `rule.attachment.schedule-b.json` / `.v2.json` / `.v3.json`. They do **not** carry empty `adjustment_rows`; the field is absent. Their schemas are `attachment-rule.v1` / `v2`, so they never enter check 10c (gated to v6/v8/v9). The lead's "empty `adjustment_rows`" safety argument is false as written. Safety holds because those versions are outside the check. v4 (schema v6, three rows) is in the map and matches.

Check 10c allowance: origin/main used `citizen["schema"] == "attachment-rule.v6"`. Now `{v6, v8, v9}`. Existing v8 citizens (`attachment.f8949.v2.json`, `attachment.schedule-d.v6.json`) have `adjustment_rows` length 0 and `authority.kind == single_family`, so they never take the composition/positive-basis branch. The remaining conjuncts (`operation == subtract`, composition publishes `positive-total`, line symbol `taxable-total`) are the Schedule B Part I shape. Widening does not admit Form 8949 or Schedule D, or any other committed attachment, into that exception.

### 3. Whether the input forces a tax classification

Committed `value_schema` in `obligation-acquisition.bundle.json`: properties `acquired_on`, `accrued_interest_paid_to_seller`, `concerns_reported_payer`, and three yes/no/unknown recognition fields. `required` is `["acquired_on", "concerns_reported_payer"]`. No adjustment class, schedule, line, or coverage flag.

`test_the_person_supplied_no_tax_classification` constructs `Acquisition.record()` — the test helper — and greps a word list (`adjustment`, `schedule`, `line`, `taxable`, `deduct`). It never loads the bundle. That test is a rehearsal of the helper, not a schema guarantee. The committed schema, inspected directly, stays on the ordinary-fact side: a purchase date, an amount paid to a seller, a payer-recognition answer, and three ordinary questions about the instrument. The engine-side `quantity` tag on the **scalar** companion (`tax.us.2025.quantity.taxable-interest`) is not user input.

Stop condition 4 holds. The rehearsal is not a blocking evidence failure because the authoritative payload was checked.

### 4. T1–T9

Every case goes through `live_coordinate_run` (`_run` at line 289) against `package.core-calculations` v34 / `published-packages` v29 / release v27. `_refusal_codes` is scoped to `tax.us.2025.obligation.acquisition.member-validation.synthesized`, not a run-wide sweep.

| Case | Honest? | What actually fails if the behavior regresses |
| --- | --- | --- |
| T1 | Yes for the includible total | Line 2b `resolved.value == BASE_BOX1`. The sibling test *name* says no row renders; the assertion requires the derived heading present. Presentation always emits declared `adjustment_rows` (`presentation_projection.py:403`). The heading-present assertion is the real one. |
| T2 | Yes for current-year arithmetic and provenance labels | Line 2b = 1700; both `"Accrued Interest"` and `"Accrued Interest (bond acquisition)"` headings. Basis consequence is not published (Track 0 deferral; no basis fact type). |
| T3 | Yes | `ACCRUED_AMOUNT_NOT_SUPPLIED` on the family's synthesized artifact, and line 2b blocked with that artifact in `missing`. An omitted scalar member plus a removed constraint would publish a zero subtraction; the test would fail. |
| T4 | Yes | `IDENTITY_ASSOCIATION_UNMATCHED` plus line 2b withheld. |
| T5 | Yes | Second box-1 item from the **same** payer (`extra_b1`). Association compares payer + tax-year. `runner.py` uses `list.count` on counterpart identities, so two statements from one payer are two matches, not a collapsed set. Code `IDENTITY_ASSOCIATION_AMBIGUOUS`; line 2b withheld. |
| T6 | **No** — see F1 | — |
| T7 | Yes | Amount correction moves line 2b; uses `assertion`, not `member-transition`. |
| T8 | Yes, recast | Plan text is "facts concern exactly one." The test records two acquisitions under one payer and asserts both subtract (2000 − 420). That is the collision test: payer-aggregate identity would supersede to one member. Load-bearing for "not payer-aggregate identity." |
| T9 | Yes for the bounded neighbours | Three recognition overrides each assert their own code on the synthesized artifact. Unanswered `periodic_in_arrears` takes the `field_absent` arm of `any(field_absent, field_not_equals)`. T9 does not re-assert line 2b withheld; that path is the same synthesized prerequisite T3 already observes. Box-3 / §135 is named as a neighbour in the domain model and is not a T9 live case; the plan's T9 is the generic unsupported-neighbour slot, filled here by the three bounded-treatment guards. |

### 5. Departures from Track 0

**Payer-level association, not statement-level.** `identity_association` components are `concerns_reported_payer` + `tax-year` against counterpart `payer` + `tax-year`. T5 and T8 as implemented are expressible at that grain. Two statements from one payer covering different obligations cannot be told apart; named in the domain model Part 5. Sound for the bounded slice.

**`subject` kept in the identity key.** Distinct from 1099-INT (payer/statement/year). Dropping it would make the purchase look like a payer attribute. Sound.

**Three recognition fields optional** (plus the amount). Track 0's all-required `value_schema` would refuse construction (`FindingModelError`) rather than name T3/T9 absences. Family `member_constraints` still require the bounded answers via `any(field_absent, field_not_equals)` and `field_absent` on the amount. The previously required-ness was preventing the states the milestone exists to name, not a load-bearing invariant worth keeping.

**Schedule B v5 `itemizes_members` only** on the canonical family. `_families_reached` for attachments treats `source_family` as `itemizes_members` and does **not** scan adjustment `subtotal_symbol` for `reads_subtotal`. Widening along `projects_from` preserves `itemizes_members`. Declaring `reads_subtotal` is `FAMILY_ACCOUNTING_UNREACHED`. Line 2b legitimately has both: `requires` the scalar subtotal (`reads_subtotal`) and `require_closed` on the scalar family (`itemizes_members`), each widened to the constrained canonical family. Sound.

### 6. Track 1 collapse

The plan itself (`Track 1` section) collapses the prototype round when Track 0 leaves one coherent reversible shape. Track 0 compared: reuse of the reported amount into the acquisition (violates T6), a rule-language join (contradicts the flat symbol table and ADR-0066 decision 4), deferring T5/T8 (plan-disallowed), and the additive `source-family.v3` `identity_association`. Parallel scalar fact types without an object-valued member cannot host the association components. Those are non-viability arguments, not inconvenience. Collapse is justified.

### 7. Published history and data safety

- `packages/schemas/tax/published.json`: one added key `attachment-rule.v9.schema.json`; no checksum changes; no removals. File SHA-256 matches the new manifest entry.
- `packages/schemas/derivation/published.json`: added `artifact-package.v26.schema.json` and `source-family.v3.schema.json` only.
- Historical `attachment-rule.v8`, `artifact-package.v25`, `package.core-calculations.v33.json` are byte-identical to `origin/main`.
- In-process `validate_package`: v33 vs `published-packages.v28.json` `ok=True` issues=0; v34 vs `published-packages.v29.json` `ok=True` issues=0.
- `git diff --check origin/main..0cac5ce9` clean.
- Identities in the new fixtures and tests are `demo.*` / `demo.oat.*`. Amounts are 2000 / 300 / 250 / 120 / 400. No absolute workstation paths in the object diff (`git diff --check` plus path grep).
- `python3 tools/envelope_scan.py --range origin/main..HEAD` — empty, exit 0 (range includes the charter commit; the object is a subset).
- `python3 tools/governance_lint.py` — conformant.

---

## Mechanical gates (rerun, not accepted)

| Check | Result |
| --- | --- |
| Full suite at `0cac5ce9` (detached worktree) | **1502 passed, 20 skipped, 4135 subtests passed**, 105s, exit 0 |
| `governance_lint.py` | conformant |
| `envelope_scan.py --range origin/main..HEAD` | clean |
| Fast lane sequential, detached `6758be16` | 6 failed, 680 passed, 8 skipped, 2716 subtests, 21.4s |
| Fast lane sequential, detached `0cac5ce9` | 6 failed, 680 passed, 8 skipped, 2731 subtests, 22.0s |

Sequential FAILED sets are identical (diff empty). Every failure is `fast-lane budget exceeded` against the 3.0s cap. No logic failure. Extra 15 subtests at T2 come from the `test_dsbs_t1_schema_citizens` v4/v5 loop, not from the live translation module (that module is selected out of the fast lane).

A contended parallel run of both lanes plus the full suite produced 18 vs 17 budget trips (T2 ⊂ T0; the extra T0 case was `test_duplicate_directories_rejected`). That matches the lead's caution that counts are timing-sensitive under `-n auto`. Sequential measurement reproduces the claimed six-failure identical sets.

---

## Box and qualitative notes

Observed report (box-1), user declaration (acquisition), derived adjustment (scalar subtotal + line 2b), and closure (affirmative-only on both new families) remain distinct. T1 closed-empty vs T3 member-with-absent-amount are different states. Association is an engine check over identity, not a user-supplied classification.

Provenance: T2 renders two Schedule B labels so the transcribed class and the derived class are not the same row. Correction of a current member is `assertion` (T7), matching `findings.py`'s rejection of a no-op `member-transition`.

No published schema was mutated. No data-boundary breach observed.

---

## What was successfully verified (reuse on repair)

- v9 / v26 / v3 are additive successors; manifests only append.
- v33 remains valid; v34 is valid.
- `_ADJUSTMENT_SURFACES` fail-closes unrecognized versions that carry adjustment slots.
- 10c `{v6,v8,v9}` does not admit the committed v8 attachments.
- Ordinary-fact `value_schema` does not ask for a tax class.
- T1, T2 (current-year), T3, T4, T5, T7, T8, T9 drive `live_coordinate_run` and would fail on the named regressions.
- Payer-level association, optional recognition fields, `subject` key, and Schedule B `itemizes_members` only are sound.
- Track 1 collapse is plan-authorized and the rejected rivals are non-viable.
- Full suite green at `0cac5ce9`. Fast-lane budget failures are pre-existing and set-identical to Track 0.

Measurement used two detached worktrees, one at each commit.

---

## Foreman triage (not the reviewer's text)

Verdict accepted. Four items repaired on top of `0cac5ce9`; none required a
design change.

- **F1 — T6 not exercised.** Repaired as the reviewer scoped it: one added case
  correcting box 1, asserting line 2b moves by the document's delta and the
  Schedule B row still cites the person's original finding. Mutation-checked.
- **The false safety argument.** The reviewer found that this milestone's
  evidence justified the de-gated Schedule B check with an invented mechanism —
  historical versions "carry empty `adjustment_rows`" — when in fact they have
  no adjustment structure and never reach the check, which is gated on schema.
  Conclusion held, reasoning did not. Corrected in place and the error left on
  the record rather than quietly rewritten.
- **The rehearsal test.** `test_the_person_supplied_no_tax_classification`
  inspected the test helper, never the committed bundle. Now reads the
  committed `value_schema` and checks the helper against it.
- **The misnamed T1 test.** Asserted the heading was present under a name
  saying no row renders. Renamed and strengthened to a zero tie-out.

Not repaired, deliberately: the reviewer's observation that T8's plan text
("facts concern exactly one obligation") is satisfied by a test that records
two acquisitions and asserts both subtract. That is the collision case — a
payer-aggregate identity would supersede to a single member — and it is the
load-bearing observation. Recast, not weakened.
