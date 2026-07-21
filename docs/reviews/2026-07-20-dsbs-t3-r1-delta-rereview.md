# Track 3 R1 Fix Delta — Final Independent Re-Review

Date: 2026-07-20

Reviewer: author-independent re-reviewer

Branch: `track/dsbs-t3-qdcg-line16`, at `cf08e37` (this review's own commit
follows). Object under review: commit `c1cd01f` alone, following
administrative charter commit `1636110` (a charter file only — not part of
the object under review, per this charter's explicit instruction; not
re-flagged as a scope issue).

## Verdict: **ready**

R1 is genuinely discharged. Both named tests now select one explicit,
named target member (`tax.us.2025.rule.form1040-line2b` v1) located
directly by its known filename, with loud-failure membership and identity
assertions before tampering. No residual first-match-loop pattern remains
in either test. The membership claim is accurate. Collateral scope is
exactly the two named test files. Original test intent (`Refusal` /
`MEMBER_ABSENT_OR_MISMATCH`) is preserved. Boundary/data safety is clean.
The full verification battery passes. **Track 3 as a whole (original
review + F1 fix + R1 fix) is ready for its review gate.** The owner holds
the merge decision (ADR-0030).

## Check results

### 1. R1 discharged — pass

Read `tests/test_frrs_t3_resolver_bootstrap.py::ReleaseRegistrySubstitutions::test_changed_member_bytes_under_honest_registry_refuses`
(lines 216–253) and
`tests/test_frrs_t4_w2_live_integration.py::ResolverCounterProbes::test_member_substitution_has_exact_refusal_and_layout_is_inert`
(lines 368–401) directly.

Both now define `TARGET_ID = "tax.us.2025.rule.form1040-line2b"` and
`TARGET_VERSION = "v1"`, then:

- (a) assert `any(m.get("id") == TARGET_ID and str(m.get("version", "v1"))
  == TARGET_VERSION and m.get("role") == "computation" for m in
  package["members"])`, with failure message
  `f"named target {(TARGET_ID, TARGET_VERSION)} is not a computation
  member of interest-slice"` — this is a genuine membership check, not a
  vacuous one: it inspects the parsed `package.interest-slice.json`
  members list and requires `role == "computation"` specifically.
- File is located directly: `members / "rule.form1040-line2b.json"` (T3)
  and `content / "rule.form1040-line2b.json"` (T4) — by known filename,
  no directory scan.
- `assert target.is_file(), f"named target file missing: {target}"` —
  fails loudly if the file is absent/renamed.
- (b) `assert (body.get("id"), str(body.get("version", "v1"))) ==
  (TARGET_ID, TARGET_VERSION)` with a message reporting both the expected
  and found id/version — fails loudly on a mismatch rather than silently
  substituting another file.

All four assertions are non-vacuous: each references the actual loaded
package/file bodies and would raise `AssertionError` (test would error,
not silently proceed) if the named target were ever missing, renamed, or
reclassified.

### 2. No reintroduced first-match logic — pass

Grepped both files for `for `/`break`/`next(` near the selection code.
Within `test_changed_member_bytes_under_honest_registry_refuses` (T3, ends
line 253) the only `for` is the generator clause `for m in
package["members"]` inside the `any(...)` membership check — not an
iterate-and-break loop; there is no `break` anywhere in this function.
Within `test_member_substitution_has_exact_refusal_and_layout_is_inert`
(T4, lines 368–401) the only `for` is the equivalent `any(...)` generator
clause; no `break`, no `next(`. The old "iterate sorted glob candidates,
break on first membership match" pattern is fully gone from both
functions — not left as dead/unreachable code.

(Other `next(`/`for`/`break` occurrences found by the grep belong to
unrelated tests in the same files — e.g.
`test_changed_package_bytes_under_honest_registry_refuses` at T3 line 259
and various fixture-setup loops in T4 — none inside the two tests under
review.)

### 3. Membership claim is accurate — pass

Read `packages/content/tax/2025/package.interest-slice.json` directly.
Line 37:

```
{ "role": "computation", "schema": "rule-artifact.v2", "id": "tax.us.2025.rule.form1040-line2b", "version": "v1" }
```

`tax.us.2025.rule.form1040-line2b` v1 is genuinely listed with
`role: "computation"`, confirming the fix's citation.

### 4. Collateral scope — pass

`git diff --stat c1cd01f^..c1cd01f` (the single commit's own diff, not
`1636110..c1cd01f`):

```
tests/test_frrs_t3_resolver_bootstrap.py  | 38 +++++++++++++++++--------------
tests/test_frrs_t4_w2_live_integration.py | 37 +++++++++++++++++-------------
2 files changed, 42 insertions(+), 33 deletions(-)
```

Exactly the two named test files, nothing else. No DSBS/Track 3 content,
kernel, `marshal.py`, or resolver implementation file changed.

### 5. Original test intent preserved — pass

T3 (line 253): `self.assertEqual(r.reason, "MEMBER_ABSENT_OR_MISMATCH")`
after `self.assertIsInstance(r, Refusal)` / `assert isinstance(r,
Refusal)`, tampering the target body with `body["_tamper"] = "changed
bytes"`.

T4 (lines 399–401): `self.assertIsInstance(refusal, Refusal)` /
`assert isinstance(refusal, Refusal)` /
`self.assertEqual(refusal.reason, "MEMBER_ABSENT_OR_MISMATCH")`, tampering
with `body["_tamper"] = True`.

Both tamper the genuine bytes of the now-correctly-identified named
target file, and both assertions are unchanged from before the fix.

### 6. Boundary and data safety — pass

`git diff c1cd01f^..c1cd01f -- tools/scaffold_live_acts.py workspace-seed/`
is empty; `git status --porcelain` on those paths is clean — both
untouched. The delta contains only test-selection code, comments, and
synthetic tamper markers (`"_tamper": "changed bytes"` / `True`); no real
value, workspace path, or refusal text beyond the pre-existing
`MEMBER_ABSENT_OR_MISMATCH` reason string entered the delta. Ran the
per-review safety scan: `.venv/bin/python3 tools/envelope_scan.py --range
main..HEAD` exited 0, no findings.

### 7. Verification battery — pass

All re-run independently on this worktree (venv was healthy, no rebuild
needed):

- `.venv/bin/python3 -m unittest` — `Ran 541 tests in 120.050s`, **OK**.
- `.venv/bin/python3 -m mypy` — **Success: no issues found in 102 source
  files**.
- `.venv/bin/python3 tools/governance_lint.py` — **governance lint:
  conformant**.
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — exit 0,
  no findings.
- The two named tests standalone —
  `.venv/bin/python3 -m unittest
  tests.test_frrs_t3_resolver_bootstrap.ReleaseRegistrySubstitutions.test_changed_member_bytes_under_honest_registry_refuses
  tests.test_frrs_t4_w2_live_integration.ResolverCounterProbes.test_member_substitution_has_exact_refusal_and_layout_is_inert`
  — `Ran 2 tests in 0.509s`, **OK**.

## Findings

No findings raised (S1... reserved, none needed). All seven checks pass
outright.

## Combined Track 3 conclusion

The original review's nine passing checks, the F1 fix (checks 1, 2, 4, 6,
7 of the F1 delta re-review), and this R1 fix (all 7 checks above) are
all now verified independently. Track 3 as a whole is **ready** for its
review gate. This review made no implementation or content changes; the
owner holds the merge decision (ADR-0030).
