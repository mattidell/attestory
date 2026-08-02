# Capital-Gain Distributions / Line 7a — Track 3 F1–F3 Repair Recheck

Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-30-capital-gain-distributions-line7a-track3-repair-recheck.md`

Role: original author-independent Track-3 Reviewer, High tier / high effort.
This is a focused delta recheck, not a second broad review.

## Object, posture, and boundary

- Orientation resolved `HEAD` to
  `818cf266d239893c0b6d10c86ccf0893da4ffea9`; `git rev-parse HEAD`
  independently matched it.
- Exact repair range:
  `3b3291307d7a4258a2f5476208e1cecd2c0ed103..202ae9740da7689478f0cb52386f061b4ff01b1d`.
  It contains exactly one commit. The repair commit's parent is exactly
  `3b3291307d7a4258a2f5476208e1cecd2c0ed103`, and the current charter commit
  is its direct successor.
- After `git fetch origin --prune`, the branch was 0 behind and 8 ahead of
  `origin/main`; no merged PR was returned for the branch, so the workspace
  was not spent.
- Evidence ceiling: static projector mutations plus the existing synthetic
  v8/v3 `live_coordinate_run` goldens. No real browser/workspace session,
  real data, contract reopening, or new product surface was used.
- Independence: no Builder thread, rationale, summary, self-assessment, or
  reasoning was consulted. The committed range, projector, tests, content,
  goldens, and credited surfaces were read and measured directly.
- Credited evidence from the original review remains everything outside F1,
  F2, and F3: the Track-3 boundary and live entrypoint; atomic blocked and
  inapplicable states; strict model and write boundary; product/frozen-harness
  rendering, redaction, accessibility, DOM safety, and sibling containment;
  harness parity; prerequisite, Track-2, lifecycle, resolver, confinement,
  and data-safety measurements.
- Stop conditions checked: range/tip/ancestry drift; paths outside the
  projector and focused test; schema, citizen, ADR, tax-rule, field, citation,
  package, release, adoption, resolver, evaluator-operation, caller-result,
  or model-version change; tax-specific projector branching; valid-golden,
  browser-fixture/manifest, page, Track-1/2, admission, lifecycle, package-
  validation, or legacy-path change; weakened test/validator; unattributable
  failure; governance interpretation; and real/private material. None fired.

## 1. Exact range and containment

The one repair commit changes exactly two files:

```text
M packages/derivation/presentation_projection.py
M tests/test_capital_gain_distributions_line7a_t3_presentation.py
```

The projector's four changed regions map entirely to the findings:

| Hunk | Finding / obligation |
| --- | --- |
| Fixed categorical comparison at lines 210–214 | F1 |
| Generic citation identity and owning-rule chain at lines 239–274 | F2/F3 plus legacy-path preservation |
| Duplicate resolved-citation rejection at lines 349–355 | F2/F3 |
| Citation-chain application to numeric and categorical publications at lines 369–370 | F2/F3 |

The focused test additions map to F1 alternate/empty values, F2 categorical
citation mutations, F3 numeric citation mutations, valid atomic numeric and
categorical paths, and the legacy no-citations control. No unrelated cleanup,
schema, content, package, golden, renderer, fixture, manifest, phase pointer,
or process record is inside the repair range.

## 2. F1 — exact fixed categorical publication

At `packages/derivation/presentation_projection.py:210-214`, a fixed
categorical field now requires a string source value exactly equal to the
field's declared `published_value.render` instruction. The accepted return
shape remains `published_categorical` with `act` only; no categorical `value`
is copied into the model.

Independent mutations produced:

```text
ACCEPT categorical checked atomic
REJECT categorical value "no"
REJECT categorical value "unchecked"
REJECT categorical value ""
REJECT categorical value 1
REJECT categorical value None
REJECT categorical value "demo.arbitrary"
```

Each negative reused the otherwise-valid field, rule, citation, state,
publication, and disposition fixture, so rejection is attributable to the
fixed-value comparison rather than an earlier malformed input. The committed
test covers `"no"`, `"unchecked"`, `""`, and a non-string; the independent
matrix additionally covered `None` and another arbitrary string.

**F1 is closed.**

## 3. F2/F3 — generic declared-citation chain

The complete join is generic:

1. `field.binds_symbol` selects exactly one disposition.
2. The disposition's `artifact_id` selects the owning resolved rule.
3. That rule must publish the joined field symbol.
4. If the rule declares a non-empty `citations` list, the field must declare
   one well-formed `(id, version)` citation, the owning rule must declare that
   exact identity exactly once, and the resolved graph must contain it.
5. Every resolved `citation.v1` citizen is indexed before any field projection;
   a duplicate `(id, version)` rejects globally rather than overwriting.
6. A legacy owning rule without a citation declaration returns through the
   established path.

The chain is applied to every accepted numeric or categorical publication at
`presentation_projection.py:369-370`. Direct grep for `line-7a`, `line7a`,
`line-7b`, `line7b`, or `form1040` in the generic projector returned no match.

The independent mutation matrix used otherwise-valid synthetic models and
produced:

```text
REJECT categorical missing field citation
REJECT categorical missing resolved citation
REJECT categorical duplicate resolved identity
REJECT categorical matching wrong field/resolved identity
REJECT categorical matching wrong field/resolved version

ACCEPT numeric valid atomic
REJECT numeric missing field citation
REJECT numeric missing resolved citation
REJECT numeric duplicate resolved identity
REJECT numeric matching wrong field/resolved identity
REJECT numeric matching wrong field/resolved version

REJECT owning rule duplicate exact declaration
ACCEPT legacy owning rule without citations
```

The matching-wrong cases supplied the mutated field's wrong citation citizen
in the resolved graph. They therefore reached and failed the owning-rule
exactness check rather than failing merely because the wrong citizen was
absent. The duplicate-resolved cases reached the global citation index and
failed there. The rule-duplicate case supplied one valid resolved citizen but
declared its exact identity twice in the owning rule, isolating the
exactly-once requirement.

The focused committed tests are honest:

- categorical value failures retain valid lineage and citation inputs;
- missing categorical citation removes only the resolved citation;
- wrong categorical identity/version supplies a matching wrong citizen, so
  the owning rule is the rejecting link;
- duplicate citizens are otherwise byte-equal valid citizens;
- numeric missing, wrong, and duplicate cases share the valid numeric field,
  rule, state, publication, and disposition; and
- the legacy control omits only the owning rule's citation declaration and
  proves successful publication.

`tests.test_presentation_l2_integration` independently confirms that any
`PresentationModelError` propagated through `live_coordinate_run` leaves
neither the result file nor the reserved presentation artifact. Thus every
F1/F2/F3 rejection occurs before a presentation artifact is written.

**F2 and F3 are closed.**

## 4. Valid-output byte identity and credited surfaces

The three Track-3 models were independently regenerated through
`live_coordinate_run`, serialized with the committed generator's exact
format, and compared as bytes:

```text
eligible
  47230 bytes
  sha256 cf0d07cd7722708fb7ec991f04b79968ed8c908ae0eefd7fa0354101121bdb6d
missing-authority
  30791 bytes
  sha256 91492dcad4737f421b37d0b084c81ac4c749333e706e677ad149da940d4da517
schedule-d-required
  30638 bytes
  sha256 f59bb89e01564d04439f8fd92038679e3d3d8feb263e9448123625f98d74edbc
```

All three generated byte strings exactly matched the committed goldens. The
eligible line 7a remains numeric `1500`; eligible line 7b remains atomic
`published_categorical` with no value key; missing-authority remains blocked;
and Schedule-D-required remains guard-inapplicable.

An exact repair-range diff over the established v1/v6 production-shaped
fixture, all three Track-3 goldens, both citation-walk pages, all four
slice-specific browser fixtures, the slice manifest, and
`packages/derivation/live.py` was empty. The projector constant is
`presentation-model.v1` at both endpoints. The repair therefore leaves the
internal model version, valid goldens, renderer pages, browser fixtures,
manifest, live write path, and credited presentation surfaces byte-identical.

## 5. Focused verification

Each charter command was run once:

```text
python3 -m unittest tests.test_capital_gain_distributions_line7a_t3_presentation
# Ran 6 tests in 4.748s — OK

python3 -m unittest tests.test_presentation_l2_integration
# Ran 29 tests in 3.029s — OK

python3 -m unittest tests.test_presentation_live_session
# Ran 15 tests in 15.108s — OK

python3 -m unittest tests.test_capital_gain_distributions_line7a_line7b_prerequisite
# Ran 5 tests in 2.530s — OK

python3 -m unittest tests.test_capital_gain_distributions_line7a_t2_coordinator
# Ran 9 tests in 4.757s — OK

node tools/presentation_harness/run.mjs \
  --manifest tools/presentation_harness/examples/manifests/capital-gain-distributions-line7a.v1.json
# 9 pass, 0 fail, 0 error

git diff --check \
  3b3291307d7a4258a2f5476208e1cecd2c0ed103..202ae9740da7689478f0cb52386f061b4ff01b1d
# clean

python3 tools/governance_lint.py
# governance lint: conformant

python3 tools/envelope_scan.py --range main..HEAD
# clean (exit 0)
```

No full-suite run or real-data operation was performed.

## Verdict

**READY**

F1, F2, and F3 are closed by a generic fixed-categorical equality check,
global duplicate-citation rejection, and one exact field → owning rule →
resolved citizen chain for declared citations, while the legacy no-citations
path remains intact. Independent mutations reject every required malformed
categorical and numeric case for the intended reason, valid output remains
atomic and byte-identical, and all focused credited-evidence and safety checks
are green. No residual finding is recorded.
