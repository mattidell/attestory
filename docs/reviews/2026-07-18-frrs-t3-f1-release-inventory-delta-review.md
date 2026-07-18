# First Real Return Slice — Track 3 F1 Release-Inventory Repair — Delta Review

Reviewer: owner-authorized, author-independent delta reviewer. Date:
2026-07-18. Branch: `repair/frrs-t3-f1-release-inventory`. Reviewed delta:
`b31bc46` → `0001e74` (one implementation commit). Charter:
`docs/reviews/charter-2026-07-18-frrs-t3-f1-release-inventory-delta-review.md`.
Original finding: F1 in
`docs/reviews/2026-07-18-frrs-t3-resolver-bootstrap-premerge-review.md`.
This review does not alter implementation, contracts, fixtures, or merge state.

## Verdict

**Merge-ready.** The narrow repair closes F1: a schema-invalid release document
with the adoption-pinned identity is excluded from the inventory rather than
raising `SchemaValidationError`. A separately checksum-pinned, schema-valid
release remains the only authority. When no valid release remains, resolution
returns a typed `Refusal`.

No blocking, scope, production-condition, or non-blocking findings were found
in this delta. Existing findings F2/F4/F5/F6 and Track-4 production conditions
were outside this review's authorized repair scope and were not reopened.

## Evidence

- Scope: `git diff --name-status b31bc46..0001e74` shows only
  `packages/derivation/production_resolver.py` and
  `tests/test_frrs_t3_resolver_bootstrap.py`. The runtime change imports and
  catches the specific `SchemaValidationError` while inventorying matching
  release candidates; the executed golden explicitly omits the required
  `package_registry_sha256` from an identity-matching candidate. No ADR,
  schema, fixture/generator, package-content, F2/F4/F5/F6, or Track-4 files
  enter the delta. `git diff --check b31bc46..0001e74` is clean.
- `python3 -m unittest tests.test_frrs_t3_resolver_bootstrap` → **31 tests
  passed**.
- `python3 -m unittest` → **passed** (full suite).
- `python3 -m mypy packages tools tests` → **Success: no issues found in 86
  source files**.
- `python3 tools/governance_lint.py` → **governance lint: conformant**.
- Data-safety scan of `git diff b31bc46..0001e74` for absolute local paths,
  ignored personal-data locations, and SSN-like values → **no matches**.

## Independent Counter-Probe

Using the clean current interest-slice adoption and a temporary publication
surface, I placed a JSON object that shared the pinned release `id` and
`version` with the honest release but omitted required
`package_registry_sha256`.

- With the invalid candidate plus the honest pinned release, resolution returned
  `ResolvedGraph` (`ok=True`), with no exception.
- With only that invalid identity-matching candidate, resolution returned
  `Refusal` (`ok=False`, `RELEASE_ABSENT_OR_MISMATCH`), with no exception.

The existing forged-release and replaced-registry focused kills also executed
in the 31-test focused suite and passed, preserving authority behavior.

## Recommendation

The F1 repair is merge-ready. The owner may merge the repair branch; no
contract redesign or further repair is needed for this finding.
