# Track 6b — saved reader build report

## Delivered

`presentation_projection.py` now adds an optional `calculationView` only when a resolved v12 statement-amount role is present. The view retains exact keyed findings, producer identity, disposition code/missing data, pins, values, current structured statement labels, source-finding fact type identity/title, parameter declarations, claims, and attached responsibilities. A blocked amount preserves its recorded code; a published amount cannot carry blocked fields. Claim labels come from a current non-shared entity key on that claim fact when evidence has no label. `{statement}` is rendered from the current recorded statement label before saving.

The calculation view remains marked `integrated: false`. The presentation validator checks closed shape, internal consistency, unsafe values, required outcome axes, and that a published conclusion has the declared bare/no-whole-disqualifier posture. Run-to-projection equality is exercised separately while the run evidence is available.

The disposable generator clones the production v34 package/publication surface, appends the synthetic v12 reader rules and declarations, reseals the temporary package, and runs one `live_coordinate_run` per scenario. Each presentation file comes directly from the coordinator writer. The generator discards the live outcome, reloads the saved file, and validates it before returning. No product tax content or published schema was edited.

## Saved outcomes and evidence

Generated ignored files:

- [`ordinary/presentation.json`](../../../../../temp/track6b/ordinary/presentation.json): S1 amount 400.0, S2 amount 700.0, both no-link/bare, three responsibility findings each, and the rule-owned line note. Schedule 1 line 21 remains 1100.
- [`adverse/presentation.json`](../../../../../temp/track6b/adverse/presentation.json): the S1 vehicle claim classifies to 1 and makes its whole-amount-disqualifier count 1; S1 amount is 0 with no responsibility or note. S2 remains 700. Schedule 1 line 21 remains 1100.
- [`unresolved/presentation.json`](../../../../../temp/track6b/unresolved/presentation.json): the untreated S1 claim blocks the scope count with `DEPENDENCY_INVALID` and blocks amount/conclusion with `DEPENDENCY_ABSENT`; S1 has no value, responsibility, or note. S2 remains 700. Schedule 1 line 21 remains 1100.

Each file has one run id and two statement groups. The live fidelity test compares amount/axis/claim/responsibility publications and disposition rows to the projected file, checks exact rule and parameter identities, compares the line-21 finding to the same run’s publication, drops live objects, and reopens the saved JSON. It asserts the entire S2 group is byte-stable across the three cases.

The same validated package graph is marshalled once per ordinary/adverse/unresolved case and run through both `runner.run` and `run_reference`. Their keyed reader disposition, value, pin, code, and missing snapshots match for S1 and S2. The live controls also verify tuition maps to classifier 0 while retaining S1’s limited responsibility treatment, and a linked S1 becomes `linked` without changing S2’s bare route. `ExperimentalLinkCount.test_missing_subject_identity_blocks_only_that_statement` and `test_present_link_row_without_identity_keys_blocks` in `tests/derivation/test_experimental_link_count.py` cover missing subject identity and a present link with unavailable identity keys in both runners. The Track 6b linked-selection live control covers S1 selection separately. Existing cross-category copy regressions remain green.

The browser harness observation is [`harness-observation-final.json`](../../../../../temp/track6b/harness-observation-final.json) (35 criteria passed). It was captured from the saved files after generation and reload. The HTML remains a thin synthetic demonstration; the candidate sentences and presentation are provisional.

## Verification

- `pytest tests/test_track6b_saved_model_fidelity.py tests/derivation/test_calculation_view_projection.py tests/test_sli_saved_reader_page.py tests/derivation/test_experimental_link_count.py tests/test_f1098e_student_loan_interest_agi_track6.py -q` — 29 passed.
- `pytest tests/test_sli_circumstance_association_a4_pass2.py::CrossCategoryCopyDoesNotBecomeDestinationCategory tests/derivation/test_experimental_link_count.py::ExperimentalLinkCount -q` — 11 passed.
- `python -m mypy packages/derivation/presentation_projection.py tests/derivation/test_calculation_view_projection.py tests/test_track6b_saved_model_fidelity.py` — success.
- `python3 tools/governance_lint.py` — conformant; `git diff --check` — clean.
- `pytest` — **2363 passed, 20 skipped in 127.00s**. Fresh final-tree capture: [`full-suite-final.log`](../../../../../temp/track6b/full-suite-final.log). An earlier sandbox-restricted diagnostic run had loopback/browser permission failures; it is not the final result. The final run used approved loopback access and passed.
- Reproduction: `python3 tools/presentation_harness/examples/generate_track6b_saved_presentations.py`; then `node tools/presentation_harness/run.mjs --manifest tools/presentation_harness/examples/manifests/statement-calculation-track6b.v1.json --observation-out temp/track6b/harness-observation-final.json`.

## Limits

This demonstrates a bounded synthetic reader and the existing worksheet result together in one live run. It does not change the worksheet, determine complete student-loan eligibility, integrate the reader into the product page, or settle final wording/layout. G2 remains open, and ADR 0076 Part 3 remains outside this track.

## Bounded reader repair after independent review

### Implemented

The experimental saved-file page now gives four distinct readings: supplied inputs, selected assumptions and copied rule-stated basis, conclusions, and filer responsibilities. It keeps technical producer/version identities, original dispositions, values, pins, codes, and missing details in keyboard-accessible named evidence disclosures. It renders saved text through text nodes and preserves the existing worksheet as a separate line-21 section. No generator, projector, execution rule, saved-model shape, product page, or worksheet behavior changed.

### Demonstrated

The browser regression checks the three generated `presentation.json` files directly. It verified ordinary/adverse/unresolved first readings, exact source and line-note values, S1/S2 separation, S2 reading and evidence stability, named producer/pin evidence, keyboard disclosure access, and worksheet values. The pre-repair page failed the strengthened browser checks; the retained negative capture is `temp/track6b/reader-repair/pre-repair-final/browser-check.json`, with command summary `temp/track6b/reader-repair/pre-repair-final.stdout.json` and stderr log `temp/track6b/reader-repair/pre-repair-final.stderr.log`. The final positive observation is `temp/track6b/reader-repair/final/browser-check.json`; its command summary is `temp/track6b/reader-repair/final/browser-check.stdout.json` (passed, zero failures). Collapsed first-reading screenshots are `ordinary-collapsed.png`, `adverse-collapsed.png`, and `unresolved-collapsed.png` under `temp/track6b/reader-repair/final/`; opened unresolved evidence is `unresolved-open-evidence.png` in that directory.

| Saved S1 case | Supplied | Why the saved amount has this result | Recorded responsibility treatment |
| --- | --- | --- | --- |
| Ordinary | Reported interest 400 | No link or statement-wide claim was selected. The selected zero defaults leave the amount at 400; the copied rule basis states the limited favourable posture. | Three published candidate statements identify the institution, credential and half-time conditions that this view does not check. |
| Adverse | Reported interest 400 and a vehicle claim | The saved classifier and scope result select the synthetic whole-amount treatment, giving zero. | The favourable conclusion is inapplicable; no responsibility wording was published. |
| Unresolved | Reported interest 400 and a demo-untreated claim | The classifier blocks, then scope and dependent outcomes block. No amount is available. The original classifier code and empty missing list do not supply a more specific cause. | No responsibility wording was published; the recorded producer diagnostics remain inspectable. |

S2 retains 700, its readings and displayed evidence across all three cases. The
separate actual worksheet deduction is 1100 in every case. Foreman review
inspected the three first-reading captures and opened blocked classifier
capture, compared displayed S2 readings with the saved data, and verified the
three saved presentation files are byte-for-byte unchanged. The generator,
projector, product page and unrelated `package-lock.json` are also unchanged.

### Verification and limits

Verification for this repair:

- The updated manifest harness passed 41 case/criterion checks; capture: `temp/track6b/reader-repair/final/harness-observation.json`.
- `python3 -m pytest tests/test_sli_saved_reader_page.py -q` — 5 passed.
- `python3 -m mypy tests/test_sli_saved_reader_page.py` — no issues.
- `python3 tools/governance_lint.py` — conformant; `git diff --check` — clean.
- One full `python3 -m pytest` run, session 71005 — **2364 passed, 20 skipped in 136.52s**. Captured at `temp/track6b/reader-repair/final/full-suite.stdout.log`; stderr is empty. The full run includes the repository envelope/data-safety tests, including `tests/test_envelope_hooks.py`.

The demonstration establishes automated recovery of saved-model readings and evidence, and a keyboard-operable disclosure path in the tested browser. It does not establish human comprehension, owner acceptance of the provisional wording, complete eligibility, or product integration. The page remains experimental and uses only the bounded synthetic cases.

Reproduce the saved-file browser checks after generating the three cases with
the existing generator command above:

```sh
node tools/presentation_harness/examples/verify_track6b_reader.mjs --output-dir temp/track6b/reader-repair/reproduced
```

The verifier reads only the saved files; it does not execute the engine.
Local checks are recorded evidence. CI remains the merge gate of record; this
repair has not been pushed or merged. G2 and ADR 0076 Part 3 remain open.
