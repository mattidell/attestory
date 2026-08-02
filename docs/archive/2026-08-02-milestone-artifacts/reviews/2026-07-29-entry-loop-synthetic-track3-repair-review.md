# Track 3 repair review — The Entry Loop (synthetic), entry-field contract

- Reviewer: Reviewer
- Charter: `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-29-entry-loop-synthetic-track3-repair-review.md`
- Reviewed repair: `0c9df17`
- Review range: `0c9df17^..0c9df17`
- Orientation: `08ee03d0e15c0a36fce4e45673e91ebef6d965ba` on
  `milestone/entry-loop-synthetic`; 0 behind / 54 ahead of `origin/main-ui`,
  not spent.

## Verdict: **NOT READY**

The repair narrows the prose truthfully, validates the shipped W-2 declaration
against the schema at runtime, and adds a derivation test that demonstrably
bites. Two blocking claims remain false: the schema still admits non-money
fields by attaching its irrelevant money variant, and the claimed F2 regression
coverage never reaches the validator or the equality branch it names.

## Blocking findings

1. **F1's discriminator is structural but does not make the four non-money
   declarations refuse.**

   `format.oneOf` has one `currency_amount_format` branch, and that branch
   requires `kind: "currency-amount"`; an unknown kind is rejected by the
   branch's `const`. Appending a date or choice branch later would be an
   additive, non-breaking union change for existing currency declarations. The
   new title and description are also much more honest: this is a money-field
   contract with one format variant, and `correction.kind` is now accurately
   described as closed to one observed member. The shared source/destination/
   purpose/correction core is unchanged.

   But the charter's decisive measurement does not hold. A properly-shaped
   checkbox, employer name/EIN, date, or filing-status format is refused because
   no `oneOf` branch matches its non-currency `kind`. Yet each of those four
   proposed fields, like the 1099-INT amount, is accepted if it carries the
   ten-key `currency-amount` object. I independently constructed all five;
   all validated. The schema has no relationship between source/destination
   text and `format.kind`, so it cannot tell an employer-name declaration that
   falsely claims a dollar format from a money declaration.

   Thus the old defect remains in the form the charter expressly required this
   repair to eliminate: an irrelevant currency object silently admits a
   non-money field. The narrowed prose prevents a generic overclaim but does
   not make the schema refuse those instances. Close this either by adding a
   supported semantic discriminator that makes the relationship checkable, or
   by removing the claim that the schema itself distinguishes incompatible field
   types and recording its actual, format-only boundary. Do not retain the
   milestone statement that the four fields are uncovered if their declarations
   still validate unchanged except for `kind`.

2. **The F2 regression tests are vacuous, and the separate W-2
   format-equality claim is not enforceable on this parser path.**

   The runtime implementation itself now has the right primary order:
   parse → load/check `entry-field.v1` → `validator.is_valid(contract)` →
   W-2 format comparison. The former hand-rolled field presence/type checks
   are gone. With a faithful temporary repository layout I reproduced all three
   F2 refusals (missing `id` plus invalid `version`, unknown top-level key, and
   unknown correction kind), each as only `entry-field-unavailable`; an
   unknown format kind is also refused. Missing and corrupt schema files fail
   closed with the same generic error. No rejected declaration, value, schema
   path, response, log, or console output is exposed. `jsonschema` was already
   a declared dependency and used by three kernel modules; no fallback was
   added.

   The new tests do not establish those facts. `_write_field_declaration()`
   writes `W2_BOX1_FORMAT};\n`, whereas the loader requires a `\n};\n` closing
   marker; it also writes no schema at the temporary root. Each test therefore
   passes on an earlier marker/schema-unavailable failure even if schema
   validation is deleted. The purported different-format case shares both
   problems. If those were repaired, it would still not exercise the equality
   branch: the loader substitutes the caller-supplied `format_spec` into the
   only accepted `"format": W2_BOX1_FORMAT` expression, then compares the
   resulting value to that same `format_spec`. Equality is necessarily true on
   every parseable field declaration; a literal different format fails earlier
   at the regex-count guard rather than for the documented runtime reason.

   This leaves a false coverage and behaviour claim in the milestone record:
   the F2 regression does not guard schema validation or separately prove
   format equality. Close it with faithful fixtures that contain the schema and
   parser-valid field source, plus either an equality constraint that can be
   false on a parser-valid declaration or an honest removal of the tautological
   constraint and its claimed test. The present implementation's fail-closed
   behaviour is good evidence, but it is not protected by the tests said to
   protect it.

## Measurements that hold

- **F1 mechanics:** removing `format.kind` or using an unknown kind is rejected
  by the schema. The one-member `oneOf` is a genuine discriminator, not merely
  a decorative property; its limitation is the absent semantic link described
  in Finding 1.
- **F2 runtime and schema availability:** the schema is read from the repository
  runtime root under `packages/schemas/entry/`. That root is already required
  by `SyntheticW2EntryRuntime` for source and content; no supported runtime path
  omits it. An unreadable, invalid-JSON, or schema-invalid file raises only
  `entry-field-unavailable`, so validation is never skipped. The W-2 equality
  check is textually after schema validation and includes `kind` because it
  compares the complete dict, though, as noted, this path supplies both sides
  from the same object.
- **F3 derivation proof:** `RenderedFieldDerivation` passed locally. I then
  copied the surface, changed the declaration to distinct synthetic text, and
  restored hardcoded original labels/purpose in the copied Svelte template. The
  helper exited 0 only after reaching the real served DOM, reporting
  `{"present": false, "absent": false}`; the Python assertion for
  `{"present": true, "absent": true}` consequently failed. This catches the
  defect the former source-string test missed. The helper cannot succeed without
  loading the page and finding the input; launch, navigation, selector, or DOM
  evaluation failures throw/catch and produce nonzero. It is gated exactly like
  the existing compiled-client test. CI installs neither the vendored tree nor
  a browser/Node toolchain, so it is skipped there; F3 is reproducible evidence
  on the equipped machine, not a continuously executed CI check.
- **Data safety of F3:** the helper invokes `launchChrome(null)`, uses only
  synthetic declaration text and temporary build output, and emits a fixed
  generic failure token. It adds no residency locator or profile path to an
  argument, URL, output, or failure text. Normal failure reaches the helper's
  disposal and the test's temporary-directory cleanup. An externally killed
  helper retains the already-recorded `launchChrome()` orphan/profile risk; this
  test introduces no different leak mechanism, but it cannot claim to close
  that inherited timeout case.
- **Format regression and seam:** adding `kind` changes neither accepted forms
  (`90000`, comma grouping, optional currency prefix) nor the examined numeric
  refusals; the three Track 2d format/parser tests pass. The parser retains one
  export marker and one regex substitution; `kind` travels inside the existing
  injected format dict and adds no parsing path.
- **Metadata and scope:** independently recomputed all 943 manifest entries;
  every path, byte count, and SHA-256 matches, for 5,083,946 bytes. The 29-byte
  increase from 5,083,917 is exactly the added `kind` line in
  `w2-box1-format.js`; manifest, registry, release, and adoption pins all
  match. The reviewed range makes no criteria change, accessibility repair,
  presentation model, ADR, maturity movement, second fact family, residency
  locator, or non-synthetic data change. `python3 tools/envelope_scan.py
  --range main..HEAD` completed cleanly.

## Residual uncertainty

Even after the money-format boundary is stated honestly, a second field family
may show that the apparently shared source/destination/purpose/correction core
needs an explicit semantic control/value type. One W-2 money field cannot prove
that either way. This is a note for the owner, not a request to draft an ADR in
this track.
