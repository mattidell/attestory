# Track 3 review — The Entry Loop (synthetic), entry-field contract

- Reviewer: Reviewer
- Charter: `docs/reviews/charter-2026-07-29-entry-loop-synthetic-track3-review.md`
- Reviewed build: `23b9e1f81bc70ad7485af8d8706751b0c482bcde`
- Review range: `23b9e1f^..23b9e1f`
- Orientation: `9a6522d762ef1ac18bd624b5625c465059d60786`, on
  `milestone/entry-loop-synthetic`; 0 behind / 50 ahead of `origin/main-ui`,
  not spent.

## Verdict: **NOT READY**

The field declaration is a useful extraction from W-2 Box 1, and the record of
the evaluation is complete. It is not yet honestly a contract for *any* entry
field: the only allowed accepted-format shape is a positive currency amount,
and the runtime's stated validation contract is not the schema it publishes.

## Blocking findings

1. **`entry-field.v1` overclaims generality; its required `format` is a
   currency-format variant.**

   I tried five plausible declarations without changing the schema:

   | Proposed field | Result |
   | --- | --- |
   | 1099-INT Box 1 interest amount | Fits the currency shape. |
   | W-2 Box 13 retirement-plan checkbox | Cannot honestly fit; it needs boolean control/labels rather than currency symbol, fraction digits, positivity, and max value. |
   | Employer name/EIN | Cannot honestly fit; it needs text or identifier constraints. |
   | Date | Cannot honestly fit; it needs a date syntax/calendar constraint. |
   | Filing-status choice | Cannot honestly fit; it needs a finite choice set. |

   All five can be made *schema-valid* only by retaining the irrelevant ten-key
   currency object. That is a syntactic escape, not a declaration of the field's
   accepted format. The correct result is (b): the present `accepted_format` is
   a currency-format model that needs to be one discriminated variant among
   several (or the schema must be named and described honestly as a money-field
   contract until those variants exist). The same caution applies to
   `correction.kind`: `{"enum": ["same-field-reuse"]}` is closed in JSON
   Schema, despite the prose calling it an open enum. One observed member is
   honest; calling that closed, provisional shape open is not.

   Close this by either adding an explicit format discriminator with only the
   variants supported by evidence, or narrowing `entry-field.v1`'s stated
   scope to the single money/W-2 shape. Do not retain a generic title and
   description while every field is required to be currency.

2. **The loader and schema disagree, so `field_contract` is not guaranteed to
   be an `entry-field.v1` instance at runtime.**

   I constructed a field module with the required W-2 source, destination,
   purpose, correction, and exact existing format, but omitted `id` and set
   `version` to `not-a-version`. `_load_w2_box1_field` accepted it;
   `jsonschema.validate` rejected it because `id` is required (and would also
   reject the version pattern). The loader also accepts unknown top-level keys
   which the schema forbids.

   Conversely, I constructed a schema-valid declaration containing a different
   but valid `accepted_format`; the schema accepted it and the loader refused
   it with `entry-field-unavailable`, because the loader requires bytewise data
   equality with the separate W-2 format declaration. That latter constraint is
   sensible for this W-2 runtime, but it demonstrates that the schema is not
   the loader's contract.

   Close this by validating the parsed declaration against `entry-field.v1` at
   load time, then applying the small W-2-specific equality constraint as a
   separate constraint. Keeping the field schema outside `SchemaRegistry` is
   sound here: it validates no act, fact, or finding. That is not a reason to
   duplicate a drifting subset of its rules in Python. Loader failures do fail
   closed: all exercised malformed/declaration-mismatch paths produce only
   `entry-field-unavailable` and return no rejected declaration or value.

## Weakening findings

3. **The tests do not prove rendered derivation.** `EntryPage.svelte` does, on
   direct inspection, render all three required visible pieces from the module:
   `formatSourceLabel()`, `W2_BOX1_FIELD.source.label`, and
   `formatDestinationPurpose()`. The visible words therefore are genuinely
   derived from the same source file that feeds the API declaration, rather
   than duplicated template literals.

   `test_field_names_source_box_purpose_and_format_before_entry`, however,
   only searches source strings. It would pass if a hardcoded rendered label
   were added while the required expressions survived elsewhere in the file.
   The Chrome-driven test reaches the compiled page, but asserts only input,
   completion text, and API requests; it does not assert these labels or mutate
   a declaration to demonstrate the rendered dependency. Close this with a
   compiled/browser test that changes a fixture declaration to distinct
   synthetic text and asserts the corresponding DOM text, or an equivalent
   rendered-DOM assertion coupled to the declaration values.

4. **The seam is accurately named but was widened unnecessarily.** The
   recommendation is specific and right: canonical JSON for the field and its
   accepted format, imported/bundled by JS and parsed directly by Python. The
   implemented path instead adds a second source-language parser dependency:
   it finds `export const`, seeks the first `\n};\n`, replaces exactly one
   `"format": W2_BOX1_FORMAT`, then JSON-decodes the result. A marker or
   closing-brace-shaped comment/nested JS construct makes this brittle; an
   additional matching format property makes the count fail closed. A format
   occurrence before the selected export is outside the sliced body and is not
   substituted.

   Since the charter did not require the migration and the failures are closed,
   this is not a block by itself. But a field-only canonical JSON document could
   have avoided introducing regex substitution while leaving the pre-existing
   format seam intact. The next field contract should take the recorded JSON
   route rather than extend this parser convention again.

## Measurements and scope checks

- **Criteria from declarations:** 2.1's document, exact box, and printed label
  are structurally checkable from `field_contract`; 2.2's destination and
  non-empty purpose are structurally checkable. A person must still judge that
  the purpose is a meaningful explanation rather than filler, and must still
  see the page to assess presentation/accessibility. 2.3's guidance/validator
  consistency can be checked from the format declaration, but whether examples
  let a person state the format without guessing remains a judgement of their
  sufficiency. I agree with the record on that irreducible residue.
- **Recorded observations:** all three required evaluation observations and
  both dispositions are present in the milestone record, and are framed as
  observations: per-control rather than per-context focus indication; the
  unmeasured Tab/Shift+Tab and Enter/Space operations; the bundled accessibility
  row and conflated bar; kernel contribution-id refusal masking the local
  staleness-check coverage; and the killed-caller `launchChrome()`/`mkdtemp`
  leak.
- **Surface metadata:** independently recomputed all 943 manifest entries from
  the content tree (5,083,917 bytes); every path, byte count, and SHA-256
  matched. The manifest checksum matches the registry and adoption pin; the
  release's registry digest and the adoption's release checksum both match.
  The only additions are the field module and field schema, with the expected
  page/build and four surface-metadata updates. No criteria edit, accessibility
  repair, presentation model, ADR, maturity change, second fact family,
  residency locator, or non-synthetic data appears in the reviewed range.
- **Verification:** `python3 -m unittest tests.test_entry_loop_t1` — 31 tests
  passed in 27.155s. `python3 tools/envelope_scan.py --range main..HEAD` —
  clean (exit 0). The charter's independently reproduced full verification was
  confirmed as the governing full battery and was not re-run.

## Residual uncertainty

The most likely remaining error I cannot prove from this one-field sample is
whether `source`, `destination`, `purpose`, and correction affordance can remain
one shared core once a non-money family is built. The currency-only format
problem is proven; the rest still has only W-2 Box 1 as evidence. That is a
note for the owner, not a recommendation to draft an ADR in this track.
