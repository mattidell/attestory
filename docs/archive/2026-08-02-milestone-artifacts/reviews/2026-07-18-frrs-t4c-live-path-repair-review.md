# First Real Return Slice — Track 4c Live Path Repair — Pre-Merge Review

Reviewer: owner-authorized, author-independent pre-merge seat. Date: 2026-07-18.
Branch: `repair/frrs-t4-record-pin-origin` at `a6d513c`
(`a6d513ce1856e332325b88847c6ec99411747867`). Charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t4c-live-path-repair-review.md`.
Implementation charter:
`docs/archive/2026-08-02-milestone-artifacts/reviews/charter-2026-07-18-frrs-t4c-live-path-repair.md`. Findings under
review: F1–F3 in `docs/archive/2026-08-02-milestone-artifacts/reviews/2026-07-18-frrs-t4-live-path-findings.md`.
Contracts read for this seat: ADR-0009, ADR-0014, ADR-0024/0028, ADR-0027,
ADR-0031/0032/0033, ADR-0034. This review changes no implementation, fixture,
ADR, schema, package content, or merge state.

Review clone: fresh detached worktree at `a6d513c`
(`/tmp/frrs-t4c-review-20260718171951`). The untracked
`tools/scaffold_live_acts.py` was **not** present in the review clone and was
not used. All evidence is synthetic.

## Verdict

**Merge-ready.**

Independent measurement closed F1, F2, and F3 on the live path (act log →
contribution/projection → marshal → coordinator), preserved historical v1/v2
publication and the v2 blocking counter-probes, proved deterministic
regeneration of the new v3/registry/release/adoption pins, and proved that the
new coordinator-from-facts golden fails if any one of F1/F2/F3 is surgically
reverted. Full battery: **433** unittests, mypy, governance lint, data-safety
scan, regeneration idempotence, and envelope-gate verify — all clean.

No blocking or scope-defect finding. One non-blocking claim-accuracy note on
F1’s “strictly additive” wording (see N1). No production-condition finding is
introduced by this delta; pre-existing `SOURCE_SET_UNCLOSED` vs record-schema
enum tension is noted only as out-of-scope context (see Observation).

The review is advisory. The owner decides merge disposition.

## Measurements

### 1. F1 — `derivation-record.v2` pin widening

**Passed** (with non-blocking claim note N1).

Independent JSON Schema probes against the committed
`derivation-record.v2.schema.json` pin `$def`, compared to
`rule-artifact.v2` and to the pre-repair schema at `57cdb64^`:

| Case | Result |
| --- | --- |
| `parameter` role pin | valid under new schema; invalid under pre-repair |
| `input` + `origin: "assertion"` | valid under new; invalid under pre-repair |
| `input` + `origin: "declared_default"` | valid under new; invalid under pre-repair |
| `origin` on `parameter` / `adoption` / `choice` | rejected under new (input-pin conditional) |
| Committed example `packages/sample_data/core_tax_conditions/examples/derivation-record.v2.json` | valid under both pre-repair and new |
| Started record; blocked disposition with only governance / choice / default / composition pins | valid under both |
| Pre-repair `input` pin **without** `origin` | valid under pre-repair; **invalid** under new (`'origin' is a required property`) |

Schema bytes: on-disk SHA-256
`7df9e9c1d8353c4f509e2453879256dfe36f480d8132ed815bd28629968d4e5f` matches
`packages/schemas/derivation/published.json` row
`derivation-record.v2.schema.json`. That is the **only** row changed in
`published.json` relative to `57cdb64^`.

F1 commit isolation (`57cdb64`): only
`packages/schemas/derivation/derivation-record.v2.schema.json` and
`packages/schemas/derivation/published.json`. No release, adoption, or
package-registry byte in that commit.

Live-path confirmation (F2 golden): completed derivation-record pins include
`role: "input"` with `origin: "assertion"` (e.g. rounding and W-2 findings) and
`role: "parameter"` pins; the completed record validates against the widened
schema. Reverting F1 alone causes that golden to fail with
`SchemaValidationError` (`'origin' was unexpected`) when appending the
completion record.

`parameter` and the origin enum/conditional on the record pin `$def` match
`rule-artifact.v2`’s pin `$def` (record retains additional record-only roles
`adoption` / `governance` / `package`).

### 2. F2 — `rounding.convention` on the live path; lines 1a/2b/9/11/12/15/16

**Passed.**

Independent synthetic act log (reviewer-built, not a hand-built `RunContext`;
not the untracked scaffold helper) through `live_coordinate_run`:

- Package adoption: `adopt-core-v3-current.json` (scope year `2052`).
- Bundle adoptions include `core_calculations.bundle.v2.json`, which publishes
  `rounding.convention@v1` with `value_schema: {"enum": ["half_up"]}`.
- Asserted `rounding.convention|tax-year=2025` = `half_up` enters projected
  state (no `unknown fact` rejection).
- Report `stop_reason: saturated`. All seven form-field bindings publish:

  `tax.us.2025.wages.total-w2-box1`, `tax.us.2025.interest.taxable-total`,
  `tax.us.2025.income.total-income`, `tax.us.2025.income.agi`,
  `tax.us.2025.deductions.total`, `tax.us.2025.income.taxable-income`,
  `tax.us.2025.tax.total-tax`
  (form fields line-1a / 2b / 9 / 11 / 12 / 15 / 16).

- Paired records: `started` then `completed`; completion schema-valid; wage
  disposition pins include rounding finding with `origin: "assertion"`.

Counter-probes (historical / negative):

- `adopt-core-v2-current.json` still resolves to `ResolvedGraph`.
- Historical `adopt-core-current.json` (v1) still refuses
  `HARD_GATE_REFUSED` with **8** issues.
- Live v3 act log **without** the rounding assertion: wage rule blocked
  `DEPENDENCY_ABSENT` / `missing: ["rounding.convention"]`.
- Asserting rounding under the pre-F2 v1 core vocabulary still rejects
  `finding references unknown fact: rounding.convention|tax-year=2025`.

Focused suite also passes
`test_v3_live_path_publishes_all_covered_lines_from_recorded_facts` and
`test_v3_without_rounding_preserves_the_named_dependency_block`.

### 3. F3 — W-2 closure with `family-horizon`; negatives; displaced horizon

**Passed.**

Content: `w2.bundle.v3.json` closure fact type
`tax.us.2025.w2.source-closure@v3` identity keys begin with entity
`family-horizon` (`kernel.family-horizon`) plus `tax-year` literal.
`closure-mapping.w2.v3.json` pins that fact type and
`closure_horizon_key: "family-horizon"`. `load_closure_mappings()` selects
mapping version **v3** (highest immutable version). Historical
`w2.bundle.v2.json` / `closure-mapping.w2.v2.json` bytes are unchanged and
still tax-year-only on the v2 closure fact type.

Admission (`resolve_closure_admissions` with v3 mapping, current horizon
`demo.w2.h0`):

| Shape | Admits empty-set? |
| --- | --- |
| single current literal `True` | **yes** |
| absent | no |
| `False` | no |
| displaced horizon (`demo.w2.old` vs current `demo.w2.h0`) | no |
| non-boolean (`"true"`) | no |
| duplicate true findings on same horizon | no |

Live path:

- Empty W-2 family + current true closure → line-1a rule **published**
  (empty-set authority).
- Present wages still publish through aggregation (existing ADR-0014 path).
- v2 bundle + horizon-keyed closure assertion still raises
  `FindingModelError: unknown fact` (former F3 rejection retained).

Displaced-horizon **admission** is the governing refusal (table above). Kernel
`facts_of` only materializes entity-keyed facts for **current** entities, so a
closure asserted against a superseded horizon cannot enter current finding
state as an unknown fact either — consistent with non-admission of displaced
closure authority.

### 4. Immutability and deterministic regeneration

**Passed.**

Unchanged vs merge-base `f977b4d` (among others checked):

- `package.core-calculations.json` / `.v2.json`
- `w2.bundle.json` / `.v2.json`
- `core_calculations.bundle.json`
- `closure-mapping.w2.v2.json`
- `rule.wages-line1a.json` / `.v2.json`
- `family.w2.v2.json`

New immutable generation only: `core_calculations.bundle.v2.json`,
`package.core-calculations.v3.json`, `w2.bundle.v3.json`,
`closure-mapping.w2.v3.json`, registry rows, release checksum, and adoption
pins (including new `adopt-core-v3-current.json`). Adoption/release edits are
checksum pin updates for the regenerated publication surface — not rewrites of
v1/v2 package or citizen bodies.

From a clean review clone:

- `python3 tools/generate_frrs_t4_content.py`
- `python3 tools/generate_frrs_t3_fixtures.py`

→ **no byte drift** against committed content and `packages/sample_data/frrs_t3`.
Focused test `test_generated_v2_bytes_and_track_three_pins_are_current` also
passes.

### 5. Root-cause closure (golden depends on F1/F2/F3)

**Passed.** Named coordinator golden:
`LiveCoordinator.test_v3_live_path_publishes_all_covered_lines_from_recorded_facts`
(and empty-set golden where noted). Baseline: **PASS**.

| Revert | How | Named result |
| --- | --- | --- |
| **F1** | Restore pre-`57cdb64` derivation-record.v2 pin `$def` + published row | Golden **ERROR**: `SchemaValidationError` — `origin` unexpected on input pins when writing completion record |
| **F2** | Strip `rounding.convention` from `core_calculations.bundle.v2.json`, reseal citizen checksum + T3 fixtures | Golden **ERROR**: `FindingModelError: unknown fact: rounding.convention\|tax-year=2025` |
| **F3** | Remove `family-horizon` from v3 W-2 closure identity keys, reseal + T3 fixtures | Golden **ERROR** and empty-set golden **ERROR**: `unknown fact` on `…source-closure\|family-horizon=…` |

After each probe, tree restored; baseline golden **PASS** again.

### 6. Standard battery

| Check | Result |
| --- | --- |
| Focused `tests.test_frrs_t4_w2_live_integration` | **17** passed |
| `python3 -m unittest discover -s tests` | **433** tests, **OK** (~58s) |
| `python3 -m mypy packages tools tests` | **Success: no issues found in 91 source files** |
| `python3 tools/governance_lint.py` | **governance lint: conformant** |
| Regeneration idempotence | clean (no drift) |
| `git diff --check f977b4d a6d513c` | clean |
| Data-safety scan of full delta tip bodies | no absolute local paths, no SSN shapes, no workspace locators; only milestone prose “real W-2” phrasing in docs (not personal data) |
| Envelope gate in review environment | `install_envelope_hooks.py` + `envelope_scan.py --verify` → **installed and verified**; `tests.test_envelope_hooks` **12** passed |

Synthetic-only: no personal data, real-run artifacts, workspace locators, or
hand-built production `RunContext` in the review probes. Scaffold helper not
used and not present in the review clone.

## Findings classification

### Blocking

None.

### Scope defect

None. Delta stays inside the Track 4c fence: pin widening, v3 content cycle for
rounding + W-2 closure/mapping, loader highest-mapping selection, generators,
fixtures, and the missing live golden class. No ADR redesign; no new tax lines
or UI.

### Production condition (owning track)

None **introduced by this repair**. Exit criterion 1 remains an owner-held
milestone condition until merge, as the findings record already states — not a
defect in the repair delta.

### Non-blocking

**N1 — F1 is not purely additive for legacy input pins without `origin`.**
The builder/findings text calls the pin change “strictly widening.” Adding
`parameter` and permitting `origin` on inputs is widening; **requiring**
`origin` on every `input` pin is a concurrent narrowing relative to pre-repair
`derivation-record.v2` (input pins without `origin` were previously valid).
That narrowing correctly aligns the record pin `$def` with `rule-artifact.v2`
and with the v2 runner’s pin emission. No committed derivation-record.v2
fixture with origin-less input pins fails; the live path always emits
`origin` on v2 input pins. **Not merge-blocking.** Owner may optionally tighten
the findings/charter wording from “strictly additive/widening” to “aligned with
rule-artifact.v2 (parameter + input-origin conditional).”

### Observation (out of scope; not a Track 4c defect)

Live coordination of an empty family **without** any closure currently attempts
to record blocked disposition code `SOURCE_SET_UNCLOSED`, which is used in some
scenario reports but is **not** in the `derivation-record.v2` disposition
`code` enum (`SOURCE_SET_OPEN` is). That path raises `SchemaValidationError` on
record append. Pre-existing tension; not required by this charter; empty-set
**with** asserted true closure (F3 repair path) publishes cleanly.

## Recommendation

The Track 4c live-path repair is **merge-ready**. The owner may merge
`repair/frrs-t4-record-pin-origin` at `a6d513c` when ready. Optional follow-up:
N1 wording cleanup; separately track the `SOURCE_SET_UNCLOSED` enum alignment if
desired. This seat does not merge, push to `main`, open GitHub review objects,
or dispatch further agents.
