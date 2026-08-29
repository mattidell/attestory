# Examination: Ordinary Input Mapping (Seam 6)

## Starting condition

The charter describes this as a repair of an existing mapper
(`packages/tax/obligation_acquisition_mapping.py`,
`tests/test_obligation_acquisition_translation.py`). On this branch — cut
from `milestone/document-ordinary-fact-translation-seams`, itself cut from
`origin/main` before the prior single-track attempt — neither file exists.
The prior attempt's edits live only uncommitted in a sibling worktree on
`milestone/document-ordinary-fact-translation` (NOT-READY, reference
evidence only) and were not read to produce this module. This is therefore a
first build against the charter's five requirements, not a diff against
prior code.

## What the module does

`packages/tax/obligation_acquisition_mapping.py` maps one **structured**
ordinary-language answer set — never free text — about a bond (or other
interest-bearing obligation) acquisition and an accrued-interest payment to
the seller, into one canonical circumstance fact.

- **Subject and scope agree.** The module's docstring states the one
  circumstance it maps (acquisition between interest dates + accrued
  interest paid to seller) and nothing else. `map_ordinary_acquisition_answers`
  emits exactly one `finding.v2` per call; nothing about disposition,
  premium, or market discount is ever produced.
- **Structured input only.** `ORDINARY_ANSWERS_SCHEMA` is a closed JSON
  Schema (`additionalProperties: false`) over six named ordinary fields.
  `validate_ordinary_answers` fails closed on anything else — an extra key,
  a missing key, or a malformed value — before a fact is ever built.
- **Contribution admission validates the output.** The real, general
  manual-entry boundary — `packages.kernel.contribution.apply_contribution_batch`
  (ADR-0032 D2) — is what makes the emitted finding real. This module builds
  the same `contribution` / `assertion` acts any other manual-entry fact
  uses (`build_ordinary_acquisition_contribution`) and calls that applicator
  (`contribute_ordinary_acquisition`); it does not reimplement or shortcut
  admission. `tests/test_obligation_acquisition_translation.py::TestContributionAdmissionValidatesOutput`
  proves both the positive path and that admission still rejects a
  well-formed-looking finding whose evidence does not match its
  contribution — the boundary genuinely checks, it does not rubber-stamp.
- **Only canonical circumstance facts.** The emitted `value` names exactly
  five fields (below) — no tax conclusion, adjustment, or election.
- **No tax classification ever requested or supplied.** The six-question
  user-facing surface (`ORDINARY_QUESTIONS`) is asserted, by test, to
  contain none of: taxable, tax treatment, adjustment, deduct, schedule b,
  election, classification, exclusion, basis. The schema's property set is
  asserted to contain no field naming treatment/classification/election/
  adjustment. This is a structural guarantee (closed schema), not a review
  convention.

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

## What was NOT built (correctly out of this seam's scope)

- Association between this circumstance and a reported interest item (Seam
  2), and the amount-cannot-exceed-report constraint (Seam 3).
- Any tax-rule derivation of the accrued-interest treatment (Seam 5).
- A rival builder — the charter and milestone plan both name this as
  direct-build with no genuine second stance.
