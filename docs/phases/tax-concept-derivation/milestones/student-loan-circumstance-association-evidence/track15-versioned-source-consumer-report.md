# Track 15 — versioned source and neutral consumer report

## Registered surface

The new immutable snapshot is `packages/content/tax/2025/published-packages.v34.json` (SHA-256 `78c2c9ca57ab8293a4cb3805b0049cc4fd550bbf19ea74b9bcf47a812cb7e246`). It preserves all 496 citizen and 39 package entries from v33 unchanged, then adds four citizens and one package. The release is `demo.release.sli-relationship-source.2025@v34`, stored at `packages/sample_data/student_loan_relationship_source/publication_surface/releases/demo.release.sli-relationship-source.2025.v34.json` (SHA-256 `9f545bb7320cf7dd970ac58f6aec76f95ee8bc816d4d416610ccb5fdc4466eff`). Its `package_registry_sha256` exactly matches the v34 registry bytes.

The registered citizens are the existing Track 14 candidate source bundle `tax.us.2025.sli-relationship-source@v1`, the synthetic output vocabulary `demo.tax.2025.sli-relationship-observation-vocabulary@v1`, and two diagnostic rules: `demo.rule.tax.2025.sli.financing-observation@v1` and `demo.rule.tax.2025.sli.statement-inclusion-observation@v1`. The synthetic package is `demo.tax.2025.package.sli-relationship-source-diagnostic@v2`, with package checksum `d9953bd34ac273f4f5f9f61811e803b45188958516ab2e1d9e20355ef4bf5c7e`.

The registry adds no tax result, eligibility rule, amount rule, or worksheet consumer. No existing production route selects this package. The tests select it only through an explicit, synthetic package adoption pinned to this release; registration by itself is not a production product flow.

An earlier whole-fact-type collector draft was discarded before handoff. Its result combined claims across subjects, so one claim’s lifecycle could not be tested independently. It is absent from v34. The selected rules use existing subject dispatch to publish a separate neutral observation per relationship finding while retaining that finding’s exact keys.

## Executed path and evidence

`tests/test_sli_track15_versioned_source_consumer.py` starts with the real Track 14 content loading, contribution admission, ActLog persistence, and recovered relationship projection. The test adds a second synthetic borrowing, schooling situation, and statement with equal descriptions but separate identities. One answer affirms financing and statement inclusion for each selected pair; the first answer records an unknown interest portion. No selection comes from equal labels or amounts.

The test verifies the source bundle’s canonical citizen checksum, every admitted package member’s registry checksum, the package checksum, the exact release registry digest, and the adoption’s exact release-byte checksum. `validate_package` admits the package, then the release-rooted production resolver resolves the same package from the fresh ActLog projection. The forward and reference runners produce identical results. Each result preserves the exact borrowing/schooling or statement/borrowing keys and has the complete relevant pin set: the diagnostic package adoption, its specific producer, and the one source relationship finding it observes. The two financing results and two inclusion results have distinct subject identities.

The Track 14 claim lifecycle APIs correct and withdraw financing and inclusion claims separately. Each predecessor observation disappears after correction; the successor observation uses the corrected identity. Withdrawal removes only that successor. All unaffected results retain the same finding ID, value, and pins after each operation. Correcting Form 1098-E box 1 leaves both inclusion observations unchanged. A `no` financing response and `cannot-tell` inclusion response remain answer evidence, create no claims, and add no observation.

## Applicability and composition boundary

Retracting the schooling source target leaves the Track 14 relationship finding current. The diagnostic rule still publishes its neutral observation for that finding, while `current_claim_applicability` reports `unresolved-applicability`. Thus source-target retraction does not automatically make a relationship finding unusable downstream. The guard is opt-in, and a later consumer must explicitly use it before relying on the relationship.

The amount-correction case changes the value of the named statement source while preserving its source identity. The inclusion claim and its diagnostic observation remain unchanged, and the applicability query still reports `current`. The available record cannot distinguish this amount-only correction from a same-identity change to which borrowings the statement includes. The current identity therefore does not prove that the earlier inclusion still applies. No composition change was simulated or inferred from amount, lender, label, or order; a later tax consumer needs clarification or a composition-aware source contract before relying on that relationship.

The neutral observations do not read or pin the schooling or statement source facts. They prove transport of current relationship findings and their exact identities only. They are not safe tax conclusions and do not establish source-target applicability or statement composition.

## Verification

- Focused consumer, Track 14 source, fixture-safety, and envelope-hook tests — 29 passed, 5 subtests passed.
- `python3 -m mypy packages/tax/sli_relationship_recording.py tests/test_sli_track15_versioned_source_consumer.py` — clean.
- `python3 tools/governance_lint.py` — conformant.
- `git diff --check` — clean.
- The test resolves the exact v34 release and package through the normal production resolver and validates the package member graph.
- The checksum check confirmed v33’s 496 citizen and 39 package entries are preserved in v34 without changing their checksums.
- Captured full suite, `python3 -m pytest -n auto` with `pipefail` and local socket permission from process start — **2,403 passed, 20 skipped, 0 failed; exit 0; 327.60 seconds**. Session handle: `70929`. The durable ignored log and metadata are `temp/track15/full-suite.log` and `temp/track15/full-suite-metadata.json`.
- Executable SHA-256: Python 3.14.3 `83177d8351dbd470c6072025c5d4a56162437b12110e56f2a798564e64e012e5`; pytest module entrypoint `37f8b6a3df1aef71336bce85e366db968ede153dd72ad4e60bebff79e279dc40`.
- An initial invocation was interrupted before completion because the ignored `temp/track15/` directory did not yet exist for `tee`; after creating it, the one captured full-suite run above completed successfully. The captured run was not repeated.
