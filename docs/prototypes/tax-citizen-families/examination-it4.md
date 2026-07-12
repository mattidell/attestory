# Examination — Iteration 4 (bounded integration proof)

Builder seat: `roles/builder.md` (iteration 4). Branch:
`prototypes/tax-citizen-families/it4`. This iteration adds no tax coverage. It
determines whether the useful it3 contract decisions operate through the
**ratified authoritative boundaries** — not fixture booleans or harness-local
helpers, the it3 failure mode the round-2/disposition review identified.

Two commands reproduce everything:

```
PYTHONPATH=. python3 docs/prototypes/tax-citizen-families/it4/tools/harness.py      # I1-I9, 92 checks, exit 0
PYTHONPATH=. python3 docs/prototypes/tax-citizen-families/it4/tools/regression.py   # it3 goldens, 14 scenarios, exit 0
```

**Evidence closeout (final pass).** The initial it4 build left four charter
requirements demonstrated by harness gates but thin on *committed* or
*both-direction* evidence; this pass closes them, all green: I4 mixed-year
negatives now cover **fact types, citations, symbol bindings, and scenario
provenance** (not only rules/parameters/form fields); I7 rejects a **wrong-year
citation in both directions**; I8 adds **committed positive/negative example
files** for projection adoption/pins, correction/supersession, package
membership, provenance resolution, coverage reconstruction, and explanation
termination (harness section `I8b`); and I9 adds bypass probes for a
**hard-coded coverage map** and a **hard-coded explanation input index**.

Captured output: `it4/EVIDENCE.txt`. Section headers in the harness output
(`=== I1 ===` …) locate each gate's checks.

## The ordinary authoritative path

`it4/tools/integration.py` builds a real synthetic `Workspace` over the ratified
kernel `ActLog` (combined published registry). Per scenario it: (1) appends
`bundle-adoption`, `entity-introduced`, `evidence-submitted`, and `assertion`
acts; (2) projects current findings through the kernel projection — which
**enforces** the elective⟺basis rule and fact-lattice existence; (3) assembles a
`RunContext` from that projection through the **adopted package's** members and
the declared symbol bindings; (4) calls `run_and_record` (adoption gate on)
against a persisted `RecordStream`; (5) appends publications to the act log; and
(6) reads current/displaced findings through `projection.workspace_currency`
(ADR-0010). Every gate below is exercised on this path; no gate is closed by a
helper the ordinary path does not use.

## Disposition summary

Eight gates **closed with end-to-end evidence**; **I2 is closed for the symbol
projections and ESCALATED for the `closed_sets` set-membership projection** (a
ratified-runner limitation, with a committed minimal failing test). No gate is
closed by prose.

## I1–I9 checklist

| Gate | Disposition | Evidence (harness section / path) | Authoritative component exercised |
|---|---|---|---|
| **I1** authoritative materialization | closed | `harness.py` §I1; `integration.py` `materialize`/`project_run_context` | kernel `ActLog` + `findings.project` (elective⟺basis, fact existence) |
| **I2** adopted + pinned projections | **closed (symbols) + ESCALATED (closed_sets)** | `harness.py` §I2 (a)(b)(c); `content/rules.2025.json` `us.rule.proj.*`; `spikes/integration-substrate.md` | adopted package assembly + runner pins; **ratified `evaluator.collect`/`closed_sets` for the escalation** |
| **I3** W-2 correction lifecycle | closed | `harness.py` §I3 | `currency.compute_currency` (same-fact correction) + `projection.workspace_currency` (derivation edge) |
| **I4** closed package + provenance joins | closed | `harness.py` §I4 | `package_validation.validate_package` (scope cross-check) |
| **I5** record-derived coverage | closed | `harness.py` §I5; `coverage_from_record` over the persisted record | `records.RecordStream` (actual completion record) |
| **I6** record-grounded explanations | closed | `harness.py` §I6 | derived-finding pins + persisted `RecordStream` + kernel value_schema |
| **I7** citation semantic attachment | closed | `harness.py` §I7; `content/citation-resolver.v1.json`; `instances/negative/citation-attachment.*` | versioned resolver contract on the validation path |
| **I8** relationship examples | closed | `harness.py` §I8 + §I8b; `instances/positive`, `instances/negative`, `instances/expected.json` | published/it3 schemas + fact value_schema + resolver + `validate_package` + `coverage_from_record` + real pins |
| **I9** bypass resistance | closed | `harness.py` §I9 | runner-over-projection, adopted package, `run_and_record` adoption gate, citation resolver |

## Gate detail (what makes each non-tautological)

**I1.** The run consumes only real projected findings: §I1 asserts every
`RunContext` input/source id is a current finding projected from the act log, and
that `wage-sources.closed` / `std-ordinary-eligible` / `ordinary-tax-method`
reach the runner **only as derived projections published in the run**, never as a
fixture boolean. `line16 = 3011` is computed through the full path.

**I2 — closed for symbol projections.** The five `us.rule.proj.*` rules are
package members. §I2(a) shows each projected symbol's derived finding **pins its
adopted projection rule and its attested finding**. §I2(b) **withholds**
`us.rule.proj.interest-closed` from the adopted package → line 2b blocks: the
adopted projection is load-bearing on the ordinary path.

**I2 — ESCALATED for `closed_sets`.** §I2(c): with the closure finding *and* its
projection rule present, withholding the `closed_sets` projection makes the
empty-set path block `SOURCE_SET_UNCLOSED`. `closed_sets` is a bare
`frozenset[str]` field of `RunContext` that no rule can produce and no pin
captures, so this projection **cannot be adopted or pinned through the ratified
runner** (`evaluator.collect`). Closing it requires teaching the ratified runner
to read closure findings natively — a `packages/` change, out of bounds for this
seat. This is the same gap it3's R3 named, now proven end-to-end. **Not
simulated.** See `spikes/integration-substrate.md`.

**I3.** An original two-slip run publishes `line 1a = 42000`. A correction
finding for the **same fact identity** (same employer/year/W-2-slip entity) is
asserted; `workspace_currency` then shows the original W-2 finding displaced by
same-fact correction (kernel currency) and the run-1 `line 1a` derived finding
displaced along the derivation edge (ADR-0010) — while the second slip's fact is
untouched (distinct W-2-slip entity). Re-derivation publishes `line 1a = 47000`.
Evidence ids remain separate from findings throughout.

**I4.** `validate_package` proves closure/unique-output over the member corpus;
scenario→package→rules→form-fields→citations and fact-type→symbol joins resolve;
the 2026 package validates as a later-year positive. Mixed-year negatives now
span **every included citizen kind**: rules and parameters (`SCOPE_MISMATCH` in
both directions via `validate_package`); form fields (a 2026 field binding a 2025
symbol); **fact types** (a 2026 wage finding is asserted into a 2025 workspace
and the tax-year join excludes it from the run, so `line 1a` stays 42000 — proven
on the path); **citations** (a 2025 form field citing a 2026 citation); **symbol
bindings** (a 2026 symbol in the 2025 bindings); and **scenario provenance** (a
2025 scenario naming the 2026 package).

**I5.** Coverage is read from the **actual `derivation-record.v1`** emitted by
`run_and_record` (the persisted `RecordStream`), not a hand-built dict: interest
OPEN, wage CLOSED from the `unclosed_interest` record; a contradictory stored
"closed" projection is ignored. Integration finding: an invalid source **value
never becomes a finding** — the kernel value_schema rejects it at projection — so
coverage cannot see a phantom source.

**I6.** Present-zero and closure-backed-zero walks terminate at real pins to
attested findings (the closure-zero walk chains line 2b → the derived
`interest-sources.closed` → the attested closure finding). The no-source and
false-guard states terminate at the **persisted record** (a block missing the
closed symbol; an inapplicable disposition with `guard_result=false`). The
invalid-source state terminates at the **kernel value_schema** (E9.1). Removing
the real closure finding makes the closure-zero walk incomplete (line 2b not
published).

**I7.** `content/citation-resolver.v1.json` is a versioned contract invoked by
the validation path (`resolve_attachment`). It rejects wrong line, **wrong year
in both directions** (expected 2026 / citation 2025, and expected 2025 / citation
2026), wrong content role, and a valid citation attached to the wrong subject —
all committed as negatives under `instances/negative/`.

**I8b — committed relationship examples.** Each new/changed it4 relationship has
a committed positive and negative example file, each checked by a real authority
(not a harness mutation): projection adoption/pins
(`rule.projection*.json`, checked by the value-refs⊆requires pinnability rule);
correction/supersession (`finding.w2-correction*.json`, checked by same-fact
identity); package membership (`package-member.*.json`, checked by
`validate_package` `ROLE_MISMATCH`); provenance resolution
(`scenario.dangling-package.json`, checked against the known package set);
coverage reconstruction (`coverage.{expected,stale}.json`, checked against
`coverage_from_record` over the actual persisted record); and explanation
termination (`explanation.{closure-zero.expected,fabricated}.json`, checked
against the real pins of the derived projection).

**I9.** Each it3 bypass is attempted and rejected, naming the component: a
fixture boolean without an asserted finding → runner blocks the projection rule
and line 2b; an unpinned projection (rule withheld from the package) → line 12
blocks; an unresolved provenance package id → `run_and_record` adoption gate
raises `AdoptionError`; a schema-valid but semantically wrong citation → the
resolver rejects it; a **hard-coded coverage map** claiming all-closed → the
record-derived consumer ignores it and reports interest OPEN; and a **hard-coded
explanation input index** → the walk still terminates at the real pinned finding
and the fabricated id never appears, because structure comes from the
derived-finding pins, not the index.

## it3 → it4 change inventory

**Per-artifact / per-family.**

| Artifact | Change | Reason |
|---|---|---|
| `schemas/{form-field,source-citation,citation-attachment,symbol-binding,scenario}.v1` | reused unchanged | the it3 citizen families are sufficient; it4 tests their operation, not their shape |
| `content/bundle.tax-2025.json` | **rewired** | closure/eligibility/method value_schemas → scalar boolean; the op vocabulary has no field access, so an adopted projection rule can only read a scalar (I1/I2) |
| `content/rules.2025.json` | **rewired (added 5)** | `us.rule.proj.*` adopted projection rules publish the symbols the tax rules read (I2) |
| `content/package.tax-2025.json` | **rewired** | +5 projection-rule members so the projections are in the adopted scope (I2) |
| `content/symbol-bindings.2025.json` | **rewired** | the closure/eligibility/method bindings now name the raw attested-finding input; the projection rule produces the downstream symbol (I2/legibility) |
| `content/citation-resolver.v1.json` | **added** | versioned resolver contract for the validation path (I7) |
| `content/closure-projection.md` | reused | the R3/I2 `closed_sets` escalation contract |
| `content/parameters/*`, `content/form-fields.2025.json`, `content/citations.2025.json`, `content/citation-attachments.2025.json`, `content/evolution/*` | reused unchanged | tax content frozen (charter) |
| `fixtures/scenarios.json`, `scenarios.2026.json` | reused unchanged | `scenario.v1` provenance already sufficient |
| `instances/positive/finding.{closure-attested,std-eligibility}.json` | **rewired** | values → scalar boolean to match the rewired facts |
| `instances/negative/citation-attachment.{wrong-role,wrong-subject,wrong-year-reverse}.json` | **added** | I7 requires wrong-role, wrong-subject, and both wrong-year directions |
| `instances/{positive,negative}/rule.projection*.json`, `finding.w2-correction*.json`, `package-member.*.json`, `scenario.dangling-package.json`, `coverage.{expected,stale}.json`, `explanation.{closure-zero.expected,fabricated}.json` | **added** | I8 committed relationship examples (projection pins, correction, membership, provenance, coverage, explanation) |
| `instances/expected.json` | rewired | registers the new attachment negatives |
| `tools/integration.py` | **added** | the authoritative-path adapter (charter-permitted throwaway integration adapter) |
| `tools/harness.py` | **rewired (replaced)** | the it3 schema/`run()` harness is replaced by the I1-I9 authoritative harness |
| `tools/regression.py` | **added** | the it3 golden regression over the authoritative path |
| `spikes/integration-substrate.md` | **added** | authoritative-path design + I2 escalation |
| `spikes/closure-semantics.md` | reused | it3 closure decision (now with corrected scalar shape) |

**Gate matrix (change → gate → evidence → command).**

| Change | Gates | Evidence | Command |
|---|---|---|---|
| scalar closure/elig/method facts | I1, I2 | §I1, §I2(a) | `harness.py` |
| 5 adopted projection rules | I2 | §I2(a)(b) | `harness.py` |
| package +5 members | I2, I4 | §I2(b), §I4 | `harness.py` |
| symbol bindings rewire | I1, I4 | §I1, §I4 | `harness.py` |
| citation-resolver.v1 + 2 negatives | I7, I8, I9 | §I7, §I8, §I9 | `harness.py` |
| integration adapter | I1–I6, I9 | all sections | `harness.py` |
| regression harness | semantic-loss guard | regression output | `regression.py` |
| closed_sets escalation note | I2 | §I2(c), `spikes/integration-substrate.md` | `harness.py` |

**Retained only for regression / scope, not new it4 evidence.** The it3 fixtures
`invalid_source_value` and `itemize_true` are *not* run through the authoritative
path (the kernel rejects the invalid value at assertion, I5/I6; itemized amounts
are out of scope): they are skipped by `regression.py` and their states are shown
by dedicated gates. The `content/evolution/` 2026 slice is used for I4 scope
checks only, not an authoritative 2026 run.

## it3 conclusions that remain supported

- **fact-type.v1 sufficiency (it3 Q1):** supported — every tax fact type,
  including the rewired scalar closures, conforms to the unchanged kernel
  `fact-type.v1`, and the kernel accepts them through real assertion acts.
- **first-class form fields, inert citations, box-as-identity-key, versioned
  evolution:** supported — unchanged and exercised through joins (I4) and the
  authoritative run (I1).
- **closure as an attested determinable fact (it3 R2):** strengthened — now
  asserted through a real act with the kernel enforcing determinable⟺non-elective
  basis, and projected by an adopted rule (I2).
- **closure-backed zero pins the closure assertion (it3 R3):** strengthened — the
  pin chain is now real, from line 2b through the derived projection to the
  attested finding (I6). The `closed_sets` machinery dependency it3 flagged is
  confirmed load-bearing and escalated (I2).

## Escalations for owner / governance

1. **`closed_sets` cannot be a pinned, adopted projection (I2).** The ratified
   `evaluator.collect` gates empty-set publication on a bare `frozenset` no rule
   produces. Making closure natively runner-read is a `packages/` decision.
   Minimal failing test: `harness.py` §I2(c).
2. **Runner fragility (observation).** A rule whose guard passes but whose value
   refs a symbol that was never provided or published raises `KeyError` in
   `runner.pins_for` rather than a contained block. it4 avoids it by keeping
   itemized amounts out of scope; a conforming corpus should `require` every
   symbol its value refs. Not exercised as a gate; noted for the machinery owner.
3. **Value validation timing (observation).** The kernel validates a finding's
   value against its fact-type value_schema at **projection**, not at act append;
   an invalid value can be appended but poisons the projection. A conforming
   intake path must pre-validate before appending the assertion act. Demonstrated
   in I5/I6 (`invalid_rejected_at_projection`).

## Exhibit index

`it4/README.md` maps the tree. Adapter + harness + regression: `it4/tools/`.
Design + escalation: `it4/spikes/integration-substrate.md`. Captured runs:
`it4/EVIDENCE.txt`.
