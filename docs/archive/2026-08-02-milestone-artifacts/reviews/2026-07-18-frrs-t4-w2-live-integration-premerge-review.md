# First Real Return Slice — Track 4 W-2 Closure and Live Integration — Pre-Merge Review

Reviewer: owner-authorized, author-independent pre-merge reviewer. Date:
2026-07-18. Branch: `track/frrs-t4-w2-closure-live-integration`. Reviewed
implementation delta: `6858ad7` → `c39a79b` (one grouped Track-4 commit).
Charters: `docs/reviews/charter-2026-07-18-frrs-t4-w2-live-integration.md`
and `docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t4-w2-live-integration-premerge-review.md`.
Contracts reviewed: ADR-0014, ADR-0027, ADR-0028, ADR-0031, ADR-0032,
ADR-0033, and the Track-3 pre-merge/F1 repair reviews. This review does not
modify implementation, contracts, schemas, fixtures, or the unrelated untracked
Track-1 review record.

## Verdict

**Not merge-ready. Three blocking findings.** The synthetic core-v2 resolver
and most W-2 closure mechanisms work, and the regression/validation suites are
green. However, Track 4 claims to install the ADR-0031 independent,
integrity-checked envelope gate and a safe capability-gated coordinator. The
gate can be hand-forged, and an invalid output path commits a completed live-run
account before it refuses the path. Separately, the newly published W-2 wage
fact is pinned to the taxable-interest quantity, contrary to the charter's
required wages quantity. These are production-boundary/content correctness
defects, not merely missing test coverage.

## Required measurements and evidence

1. **RG-1 and immutable content — passed.** `core-calculations@v2` resolves
   with `validation.ok == True`; the historical v1 adoption returns
   `HARD_GATE_REFUSED` with exactly eight contained issues; the generator
   reproduces committed core-v2 content and Track-3 release/adoption bytes.
   No published v1 citizen is changed in the reviewed delta.
2. **ADR-0014 closure — mostly passed, with F3 below.** The focused probe
   verified empty only on one current literal `true`; absent, false, displaced,
   non-boolean, and duplicate closure evidence all block. Present wages
   aggregate without a closure pin. Mapping and family are resolver-adopted
   package members and mapping fact pins are exact v2 pins.
3. **ADR-0027/0028 ledger — substantially present.** The v2 package validates
   role canon, form-field producers, versioned bundles/facts, exact mapping
   edges, composition obligations/binding, quantity validation, and the
   focused reject/non-trigger coverage. The closing note explicitly lists the
   ADR-0033 §4 rows and retains historical-v1 migration as deferred.
4. **Track-3 residuals — passed.** The physical-layout probe adds a nested
   duplicate of an exact member and preserves the resolved graph. Member-byte
   substitution now requires `MEMBER_ABSENT_OR_MISMATCH`. The marshalling token
   constructor rejects an arbitrary seal.
5. **Scope and safety — passed.** The delta contains no personal data,
   workspace locator, real-run report, UI/OCR/e-file/coverage expansion, new
   ADR, or changed v1 bytes. Full-delta scans for absolute local-path markers,
   ignored personal-data locations, and SSN-shaped values found no matches.

## Independent counter-probes

- A hand-created `InstalledEnvelopeGuards` with the public workspace path and
  `sha256("ADR-0031-envelope-gate:" + path)` is accepted by
  `LiveWorkspace.guarded_push`. It was never returned by
  `install_envelope_guards`.
- Calling `live_coordinate_run(..., output_name="../../escape.json")` raises
  `ResidencyViolation`, but only after `execute_and_record_marshaled` has
  written two records (`started` and `completed`) under `L/records`; no declared
  output exists. Thus a rejected path manufactures a completed run account.
- `w2.bundle.v2.json` assigns W-2 box-1 wages
  `{"id": "tax.us.2025.quantity.taxable-interest", "version": "v1"}`.
  The declared vocabulary itself distinguishes `taxable-interest` and `wages`.

## Findings

### F1 — The purported installed envelope guard is publicly forgeable

**Classification: blocking.**

`packages/derivation/live_workspace.py:80-116` exposes a public frozen
dataclass whose integrity value is a deterministic SHA-256 of the public
workspace path. A caller can instantiate a matching token directly and pass it
to `guarded_commit` or `guarded_push`; `_require_installed_guard` accepts it.
That is not an integrity-checked, installed hook/guarded-transport capability,
and it cannot establish the charter's required refusal of an uninstalled guard
or raw `--no-verify`/transport bypass. The coordinator's empty calls to these
methods do not install a Git hook, bind remote credentials, or scan an outgoing
envelope.

Repair direction: make the gate unforgeable outside installation and bind it to
real independent commit/push entrypoints that scan the full envelope before any
publication. Add executed forged-token, tampered-token, raw-transport, and
`--no-verify` kill tests.

### F2 — Output-path refusal writes a completed run record before refusing

**Classification: blocking.**

`packages/derivation/live.py:105-118` opens the record stream and calls
`execute_and_record_marshaled` before it validates the final declared output
path. A path escape is structurally refused by `live_output_path`, but only
after a `started` and a `completed` record claim a completed run. This violates
the coordinator's paired-record/declared-output transaction boundary and makes
a rejected request observable as a completed run inside the live residency.

Repair direction: validate and reserve the declared output path before opening
the record stream, or record a distinct safely-defined failure state rather than
completion. Add a kill test that a path-escape request creates neither records
nor output (or whatever explicitly ratified failure-accounting contract is
implemented).

### F3 — W-2 wages are assigned the taxable-interest quantity

**Classification: blocking.**

`tools/generate_frrs_t4_content.py:49` and the generated immutable
`packages/content/tax/2025/w2.bundle.v2.json` pin
`tax.us.2025.w2.box1-wages` to `tax.us.2025.quantity.taxable-interest`.
The Track-4 charter requires a wages quantity vocabulary and ADR-0028 makes
quantity identity the basis of same-quantity aggregation/force-declare checks.
The vocabulary lists `wages` separately, so this is a semantic mislabelling of
the new W-2 source amount even though the current validator accepts it.

Repair direction: publish the correct immutable wages quantity citizen/pin (and
the dependent package, registry, release, and adoption bytes) or otherwise use
the ratified representation that unambiguously identifies wages. Add a semantic
golden proving W-2 and taxable-interest inputs are not treated as the same
quantity merely because they share a vocabulary container.

## Verification

- `python3 -m unittest tests.test_frrs_t4_w2_live_integration tests.test_frrs_t3_resolver_bootstrap -v` → **40 tests passed**.
- `python3 -m unittest` → **413 tests passed** (discovered count 413).
- Available `mypy` 2.1.0 executable over `packages tools tests` → **Success: no issues found in 88 source files**. The repository `.venv` is stale in this environment (its launcher references a missing interpreter), so its documented invocation could not run; the available executable completed the same target set.
- `python3 tools/governance_lint.py` → **governance lint: conformant**.
- `git diff --check 6858ad7..c39a79b` → clean.

## Recommendation

Do not merge Track 4 until F1–F3 are repaired and independently re-reviewed.
No scope defect, production condition, or non-blocking finding is recorded in
addition to those blockers.
