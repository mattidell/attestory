# R4 Independent Re-review — Core Tax Conditions Remediation

Reviewer: owner-launched independent context (not the foreman, not the R1/R2
builder, not supplied their in-progress work). Date: 2026-07-15. Charter:
`charter-2026-07-15-core-tax-conditions-r4-independent-rereview.md`. Branch
under review: `milestone/core-tax-conditions` @ `aab4cfc`; delta measured is
R1 (`85ce351`) + R2 (`351c880`). Measurement note only — no production code,
fixtures, or `main` were modified.

## Verdict

**not ready.**

The remediation *code* is sound: exclusive projection and member-byte
verification both work as required, and I reproduced both properties directly.
But the R1 remediation item's **required ACM-A1 golden is inert** — no test in
the suite executes it — so the decision-blocking PMR-1 property is not guarded
by verification. That is the same "green suite over an unexercised condition"
pattern PMR-3 named, recurring inside the remediation. A `not ready` verdict
stops R5.

## Independent verification run (this branch, this context)

```text
.venv/bin/python3 -m unittest                 PASS  (351 tests)
.venv/bin/python3 -m mypy                      PASS  (76 files)
.venv/bin/python3 tools/governance_lint.py     PASS  (conformant)
```

Additional probes I ran are cited per measurement below.

## Measurement 1 — Exclusive projection (PMR-1 / ADR-0027 decision 7) — **FAIL**

**Mechanism: correct.** `packages/derivation/runners/derive.py:_load_content_fixture`
builds a `(id, version) → citizen` corpus (glob of the package directory plus
fixture-referenced citizens), then calls `validate_package(...)` and projects
**only** `validation.resolved_members` into the runner surface
(`derive.py:83`). `resolved_members` is populated solely from resolved
`package["members"]` pins (`package_validation.py:580`) and is consumed at
exactly one site (`derive.py:83`). Co-located unpinned files land in the corpus
but, absent a pin, never resolve and never project. This replaces the Track-6
fixture composition helper with a real resolved-graph boundary, as R1 required.

**Live proof it holds:** running the golden scenario through the production CLI
—
`.venv/bin/python3 -m packages.derivation.runners.derive --scenario
packages/sample_data/tax/scenarios/acm_a1_unpinned_content/scenario.json --json`
— reproduces the committed `expected/report.json` exactly, and the unpinned
rule's identifiers (`tax.us.2025.unpinned_result`, `unpinned-hack`) appear
**zero** times in the output. `rule.unpinned.json` is confirmed absent from
`package.core-calculations.json`'s 44 member pins.

**Why this still fails the measurement.** The charter requires me to *confirm
the ACM-A1 golden proves* co-located unpinned content cannot affect either
surface. It does not, because **no test executes the golden**:

- `tests/tax/test_track6_integration.py:25` drives scenarios from a hardcoded
  `NAMES` tuple of six scenarios; `acm_a1_unpinned_content` is **not** among
  them (`grep acm tests/tax/test_track6_integration.py` → none).
- `grep -rln "acm_a1_unpinned_content|acm_a1|unpinned" --include=*.py` over the
  whole tree (excluding `.venv`) returns **zero** files.

So the golden's correctness rests on a one-time manual observation, not a
verification guard. Nothing in `-m unittest` fails if the exclusive-projection
boundary regresses (e.g. if someone reintroduces the fixture-composition
helper that projected unpinned content). The decision-blocking property PMR-1
was raised to close is therefore unproven *by the suite* — the exact failure
mode PMR-3 flagged. The R1 charter states "Golden (**required**)"; the
deliverable is present as a fixture but not discharged as a test.

Remedy to clear this: add the `acm_a1_unpinned_content` scenario to the
executed golden set (e.g. `NAMES` in `test_track6_integration.py`, or a
dedicated assertion that its CLI report omits `unpinned_result`), so a
regression of the projection boundary turns the suite red.

## Measurement 2 — Member-byte verification (PMR-2 / ADR-0027 decision 6, PC3) — **PASS**

Every resolved-member path routes through a publication-registry byte check.
`validate_package` (`package_validation.py:215`) computes `citizen_checksum`
over canonical bytes and, for each pinned member, requires an entry in the
publication registry: a missing entry yields `MEMBER_UNPUBLISHED`, a byte
divergence yields `MEMBER_CHECKSUM_MISMATCH`, and in **both** cases the member
is `continue`d — excluded from `resolved`/`resolved_members` and thus never
projected. The behavior is fail-closed: unverified content is never admitted.

- **Sole production caller passes the registry.** `derive.py:69–72` loads
  `load_published_citizen_checksums(...)` from `fixture["package_registry"]`
  and passes it to `validate_package`. `resolved_members` is consumed only at
  `derive.py:83`, so there is no projection surface that bypasses the check.
- **Altered bytes under unchanged `(id, version)` are rejected.**
  `tests/derivation/test_package_validation.py::Parity7MemberVerification`
  mutates a member's bytes while retaining its `(id, version)` and the original
  registry checksum, and asserts `MEMBER_CHECKSUM_MISMATCH`. It exists and
  passes (verified independently, 13 tests OK in that module).
- The other `validate_package` call sites are all in tests and omit the
  checksum argument (the parameter is optional for back-compat); none is a
  production derivation/rendering surface, so this is not a bypass.

Registry checksums live in `published-packages.json` under a `citizens` array
(45 entries) — the ADR-0003 publication-registry pattern PC3 prescribes.

## Measurement 3 — No remediation-created contract hole — **PASS**

- **No second membership authority.** Membership remains the `package["members"]`
  pin set resolved by `validate_package`. R1's corpus glob is candidate
  *supply* only; it never confers membership (unpinned globbed files do not
  project, proven in Measurement 1).
- **No filesystem-path membership authority.** Paths select candidate bytes,
  not members; pins alone decide inclusion.
- **No package-embedded duplicate checksum authority.** R2 records member
  checksums in the `published-packages.json` publication registry, not embedded
  in the package. The lone `package_checksum` field in
  `package.core-calculations.json:90` predates remediation (introduced Track 3,
  `571f0cf`), and `verify_published_package` treats the **registry** entry as
  final authority (`PACKAGE_VERSION_REWRITE`), using the embedded value only as
  a self-consistency guard. Consistent with ADR-0027 decision 3's ban on
  dual-bookkept embedded content checksums.

## Measurement 4 — Verification evidence — **PARTIAL / FAIL**

- **R3 names all three required green commands** — confirmed in
  `2026-07-15-core-tax-conditions-r3-verification.md` (`-m unittest`, `-m mypy`,
  `tools/governance_lint.py`). PASS.
- **R2 focused test exists** — `Parity7MemberVerification` in
  `tests/derivation/test_package_validation.py`. PASS.
- **R1 focused test does not exist as an executed test.** The handoff
  (`docs/foreman-handoff.md:47–48`) states R1 "adds the required ACM-A1 golden"
  and cites `tests.tax.test_track6_integration` as green — implying coverage
  that is not there, since that suite's `NAMES` excludes the scenario. The
  green status of `test_track6_integration` does not exercise the ACM-A1
  golden. FAIL.

## Stop

Per the charter, this `not ready` verdict **stops R5**. The single blocking gap
is narrow and does not require redoing correct work: wire the existing,
already-correct `acm_a1_unpinned_content` golden into the executed suite so the
exclusive-projection property is guarded, then re-verify (R3-style) and
re-review the delta. The foreman triages and charters the follow-up; this note
authorizes no change to `main`.
