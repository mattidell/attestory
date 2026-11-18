# P0c: validated successor and strict replay complete

Source `HEAD`: `ee8ebbb4e51b7549574c7966e8b910281031b438`, branch
`milestone/plain-line-texts-2025`. Orientation matched Git. After fetch,
the branch was zero behind and seven ahead of derived ratified line
`origin/main`, with no merged PR found. Charter:
`docs/reviews/plain-line-texts/charter-p0c.md`; plan Decisions 1–6 govern.

## Validation

`p0c_validate.py` adopts P0b's exact 50 prepared successor citizens after
checking their recorded hashes, applies the wording refinements below, and
builds core v96, registry v94 and release v94 from the published v95 surface.
All 50 citizens still have exact byte-undo witnesses: reversing only their
57 declared prose properties and root versions restores their predecessors.
Values, requires, pins, guards, missing names, refusal codes, questions and
all other predecessor bytes remain unchanged.

The validator's successor table is local to its function. The evidence-only
`p0c_runtime.py` transforms that function's AST and temporarily replaces its
code on the existing function object, so imported aliases use the same
validator. It adds exactly Decision 5's v96 entry, identical to v68 except
line-2b field v7. Removing the entry restores the complete original AST;
the original code object is restored after each context. There is no file
edit, bypass, changed predicate or changed historical entry.

| Package/field under the runtime entry | Result |
| --- | --- |
| v96 / line-2b field v7 | Valid; normal successor generator validates package, registry and release |
| Same v96 / field v6 | Rejected: NOMINEE_RETURN_SUCCESSOR_GRAPH_MIXED |
| v95 / field v7 | Rejected with the same code |
| Unchanged v95 / field v6 | Valid before, during and after injection |

`p0c-validation.json` contains the exact entry, generation checksums,
controls and all successor hashes. There are no inherited inconsistencies.
The final scratch surface contains the same 50 citizens, one package, one
registry and one release; no production content is published or edited.

## Strict replay

The P0b baseline carries complete disposition rows, every publication value,
and complete real presentation models. Its core fingerprint was checked
before reuse. The scratch side uses the same live coordinator and production
saved-page renderer, with the authorized entry injected in each worker.
Nine workers (CPU count minus one) attempted all 775 recorded lists; nine
completed synthetic smoke cases were reused. No recorded answers were
repaired or changed.

| Population | Classification | Lists |
| --- | --- | ---: |
| Recorded | Expected declared sentences only | 691 |
| Recorded | Identical pre-page error | 84 |
| Recorded | Unexpected | 0 |
| Synthetic | Expected declared sentences only | 8 |
| Synthetic | Identical resolver refusal | 1 |
| Synthetic | Unexpected | 0 |

The 84 errors still consist of 82 FindingModelError, one SourceAuthorityError
and one HorizonModelError. They produce no page; matching those errors is
not evidence of computed return values for those lists. The synthetic
refusal remains ADOPTION_NONE_CURRENT.

**223,157 disposition rows and 60,114 form fields** were compared across all
699 successful pairs. The complete models, including their detail surfaces
and explanation data, are compared as well. Successor replay wall time was
**701.372 seconds**. Fixture preparation plus the worker-pool invocation was
753.987 seconds; these timings exclude the subsequent serial reclassification,
mutation controls and browser check. The prior v95 live replay took 688.08
seconds and was reused, not rerun as a second population baseline.

`p0c_compare.py` applies integrity gates before contextual labels:

- Compare row identities and multiplicity, including additions/removals;
  compare every value with JSON type precision (including booleans),
  disposition, code, missing-name list and guard result.
- Compare section/field identities and order, resolved values, dispositions,
  active codes and complete reasons/question metadata, including missing or
  extra properties.
- Compare every whole row and the whole model. The expected model is built
  only by replacing a declared old property at its supplying citizen ID,
  plus the known projected attachment-title prefix. There is no global
  sentence substitution or omission of hidden field instructions.

The only metadata canonicalization is the declared package/citizen version
transition, deterministic generated finding/publication-act/graph IDs, and
unordered pin/edge sets. Complete row and publication collections are matched
with multiplicity, independent of incidental enumeration order. Other
unplanned text and data remain in the comparison.

One additional keyed collection needs order-independent comparison:
`mortgageBorrowingExplanation.reports[].boxObservations`. Published v95 was
run with PYTHONHASHSEED 1 and 2; it returned the same box-2/box-3 identities
and values in opposite orders. The source appends from current findings at
`packages/derivation/presentation_projection.py:2941`. This is proved on
v95 in `p0c-order-check.json`, not attributed to the baseline by assumption.
Each observation's full fact type, finding ID and value, including
multiplicity and additions/removals, is still compared. Page section order
and other detail-list orders are not relaxed. The incidental box ordering
is not a wording repair or a proposed projection edit.

`p0c-replay.json` records the classification for every list. The resumable
`strict-replay-part.json` is outside the repository and records both core
fingerprints, the active wording hash, each input digest, final classifications
and complete result-file references. Its baseline reference is relative;
complete rows/models/pages remain alongside the part and in the preserved
P0b baseline directory. The private report gives those locations. Track 0
can reclassify the saved evidence without rerunning either core.

## Mutation controls

All **16 controls were rejected**, using actual successful successor pairs:

- Publication value; page value; boolean substituted for a numeric value.
- Disposition; refusal code; missing name; question identity.
- Unplanned sentence; a planned sentence inserted into the wrong property.
- Added and removed row; added and removed page field.
- Changed mortgage observation value; added and removed box observation.

`p0c-mutations.json` names the case and rejecting gate for each mutation.
The last three controls explicitly prove that order-independent observation
comparison does not hide changed data or lost/extra records.

## Wording recheck and drawn-page verification

All 57 replacements were re-read against their local 2025 sources, supplying
producer and drawn census context. **41 are retained; 16 are refined.**
Thirteen zero explanations now allow for rounding a nonzero cents amount
instead of asserting a literal zero input or an unrounded zero total. The
2025 Form 1040 instructions' Rounding Off to Whole Dollars section (printed
page 23) and the adopted producer expressions support this distinction.
The EIC clarification preserves its existing two zero branches without
attributing an application guard to a literal worksheet instruction. The
mortgage check preserves currentness, and the foreign-credit explanation
preserves an incomplete **or failed** condition rather than promising that
any settled answer suffices.

`p0c-wording.json` is the active 57-property manifest for the same 50 citizens.
`p0c-wording-check.json` records the disposition, local-source check and
census coverage for each replacement. P0b's historical manifest is untouched.
The changed replacements are listed below; all other P0b replacements stay
as recorded there.

| Property | P0b replacement | P0c replacement |
| --- | --- | --- |
| form.eic-worksheet-a.line-2#dispositions.computed_zero.explain | Worksheet A line 2 is zero under the worksheet rule for earned income below $1 or the EIC Table amount for line 1. | Worksheet A line 2 is zero because the earned income on line 1 is below $1 or gives a zero credit in the EIC Table. |
| form1040.line-25a#dispositions.computed_zero.explain | The federal income tax withholding in box 2 of your recorded Forms W-2 adds to zero. | The federal income tax withholding in box 2 of your recorded Forms W-2 totals zero after rounding. |
| form1040.line-25b#dispositions.computed_zero.explain | The recorded federal income tax withholding from Forms 1099 and SSA-1099 adds to zero. | The recorded federal income tax withholding from Forms 1099 and SSA-1099 totals zero after rounding. |
| form1040.line-25c#dispositions.computed_zero.explain | The federal income tax withholding in box 4 of your recorded Forms W-2G adds to zero. | The federal income tax withholding in box 4 of your recorded Forms W-2G totals zero after rounding. |
| form1040.line-26#dispositions.computed_zero.explain | Your estimated tax payments and amount applied from your 2024 return are zero because you entered zero for that amount. | Your estimated tax payments and amount applied from your 2024 return are zero after the amount you entered is rounded to whole dollars. |
| form1040.line-2a#dispositions.computed_zero.explain | You confirmed the tax-exempt interest records are complete, and the combined Form 1099-INT box 8 and Form 1099-DIV box 12 amount is zero. | You confirmed the tax-exempt interest records are complete, and the combined Form 1099-INT box 8 and Form 1099-DIV box 12 amount is zero after rounding. |
| form1040.line-2b#dispositions.computed_zero.explain | Your taxable interest is zero because the completed interest totals, after the recorded adjustments, add to zero. | Your taxable interest is zero after the completed interest totals and recorded adjustments are combined and rounded. |
| form1040.line-32#dispositions.computed_zero.explain | Your other payments and refundable credits total zero because the completed payment and credit amounts add to zero. | Your other payments and refundable credits round to zero when the completed payment and credit amounts are totaled. |
| form1040.line-37#dispositions.computed_zero.explain | You owe no additional tax on line 37 because your total payments are at least your total tax. | The amount still owed after comparing your total tax with your payments is zero after rounding. |
| form1040.line-3a#dispositions.computed_zero.explain | The qualified dividends in box 1b of your recorded Forms 1099-DIV add to zero, and those records are complete. | The qualified dividends in box 1b of your recorded Forms 1099-DIV total zero after rounding, and those records are complete. |
| form1040.line-3b#dispositions.computed_zero.explain | The ordinary dividends in box 1a of your recorded Forms 1099-DIV add to zero, and those records are complete. | The ordinary dividends in box 1a of your recorded Forms 1099-DIV total zero after rounding, and those records are complete. |
| form1040.line-4b#dispositions.computed_zero.explain | Your fully taxable IRA distributions total zero because none are recorded or their amounts add to zero, and those records are complete. | Your fully taxable IRA distributions total zero because none are recorded or their total rounds to zero, and those records are complete. |
| form1040.line-7a#dispositions.computed_zero.explain | Your capital gain or loss is zero after the Schedule D calculation, or the box 2a capital gain distributions add to zero when Schedule D is not required. | Your capital gain or loss is zero after the Schedule D calculation, or after rounding the box 2a capital gain distributions when Schedule D is not required. |
| schedule-d.line-13#dispositions.computed_zero.explain | Your capital gain distributions are zero because the amounts in box 2a of your recorded Forms 1099-DIV add to zero. | Your capital gain distributions are zero after the amounts in box 2a of your recorded Forms 1099-DIV are totaled and rounded. |
| schedule3.line-1#dispositions.blocked.explain | Your foreign tax credit cannot be calculated until the foreign tax records are complete and the answers about claiming the credit, the related income, the applicable dollar limit, and the tax calculation are settled. | Your foreign tax credit cannot be calculated because the required foreign tax records or answers about claiming the credit, eligible taxes and related income, the dollar limit, or the tax calculation are incomplete or do not meet the conditions for this calculation. |
| rule.effective-proceeds-support-count#notes | This check gives 1 only when exactly one recorded confirmation links the loan to how its proceeds were used and all five current answers about that use are available. It checks that the answers are complete; it does not count uses of the proceeds. | This check gives 1 only when exactly one current confirmation links the loan to how its proceeds were used and all five current answers about that use are available. It checks that the answers are complete; it does not count uses of the proceeds. |

The unmodified production page was then drawn for every one of the **699
successor pages** in Chrome 157.0.8103.79. Initial text and every ordinary
content-bearing detail panel were checked. All 57 new texts appear with
exactly their P0b census list coverage; no old flagged text remains on those
surfaces. There are zero render alerts and zero non-loopback requests.
`p0c-drawn-check.json` records each property's expected and actual coverage.
Parked support-trace/citation captions and badges are excluded, as Decisions
1–2 require. No page-owned text was redesigned.

## Recommendation and decisions for the foreman

Proceed to independent Track 0 using the active P0c manifest, runtime-entry
controls and saved comparison part. This is prototype evidence on the
recorded/synthetic population, not production publication or a green CI gate.

- Disposition the 16 wording refinements in independent review before
  publication; retain the complete-calculation and absence distinctions.
- Track 1 must make Decision 5's additive v96 graph entry in production and
  add its historical-version controls. The harness injection is not a
  deployed engine change.
- Keep the 84 unchanged pre-page errors and the observed v95 ordering variance
  visible as evidence limits. No repair of either belongs to this unit.

Local syntax, evidence consistency, data-safety and envelope checks are
recorded in `p0c-checks.json`. There were no packages/ or tests/ source edits,
governance reads, pushes, sub-agents or leftover background jobs.
