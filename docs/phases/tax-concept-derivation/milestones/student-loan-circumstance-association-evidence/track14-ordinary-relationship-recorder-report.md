# Track 14 — ordinary relationship recorder handoff

## Delivered source slice

The candidate content declaration is `tax.us.2025.sli-relationship-source@v1`.
It declares a schooling situation keyed by period, institution and programme;
an affirmative financing claim keyed by that situation and an opaque borrowing
reference; and an affirmative statement-inclusion claim keyed by a specific
1098-E source and borrowing. Schooling descriptions are ordinary strings. They
are values, not identity keys. The identifiers in tests are synthetic fixture
handles and do not define person-facing or production identity. The bundle is
not published or registered.

Person-facing recognition cards/selection and ordinary schooling or statement
intake are outside this recorder: tests create those current subjects through
generic synthetic source admission, while the relationship API validates the
selected internal handles. The bundle is schema-validated and adopted directly
by Track 14 tests only. Production resolver admission and publication are
deferred to a later consumer/publication unit; no production resolver or
downstream consumer run is claimed.

One submission preserves both separate answers and may admit both claims
through `apply_contribution_batch`. Only `yes` creates a claim. `no`,
`cannot-tell` and `unanswered` remain in the submitted answer evidence.
`interest_portion_response: unknown` leaves an affirmative inclusion definite.
Caller-supplied actor and time are required. The durable entry points write
through `ActLog`; a fresh `ActLog` instance recovers the claims, evidence and
current projection.

## Exercised lifecycle and boundaries

The focused tests cover a single save affirming both claims, a known financing
claim with uncertain inclusion, an unanswered/uncertain-only answer, unresolved
equal-looking subjects, two borrowings financing one schooling situation, a
distinct equal-described schooling situation, and two distinct statements.
They correct and withdraw financing and statement-inclusion claims separately
and assert that the other claim retains its finding identity and standing.

A schooling value correction updates the current source value while leaving
the still-applicable financing assertion current. Retracting that schooling
target leaves the claim history intact and makes its applicability
`unresolved-applicability`. A statement box-1 amount correction preserves both
relationship findings and reports the inclusion as current. Retracting the
named statement source leaves both claim histories present, marks only the
inclusion claim unresolved, and leaves financing current.

`current_claim_applicability` is an **opt-in source-use guard**. It reports
whether each current claim's exact source fact is current. It is not wired into
all consumers, does not itself hold a result, and does not automatically guard
any downstream tax use. It also cannot discern a same-key statement
composition change: it checks that the named statement source identity remains
current, not whether that statement now includes the same borrowings. A
consumer must not treat `current` from this check as proof that statement
composition or claim applicability is safe for tax use.

An unresolved-answer test saves two equal-looking borrowing, schooling and
statement candidates in recognition context with no selected subject, then
reopens the ActLog and confirms the candidates and `cannot-tell`/`unanswered`
responses remain inspectable without either claim. A separate `no` response
test confirms negative answers remain recorded without creating affirmative
relationship findings; they are answers, not tax results.

## Consumer evidence ceiling

This track did not exercise the charter-permitted test-local neutral consumer
through both runners. That is an unexecuted optional evidence path, not a
capability gap or a charter prohibition. Consequently there are no actual
computation pins or consumed source sets for these relationships in this
handoff. The executed evidence ceiling is contribution admission, durable
ActLog recovery and current source projection, including the explicit
applicability query above. A production tax consumer, saved tax presentation,
tax result, G2 pass, reader acceptance and worksheet integration remain
deferred.

Borrowing entity succession has separate kernel currency behavior: when the
borrowing named by a relationship claim is superseded, the claim findings leave
the current projection through their individuation keys, while remaining in
history. The applicability query enumerates current claims, so those displaced
claims do not appear as unresolved rows.

## Verification

- `pytest tests/test_sli_relationship_recording.py tests/test_kernel_fixtures.py -q` — 15 passed, 5 subtests passed.
- `python3 -m mypy packages/tax/sli_relationship_recording.py tests/test_sli_relationship_recording.py` — clean.
- `python3 tools/governance_lint.py` — conformant.
- `tests/test_kernel_fixtures.py` passed as the focused synthetic-fixture safety check.
- The Track 14 bundle and each nested fact type validate through the workspace schema registry and are adopted directly in Track 14 tests. The bundle has no published citizen checksum.
- `git diff --check` — clean.
- First full-suite run before the registry repair: **104 failed, 2301 passed, 20 skipped; exit 1; 317.78s**. Its log and metadata remain `temp/track14/full-suite.log` and `temp/track14/full-suite-metadata.txt`; session handle `24280`. It reported widespread `REGISTRY_CHECKSUM_MISMATCH` refusals because the then-modified published registry no longer matched release attestations. This run was not repeated with the same inputs.
- The published registry has since been restored byte-for-byte from committed HEAD. The representative formerly failing test, `tests/test_dsbs_t2_coordinator.py::Lines3a3bPublication::test_both_boxes_present_publish_their_own_totals`, passed (1 passed in 3.10s).
- Fresh full suite after the registry repair, one captured run with local socket access: **2401 passed, 20 skipped; exit 0; 283.09s**. The durable log is `temp/track14/full-suite-after-registry-repair.log`, metadata is `temp/track14/full-suite-after-registry-repair-metadata.txt`, and the captured session handle was `58338`.
- Executable hashes for both full-suite captures: Python 3.14.3 SHA-256 `83177d8351dbd470c6072025c5d4a56162437b12110e56f2a798564e64e012e5`; pytest 9.1.1 SHA-256 `ff99a092615ea26925d2cab494fa7504439b7a46fe2b8e8cfb599d43bb73de1a`. Local executable paths are retained in the ignored capture metadata.

The before/after results establish that restoring the published registry bytes
removed the release-attestation mismatch failures. The unregistered Track 14
bundle remains a candidate for a later production resolver and publication
unit.
