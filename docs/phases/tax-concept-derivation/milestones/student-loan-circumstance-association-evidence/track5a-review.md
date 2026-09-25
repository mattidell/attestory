# Track 5a — independent review record

- Reviewer: independent sonnet sub-agent, fresh context, read-only, 2026-09-24. Grok was not used: its
  build credit was exhausted during the first 5a dispatch, which wrote no files; the unit was rebuilt by a
  sonnet builder.
- Verdict: **pass, no defects.**
- Schema protocol: v11 = v10 + `subject`, `joined`, `direction`, `dependentRequired`; v32 = v31 + v11
  admission, the same shape v31 used over v30; `published.json` adds exactly two entries;
  `tests/test_schema_registry.py` 14 passed.
- Static checks: pin resolution only against fact-type members; containment by identity-key names in the
  declared direction, nothing weaker; `link_coverage` rules must declare `joined` = `links` and
  `joined_contains_subject`. No runtime or scheduling behaviour. Existing `_link_coverage_issues` already
  rejects a node in `when` and more than one `value` node.
- Admission parity: every v10 set in the assigned modules admits v11 with identical `link_coverage` edges.
  `runner.py`'s two v10 sets are untouched by design — Track 5b.
- Tests: 22 new, all v11 on v32; legacy probes untouched. The foreman's addition of v32 to the
  `rule-artifact.v7` enumeration in `tests/test_later_year_basis_reuse_track0.py` is correct (v32 is also
  outside the collect-target guard's v17 allowlist).
- Verification (reviewer's own run): full suite 2245 passed, 20 skipped; mypy clean (278 files); governance
  lint conformant; `git diff --check` clean.
- Questions, not defects: the runner's v11 admission is 5b scope; ADR residual 1 (a weak declaration passes
  containment) is asserted as a residual.
