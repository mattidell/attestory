# Examination: Ordinary Input Mapping (Seam 6)

## Starting condition

The charter was drafted describing this as a repair of an existing mapper
(`packages/tax/obligation_acquisition_mapping.py`,
`tests/test_obligation_acquisition_translation.py`). On this branch — cut
from `milestone/document-ordinary-fact-translation-seams`, itself cut from
`origin/main` before the prior single-track attempt — neither file exists.
The prior attempt's edits live only uncommitted in a sibling worktree on
`milestone/document-ordinary-fact-translation` (NOT-READY, reference
evidence only) and were not read to produce this module. **This was
therefore a first build against the charter's five requirements, not a
repair of, or diff against, prior code.** The charter is corrected
(2026-08-28, post eligibility-review R1) to say so plainly; the "repair"
framing was a documentation defect, not a description of what happened,
though it did not change the routing conclusion (direct-build, no rival).

## What the module does

`packages/tax/obligation_acquisition_mapping.py` maps one **structured**
ordinary-language answer set — never free text — about a bond (or other
interest-bearing obligation) acquisition and an accrued-interest payment to
the seller, into one canonical circumstance fact.

- **Subject and scope agree.** The docstring states the one circumstance
  mapped (acquisition between interest dates + accrued interest paid to
  seller) and nothing else. `map_ordinary_acquisition_answers` emits exactly
  one `finding.v2` per call; nothing about disposition, premium, or market
  discount is ever produced.
- **Structured input only.** `ORDINARY_ANSWERS_SCHEMA` is a closed JSON
  Schema (`additionalProperties: false`) over six named ordinary fields.
  `validate_ordinary_answers` fails closed on anything else — an extra key,
  a missing key, or a malformed value — before a fact is ever built.
- **Contribution admission validates the output.** The real, general
  manual-entry boundary — `packages.kernel.contribution.apply_contribution_batch`
  (ADR-0032 D2) — is what makes the emitted finding real. This module builds
  the same `contribution`/`assertion` acts any other manual-entry fact uses
  and calls that applicator; it does not reimplement or shortcut admission.
  `TestContributionAdmissionValidatesOutput` proves both the positive path
  and that admission rejects a well-formed-looking finding whose evidence
  does not match its contribution.
- **Only canonical circumstance facts.** The emitted `value` names exactly
  five fields (below) — no tax conclusion, adjustment, or election.
- **No tax classification ever requested or supplied.** `ORDINARY_QUESTIONS`
  is asserted, by test, to contain none of: taxable, tax treatment,
  adjustment, deduct, schedule b, election, classification, exclusion,
  basis. The schema's property set is asserted to contain no field naming
  treatment/classification/election/adjustment — a structural guarantee, not
  a review convention.

## Worked example

Ordinary answers (all fields a person can state from memory of their own
purchase, none requiring tax knowledge):

```json
{
  "payer_name": "Demo Municipal Authority",
  "obligation_description": "10-year municipal bond, series demo-2025",
  "obligation_reference": "demo-cusip-000111222",
  "acquisition_date": "2025-03-14",
  "accrued_interest_paid_to_seller": 42.5,
  "currency": "USD",
  "tax_year": 2025
}
```

`map_ordinary_acquisition_answers` emits:

```json
{
  "schema": "finding.v2",
  "id": "demo.finding.acq-a",
  "fact_id": "demo.tax.obligation-acquisition-circumstance|payer=Demo Municipal Authority,reference=demo-cusip-000111222,tax-year=2025",
  "value": {
    "obligation": {
      "payer_name": "Demo Municipal Authority",
      "description": "10-year municipal bond, series demo-2025",
      "reference": "demo-cusip-000111222"
    },
    "acquisition_date": "2025-03-14",
    "accrued_interest_paid_to_seller": 42.5,
    "currency": "USD",
    "tax_year": 2025
  },
  "basis": "attested",
  "evidence_ids": ["demo.evidence.acq-a"],
  "contribution_id": "demo.contribution.acq-a"
}
```

Five value fields, named: `obligation` (itself `payer_name`, `description`,
`reference`), `acquisition_date`, `accrued_interest_paid_to_seller`,
`currency`, `tax_year`. `basis` is `"attested"` — what the person stated
about their own circumstance — distinct from `"documentary"` (what a report
said), matching the milestone's separation of source report from
user-supplied circumstance.

`contribute_ordinary_acquisition` then runs this finding through
`apply_contribution_batch` exactly as any other manual-entry contribution:
a `contribution` act anchors the evidence, an `assertion` act carries the
`finding.v2`, and the applicator writes the Article-14 started/terminal
process account. `tests/test_obligation_acquisition_translation.py` runs
this end to end and asserts the terminal record reaches `"completed"`.

## Fact-lattice identity: a scoped simplification, named honestly

A kernel literal identity key enumerates its admissible values at
declaration time (`fact-type.v1`). Rather than pre-deciding an
entity/association shape that Seam 1 and Seam 2 have not yet selected, this
module's own admission fixture (`build_obligation_acquisition_bundle`)
declares a one-off literal domain equal to exactly the payer, reference, and
tax year the person just supplied. This is enough to prove this seam's
mapping-and-admission path through the real contribution boundary; it is
**not** a claim about the identity/association mechanism Seam 1–3 will
select for production, and a later integration is expected to adopt
whatever richer vocabulary those seams choose instead of this fixture
bundle.

**Explicit disposability statement (eligibility review R1, condition 2):**
`build_obligation_acquisition_bundle` is a disposable test convenience: it
does not ship to production and is not a pre-selected answer to Seam 1/2's
still-open canonical identity design. It enumerates one instance's literal
values per call and cannot represent a second obligation from the same
payer without a fresh bundle, so it is not a producible vocabulary
declaration by construction. Only `map_ordinary_acquisition_answers`,
`validate_ordinary_answers`, `build_ordinary_acquisition_contribution`, and
`contribute_ordinary_acquisition` are production-adoption candidates,
contingent on Seam 1/2's identity-key kind selection; the production
fact-type/bundle declaration is Seam 1/2's output, not Seam 6's. The
module's own docstring on `build_obligation_acquisition_bundle` now states
this explicitly, not only this document.

## Repair round (post adversary-r1 and eligibility-r1)

Three numeric/date-boundary gaps the adversarial review found under attack
have been closed:

1. **`inf`/`nan` for `accrued_interest_paid_to_seller` (decision-blocking).**
   JSON Schema's `"type": "number"` does not exclude non-finite values, so
   `inf`/`nan` previously passed `validate_ordinary_answers` and were
   admitted end to end as `"completed"` — fail-open, violating the charter's
   fail-closed requirement. `validate_ordinary_answers` now calls
   `_reject_non_finite_numbers` first, walking every numeric schema
   property and raising `OrdinaryInputError` before any act is built.
   Regression tests (`test_infinite_accrued_amount_is_rejected_before_admission`,
   `test_nan_accrued_amount_is_rejected_before_admission`) assert rejection
   at `validate_ordinary_answers` and that no contribution/finding is ever
   recorded — proven pre-admission, not post-hoc.
2. **Whitespace-only `payer_name` (lower severity).** `minLength: 1` counted
   whitespace as content; the schema now also requires `"pattern": r"\S"`.
   Regression test: `test_whitespace_only_payer_name_is_rejected`.
3. **Future `acquisition_date` (lower severity) — decided, not left open.**
   This circumstance is inherently retrospective ("I acquired ... and paid
   the seller the interest that had already accrued"); no legitimate
   in-scope scenario has this not yet having happened, so a future date is
   an invalid instance, not merely an implausible one.
   `validate_ordinary_answers` now also calls
   `_reject_future_acquisition_date`, rejecting any date later than today.
   Regression test: `test_future_acquisition_date_is_rejected`.

**Deliberately left as-is:** the double-submission/dedup gap (adversary-r1
§5 — fresh-id resubmission produces two live findings sharing one `fact_id`
under the fixture's `"free"` supersession policy). Already correctly named
above ("Fact-lattice identity") as a disclosed scope limitation belonging to
Seams 1–3's identity/association and correction design, not a defect in
this seam's admission-validation guarantee; not touched here.

## What was NOT built (correctly out of this seam's scope)

- Association between this circumstance and a reported interest item (Seam
  2), and the amount-cannot-exceed-report constraint (Seam 3).
- Any tax-rule derivation of the accrued-interest treatment (Seam 5).
- A rival builder — the charter and milestone plan both name this as
  direct-build with no genuine second stance.
