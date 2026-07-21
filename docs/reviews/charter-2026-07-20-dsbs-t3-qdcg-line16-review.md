# Charter: Track 3 — Line 16 under D2 — Author-Independent Pre-Merge Review

Date: 2026-07-20. Prepared by the foreman; the owner dispatches this seat
(ADR-0034). The reviewer is author-independent: it reads this charter, the
Track 3 build charter (`docs/reviews/charter-2026-07-19-dsbs-t3-qdcg-line16.md`),
ADR-0038 (and its cited prototype evidence — `docs/prototypes/qdcg-worksheet/repair2/design.md`,
`docs/prototypes/qdcg-worksheet/reviews/confirmation-r2.md`), ADR-0037,
ADR-0035, ADR-0036, and the branch `track/dsbs-t3-qdcg-line16` — not the
authoring session's self-report. Treat the branch as the sole source of
truth.

## Object under review

The delta `ebec569..track/dsbs-t3-qdcg-line16` (charter itself is `ebec569`):
`3b3db78` (bidirectional declaration/signal contradiction interlock,
kernel), `a0574a5` (tax registration of the box-2a contradiction rule),
`7732cc5` (QDCG worksheet line-16 v2 successor content and the two
declared-absence citizens), `f12e7a1` (goldens, admission guards, interlock
kill-tests). Confirm this commit list is exhaustive and in this order —
don't take it on faith.

## Falsifiable checks

### 1. Declared-absence fact-type citizens (deliverable 1, `7732cc5`/`f12e7a1`)

Read `packages/content/tax/2025/qdcg.bundle.json`. Confirm both
`tax.us.2025.capital-gain-distributions` and
`tax.us.2025.schedule-d-required` are bundle-adopted (not bare
`fact-type.v2` members — confirm against Track 2's precedent for what
"bare" would look like and that this delta avoids it), categorical
`{yes, no}` domain, no default, presence-before-value.

**Named finding to investigate, not pre-judged:** the builder self-reported
scoping the new package-admission domain guard
(`CONDITIONAL_DEPENDENCY_MEMBER_NOT_YES_NO` in `package_validation.py`) to
fire only on `conditional_dependency_set` members the rule *also*
references via `category_literal`, rather than on every CDS member
unconditionally — stating a blanket check broke ADR-0037's own generic
numeric-member goldens from Track 0a. Read the guard implementation and
confirm: (a) the scoping claim is accurate (a blanket version really would
break named Track 0a goldens — reproduce or cite the specific test), (b)
the scoped guard still genuinely rejects a non-`{yes,no}` domain for these
two citizens with a real negative test (not vacuous), (c) this doesn't
silently under-enforce for some other CDS member that also deserves the
check but isn't `category_literal`-referenced — is there a case ADR-0038
implies should be caught that this scoping misses? This is the single
highest-priority judgment call in this delta; give it real scrutiny rather
than accepting the builder's stated rationale.

### 2. Line-16 `rule-artifact.v3` successor and package pin (deliverable 2, `7732cc5`)

Read `packages/content/tax/2025/rule.form1040-line16.v2.json`. Confirm:
exactly one versioned successor owns line 16 (no dual producers, no
`conflict_semantics` selector); the `conditional_dependency_set` guard node
is first and unconditionally in the outer `all` — the exact Repair 2 shape,
not reordered; both declarations `"no"` publishes the worksheet result;
either `"yes"` yields `inapplicable`/`guard_inapplicable` with no new
custom code (grep for any new blocked/walk code this delta might have
added). Confirm the package pin in
`packages/content/tax/2025/package.core-calculations.v6.json` moves the
adopted line-16 producer from v1 to this v2 content citizen, and that
`conditional_dependency_set` is genuinely schema-admissible only under
`rule-artifact.v3` (re-check the schema, don't take the charter's claim on
faith).

### 3. QDCG ladder (deliverable 3, `7732cc5`)

Confirm the ladder is expressed entirely in the closed committed vocabulary
(`choose`/`compare`/`subtract`/`max`/`bracket_fold`/`round`, plus whatever
already-present ops the builder's report claims it reused — verify each
claimed op actually pre-dates this branch, i.e. is not newly added here).
Confirm qualified dividends of zero reaches the existing ordinary-bracket
computation unchanged, reading neither declaration — verify via the actual
pin/access log in a golden run, not by static inspection of the rule file
alone.

### 4. Bidirectional admission-locus contradiction interlock (deliverable 4, `3b3db78`/`a0574a5`)

Read `_enforce_...` (or equivalent) in `packages/kernel/findings.py` and
the new `registry.declaration_signal_contradictions`-style mechanism in
`packages/kernel/schema_registry.py`. Confirm the mechanism is generic
(reads a registry-declared pair, no tax-domain string literal baked into
`packages/kernel/*.py`) and that `packages/tax/loader.py` declares exactly
the one pair (capital-gain-distributions `"no"` vs.
`CAPITAL_GAIN_DISTRIBUTION_RECORDED`). Confirm the three kill-test orders
in `tests/tax/test_dsbs_t3_contradiction_interlock.py` genuinely fail
closed in all three orders (declaration-first, signal-first, same-batch —
read the raise sites, not just each test's final assertion) and that a
violating pair is never recorded (the successor state is never observable
by the caller).

### 5. Structural no-reach-around (deliverable 5, `f12e7a1`)

Confirm the committed test asserts the line-16 successor's content names
neither the `CAPITAL_GAIN_DISTRIBUTION_RECORDED` signal nor the recorded
1099-DIV box-2a fact type anywhere — re-run the grep yourself against
`rule.form1040-line16.v2.json`, don't trust the test's own self-description.

### 6. Collateral fix — `marshal.py` (flagged by the builder, not in the original 5 deliverables)

The builder reports extending `_rule_required_symbols` in
`packages/derivation/marshal.py` so a v3 rule's `when`-embedded declaration
refs (never present in `requires`) reach a live run — stated as "the same
gap Track 2 closed for `attachment-rule.v1`." Confirm: this is genuinely
necessary (without it, does a live run actually fail to observe the
declaration citizens?); it is additive and does not change behavior for
any existing `rule-artifact.v1/v2` citizen (read the diff at the exact
hunk); it is in scope under the charter's boundary clause allowing
additive admission-path changes only where a deliverable requires them —
confirm this fix is actually load-bearing for deliverable 2/4, not
opportunistic drift beyond charter scope.

### 7. Package versioning

Confirm `package.core-calculations.v6.json` is the next distinct version at
a new synthetic scope year (not reusing v5's 2054), that derived
registry/release checksums were regenerated (check
`packages/content/tax/2025/published-packages.json` and the release
fixture diff), and that the adoption fixture
(`adopt-core-v6-current.json`) follows the committed pattern. If
`entrypoints` was used for reachability (Track 2's `dividend-universe.v1`
precedent), confirm it lists the new citizens and that no adjacency-walker
code changed.

### 8. Six named golden classes — authoritative surface

Grep `tests/test_dsbs_t3_line16_coordinator.py` yourself for
`live_coordinate_run` vs `RunContext(`; confirm the one `RunContext(` hit
(`Line16WorksheetValues`, per the builder's report) is genuinely
non-substitutive and docstring-labeled, and cannot be mistaken for
satisfying any of the six mandatory classes on its own. For each of the six
classes (qualified-positive both-"no" publish strictly below ordinary;
qualified-zero reduction with declarations untouched; both-absent walk
naming both; each-absent-alone walk naming exactly one; both present-"yes"
outcomes distinct-from-absence disposition; supersession displacement),
confirm the test actually constructs the claimed scenario and asserts the
claimed outcome — read the test body, not just its name.

### 9. Boundary and data safety

No Schedule D machinery beyond the declaration citizen itself. No 1099-DIV
closure-mapping or live-run/workspace integration (Track 4 territory). No
new evaluator operations (re-verify deliverable 3's claim). No new
blocked/walk vocabulary codes or disposition shapes beyond what's named
above. Ratified ADR-0035/0036/0037/0038 decisions and Track 0a/1/2 citizens
are not reopened except deliverable 4's admission-path addition. Every
fixture/golden is manufactured `demo.*`/`demo-*` data. Run the per-review
safety scan. Never commit `tools/scaffold_live_acts.py` or
`workspace-seed/` — confirm they are still untracked on this branch.

### 10. Verification battery (re-run, not trusted)

On the branch: `.venv/bin/python3 -m unittest`, `.venv/bin/python3 -m
mypy`, `.venv/bin/python3 tools/governance_lint.py`, and
`.venv/bin/python3 tools/envelope_scan.py --range main..HEAD` — all green.
The builder reports 2 pre-existing unittest failures confirmed unrelated
via `git stash`/base comparison at `ebec569` — reproduce that comparison
yourself rather than accepting the claim.

## Verdict

Write `docs/reviews/2026-07-20-dsbs-t3-qdcg-line16-review.md` on the branch
with an explicit `ready` / `not ready` verdict and findings numbered F1…,
each tied to a check above with file/line evidence. The foreman triages
findings; the owner holds the merge (ADR-0030). Merge of this track closes
Track 3; Track 4 (1099-DIV closure content and live-run integration) opens
next and closes the milestone.
