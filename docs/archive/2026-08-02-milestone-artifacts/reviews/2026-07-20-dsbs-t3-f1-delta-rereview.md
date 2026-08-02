# Track 3 F1 Delta Re-Review

Date: 2026-07-20

Reviewer: author-independent re-reviewer

Branch: `track/dsbs-t3-qdcg-line16`

Object: `c0731f4..1247b89`, read against the original Track 3 review, Finding
F1, and the F1 remediation charter. This is a delta review only; the original
review's nine passing checks stand unless this delta disturbs them.

## Verdict: **not ready**

F1 is genuinely discharged and the full verification battery is green, but
the delta does not satisfy two literal charter requirements: the selector
still chooses an arbitrary first member among five qualifying package members,
and the requested `c0731f4..1247b89` range includes the intervening remediation
charter in addition to the two test files. No production, Track 3 content,
kernel, marshal, resolver, scaffold, or workspace-seed file was changed.

## Check results

### 1. F1 discharged, not relocated — pass

Both named tests now read `package.interest-slice.json`, construct keys from
its `role == "computation"` members, and compare each candidate body's
`(body.get("id"), str(body.get("version", "v1")))` against those keys before
tampering. They no longer select an unrelated first rule from the content
directory.

I read `packages/derivation/production_resolver.py` directly. Its
`_resolve_member_corpus` indexes candidates under exactly the same identity
shape, `(id, str(body.get("version", "v1")))`, then admits only the body whose
canonical checksum matches the registry-pinned digest. The fix's identity
comparison therefore targets the resolver's actual member-key surface rather
than an invented key.

### 2. Track 3 line-16 rule is excluded — pass

The interest package's computation members are the five v1 rules listed at
`packages/content/tax/2025/package.interest-slice.json:33-37`. The new
`rule.form1040-line16.v2.json` has identity
`(tax.us.2025.rule.form1040-line16, v2)`, which is absent from that list. It
would sort before the intended interest rules under the old unfiltered glob,
but the new membership test skips it and selects an actual interest-package
member. Both affected tests pass standalone and return the required
`MEMBER_ABSENT_OR_MISMATCH` refusal after the selected member bytes are
changed.

### 3. Collateral scope — fail as literally written; see R2

`git diff --stat c0731f4..1247b89` reports three files: the remediation
charter plus the two named test files. The actual fix commit `1247b89` itself,
and `git diff --stat c9e8544..1247b89`, contain only the two test files. The
range named by this charter nevertheless includes `c9e8544`, so the exact
two-file assertion does not hold. Direct path checks show no DSBS/Track 3
content, schema, kernel, `marshal.py`, resolver implementation,
`tools/scaffold_live_acts.py`, or `workspace-seed/` change.

### 4. Original test intent — pass

The original refusal assertions and reason strings remain unchanged:

- T3 asserts `Refusal` and `MEMBER_ABSENT_OR_MISMATCH` after adding
  `"_tamper": "changed bytes"` to the selected body.
- T4 asserts `Refusal` and `MEMBER_ABSENT_OR_MISMATCH` after adding
  `"_tamper": true` to the selected body.

The mutations are genuine byte changes. The targeted tests reach the resolver
member-admission refusal, not a weakened assertion or a different early exit.

### 5. New selection fragility — fail as literally written; see R1

There are five qualifying computation members, not one. Both tests iterate
`sorted(...glob("rule.*.json"))` and break on the first membership match.
That is deterministic on the current surface, and any of the five members is
semantically sufficient to trigger the same checksum refusal, but the
tie-break is still an arbitrary lexicographic-first choice rather than a
principled named member selection. A future same-key candidate or a package
member/file-layout change could move the selected path without proving that
the intended verified body was the one mutated. This is a residual instance
of the order-sensitive assumption the charter explicitly asks this re-check
to rule out.

### 6. Boundary and data safety — pass

The delta contains only test-selection code/comments and synthetic tamper
markers. No real value, workspace path, personal identifier, or new refusal
text entered the delta. The required per-review safety scan was clean:
`.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` exited 0.
The owner-held scaffold and workspace-seed paths were untouched.

### 7. Verification battery — pass

All commands were run independently on this worktree:

- `.venv/bin/python3 -m unittest` — `Ran 541 tests in 121.789s`, **OK**.
- `.venv/bin/python3 -m mypy` — **Success**, no issues in 102 source files.
- `.venv/bin/python3 tools/governance_lint.py` — **conformant**.
- `.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — exit 0,
  no findings.
- The two previously failing tests alone — `Ran 2 tests`, **OK**.

## Findings

### R1 — Arbitrary first among five qualifying members — blocking for this charter

The remediation corrected the original unfiltered-directory defect, but both
copies of the new logic still choose the lexicographically first member from
five eligible computation rules. Membership makes the current test pass, and
the current result is repeatable, but it does not establish a principled
target identity. The selector should use one explicit package-declared target
(or another charter-justified canonical tie-break) rather than another
implicit “any first match” convention. No fix was made in this review.

### R2 — The chartered range is not a two-file range — blocking for this charter

The literal `c0731f4..1247b89` diff includes `c9e8544`'s required remediation
charter, so its stat is three files rather than exactly the two test files.
This is process/documentation scope, not a production collateral change, but
it fails the delta check as written and must be reconciled by the owner before
the review can report every charter item satisfied.

## Combined Track 3 conclusion

The original review's nine passing checks remain undisturbed, and F1's
functional regression is fixed. The two residual charter findings above keep
Track 3 as a whole **not ready** for its review gate. The owner holds any merge
decision; this review made no implementation or content changes.
